# OpenBot Team Setup Guide

This guide describes how to import and run this OpenBot team on another machine.

## Prerequisites
- OpenBot runtime installed on Windows, macOS, or Linux.
- API keys or provider connections configured for:
  - Antigravity / Gemini
  - Grok (xAI)
  - Codex / OpenAI ChatGPT Plus

## Import Methods

### Option A: OpenBot UI Import
1. Clone this repository:
   ```bash
   git clone https://github.com/barryedwardmiller-beep/openbot-team.git
   ```
2. Open OpenBot and navigate to **Agents Settings**.
3. Import the team using `team-manifest.json` or create agents matching the profiles in `agents/*/profile.json`.

### Option B: Direct Workspace Placement
1. Copy the skill directories in `skills/` to your OpenBot skills folder or your agents' `.agents/skills/` directories.
2. Place the agent utility scripts into their respective workspace directories.
3. Configure the agent profiles as defined in `team-manifest.json`.
