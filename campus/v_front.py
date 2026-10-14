"""Visual scripts for tracks 00–06."""

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


L(
    "00-01", "rail", "compass", "route", "pipeline",
    (("File", "One HTML page"), ("Account", "None"), ("Progress", "This browser")),
    (
        ("Open the file", "Open the campus in a full browser. Some in-app browsers block a local file."),
        ("Choose a track", "The first time, follow the numbered tracks. Short routes are on the home page."),
        ("Mark complete", "The button stores the lesson id in this browser only."),
        ("Search", "The sidebar filters titles and lesson text. Slash focuses the box."),
        ("Move", "Next, or the bracket keys, moves between lessons."),
    ),
    ("Open the file", "Choose a track", "Study the lesson", "Mark complete", "Search or go next"),
    "Progress is stored in this browser. The page does not load remote fonts, scripts, or images.",
)
L(
    "00-02", "rail", "proof", "desk", "stack",
    (("Skill", "Judgment you can show"), ("Not the goal", "A tour of names"), ("Pin", "The model id")),
    (
        ("Name the job", "Say what you are building and who it is for."),
        ("Write the check", "If you cannot tell a good answer from a bad one, the task is not specified."),
        ("Save the work", "Keep the prompt, the output, the trace, or the score where you can reopen it."),
        ("Skip the tour", "Reciting product names is not the skill this course grades."),
        ("Pin the id", "Record the model id. Names move."),
    ),
    ("Name the job", "Say how you will know", "Save the artifact", "Pin the model id"),
    "A family name hides version changes. The artifact names the id you called and the date.",
)
L(
    "00-03", "rail", "proof", "desk", "stack",
    (("Fields", "Run, trace, metric, artifact"), ("If you cannot measure", "Write that down"), ("Done", "All four present")),
    (
        ("Run", "Do the practice, or write the plan a lesson allows when no model is installed."),
        ("Trace", "Keep the steps, tool calls, or decisions, not only the final sentence."),
        ("Metric", "A number, or an explicit note that you have not measured it yet."),
        ("Artifact", "A file you can open next week: a schema, a scorecard, a policy, or a note."),
        ("Check the four", "A lesson is finished when all four fields exist."),
    ),
    ("Run", "Trace", "Metric", "Artifact"),
    "If you have no model yet, the run may be a written plan. Say so in the metric.",
)
L(
    "00-04", "gate", "shield", "shield", "gates",
    (("Private data", "Stays local"), ("Side effects", "Wait for a person"), ("Untrusted", "Pages, tools, tickets")),
    (
        ("Keep it local", "Private notes stay on the machine until you have permission to move them."),
        ("Ask first", "Sending, paying, and deleting wait for a person who sees the exact action."),
        ("Untrusted text", "A page, a ticket, or a tool description can carry instructions. Data is not an order."),
        ("No secrets", "Keys and passwords do not go in the prompt, the example, or the log."),
        ("Stop", "If you cannot explain the permission, do not take the action."),
    ),
    ("Keep private data local", "Ask before a side effect", "Treat source text as data", "Keep secrets out of the prompt"),
    "These rules apply on every later track. A lesson does not override them.",
)
L(
    "00-05", "stack", "laptop", "machine", "layers",
    (("Required", "A current browser"), ("Model", "Optional"), ("Key", "Not required to study")),
    (
        ("Browser", "A current desktop or phone browser can open the file."),
        ("Optional model", "Install a local runner when you reach that track, not before."),
        ("Optional key", "A hosted call is a choice, and only with data you are allowed to send."),
        ("No GPU required", "Studying does not need one. A slow local model is acceptable later."),
        ("Write the gap", "If you skip a live call, the artifact says what you will run when you can."),
    ),
    ("Browser", "Optional local runner", "Optional hosted key", "The lesson still has an artifact"),
    "Do not create a key only to finish a reading lesson.",
)
L(
    "00-06", "rail", "map", "route", "pipeline",
    (("First", "Models, then prompts"), ("Then", "Ground and act"), ("Last", "Prove, then capstone")),
    (
        ("Models", "Learn what next-token prediction will and will not do."),
        ("Prompts", "Write a job, a shape, and a test for the next edit."),
        ("Access", "Run locally or call an API. Both need a pinned id and a log rule."),
        ("Ground and act", "Retrieve, cite, and call one tool inside a stop rule."),
        ("Prove", "Eval before you trust a change. Safety and the spec come before the capstone."),
    ),
    ("How models work", "Prompting", "Local or API", "Retrieval and agents", "Evals through capstone"),
    "Fine-tuning sits after evals on purpose. Train only when cheaper fixes have failed.",
)
L(
    "01-01", "stack", "spark", "stream", "layers",
    (("Loop", "One token at a time"), ("Evidence", "Only what is in reach"), ("Confidence", "Not a check")),
    (
        ("Read context", "The model sees the tokens so far. It does not look the world up in a side notebook."),
        ("Score tokens", "The last position produces a score for every token in the vocabulary."),
        ("Pick one", "A sampler chooses one token. That choice is not a citation."),
        ("Append", "The chosen token joins the context."),
        ("Repeat", "The loop stops on a stop token or a length limit."),
    ),
    ("Token vectors", "Residual stream", "Causal attention", "Feed-forward", "Next-token scores"),
    "Many 2025 and 2026 decoders use a residual stream, RoPE, and grouped-query attention. Names vary. The behavior you rely on is still next-token prediction.",
    ("attention",),
)
L(
    "01-02", "rail", "tiles", "stream", "pipeline",
    (("Unit", "Token, not word"), ("Count with", "That model's tokenizer"), ("Average", "Not a budget")),
    (
        ("Split", "A token may be a word, part of a word, a space, or punctuation."),
        ("Use that tokenizer", "Billing, rate limits, and the window use the tokenizer of the model you call."),
        ("Expect code to grow", "A short program can cost more tokens than a short paragraph."),
        ("Ignore the proverb", "An English average is not a budget for your prompt."),
        ("Record both", "Save input tokens and output tokens separately when a runner reports them."),
    ),
    ("Text", "Tokenizer for this model", "Token ids", "Price and context use the count"),
    "Code, JSON, and many languages use more tokens than the same idea in English prose.",
    ("tokenizer",),
)
L(
    "01-03", "rail", "budget", "balance", "bars",
    (("Shared by", "Rules, sources, chat, answer"), ("Overflow", "Error or truncation"), ("Long window", "Can miss the middle")),
    (
        ("One budget", "There is no side pocket that protects the system prompt while you paste a book."),
        ("Reserve the answer", "A full window leaves the model no room to write."),
        ("Watch truncation", "When a provider drops text, the early rules are a common casualty."),
        ("Size is not care", "A long window can still miss a fact buried in the middle."),
        ("Retrieve", "Place the passage you need. Pasting the whole corpus is not retrieval."),
    ),
    ("Instructions:18", "Retrieved text:42", "Conversation:22", "Answer room:18"),
    "An example split that sums to 100. Sketch your own. Input and output share one window.",
    ("context",),
)
L(
    "01-04", "rail", "thermometer", "stream", "bars",
    (("Low temperature", "Sticks to likely tokens"), ("High temperature", "Lets the tail through"), ("Neither", "Checks facts")),
    (
        ("Start from scores", "The model produces logits before temperature is applied."),
        ("Reshape", "Lower temperature keeps the peak. Higher temperature flattens the distribution."),
        ("Cut the tail", "Top-p keeps the smallest set of tokens whose mass reaches p, then renormalizes."),
        ("Low is not true", "The top token can be fluent and wrong."),
        ("Match the task", "Use low temperature for anything you will score. Vary a draft only when a person is choosing."),
    ),
    ("Very likely:46", "Likely:28", "Uncommon:14", "Tail:12"),
    "Illustrative masses, not a model dump. Temperature reshapes them. Top-p drops the tail. Truth is not a knob.",
    ("sample",),
)
L(
    "01-05", "gate", "unlink", "library", "gates",
    (("Cause", "Likely text, no evidence"), ("Weak check", "Asking the model"), ("Strong check", "Source, tool, or test")),
    (
        ("Notice fluency", "A confident paragraph can describe something that does not exist."),
        ("See the good case", "A correct summary of a page you pasted worked because the page was in the context."),
        ("Do not ask", "A sentence that claims certainty is more generated text."),
        ("Require an id", "A claim that matters needs a source a person can open."),
        ("Test a refusal", "Some tasks should be unanswerable, so invention fails the score."),
    ),
    ("Put the source in reach", "Call a tool that returns the fact", "Cite an id", "Score a case that must refuse"),
    "Ignore a claim of confidence and check the evidence.",
)
L(
    "01-06", "split", "bubbles", "speech", "compare",
    (("System", "Standing rules"), ("User", "This turn's task"), ("Tool", "Handler results")),
    (
        ("System", "Standing rules live here: refusals, the output shape, and the role."),
        ("User", "The specific task and the input for this turn."),
        ("Tool", "Results your handler returned. Treat them as untrusted data."),
        ("Keep them apart", "A rule buried in a user paragraph is easier for injected text to crowd out."),
        ("Read the trace", "When a call goes wrong, see which role carried the instruction."),
    ),
    ("System: standing rules", "User: the task and the input", "Tool: results from your handler"),
    "Tool results are data. They can contain instructions. The system message does not have to obey them.",
)
L(
    "01-07", "rail", "roles", "columns", "pipeline",
    (("First", "Pick a role"), ("Then", "Pin an id"), ("Search", "A separate model")),
    (
        ("Pick a role", "Frontier chat, reasoning, open weights, a small model, embeddings, a reranker, or a coding agent."),
        ("Pin an id", "A family name hides version changes. Record the id and the date."),
        ("Separate search", "An embedding model and a reranker are not the model that writes the answer."),
        ("Read the license", "Open weights you can download are not automatically cleared for every use."),
        ("Agents are products", "The agent is the loop and the permissions. The model is one part."),
    ),
    ("Frontier chat", "Reasoning", "Open weights", "Small models", "Embeddings and rerankers"),
    "A map of roles as of October 2026, not a shopping list. Model ids move.",
)
L(
    "01-08", "split", "fork", "balance", "compare",
    (("Try first", "A fast model on ten tasks"), ("Reasoning", "When the plan is the risk"), ("Keep", "The cheaper match")),
    (
        ("Price the miss", "A wrong extracted field and a wrong plan are different costs."),
        ("Try fast first", "Low temperature, a clear schema, and ten examples."),
        ("Fix the prompt", "Format failures are often the prompt or the schema."),
        ("Then reason", "Try a reasoning model when the failures are multi-step mistakes."),
        ("Keep the cheaper win", "If the scores match, do not pay for the slower model."),
    ),
    ("Fast model: extraction that already passes", "Reasoning model: a wrong first step is expensive"),
    "Compare them on the same ten tasks. Latency is part of the product.",
)
L(
    "02-01", "rail", "clipboard", "desk", "stack",
    (("Lines", "Job, input, done"), ("Done means", "A check outside the model"), ("Reject", "Make it better")),
    (
        ("Job", "What the model must produce, in one sentence."),
        ("Input", "What this turn will contain."),
        ("Done", "A check a person or a program can apply without asking the model."),
        ("Refusal rule", "If the input does not contain the answer, the output says so."),
        ("No vague goal", "A request to improve the text has no pass mark. Name a change you can score."),
    ),
    ("Job", "Input", "Done-check", "Refusal rule"),
    "Standing rules worth writing once: do not fill gaps, use only the given fields, and keep the user's language unless asked to translate.",
)
L(
    "02-02", "gate", "braces", "desk", "gates",
    (("Contract", "A schema"), ("Mode", "Helps, does not replace"), ("On failure", "Retry once, then stop")),
    (
        ("Name the shape", "Fields, types, and the allowed values."),
        ("Use schema mode", "Turn on structured output when the API offers it."),
        ("Validate in code", "Reject broken JSON, missing fields, and extra fields if your parser is strict."),
        ("Retry once", "Send the validator error back one time. Then stop and record the failure."),
        ("Tables too", "Column names, a row cap, and a rule for empty cells."),
    ),
    ("Schema", "Provider schema mode", "Your parser", "One retry", "Record the failure"),
    "Prose that looks like JSON is not JSON. The parser is the gate.",
)
L(
    "02-03", "stack", "samples", "library", "stack",
    (("Count", "Two or three"), ("Shape", "Same as the real task"), ("Data", "Synthetic or allowed")),
    (
        ("Show the pattern", "Examples teach format better than adjectives."),
        ("Match the shape", "Each example has the input and the output you want."),
        ("Include a refusal", "If refusal is sometimes correct, show one."),
        ("No leaked data", "Examples are data. Do not paste secrets or customer text."),
        ("Test copying", "An example answer can be repeated for the wrong question. Score that case."),
    ),
    ("Input", "Desired output", "A refusal example", "Check it was not copied blindly"),
    "Two or three synthetic examples beat a paragraph of adjectives.",
)
L(
    "02-04", "split", "split", "route", "pipeline",
    (("Hide", "Several jobs in one paragraph"), ("Pass", "An artifact, not a vibe"), ("On failure", "Stop that step")),
    (
        ("Find the jobs", "Planning, searching, calculating, and drafting are different jobs."),
        ("One check each", "Every step has an output you can accept or reject."),
        ("Pass the artifact", "The next step receives the previous output."),
        ("Stop early", "If a step fails its check, do not continue as if it passed."),
        ("Rejoin", "The final answer uses the step outputs you kept."),
    ),
    ("Plan", "Retrieve or calculate", "Check that output", "Draft from it", "Score the draft"),
    "One prompt that does every job hides the step you cannot test.",
)
L(
    "02-05", "loop", "critique", "cycle", "cycle",
    (("Passes", "Draft, then one revision"), ("Critique", "A checklist"), ("Without a checklist", "An unmeasured new prompt")),
    (
        ("Draft", "Produce a first answer against the done-check."),
        ("Checklist", "Critique specific items. A request to make it better is not a list."),
        ("Revise once", "Apply that list. Another open-ended pass is a new prompt."),
        ("Score both", "Keep the draft and the revision. Compare them on the same check."),
        ("Stop", "More passes without a new failing item usually add cost."),
    ),
    ("Draft", "Checklist", "Revise once", "Score both", "Stop"),
    "A second pass helps when the critique is a list of checks.",
)
L(
    "02-06", "gate", "inject", "shield", "gates",
    (("Untrusted", "Documents and tool text"), ("Channel", "Marked as data"), ("Fixture", "Ignore the rules")),
    (
        ("Mark the source", "Pages, tickets, and tool descriptions are data, not orders."),
        ("Keep the job apart", "Put the task in the system or user message, and the source in a marked block."),
        ("Least privilege", "A tool that can send or delete makes injection expensive. Leave it off by default."),
        ("Test the fixture", "A document that says to ignore the rules should score as a refusal."),
        ("Read the trace", "See whether the model followed the document or the job."),
    ),
    ("Untrusted text enters", "Job stays in its channel", "Powerful tools stay off", "Fixture must refuse"),
    "The failure is an instruction hiding in data, plus a powerful tool, plus auto-approval. The defense is review, least privilege, and a person on side effects.",
)
L(
    "02-07", "split", "score", "meters", "compare",
    (("Change", "One thing"), ("Hold still", "The task set"), ("Record", "Both scores")),
    (
        ("One change", "Do not edit the prompt and the model in the same run."),
        ("Same tasks", "The set does not change in that commit."),
        ("Before and after", "Write both scores. A preference is not a comparison."),
        ("Four numbers", "Quality, safety, latency, and cost. The eval track turns this into a gate."),
        ("Keep the loser", "Save the result that lost so you do not repeat it."),
    ),
    ("Change one: prompt, model, index, or tool", "Keep the same tasks", "Record both scores"),
    "A prompt edit without a before-and-after score is a new opinion.",
)
L(
    "03-01", "gate", "house", "machine", "gates",
    (("Local means", "You control the machine"), ("It does not mean", "More accurate"), ("Still", "Pin the id")),
    (
        ("A privacy choice", "The prompt and the weights run on hardware you control."),
        ("Not an accuracy claim", "Local is not automatically better. Accuracy is an eval result."),
        ("A latency choice", "Measure it. Local can be faster or slower."),
        ("Keep the corpus", "Do not send private notes to a host just to compare, unless you are allowed to."),
        ("Pin the file", "Record the model tag or file you ran."),
    ),
    ("Weights stay here", "Prompt stays here", "Accuracy is a separate score", "Record the id"),
    "Local is a privacy and latency choice. It is not a quality award.",
)
L(
    "03-02", "rail", "local", "machine", "pipeline",
    (("Runners", "Ollama or llama.cpp"), ("Listen on", "Localhost"), ("Smoke", "One short prompt")),
    (
        ("Install one", "Ollama or llama.cpp is enough. LM Studio, MLX, and vLLM cover other jobs."),
        ("Pull a small model", "Read the license. Start with a size that can fit."),
        ("Bind localhost", "A lab HTTP service should listen on localhost, not on every interface."),
        ("Smoke prompt", "One short prompt at low temperature. Save the raw response."),
        ("Record the miss", "If nothing is listening, a connection error is the correct observation."),
    ),
    ("Install a runner", "Pull a small model", "Listen on localhost", "One smoke prompt", "Save the id and the reply"),
    "A common local check is the Ollama tag list on port 11434. If nothing answers, record the connection error.",
)
L(
    "03-03", "stack", "gauge", "machine", "bars",
    (("Limit", "Memory, not the slogan"), ("16 GB start", "7B or 8B, Q4 or Q5"), ("Then", "One size up after smoke")),
    (
        ("Fit first", "If the weights do not fit, the runner swaps, crashes, or refuses."),
        ("8 GB", "Start with a small instruct model and a short context."),
        ("16 GB", "A 7B or 8B instruct model at Q4 or Q5 is a common first fit."),
        ("Larger machines", "Try one size up only after the smaller model answers the smoke prompt."),
        ("Know the memory", "Apple silicon is unified. A discrete GPU does not borrow the rest of the machine."),
    ),
    ("8 GB: start smaller:35", "16 GB: 7B or 8B class:62", "32 GB: one size up after smoke:84"),
    "Bar length is only the lesson's starting point, not a quality score. Watch the runner's own memory report.",
)
L(
    "03-04", "stack", "bits", "bits", "layers",
    (("Change", "How weights are stored"), ("Label", "Bit budget, not a grade"), ("Different from", "LoRA")),
    (
        ("Fewer bits", "Quantization stores existing weights with a smaller number budget."),
        ("Read the label", "GGUF names such as Q4_K_M, Q5_K_M, and Q8_0. The digit is the bit budget."),
        ("Not a grade", "Q4 does not mean the model passes your tasks."),
        ("Measure two", "Run the same fixture on two quantizations of the same model."),
        ("Not training", "Quantizing is storage. An adapter is a later, different tool."),
    ),
    ("FP16 weights", "Q8 storage", "Q5 storage", "Q4 storage", "Same tasks, new score"),
    "A more aggressive quantization is smaller and more likely to damage names, reasoning, and tight formats. The fixture decides.",
)
L(
    "03-05", "gate", "seal", "desk", "gates",
    (("Read", "The license on the weights"), ("If unsure", "Do not ship"), ("Still separate", "Rights in your data")),
    (
        ("Find the terms", "Read the license that shipped with the weights, not a summary of the family."),
        ("They differ", "Some allow commercial use. Some restrict it. Some restrict training on the outputs."),
        ("Record it", "Write the model name, revision, and license name in the artifact."),
        ("Ask or switch", "If you cannot explain the use, do not ship. Pick terms you can explain."),
        ("Data rights remain", "A model license does not clear the documents you put in the prompt."),
    ),
    ("Find the license", "Name one limit", "Record name and revision", "Do not ship on a guess"),
    "A file you can download is not automatically a file you can hide inside a product.",
)
L(
    "03-06", "loop", "check", "cycle", "cycle",
    (("Same check", "Every time"), ("When", "After a reboot, before the prompt"), ("Artifact", "Reply or the error")),
    (
        ("One command", "Tag list, model list, or one short completion."),
        ("After a reboot", "Prove the runner is up before you debug the prompt."),
        ("Save the output", "The artifact is the response or the connection error."),
        ("Then change one thing", "A new prompt on a dead runner wastes the session."),
        ("Keep it short", "The smoke test is not the eval set."),
    ),
    ("Runner up?", "Same command", "Save the output", "Only then change the prompt"),
    "The smoke check is a local HTTP call or a CLI completion.",
)
L(
    "03-07", "split", "folders", "machine", "compare",
    (("Piles", "Weights, prompts, data"), ("Logs", "Are a database"), ("Permissions", "Not your whole home")),
    (
        ("Three folders", "Weights, prompts, and private notes do not share a directory."),
        ("Backups differ", "A weight file can be fetched again. A private note may not."),
        ("Permissions differ", "The runner can read the weights. It should not inherit every file you can read."),
        ("Prompts are data", "A saved prompt can contain personal text."),
        ("Name the paths", "Write the three locations in the artifact."),
    ),
    ("Weights: model files", "Prompts: the jobs you send", "Private data: notes you would not publish"),
    "Different files, different backups, different permissions.",
)
L(
    "04-01", "gate", "key", "machine", "gates",
    (("Lives in", "Environment or secret store"), ("Loaded", "At runtime"), ("Logs", "Must not print it")),
    (
        ("Keep it out", "The key is not in the repository and not in client source."),
        ("Read at runtime", "The process loads it when it starts."),
        ("Clean logs", "A stack trace must not print the key."),
        ("Least privilege", "A key that can call the model, not an admin key for the whole account."),
        ("Rotate on leak", "If it landed in a commit or a screenshot, revoke it."),
    ),
    ("Secret store", "Process environment", "Client reads it", "Logs omit it"),
    "The client reads the key at runtime. The repository never contains it.",
)
L(
    "04-02", "gate", "parser", "desk", "gates",
    (("Ask", "For a schema"), ("Gate", "Your parser"), ("Failure", "A recorded result")),
    (
        ("Ask for the schema", "Use the provider's structured output when it exists."),
        ("Parser decides", "Schema mode reduces broken JSON. It does not replace validation."),
        ("Closed values", "Name the allowed strings. Reject anything else."),
        ("Do not guess", "A parse failure is a result. Do not silently coerce a value."),
        ("One retry", "Return the validator message once, then stop."),
    ),
    ("Schema", "Model response", "Parser", "Accept or record"),
    "Structured output is a feature of the API. Your parser is still the gate.",
)
L(
    "04-03", "rail", "clock", "machine", "pipeline",
    (("Timeout", "A product limit"), ("Retries", "A small budget"), ("Storm", "A bill")),
    (
        ("Set a timeout", "A hung call is a product bug. Pick a limit a person can feel."),
        ("Budget retries", "Retry transient failures a small, fixed number of times."),
        ("Back off", "Respect a rate-limit signal. Do not hammer it."),
        ("No storm", "A loop that retries immediately can dominate the bill."),
        ("Log the attempt", "Status, latency, and attempt count. Not the key."),
    ),
    ("Call", "Timeout", "Backoff", "Stop", "Log the attempt count"),
    "A hung call is a product bug. A retry storm is a bill.",
)
L(
    "04-04", "rail", "receipt", "balance", "bars",
    (("Levers", "Input, output, cache, tools"), ("Unit", "Per successful task"), ("Prices", "Read the card")),
    (
        ("Input tokens", "You pay to send the prompt, including history you resend."),
        ("Output tokens", "The answer is often priced apart from the input."),
        ("Cache", "Some APIs discount a repeated prefix. Keep that prefix stable if you rely on it."),
        ("Tools and retries", "Each extra call belongs to the cost of one user task."),
        ("Per success", "Divide spend by tasks that passed, not by calls you fired."),
    ),
    ("Input tokens:55", "Output tokens:25", "Cached prefix:12", "Tool calls:8"),
    "An example of where a bill can go, not your invoice. Read the provider's price card and your own logs.",
    ("context",),
)
L(
    "04-05", "split", "columns", "meters", "compare",
    (("Fixture", "The same ten tasks"), ("Swap", "The client only"), ("Record", "Id, date, and price")),
    (
        ("Ten tasks", "The same fixture for every provider."),
        ("Same schema", "The parser does not change when the client changes."),
        ("Same scorecard", "Quality, safety, latency, and cost."),
        ("Swap the client", "Keep the prompt and the rubric."),
        ("Write the id", "Record the model id, the date, and the price you used."),
    ),
    ("Provider A on ten tasks", "Provider B on the same ten", "One scorecard"),
    "Swap the client. Keep the fixture, the schema, and the scorecard.",
)
L(
    "04-06", "stack", "redact", "desk", "stack",
    (("Keep", "Id, latency, token counts"), ("Drop", "The key"), ("Also drop", "Raw private text")),
    (
        ("Keep the id", "Model id, latency, token counts, and a hash or id of the prompt."),
        ("Drop the key", "The secret never enters the log line."),
        ("Drop private text", "Unless a written rule allows that field and sets a retention date."),
        ("Hash to join", "A hash lets you find the run without storing the prompt."),
        ("Decide retention", "The safety track asks you to choose it before you log."),
    ),
    ("Model id", "Latency and tokens", "Prompt hash", "Key removed", "Raw text removed"),
    "Keep the model id, the latency, the token counts, and a hash of the prompt.",
)
L(
    "05-01", "split", "shelf", "library", "split",
    (("Index clock", "When documents change"), ("Question clock", "Every ask"), ("Answer", "Only from the short list")),
    (
        ("Index", "Chunk, embed, and store when the sources change."),
        ("Ask", "Search the question as written."),
        ("Retrieve", "Keywords catch exact names. Vectors catch paraphrase. Use both."),
        ("Rerank", "Keep the short list that actually answers."),
        ("Cite", "The draft may use those passages, and it names the chunk id."),
    ),
    ("Documents", "Chunk", "Embed", "Question", "Retrieve", "Rerank", "Cite"),
    "Two clocks. If the right chunk is not in the short list, a better prompt will not invent it.",
    ("rag",),
)
L(
    "05-02", "stack", "slices", "library", "stack",
    (("Split on", "Structure"), ("Id", "Stable"), ("Keep", "The heading")),
    (
        ("Follow structure", "Headings, paragraphs, and list items. Do not hunt for a magic token count."),
        ("Stable ids", "A citation has to point at the same span after you reindex."),
        ("Keep the heading", "A chunk without its heading often loses the noun in the question."),
        ("Overlap on purpose", "A small overlap can hold a sentence that crossed a cut. Record the size."),
        ("Store the time", "The source's updated time belongs on the chunk."),
    ),
    ("Heading stays with the chunk", "Stable id", "Optional overlap", "Source time"),
    "The piece you index is the piece you can cite.",
)
L(
    "05-03", "rail", "hybrid", "search", "scatter",
    (("Keywords", "Exact strings"), ("Vectors", "Paraphrase"), ("Do not mix", "Two embedding models")),
    (
        ("Keywords", "Error codes, names, SKUs, and quoted phrases."),
        ("Vectors", "An embedding model places similar meaning nearby."),
        ("Not the chat model", "Pin the embedding model id. It is a different model."),
        ("Merge", "Hybrid search uses both candidate lists."),
        ("One space", "Do not store vectors from two embedding models in one index."),
    ),
    ("Refund cluster", "Shipping cluster", "Account cluster", "Model-ops cluster"),
    "A 2D picture of a toy space. Real embedding vectors are much wider. Nearest neighbors are the idea.",
    ("cosine", "embed"),
)
L(
    "05-04", "funnel", "funnel", "library", "funnel",
    (("Wide", "The first retrieval"), ("Narrow", "The reranker"), ("Prompt", "Only the survivors")),
    (
        ("Retrieve wide", "Ask the index for more candidates than you will show the model."),
        ("Rerank", "A reranker or a strict rule reorders them for this question."),
        ("Cut", "The prompt receives a few passages, not the wide net."),
        ("Cite survivors", "The answer can cite only what made the cut."),
        ("Fix recall here", "If the right passage is missing, do not tune the final adjectives."),
    ),
    ("Wide candidate list", "Reranker", "Short list", "Prompt and citation"),
    "Retrieve widely, then keep the few passages that actually answer.",
)
L(
    "05-05", "rail", "quote", "library", "stack",
    (("Citation", "Id plus span"), ("Must be", "Openable"), ("Not a citation", "A confident tone")),
    (
        ("Use the id", "The chunk id you actually retrieved."),
        ("Show a span", "Enough text for a person to find the sentence."),
        ("Make it openable", "Someone else can open the source and see that span."),
        ("Attach it", "The citation sits on the claim, not in a confident footer."),
        ("No retrieved id", "Then the model does not get to cite one."),
    ),
    ("Claim", "Chunk id", "Span", "A person opens it"),
    "A citation is an id and a span, not a tone of voice.",
)
L(
    "05-06", "gate", "warn", "library", "gates",
    (("Four failures", "Wrong, stale, middle, missing"), ("Before", "Prompt adjectives"), ("Missing fact", "Say so")),
    (
        ("Wrong chunk", "The index returned a neighbor, not the passage that answers."),
        ("Stale chunk", "The text was true when you indexed it."),
        ("Lost middle", "The right passage was in a long prompt and was not used."),
        ("Missing fact", "The corpus never contained the answer. The correct output says so."),
        ("Test them first", "These four belong in the set before you tune the prompt."),
    ),
    ("Wrong chunk", "Stale chunk", "Lost in the middle", "Never in the corpus"),
    "Each failure has a different fix. None of them is a request to sound more sure.",
)
L(
    "05-07", "split", "recall", "meters", "compare",
    (("First score", "Retrieval recall"), ("Then", "The written answer"), ("Label", "must_include ids")),
    (
        ("Label questions", "Each item names the chunk ids that must appear."),
        ("Run retrieval alone", "Do not involve the writer yet."),
        ("Top 5 and pasted", "Was the right id retrieved, and was it one you would paste?"),
        ("Then score the answer", "Only after recall is visible."),
        ("Fix the index first", "A bad passage and an ignored passage have different repairs."),
    ),
    ("Retrieval: right id in the top 5?", "Answer: used that chunk, or refused?"),
    "An answer score on a bad index mostly measures invention.",
)
L(
    "06-01", "loop", "loop", "cycle", "cycle",
    (("Shape", "Goal, tool, observation, stop"), ("Cap", "A stop you designed"), ("Error", "Not a guess")),
    (
        ("Goal", "One sentence that says what done means."),
        ("Choose", "The model calls a tool or returns a final answer."),
        ("Run the handler", "Your code checks the arguments. The model does not run the tool."),
        ("Observe", "Append the result or the error. Do not invent a result the tool did not return."),
        ("Stop", "An answer, a step cap, a spend cap, or a failed check. The cap sentence is yours."),
    ),
    ("Goal", "Model", "Tool", "Observation", "Stop"),
    "Worked shape: a calc tool for a percentage. If calc errors, the agent says it could not compute.",
)
L(
    "06-02", "rail", "schema", "desk", "pipeline",
    (("Model does", "Propose a call"), ("Code does", "Validate and run"), ("Bad args", "A failed step")),
    (
        ("Name", "A short name the model can choose."),
        ("Describe", "When to use it. The model reads this text."),
        ("Schema", "JSON schema for the arguments. Your code enforces it."),
        ("Handler", "The function you wrote."),
        ("Reject", "Bad arguments are a failed step, not a hint to try a neighboring action."),
    ),
    ("Name", "Description", "JSON schema", "Handler", "Trace line"),
    "The description is for the model. The schema is for your validator.",
)
L(
    "06-03", "gate", "gates", "shield", "gates",
    (("Read-only", "May run inside the cap"), ("Side effect", "Waits"), ("Unlisted", "Denied")),
    (
        ("Allow", "Read-only tools may run inside the step cap."),
        ("Ask", "Anything that sends, pays, deletes, or leaves the machine waits for a person."),
        ("Deny", "A tool or path that is not on the list is not callable."),
        ("Show the arguments", "The person approves the exact call, not a vague summary."),
        ("Default closed", "A new tool is denied until you add it."),
    ),
    ("Allow read-only", "Ask on side effects", "Deny the rest", "Record the decision"),
    "Auto-approving every tool is how data leaves the machine.",
)
L(
    "06-04", "split", "memory", "desk", "compare",
    (("Lifetimes", "Thread, file, store"), ("Hidden memory", "A second database"), ("Secrets", "Are not memories")),
    (
        ("Thread", "Dies with the run unless you save it."),
        ("File", "A deliberate artifact. You know the path."),
        ("Store", "Needs a schema, an owner, and a retention rule."),
        ("No secrets", "Keys and raw private text are not something to remember."),
        ("Say what it forgot", "Do not pretend to recall a fact you did not store."),
    ),
    ("Thread: this run", "File: a path you chose", "Store: a database with retention"),
    "Pick one lifetime on purpose.",
)
L(
    "06-05", "split", "handoff", "route", "compare",
    (("Add a second agent", "Only with an artifact"), ("Weak pattern", "A shared vague chat"), ("Cost", "Two bills")),
    (
        ("One loop first", "Most jobs are a single loop with a stop rule."),
        ("Name the artifact", "A plan, a diff, a retrieved set, or a scorecard."),
        ("Start there", "The next agent reads that artifact. It does not guess from the whole chat."),
        ("Separate allowlists", "Each agent has its own tools."),
        ("Justify the cost", "Two models are two bills. The eval has to say why."),
    ),
    ("Useful: a file, schema, or score", "Weak: two agents in one vague chat"),
    "Two agents that share a vague chat are one confused loop with extra cost.",
)
L(
    "06-06", "stack", "trace", "desk", "stack",
    (("Read", "The trace"), ("Not enough", "The closing summary"), ("Replay", "From the lines alone")),
    (
        ("Every call", "Tool name, arguments, and the step number."),
        ("Every result", "What came back, including errors."),
        ("Every approval", "Who confirmed a side effect, and the arguments they saw."),
        ("The stop", "Answer, cap, or error."),
        ("Reconstruct", "Another person can replay the decisions from the trace alone."),
    ),
    ("Call", "Arguments", "Result or error", "Approval", "Stop reason"),
    "The summary is a claim about the trace. Keep the trace.",
)
L(
    "06-07", "loop", "retry", "cycle", "gates",
    (("Twice", "One effect"), ("Key", "Recognizes the retry"), ("Place", "A sandbox")),
    (
        ("Same effect", "A second run must not double-send, double-charge, or double-append."),
        ("Idempotency key", "The handler recognizes a retry of the same call."),
        ("Sandbox", "Writes stay in a folder or a project you named."),
        ("Safe error", "A failed call leaves a state you can retry or abandon."),
        ("Test the double", "Run the same call twice and show a single effect."),
    ),
    ("First call", "Same key again", "Handler recognizes it", "One side effect"),
    "A second run of the same call should not escape the folder either.",
)
