# Daily Blogger Queue

Daily flow:

1. Read the first JSON topic from `content/blogger_queue/`.
2. Render it into an English MEP BIM blog post.
3. Publish it to Blogger.
4. Delete the JSON topic file after successful publishing.
5. Write only title and URL to `logs/blogger_daily_publish.jsonl`.

The published article body is not kept locally after upload.

## Seed Topics

This fills the queue with a full 365-topic annual MEP BIM training plan. Existing topic files are not overwritten.

```bash
python3 scripts/daily_blogger_queue_publish.py --seed-topics
```

Current topic system covers MEP BIM coordination, HVAC duct BIM, HVAC piping BIM, plumbing and sanitary BIM, fire protection BIM, electrical BIM, Revit MEP workflow, Navisworks workflow, BIM data and QA, BIM automation, project case studies, and daily BIM career training.

## Test Without Publishing

```bash
python3 scripts/daily_blogger_queue_publish.py --dry-run
```

## Publish One Queued Topic

```bash
python3 scripts/daily_blogger_queue_publish.py
```

## Install Daily macOS Schedule

```bash
mkdir -p ~/Library/LaunchAgents
cp config/launch_agents/com.luabimlab.daily-blogger-post.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.luabimlab.daily-blogger-post.plist
```

Default schedule: every day at 08:00.

## Stop Schedule

```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.luabimlab.daily-blogger-post.plist
```
