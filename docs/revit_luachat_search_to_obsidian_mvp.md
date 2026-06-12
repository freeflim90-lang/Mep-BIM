# Revit LUAChat Search-to-Obsidian MVP

## Direction

Use LUAChat first as a search-assisted chatbot, then capture every useful question and answer as an Obsidian knowledge candidate.

```text
Revit Add-in
-> LUA BIM LABS backend
-> local Obsidian / knowledge_base search
-> web/search supplement when local score is low
-> answer user
-> save Q/A, sources and gaps to Obsidian
```

## Knowledge Policy

Search-assisted answers are not treated as approved knowledge.

They are saved as review candidates:

```text
status: search-assisted-needs-review
source_mode: search-assisted
tags: QA, revit-assistant, knowledge-loop, search-assisted
```

The candidate should be promoted later only after review or repeated successful use.

## Promotion Flow

1. User asks a Revit/BIM question.
2. Backend searches local knowledge first.
3. If local score is low, backend supplements with search.
4. Backend returns a practical answer.
5. Obsidian receives a Q/A note with sources and search evidence.
6. The same answer is appended to the agent QA file as `needs-review`.
7. A human or curator later promotes stable entries to approved knowledge.

## Why This MVP

- No need to finish a perfect knowledge base before release.
- Real user questions become the roadmap.
- Search API cost and quality can be controlled in the backend.
- API keys remain server-side, not inside the add-in.
- Obsidian becomes the review queue and knowledge growth record.

## Guardrail

Do not directly promote search output into approved guidance. Keep search-assisted content as candidate material until reviewed.
