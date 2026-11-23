# 第5回 解答

## 演習

- 回答モデル（実行時の`[model]`）：`gemini-3.5-flash-lite`
- 比較した質問：第2回の説明では、LoRAは何を固定し何を学習しますか？ QLoRAは何を加えますか？
- 対象資料（全文投入と他の方式で範囲が違う点も記録）：Vector / Tree / Graph use the 214 pages of lectures 1–3. Full context uses all 9 documents (438 pages, 227,971 characters). So full context had much more material, not the same conditions.

### 各方式の結果

| 方式 | 回答の要点・正しさ | 引用ページと根拠 | 時間（秒） | 入力／出力トークン数 | モデル応答回数 | 生成API推定費用（USD） |
|---|---|---|---|---|---|---|
| 全文投入 | Treated the question as homework and only gave "hints": LoRA freezes the base weights and learns two small matrices A·B (correct). For QLoRA it only said "how the weights are compressed (bit count)"; it never said 4-bit quantization. Partly correct, not a direct answer | 第2回 PDF p.51, p.52 | 90.40 | 117,025 / 175 | 1 | 0.004589 |
| ベクトル検索 | Correct: base weights frozen, only the low-rank matrices A·B are learned; QLoRA adds 4-bit quantization of the base model | 第2回 PDF p.51, p.52 | 2.63 | 3,341 / 234 | 2 | 0.001587 |
| Tree | Correct, mentions quantization and 4-bit | 第2回 PDF p.52 | 5.53 | 9,229 / 325 | 5 | 0.003581 |
| Graph | Correct, mentions quantization and 4-bit | 第2回 PDF p.51, p.52 | 3.53 | 5,775 / 234 | 2 | 0.002318 |

- 検索だけを実行して見つかったページと、その本文で確認できたこと：`uv run python -m app.retrieval "LoRA QLoRA 違い"` returned 第2回「基盤モデルの仕組み」 pages 52, 51, 60, 47, 61 in that order. p.52 and p.51 are the ones that actually answer the question; the others only share words (LoRA, fine-tuning).
- `--trace`で見えたツール呼び出し（ツール名・引数・回数、Treeでたどった目次など）：
  - Vector: 1 call, `search_materials({'query': 'LoRA 固定 学習 QLoRA 追加'})`
  - Tree: 4 calls, `browse_tree({})` → `lec02-main` → `lec02-main-s045` → `lec02-main-p052`
  - Graph: 1 call, `search_graph({'query': 'LoRA 固定 学習 QLoRA 追加'})`
- 取得した情報が足りなかった例、取得できたのに回答へ使えなかった例：Full context had p.51 and p.52 in the input and cited them, but did not use them to answer: it followed the "don't give homework answers" instruction and only gave hints, and the QLoRA part stayed vague. The information was there; the model did not use it.
- 今回の用途に採用したい方式と、その理由・比較条件の限界：Vector search. It found the right pages first, was the fastest and cheapest, and gave a direct, correct answer. Tree also worked but needed 5 model calls and almost 3× the tokens. Limits: one question, one run per method, and full context used a bigger set of documents. A question that needs pages from different chapters could change the result.
- 気づき・疑問：
  - Full context used about 35× more input tokens than vector search and took 90 s, and the answer was worse.
  - On the first try (and for about 30 minutes) almost every run failed with HTTP 503 "high demand", for `gemini-3.5-flash-lite`, `gemini-3.5-flash` and `gemini-3.1-flash-lite`. Retrieval alone (no generation) worked. I reran later with retries. The Graph run that worked during the 503 period took 14.65 s; the later one took 3.53 s, so time depends a lot on the API load. Logs: `lectures/05/runs/`.

## 宿題

- 取り組んだレベル：基礎
- やったこと（変更したファイル・設定・処理、または設計した取得方法）：I changed only `RAG_TOP_K` in `app/config.py` from 5 to 2 and ran the same question with vector search. Then I set it back to 5.
- 比較した質問と、固定した条件（モデル・対象資料など）：The same question as above. Same model (`gemini-3.5-flash-lite`), same documents (lectures 1–3), same instructions.
- 結果（変更前後の回答・根拠、`--trace`の出力、時間・トークン数・生成API推定費用など）：

  | RAG_TOP_K | tool call | 引用ページ | 時間（秒） | 入力／出力トークン数 | 応答回数 | 費用（USD） |
  |---|---|---|---|---|---|---|
  | 5 | `search_materials('LoRA 固定 学習 QLoRA 追加')` | 第2回 p.51, p.52 | 2.63 | 3,341 / 234 | 2 | 0.001587 |
  | 2 | `search_materials('LoRA QLoRA 固定 学習')` | 第2回 p.51, p.52 | 3.62 | 2,050 / 204 | 2 | 0.001125 |

  Both answers are correct (base weights frozen, low-rank A·B learned, QLoRA adds 4-bit quantization).
- 改善した例と、残る失敗・制約：With top-2, input tokens went down 39% and cost 29%, with the same pages and the same answer, because p.52 and p.51 were already the top two results. Time did not improve (2.63 → 3.62 s), which is probably API load, not the setting. The risk: a question that needs pages from different places (for example lecture 3 p.13, 39, 40) would lose evidence with top-2.
- 気づき・疑問：Fewer pages is good only when the search ranks the right pages first. For this question 2 was enough, but I would not use 2 as a fixed value. It would be better to decide the number by question type, or to check a small set of questions with known pages before changing it.
