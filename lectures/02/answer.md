# Lecture 02 – Answer

## Assignment

### Level chosen
Implementation

### Data I changed
- **Own topic:** a fictional FAQ for an evacuation drill with 5 entries: date and time, registration, assembly point, report format, and report deadline. Everything is invented: no real dates, URLs or organizations.
- **Kept the same as the original:** the output format `{"answer": <text>, "needs_review": <boolean>}`, the `needs_review` design, the evaluation functions and `CONFIG` (Qwen/Qwen3.5-0.8B at a pinned revision, LoRA r=16 / alpha=32, lr=2e-4, 20 epochs, greedy decoding). No quantization.
- **GROUNDED:** 4 question templates per entry (2 for train, 1 for valid, 1 for test), plus 2 test-only questions per entry. The required keywords are taken verbatim from each FAQ line (e.g. "15 de octubre" and "10:00"; "72 horas" and "certificación").
- **UNGROUNDED:** 8 questions (4 train, 2 valid, 2 test) plus 4 test-only questions. The expected answer is fixed ("Esta información no está en la FAQ. Es necesario confirmar con la organización.") with `needs_review: true`, and the required keyword is "confirmar".
- **Size:** train 14 (10 grounded, 4 ungrounded), valid 7, test 21 (15 grounded, 6 ungrounded).
- **Other changes:** the system prompt and all data are in Spanish. The knowledge questions in section 6 were adapted to the topic: 3 ungrounded questions and 1 control question taken from the test set.

### How I prepared the "ungrounded" questions
1. **Same domain:** they are questions a real drill participant would ask (whether private companies can take part, first-aid kits, rain, size of the brigade, colleagues in a wheelchair, notifying the fire department, etc.). This way the model cannot recognize them just because the topic is different.
2. **No answer in the FAQ:** I checked each question against the 5 FAQ lines and dropped any that could be inferred from one of them. For example, I removed "Can the drill be held on another day?" because the FAQ's fixed date could be read as an answer.
3. **Deliberate hard negatives:** I included questions that share vocabulary with the FAQ but are not answered by it: "Does each employee get a certificate?" (the FAQ only mentions certification for the organization) and "Can I register two branches with a single form?" (the FAQ mentions the form, but not branches). They test whether the model takes a line about a different topic and answers with confidence.
4. **No overlap:** questions are assigned by template to train, valid and test, and an `assert` checks that no question is repeated.

### Results (my own run on Colab, T4)
| | format_rate | content_rate | both_rate | eval seconds |
|---|---|---|---|---|
| Before (base, 32-bit) | 0.952 (20/21) | 0.524 (11/21) | 0.524 | 52.5 |
| After (LoRA) | 1.000 (21/21) | 1.000 (21/21) | 1.000 | 42.7 |

- Training loss: 1.892 (step 10) → 0.092 (step 20) → 0.017 (step 30) → **0.013 (step 40, final)**
- Training time: 216 s · Steps: 40 (20 epochs) · Trainable parameters: 6,389,760 of 758,782,784 (0.84%)
- Regressed questions: none (`regressed = []`).

**Failures before training (10 content failures out of 21), by type:**
| Type | Count | Examples |
|---|---|---|
| Format: missing `needs_review` key | 1 | "¿En qué fecha y a qué hora es la evacuación?" (correct text, key omitted) |
| Grounded question dodged (`needs_review: true`) | 1 | "¿Cómo es el proceso de inscripción?" answered correctly but flagged for review |
| Grounded, partial answer (required keyword missing) | 3 | "NIT_entidad.xlsx" without "Excel" (×2); "72 horas" without "certificación" |
| Ungrounded question answered with confidence (`needs_review: false`) | 3 | Wheelchair → reused the assembly-point line; fire department → "No, it is not required according to the FAQ"; evacuation time → "No" |
| Ungrounded, flagged but inconsistent | 2 | Coordinator: "not specified" but no "confirm"; two branches: `needs_review: true` but the answer asserts "No, it is not allowed" |

The interesting point is that the prompt alone already made the model follow the JSON format 95% of the time. With this topic in Spanish, the main problem before training was **content and grounding judgment**, not format.

After training, all 21 answers are the **verbatim FAQ line** (grounded) or the **fixed ungrounded sentence**. That includes the hard negative in the test set ("Can I register two branches with a single form?"), which before training was flagged but answered "No, it is not allowed". (The "certificate" hard negative is in valid, so it is not scored.) There are no remaining failures in this test set.

**Section 6 (knowledge questions)**
| Question | In FAQ | Before | After |
|---|---|---|---|
| ¿Cuál es el número de emergencias de la ciudad? (city emergency number) | No | needs_review | needs_review |
| ¿Cómo se llama el coordinador del simulacro? (coordinator's name) | No | format_error (missing key) | needs_review |
| ¿Habrá un segundo simulacro este año? (second drill this year) | No | needs_review | needs_review |
| ¿Cuál es la fecha del simulacro? (date of the drill, control) | Yes | asserted (correct) | asserted (correct) |

No ungrounded question ended as "asserted" in my run. Before training the model already recognized 2 of 3 as missing, but in its own wording; after training it uses the fixed sentence for all 3.

**Optional (section 8, 4-bit NF4, no training):** weight memory 3.01 GB → 0.76 GB, but format_rate dropped to 0.714 and content_rate to 0.381. Several ungrounded questions got a bare `false` instead of a JSON object (`not_object`). So quantization alone changed the outputs, and for the worse in this case.

### Reflection: when fine-tuning is and isn't a good fit
- **Good fit:** making the output consistent. With only 14 examples and a few minutes of LoRA training, the model always returned valid JSON, the same wording, and a consistent `needs_review` decision. The prompt alone couldn't guarantee this: the model mixed "flagged but asserting" answers, partial answers and missing keys.
- **Be careful with the 100%:** the result is less impressive than it looks.
  - The FAQ is identical in train and test, so the model may have learned "this kind of question → this line" instead of reading the FAQ. A real test would change the FAQ content (e.g. a new date) and check whether the answer follows it.
  - The model learned to copy the whole FAQ line, which automatically contains the required keywords. This makes the metric easy to pass, and the answers less concise (e.g. "What sign marks the safe zone?" returns the whole sentence).
  - The test set is small (21 questions, only 6 ungrounded), and all ungrounded questions share one fixed answer.
- **Not a good fit:** adding or updating knowledge. If the FAQ changes, the model must be retrained, and nothing guarantees that it judges grounding correctly for new kinds of questions. For a real FAQ assistant I would use retrieval (RAG) for the content plus schema validation or constrained decoding for the format, and use fine-tuning only if the format or style still needs it.

### What I verified myself
- I ran the whole notebook on Colab (T4) from top to bottom with `executed_training_myself: true`.
- I read the before/after output tables question by question and classified the failures above myself.
- I checked that each ungrounded question cannot be answered from any of the 5 FAQ lines.
- AI tools were used to help prepare the dataset and draft this text; all figures come from my own run (`result.json`, `eval_before.json`, `eval_after.json`).
