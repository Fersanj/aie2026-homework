# AI Engineering 2026 – Homework (Fer)

| Lecture | Content |
|---|---|
| [02](lectures/02/answer.md) | LoRA format tuning — Implementation level (own FAQ topic: fictional evacuation drill) |
| [03](lectures/03/answer.md) | AI agents (Pydantic AI) — Implementation level: `save_learning_log` with human approval (`requires_approval=True`) |

Files for lecture 02:
- `lectures/02/answer.md` – assignment write-up (level, data changes, results, reflection)
- `lectures/02/lora_format_tuning_tarea_implementacion.ipynb` – notebook with my own dataset
- `lectures/02/results/` – `result.json`, `eval_before.json`, `eval_after.json` from my Colab (T4) run

Files for lecture 03 (course code from `matsuolab/lecture-ai-engineering-2026`, with my changes):
- `lectures/03/answer.md` – exercise + assignment write-up
- `app/tools.py` – added `make_quiz` (exercise) and `save_learning_log` (assignment)
- `app/agent.py` – registered both tools, `requires_approval=True`, `output_type=[str, DeferredToolRequests]`, approval loop in the CLI
- `tests/test_learning_log.py` – tests for the new tools and the approve/deny flow (no API key needed)

Run in Codespaces: `uv run pytest -q` · `uv run python -m app.agent --trace "今日学んだLoRAの要点を学習ログに保存して"`
