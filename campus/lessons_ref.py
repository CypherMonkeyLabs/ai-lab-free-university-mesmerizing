"""Glossary, interview practice, and course questions."""

from campus.schema import CK, H, P, TB, UL, lesson

LESSONS = []


def add(item):
    LESSONS.append(item)


def gloss(lid, term, definition, why):
    add(lesson(
        lid, "GL", "core", 4,
        term,
        definition,
        [
            P(definition),
            P(why),
            CK(f"How does this course use “{term}”?", definition),
        ],
    ))


gloss(
    "GL-01", "Token",
    "A chunk of text the model reads or writes. Not always a whole word.",
    "Bills, rate limits, and the context window are counted in tokens. Count them with the tokenizer for the model you call.",
)
gloss(
    "GL-02", "Context window",
    "The token budget for one request, shared by instructions, sources, conversation, and the answer.",
    "If you fill it with pasted files, the standing rules and the answer compete for what remains.",
)
gloss(
    "GL-03", "Temperature",
    "A sampling control. Lower sticks to likely tokens. Higher lets less likely tokens through.",
    "Use low temperature for anything you score. Temperature does not check facts.",
)
gloss(
    "GL-04", "Hallucination",
    "Fluent text that is not grounded in a source, a tool result, or a test you can check.",
    "Ask for evidence. Do not ask the model whether it is confident.",
)
gloss(
    "GL-05", "Structured output",
    "A response constrained to a schema, then validated by your code.",
    "Schema mode reduces broken JSON. It does not make the values true.",
)
gloss(
    "GL-06", "Embedding",
    "A vector for a piece of text, used for similarity search. Produced by an embedding model, not by the chat model.",
    "If you change embedding models, re-embed the corpus. Do not mix vectors from two models in one index.",
)
gloss(
    "GL-07", "Chunk",
    "The piece of a document you index, retrieve, and cite.",
    "Give it a stable id and a span. A chunk that mixes topics makes the citation useless.",
)
gloss(
    "GL-08", "Hybrid search",
    "Keyword search and vector search together, merged into one candidate list.",
    "Keywords catch exact codes and names. Vectors catch paraphrases. In 2026 this is the ordinary default.",
)
gloss(
    "GL-09", "Reranker",
    "A model or rule that reorders a short candidate list for one question.",
    "It cannot recover a passage the first stage never retrieved.",
)
gloss(
    "GL-10", "Citation",
    "An id and a span a person can open, attached to a claim.",
    "A bibliography the model composed is not a citation. Check that the id was in the retrieved set.",
)
gloss(
    "GL-11", "Tool call",
    "A proposed function name and arguments. Your code validates them and runs the handler.",
    "The model does not execute the tool. Your program does, if the allowlist says yes.",
)
gloss(
    "GL-12", "Agent",
    "A loop that lets a model call tools, read observations, and stop on a rule you set.",
    "A long prompt without tools is not an agent. A loop without a step cap is not finished.",
)
gloss(
    "GL-13", "MCP",
    "Model Context Protocol. A standard way for a host's client to talk to a server that offers tools, resources, and prompts.",
    "The server is not the language model. Connecting a server is a permission decision.",
)
gloss(
    "GL-14", "MCP host, client, and server",
    "The host is the app a person uses. The client speaks MCP. The server implements the capabilities.",
    "Secrets for a database belong on the server, not in the prompt.",
)
gloss(
    "GL-15", "Eval",
    "A versioned set of tasks, a scorer, and a record of the model, prompt, and index you ran.",
    "Compare to a baseline. A single impressive answer is not an eval.",
)
gloss(
    "GL-16", "Golden set",
    "The small task set you trust enough to gate a change. This course starts at ten tasks you can explain.",
    "Keep the expected checks human-owned. Do not train on this set.",
)
gloss(
    "GL-17", "Judge model",
    "A model that applies a written rubric to an answer. It is a second system, with its own error rate.",
    "Audit it against scores you made by hand before you let it gate a release.",
)
gloss(
    "GL-18", "LoRA",
    "Low-Rank Adaptation. Trains small matrices while the base model stays frozen.",
    "QLoRA stores that frozen base in quantized form so the job fits on less hardware. Quantization alone is not training.",
)
gloss(
    "GL-19", "Quantization",
    "Storing an existing model's weights in fewer bits so they fit and load faster.",
    "The label, such as Q4, is not a quality score. Compare quantizations on your tasks.",
)
gloss(
    "GL-20", "Prompt injection",
    "Untrusted text — a page, a ticket, a tool description — that tries to instruct the model.",
    "The model is not the boundary. Tool permissions, argument checks, and human approval are.",
)
gloss(
    "GL-21", "Trace",
    "The ordered record of tool calls, arguments, results, approvals, and stops.",
    "When the summary and the trace disagree, believe the trace.",
)
gloss(
    "GL-22", "Human approval",
    "A person confirms the exact arguments of a side effect before the handler runs.",
    "A field inside the model's tool call that says approved is not an approval.",
)
gloss(
    "GL-23", "Coding agent",
    "An agent whose tools read and edit a repository and may run commands you allowed.",
    "The result is the diff and the tests you reran, not the agent's closing summary.",
)
gloss(
    "GL-24", "Allowlist",
    "The tools or commands that may run. Everything else is denied.",
    "A denylist fails when you add a tool and forget to classify it.",
)

add(lesson(
    "IV-01", "IV", "practice", 8,
    "How do you decide to fine-tune?",
    "Exclude the cheaper fixes with an eval, then train only for the gap that remains.",
    [
        H("A short answer"),
        P("I fine-tune only after a fixed task set shows that the schema, the prompt, retrieval, and tools still leave a behavior I can teach with examples. Facts that change stay in retrieval. I keep the adapter only if it beats the base model on that set without new safety failures."),
        H("If they ask you to go further"),
        UL([
            "Show the scorecard: base versus adapter, regressions named.",
            "Say what you refused to train on: secrets, eval rows, data you do not have rights to.",
            "Name LoRA or QLoRA as the usual method, and quantization as a different tool.",
        ]),
        CK("What do you say if you have not trained a model yet?", "Walk the exclusion list on a system you know. 'Not yet, because retrieval was the failure' is a competent answer."),
    ],
))

add(lesson(
    "IV-02", "IV", "practice", 8,
    "How do you evaluate a prompt or model change?",
    "Same tasks, four numbers, a gate you wrote beforehand.",
    [
        H("A short answer"),
        P("I keep a versioned task set and score quality, safety, latency, and cost. I pin the prompt, model id, and index. I compare to the last baseline and block the change if a safety task regresses or the gate I wrote in advance fails."),
        H("If they ask you to go further"),
        UL([
            "Separate retrieval recall from answer quality.",
            "Use exact checks where you can, and a rubric-backed judge only where you must, audited by hand.",
            "Do not hide a regression inside a flat average.",
        ]),
        CK("What is a regression?", "A task that passed on the baseline and fails on the change."),
    ],
))

add(lesson(
    "IV-03", "IV", "practice", 8,
    "How do you stop an agent from doing damage?",
    "An allowlist, a step cap, validated arguments, and a person on side effects.",
    [
        H("A short answer"),
        P("The agent can call only named tools. Arguments have to match the schema before the handler runs. Read-only tools stay inside a step and spend cap. Sending, paying, deleting, and pushing wait for a person who sees the exact arguments. The trace is what I review, not the summary."),
        H("If they ask you to go further"),
        UL([
            "Approval is a record in your program, not a field the model sets.",
            "Retries of side effects need idempotency keys.",
            "Tool descriptions are untrusted text.",
        ]),
        CK("Why not rely on the system prompt?", "Because a document the model reads can contradict it, and a tool that is wired up can still be called."),
    ],
))

add(lesson(
    "IV-04", "IV", "practice", 8,
    "What is MCP, and when would you use it?",
    "A protocol for connecting a host to a tool server, when more than one app should share that server.",
    [
        H("A short answer"),
        P("MCP lets a host's client talk to a server that exposes tools, resources, and prompts over stdio locally or HTTP remotely. I use it when I want a reviewed server — notes, tickets, docs — available to an assistant without inventing a plugin format. I do not enable a server I have not read, and I do not auto-approve write tools."),
        H("If they ask you to go further"),
        UL([
            "Host, client, and server are different roles. The server is not the model.",
            "Resources are still untrusted input.",
            "A remote server needs authentication and least privilege.",
        ]),
        CK("Is installing an MCP server free?", "No. It is a permission change. Treat it like a plugin."),
    ],
))

add(lesson(
    "IV-05", "IV", "practice", 8,
    "How do you review a coding agent's change?",
    "Read the diff, rerun the tests, and reject hunks that do not serve the goal.",
    [
        H("A short answer"),
        P("I look at the diff as a teammate's change: extra files, weakened tests, new dependencies, and anything outside the goal. I run the test command myself and read the output. Secrets, push, and unrestricted shell are denied in the tool layer. The person who merges is responsible."),
        H("If they ask you to go further"),
        UL([
            "A plan before a wide edit is cheaper than unwinding one.",
            "A test the agent rewrote to go green is a failed review.",
            "Lines generated is not the metric. Review time and escaped bugs are.",
        ]),
        CK("The agent says tests passed. What do you need to see?", "The command and the output, rerun by you, plus a test diff that still asserts the behavior you wanted."),
    ],
))

add(lesson(
    "IV-06", "IV", "practice", 7,
    "How do you control cost and latency?",
    "Smaller context, a cheaper model where the eval allows it, caps, and cost per successful task.",
    [
        H("A short answer"),
        P("I retrieve passages instead of pasting the corpus, cap output tokens, and route easy rows to a smaller model only when those rows pass the same checks. I set timeouts and backoff. I report cost per successful task, not per call, and I read the provider's current prices rather than a memorized rate."),
        H("If they ask you to go further"),
        UL([
            "Prompt caching and batch are levers when the workload matches them. Measure the cache hit.",
            "A reasoning model is a latency decision, not a default.",
            "A retry storm is a design bug.",
        ]),
        CK("Why not cost per call?", "Retries, failures, and human cleanup are part of the cost of one success."),
    ],
))

add(lesson(
    "IV-07", "IV", "practice", 7,
    "How do you know a grounded answer is not invented?",
    "The citation has to be an id you retrieved, and some tasks must refuse.",
    [
        H("A short answer"),
        P("I score retrieval separately: did the right chunk id appear. The answer may cite only ids that were retrieved, and the code drops the rest. The task set includes questions the corpus cannot answer, where refusal is the pass. A fluent paragraph with a made-up bibliography fails."),
        H("If they ask you to go further"),
        UL([
            "Hybrid search plus a reranker is the usual pipeline.",
            "If recall is bad, I do not tune the writing prompt first.",
            "I store the index time next to the source time.",
        ]),
        CK("What do you check in code, not by reading tone?", "That every cited id was in the retrieved set, and that a refusal task did not invent one."),
    ],
))

add(lesson(
    "IV-08", "IV", "practice", 8,
    "What goes in an AI product spec?",
    "The job, the non-goals, the four numbers, the failure states, and the kill switch.",
    [
        H("A short answer"),
        P("I write the person's job before the model name, including what this version will not do. Success is quality, safety, latency, and cost per successful task, plus a counter-metric so the team cannot game one number. Empty, slow, wrong, and unsafe states are specified. A limited release has an audience and a way to turn the model path off."),
        H("If they ask you to go further"),
        UL([
            "Buying an agent UI does not replace the eval or the data policy.",
            "Voice adds a latency budget, a transcript, and a human handoff.",
            "Unattended send is a non-goal unless someone has owned that risk in writing.",
        ]),
        CK("Why name non-goals?", "An unnamed non-goal gets built the moment a demo suggests it."),
    ],
))

add(lesson(
    "FQ-01", "FQ", "core", 3,
    "Is this course free?",
    "Yes. You can use it, share it, and remix it under the MIT license.",
    [
        P("The campus file and the text are MIT licensed. You do not need an account or a key to read them. MIT is not a warranty. Third-party model licenses, data, and trademarks stay with their owners."),
        CK("Do you need to pay the author to teach from the file?", "No. Keep the copyright notice if you redistribute it."),
    ],
))

add(lesson(
    "FQ-02", "FQ", "core", 3,
    "Do I need an API key or a GPU?",
    "No, not to study. Add a local model or a hosted key only when you choose to run a live call.",
    [
        P("A current full browser is enough for every lesson. Practices without a model ask for a written artifact. A small quantized model is the first live step, and only if your machine has the memory. Fine-tuning is optional and comes after the eval says you need it."),
        CK("Can you finish the capstone without a hosted key?", "Yes, with a local model, or with synthetic tasks and an explicit 'not run' on live scores if you are honest in the log."),
    ],
))

add(lesson(
    "FQ-03", "FQ", "core", 3,
    "Does the page send my progress anywhere?",
    "No. Progress stays in this browser. The page does not load remote fonts, scripts, or images.",
    [
        P("Marking a lesson complete writes to local storage on your machine. Clearing site data for the file clears the marks. There is no account."),
        CK("Will a classmate see your checkmarks?", "No. They have their own browser storage."),
    ],
))

add(lesson(
    "FQ-04", "FQ", "core", 4,
    "Which model should I install?",
    "A small instruct model whose license you have read, in a size that fits your memory.",
    [
        P("This course does not crown a vendor. School 01 lists the roles — frontier, reasoning, open-weight, small, embedding, coding agent — and School 03 tells you how to pick a size. Pin the id in your notes and score it on your tasks. Re-check names; they move."),
        CK("Why will the course not name a single best model?", "Because the right model depends on the task, the hardware, the license, and the date. The decision procedure is more durable than a shopping pick."),
    ],
))

add(lesson(
    "FQ-05", "FQ", "core", 3,
    "How is this different from a video tutorial?",
    "Each lesson ends in an artifact you can reopen: a schema, a task set, a policy page, or a scorecard.",
    [
        P("Watching is optional. The practices are the course. If you cannot show the artifact, you have not finished the lesson, even if the topic felt familiar."),
        CK("What do you keep from a lesson?", "A file or a note with a run, a trace if something ran, a metric, and the artifact itself."),
    ],
))

add(lesson(
    "FQ-06", "FQ", "core", 3,
    "Can I use the lessons at work?",
    "The text is MIT. Your employer's data, model licenses, and policies still apply.",
    [
        P("You may use and adapt the material. You may not upload private work data because a lesson said to try a model. Fill the safety page with your real constraints. A model license can forbid uses the MIT license on this file does not."),
        CK("Does MIT on this course clear a model weight you downloaded?", "No. The weight has its own license."),
    ],
))

add(lesson(
    "FQ-07", "FQ", "core", 3,
    "How do I report a mistake in a lesson?",
    "Open an issue with the lesson id, the sentence, and the correction.",
    [
        P("Include the lesson id, such as 07-05, and a source a reviewer can check for anything that depends on a spec or a product behavior. Specs move. A dated correction is more useful than a new slogan."),
        CK("What should a correction contain?", "The lesson id, the wrong sentence, and the replacement, with a source when the fact is about a vendor or a spec."),
    ],
))

add(lesson(
    "FQ-08", "FQ", "core", 4,
    "Is there a certificate?",
    "No. The capstone folder is the evidence.",
    [
        P("There is no exam board behind this file. If you want to show the work, share the capstone: tasks, policy page, scorecard, and a trace with secrets removed. A badge would say less."),
        P("Related reading lives in the repository README: how to download the file, how the tracks connect, and how to adapt the course."),
        CK("What can you show a hiring manager instead of a certificate?", "A capstone you can demo: a citation, a refusal, a trace, and a scorecard you can explain."),
    ],
))
