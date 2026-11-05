# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：The plain LLM has no way to know this course. The agent first looked it up with `search_glossary` and gave the real answer: 基礎・実装・発展, and doing one of them is enough.
- `--trace` で見えたツール呼び出し（ツール名と引数）：For "LoRAとQLoRAの違いは？": `search_glossary({'query': 'LoRA'})` and `search_glossary({'query': 'QLoRA'})`, one term per call.
- 1つの質問での LLM 呼び出し回数（`requests`）：2 (`tool_calls=2`).
- 追加したツールと、docstring に書いた説明：`make_quiz(lecture)`. It picks a random glossary term from that lecture and returns a question and the answer. Docstring: use it when the user asks for a review question or a quiz about a lecture. For "第2回の内容から確認問題を1問出して" the model called `make_quiz({'lecture': 2})` and showed only the question (about SFT), not the answer.

## 宿題

- 取り組んだレベル：実装
- やったこと：I added `save_learning_log(title, content)`, which saves a note as a Markdown file in `learning_log/`. I registered it with `requires_approval=True` and added `DeferredToolRequests` to the agent's `output_type`. In the CLI, when the agent stops for approval, I show the tool call and ask `Save? [y/N]`, then run the agent again with the previous messages and my answer. Anything other than `y` counts as no.
- 結果：
  - `uv run pytest -q`: 14 passed.
  - "今日学んだLoRAの要点を学習ログに保存して" + `n`: the model called `search_glossary('LoRA')`, then `save_learning_log`, and the run stopped at `Save? [y/N]`. Nothing was written (`learning_log/` did not even exist).
  - Same question + `y`: the file `learning_log/20261104-235945_LoRAの要点.md` was created with the summary.
  - "LoRAとは？": only `search_glossary` was called. No save, no prompt.
- 気づき・疑問：
  - When I answered `n`, the tool returned "The tool call was denied", but the model still replied 「学習ログを保存しました」. The file was not written, so the approval in the code worked, but the final message from the model was wrong. The check has to be in the program, not in the prompt. A clearer denial message or a line in `INSTRUCTIONS` could help the model report it correctly.
  - The model put its own `# heading` in `content`, so the saved file has the title twice.
  - Approval adds one more run of the agent, so one more LLM call.
