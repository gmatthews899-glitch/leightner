# Claude Code Instructions

**Read `AGENTS.md` first. All rules in that file apply.**

This file adds Claude-specific notes on top of the shared agent instructions.

---

## Claude-specific guidance

### Use extended thinking before substantial changes
For any non-trivial task (new feature, refactor, debugging a real error), take the time to think through the approach before generating code. The operator is not a developer — if your first attempt is wrong, they cannot easily diagnose why. Get it right the first time by thinking it through first.

### When the operator pastes code or errors
- Read them carefully before reacting
- Quote the specific line or message you are responding to, so the operator can follow along
- Do not summarize error messages away — the actual text of the error is the evidence

### Long conversations
- When context gets long, proactively suggest the operator start a new conversation for a new task
- Before that happens, write a brief summary of current state they can paste into the new conversation

### File reads
- Before editing any file, read it fresh. Do not rely on what you think is in it from earlier in the conversation. Files change, including from tool calls the operator ran themselves.

### The operator works with another Claude in a separate chat for planning
The operator plans the project in a separate Claude conversation where `PROJECT_CONTEXT.md` lives. That Claude writes prompts that get pasted to you here in Claude Code. You are the executor; the other Claude is the architect. This means:

- Prompts from the operator may be carefully scoped — respect the scope precisely, do not expand it
- If a prompt seems too narrow and you think something important is missing, say so before proceeding — but wait for confirmation before acting
- The operator may reference decisions made in the other conversation that aren't in the code yet. Check `PROJECT_CONTEXT.md` before asking them to re-explain

---

## Everything else is in `AGENTS.md` — read that file.
