# 第1回 解答

## 演習

- 講座に固有の質問（宿題の3レベル）へのモデルの回答（要約でよい）：It did not know the course. It gave a "general" answer: レベル1 基礎・ベーシック, レベル2 応用・スタンダード, レベル3 発展・アドバンスド, and told me to check the course materials.
- 用語集の正しい意味と比べて気づいたこと：The glossary (`homework-levels`) says the levels are 基礎・実装・発展, and doing any one of them is enough. The model got 基礎 and 発展 right by chance, but the middle one is wrong (応用 instead of 実装), and it presents them as difficulty grades, not as "pick one". It sounds confident even though it is guessing. For "LoRAとは何ですか？" (a general term) the answer was correct.
- 表示できたトークン数（入力 / 出力）：LoRA question: 7 / 682. 3レベル question: 21 / 611 (`gemini-3.5-flash-lite`). I added this to `app/ask.py` with `response.usage_metadata.prompt_token_count` and `candidates_token_count`.

## 宿題

- 取り組んだレベル：基礎
- やったこと：I asked the same question (「AIE2026の講座の宿題にある「3レベル」とは何ですか？」) 3 times with `gemini-3.5-flash-lite` and 3 times with `gemini-3.5-flash` (`AIE_MODEL`). Outputs are in `lectures/01/runs/`.
- 結果：

  | model | run | input / output tokens | the 3 levels it gave |
  |---|---|---|---|
  | flash-lite | 1 | 21 / 592 | 初級・中級・上級 style, then "pick one or do all in order" |
  | flash-lite | 2 | 21 / 473 | 基礎 / 応用 / 発展・挑戦 |
  | flash-lite | 3 | 21 / 532 | 基礎・入門 / 応用・実践 / 発展・挑戦 |
  | flash | 1 | 21 / 581 | 基礎・必須 / 応用・標準 / 発展・挑戦 |
  | flash | 2 | 21 / 668 | 基礎・必須 / 応用・標準 / 発展・挑戦 |
  | flash | 3 | 21 / 685 | 基礎・必須 / 応用・標準 / 発展・チャレンジ |

  Correct answer (glossary): 基礎・実装・発展, any one is enough.
- 気づき・疑問：
  - None of the 6 answers knew the course. All of them said "in general" and guessed. No run said 実装.
  - flash-lite changed more between runs (one run used 初級・中級・上級 and did not even give a fixed list). flash gave almost the same structure all 3 times, and its answers were longer (about 645 output tokens on average vs about 530).
  - Being more consistent did not make flash more correct. It was consistently wrong, and it even called level 1 "必須" (required), which is not true for this course. Asking several times can show that the model is guessing, but it cannot fix missing knowledge. For course-specific facts the model needs the course data (this is what the agent with the glossary does in lecture 3).
