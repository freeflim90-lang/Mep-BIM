# MEP·BIM Coordination Console — 개발 핸드오프

> Claude Code 또는 개발팀에게 그대로 전달 가능한 구현 사양서.
> 기준 UI: `ui_kits/console/index.html` (5개 탭 · React + JSX)
> 통합 대상: 기존 Revit Add-in (Point Marker + 3D Section Box + Clash Report 자동 생성)

---

## 0. 한 줄 요약

> **기존 Revit Add-in이 만드는 Point Marker / Section Box / 보고서 데이터를, 본 대시보드가 단일 진실(Single Source of Truth)로 흡수해 충돌·RFI·통합모델·공정·시공확인 5개 영역을 한 화면에서 운영한다.**

---

## 1. 시스템 구성

```
┌────────────────────── Revit (Desktop) ──────────────────────┐
│  [기존 Add-in]                                              │
│   ├─ Clash Detect → Point Marker 자동 생성                  │
│   ├─ Marker → 3D Section Box View 자동 생성                 │
│   └─ Clash Report (PDF/Docx) 자동 생성                      │
│                                                              │
│  [본 사양으로 추가할 모듈]                                  │
│   ├─ ParameterBinder    (Marker ↔ 공유 파라미터 동기)       │
│   ├─ ThumbnailCapturer  (Section Box View 이미지 export)    │
│   ├─ SyncService        (REST PUSH / WebSocket)             │
│   ├─ LocalHttpListener  (localhost:7891 - Jump 명령 수신)   │
│   └─ ExternalEventHandlers (Revit 메인 스레드 작업 큐)      │
└──────────────────────────────────────────────────────────────┘
              │ HTTPS / WSS                  ↑
              ▼                              │
┌──────────────── Backend (Node + PostgreSQL) ────────────────┐
│  Fastify · Prisma · WebSocket(ws) · PDFKit                  │
│   /api/clashes  /api/rfis  /api/models  /api/tasks          │
│   /api/punch    /api/reports  /ws (push)                    │
└──────────────────────────────────────────────────────────────┘
              ▲ HTTPS / WSS
              │
┌─────────────── Frontend (React + Vite) ─────────────────────┐
│  현재 ui_kits/console 디자인을 그대로 프로덕션화            │
│   5개 탭: Clash · RFI · Federation · Schedule · As-built    │
│   APS Viewer 임베드 (3D)                                    │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. 공유 데이터 모델 (TypeScript / C# 양쪽 호환)

### 2-1. Clash (= Revit Point Marker 1개)

```typescript
// shared/types.ts
export interface Clash {
  id: string;                    // CL-2041
  revitUniqueId: string;         // Marker FamilyInstance.UniqueId — 역참조용
  position: { x: number; y: number; z: number };  // mm
  gapMm: number;                 // -42.5 (음수: overlap, 양수: clearance)
  level: string;                 // "LV.04"
  gridRef: string;               // "C-7"
  systemA: { code: string; ko: string };   // { code:"HVAC", ko:"기계 덕트" }
  systemB: { code: string; ko: string };
  severity: "critical" | "warn" | "info";
  status: "open" | "investigating" | "rfi" | "resolved" | "ignored";
  assignedTo: string | null;
  foundAt: string;               // ISO
  resolvedAt: string | null;
  sectionViewId: string;         // Revit View3D ElementId
  thumbnailUrl: string;          // /assets/thumbs/CL-2041.png
  reportUrl: string | null;      // /reports/CL-2041.pdf (Add-in 생성본)
  rfiId: string | null;
}
```

```csharp
// Revit/Shared/ClashDto.cs
public record ClashDto(
    string Id, string RevitUniqueId,
    Vec3 Position, double GapMm,
    string Level, string GridRef,
    SystemRef SystemA, SystemRef SystemB,
    string Severity, string Status,
    string AssignedTo,
    DateTime FoundAt, DateTime? ResolvedAt,
    string SectionViewId, string ThumbnailBase64,
    string ReportUrl, string RfiId
);
public record Vec3(double X, double Y, double Z);
public record SystemRef(string Code, string Ko);
```

### 2-2. RFI · Model · Task · PunchItem (요약)

```typescript
export interface Rfi {
  id: string;                    // RFI-2026-038
  title: string;
  clashIds: string[];            // 묶인 충돌
  from: string; to: string;
  state: "draft" | "review" | "negotiation" | "answered" | "closed";
  dueAt: string;
  attachmentUrls: string[];      // PDF 경로 (Add-in이 생성한 보고서 포함)
  approvals: { role: string; user: string; at: string }[];
}

export interface FederatedModel {
  discipline: "ARCH" | "STR" | "MEP" | "ELEC" | "FP";
  name: string;
  fileName: string;              // ARCH-2026-04.rvt
  version: string;               // "v 12"
  surveyPoint: { n: number; e: number; z: number };
  coordStatus: "aligned" | "drift" | "unlinked";
  driftMm: { x: number; y: number; z: number } | null;
  lastSyncAt: string;
  syncedBy: string;
}

export interface ScheduleTask {
  wbs: string;                   // "2.1"
  name: string;
  discipline: string;
  startWeek: string; endWeek: string;
  percentDone: number;
  predecessors: string[];        // wbs[]
  spatialScope: { levels: string[]; grids: string[] };
  linkedClashIds: string[];      // 자동 매칭
}

export interface PunchItem {
  id: string;                    // PL-2026-018
  title: string;
  discipline: string;
  level: string; gridRef: string; z: number;
  state: "open" | "fixing" | "done" | "rejected";
  registeredBy: string; registeredAt: string;
  assignedTo: string; dueAt: string;
  photos: string[];              // URL[]
  checklist: { label: string; done: boolean }[];
  history: { at: string; by: string; what: string }[];
  linkedRfiId: string | null;
}
```

---

## 3. Revit Add-in (C# / .NET Framework 4.8 · Revit 2022+)

### 3-1. 프로젝트 구조

```
RevitAddin.MepBim/
├─ RevitAddin.MepBim.csproj
├─ MepBim.addin                  # 매니페스트
├─ App.cs                        # IExternalApplication
├─ Shared/
│   ├─ MepBimConfig.cs           # 서버 URL, 토큰
│   └─ ClashDto.cs, RfiDto.cs ...
├─ SharedParameters/
│   └─ MEPBIM_ClashMarker.txt    # 공유 파라미터 정의
├─ Services/
│   ├─ MarkerSerializer.cs       # Marker → ClashDto
│   ├─ ThumbnailCapturer.cs      # View3D → PNG
│   ├─ SyncService.cs            # HttpClient PUSH + WebSocket
│   ├─ LocalHttpListener.cs      # localhost:7891 (Jump 수신)
│   └─ ParameterBinder.cs        # ClashDto → Marker 파라미터 쓰기
├─ Handlers/                     # ExternalEvent — UI 스레드
│   ├─ JumpToMarkerHandler.cs
│   ├─ UpdateParameterHandler.cs
│   └─ RefreshMarkersHandler.cs
└─ UI/
    └─ RibbonTab.cs
```

### 3-2. 공유 파라미터 정의

`SharedParameters/MEPBIM_ClashMarker.txt`:

```
*META    GUID    NAME                   DATATYPE    GROUP
PARAM    e6c3...  MEPBIM_ClashId        TEXT        1
PARAM    e6c4...  MEPBIM_GapValue       LENGTH      1
PARAM    e6c5...  MEPBIM_SystemA        TEXT        1
PARAM    e6c6...  MEPBIM_SystemB        TEXT        1
PARAM    e6c7...  MEPBIM_GridRef        TEXT        1
PARAM    e6c8...  MEPBIM_LevelRef       TEXT        1
PARAM    e6c9...  MEPBIM_Severity       TEXT        1
PARAM    e6ca...  MEPBIM_Status         TEXT        1
PARAM    e6cb...  MEPBIM_AssignedTo     TEXT        1
PARAM    e6cc...  MEPBIM_SectionViewId  TEXT        1
PARAM    e6cd...  MEPBIM_SyncedAt       TEXT        1
PARAM    e6ce...  MEPBIM_RfiId          TEXT        1
```

`Generic Models > MEPBIM_ClashMarker` Family에 binding.

### 3-3. App.cs — 진입점

```csharp
public class App : IExternalApplication {
    public static SyncService Sync;
    public static LocalHttpListener Listener;
    public static JumpToMarkerHandler JumpEvent;
    public static UpdateParameterHandler UpdateEvent;

    public Result OnStartup(UIControlledApplication app) {
        var config = MepBimConfig.Load();
        Sync     = new SyncService(config);
        Listener = new LocalHttpListener(port: 7891);

        // ExternalEvent — 메인 스레드 큐
        JumpEvent   = new JumpToMarkerHandler();
        UpdateEvent = new UpdateParameterHandler();
        ExternalEvent.Create(JumpEvent);
        ExternalEvent.Create(UpdateEvent);

        // 문서 변경 hook — Marker 수정 감지
        app.ControlledApplication.DocumentChanged += OnDocumentChanged;
        app.ControlledApplication.DocumentSaved   += OnDocumentSaved;

        // 리스너 시작 (대시보드 → Revit Jump 명령 수신)
        Listener.OnJump += cmd => JumpEvent.Raise(cmd);
        Listener.Start();

        RibbonTab.Build(app);
        return Result.Succeeded;
    }

    public Result OnShutdown(UIControlledApplication app) {
        Listener.Stop();
        Sync.Dispose();
        return Result.Succeeded;
    }

    private void OnDocumentChanged(object s, DocumentChangedEventArgs e) {
        var modified = e.GetModifiedElementIds()
            .Select(id => e.GetDocument().GetElement(id))
            .OfType<FamilyInstance>()
            .Where(f => f.Symbol.FamilyName == "MEPBIM_ClashMarker");
        foreach (var m in modified) Sync.PushClashDelta(m);
    }
}
```

### 3-4. MarkerSerializer.cs

```csharp
public class MarkerSerializer {
    public ClashDto Serialize(FamilyInstance marker, Document doc) {
        var p   = (marker.Location as LocationPoint).Point;
        var vid = marker.LookupParameter("MEPBIM_SectionViewId").AsString();
        var view = doc.GetElement(new ElementId(int.Parse(vid))) as View3D;

        var thumb = ThumbnailCapturer.Capture(doc, view, 800, 600);

        return new ClashDto(
            Id:             marker.LookupParameter("MEPBIM_ClashId").AsString(),
            RevitUniqueId:  marker.UniqueId,
            Position:       new Vec3(p.X * 304.8, p.Y * 304.8, p.Z * 304.8),
            GapMm:          marker.LookupParameter("MEPBIM_GapValue").AsDouble() * 304.8,
            Level:          marker.LookupParameter("MEPBIM_LevelRef").AsString(),
            GridRef:        marker.LookupParameter("MEPBIM_GridRef").AsString(),
            SystemA:        ParseSys(marker.LookupParameter("MEPBIM_SystemA").AsString()),
            SystemB:        ParseSys(marker.LookupParameter("MEPBIM_SystemB").AsString()),
            Severity:       marker.LookupParameter("MEPBIM_Severity").AsString(),
            Status:         marker.LookupParameter("MEPBIM_Status").AsString(),
            AssignedTo:     marker.LookupParameter("MEPBIM_AssignedTo").AsString(),
            FoundAt:        DateTime.UtcNow,        // 또는 Marker 생성 시 저장
            ResolvedAt:     null,
            SectionViewId:  vid,
            ThumbnailBase64:Convert.ToBase64String(thumb),
            ReportUrl:      null,
            RfiId:          marker.LookupParameter("MEPBIM_RfiId").AsString()
        );
    }
}
```

### 3-5. ThumbnailCapturer.cs

```csharp
public static class ThumbnailCapturer {
    public static byte[] Capture(Document doc, View3D view, int w, int h) {
        var tmp = Path.Combine(Path.GetTempPath(), $"mepbim_{Guid.NewGuid()}.png");
        var opts = new ImageExportOptions {
            FilePath        = tmp,
            ZoomType        = ZoomFitType.FitToPage,
            PixelSize       = w,
            ImageResolution = ImageResolution.DPI_150,
            ExportRange     = ExportRange.SetOfViews,
            HLRandWFViewsFileType = ImageFileType.PNG,
            ShadowViewsFileType   = ImageFileType.PNG
        };
        opts.SetViewsAndSheets(new List<ElementId> { view.Id });
        doc.ExportImage(opts);
        var bytes = File.ReadAllBytes(tmp);
        File.Delete(tmp);
        return bytes;
    }
}
```

### 3-6. SyncService.cs

```csharp
public class SyncService : IDisposable {
    private readonly HttpClient _http;
    private readonly ClientWebSocket _ws;
    private readonly MepBimConfig _cfg;

    public SyncService(MepBimConfig cfg) {
        _cfg = cfg;
        _http = new HttpClient { BaseAddress = new Uri(cfg.BackendUrl) };
        _http.DefaultRequestHeaders.Authorization =
            new AuthenticationHeaderValue("Bearer", cfg.ApiToken);
        _ws = new ClientWebSocket();
        _ = ConnectWs();
    }

    public async Task PushClashes(IEnumerable<ClashDto> clashes) {
        var json = JsonSerializer.Serialize(clashes);
        var resp = await _http.PostAsync("/api/clashes/bulk",
            new StringContent(json, Encoding.UTF8, "application/json"));
        resp.EnsureSuccessStatusCode();
    }

    public async Task PushClashDelta(FamilyInstance marker) {
        // DocumentChanged hook에서 호출
        var dto = new MarkerSerializer().Serialize(marker, marker.Document);
        await _http.PatchAsync($"/api/clashes/{dto.Id}",
            new StringContent(JsonSerializer.Serialize(dto), Encoding.UTF8, "application/json"));
    }

    private async Task ConnectWs() {
        await _ws.ConnectAsync(new Uri(_cfg.WsUrl), CancellationToken.None);
        _ = ReceiveLoop();
    }

    private async Task ReceiveLoop() {
        var buf = new byte[8192];
        while (_ws.State == WebSocketState.Open) {
            var r = await _ws.ReceiveAsync(buf, CancellationToken.None);
            var msg = JsonSerializer.Deserialize<WsMessage>(buf.AsSpan(0, r.Count));
            // 대시보드에서 상태/담당자 변경 → Marker 파라미터 업데이트
            if (msg.Type == "clash.updated")
                App.UpdateEvent.Raise(msg.Payload);
        }
    }

    public void Dispose() { _http?.Dispose(); _ws?.Dispose(); }
}
```

### 3-7. LocalHttpListener.cs — 대시보드 → Revit Jump

```csharp
public class LocalHttpListener {
    public event Action<JumpCmd> OnJump;
    private readonly HttpListener _l;

    public LocalHttpListener(int port) {
        _l = new HttpListener();
        _l.Prefixes.Add($"http://localhost:{port}/");
    }

    public void Start() {
        _l.Start();
        Task.Run(Loop);
    }

    private async Task Loop() {
        while (_l.IsListening) {
            var ctx = await _l.GetContextAsync();
            if (ctx.Request.Url.AbsolutePath == "/revit/show" &&
                ctx.Request.HttpMethod == "POST") {
                using var r = new StreamReader(ctx.Request.InputStream);
                var cmd = JsonSerializer.Deserialize<JumpCmd>(await r.ReadToEndAsync());
                OnJump?.Invoke(cmd);
                ctx.Response.StatusCode = 200;
            }
            ctx.Response.Close();
        }
    }

    public void Stop() => _l.Stop();
}

public record JumpCmd(string MarkerUniqueId, string SectionViewId);
```

### 3-8. JumpToMarkerHandler.cs (ExternalEvent)

```csharp
public class JumpToMarkerHandler : IExternalEventHandler {
    private JumpCmd _pending;
    private ExternalEvent _evt;

    public void Raise(JumpCmd cmd) {
        _pending = cmd;
        _evt ??= ExternalEvent.Create(this);
        _evt.Raise();
    }

    public void Execute(UIApplication app) {
        var uidoc = app.ActiveUIDocument;
        var doc   = uidoc.Document;
        var view  = doc.GetElement(new ElementId(int.Parse(_pending.SectionViewId))) as View3D;
        if (view == null) return;

        uidoc.ActiveView = view;
        var marker = doc.GetElement(_pending.MarkerUniqueId);
        if (marker != null) {
            uidoc.Selection.SetElementIds(new List<ElementId> { marker.Id });
            uidoc.ShowElements(marker.Id);
        }
        // Revit 창을 최상단으로
        System.Diagnostics.Process.GetCurrentProcess().MainWindowHandle.SetForeground();
    }

    public string GetName() => "MEPBIM Jump To Marker";
}
```

### 3-9. UpdateParameterHandler.cs (대시보드 변경 → Revit 반영)

```csharp
public class UpdateParameterHandler : IExternalEventHandler {
    private ClashUpdate _pending;
    private ExternalEvent _evt;
    public void Raise(ClashUpdate u) { _pending = u; _evt ??= ExternalEvent.Create(this); _evt.Raise(); }

    public void Execute(UIApplication app) {
        var doc = app.ActiveUIDocument.Document;
        var marker = doc.GetElement(_pending.RevitUniqueId);
        if (marker == null) return;
        using var tx = new Transaction(doc, "MEPBIM update from dashboard");
        tx.Start();
        marker.LookupParameter("MEPBIM_Status")    ?.Set(_pending.Status);
        marker.LookupParameter("MEPBIM_AssignedTo")?.Set(_pending.AssignedTo);
        marker.LookupParameter("MEPBIM_SyncedAt")  ?.Set(DateTime.UtcNow.ToString("o"));
        tx.Commit();
    }
    public string GetName() => "MEPBIM Update From Dashboard";
}
```

---

## 4. Backend (Node.js + Fastify + Prisma + PostgreSQL)

### 4-1. 프로젝트 구조

```
backend/
├─ package.json
├─ prisma/schema.prisma
├─ src/
│   ├─ server.ts           # Fastify 부트
│   ├─ routes/
│   │   ├─ clashes.ts
│   │   ├─ rfis.ts
│   │   ├─ models.ts
│   │   ├─ tasks.ts
│   │   ├─ punch.ts
│   │   └─ reports.ts      # PDFKit 보고서 빌드
│   ├─ ws/hub.ts           # WebSocket 브로드캐스트
│   ├─ services/
│   │   ├─ clashService.ts
│   │   ├─ rfiBuilder.ts   # 다중 Clash → RFI 묶기
│   │   └─ pdfBuilder.ts
│   └─ shared/types.ts     # FE/Add-in과 공유
└─ tsconfig.json
```

### 4-2. Prisma 스키마 핵심

```prisma
model Clash {
  id              String   @id
  revitUniqueId   String   @unique
  posX            Float
  posY            Float
  posZ            Float
  gapMm           Float
  level           String
  gridRef         String
  systemACode     String
  systemBCode     String
  severity        String
  status          String
  assignedTo      String?
  foundAt         DateTime
  resolvedAt      DateTime?
  sectionViewId   String
  thumbnailUrl    String
  reportUrl       String?
  rfi             Rfi?     @relation(fields: [rfiId], references: [id])
  rfiId           String?
}

model Rfi {
  id              String   @id
  title           String
  fromUser        String
  toUser          String
  state           String
  dueAt           DateTime
  clashes         Clash[]
  approvals       Approval[]
  createdAt       DateTime @default(now())
}

model FederatedModel {
  discipline      String   @id     // "MEP"
  name            String
  fileName        String
  version         String
  surveyN         Float
  surveyE         Float
  surveyZ         Float
  coordStatus     String
  driftX          Float?
  driftY          Float?
  driftZ          Float?
  lastSyncAt      DateTime
  syncedBy        String
}

model ScheduleTask {
  wbs             String   @id
  name            String
  discipline      String
  startWeek       String
  endWeek         String
  percentDone     Int
  predecessors    String[]
  levels          String[]
  grids           String[]
}

model PunchItem {
  id              String   @id
  title           String
  discipline      String
  level           String
  gridRef         String
  z               Float
  state           String
  registeredBy    String
  registeredAt    DateTime
  assignedTo      String
  dueAt           DateTime
  photos          String[]
  checklist       Json
  history         Json
  linkedRfiId     String?
}
```

### 4-3. 주요 라우트

```ts
// src/routes/clashes.ts
import { FastifyInstance } from 'fastify';
import { hub } from '../ws/hub';

export default async (app: FastifyInstance) => {
  app.get('/api/clashes', async (req) => {
    const { status, level, assignedTo } = req.query as any;
    return prisma.clash.findMany({ where: { status, level, assignedTo } });
  });

  app.get('/api/clashes/:id', async (req) => {
    return prisma.clash.findUnique({ where: { id: req.params.id } });
  });

  // Add-in이 PUSH
  app.post('/api/clashes/bulk', async (req) => {
    const dtos = req.body as ClashDto[];
    // base64 → 파일 저장, thumbnailUrl 발급
    for (const d of dtos) {
      d.thumbnailUrl = await saveThumb(d.id, d.thumbnailBase64);
      delete d.thumbnailBase64;
    }
    await prisma.clash.createMany({ data: dtos, skipDuplicates: true });
    hub.broadcast({ type: 'clash.bulk', payload: dtos });
    return { count: dtos.length };
  });

  // 대시보드가 PATCH (상태/담당자 변경)
  app.patch('/api/clashes/:id', async (req) => {
    const updated = await prisma.clash.update({
      where: { id: req.params.id },
      data: req.body as any
    });
    hub.broadcast({ type: 'clash.updated', payload: updated });
    return updated;
  });
};
```

### 4-4. WebSocket Hub

```ts
// src/ws/hub.ts
import { WebSocketServer } from 'ws';
const wss = new WebSocketServer({ port: 7900 });
const clients = new Set<any>();
wss.on('connection', s => { clients.add(s); s.on('close', () => clients.delete(s)); });
export const hub = {
  broadcast(msg: any) {
    const txt = JSON.stringify(msg);
    for (const s of clients) s.readyState === 1 && s.send(txt);
  }
};
```

### 4-5. RFI 빌더 (다중 Clash → RFI)

```ts
// src/services/rfiBuilder.ts
export async function createRfiFromClashes(clashIds: string[], from: string, to: string) {
  const clashes = await prisma.clash.findMany({ where: { id: { in: clashIds } } });
  const id = `RFI-${new Date().getFullYear()}-${pad(await nextSeq())}`;
  const rfi = await prisma.rfi.create({
    data: {
      id,
      title: summarize(clashes),               // "HVAC×구조 충돌 3건 (LV.04 C-7~D-3)"
      fromUser: from, toUser: to,
      state: 'draft', dueAt: addDays(5),
      clashes: { connect: clashes.map(c => ({ id: c.id })) }
    }
  });
  await prisma.clash.updateMany({
    where: { id: { in: clashIds } },
    data: { rfiId: id, status: 'rfi' }
  });
  return rfi;
}
```

### 4-6. 보고서 PDF 빌더

```ts
// src/services/pdfBuilder.ts — RFI 보고서
import PDFDocument from 'pdfkit';
export async function buildRfiPdf(rfiId: string): Promise<Buffer> {
  const rfi = await prisma.rfi.findUnique({
    where: { id: rfiId },
    include: { clashes: true, approvals: true }
  });
  const doc = new PDFDocument({ size: 'A4', margin: 50 });
  const chunks: Buffer[] = [];
  doc.on('data', c => chunks.push(c));

  // 표지 / 요약 / 위치 / 각 Clash 페이지 (썸네일+메타) / 결재란
  doc.fontSize(18).text(`RFI ${rfi.id}`).moveDown();
  doc.fontSize(12).text(rfi.title).moveDown();
  for (const c of rfi.clashes) {
    doc.addPage();
    doc.image(`./uploads/thumbs/${c.id}.png`, { width: 480 }).moveDown();
    doc.text(`${c.id} · ${c.level} / ${c.gridRef} · Δ ${c.gapMm.toFixed(1)}mm`);
  }
  doc.end();
  return new Promise(r => doc.on('end', () => r(Buffer.concat(chunks))));
}
```

---

## 5. Frontend (React + Vite — 현재 prototype을 프로덕션화)

### 5-1. 마이그레이션 가이드

현재 `ui_kits/console/` 의 JSX 파일들을 그대로 `frontend/src/` 로 이동 후:

```
frontend/
├─ package.json     # react 18, vite, axios, zustand, @types/*
├─ vite.config.ts
├─ src/
│   ├─ main.tsx
│   ├─ App.tsx              # 현재 App.jsx → .tsx
│   ├─ components/
│   │   ├─ Sidebar.tsx
│   │   ├─ Chrome.tsx
│   │   ├─ Viewport.tsx     # ★ APS Viewer 임베드로 교체
│   │   ├─ Analytics.tsx
│   │   ├─ ClashList.tsx
│   │   ├─ Inspector.tsx
│   │   ├─ Bits.tsx
│   │   └─ tabs/
│   │       ├─ RfiView.tsx
│   │       ├─ FedView.tsx
│   │       ├─ ScheduleView.tsx
│   │       └─ AsbView.tsx
│   ├─ store/
│   │   ├─ useClashStore.ts # zustand + WebSocket 연결
│   │   ├─ useRfiStore.ts
│   │   └─ ...
│   ├─ api/
│   │   ├─ client.ts        # axios
│   │   └─ ws.ts            # WebSocket reconnect
│   └─ styles/console.css   # 그대로 사용
```

### 5-2. WebSocket + zustand 통합

```ts
// src/store/useClashStore.ts
import { create } from 'zustand';
import { api } from '../api/client';
import { subscribe } from '../api/ws';

export const useClashStore = create((set, get) => ({
  clashes: [] as Clash[],
  selectedId: null as string | null,
  loading: false,

  async load() {
    set({ loading: true });
    const { data } = await api.get<Clash[]>('/api/clashes');
    set({ clashes: data, loading: false });
  },

  select(id: string) { set({ selectedId: id }); },

  async update(id: string, patch: Partial<Clash>) {
    const { data } = await api.patch(`/api/clashes/${id}`, patch);
    set(s => ({ clashes: s.clashes.map(c => c.id === id ? data : c) }));
  },

  // Revit으로 점프 — localhost listener 호출
  async jumpToRevit(id: string) {
    const c = get().clashes.find(x => x.id === id);
    if (!c) return;
    await fetch('http://localhost:7891/revit/show', {
      method: 'POST',
      body: JSON.stringify({
        markerUniqueId: c.revitUniqueId,
        sectionViewId:  c.sectionViewId
      })
    }).catch(() => alert('Revit Add-in이 실행 중인지 확인하세요'));
  }
}));

// WebSocket 푸시 → store 자동 동기화
subscribe('clash.bulk',    (clashes) => useClashStore.setState(s => ({
  clashes: mergeBy('id', s.clashes, clashes)
})));
subscribe('clash.updated', (c) => useClashStore.setState(s => ({
  clashes: s.clashes.map(x => x.id === c.id ? c : x)
})));
```

### 5-3. APS Viewer 임베드 (Viewport.tsx 교체)

```tsx
// src/components/Viewport.tsx — 현재 SVG를 실제 모델로
import { useEffect, useRef } from 'react';
import { useClashStore } from '../store/useClashStore';

declare const Autodesk: any;
export const Viewport = () => {
  const ref = useRef<HTMLDivElement>(null);
  const selectedId = useClashStore(s => s.selectedId);
  const clash      = useClashStore(s => s.clashes.find(c => c.id === s.selectedId));

  useEffect(() => {
    Autodesk.Viewing.Initializer({
      getAccessToken: cb => api.get('/api/aps/token').then(r => cb(r.data.token, 3600))
    }, async () => {
      const viewer = new Autodesk.Viewing.GuiViewer3D(ref.current);
      viewer.start();
      // urn은 backend에서 발급
      const { data } = await api.get('/api/aps/manifest');
      Autodesk.Viewing.Document.load(`urn:${data.urn}`, (doc: any) => {
        viewer.loadDocumentNode(doc, doc.getRoot().getDefaultGeometry());
      });
    });
  }, []);

  // 선택된 Clash로 카메라 이동
  useEffect(() => {
    if (clash) viewer?.navigation.setTarget(clash.position);
  }, [selectedId]);

  return (
    <div className="viewport">
      <div className="vp-top">
        {/* 기존 탭 + 좌표 + Source */}
        <Button onClick={() => useClashStore.getState().jumpToRevit(selectedId!)}>
          Revit으로 점프 →
        </Button>
      </div>
      <div ref={ref} className="vp-canvas"/>
    </div>
  );
};
```

### 5-4. Inspector에 썸네일 영역 추가

```tsx
{c.thumbnailUrl && (
  <div className="ins-section">
    <div className="ins-section-title">Section Box · Revit</div>
    <img src={c.thumbnailUrl} alt={c.id}
         style={{ width:'100%', borderRadius:3, border:'1px solid rgba(255,255,255,.06)' }}/>
  </div>
)}
```

---

## 6. 인증 + 환경 변수

```env
# .env (backend)
DATABASE_URL=postgresql://...
APS_CLIENT_ID=...
APS_CLIENT_SECRET=...
JWT_SECRET=...
ADDIN_API_TOKEN=mepbim-addin-...   # Add-in 전용
```

```json
// %APPDATA%\MepBim\config.json (Add-in)
{
  "backendUrl": "https://api.mepbim.example.com",
  "wsUrl":      "wss://api.mepbim.example.com/ws",
  "apiToken":   "mepbim-addin-..."
}
```

---

## 7. 통합 시나리오 — End-to-end 검증

| 시나리오 | 트리거 | 기대 결과 |
|---|---|---|
| **신규 충돌 발견** | Revit에서 Clash Detect 실행 → Add-in이 Marker 생성 | 3초 내 대시보드 충돌 리스트에 신규 행 추가, KPI "247 → 248" |
| **담당자 지정** | 대시보드에서 "박지우" 선택 | Revit Marker의 `MEPBIM_AssignedTo` 파라미터에 자동 반영 |
| **상태 변경** | 대시보드 인스펙터 → "해결 표시" | Revit Marker 색상/상태 파라미터 갱신, 푸터 KPI 감소 |
| **Revit으로 점프** | 대시보드 행에서 "Revit으로 점프 →" 클릭 | 듀얼 모니터의 Revit이 해당 Section Box로 전환 + Marker 선택 |
| **RFI 묶기** | 대시보드 충돌 3개 다중선택 → "RFI 발의" | 신규 RFI 카드 생성, 3개 Clash의 status가 "rfi"로 변경 |
| **PDF 보고서 다운로드** | RFI 인스펙터 → "보고서 PDF" | 표지 + Clash별 페이지 + 결재란 포함된 A4 PDF 다운로드 |

---

## 8. 8주 스프린트 계획

| 주차 | 백엔드 | 프론트엔드 | Add-in |
|---|---|---|---|
| **W1** | 프로젝트 부트, Prisma 스키마, /api/clashes CRUD | Vite 부트, JSX→TSX 이전 | 프로젝트 부트, 공유 파라미터 binding |
| **W2** | /bulk + WebSocket Hub | useClashStore + WS 연결 | MarkerSerializer + Thumbnail + SyncService |
| **W3** | RFI 라우트 + builder | RfiView store 연결 | LocalHttpListener + JumpHandler |
| **W4** | PDFKit 보고서 | 인스펙터 썸네일/Jump 버튼 | UpdateParameterHandler (양방향) |
| **W5** | Federation 모델 라우트 | FedView store 연결 | DocumentChanged → 자동 delta push |
| **W6** | Schedule 라우트 + .mpp parser | ScheduleView 4D 시뮬레이션 | RibbonTab UI |
| **W7** | Punch 라우트 + 사진 업로드 | AsbView store 연결 | MSI 인스톨러 (WiX) |
| **W8** | APS Viewer 토큰 + Webhook | APS Viewer 임베드 | 통합 E2E 테스트, 코드 사인 |

---

## 9. 추가 권장 사항

1. **BCF 2.1 export/import** — Navisworks/Solibri 호환 (Phase 2)
2. **ACC Issues API 양방향 동기** — 발주처가 ACC 쓰는 경우 (Phase 2)
3. **모바일/태블릿 현장 앱** — `ui_kits/field/` 기반 PWA (Phase 3)
4. **감사 로그** — 모든 PATCH를 `audit_log` 테이블에 추적
5. **Sentry + OpenTelemetry** — 운영 모니터링
6. **Revit 버전 호환성 매트릭스** — 2022 / 2023 / 2024 (UIControlledApplication API 변화)

---

## 10. 참고 자료

- **공유 파라미터 가이드**: Autodesk Revit API Docs > Shared Parameters
- **APS Viewer SDK**: aps.autodesk.com/en/docs/viewer/v7/
- **BCF 2.1 스펙**: github.com/buildingSMART/BCF-XML
- **ISO 19650**: BIM 협업 정보 관리 국제 표준
- **본 대시보드 디자인 소스**: `ui_kits/console/` (이 프로젝트)

---

**문의 / 디자인 변경 요청은 본 대시보드 디자인 소스(`ui_kits/console/`) 기준으로 진행합니다.**
