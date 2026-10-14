"""Visual scripts for the glossary, interview practice, and course questions."""

from __future__ import annotations

LESSONS: dict[str, dict] = {}


def L(lid, layout, icon, hero, plate, facts, steps, rows=(), note="", widgets=()):
    LESSONS[lid] = {
        "id": lid,
        "layout": layout,
        "icon": icon,
        "hero": hero,
        "plate": plate,
        "facts": facts,
        "steps": steps,
        "plate_rows": list(rows),
        "plate_note": note,
        "widgets": list(widgets),
    }


def term(lid, icon, hero, plate, word, meaning, steps, rows, note=""):
    L(
        lid, "rail", icon, hero, plate,
        (("Term", word), ("Use it when", "You can point at the mechanism"), ("Practice", "In the numbered track")),
        steps, rows, note or meaning,
    )


term(
    "GL-01", "tiles", "stream", "pipeline", "Token",
    "A chunk of text the model reads or writes. Not always a whole word.",
    (
        ("A chunk", "A token may be a word, part of a word, or punctuation."),
        ("Not a word count", "Billing and the window use tokens from this model's tokenizer."),
        ("Code costs more", "JSON and code often use more tokens than English prose."),
        ("Count it", "Do not budget from an English average."),
    ),
    ("Text", "This model's tokenizer", "Token count", "Price and window"),
)
term(
    "GL-02", "budget", "balance", "bars", "Context window",
    "The token budget for one request, shared by instructions, sources, conversation, and the answer.",
    (
        ("One limit", "Input and output share it."),
        ("Four spenders", "Instructions, retrieved text, conversation, and the answer."),
        ("Overflow", "The call errors, or the provider truncates."),
        ("Size is not attention", "A long window can still miss the middle."),
    ),
    ("Instructions:20", "Sources:40", "Conversation:20", "Answer:20"),
    "An example split, not a rule.",
)
term(
    "GL-03", "thermometer", "stream", "bars", "Temperature",
    "A sampling control. Lower sticks to likely tokens. Higher lets less likely tokens through.",
    (
        ("After the scores", "Temperature reshapes logits. It does not add evidence."),
        ("Low", "The likely tokens stay likely."),
        ("High", "Unlikely tokens get a chance."),
        ("Not a truth knob", "Temperature zero can still repeat a wrong top token."),
    ),
    ("Peak:52", "Next:26", "Tail:22"),
    "Illustrative shape only.",
)
term(
    "GL-04", "unlink", "library", "gates", "Hallucination",
    "Fluent text that is not grounded in a source, a tool result, or a test.",
    (
        ("Fluent", "The sentence can sound finished and still be false."),
        ("Ground it", "A source in context, a tool result, or a test."),
        ("Do not ask", "A claim of certainty is more generated text."),
        ("Score a refusal", "Some items must be unanswerable."),
    ),
    ("No source in reach", "Model still writes", "Check fails", "Correct behavior was to refuse"),
)
term(
    "GL-05", "braces", "desk", "gates", "Structured output",
    "A response constrained to a schema, then validated by your code.",
    (
        ("Name the fields", "Types and allowed values."),
        ("Use the API mode", "When the provider offers schema mode, turn it on."),
        ("Parse anyway", "The model can still wrap or drop a bracket."),
        ("Failure is data", "Retry once with the validator error, then record it."),
    ),
    ("Schema", "Response", "Parser", "Accept or record"),
)
term(
    "GL-06", "hybrid", "search", "scatter", "Embedding",
    "A vector for a piece of text, used for similarity search. A separate model produces it.",
    (
        ("A vector", "Similar meaning lands nearby. That is the hope you then measure."),
        ("Not the chat model", "Pin the embedding model id."),
        ("One index, one model", "Do not mix two embedding models in one space."),
        ("Keywords remain", "Exact names still want keyword search."),
    ),
    ("Refund cluster", "Shipping cluster", "Account cluster", "Ops cluster"),
    "Toy 2D clusters, not a real embedding dump.",
)
term(
    "GL-07", "slices", "library", "stack", "Chunk",
    "The piece of a document you index, retrieve, and cite.",
    (
        ("Split on structure", "Headings and paragraphs, not a magic length."),
        ("Stable id", "The citation has to survive a reindex."),
        ("Keep the heading", "The chunk should still name its subject."),
        ("Store the time", "Freshness belongs on the chunk."),
    ),
    ("Document", "Heading plus body", "Stable id", "Source time"),
)
term(
    "GL-08", "hybrid", "search", "split", "Hybrid search",
    "Keyword search and vector search together, merged into one candidate list.",
    (
        ("Keywords", "Exact codes, names, and quotes."),
        ("Vectors", "Paraphrase and nearby meaning."),
        ("Merge", "One candidate list, not a debate about which camp."),
        ("Then rerank", "The wide list is not the prompt."),
    ),
    ("Keyword hits", "Vector hits", "Merged candidates", "Short list"),
)
term(
    "GL-09", "funnel", "library", "funnel", "Reranker",
    "A model or rule that reorders a short candidate list for one question.",
    (
        ("After retrieval", "You already have candidates."),
        ("Reorder", "For this question, not for the whole corpus."),
        ("Cut", "The prompt sees the few that remain."),
        ("Missing still missing", "A reranker cannot cite a chunk you never retrieved."),
    ),
    ("Wide list", "Reranker", "Short list", "Citation"),
)
term(
    "GL-10", "quote", "library", "stack", "Citation",
    "An id and a span a person can open, attached to a claim.",
    (
        ("Id", "The chunk you retrieved."),
        ("Span", "Enough text to find the sentence."),
        ("Openable", "Another person can look at it."),
        ("On the claim", "Not a confident tone at the end."),
    ),
    ("Claim", "Chunk id", "Span", "Person opens it"),
)
term(
    "GL-11", "schema", "desk", "pipeline", "Tool call",
    "A proposed function name and arguments. Your code validates them and runs the handler.",
    (
        ("Proposal", "The model names a tool and arguments."),
        ("Schema", "Your code rejects arguments that do not match."),
        ("Handler", "You wrote the function. The model does not run it."),
        ("Trace", "Name, arguments, and result are a line in the log."),
    ),
    ("Name", "Arguments", "Validator", "Handler", "Trace"),
)
term(
    "GL-12", "loop", "cycle", "cycle", "Agent",
    "A loop that lets a model call tools, read observations, and stop on a rule you set.",
    (
        ("Not a persona", "The word means the loop, not a character."),
        ("Tools", "Only the list you allowed."),
        ("Observations", "Results and errors come back as data."),
        ("Stop", "Answer, cap, or error. The cap message is yours."),
    ),
    ("Goal", "Model", "Tool", "Observation", "Stop"),
)
term(
    "GL-13", "trio", "columns", "pipeline", "MCP",
    "Model Context Protocol. A host's client talks to a server of tools, resources, and prompts.",
    (
        ("A protocol", "Shared shape, instead of a private plugin format."),
        ("Not the model", "The server is ordinary software."),
        ("Three primitives", "Tools, resources, and prompts."),
        ("Transports", "stdio locally. Streamable HTTP remotely."),
    ),
    ("Host", "Client", "Transport", "Server"),
    "Older remote servers used server-sent events. Check the spec you implement.",
)
term(
    "GL-14", "trio", "columns", "compare", "Host, client, server",
    "The host is the app. The client speaks MCP. The server implements the capabilities.",
    (
        ("Host", "The product a person opens. It owns consent."),
        ("Client", "Initialize, list, and call."),
        ("Server", "Tools, resources, prompts, and the credentials behind them."),
        ("Split the secret", "A password lives on the server, not in the prompt."),
    ),
    ("Host: the product", "Client: the session", "Server: the work"),
)
term(
    "GL-15", "tasks", "meters", "pipeline", "Eval",
    "A versioned set of tasks, a scorer, and a record of the model, prompt, and index.",
    (
        ("Tasks", "The set has an id."),
        ("Scorer", "Quality, safety, latency, and cost."),
        ("Record", "Model id, prompt, and index version."),
        ("Gate", "Ship or fix against a baseline."),
    ),
    ("Tasks", "Pinned run", "Scores", "Gate"),
)
term(
    "GL-16", "ten", "desk", "stack", "Golden set",
    "The small task set you trust enough to gate a change. This course starts at ten.",
    (
        ("Small", "Ten you can explain."),
        ("Includes refusals", "Some items must fail closed."),
        ("Boring cases", "Empty input and exact strings."),
        ("You can audit it", "If you cannot say why an item exists, drop it."),
    ),
    ("Ten tasks", "A reason each", "Refusals included", "Gate uses this set"),
)
term(
    "GL-17", "rubric", "desk", "gates", "Judge model",
    "A model that applies a written rubric. It is a second system with its own error rate.",
    (
        ("Rubric first", "Criteria, not a vibe."),
        ("Audit", "Score a slice yourself."),
        ("Pin it", "The judge has a model id too."),
        ("Person owns the gate", "The judge is evidence, not the release."),
    ),
    ("Rubric", "Judge", "Human audit", "Gate"),
)
term(
    "GL-18", "adapter", "layers", "layers", "LoRA",
    "Low-Rank Adaptation. Small matrices train while the base model stays frozen.",
    (
        ("Freeze", "The base weights do not update."),
        ("Small matrices", "The trainable piece is low rank."),
        ("Save the adapter", "Plus the base model id it attaches to."),
        ("QLoRA", "The frozen base is stored quantized. You are still training the adapter."),
    ),
    ("Frozen base", "Low-rank adapter", "Matching base id", "Eval versus base"),
)
term(
    "GL-19", "bits", "bits", "layers", "Quantization",
    "Storing an existing model's weights in fewer bits so they fit and load faster.",
    (
        ("Storage", "Not a training run."),
        ("The digit", "Q4 is a bit budget, not a quality score."),
        ("Measure", "Same tasks, two quantizations."),
        ("Not LoRA", "Do not mix the words in a review."),
    ),
    ("Wider numbers", "Fewer bits", "Same tasks", "Keep the one that passes"),
)
term(
    "GL-20", "inject", "shield", "gates", "Prompt injection",
    "Untrusted text that tries to instruct the model.",
    (
        ("Where", "A page, a ticket, a tool description, a retrieved chunk."),
        ("What it wants", "To override the job."),
        ("Defense", "Marked channels, least privilege, a person on side effects."),
        ("Fixture", "A document that says to ignore the rules should score as a refusal."),
    ),
    ("Untrusted text", "Job channel", "No extra tools", "Refusal fixture"),
)
term(
    "GL-21", "trace", "desk", "stack", "Trace",
    "The ordered record of tool calls, arguments, results, approvals, and stops.",
    (
        ("Calls", "Name and arguments."),
        ("Results", "Including errors."),
        ("Approvals", "Who saw the exact side effect."),
        ("Stop", "Answer, cap, or error. The summary does not replace the lines."),
    ),
    ("Call", "Arguments", "Result", "Approval", "Stop"),
)
term(
    "GL-22", "person", "shield", "gates", "Human approval",
    "A person confirms the exact arguments of a side effect before the handler runs.",
    (
        ("Which actions", "Send, pay, delete, and anything irreversible."),
        ("Exact arguments", "Not a summary that hides a field."),
        ("Then the handler", "Drafting is not the same as doing."),
        ("Record it", "Person and time, in the trace."),
    ),
    ("Draft", "Show arguments", "Person", "Handler"),
)
term(
    "GL-23", "repo", "machine", "pipeline", "Coding agent",
    "An agent whose tools read and edit a repository and may run commands you allowed.",
    (
        ("Rules first", "Directories, commands, secrets, and network."),
        ("Plan", "A plan you can reject."),
        ("Result", "The diff and the test command."),
        ("Review", "A person reads the hunks and reruns the command."),
    ),
    ("Allowlist", "Plan", "Diff", "Tests", "Person"),
)
term(
    "GL-24", "gates", "shield", "gates", "Allowlist",
    "The tools or commands that may run. Everything else is denied.",
    (
        ("Write it", "If it is not listed, it is not callable."),
        ("Read-only", "May run inside the cap."),
        ("Side effects", "Wait even if listed, unless you have a stronger rule and an eval."),
        ("Default closed", "A new tool starts denied."),
    ),
    ("Listed and read-only", "Listed and needs a person", "Unlisted: denied"),
)

L(
    "IV-01", "rail", "ladder", "route", "pipeline",
    (("Decision", "Train only after cheaper fixes"), ("Method", "LoRA or QLoRA"), ("Evidence", "Same tasks, both models")),
    (
        ("Exclude the cheap fixes", "Prompt, schema, retrieval, and tools, each with a score."),
        ("Name the gap", "The failures those did not close."),
        ("Say the method", "LoRA or QLoRA, and quantization as a different tool."),
        ("Compare", "Adapter versus base, including tasks that used to pass."),
    ),
    ("Prompt and schema", "Retrieval or tool", "Measured gap", "Adapter versus base"),
    "Exclude the cheaper fixes with an eval, then train only for the gap that remains.",
)
L(
    "IV-02", "rail", "tasks", "meters", "pipeline",
    (("Same", "Tasks"), ("Four", "Quality, safety, latency, cost"), ("Written", "Before you look")),
    (
        ("Freeze the set", "The tasks do not change in the same commit as the prompt."),
        ("Four numbers", "Quality, safety, latency, and cost."),
        ("Baseline", "The previous score sits beside the new one."),
        ("Gate first", "You wrote ship-or-fix before you saw the new number."),
    ),
    ("Same tasks", "Pinned ids", "Four numbers", "Gate"),
    "Same tasks, four numbers, a gate you wrote beforehand.",
)
L(
    "IV-03", "gate", "gates", "shield", "gates",
    (("List", "Allowlist"), ("Cap", "Steps and spend"), ("Person", "Side effects")),
    (
        ("Allowlist", "Unlisted tools are denied."),
        ("Schema", "Arguments are validated before the handler."),
        ("Cap", "A step cap and a spend cap are stops you designed."),
        ("Person", "Send, pay, and delete show the exact arguments first."),
    ),
    ("Allowlist", "Validated arguments", "Step cap", "Human gate"),
    "An allowlist, a step cap, validated arguments, and a person on side effects.",
)
L(
    "IV-04", "rail", "trio", "columns", "pipeline",
    (("What", "A protocol, not a model"), ("When", "More than one app shares a server"), ("Unless", "You have not read the server")),
    (
        ("Define it", "A host's client talks to a server of tools, resources, and prompts."),
        ("When", "You want a reviewed server reused by more than one app."),
        ("Transports", "stdio locally, streamable HTTP remotely."),
        ("Consent", "You do not enable an unread server, and you do not auto-approve writes."),
    ),
    ("Host", "Client", "Server", "Consent"),
    "Use it when more than one app should share a reviewed server.",
)
L(
    "IV-05", "split", "diff", "desk", "compare",
    (("Read", "The diff"), ("Rerun", "The tests"), ("Reject", "Hunks that miss the goal")),
    (
        ("Read hunks", "As if a new teammate wrote them."),
        ("Rerun", "The same command the agent ran."),
        ("Reject extras", "Drive-by edits and deleted assertions."),
        ("Ignore the bow", "The summary does not replace the diff."),
    ),
    ("Read the diff", "Rerun the tests", "Reject hunks outside the goal"),
    "Read the diff, rerun the tests, and reject hunks that do not serve the goal.",
)
L(
    "IV-06", "rail", "receipt", "balance", "bars",
    (("Context", "Smaller"), ("Model", "Cheaper where the eval allows"), ("Unit", "Cost per successful task")),
    (
        ("Shrink context", "Send the passages you need, not the whole history."),
        ("Match the model", "A fast model where the ten tasks already pass."),
        ("Cap it", "Steps, tokens, and retries have budgets."),
        ("Per success", "Cost and latency of tasks that passed, not of calls you fired."),
    ),
    ("Input tokens:50", "Output tokens:25", "Retries and tools:25"),
    "Example shares of a bill, not a quote.",
)
L(
    "IV-07", "gate", "quote", "library", "gates",
    (("Cite", "An id you retrieved"), ("Refuse", "When it is absent"), ("Ignore", "A tone of certainty")),
    (
        ("Retrieved id", "The citation has to be a chunk the retriever returned."),
        ("Openable span", "A person can find the sentence."),
        ("Refusal tasks", "Some questions must not be answered from the corpus."),
        ("Separate scores", "Retrieval recall, then the written answer."),
    ),
    ("Retrieved id", "Span", "Refusal case", "Two scores"),
    "The citation has to be an id you retrieved, and some tasks must refuse.",
)
L(
    "IV-08", "stack", "spec", "desk", "stack",
    (("Has", "Job, non-goals, four numbers"), ("Also", "Failure states"), ("And", "A kill switch")),
    (
        ("The job", "Person, job, and constraint."),
        ("Non-goals", "What version one will not do."),
        ("Four numbers", "Quality, safety, latency, and cost."),
        ("States and switch", "Empty, slow, wrong, unsafe, and a way to turn it off."),
    ),
    ("Job", "Non-goals", "Four numbers", "Failure states", "Kill switch"),
    "The job, the non-goals, the four numbers, the failure states, and the kill switch.",
)

L(
    "FQ-01", "rail", "seal", "desk", "stack",
    (("Price", "Free"), ("License", "MIT"), ("Certificate", "None")),
    (
        ("Free to use", "You can read it without an account."),
        ("Free to share", "The MIT license allows reuse."),
        ("Free to change", "Say what you changed if you publish a remix."),
        ("Keep the notice", "The copyright notice stays with the text."),
    ),
    ("Use", "Share", "Remix", "Keep the copyright notice"),
    "There is no account and no certificate.",
)
L(
    "FQ-02", "rail", "laptop", "machine", "layers",
    (("To study", "A browser"), ("Later", "A local model or a key"), ("Only with", "Data you may send")),
    (
        ("No, to study", "The page is the course."),
        ("Optional runner", "Add one when a practice asks for a live local call."),
        ("Optional key", "A hosted call is a choice, not a requirement."),
        ("Write the plan", "Lessons accept a written plan when you have no model."),
    ),
    ("Browser", "Optional local model", "Optional key", "Written plan still counts"),
    "Add a local model or a hosted key only when you choose to run a live call.",
)
L(
    "FQ-03", "gate", "shield", "machine", "gates",
    (("Progress", "This browser"), ("Remote assets", "None"), ("Uploads", "None")),
    (
        ("Local storage", "Mark complete writes lesson ids in this browser."),
        ("No remote assets", "The page does not load remote fonts, scripts, or images."),
        ("No account", "There is nowhere for progress to be sent."),
        ("Clearing the browser", "Clears the progress. That is the tradeoff."),
    ),
    ("Browser storage", "No remote fonts", "No remote scripts", "No account"),
    "Progress stays in this browser.",
)
L(
    "FQ-04", "stack", "gauge", "machine", "bars",
    (("Fit", "Your memory"), ("License", "Read it"), ("Start", "Smaller than your pride")),
    (
        ("A small instruct model", "One whose license you have read."),
        ("Fit the machine", "8 GB starts smaller. 16 GB can try a 7B or 8B class at Q4 or Q5."),
        ("Smoke it", "One prompt before you debate quality."),
        ("Measure", "The runner's memory report beats a slogan."),
    ),
    ("8 GB: smaller model:35", "16 GB: 7B or 8B class:62", "Then one size up:80"),
    "Starting points from the local-model track, not a leaderboard.",
)
L(
    "FQ-05", "split", "proof", "desk", "compare",
    (("Ends in", "An artifact"), ("Not in", "A vibe"), ("Examples", "Schema, tasks, policy, scorecard")),
    (
        ("An artifact", "A schema, a task set, a policy page, or a scorecard."),
        ("Four fields", "Run, trace, metric, and the file."),
        ("Reopen it", "Next month the same file still answers what you did."),
        ("A video cannot", "Watching is not the same as the artifact."),
    ),
    ("Watching a demo", "A file you can reopen"),
    "Each lesson ends in an artifact you can reopen.",
)
L(
    "FQ-06", "gate", "policy", "shield", "gates",
    (("Text", "MIT"), ("Data", "Your employer's rules"), ("Weights", "Their license")),
    (
        ("The text is usable", "MIT covers this course."),
        ("Data rules remain", "Employer policy still decides what you may paste."),
        ("Model licenses remain", "Open weights are not one license."),
        ("No secrets", "A lesson that mentions an API is not permission to paste customer data."),
    ),
    ("Course text", "Employer data rules", "Model license", "No secrets in the prompt"),
    "The text is MIT. Your employer's data, model licenses, and policies still apply.",
)
L(
    "FQ-07", "rail", "incident", "desk", "pipeline",
    (("Include", "The lesson id"), ("Include", "The sentence"), ("Include", "The correction")),
    (
        ("Lesson id", "For example 07-01."),
        ("The sentence", "Quote the line that is wrong."),
        ("The correction", "What it should say."),
        ("A date helps", "Specs and model names move. A dated source helps the reviewer."),
    ),
    ("Lesson id", "The sentence", "The correction", "A dated source"),
    "Open an issue with the lesson id, the sentence, and the correction.",
)
L(
    "FQ-08", "rail", "folder", "folder", "stack",
    (("Certificate", "No"), ("Evidence", "The capstone folder"), ("Gate", "Including not yet")),
    (
        ("No certificate", "The course does not issue one."),
        ("The folder", "Notes, tests, trace, and scorecard."),
        ("The demo", "A pass, a refusal, the trace, and the card."),
        ("A no is finished", "Defending a gate that says not yet still counts."),
    ),
    ("Tests", "Trace", "Scorecard", "The gate sentence"),
    "The capstone folder is the evidence.",
)
