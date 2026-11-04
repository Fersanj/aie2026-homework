# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：[ ]
- `--trace` で見えたツール呼び出し（ツール名と引数）：[ ]
- 1つの質問での LLM 呼び出し回数（`requests`）：[ ]
- 追加したツールと、docstring に書いた説明：`make_quiz(lecture)`. It picks a random glossary term from that lecture and returns a question and the answer. Docstring: use it when the user asks for a review question or a quiz about a lecture.

## 宿題

- 取り組んだレベル：実装
- やったこと：I added `save_learning_log(title, content)`, which saves a note as a Markdown file in `learning_log/`. I registered it with `requires_approval=True` and added `DeferredToolRequests` to the agent's `output_type`. In the CLI, when the agent stops for approval, I show the tool call and ask `Save? [y/N]`, then run the agent again with the previous messages and my answer. Anything other than `y` counts as no.
- 結果：[ ]
- 気づき・疑問：[ ]
