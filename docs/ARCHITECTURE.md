# OpenBot Team Architecture & Collaboration

```mermaid
flowchart TD
    User([User / Boss]) -->|Direct Request| TM[Task Manager\ngpt-oss-120b-medium]
    
    subgraph OpenBot Multi-Agent Mesh
        TM -->|Delegate Search / Shopping| SB[Search Bot\ngrok-4.6]
        TM -->|Delegate Document Processing| CG[ChatGPT Worker\ngpt-6.1-sol]
        TM -->|Delegate Web Development| WC[Website Creator\ngemini-3.8-flash]
        TM -->|Delegate Email Management| GM[Gmail Bot\ngemini-3.8-flash]
        TM -->|Delegate Git & Repo Ops| GH[Github Bot\ngemini-3.8-flash]
        
        SB -.->|Share Results| TM
        CG -.->|Share PDFs / Takeoffs| TM
        WC -.->|Deploy Sites / Demos| TM
        GM -.->|Fetch / Draft Emails| TM
        GH -.->|Push Code / Sync| TM
    end

    subgraph Shared Resources & Skills
        WC --- S1[openbot-site-hosting]
        TM --- S2[openbot-data]
        GH --- S3[openbot-skill-creator]
        SharedStorage[(OpenBot Shared Workspace)]
    end
```

## Agent Roles & Responsibilities

| Agent | Model | Provider | Core Responsibilities |
|---|---|---|---|
| **Task Manager** | `gpt-oss-120b-medium` | Antigravity | Central orchestrator. Coordinates multi-step workflows, delegates subtasks, and combines deliverables. |
| **Search Bot** | `grok-4.6` | Grok | Deep web research, comparative pricing, materials pricing analysis, and structured catalog comparisons. |
| **ChatGPT Worker** | `gpt-6.1-sol` | Codex | Complex analysis, video/transcript processing, statement-of-work (SOW) parsing, and takeoff generation. |
| **Website Creator** | `gemini-3.8-flash` | Antigravity | Full-stack frontend development, catalog generators, interactive presentations, and local site hosting. |
| **Gmail** | `gemini-3.8-flash` | Antigravity | Monitoring, reviewing, summarizing incoming client/vendor emails, and staging drafted replies. |
| **Github Bot** | `gemini-3.8-flash` | Antigravity | Managing git branches, commits, PRs, releases, issue tracking, and repository lifecycle. |
