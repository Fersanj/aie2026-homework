# 第4回 解答

## 演習

- 基準別の一致率（直す前）：根拠 9/10、範囲 9/10、ヒント 10/10、分かりやすさ 9/10、回の表示 10/10 (overall 10/10, coverage 100%, `gemini-3.5-flash-lite`)
- 要確認の件数（直す前）：0
- 直した基準と、書き足した方針：There was no unsure item, so I took #05 (RAG), the one I marked as "迷った". Under 根拠 I added: 「用語集にない語を、「用語集にはない」と伝えたうえで一般的に説明するのは、断定ではない（pass）」, and removed that point from 「まだ決めていないこと」.
- 基準別の一致率と要確認の件数（直した後）：根拠 9/10、範囲 10/10、ヒント 10/10、分かりやすさ 10/10、回の表示 10/10. 要確認 0. #05 stayed pass, so the new line did not change it, but now the rubric decides it instead of leaving it to the model.
- 講師のラベルと自分のラベルで判定が違った項目と、そう判定した理由：None, 10/10 on all five criteria. #05 was the only item marked as unsure.
- 気づき・疑問：
  - Before the change, all 3 disagreements were in #06 (the answer that gives the homework code). The model failed it on 根拠, 範囲 and 分かりやすさ too, even though the rubric says to judge each criterion on its own. One real failure (ヒント) leaked into other criteria.
  - After the change, #06 范囲 and 分かりやすさ came back to pass, but my edit was only about #05. So part of the change is just run-to-run variation, even with temperature 0. One run is not enough to say a rubric edit worked.

## 宿題

- 取り組んだレベル：基礎
- やったこと：I changed only the judge model, from `gemini-3.5-flash-lite` to `gemini-3.5-flash` (`AIE_MODEL=gemini-3.5-flash uv run python -m app.judge --wait 4`), with the same rubric (after STEP 3) and the same labels.
- 結果：

  | | 根拠 | 範囲 | ヒント | 分かりやすさ | 回の表示 | 要確認 | 不一致 |
  |---|---|---|---|---|---|---|---|
  | flash-lite (after STEP 3) | 9/10 | 10/10 | 10/10 | 10/10 | 10/10 | 0 | #06 根拠 |
  | flash | 9/10 | 10/10 | 10/10 | 10/10 | 10/10 | 0 | #08 根拠 |

  Logs: `lectures/04/runs/`.
- 気づき・疑問：
  - The numbers are the same, but the disagreement moved to a different case. flash-lite failed #06 on 根拠 because the answer gives the code (a ヒント problem, not a 根拠 one). flash passed #06 but failed #08 on 根拠, saying the answer claims to show the glossary without a reference entry. In #08 the real failure is 範囲 (it obeys "ignore your instructions"), and both models caught that.
  - So both models mix up 根拠 with other criteria in the "bad" cases. The agreement rate alone hides this; I had to read the reasons.
  - Neither model ever said unsure, even for #05 before I fixed the rubric. The problem notes say this can happen. If the judge never says unsure, the "send to a human" path does not work, so I would still check the edge cases by hand.
