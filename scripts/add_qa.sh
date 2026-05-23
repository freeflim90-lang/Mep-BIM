#!/bin/zsh
# Q&A를 Obsidian NAS_Knowledge에 저장하는 대화형 입력 도구
# 사용법: ./scripts/add_qa.sh

set -euo pipefail

PROJECT_DIR="/Users/choejeong-yeon/LUA BIM LABS"
PYTHON="$PROJECT_DIR/.dev-venv/bin/python"

if [[ ! -x "$PYTHON" ]]; then
  PYTHON="$(command -v python3)"
fi

echo "──────────────────────────────────────"
echo " LUA BIM LABS  Q&A 지식 저장 도구"
echo "──────────────────────────────────────"
echo ""

echo "카테고리 선택:"
echo "  1) 팀원간질문"
echo "  2) 교육온보딩"
echo "  3) 클라이언트"
echo "  4) Claude대화"
printf "번호 [1]: "
read -r cat_num

case "${cat_num:-1}" in
  2) CATEGORY="교육온보딩" ;;
  3) CATEGORY="클라이언트" ;;
  4) CATEGORY="Claude대화" ;;
  *) CATEGORY="팀원간질문" ;;
esac

echo ""
echo "도메인 선택:"
echo "  1) BIM실무  2) Revit  3) Dynamo  4) MEP"
echo "  5) Navisworks  6) 조직운영  7) 개발기술  8) 기타"
printf "번호 [1]: "
read -r dom_num

case "${dom_num:-1}" in
  2) DOMAIN="Revit" ;;
  3) DOMAIN="Dynamo" ;;
  4) DOMAIN="MEP" ;;
  5) DOMAIN="Navisworks" ;;
  6) DOMAIN="조직운영" ;;
  7) DOMAIN="개발기술" ;;
  *) DOMAIN="BIM실무" ;;
esac

echo ""
printf "제목: "
read -r TITLE

if [[ -z "$TITLE" ]]; then
  echo "제목이 없으면 저장할 수 없습니다."
  exit 1
fi

echo ""
echo "질문 내용 (입력 완료 후 빈 줄에서 Ctrl+D):"
QUESTION=$(cat)

echo ""
echo "답변 내용 (입력 완료 후 빈 줄에서 Ctrl+D):"
ANSWER=$(cat)

echo ""
printf "출처 (사람 이름, 채널 등, 비워도 됨): "
read -r SOURCE

echo ""
"$PYTHON" "$PROJECT_DIR/scripts/save_qa.py" add \
  --title "$TITLE" \
  --q "$QUESTION" \
  --a "$ANSWER" \
  --category "$CATEGORY" \
  --domain "$DOMAIN" \
  --source "$SOURCE"

echo ""
echo "저장 완료. Obsidian에서 NAS_Knowledge 폴더를 확인하세요."
