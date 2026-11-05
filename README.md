# OpenBot Multi-Agent Team

Production multi-agent team configuration exported from OpenBot. This repository contains the complete agent roster, architectural documentation, skills, routines, and worker utilities ready for deployment.

---

## 👥 The Agent Team

```
                                  ┌───────────────────┐
                                  │   Task Manager    │
                                  │ (Lead Orchestrator)│
                                  └─────────┬─────────┘
        ┌───────────────────┬───────────────┼───────────────┬───────────────────┐
        ▼                   ▼               ▼               ▼                   ▼
┌───────────────┐   ┌───────────────┐ ┌───────────┐ ┌───────────────┐   ┌───────────────┐
│  Search Bot   │   │ChatGPT Worker │ │Website    │ │     Gmail     │   │  Github Bot   │
│ (Comparisons) │   │ (Analysis/SOW)│ │  Creator  │ │(Email Summaries)│ │ (Source Sync) │
└───────────────┘   └───────────────┘ └───────────┘ └───────────────┘   └───────────────┘
```

| Agent Name | Model | Provider | Description |
|---|---|---|---|
| **Task Manager** | `gpt-oss-120b-medium` | Antigravity | Managing and orchestrating all team bots |
| **Search Bot** | `grok-4.6` | Grok | Web search, product discovery, and comparative shopping |
| **ChatGPT Worker** | `gpt-6.1-sol` | Codex | SOW analysis, takeoff extraction, and transcription |
| **Website Creator** | `gemini-3.8-flash` | Antigravity | Design and frontend web application development |
| **Gmail** | `gemini-3.8-flash` | Antigravity | Email review, summarization, and outbound drafting |
| **Github Bot** | `gemini-3.8-flash` | Antigravity | GitHub account automation, repositories, and sync |

---

## 📁 Repository Structure

```
├── README.md                  # Executive overview and quick start (this file)
├── team-manifest.json         # Complete machine-readable configuration of all agents
├── agents/                    # Individual agent profiles, readmes, and scripts
│   ├── task-manager/          # Lead orchestrator configuration
│   ├── github-bot/            # GitHub automation bot configuration
│   ├── website-creator/       # Web builder bot configuration and scripts
│   ├── search-bot/            # Price comparison & shopping bot configuration
│   ├── chatgpt-worker/        # Document analysis & transcription bot configuration
│   └── gmail/                 # Email management bot configuration
├── skills/                    # Reusable OpenBot agent skills
│   ├── openbot-data/          # Cross-agent structured database persistence
│   ├── openbot-site-hosting/  # Static site deployment and management
│   └── openbot-skill-creator/ # Dynamic skill generation engine
├── routines/                  # Automated agent routines and background jobs
└── docs/                      # Architectural diagrams and setup documentation
    ├── ARCHITECTURE.md        # Detailed agent mesh and communication diagrams
    └── SETUP.md               # Guide to importing and running the bots
```

---

## 🚀 Quick Start for Management

1. **Clone the repository:**
   ```bash
   git clone https://github.com/barryedwardmiller-beep/openbot-team.git
   ```
2. **Review Team Setup:**
   - Inspect [team-manifest.json](team-manifest.json) for the full JSON configuration.
   - Read [ARCHITECTURE.md](docs/ARCHITECTURE.md) for how the bots collaborate.
   - Refer to [SETUP.md](docs/SETUP.md) for import and environment requirements.

---

*Exported automatically by Github Bot.*
