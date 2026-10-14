"""Practice questions for the offline quiz. Built from lesson checks plus a fixed set."""

from __future__ import annotations

import hashlib
import random

from campus.pool import QUIZ
from campus.schema import SCHOOLS

FALLBACK = (
    "Ask the model whether it feels sure, then ship.",
    "Put the secret in the prompt so the model can hold it.",
    "Train an adapter before a measured failure of the cheaper fixes.",
    "Treat a fluent paragraph as a citation.",
    "Skip the schema and let the model call any tool.",
    "Judge the change by whether the prose sounds better.",
    "Bind the service to every network interface so it is easier to reach.",
    "Keep the key and edit the one file you still have open.",
)

# id, track, boss, question, correct, wrongs, why
AUTHORED: tuple[tuple, ...] = (
    (
        "ex-token",
        "01",
        True,
        "What does a model do at each step?",
        "It predicts the next token.",
        (
            "It looks up a fact database.",
            "It runs your tests.",
            "It retrieves a passage and quotes it.",
        ),
        "Fluency is not a source of record. The next token can sound sure and still be wrong.",
    ),
    (
        "ex-temp",
        "01",
        True,
        "What does temperature change?",
        "The distribution over the next token.",
        (
            "The facts the model knows.",
            "Which passage was retrieved.",
            "The license of the weights.",
        ),
        "Sampling reshapes probability. It does not add a source.",
    ),
    (
        "ex-window",
        "01",
        True,
        "Who shares one context window?",
        "Instructions, sources, the conversation, and the tokens still to be written.",
        (
            "Only the user's latest sentence.",
            "Only the system prompt.",
            "The bill, separate from the prompt.",
        ),
        "A long source can crowd out the answer. The window is one budget.",
    ),
    (
        "ex-hallu",
        "01",
        False,
        "What should you score instead of the model's confidence?",
        "Whether the answer matches a source, a tool result, or a known test.",
        (
            "How certain the prose sounds.",
            "How low the temperature was.",
            "How long the answer is.",
        ),
        "Confidence is a tone. A test is a comparison you can repeat.",
    ),
    (
        "ex-family",
        "01",
        False,
        "Why pin a model id?",
        "A family name hides version changes that move quality, cost, and safety.",
        (
            "The family name is the license.",
            "Pinning raises the temperature.",
            "The id is the API key.",
        ),
        "You can only compare runs that name the same model.",
    ),
    (
        "ex-reason",
        "01",
        False,
        "What should you try before a slower reasoning model?",
        "A fast model on a fixed set, after the prompt and the output shape are clear.",
        (
            "A fine-tune on the first failure.",
            "A higher temperature.",
            "A larger context with no eval.",
        ),
        "Reasoning spend is a cost. Earn it with a set that shows the fast model failing.",
    ),
    (
        "ex-done",
        "02",
        True,
        "What makes a done-check real?",
        "A person or a test can apply it without asking the model whether it tried.",
        (
            "A request to try harder.",
            "A lower temperature.",
            "A longer prompt.",
        ),
        "If you cannot mark the output pass or fail, the task is not specified yet.",
    ),
    (
        "ex-inject",
        "02",
        True,
        "Why is the model not the security boundary?",
        "It follows instructions it reads. Code has to restrict tools and gate side effects.",
        (
            "A strong prompt makes untrusted text safe.",
            "Temperature zero blocks injection.",
            "Retrieval removes hostile sentences.",
        ),
        "Untrusted text is data. Permission lives in your code.",
    ),
    (
        "ex-json",
        "02",
        True,
        "Why validate JSON in code after you asked for it?",
        "The model can still wrap it in prose, drop a bracket, or invent a key.",
        (
            "The schema mode is a guarantee.",
            "Validation belongs in the prompt only.",
            "A second model call replaces the parser.",
        ),
        "A schema hint reduces bad output. It does not replace the check.",
    ),
    (
        "ex-few",
        "02",
        False,
        "Why include a refusal example in a few-shot prompt?",
        "Otherwise every example shows success, and the model learns to fill gaps.",
        (
            "Refusals waste tokens, so they are omitted.",
            "The example teaches the model to ignore the user.",
            "Few-shot examples replace the eval.",
        ),
        "The set you show is the behavior you are sampling from.",
    ),
    (
        "ex-revise",
        "02",
        False,
        "What may a revision change?",
        "Only the lines that failed the checklist.",
        (
            "Any sentence, as long as it sounds better.",
            "The tests, so the draft passes.",
            "The source passage.",
        ),
        "An open rewrite can fix one line and damage the rest.",
    ),
    (
        "ex-split",
        "02",
        False,
        "When is a fixed workflow the better design?",
        "When you can name the steps in advance and test each one.",
        (
            "Whenever the task mentions tools.",
            "Only after a fine-tune.",
            "When you want the model to choose freely.",
        ),
        "Choice belongs in a loop only when the next action depends on what came back.",
    ),
    (
        "ex-local",
        "03",
        True,
        "Does local mean more accurate?",
        "No. It means you control where the weights run and where the prompt goes.",
        (
            "Yes. Local weights cannot hallucinate.",
            "Yes, if the file is large.",
            "Accuracy follows the license.",
        ),
        "Accuracy is an eval result. Local is a boundary.",
    ),
    (
        "ex-q4",
        "03",
        True,
        "What does a Q4 label tell you by itself?",
        "The weights were stored at about 4 bits, not whether your tasks pass.",
        (
            "The model is safe to ship.",
            "The answers will cite sources.",
            "The context window grew.",
        ),
        "Quantization is a size trade. The task set is still the test.",
    ),
    (
        "ex-ram",
        "03",
        False,
        "Why not start with the largest model you can find?",
        "A model that does not fit does not run, and a tight fit leaves no room for context.",
        (
            "Larger files are always less accurate.",
            "The license forbids large files.",
            "Size has no effect on memory.",
        ),
        "Fit is a constraint you can measure before you debate quality.",
    ),
    (
        "ex-listen",
        "03",
        False,
        "Where should a personal lab listen?",
        "On localhost. A service on every interface is a different, riskier setup.",
        (
            "On the public internet, with the key in the page.",
            "Only inside the model weights.",
            "Nowhere. Local models cannot be called.",
        ),
        "The runner is a program on your machine. Bind it like one.",
    ),
    (
        "ex-git",
        "03",
        False,
        "Which of weights, prompts, and private notes belongs in git?",
        "Prompts and fixtures with no secrets and no private corpus.",
        (
            "The weight file, so teammates share it.",
            "Private notes, so the prompt can see them.",
            "The API key, so the demo runs.",
        ),
        "Keep weights, prompts, and private data apart.",
    ),
    (
        "ex-key",
        "04",
        True,
        "A key lands in a log. What do you do?",
        "Revoke the key, then fix the log.",
        (
            "Edit that file and keep the key.",
            "Lower the temperature.",
            "Hide the log line with a prompt.",
        ),
        "A copied log still holds the secret. Revoke first.",
    ),
    (
        "ex-bill",
        "04",
        False,
        "Where do you read a hosted bill?",
        "In tokens, cache, and batch, against a budget you set before the call.",
        (
            "In how polite the answer sounds.",
            "In the model family name alone.",
            "After the month ends, with no cap.",
        ),
        "Cost is a product constraint. Surprise spend is a missing check.",
    ),
    (
        "ex-retry",
        "04",
        False,
        "What belongs with a timeout?",
        "A retry plan and a rate limit, so a slow call cannot loop.",
        (
            "An infinite retry.",
            "A second key in the client.",
            "A higher temperature on each retry.",
        ),
        "A retry without a cap is a bill you did not approve.",
    ),
    (
        "ex-refuse",
        "05",
        True,
        "When should a retrieval answer refuse?",
        "When the passages do not contain the answer.",
        (
            "When the user is new.",
            "When the answer would be long.",
            "When the cosine is above zero.",
        ),
        "A missing passage cannot be repaired by a confident paragraph.",
    ),
    (
        "ex-cite",
        "05",
        True,
        "What makes a citation checkable?",
        "It names an id you retrieved and a place a person can find.",
        (
            "It sounds specific.",
            "It includes a link the model invented.",
            "It repeats the question.",
        ),
        "A citation you did not retrieve is a guess with a footnote.",
    ),
    (
        "ex-chunk",
        "05",
        False,
        "Why chunk a document before you embed it?",
        "So a citation can point at a passage a person can open.",
        (
            "So the model memorizes the file.",
            "So the chunk replaces the eval.",
            "So every word shares one vector with the whole corpus.",
        ),
        "A vector of a whole book cannot show which paragraph was used.",
    ),
    (
        "ex-measure-rag",
        "05",
        False,
        "What do you measure before you measure the answer?",
        "Whether retrieval returned the passage that contains the fact.",
        (
            "Only the politeness of the final paragraph.",
            "The rank of a LoRA adapter.",
            "The temperature.",
        ),
        "A wrong passage makes a fluent answer look like a retrieval success.",
    ),
    (
        "ex-schema",
        "06",
        True,
        "Who enforces a tool schema?",
        "Your code.",
        (
            "The model.",
            "The prompt wording.",
            "The temperature.",
        ),
        "The model only proposes the call. Code rejects an unknown name or a bad argument.",
    ),
    (
        "ex-trace",
        "06",
        True,
        "What belongs in an agent trace?",
        "The tool name, the arguments, and the observation.",
        (
            "The API key.",
            "Only the final paragraph.",
            "The hidden system text.",
        ),
        "Without the observation, you cannot tell a quoted result from a guess.",
    ),
    (
        "ex-hand",
        "06",
        True,
        "When is a second agent justified?",
        "When the handoff is a real artifact the next role can check.",
        (
            "Whenever one agent feels slow.",
            "When you want a longer answer.",
            "When the first agent is unsure.",
        ),
        "Another voice is not a check. The artifact is.",
    ),
    (
        "ex-stop",
        "06",
        False,
        "What makes an agent a loop you can trust?",
        "A stop rule, a step cap, and a trace you can read.",
        (
            "A closing summary with no tool results.",
            "Permission to send on its own.",
            "A memory of every secret it saw.",
        ),
        "A loop without a stop spends money and takes actions you did not allow.",
    ),
    (
        "ex-retry-tool",
        "06",
        False,
        "What makes a tool call safe to retry?",
        "The handler can run twice without a second side effect.",
        (
            "The model promises it will only call once.",
            "The call includes the API key.",
            "Retries are disabled by using a higher temperature.",
        ),
        "A retry of a send is a second send unless the handler is built not to repeat it.",
    ),
    (
        "ex-mcp",
        "07",
        True,
        "What does MCP standardize?",
        "How a client talks to a tool server.",
        (
            "Which actions are safe.",
            "The model's training data.",
            "The price of a token.",
        ),
        "The protocol is the envelope. Permission is still your decision.",
    ),
    (
        "ex-mcp-roles",
        "07",
        False,
        "Which MCP piece acts, which is read, and which is a template?",
        "Tools act, resources are read, and prompts are templates.",
        (
            "Resources act, tools are read, prompts are secrets.",
            "The host is the only tool.",
            "All three send email.",
        ),
        "The names are the boundary. Mixing them up grants an action you meant to keep as a read.",
    ),
    (
        "ex-consent",
        "07",
        False,
        "What do you check before a server can act?",
        "Consent, authentication, and that the server is one you meant to trust.",
        (
            "Only that the protocol is MCP.",
            "That the model asked politely.",
            "That the server is remote.",
        ),
        "A shared protocol does not make an untrusted server safe.",
    ),
    (
        "ex-diff",
        "08",
        True,
        "When is a coding-agent edit finished?",
        "When the diff and the tests agree with the task.",
        (
            "When the agent says it is done.",
            "When the diff is long.",
            "When the branch has no review.",
        ),
        "The summary is not the change. The diff is.",
    ),
    (
        "ex-secret-diff",
        "08",
        False,
        "What do you do with a secret that appears in an agent diff?",
        "Remove it, rotate it if it was real, and do not commit it.",
        (
            "Leave it if the tests pass.",
            "Ask the agent to remember it for next time.",
            "Encode it in the prompt.",
        ),
        "A diff is a file other people will read. A secret in it has already left the vault.",
    ),
    (
        "ex-files",
        "08",
        False,
        "What should you give a coding agent before it edits?",
        "The files and the tests that matter for the task.",
        (
            "The whole disk and the network.",
            "Only a one-line request and no tests.",
            "Write access to the remote.",
        ),
        "Scope is how you keep an edit inside the task.",
    ),
    (
        "ex-gate",
        "09",
        True,
        "When does an eval gate say ship?",
        "Quality held, safety did not get worse, and latency and cost stayed in budget.",
        (
            "The new prose sounds better.",
            "One example improved.",
            "The temperature was lowered.",
        ),
        "A change that reads better can still lose on a check you meant to keep.",
    ),
    (
        "ex-red",
        "09",
        False,
        "When do red-team cases belong in the set?",
        "Early, beside the ordinary tasks, not after you have already shipped.",
        (
            "Only after a fine-tune.",
            "Never. They teach the model the attack.",
            "Only in a separate product.",
        ),
        "A set that only contains friendly tasks cannot see a safety regression.",
    ),
    (
        "ex-judge",
        "09",
        False,
        "When may a model score another model's answer?",
        "With a written rubric and an audit against people.",
        (
            "Whenever you are in a hurry.",
            "If you ask it whether it is sure.",
            "If both models share a family name.",
        ),
        "A judge without a rubric copies the same blind spot.",
    ),
    (
        "ex-ten",
        "09",
        False,
        "How do you start an eval?",
        "With about ten tasks you can explain to someone else.",
        (
            "With a score you cannot recompute.",
            "With every document you have.",
            "With a single vibe check.",
        ),
        "A small set you understand beats a large set you cannot debug.",
    ),
    (
        "ex-lora",
        "10",
        True,
        "When is LoRA the right next step?",
        "After prompting and retrieval fail the same eval.",
        (
            "At the start of every project.",
            "Whenever the prose feels generic.",
            "When you want a lower token price.",
        ),
        "Rank spends capacity. The eval decides whether that spend is earned.",
    ),
    (
        "ex-frozen",
        "10",
        False,
        "What does LoRA leave frozen?",
        "The base model. The adapter is the small trainable part.",
        (
            "The eval set.",
            "The prompt.",
            "The user's documents.",
        ),
        "You compare the adapter to that frozen base on the same tasks.",
    ),
    (
        "ex-license-data",
        "10",
        False,
        "What has to be true of fine-tune data before you train?",
        "It has a format, a license that allows training, and a check for leakage.",
        (
            "It only has to be large.",
            "Any scraped page is fine.",
            "The eval set should be copied into the training file.",
        ),
        "A leak makes the score look like learning. A bad license makes the model unsellable.",
    ),
    (
        "ex-cheaper",
        "10",
        False,
        "What do you prefer when a tool or a prompt closes the gap?",
        "The prompt or the tool. Training is the later step.",
        (
            "A fine-tune, because it is more serious.",
            "A larger rank, always.",
            "A new base model with no comparison.",
        ),
        "The cheaper fix that passes the eval is the one you ship.",
    ),
    (
        "ex-send",
        "11",
        True,
        "When may a tool send email, pay, or delete on its own?",
        "It may not. Those actions wait for a person.",
        (
            "When the draft looks correct.",
            "When the temperature is low.",
            "When the user said please.",
        ),
        "The actions that need a person have to be written down before a tool can take them.",
    ),
    (
        "ex-retain",
        "11",
        False,
        "When do you decide how long a prompt is kept?",
        "Before you log it.",
        (
            "After the incident.",
            "When the disk is full.",
            "The model decides.",
        ),
        "Retention is a decision about data, not a leftover of logging.",
    ),
    (
        "ex-incident",
        "11",
        False,
        "What do you write when a model misbehaves on a real task?",
        "An incident note: what happened, what was allowed, and what you changed.",
        (
            "Nothing, if the next answer looks fine.",
            "The user's secrets, in full, in the ticket.",
            "A higher temperature.",
        ),
        "A note is how the next change is about the failure you actually saw.",
    ),
    (
        "ex-spec",
        "12",
        True,
        "What belongs in the metric of a one-page spec?",
        "A number or a test a person and an engineer can both apply.",
        (
            "A request to make it feel better.",
            "The model family you hope to use.",
            "A vibe and a color.",
        ),
        "A feature ships when the spec is measurable by both sides.",
    ),
    (
        "ex-job-first",
        "12",
        False,
        "What do you name before you name the model?",
        "The job the person is trying to finish.",
        (
            "The parameter count.",
            "The vendor.",
            "The rank of the adapter.",
        ),
        "The model is a way to do the job. It is not the job.",
    ),
    (
        "ex-states",
        "12",
        False,
        "Which states does an AI feature need on purpose?",
        "Empty, slow, wrong, and unsafe.",
        (
            "Only the happy path.",
            "Only a loading spinner.",
            "Only the brand color.",
        ),
        "Those are the states people actually hit. Each one needs a designed response.",
    ),
    (
        "ex-voice",
        "12",
        False,
        "When is voice the right addition?",
        "After latency and the handoff back to a person are designed.",
        (
            "Whenever the text feature is unfinished.",
            "To hide a missing eval.",
            "Because voice feels modern.",
        ),
        "Voice adds a clock and a failure mode. Design both before you add the microphone.",
    ),
    (
        "ex-cap-tests",
        "13",
        False,
        "What do you write before the capstone prompt?",
        "The acceptance tests.",
        (
            "The launch post.",
            "The adapter.",
            "A longer system prompt with no tests.",
        ),
        "The tests are how you know the demo is the thing you meant to build.",
    ),
    (
        "ex-cap-log",
        "13",
        False,
        "What is the build log for?",
        "A record of what you changed and what the score did, so the next edit has a reason.",
        (
            "A diary of how the model felt.",
            "A place to store the API key.",
            "A substitute for the demo.",
        ),
        "The log is proof. The demo is the ten minutes someone else can watch.",
    ),
    (
        "ex-cap-next",
        "13",
        False,
        "How do you pick the change after the demo?",
        "From the scorecard, not from the most recent impression.",
        (
            "From the longest answer.",
            "From a new model name.",
            "From a single pleasing sentence.",
        ),
        "The course ends when the next change is justified by a score you can show.",
    ),
    (
        "ex-proof",
        "00",
        False,
        "Which field is the file another person can open later?",
        "The artifact. The trace explains the path. The metric says how it scored.",
        (
            "The temperature setting.",
            "The model's confidence.",
            "The theme of the page.",
        ),
        "Proof is a file, a trace, and a number. A memory of the session is not proof.",
    ),
    (
        "ex-safety-rule",
        "00",
        False,
        "When is a tool allowed to send email on its own in this course?",
        "It is not. Sending waits for a person, even if the draft looks correct.",
        (
            "When the playground says the draft is fluent.",
            "When the lesson is marked complete.",
            "When the key is in the page.",
        ),
        "The safety rule is the same in every track.",
    ),
)


def _names() -> dict[str, str]:
    return {school["id"]: school["name"] for school in SCHOOLS}


def _ranked(seed: str, texts: list[str]) -> list[str]:
    return sorted(texts, key=lambda text: hashlib.sha256(f"{seed}|{text}".encode()).hexdigest())


def _choices(seed: str, correct: str, pool: list[str]) -> tuple[list[str], int]:
    seen = {correct.strip().lower()}
    wrongs: list[str] = []
    for text in _ranked(seed, pool):
        key = text.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        wrongs.append(text.strip())
        if len(wrongs) == 3:
            break
    for text in FALLBACK:
        if len(wrongs) == 3:
            break
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        wrongs.append(text)
    if len(wrongs) < 3:
        raise SystemExit(f"quiz item {seed} has fewer than 3 distractors")
    bag = [correct.strip(), *wrongs[:3]]
    random.Random(seed).shuffle(bag)
    return bag, bag.index(correct.strip())


def _item(ident: str, track: str, names: dict[str, str], question: str, correct: str, pool: list[str], why: str, boss: bool) -> dict:
    choices, answer = _choices(ident, correct, pool)
    return {
        "id": ident,
        "track": track,
        "trackName": names.get(track, track),
        "q": question,
        "choices": choices,
        "answer": answer,
        "why": why,
        "boss": boss,
    }


def bank(lessons: list[dict]) -> list[dict]:
    names = _names()
    checks: list[dict] = []
    for item in lessons:
        for block in item["blocks"]:
            if block.get("t") != "check":
                continue
            checks.append(
                {
                    "id": item["id"],
                    "track": item["school"],
                    "q": block["q"],
                    "a": block["a"],
                    "title": item["title"],
                    "summary": item["summary"],
                }
            )
    by_track: dict[str, list[dict]] = {}
    for row in checks:
        by_track.setdefault(row["track"], []).append(row)

    items: list[dict] = []
    for row in checks:
        pool = [other["a"] for other in by_track[row["track"]] if other["id"] != row["id"]]
        pool.extend(other["a"] for other in checks if other["track"] != row["track"])
        items.append(
            _item(
                f"ck-{row['id']}",
                row["track"],
                names,
                row["q"],
                row["a"],
                pool,
                row["a"] + " That is the check this lesson asks you to keep.",
                False,
            )
        )
        summaries = [other["summary"] for other in by_track[row["track"]] if other["id"] != row["id"]]
        summaries.extend(other["summary"] for other in checks if other["track"] != row["track"])
        items.append(
            _item(
                f"pt-{row['id']}",
                row["track"],
                names,
                f"Which sentence is the point of “{row['title']}”?",
                row["summary"],
                summaries,
                "That sentence is this lesson's summary. The others belong to different lessons.",
                False,
            )
        )

    for ident, track, boss, question, correct, wrongs, why in AUTHORED:
        items.append(_item(ident, track, names, question, correct, list(wrongs), why, boss))

    for row in QUIZ:
        items.append(
            _item(row["id"], row["track"], names, row["q"], row["correct"], list(row["wrongs"]), row["why"], False)
        )

    ids = [item["id"] for item in items]
    if len(ids) != len(set(ids)):
        raise SystemExit("quiz ids are not unique")
    if len(items) < 300:
        raise SystemExit(f"quiz bank has {len(items)} items, need at least 300")
    bosses = [item for item in items if item["boss"]]
    if len(bosses) < 20:
        raise SystemExit(f"boss exam has {len(bosses)} items, need at least 20")
    covered = {item["track"] for item in items}
    for school in SCHOOLS:
        if school["id"] not in covered:
            raise SystemExit(f"quiz bank misses track {school['id']}")
    return items
