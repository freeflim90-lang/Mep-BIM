# Starter Plan 레퍼런스 카드 (다국어)

Day 7·14·21·28·38·47·54·60에 텔레그램으로 발송하는 빠른 참조 카드 8종.
영어 원본(.md)을 번역해 언어별 PDF를 생성한다.

## 구조

```
reference_cards/
  card_0N_*.md          # 영어 원본 (편집은 여기서)
  card_0N_*.pdf         # 영어 PDF
  ko/  card_0N_*.md|pdf # 한국어
  ja/  …                # 일본어
  zh/  …                # 중국어(간체)
  ar/  …                # 아랍어(RTL)
```

발송기는 `get_card_path(filename, language)`로 `reference_cards/<lang>/`을
우선 찾고, 없으면 루트의 영어본으로 폴백한다(send_starter.py·send_daily.py).
현지화 PDF가 있는 언어: **ko·ja·zh·ar**. 그 외 언어는 영어로 폴백.

## 재생성

```bash
make starter-localize          # ko/ja/zh/ar 번역(누락분)+PDF 전부 재생성
```

또는 개별로:

```bash
python3 scripts/bim_education/translate_reference_cards.py --lang ko [--force]
python3 scripts/generate_reference_card_pdfs.py --lang ko --force
```

- **영어 원본(.md)을 수정한 경우** translate에 `--force`를 붙여 재번역.
- PDF는 고정 생성일을 박으므로 내용이 같으면 재생성해도 바이트 동일(멱등).

## 폰트 / 렌더링

| 언어 | 폰트 | 비고 |
|------|------|------|
| ko | AppleSDGothicNeo | |
| ja | Hiragino | |
| zh | STHeiti | |
| ar | Arial Unicode | RTL — arabic_reshaper + python-bidi로 글자결합·양방향 |
| 폴백 | Arial Unicode | ja/zh/ko/ar 글리프 모두 포함 |

의존성: `fpdf2`, `arabic-reshaper`, `python-bidi` (requirements-dev.txt).

## 알려진 이슈 / 검수 포인트

- **아랍어 브랜드 음역**: DeepSeek가 "LUA BIM LABS"를 아랍어로 음역할 때가 있다.
  Latin "LUA BIM LABS"로 정규화해야 푸터 스킵·부제 렌더가 정상.
- **렌더 검수**: 하니스 PDF 미리보기는 CJK/아랍 서브셋이 깨져 보일 수 있다.
  실제 확인은 `qlmanage -t -s 1000 -o <dir> <pdf>`로 PNG를 뽑아서 본다.
- 표 셀이 길면 행 높이 차로 살짝 겹칠 수 있다(영어본 포함 공통, 가독성엔 무방).
