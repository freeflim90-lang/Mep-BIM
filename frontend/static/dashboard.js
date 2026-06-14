        // 전역 상태 변수 (기본값: 비활성화)
        let isProfitBusinessActive = false;
        let globalCurrentBudget = 50.00;
        let aiAgentModelLabels = {};
        const lastAgentLogAt = {};
        const MAX_CONSOLE_LOG_ENTRIES = 180;
        const BACKEND_HOST = window.location.host || "127.0.0.1:8000";
        const IS_FILE_PREVIEW = window.location.protocol === "file:";
        const API_BASE = IS_FILE_PREVIEW ? "http://127.0.0.1:8000" : "";
        function apiUrl(path) {
            return `${API_BASE}${path}`;
        }

        async function fetchJson(path, options = {}) {
            const response = await fetch(apiUrl(path), options);
            return response.json();
        }

        async function postJson(path, payload, options = {}) {
            return fetchJson(path, {
                method: options.method || 'POST',
                headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
                body: JSON.stringify(payload)
            });
        }

        async function patchJson(path, payload) {
            return postJson(path, payload, { method: 'PATCH' });
        }

        function setDashboardView(viewName) {
            const viewIds = {
                command:  "commandView",
                bimland:  "bimlandView"
            };
            const activeViewId = viewIds[viewName] || "commandView";
            document.querySelectorAll('.dashboard-view').forEach(view => {
                view.classList.toggle('active', view.id === activeViewId);
            });
            document.querySelectorAll('.view-tab').forEach(button => {
                button.classList.toggle('active', button.dataset.view === viewName);
            });
        }

        /**
         * 🟢 수익 사업 모드 활성화 / 비활성화 제어 함수
         */
        function toggleCFOMode() {
            isProfitBusinessActive = !isProfitBusinessActive;
            const panel = document.getElementById('cfoPanel');
            const btn = document.getElementById('cfoToggleBtn');
            
            if (isProfitBusinessActive) {
                panel.classList.remove('inactive');
                btn.classList.add('active');
                btn.querySelector('span').innerText = "Active";
                btn.querySelector('i').className = "fa-solid fa-chart-line";
                
                // 실시간 로그 투사
                addConsoleLog("CFO", "📊 수익 사업 정관 프로토콜(70:25:5)이 작동 제어권을 확보했습니다.");
            } else {
                panel.classList.add('inactive');
                btn.classList.remove('active');
                btn.querySelector('span').innerText = "Inactive";
                btn.querySelector('i').className = "fa-solid fa-power-off";
                
                addConsoleLog("SYSTEM", "🚧 R&D 빌드 모드로 복귀. 자본 정산 알고리즘이 대기 모드로 전환됩니다.");
            }
            
            // 모드 변환에 따른 데이터 재연산 및 분배바 갱신
            calculateCFORouting(globalCurrentBudget);
        }

        function addConsoleLog(tag, message) {
            const logBox = document.getElementById('consoleLog');
            const timeStr = new Date().toTimeString().split(' ')[0];
            const logEntry = document.createElement('div');
            logEntry.className = "log-entry";
            const timeSpan = document.createElement('span');
            timeSpan.className = "time";
            timeSpan.textContent = `[${timeStr}]`;
            const statusSpan = document.createElement('span');
            statusSpan.className = "status";
            statusSpan.textContent = ` [${tag}] `;
            const messageSpan = document.createElement('span');
            messageSpan.textContent = message;
            logEntry.append(timeSpan, statusSpan, messageSpan);
            logBox.appendChild(logEntry);
            while (logBox.children.length > MAX_CONSOLE_LOG_ENTRIES) {
                logBox.removeChild(logBox.firstElementChild);
            }
            logBox.scrollTop = logBox.scrollHeight;
        }

        function normalizeAgentName(nameText) {
            let normalized = nameText.replace(/^[0-9.\s]+/, '').trim();

            if (normalized.includes("CEO 에이전트")) return "CEO";
            if (normalized.includes("조율차장")) return "조율차장";
            if (normalized.includes("건축·구조")) return "건축";
            if (normalized.includes("소방전기")) return "소방전기";
            if (normalized.includes("전기")) return "전기";
            if (normalized.includes("위생")) return "위생";
            if (normalized.includes("통신")) return "통신";
            if (normalized.includes("최고전략")) return "최고전략 (CSO)";
            if (normalized.includes("파이프라인")) return "파이프라인_오케스트레이터";
            if (normalized.includes("Caveman")) return "Caveman_토큰다이어터";
            if (normalized.includes("인프라_DevOps")) return "인프라_DevOps (Obsidian)";

            return normalized;
        }

        function formatTx(value) {
            const numericValue = Number(value || 0);
            if (numericValue >= 1000000) return `${(numericValue / 1000000).toFixed(2)}M tx`;
            if (numericValue >= 1000) return `${(numericValue / 1000).toFixed(1)}K tx`;
            return `${numericValue} tx`;
        }

        function modelBadgeClass(label) {
            if (/Coder \+ DeepSeek|Local \+ DeepSeek/i.test(label)) return "hybrid";
            if (/DeepSeek|Review/i.test(label)) return "deepseek";
            if (/Coder/i.test(label)) return "coder";
            return "local";
        }

        function fallbackModelLabel(agentName) {
            if (/CEO|COO|CFO|조율차장|최고전략|전략기획|아이디어발굴|프로젝트분석|요구사항|브랜드마케팅|견적심사원|스토어심사|글로벌_매출관리원|글로벌_유통기획관|Revit_Addin|Navisworks_Addin|제품패키징/.test(agentName)) {
                if (/Revit_Addin|Navisworks_Addin|제품패키징/.test(agentName)) {
                    return "Coder + DeepSeek V4 Pro: qwen2.5-coder:7b / deepseek-v4-pro";
                }
                return "Local + DeepSeek V4 Pro: qwen2.5:7b / deepseek-v4-pro";
            }
            if (/프로그램개발|Qwen_Coder_8B|엑셀자동화|파이프라인|빌드검증/.test(agentName)) {
                return "Coder + DeepSeek V4 Flash: qwen2.5-coder:7b / deepseek-v4-flash";
            }
            return "Local + DeepSeek V4 Flash: qwen2.5:7b / deepseek-v4-flash";
        }

        function updateNodeModelBadge(node, agentName) {
            const label = aiAgentModelLabels[agentName] || fallbackModelLabel(agentName);
            let badge = node.querySelector('.model');
            if (!badge) {
                badge = document.createElement('div');
                badge.className = "model";
                node.appendChild(badge);
            }
            badge.textContent = label;
            badge.title = `${agentName} 적용 모델: ${label}`;
            badge.classList.remove("local", "coder", "deepseek", "hybrid");
            badge.classList.add(modelBadgeClass(label));
        }

        function updateDashboardTokens(tokenData) {
            const nodes = document.querySelectorAll('.node');
            let grandTotalTx = 0;
            
            nodes.forEach(node => {
                const nameElement = node.querySelector('.name');
                if (!nameElement) return;

                const nameText = normalizeAgentName(nameElement.innerText);
                const state = tokenData[nameText];
                updateNodeModelBadge(node, nameText);

                node.classList.toggle('active', state?.status === "Active");

                if (state) {
                    const txValue = typeof state === "object" ? formatTx(state.tokens) : state;
                    const txContainer = node.querySelector('.tx');
                    if (txContainer) txContainer.innerText = txValue;
                    
                    let numValue = parseFloat(txValue);
                    if (txValue.includes('M')) numValue *= 1000000;
                    else if (txValue.includes('K')) numValue *= 1000;
                    grandTotalTx += isNaN(numValue) ? 0 : numValue;
                }
            });

            const totalCounter = document.getElementById('totalTxCounter');
            if (totalCounter) {
                totalCounter.innerText = `가상 기업 총 트랜잭션 자원량: ${(grandTotalTx / 1000000).toFixed(2)}M tx`;
            }
        }

        async function loadAiModelRouting() {
            try {
                const result = await fetchJson('/api/ai/model-routing');
                aiAgentModelLabels = result.agent_models || result.routing?.agent_models || {};
                const localModel = result.routing?.local?.knowledge_qa?.model || "qwen2.5:7b";
                const coderModel = result.routing?.local?.coder?.model || "qwen2.5-coder:7b";
                const proModel = result.routing?.deepseek?.high_stakes_strategy?.model || "deepseek-v4-pro";
                const reviewModel = result.routing?.deepseek?.final_review?.model || "deepseek-v4-flash";
                document.querySelectorAll('.node').forEach(node => {
                    const nameElement = node.querySelector('.name');
                    if (nameElement) updateNodeModelBadge(node, normalizeAgentName(nameElement.innerText));
                });
                addConsoleLog("AI_MODEL", `DeepSeek 배치 로드: Pro ${proModel} / Flash ${reviewModel} / Local backup ${localModel}, ${coderModel}`);
            } catch (error) {
                addConsoleLog("WARN", "AI 모델 배치표를 불러오지 못해 기본 로컬 우선 표기를 사용합니다.");
                document.querySelectorAll('.node').forEach(node => {
                    const nameElement = node.querySelector('.name');
                    if (nameElement) updateNodeModelBadge(node, normalizeAgentName(nameElement.innerText));
                });
            }
        }

        function applyBackendState(payload) {
            if (!payload) return;
            if (payload.type === "DECISION_LOG") {
                addConsoleLog(payload.tag || "SYSTEM", payload.message || "");
                return;
            }
            if (payload.type !== "STATE_UPDATE") return;
            updateDashboardTokens(payload.data || {});

            if (payload.current) {
                const now = Date.now();
                if (lastAgentLogAt[payload.current] && now - lastAgentLogAt[payload.current] < 2500) return;
                lastAgentLogAt[payload.current] = now;
                const activeState = payload.data?.[payload.current];
                const activeMessage = activeState?.message ? `: ${activeState.message.slice(0, 80)}` : "";
                addConsoleLog(payload.current, `상태 동기화${activeMessage}`);
            }
        }

        let _wsRetryCount = 0;
        let _wsRetryTimer = null;

        function setBackendStatus(state, label) {
            const pulse = document.getElementById('backendPulse');
            const text = document.getElementById('backendStatusText');
            pulse.classList.remove('offline', 'connecting');
            if (state === 'offline') pulse.classList.add('offline');
            else if (state === 'connecting') pulse.classList.add('connecting');
            text.innerText = label;
        }

        function connectDashboardSocket() {
            clearTimeout(_wsRetryTimer);
            _wsRetryCount++;
            const retryLabel = _wsRetryCount === 1 ? '' : ` (${_wsRetryCount - 1}회 재시도)`;
            setBackendStatus('connecting', `백엔드 연결 중…${retryLabel}`);

            const scheme = window.location.protocol === "https:" ? "wss" : "ws";
            const socket = new WebSocket(`${scheme}://${BACKEND_HOST}/ws/office`);

            socket.addEventListener('open', () => {
                _wsRetryCount = 0;
                setBackendStatus('online', '백엔드 연결됨 ✓');
                addConsoleLog("SYSTEM", "백엔드 상태 스트림이 대시보드에 연결되었습니다.");
                socket.send(JSON.stringify({ type: "PING" }));
            });

            socket.addEventListener('message', (event) => {
                try {
                    applyBackendState(JSON.parse(event.data));
                } catch (error) {
                    addConsoleLog("WARN", "해석할 수 없는 백엔드 패킷을 수신했습니다.");
                }
            });

            socket.addEventListener('close', () => {
                const delay = Math.min(3000 + (_wsRetryCount - 1) * 2000, 15000);
                const delaySec = Math.round(delay / 1000);
                setBackendStatus('offline', `백엔드 오프라인 — ${delaySec}s 후 재연결`);
                _wsRetryTimer = setTimeout(connectDashboardSocket, delay);
            });

            socket.addEventListener('error', () => {
                setBackendStatus('offline', '백엔드 연결 실패');
            });
        }

        async function submitAddinTask(event) {
            event.preventDefault();
            const button = document.getElementById('addinSubmitBtn');
            const payload = {
                target: document.getElementById('addinTarget').value,
                discipline: document.getElementById('addinDiscipline').value,
                priority: document.getElementById('addinPriority').value,
                title: document.getElementById('addinTitle').value,
                request: document.getElementById('addinRequest').value
            };

            if (!payload.request.trim()) {
                addConsoleLog("WARN", "개발 요청 내용이 비어 있습니다.");
                return;
            }

            button.disabled = true;
            addConsoleLog("ADDIN", `${payload.target} / ${payload.discipline} 개발 요청을 라우터에 전달합니다.`);

            try {
                const result = await postJson('/api/addin-task', payload);
                if (result.status === "accepted") {
                    addConsoleLog("ADDIN", `작업 접수 완료: ${result.title}`);
                } else {
                    addConsoleLog("WARN", result.reason || "작업 접수 실패");
                }
            } catch (error) {
                addConsoleLog("ERROR", "백엔드 작업 API 호출에 실패했습니다.");
            } finally {
                button.disabled = false;
            }
        }

        async function submitKnowledgeUpdate(event) {
            event.preventDefault();
            const button = document.getElementById('knowledgeSubmitBtn');
            const payload = {
                agent: document.getElementById('knowledgeAgent').value,
                title: document.getElementById('knowledgeTitle').value,
                source: document.getElementById('knowledgeSource').value,
                tags: document.getElementById('knowledgeTags').value,
                content: document.getElementById('knowledgeContent').value
            };

            if (!payload.content.trim()) {
                addConsoleLog("WARN", "저장할 공정 지식 내용이 비어 있습니다.");
                return;
            }

            button.disabled = true;
            addConsoleLog("KNOWLEDGE", `${payload.agent} 지식 업데이트를 저장합니다.`);

            try {
                const result = await postJson('/api/knowledge-update', payload);
                if (result.status === "updated") {
                    addConsoleLog("KNOWLEDGE", `${result.agent} 지식 베이스 업데이트 완료`);
                } else {
                    addConsoleLog("WARN", result.reason || "지식 업데이트 실패");
                }
            } catch (error) {
                addConsoleLog("ERROR", "지식 업데이트 API 호출에 실패했습니다.");
            } finally {
                button.disabled = false;
            }
        }

        async function loadKnowledgeAgents() {
            try {
                const result = await fetchJson('/api/knowledge-agents');
                const select = document.getElementById('knowledgeAgent');
                select.replaceChildren();
                result.agents.forEach(agent => {
                    const option = document.createElement('option');
                    option.value = agent;
                    option.textContent = agent;
                    select.appendChild(option);
                });
            } catch (error) {
                addConsoleLog("WARN", "지식 업데이트 대상 목록을 불러오지 못했습니다.");
            }
        }

        /**
         * 📊 CFO 예산 정산 및 모드별 렌더링 제어 엔진
         */
        function calculateCFORouting(totalBudget) {
            globalCurrentBudget = totalBudget;
            
            let investment = totalBudget;
            let tax = 0;
            let dividend = 0;

            // 수익사업 활성화 상태일 때만 정관 비율 분할 계산 수행
            if (isProfitBusinessActive) {
                investment = totalBudget * 0.7;
                tax = totalBudget * 0.25;
                dividend = totalBudget * 0.05;
            }

            // UI 텍스트 업데이트
            document.getElementById('cfoBudget').innerText = `$${totalBudget.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
            document.getElementById('val70').innerText = `$${investment.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
            document.getElementById('val25').innerText = `$${tax.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
            document.getElementById('val05').innerText = `$${dividend.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;

            // 배당 임계치 조건 배지 제어
            const badge = document.getElementById('dividendStatus');
            if (isProfitBusinessActive && totalBudget >= 10000.00) {
                badge.innerText = "🔓 EXECUTE READY";
                badge.className = "dividend-status-badge execute";
            } else if (isProfitBusinessActive) {
                badge.innerText = "🔒 HOLD (< $10K)";
                badge.className = "dividend-status-badge hold";
            } else {
                badge.innerText = "🔒 OFF";
                badge.className = "dividend-status-badge hold";
            }
        }

        // 초기 구동 셋팅 ($50.00 장착 및 기본 Inactive 레이아웃 작동)
        setTimeout(() => {
            const currentMonthSample = {
                "최고전략 (CSO)": "0 tx",
                "Caveman_토큰다이어터": "0 tx",
                "프로그램개발": "0 tx"
            };
            updateDashboardTokens(currentMonthSample);
            calculateCFORouting(50.00); 
            document.querySelectorAll('.view-tab').forEach(button => {
                button.addEventListener('click', () => setDashboardView(button.dataset.view));
            });
            document.getElementById('addinTaskForm').addEventListener('submit', submitAddinTask);
            document.getElementById('knowledgeUpdateForm').addEventListener('submit', submitKnowledgeUpdate);
            loadAiModelRouting();
            loadKnowledgeAgents();
            connectDashboardSocket();

            // BIM LAND 어드민 탭 이벤트
            document.querySelectorAll('.bl-admin-tab').forEach(btn => {
                btn.addEventListener('click', () => {
                    document.querySelectorAll('.bl-admin-tab').forEach(b => b.classList.remove('active'));
                    document.querySelectorAll('.bl-admin-panel').forEach(p => p.classList.remove('active'));
                    btn.classList.add('active');
                    // 케밥 케이스 → camelCase 변환 (예: loc-requests → locRequests)
                    const camel = btn.dataset.atab.replace(/-([a-z])/g, (_, c) => c.toUpperCase());
                    const panelId = 'blAdmin' + camel.charAt(0).toUpperCase() + camel.slice(1);
                    document.getElementById(panelId)?.classList.add('active');
                });
            });

            // BIM LAND 탭 클릭 시 데이터 로드 + 지도 크기 재계산
            document.querySelector('[data-view="bimland"]')?.addEventListener('click', () => {
                loadBimLandData();
                setTimeout(() => { if (_blMap) _blMap.invalidateSize(); }, 50);
            });

            // 30초마다 자동 갱신 (BIM LAND 뷰 활성 시에만)
            setInterval(() => {
                if (document.getElementById('bimlandView')?.classList.contains('active')) {
                    loadBimLandData();
                }
            }, 30000);

        }, 300);

// ═══════════════════════════════════════════════════════════ BIM LAND JS

        const BL_GRADE_COLOR  = { Normal:'#6b7280', Rare:'#3b82f6', Epic:'#8b5cf6', Legendary:'#f97316' };
        const BL_GRADE_EMOJI  = { Normal:'🟢', Rare:'🔵', Epic:'🟣', Legendary:'🟠' };
        const BL_GRADE_RADIUS = { Normal:500, Rare:1000, Epic:2000, Legendary:4000 }; // 영향권 반지름(m)
        const BL_TEAM_PALETTE = ['#ef4444','#3b82f6','#22c55e','#f59e0b','#8b5cf6','#ec4899','#06b6d4','#84cc16'];
        let _blMap = null;
        let _blMapMarkers = [];
        let _blTeamList = [];
        let _blProjects = [];
        let _blCircleMap = new Map();  // code → { movable: [...leafletLayers], origLL: [lat,lng] }

        function blTeamColor(team) {
            const idx = _blTeamList.indexOf(team);
            return BL_TEAM_PALETTE[(idx < 0 ? 0 : idx) % BL_TEAM_PALETTE.length];
        }

        async function loadBimLandData() {
            try {
                const claimStatus   = document.getElementById('blClaimsFilter')?.value || 'pending';
                const claimProject  = document.getElementById('blClaimsProjectFilter')?.value?.trim() || '';
                const claimQs       = `status=${claimStatus}${claimProject ? '&project_code='+encodeURIComponent(claimProject) : ''}`;

                const locReqStatus = document.getElementById('blLocReqFilter')?.value || 'pending';
                const gfaStatus    = document.getElementById('blGfaFilter')?.value || 'pending';

                const [terr, lb, reports, blocked, claims, projects, locReqs, gfaQueue] = await Promise.all([
                    fetchJson('/api/bim-land/territories'),
                    fetchJson('/api/bim-land/leaderboard?top=10'),
                    fetchJson('/api/bim-land/admin/reports?status=' +
                        (document.getElementById('blReportFilter')?.value || 'all')),
                    fetchJson('/api/bim-land/admin/blocked-users'),
                    fetchJson(`/api/bim-land/admin/participation-claims?${claimQs}`),
                    fetchJson('/api/bim-land/projects'),
                    fetchJson(`/api/bim-land/admin/location-change-requests?status=${locReqStatus}`),
                    fetchJson(`/api/bim-land/admin/gfa-review?status=${gfaStatus}`),
                ]);

                _blTeamList = lb.map(item => item.team);
                _blProjects = projects;
                renderBimLandStats(terr, lb, projects);
                renderBimLandMap(terr, projects);
                renderBimLandTable(terr, projects);
                renderBimLandLeaderboard(lb, projects);
                renderBimLandReports(reports);
                renderBimLandBlocked(blocked);
                renderParticipationClaims(claims);
                renderProjectList(projects);
                renderLocationRequests(locReqs);
                renderGfaReview(gfaQueue);
            } catch(e) {
                console.warn('[BIM LAND] 데이터 로드 실패:', e.message);
            }
        }

        function renderBimLandStats(terr, lb, projects) {
            const codes = Object.keys(terr);
            document.getElementById('blStatTerritories').textContent = codes.length;
            document.getElementById('blStatTeams').textContent = lb.length;
            const totalXp = Object.values(terr).reduce((s, t) => s + (t.total_xp || 0), 0);
            document.getElementById('blStatXp').textContent = totalXp.toLocaleString('ko-KR', {maximumFractionDigits:0});
            // 등록 프로젝트 수 (stat 4번째 칸 재활용)
            const statProj = document.getElementById('blStatProjects');
            if (statProj) statProj.textContent = (projects||[]).length;
        }

        // ── GFA → 원형 반지름(m) 변환 ────────────────────────────────────────────
        function gfaRadius(gfa_m2) {
            return Math.min(Math.max(Math.sqrt(Math.max(gfa_m2 || 0, 4000) / Math.PI), 80), 1400);
        }

        // ── 드래그 가능한 중심 마커 ───────────────────────────────────────────────
        function _makeDragMarker(latlng, color, onDragEnd) {
            const icon = L.divIcon({
                className: '',
                html: `<div style="width:12px;height:12px;border-radius:50%;background:${color};
                           border:2px solid rgba(255,255,255,0.85);cursor:grab;
                           box-shadow:0 0 6px rgba(0,0,0,0.6);margin:-6px 0 0 -6px"></div>`,
                iconSize: [0, 0], iconAnchor: [0, 0]
            });
            const marker = L.marker(latlng, { draggable: true, icon, zIndexOffset: 1000 });
            marker.on('dragend', async ev => {
                const { lat, lng } = ev.target.getLatLng();
                await onDragEnd(lat, lng);
            });
            marker.addTo(_blMap);
            return marker;
        }

        async function _patchProjectCoords(code, lat, lng, originalLatLng, circles) {
            const proj = (_blProjects || []).find(p => p.project_code === code);
            const name = proj?.project_name || code;
            const hasExisting = !!(proj?.latitude && proj?.longitude);

            const revert = () => {
                if (originalLatLng && circles?.length) {
                    circles.forEach(c => c.setLatLng(originalLatLng));
                }
            };

            try {
                if (hasExisting) {
                    // 재수정 — 관리자 확인 후 즉시 저장
                    const prevLat = proj.latitude.toFixed(5);
                    const prevLng = proj.longitude.toFixed(5);
                    const ok = confirm(
                        `"${name}" 위치를 변경하시겠습니까?\n\n` +
                        `현재: ${prevLat}, ${prevLng}\n` +
                        `변경: ${lat.toFixed(5)}, ${lng.toFixed(5)}`
                    );
                    if (!ok) { revert(); return; }
                }

                // 저장 (최초 설정 또는 관리자 직접 수정)
                const data = await patchJson(`/api/bim-land/admin/projects/${code}`, { latitude: lat, longitude: lng });
                if (data.status === 'updated') {
                    if (proj) { proj.latitude = lat; proj.longitude = lng; }
                    // 원이 이미 이동된 상태이므로 circleMap origLL도 갱신
                    const cm = _blCircleMap.get(code);
                    if (cm) cm.origLL = [lat, lng];
                } else {
                    revert();
                }
            } catch(e) {
                console.warn('[BIM LAND] 좌표 저장 실패:', e.message);
                revert();
            }
        }

        function renderBimLandMap(terr, projects) {
            if (!_blMap) {
                _blMap = L.map('blMap', { zoomControl: true }).setView([36.5, 127.8], 7);
                L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                    attribution: '© CartoDB', maxZoom: 19
                }).addTo(_blMap);
            }

            _blMapMarkers.forEach(m => m.remove());
            _blMapMarkers = [];
            _blCircleMap.clear();

            // ① 등록 프로젝트 (sync 없음) — GFA 원 + 드래그 마커
            const terrCodes = new Set(Object.keys(terr));
            (projects || []).forEach(p => {
                const lat = p.latitude || 0, lng = p.longitude || 0;
                if (!lat && !lng) return;
                if (terrCodes.has(p.project_code)) return;

                const gfa        = p.gross_floor_area_m2 || 0;
                const gfaApproved = p.gfa_review_status === 'approved';
                const gfaR       = gfaApproved ? gfaRadius(gfa) : 80;
                const gfaTxt     = gfa > 0
                    ? `${gfa.toLocaleString()} m²${gfaApproved ? '' : ' ⚠️검토중'}`
                    : '미입력';
                const disc   = (p.disciplines || []).join(', ') || '미지정';
                const popup  = `
                    <div style="font-family:sans-serif;font-size:12px;min-width:180px">
                        <b style="color:#e2b96f">${p.project_name}</b>
                        <div style="color:#999;font-size:10px;margin:2px 0">${p.project_code}</div>
                        <div style="font-size:10px">${p.address || '주소 미입력'}</div>
                        <div style="margin-top:4px;color:#aaa;font-size:10px">공종: ${disc}</div>
                        <div style="color:#e2b96f;font-size:10px">연면적: ${gfaTxt}</div>
                        <div style="margin-top:4px;color:#f59e0b;font-size:10px">⏳ 동기화 대기 중</div>
                    </div>`;

                const circle = L.circle([lat, lng], {
                    radius: gfaR, color: '#e2b96f', weight: 1.5,
                    fillColor: '#374151', fillOpacity: 0.5, dashArray: '5 4'
                }).bindPopup(popup).addTo(_blMap);

                const origLL = [lat, lng];
                const drag = _makeDragMarker([lat, lng], '#e2b96f', async (newLat, newLng) => {
                    circle.setLatLng([newLat, newLng]);
                    await _patchProjectCoords(p.project_code, newLat, newLng, origLL, [circle, drag]);
                });

                _blCircleMap.set(p.project_code, { movable: [circle, drag], origLL });
                _blMapMarkers.push(circle, drag);
            });

            // ② 영토 데이터 (sync 완료) — 등급 외부 원 + GFA 내부 원 + 드래그 마커
            Object.entries(terr).forEach(([code, t]) => {
                const lat = t.latitude || 0, lng = t.longitude || 0;
                if (!lat && !lng) return;

                const grade     = t.grade || 'Normal';
                const team      = t.owner_team || '?';
                const xp        = t.total_xp || 0;
                const gfa       = t.gross_floor_m2 || 0;
                const projReg   = (projects || []).find(p => p.project_code === code);
                const gfaApproved = projReg?.gfa_review_status === 'approved';
                const gfaTxt    = gfa > 0
                    ? `${gfa.toLocaleString()} m²${gfaApproved ? '' : ' ⚠️검토중'}`
                    : '미입력';
                const color     = BL_GRADE_COLOR[grade] || '#6b7280';
                const terrRad   = BL_GRADE_RADIUS[grade] || 500;
                const gfaR      = gfaApproved ? Math.min(gfaRadius(gfa), terrRad * 0.75) : 80;
                const teamColor = blTeamColor(team);
                const popup     = `
                    <div style="font-family:sans-serif;font-size:12px;min-width:190px">
                        <b>${t.project_name || code}</b>
                        <div style="margin:3px 0">
                            <span style="color:${color}">${BL_GRADE_EMOJI[grade]||''} ${grade}</span>
                        </div>
                        <div>팀: <b style="color:${teamColor}">${team}</b></div>
                        <div>XP: <b style="color:var(--accent-lua)">${xp.toLocaleString()}</b></div>
                        <div style="margin-top:4px;font-size:10px;color:#aaa">연면적: ${gfaTxt}</div>
                    </div>`;

                // 외부 영향권 원 (등급 색상, 반투명)
                const outerCircle = L.circle([lat, lng], {
                    radius: terrRad, color: teamColor, weight: 2,
                    fillColor: color, fillOpacity: 0.12
                }).bindPopup(popup).addTo(_blMap);

                // 내부 GFA 원 (실제 바닥면적, 진하게)
                const innerCircle = L.circle([lat, lng], {
                    radius: gfaR, color: color, weight: 1.5,
                    fillColor: color, fillOpacity: 0.45,
                    interactive: false
                }).addTo(_blMap);

                if (grade === 'Legendary') {
                    L.marker([lat, lng], {
                        icon: L.divIcon({ html: '<div style="font-size:18px;margin:-9px 0 0 -4px">🚩</div>',
                                          iconSize: [0, 0] })
                    }).addTo(_blMap);
                }

                // 드래그 마커 — 두 원 동시 이동 + 좌표 저장(최초) / 변경 요청(재수정)
                const origLL = [lat, lng];
                const drag = _makeDragMarker([lat, lng], color, async (newLat, newLng) => {
                    outerCircle.setLatLng([newLat, newLng]);
                    innerCircle.setLatLng([newLat, newLng]);
                    await _patchProjectCoords(code, newLat, newLng, origLL,
                                              [outerCircle, innerCircle, drag]);
                });

                _blCircleMap.set(code, { movable: [outerCircle, innerCircle, drag], origLL });
                _blMapMarkers.push(outerCircle, innerCircle, drag);
            });
        }

        function renderBimLandTable(terr, projects) {
            const tbody = document.getElementById('blTerritoryBody');
            if (!tbody) return;

            // 영토 데이터 + 미동기화 등록 프로젝트 병합
            const terrCodes = new Set(Object.keys(terr));
            const terrRows  = Object.entries(terr)
                .sort(([,a],[,b]) => (b.total_xp||0) - (a.total_xp||0))
                .map(([code, t]) => {
                    const grade  = t.grade || 'Normal';
                    const sync   = (t.last_sync_at || '').substring(0, 16);
                    const syncFile = t.last_sync_file || '';
                    const syncPath = t.last_sync_path || '';
                    const pending = t.location_pending;
                    const statusCell = pending
                        ? `<span style="color:#f59e0b;font-size:9px">📍 위치 미확인</span>`
                        : `<span style="font-size:9px">${t.status||'STABLE'}</span>`;
                    const fileCellTitle = syncPath ? ` title="${syncPath}"` : '';
                    const fileCell = syncFile
                        ? `<div${fileCellTitle} style="cursor:${syncPath?'help':'default'}">
                               <span style="color:#60a5fa;font-size:9px">📄 ${syncFile}</span>
                               <div style="color:var(--text-secondary);font-size:8px;margin-top:1px">${sync}</div>
                           </div>`
                        : `<span style="color:var(--text-secondary);font-size:9px">${sync||'-'}</span>`;
                    return `<tr style="${pending ? 'opacity:0.6' : ''}">
                        <td><span class="bl-grade ${grade}">${BL_GRADE_EMOJI[grade]||''} ${grade}</span></td>
                        <td>${t.project_name || code}</td>
                        <td style="color:${blTeamColor(t.owner_team)}">${t.owner_team||'?'}</td>
                        <td style="font-family:monospace;color:var(--accent-lua)">${(t.total_xp||0).toLocaleString()}</td>
                        <td>${fileCell}</td>
                        <td>${statusCell}</td>
                    </tr>`;
                });

            // 동기화 이력 없는 등록 프로젝트
            const pendingRows = (projects || [])
                .filter(p => !terrCodes.has(p.project_code))
                .map(p => {
                    const disc = (p.disciplines||[]).join('/') || '-';
                    const locOk = !!(p.latitude && p.longitude);
                    return `<tr style="opacity:0.55">
                        <td><span class="bl-grade Normal" style="color:#555;border-color:#333">— 미동기화</span></td>
                        <td>${p.project_name}</td>
                        <td style="color:#555">-</td>
                        <td style="font-family:monospace;color:#444">0</td>
                        <td style="color:var(--text-secondary);font-size:9px">${disc}</td>
                        <td><span style="font-size:9px;color:${locOk ? '#f59e0b' : '#555'}">
                            ${locOk ? '⏳ 동기화 대기' : '📍 위치 미확인'}
                        </span></td>
                    </tr>`;
                });

            const all = [...terrRows, ...pendingRows];
            tbody.innerHTML = all.length
                ? all.join('')
                : '<tr><td colspan="6" style="text-align:center;color:#555;padding:12px">데이터 없음</td></tr>';
        }

        function renderBimLandLeaderboard(lb, projects) {
            const el = document.getElementById('blLeaderboard');
            if (!el) return;
            const medals = ['🥇','🥈','🥉'];

            if (lb && lb.length) {
                el.innerHTML = lb.map(item => `
                    <div class="bl-rank-item">
                        <span class="bl-rank-medal">${medals[item.rank-1] || item.rank + '.'}</span>
                        <span class="bl-rank-team" style="color:${blTeamColor(item.team)}">${item.team}</span>
                        <span class="bl-rank-xp">${item.total_xp.toLocaleString()} XP</span>
                    </div>`
                ).join('');
                return;
            }

            // 동기화 데이터 없을 때 — 등록된 팀 목록만 표시
            const teamSet = new Map();
            (projects || []).forEach(p => {
                const team = p.team_name || p.registered_by || '?';
                teamSet.set(team, (teamSet.get(team) || 0) + 1);
            });
            if (!teamSet.size) {
                el.innerHTML = '<div class="bl-empty">동기화 데이터 없음</div>';
                return;
            }
            el.innerHTML = [...teamSet.entries()]
                .sort((a, b) => b[1] - a[1])
                .map(([team, cnt], i) => `
                    <div class="bl-rank-item" style="opacity:0.6">
                        <span class="bl-rank-medal">${medals[i] || (i+1) + '.'}</span>
                        <span class="bl-rank-team" style="color:${blTeamColor(team)}">${team}</span>
                        <span class="bl-rank-xp" style="color:#555">${cnt}개 프로젝트 · 0 XP</span>
                    </div>`
                ).join('');
        }

        function renderBimLandReports(reports) {
            const el = document.getElementById('blReportList');
            if (!el) return;
            if (!reports.length) { el.innerHTML = '<div class="bl-empty">신고 없음</div>'; return; }
            el.innerHTML = reports.map(r => {
                const isPending = r.status === 'pending';

                // 신고자 연락처
                const reporterPhone = r.reporter_phone
                    ? `<span class="bl-contact-chip reporter">📞 신고자 ${r.reporter_phone}</span>`
                    : `<span class="bl-contact-chip missing">📵 신고자 연락처 없음</span>`;

                // 피신고자 연락처
                const reportedPhone = r.reported_phone
                    ? `<span class="bl-contact-chip reported">📞 피신고자 ${r.reported_phone}
                        <span style="opacity:.6">(${(r.reported_phone_submitted_at||'').substring(0,16)} 제출)</span>
                       </span>`
                    : (isPending
                        ? `<span class="bl-contact-chip missing">📵 피신고자 미제출</span>`
                        : `<span class="bl-contact-chip missing">📵 피신고자 미제출</span>`);

                // 양방향 연락처 확보 여부 표시
                const bothReady = r.reporter_phone && r.reported_phone;
                const readyBadge = bothReady
                    ? `<span style="font-size:9px;color:#22c55e;font-weight:700">✅ 양방향 연락처 확보 — 관리자 검토 가능</span>`
                    : `<span style="font-size:9px;color:#f59e0b">⏳ 연락처 미확보 (${[!r.reporter_phone&&'신고자',!r.reported_phone&&'피신고자'].filter(Boolean).join(', ')} 미제출)</span>`;

                const actions = isPending ? `
                    <div class="bl-report-actions">
                        <button class="bl-btn-block"   onclick="adminResolveReport('${r.report_id}','block')">
                            <i class="fa-solid fa-ban"></i> 차단
                        </button>
                        <button class="bl-btn-dismiss" onclick="adminResolveReport('${r.report_id}','dismiss')">
                            기각
                        </button>
                    </div>` : `<div style="font-size:9px;color:var(--text-secondary);margin-top:4px">처리완료: ${r.status}</div>`;

                return `
                <div class="bl-report-card ${r.status}">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <span class="bl-report-id">${r.report_id}</span>
                        <span style="font-size:9px;color:var(--text-secondary)">${(r.filed_at||'').substring(0,16)}</span>
                    </div>
                    <div style="margin:5px 0;display:flex;flex-direction:column;gap:3px">
                        <div>신고자: <b style="color:#94a3b8">${r.reporter_email}</b></div>
                        <div>피신고자: <b class="bl-report-email">${r.reported_email}</b></div>
                        <div>프로젝트: <code style="font-size:9px;color:var(--accent-lua)">${r.project_code}</code></div>
                        <div class="bl-report-reason">${r.reason}</div>
                    </div>
                    <div style="display:flex;flex-direction:column;gap:3px;margin:5px 0;padding:6px;background:rgba(15,22,43,0.6);border-radius:5px">
                        ${reporterPhone}
                        ${reportedPhone}
                        <div style="margin-top:3px">${readyBadge}</div>
                    </div>
                    ${actions}
                </div>`;
            }).join('');
        }

        function renderBimLandBlocked(blocked) {
            const el = document.getElementById('blBlockedList');
            if (!el) return;
            if (!blocked.length) { el.innerHTML = '<div class="bl-empty">차단된 사용자 없음</div>'; return; }
            el.innerHTML = blocked.map(b => `
                <div class="bl-blocked-item">
                    <span class="bl-blocked-email">${b.email}</span>
                    <span class="bl-blocked-reason">${b.reason || ''}</span>
                    <button class="bl-btn-unblock" onclick="adminUnblockUser('${b.email}')">해제</button>
                </div>`
            ).join('');
        }

        async function submitReport() {
            const reporterEmail = document.getElementById('blReporterEmail')?.value?.trim();
            const reporterPhone = document.getElementById('blReporterPhone')?.value?.trim();
            const reportedEmail = document.getElementById('blReportedEmail')?.value?.trim();
            const projectCode   = document.getElementById('blReportProject')?.value?.trim();
            const reason        = document.getElementById('blReportReason')?.value?.trim();

            if (!reporterEmail || !reporterPhone || !reportedEmail || !projectCode || !reason) {
                alert('모든 항목을 입력해주세요. 신고자 연락처는 필수입니다.');
                return;
            }
            const data = await postJson('/api/bim-land/report', {
                reporter_email: reporterEmail,
                reporter_phone: reporterPhone,
                reported_email: reportedEmail,
                project_code:   projectCode,
                reason
            });
            alert(`신고가 접수되었습니다. (${data.report_id})\n피신고자가 연락처를 제출하면 관리자가 양방향 확인 후 처리합니다.`);
            ['blReporterEmail','blReporterPhone','blReportedEmail','blReportProject','blReportReason']
                .forEach(id => { const el = document.getElementById(id); if(el) el.value = ''; });
            loadBimLandData();
        }

        async function adminBlockUser() {
            const email  = document.getElementById('blBlockEmail')?.value?.trim();
            const reason = document.getElementById('blBlockReason')?.value?.trim();
            if (!email) return alert('이메일을 입력하세요.');
            await postJson('/api/bim-land/admin/block', { email, reason: reason || '관리자 직접 차단', blocked_by: 'admin' });
            document.getElementById('blBlockEmail').value = '';
            document.getElementById('blBlockReason').value = '';
            loadBimLandData();
        }

        async function adminUnblockUser(email) {
            if (!confirm(`${email} 차단을 해제하시겠습니까?`)) return;
            await fetch(apiUrl(`/api/bim-land/admin/block/${encodeURIComponent(email)}`), { method: 'DELETE' });
            loadBimLandData();
        }

        async function adminResolveReport(reportId, action) {
            const label = action === 'block' ? '차단 처리' : '기각';
            if (!confirm(`${reportId}를 ${label}하시겠습니까?`)) return;
            await postJson(`/api/bim-land/admin/reports/${reportId}/resolve`, { action, resolved_by: 'admin' });
            loadBimLandData();
        }

        // ── 참여 이력 신청 승인 패널 ──────────────────────────────────────────────

        function renderParticipationClaims(claims) {
            const el = document.getElementById('blClaimsList');
            if (!el) return;
            if (!claims.length) { el.innerHTML = '<div class="bl-empty">신청 없음</div>'; return; }

            const STATUS_LABEL = { pending:'⏳ 대기', approved:'✅ 승인', rejected:'❌ 거절' };
            el.innerHTML = claims.map(c => {
                const isPending = c.status === 'pending';
                const actions = isPending ? `
                    <div class="bl-report-actions">
                        <button class="bl-btn-approve" onclick="adminResolveClaim('${c.claim_id}','approve')">
                            <i class="fa-solid fa-check"></i> 승인
                        </button>
                        <button class="bl-btn-dismiss" onclick="adminResolveClaim('${c.claim_id}','reject')">
                            거절
                        </button>
                    </div>` : `<div style="font-size:9px;color:var(--text-secondary);margin-top:4px">${STATUS_LABEL[c.status]||c.status} — ${(c.reviewed_at||'').substring(0,16)}</div>`;

                return `
                <div class="bl-claim-card ${c.status}">
                    <div style="display:flex;justify-content:space-between">
                        <span style="font-family:monospace;font-size:9px;color:var(--text-secondary)">${c.claim_id}</span>
                        <span style="font-size:9px;color:var(--text-secondary)">${(c.submitted_at||'').substring(0,16)}</span>
                    </div>
                    <div style="margin:5px 0;display:flex;flex-direction:column;gap:2px">
                        <div>이메일: <b style="color:#60a5fa">${c.user_email}</b></div>
                        ${c.user_phone ? `<div style="font-size:9px;color:#4ade80">📞 ${c.user_phone}</div>` : ''}
                        ${c.company ? `<div style="font-size:9px;color:var(--text-secondary)">🏢 ${c.company}</div>` : ''}
                        <div>프로젝트: <code style="font-size:9px;color:var(--accent-lua)">${c.project_code}</code></div>
                        <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:2px">
                            <span class="bl-tag">${c.discipline}</span>
                            <span class="bl-tag">${c.role}</span>
                            <span class="bl-tag">${c.start_date} ~ ${c.end_date}</span>
                        </div>
                        <div style="font-size:9px;color:var(--text-primary);margin-top:3px;line-height:1.5;background:rgba(15,22,43,0.6);padding:5px;border-radius:4px">${c.description}</div>
                    </div>
                    ${actions}
                </div>`;
            }).join('');
        }

        async function adminResolveClaim(claimId, action) {
            const label = action === 'approve' ? '승인' : '거절';
            if (!confirm(`${claimId}를 ${label}하시겠습니까?`)) return;
            await postJson(`/api/bim-land/admin/participation-claims/${claimId}/resolve`, { action, reviewed_by: 'admin' });
            loadBimLandData();
        }

        // ── 프로젝트 등록 패널 ─────────────────────────────────────────────────────

        function renderProjectList(projects) {
            const el = document.getElementById('blProjectList');
            if (!el) return;
            if (!projects.length) { el.innerHTML = '<div class="bl-empty">등록된 프로젝트 없음</div>'; return; }
            el.innerHTML = projects.map(p => {
                const hasCoords = !!(p.latitude && p.longitude);
                const locBadge  = hasCoords
                    ? `<span style="font-size:8px;color:#22c55e;border:1px solid #22c55e;border-radius:3px;padding:0 3px">📍 위치 확인</span>`
                    : `<span style="font-size:8px;color:#f59e0b;border:1px solid #f59e0b;border-radius:3px;padding:0 3px"
                           title="좌표 등록 후 지도에 표시됩니다">📍 위치 미확인</span>`;
                const gfa    = p.gross_floor_area_m2 || 0;
                const gfaStatus  = p.gfa_review_status || 'unset';
                const gfaStatusLabel = {
                    unset:     { text:'연면적 미입력', color:'#6b7280' },
                    pending:   { text:'연면적 검토대기', color:'#f59e0b' },
                    approved:  { text:'연면적 승인', color:'#22c55e' },
                    suspended: { text:'연면적 유보', color:'#ef4444' },
                }[gfaStatus] || { text: gfaStatus, color:'#888' };
                const gfaBadge = `<span style="font-size:8px;color:${gfaStatusLabel.color};
                    border:1px solid ${gfaStatusLabel.color};border-radius:3px;padding:0 3px">
                    ${gfaStatusLabel.text}</span>`;
                const gfaTxt = gfa > 0 ? `${gfa.toLocaleString()} m²` : null;
                const safeCode = p.project_code.replace(/['"]/g, '');
                return `
                <div class="bl-project-item" style="${!hasCoords ? 'opacity:0.65' : ''}">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <code style="font-size:9px;color:var(--accent-lua)">${p.project_code}</code>
                        <div style="display:flex;gap:4px;align-items:center">
                            ${locBadge}
                            <button onclick="toggleLocSearch('${safeCode}')"
                                title="주소로 위치 이동"
                                style="font-size:8px;padding:1px 5px;background:rgba(226,185,111,0.12);
                                       color:#e2b96f;border:1px solid rgba(226,185,111,0.35);
                                       border-radius:3px;cursor:pointer">
                                🔍 위치
                            </button>
                            <button onclick="deleteProject('${safeCode}')"
                                title="프로젝트 삭제"
                                style="font-size:8px;padding:1px 5px;background:rgba(239,68,68,0.1);
                                       color:#ef4444;border:1px solid rgba(239,68,68,0.35);
                                       border-radius:3px;cursor:pointer">
                                🗑
                            </button>
                        </div>
                    </div>
                    <div id="blNameView_${safeCode}" style="display:flex;align-items:center;gap:4px;margin:2px 0">
                        <span style="font-weight:600;font-size:10px;flex:1">${p.project_name}</span>
                        <button onclick="toggleFieldEdit('${safeCode}','name')"
                            style="font-size:8px;padding:1px 5px;background:rgba(226,185,111,0.1);
                                   color:#888;border:1px solid #444;border-radius:3px;cursor:pointer">✏️</button>
                    </div>
                    <div id="blNameEdit_${safeCode}" style="display:none;align-items:center;gap:3px;margin:2px 0">
                        <input id="blNameInput_${safeCode}" type="text"
                               value="${p.project_name.replace(/"/g, '&quot;')}"
                               onkeydown="if(event.key==='Enter')saveField('${safeCode}','name');if(event.key==='Escape')toggleFieldEdit('${safeCode}','name')"
                               style="flex:1;padding:3px 6px;font-size:9px;background:#0f0f0f;
                                      border:1px solid rgba(226,185,111,0.5);color:#e2b96f;
                                      border-radius:3px;outline:none">
                        <button onclick="saveField('${safeCode}','name')"
                            style="font-size:8px;padding:2px 7px;background:rgba(34,197,94,0.15);
                                   color:#22c55e;border:1px solid rgba(34,197,94,0.4);
                                   border-radius:3px;cursor:pointer">저장</button>
                        <button onclick="toggleFieldEdit('${safeCode}','name')"
                            style="font-size:8px;padding:2px 5px;background:transparent;
                                   color:#666;border:1px solid #333;border-radius:3px;cursor:pointer">✕</button>
                    </div>
                    <div style="display:flex;justify-content:space-between;align-items:center;margin:1px 0">
                        <span style="font-size:9px;color:#a78bfa">🏢 ${p.team_name || '팀 미등록'}</span>
                        <button onclick="transferTeam('${safeCode}')"
                            title="이직 등 팀명 변경"
                            style="font-size:8px;padding:1px 5px;background:rgba(167,139,250,0.1);
                                   color:#a78bfa;border:1px solid rgba(167,139,250,0.35);
                                   border-radius:3px;cursor:pointer">
                            🔄 팀 이전
                        </button>
                    </div>
                    <div style="font-size:9px;color:var(--text-secondary)">${p.address || '주소 미입력'}</div>
                    <!-- 주소 검색으로 위치 이동 (기본 숨김) -->
                    <div id="blLocSearch_${safeCode}" style="display:none;margin-top:5px">
                        <input type="text" placeholder="🔍 주소 입력 후 선택…"
                               oninput="locSearchInput('${safeCode}', this.value)"
                               autocomplete="off"
                               style="width:100%;box-sizing:border-box;padding:4px 7px;font-size:9px;
                                      background:var(--bg-node);border:1px solid rgba(226,185,111,0.4);
                                      color:var(--text-primary);border-radius:4px">
                        <div id="blLocDrop_${safeCode}"
                             style="background:#1a1a1a;border:1px solid #333;border-radius:4px;
                                    margin-top:2px;max-height:120px;overflow-y:auto"></div>
                    </div>
                    <div style="display:flex;gap:4px;flex-wrap:wrap;margin-top:4px;align-items:center">
                        ${gfaBadge}
                        ${(p.disciplines||[]).map(d => `<span class="bl-tag">${d}</span>`).join('')}
                    </div>
                    <!-- 연면적 표시 + 인라인 수정 -->
                    <div style="margin-top:4px">
                        <div id="blGfaView_${safeCode}" style="display:flex;align-items:center;gap:4px">
                            <span style="font-size:9px;color:#aaa">연면적:</span>
                            <span style="font-size:9px;color:#e2b96f;font-weight:600">
                                ${gfa > 0 ? gfa.toLocaleString() + ' m²' : '미입력'}
                            </span>
                            <button onclick="toggleGfaEdit('${safeCode}')"
                                style="font-size:8px;padding:1px 5px;background:rgba(226,185,111,0.1);
                                       color:#888;border:1px solid #444;border-radius:3px;cursor:pointer">
                                ✏️ 수정
                            </button>
                        </div>
                        <div id="blGfaEdit_${safeCode}" style="display:none;align-items:center;gap:3px;margin-top:3px">
                            <input id="blGfaInput_${safeCode}" type="number"
                                   value="${gfa || ''}" placeholder="연면적 입력" min="0" step="100"
                                   onkeydown="if(event.key==='Enter')saveGfa('${safeCode}');if(event.key==='Escape')toggleGfaEdit('${safeCode}')"
                                   style="width:100px;padding:3px 6px;font-size:9px;
                                          background:#0f0f0f;border:1px solid rgba(226,185,111,0.5);
                                          color:#e2b96f;border-radius:3px;outline:none">
                            <span style="font-size:9px;color:#666">m²</span>
                            <button onclick="saveGfa('${safeCode}')"
                                style="font-size:8px;padding:2px 7px;background:rgba(34,197,94,0.15);
                                       color:#22c55e;border:1px solid rgba(34,197,94,0.4);
                                       border-radius:3px;cursor:pointer">저장</button>
                            <button onclick="toggleGfaEdit('${safeCode}')"
                                style="font-size:8px;padding:2px 5px;background:transparent;
                                       color:#666;border:1px solid #333;border-radius:3px;cursor:pointer">✕</button>
                        </div>
                    </div>
                    <!-- 설명 인라인 수정 -->
                    <div style="margin-top:4px">
                        <div id="blDescView_${safeCode}" style="display:flex;align-items:flex-start;gap:4px">
                            <span style="font-size:9px;color:#888;flex:1;line-height:1.4">
                                ${p.description ? p.description : '<span style="color:#444">설명 없음</span>'}
                            </span>
                            <button onclick="toggleFieldEdit('${safeCode}','desc')"
                                style="font-size:8px;padding:1px 5px;background:rgba(226,185,111,0.1);
                                       color:#888;border:1px solid #444;border-radius:3px;cursor:pointer;flex-shrink:0">✏️</button>
                        </div>
                        <div id="blDescEdit_${safeCode}" style="display:none;flex-direction:column;gap:3px;margin-top:3px">
                            <textarea id="blDescInput_${safeCode}" rows="2"
                                      onkeydown="if(event.key==='Escape')toggleFieldEdit('${safeCode}','desc')"
                                      style="width:100%;box-sizing:border-box;padding:3px 6px;font-size:9px;
                                             background:#0f0f0f;border:1px solid rgba(226,185,111,0.5);
                                             color:#ccc;border-radius:3px;outline:none;resize:vertical"
                            >${(p.description || '').replace(/</g, '&lt;').replace(/>/g, '&gt;')}</textarea>
                            <div style="display:flex;gap:3px">
                                <button onclick="saveField('${safeCode}','desc')"
                                    style="flex:1;font-size:8px;padding:2px 7px;background:rgba(34,197,94,0.15);
                                           color:#22c55e;border:1px solid rgba(34,197,94,0.4);
                                           border-radius:3px;cursor:pointer">저장</button>
                                <button onclick="toggleFieldEdit('${safeCode}','desc')"
                                    style="font-size:8px;padding:2px 5px;background:transparent;
                                           color:#666;border:1px solid #333;border-radius:3px;cursor:pointer">✕</button>
                            </div>
                        </div>
                    </div>
                </div>`;
            }).join('');
        }

        // ── 연면적 인라인 수정 ────────────────────────────────────────────────────────
        function toggleGfaEdit(code) {
            const view = document.getElementById(`blGfaView_${code}`);
            const edit = document.getElementById(`blGfaEdit_${code}`);
            if (!view || !edit) return;
            const opening = edit.style.display === 'none';
            view.style.display = opening ? 'none' : 'flex';
            edit.style.display = opening ? 'flex' : 'none';
            if (opening) document.getElementById(`blGfaInput_${code}`)?.focus();
        }

        async function saveGfa(code) {
            const input = document.getElementById(`blGfaInput_${code}`);
            if (!input) return;
            const val = parseFloat(input.value);
            if (isNaN(val) || val < 0) { alert('유효한 연면적(m²)을 입력하세요.'); return; }

            // GFA 업데이트 후 즉시 승인 (관리자 직접 수정)
            await patchJson(`/api/bim-land/admin/projects/${code}`, { gross_floor_area_m2: val });
            await postJson(`/api/bim-land/admin/gfa-review/${code}`, { action: 'approve', reviewer: 'admin' });
            loadBimLandData();
        }

        // ── 프로젝트명 / 설명 인라인 수정 ──────────────────────────────────────────────
        function toggleFieldEdit(code, field) {
            const suffix = field === 'name' ? 'Name' : 'Desc';
            const view = document.getElementById(`bl${suffix}View_${code}`);
            const edit = document.getElementById(`bl${suffix}Edit_${code}`);
            if (!view || !edit) return;
            const opening = edit.style.display === 'none';
            view.style.display = opening ? 'none' : 'flex';
            edit.style.display = opening ? 'flex' : 'none';
            if (opening) document.getElementById(`bl${suffix}Input_${code}`)?.focus();
        }

        async function saveField(code, field) {
            const suffix = field === 'name' ? 'Name' : 'Desc';
            const input = document.getElementById(`bl${suffix}Input_${code}`);
            if (!input) return;
            const val = input.value.trim();
            if (field === 'name' && !val) { alert('프로젝트명은 비워둘 수 없습니다.'); return; }

            const body = field === 'name'
                ? { project_name: val }
                : { description: val };

            const data = await patchJson(`/api/bim-land/admin/projects/${encodeURIComponent(code)}`, body);
            if (data.status === 'updated') {
                loadBimLandData();
            } else {
                alert('저장 실패: ' + (data.detail || JSON.stringify(data)));
            }
        }

        // ── 프로젝트 위치 주소 검색 이동 ────────────────────────────────────────────
        const _locSearchTimers = {};

        function toggleLocSearch(code) {
            const el = document.getElementById(`blLocSearch_${code}`);
            if (!el) return;
            const open = el.style.display === 'none' || !el.style.display;
            el.style.display = open ? 'block' : 'none';
            if (open) el.querySelector('input')?.focus();
        }

        // Nominatim 단일 호출 (countrycodes=kr, 한국어 우선)
        async function _nominatimQuery(q, limit = 6) {
            const url = 'https://nominatim.openstreetmap.org/search?' +
                new URLSearchParams({ q, format: 'json', limit,
                                      'accept-language': 'ko',
                                      addressdetails: 1, countrycodes: 'kr' });
            return fetch(url, { headers: { 'User-Agent': 'LuaBimLand/1.0' } }).then(r => r.json());
        }

        // 주소에서 건물명·상세번지 제거 → 행정구역 단위로 축약
        function _simplifyAddr(q) {
            return q
                .replace(/\s+\d+[-\s]?\d*[번길호층동]\S*/g, '')  // 번지·동호수 제거
                .replace(/\s+(B\d+|지하\d+|\d+F|\d+층)\b/gi, '')  // 층수 제거
                .trim();
        }

        function _renderLocItem(code, item) {
            const parts = item.display_name.split(',');
            const main  = item.address?.amenity || item.address?.building ||
                          item.address?.road || item.address?.suburb ||
                          item.address?.quarter || parts[0];
            const sub   = parts.slice(1, 4).map(s => s.trim()).filter(Boolean).join(' · ');
            return `<div onclick="selectLocAddr('${code}',${item.lat},${item.lon})"
                        style="padding:5px 8px;cursor:pointer;border-bottom:1px solid #222;font-size:10px"
                        onmouseover="this.style.background='rgba(226,185,111,0.1)'"
                        onmouseout="this.style.background=''">
                        <div style="color:#e2b96f">${main}</div>
                        <div style="color:#666;font-size:9px">${sub}</div>
                    </div>`;
        }

        function _manualCoordPanel(code) {
            const inputStyle = `flex:1;padding:3px 5px;font-size:9px;background:#111;
                border:1px solid #333;color:#ccc;border-radius:3px;min-width:0`;
            return `
                <div style="padding:6px 8px;border-top:1px solid #2a2a2a">
                    <div style="font-size:9px;color:#666;margin-bottom:4px">
                        📌 직접 좌표 입력
                        <span style="color:#444;margin-left:4px">네이버·카카오맵 우클릭 → 좌표 복사</span>
                    </div>
                    <div style="display:flex;gap:3px;margin-bottom:4px">
                        <input id="blLocManLat_${code}" type="number" placeholder="위도 37.xxx"
                               step="0.000001" style="${inputStyle}">
                        <input id="blLocManLng_${code}" type="number" placeholder="경도 127.xxx"
                               step="0.000001" style="${inputStyle}">
                    </div>
                    <button onclick="confirmManualCoords('${code}')"
                        style="width:100%;padding:3px;font-size:9px;background:rgba(226,185,111,0.15);
                               color:#e2b96f;border:1px solid rgba(226,185,111,0.4);border-radius:3px;cursor:pointer">
                        이 좌표로 이동
                    </button>
                </div>`;
        }

        function locSearchInput(code, q) {
            clearTimeout(_locSearchTimers[code]);
            const dd = document.getElementById(`blLocDrop_${code}`);
            if (!dd) return;
            if (!q || q.length < 2) { dd.innerHTML = ''; return; }
            dd.innerHTML = '<div style="padding:4px 6px;font-size:9px;color:#888">검색 중…</div>';
            _locSearchTimers[code] = setTimeout(async () => {
                try {
                    // 1차: 원본 쿼리
                    let results = await _nominatimQuery(q);

                    // 2차: 결과 부족 시 번지·건물명 제거 후 재시도
                    if (results.length < 2) {
                        const simple = _simplifyAddr(q);
                        if (simple && simple !== q) {
                            const more = await _nominatimQuery(simple);
                            const ids  = new Set(results.map(r => r.place_id));
                            results = [...results, ...more.filter(r => !ids.has(r.place_id))];
                        }
                    }

                    // 3차: 여전히 없으면 시·군·구 단위만 추출해서 재시도
                    if (results.length === 0) {
                        const regionMatch = q.match(/([가-힣]+(?:시|군|구|읍|면|동|리))/g);
                        const region = regionMatch ? regionMatch.slice(0, 2).join(' ') : '';
                        if (region) results = await _nominatimQuery(region);
                    }

                    const items = results.map(item => _renderLocItem(code, item)).join('');
                    dd.innerHTML = (items || '<div style="padding:5px 8px;font-size:9px;color:#888">검색 결과 없음</div>')
                                 + _manualCoordPanel(code);
                } catch(e) {
                    dd.innerHTML = '<div style="padding:4px 6px;font-size:9px;color:#f87171">검색 오류</div>'
                                 + _manualCoordPanel(code);
                }
            }, 420);
        }

        function confirmManualCoords(code) {
            const lat = parseFloat(document.getElementById(`blLocManLat_${code}`)?.value);
            const lng = parseFloat(document.getElementById(`blLocManLng_${code}`)?.value);
            if (isNaN(lat) || isNaN(lng)) { alert('위도와 경도를 모두 입력해주세요.'); return; }
            if (lat < 33 || lat > 43 || lng < 124 || lng > 132) {
                if (!confirm(`입력한 좌표(${lat}, ${lng})가 한국 범위를 벗어납니다. 그대로 적용할까요?`)) return;
            }
            selectLocAddr(code, lat, lng);
        }

        async function selectLocAddr(code, newLat, newLng) {
            newLat = parseFloat(newLat); newLng = parseFloat(newLng);

            // 검색창 닫기
            const searchEl = document.getElementById(`blLocSearch_${code}`);
            if (searchEl) searchEl.style.display = 'none';

            const circleData = _blCircleMap.get(code);
            const origLL     = circleData?.origLL || null;
            const movable    = circleData?.movable || [];

            if (!_blMap) {
                // 지도 미로드 — 좌표만 직접 저장 (최초 설정 가능)
                await _patchProjectCoords(code, newLat, newLng, origLL, []);
                loadBimLandData();
                return;
            }

            // 지도에 원이 있으면 시각적으로 이동
            movable.forEach(layer => layer.setLatLng([newLat, newLng]));
            _blMap.flyTo([newLat, newLng], Math.max(_blMap.getZoom(), 11), { duration: 1.2 });

            await _patchProjectCoords(code, newLat, newLng, origLL, movable);
        }

        // ── 위치 변경 요청 패널 ───────────────────────────────────────────────────
        function renderLocationRequests(reqs) {
            const el = document.getElementById('blLocationRequests');
            if (!el) return;
            if (!reqs || !reqs.length) {
                el.innerHTML = '<div class="bl-empty">요청 없음</div>';
                return;
            }
            el.innerHTML = reqs.map(r => {
                const isPending = r.status === 'pending';
                const statusColor = { pending:'#f59e0b', approved:'#22c55e', rejected:'#ef4444' }[r.status] || '#888';
                const date = (r.submitted_at || '').substring(0, 16);
                return `
                <div class="bl-claim-item" style="border-left:3px solid ${statusColor}">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <code style="font-size:9px;color:var(--accent-lua)">${r.request_id}</code>
                        <span style="font-size:9px;color:${statusColor}">${r.status.toUpperCase()}</span>
                    </div>
                    <div style="font-weight:600;font-size:10px;margin:2px 0">${r.project_name || r.project_code}</div>
                    <div style="font-size:9px;color:#aaa;margin-bottom:4px">
                        ${(r.prev_lat||0).toFixed(5)}, ${(r.prev_lng||0).toFixed(5)}
                        → <b style="color:#e2b96f">${(r.new_lat||0).toFixed(5)}, ${(r.new_lng||0).toFixed(5)}</b>
                    </div>
                    ${r.reason ? `<div style="font-size:9px;color:#ccc;margin-bottom:4px">사유: ${r.reason}</div>` : ''}
                    <div style="font-size:8px;color:var(--text-secondary)">요청: ${r.requester} · ${date}</div>
                    ${isPending ? `
                    <div style="display:flex;gap:4px;margin-top:6px">
                        <button onclick="resolveLocRequest('${r.request_id}','approve')"
                            style="flex:1;padding:3px;background:rgba(34,197,94,0.15);color:#22c55e;
                                   border:1px solid rgba(34,197,94,0.4);border-radius:4px;font-size:9px;cursor:pointer">
                            ✅ 승인
                        </button>
                        <button onclick="resolveLocRequest('${r.request_id}','reject')"
                            style="flex:1;padding:3px;background:rgba(239,68,68,0.12);color:#ef4444;
                                   border:1px solid rgba(239,68,68,0.4);border-radius:4px;font-size:9px;cursor:pointer">
                            ❌ 거절
                        </button>
                    </div>` : ''}
                </div>`;
            }).join('');
        }

        async function resolveLocRequest(requestId, action) {
            const data = await postJson(`/api/bim-land/admin/location-change-requests/${requestId}/resolve`, { action, reviewed_by: 'admin' });
            if (data.status === 'approved' || data.status === 'rejected') {
                loadBimLandData();
            }
        }

        // ── 연면적 검토 패널 ──────────────────────────────────────────────────────
        function renderGfaReview(projects) {
            const el = document.getElementById('blGfaReviewList');
            if (!el) return;
            if (!projects || !projects.length) {
                el.innerHTML = '<div class="bl-empty">검토 항목 없음</div>';
                return;
            }
            el.innerHTML = projects.map(p => {
                const gfa    = p.gross_floor_area_m2 || 0;
                const status = p.gfa_review_status || 'unset';
                const statusColor = { pending:'#f59e0b', approved:'#22c55e',
                                      suspended:'#ef4444', unset:'#6b7280' }[status] || '#888';
                const isPending   = status === 'pending' || status === 'unset';
                const isSuspended = status === 'suspended';
                const reviewedAt  = (p.gfa_reviewed_at || '').substring(0, 16);
                return `
                <div class="bl-claim-item" style="border-left:3px solid ${statusColor}">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <code style="font-size:9px;color:var(--accent-lua)">${p.project_code}</code>
                        <span style="font-size:9px;color:${statusColor}">${status.toUpperCase()}</span>
                    </div>
                    <div style="font-weight:600;font-size:10px;margin:2px 0">${p.project_name}</div>
                    <div style="font-size:10px;color:#e2b96f;margin:3px 0">
                        연면적: <b>${gfa > 0 ? gfa.toLocaleString() + ' m²' : '미입력'}</b>
                    </div>
                    ${status === 'unset' ? `
                    <div style="font-size:9px;color:#f59e0b;margin-bottom:4px">
                        ⚠️ 수행계획서 기반 연면적을 입력 후 재검토 요청하세요
                    </div>` : ''}
                    ${isSuspended && p.gfa_review_reason ? `
                    <div style="font-size:9px;color:#f87171;margin-bottom:4px">유보 사유: ${p.gfa_review_reason}</div>` : ''}
                    ${reviewedAt ? `<div style="font-size:8px;color:#555">검토: ${p.gfa_reviewed_by} · ${reviewedAt}</div>` : ''}
                    ${(isPending || isSuspended) ? `
                    <div style="display:flex;gap:4px;margin-top:6px">
                        <button onclick="reviewGfa('${p.project_code}','approve')"
                            style="flex:1;padding:3px;background:rgba(34,197,94,0.15);color:#22c55e;
                                   border:1px solid rgba(34,197,94,0.4);border-radius:4px;font-size:9px;cursor:pointer">
                            ✅ 승인
                        </button>
                        <button onclick="reviewGfa('${p.project_code}','suspend')"
                            style="flex:1;padding:3px;background:rgba(239,68,68,0.12);color:#ef4444;
                                   border:1px solid rgba(239,68,68,0.4);border-radius:4px;font-size:9px;cursor:pointer">
                            🚫 유보
                        </button>
                    </div>` : ''}
                </div>`;
            }).join('');
        }

        async function reviewGfa(code, action) {
            let reason = '';
            if (action === 'suspend') {
                reason = prompt('유보 사유를 입력하세요 (예: 수행계획서 미첨부, 과도한 면적 의심):', '') ?? '';
                if (reason === null) return;
            }
            const data = await postJson(`/api/bim-land/admin/gfa-review/${code}`, { action, reviewer: 'admin', reason });
            if (data.status === 'approved' || data.status === 'suspended') {
                loadBimLandData();
            }
        }

        // ── 주소 자동완성 (Nominatim / OpenStreetMap) ────────────────────────────
        let _addrTimer = null;
        let _isManualAddr = false;

        function debouncedAddrSearch(q) {
            clearTimeout(_addrTimer);
            const dd = document.getElementById('blAddrDropdown');
            if (!q || q.length < 2) { if (dd) dd.innerHTML = ''; return; }
            _addrTimer = setTimeout(() => _searchAddress(q), 420);
        }

        async function _searchAddress(q) {
            const dd = document.getElementById('blAddrDropdown');
            if (!dd) return;
            dd.innerHTML = '<div class="bl-addr-searching">검색 중…</div>';
            try {
                // 1차: 원본 쿼리
                let items = await _nominatimQuery(q);

                // 2차: 번지·건물명 제거 후 재시도
                if (items.length < 2) {
                    const simple = _simplifyAddr(q);
                    if (simple && simple !== q) {
                        const more = await _nominatimQuery(simple);
                        const ids  = new Set(items.map(r => r.place_id));
                        items = [...items, ...more.filter(r => !ids.has(r.place_id))];
                    }
                }

                // 3차: 시·군·구 단위 재시도
                if (items.length === 0) {
                    const regionMatch = q.match(/([가-힣]+(?:시|군|구|읍|면|동|리))/g);
                    const region = regionMatch ? regionMatch.slice(0, 2).join(' ') : '';
                    if (region) items = await _nominatimQuery(region);
                }

                const manualRow = '<div class="bl-addr-item" style="border-top:1px solid #2a3a5c" onclick="switchToManualFromSearch()">'
                    + '<div class="addr-sub" style="color:#e2b96f">✏️ 목록에 없으면 직접 좌표 입력</div></div>';

                if (!items.length) {
                    dd.innerHTML =
                        '<div class="bl-addr-item" onclick="switchToManualFromSearch()">'
                        + '<div class="addr-main" style="color:#e2b96f">검색 결과 없음</div>'
                        + '<div class="addr-sub">✏️ 직접 입력 모드로 전환하려면 클릭</div>'
                        + '</div>';
                    return;
                }

                dd.innerHTML = items.map(it => {
                    const parts = it.display_name.split(',');
                    const main  = it.address?.amenity || it.address?.building ||
                                  parts.slice(0, 3).join(', ');
                    const sub   = parts.slice(3, 6).join(', ');
                    const lat   = parseFloat(it.lat).toFixed(6);
                    const lon   = parseFloat(it.lon).toFixed(6);
                    const full  = it.display_name.replace(/'/g, '&#39;');
                    return `<div class="bl-addr-item" onclick="selectAddress('${lat}','${lon}','${full}')">
                        <div class="addr-main">${main}</div>
                        ${sub ? `<div class="addr-sub">${sub}</div>` : ''}
                    </div>`;
                }).join('') + manualRow;

            } catch {
                dd.innerHTML =
                    '<div class="bl-addr-item" onclick="switchToManualFromSearch()">'
                    + '<div class="addr-main" style="color:#e07070">검색 서버 연결 실패</div>'
                    + '<div class="addr-sub">✏️ 직접 입력 모드로 전환</div>'
                    + '</div>';
            }
        }

        function selectAddress(lat, lon, displayName) {
            document.getElementById('blProjAddr').value = displayName;
            document.getElementById('blProjLat').value  = lat;
            document.getElementById('blProjLng').value  = lon;
            document.getElementById('blProjAddrSearch').value =
                displayName.split(',').slice(0, 3).join(', ');
            document.getElementById('blAddrDropdown').innerHTML = '';
        }

        function switchToManualFromSearch() {
            document.getElementById('blAddrDropdown').innerHTML = '';
            if (!_isManualAddr) toggleAddrMode();
        }

        function toggleAddrMode() {
            _isManualAddr = !_isManualAddr;
            document.getElementById('blAddrAutoRow').style.display   = _isManualAddr ? 'none' : '';
            document.getElementById('blAddrManualRow').style.display = _isManualAddr ? 'flex' : 'none';
            document.getElementById('blAddrModeToggle').textContent  =
                _isManualAddr ? '🔍 자동 검색 모드' : '✏️ 직접 입력';
            document.getElementById('blAddrDropdown').innerHTML = '';
        }

        // ── 프로젝트 등록 ────────────────────────────────────────────────────────
        async function adminRegisterProject() {
            const name   = document.getElementById('blProjName')?.value?.trim();
            const team   = document.getElementById('blProjTeam')?.value?.trim();
            const person = document.getElementById('blProjPerson')?.value?.trim();
            if (!name)   { alert('프로젝트명은 필수입니다.'); return; }
            if (!team)   { alert('팀명은 필수입니다.'); return; }
            if (!person) { alert('담당자 이름은 필수입니다.'); return; }

            let addr, lat, lng;
            if (_isManualAddr) {
                addr = document.getElementById('blProjAddrManual')?.value?.trim() || '';
                lat  = parseFloat(document.getElementById('blProjLatManual')?.value || '0');
                lng  = parseFloat(document.getElementById('blProjLngManual')?.value || '0');
            } else {
                addr = document.getElementById('blProjAddr')?.value?.trim() || '';
                lat  = parseFloat(document.getElementById('blProjLat')?.value  || '0');
                lng  = parseFloat(document.getElementById('blProjLng')?.value  || '0');
            }

            const gfa   = parseFloat(document.getElementById('blProjGfa')?.value   || '0');
            const start = document.getElementById('blProjStart')?.value || '';
            const end   = document.getElementById('blProjEnd')?.value   || '';
            const disc  = (document.getElementById('blProjDisc')?.value || '')
                          .split(',').map(s => s.trim()).filter(Boolean);
            const desc  = document.getElementById('blProjDesc')?.value?.trim() || '';

            const data = await postJson('/api/bim-land/admin/projects', {
                project_name: name, team_name: team, person_name: person, address: addr,
                latitude: lat, longitude: lng, gross_floor_area_m2: gfa,
                disciplines: disc, start_date: start, end_date: end,
                description: desc, registered_by: 'admin'
            });

            if (data.status === 'registered') {
                alert(`✅ "${name}" 프로젝트가 등록되었습니다.\n자동 부여 코드: ${data.project_code}\n\n이제 참여자들은 Add-in에서 이력을 제출해야 XP를 획득할 수 있습니다.`);
                ['blProjName','blProjTeam','blProjPerson','blProjAddr','blProjAddrSearch','blProjAddrManual',
                 'blProjLat','blProjLng','blProjLatManual','blProjLngManual',
                 'blProjGfa','blProjStart','blProjEnd','blProjDisc','blProjDesc']
                    .forEach(id => { const el = document.getElementById(id); if (el) el.value = ''; });
                if (_isManualAddr) toggleAddrMode();
            } else if (data.status === 'already_exists') {
                alert(`⚠️ "${name}" 프로젝트는 이미 등록되어 있습니다.`);
            }
            loadBimLandData();
        }

        // ── 프로젝트 삭제 ────────────────────────────────────────────────────────────
        async function deleteProject(code) {
            const proj = (_blProjects || []).find(p => p.project_code === code);
            const name = proj?.project_name || code;
            if (!confirm(`"${name}" 프로젝트를 삭제하시겠습니까?\n\n이 작업은 되돌릴 수 없습니다.`)) return;
            const data = await fetchJson(`/api/bim-land/admin/projects/${encodeURIComponent(code)}`, { method: 'DELETE' });
            if (data.status === 'deleted') {
                loadBimLandData();
            } else {
                alert('삭제 실패: ' + (data.detail || JSON.stringify(data)));
            }
        }

        // ── 팀 이전 (이직) ──────────────────────────────────────────────────────────
        async function transferTeam(code) {
            const proj = (_blProjects || []).find(p => p.project_code === code);
            const currentTeam = proj?.team_name || '미등록';
            const newTeam = prompt(`현재 팀: ${currentTeam}\n\n이직 후 새 팀명을 입력하세요:`, currentTeam);
            if (!newTeam || newTeam.trim() === currentTeam) return;
            const reason = prompt('팀 이전 사유 (선택 입력):', '이직') || '이직';
            const data = await postJson(`/api/bim-land/admin/projects/${encodeURIComponent(code)}/transfer-team`, {
                new_team_name: newTeam.trim(),
                transferred_by: 'admin',
                reason
            });
            if (data.status === 'transferred') {
                alert(`✅ 팀 이전 완료\n${data.old_team} → ${data.new_team}`);
                loadBimLandData();
            } else {
                alert('팀 이전 실패: ' + (data.detail || JSON.stringify(data)));
            }
        }

        // 드롭다운 외부 클릭 시 닫기
        document.addEventListener('click', e => {
            const wrap = document.querySelector('.bl-addr-wrap');
            if (wrap && !wrap.contains(e.target)) {
                const dd = document.getElementById('blAddrDropdown');
                if (dd) dd.innerHTML = '';
            }
        });


// ═══════════════════════════════════════════════ BIM LAND JS END
