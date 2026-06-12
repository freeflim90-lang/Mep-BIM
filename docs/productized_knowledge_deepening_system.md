# LUA BIM LABS Productized Knowledge Deepening System

## Purpose

LUA BIM LABS should treat each paid service as both a product and a controlled knowledge collection channel.

The goal is to grow from a daily education service into a deeper MEP BIM mentoring and coordination knowledge system without mixing public content, client records, project-sensitive material, and reusable expert knowledge.

## Product Knowledge Layers

### 1. Starter

Service type:

- Daily general MEP BIM education
- Beginner-friendly concepts
- Basic checklists
- No project-specific review

Knowledge collected:

- Which topics attract applications
- Which daily lessons produce questions
- Beginner pain points
- Common terminology gaps
- Reusable public education snippets

Obsidian location:

```text
NAS_Knowledge/Blog_MEP_BIM
NAS_Knowledge/Starter_Plan_Clients
NAS_Knowledge/Product_Knowledge/Starter
```

Allowed reuse:

- Public blog topics
- Telegram daily lessons
- Beginner FAQs
- Starter onboarding improvements

Do not collect:

- Confidential project files
- Private drawings
- Client contracts
- Personal data beyond service operation

### 2. Personal Tutor

Service type:

- Personalized MEP BIM learning path
- Level diagnosis
- Weak-point tracking
- Limited Telegram Q&A

Knowledge collected:

- Client level diagnosis patterns
- Revit MEP skill gaps
- Discipline-specific learning blockers
- Personalized lesson templates
- Repeated Q&A patterns

Obsidian location:

```text
NAS_Knowledge/Product_Knowledge/Personal_Tutor
NAS_Knowledge/Client_Learning_Profiles
```

Allowed reuse:

- Anonymized skill-gap patterns
- Personalized curriculum templates
- Generalized Q&A
- Level diagnosis rubrics

Needs review before reuse:

- Any client-specific context
- Screenshots or examples from client work
- Questions that imply project information

### 3. Coordinator Mentor

Service type:

- BIM coordination workflow mentoring
- Clash review thinking
- Issue prioritization
- Weekly coordination direction

Knowledge collected:

- Coordination decision patterns
- Clash classification examples
- Model QA checklist improvements
- Meeting note structures
- RFI and issue tracking workflows

Obsidian location:

```text
NAS_Knowledge/Product_Knowledge/Coordinator_Mentor
NAS_Knowledge/MEP_Coordination_Playbook
```

Allowed reuse:

- Anonymized coordination cases
- General QA checklist patterns
- Clash triage methods
- Meeting and reporting templates

Restricted:

- Real project names
- Model files
- Drawings
- Clash reports unless explicitly anonymized and permission-cleared

### 4. Project Mentor

Service type:

- Custom project-specific mentoring
- Higher-risk consulting support
- Workflow and QA advisory

Knowledge collected:

- Project mentoring playbooks
- Scope definition patterns
- Risk and decision logs
- Contracted deliverable boundaries
- Custom workflow templates

Obsidian location:

```text
NAS_Knowledge/Product_Knowledge/Project_Mentor
NAS_Knowledge/Project_Mentor_Private_Review
```

Allowed reuse:

- Only fully anonymized and generalized lessons
- Internal process improvements
- Non-client-specific templates

Requires explicit review:

- Any project-derived example
- Any deliverable
- Any issue involving code, approval, design responsibility, or construction decision

## Knowledge Promotion Flow

Use four stages:

```text
Raw Intake -> Reviewed Insight -> Product Knowledge -> Public/Training Reuse
```

### Raw Intake

Examples:

- Blog post note
- Telegram question
- Google Form learning goal
- Client onboarding note
- Mentor session note

Rule:

- Keep raw notes close to their source.
- Mark private or client-related material clearly.

### Reviewed Insight

Examples:

- Common beginner mistake
- Repeated Revit MEP blocker
- Frequent clash classification issue
- Useful checklist item

Rule:

- Remove personal and project identifiers.
- Add product level and reuse tags.

### Product Knowledge

Examples:

- Starter FAQ
- Personal Tutor diagnosis rubric
- Coordinator Mentor clash triage checklist
- Project Mentor scope boundary template

Rule:

- Store in `NAS_Knowledge/Product_Knowledge/<Plan>`.
- Include source type, risk level, and reuse status.

### Public/Training Reuse

Examples:

- Blog article
- Telegram daily lesson
- Paid lesson module
- Onboarding checklist

Rule:

- Only use public-safe or anonymized content.
- Avoid legal, code-compliance, construction approval, and engineering verification claims.

## Tags

Use these tags consistently:

```text
product/starter
product/personal-tutor
product/coordinator-mentor
product/project-mentor
source/blog
source/telegram
source/google-form
source/client-session
risk/public-safe
risk/client-private
risk/project-sensitive
reuse/public-blog
reuse/telegram-lesson
reuse/paid-curriculum
reuse/internal-only
review/needed
review/approved
```

## Review Rules

Public-safe:

- General concept
- No client/project identity
- No confidential file content
- No legal/code/design approval claim

Client-private:

- Client learning profile
- Payment/service information
- Personal learning weakness
- Telegram chat ID or email

Project-sensitive:

- Real project context
- Drawings, files, models, reports
- Approval, code, design, or construction decisions

## Monthly Product Learning Review

Once per month:

1. Review new Starter questions and learning goals.
2. Identify top 10 repeated beginner issues.
3. Convert safe insights into Starter lessons.
4. Promote deeper patterns into Personal Tutor curriculum.
5. Promote coordination patterns into Coordinator Mentor playbook.
6. Keep project-sensitive material private unless explicitly reviewed.

## Launch Sequence

1. Starter: validate demand and topic interest.
2. Personal Tutor: introduce diagnosis and personalized path.
3. Coordinator Mentor: introduce coordination workflow mentoring.
4. Project Mentor: introduce custom high-scope service with clear contract boundaries.

