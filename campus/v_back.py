"""Visual scripts for tracks 07–13."""

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
    "07-01", "rail", "trio", "columns", "pipeline",
    (("Protocol", "Host talks to a server"), ("Server is", "Not the model"), ("Remote transport", "Streamable HTTP")),
    (
        ("A shared shape", "MCP lets a host talk to a tool server without a private plugin format."),
        ("Not the model", "The server lists capabilities and runs tools. The model runs in the host."),
        ("Host decides", "The app a person uses chooses what the model may see."),
        ("Client speaks", "Initialize, list, and call. The client lives in the host."),
        ("Transports", "Local servers usually use stdio. Remote servers use streamable HTTP."),
    ),
    ("Host", "MCP client", "Transport", "Server", "Tools, resources, prompts"),
    "Older remote servers used server-sent events. Read the spec version you implement.",
)
L(
    "07-02", "split", "trio", "columns", "compare",
    (("Host", "The product"), ("Client", "The session"), ("Server", "The work")),
    (
        ("Host", "Editor, desktop app, or a UI you are building. It owns consent."),
        ("Client", "Opens the session and asks before tools run."),
        ("Server", "Implements tools, resources, and prompts, and holds the credentials."),
        ("Transport", "stdio on one machine, or streamable HTTP when the server is remote."),
        ("Password", "A database password lives in the server environment, not in the prompt."),
    ),
    ("Host: the product a person opens", "Client: the MCP session", "Server: the capabilities"),
    "Do not put a database password in the prompt or in a tool description.",
)
L(
    "07-03", "gate", "primitives", "shield", "gates",
    (("Tool", "May change something"), ("Resource", "Read, still untrusted"), ("Prompt", "A template to review")),
    (
        ("Tool", "A function with arguments. Treat writes as side effects."),
        ("Resource", "Data the model may read. The body can still carry instructions."),
        ("Prompt template", "Review it the way you review any prompt change."),
        ("Match the job", "Showing a note is a resource. Appending a line is a tool that waits."),
        ("Read-only is not trusted", "Injection does not need a write tool to enter the context."),
    ),
    ("Tool: an action", "Resource: readable data", "Prompt: a template"),
    "Use the primitive that matches the risk.",
)
L(
    "07-04", "rail", "pipes", "machine", "pipeline",
    (("Where", "A child process"), ("Streams", "Standard input and output"), ("Power", "The environment you passed")),
    (
        ("Name the command", "Pin the path. Do not trust a mystery binary earlier on the path."),
        ("stdio", "The host speaks MCP on the process streams."),
        ("Narrow the environment", "Pass only the variables the server needs."),
        ("Root folder", "The server rejects paths outside the folder you set."),
        ("Read first", "Start with resources. Add a write tool only with an approval."),
    ),
    ("Host starts a process", "stdio session", "NOTES_ROOT only", "Reject paths outside it"),
    "The process is the trust boundary. It can see whatever environment you gave it.",
)
L(
    "07-05", "gate", "consent", "shield", "gates",
    (("Closer to", "Installing a plugin"), ("Remote", "Authenticate"), ("Tool text", "Untrusted")),
    (
        ("Read the list", "See what the server declares before you enable it."),
        ("Approve side effects", "A host that auto-approves has no consent left."),
        ("Authenticate", "A remote server receives what the client sends. Use the account the task needs."),
        ("No pasted strangers", "Do not enable a server because a page told you to paste the config."),
        ("Treat descriptions as data", "A hostile tool description is an instruction the model may follow."),
    ),
    ("Who published it", "Which tools write or send", "Will the host ask first", "What data can it read"),
    "Untrusted instructions in tool metadata, plus a powerful tool, plus auto-approval, is the failure mode.",
)
L(
    "07-06", "rail", "plug", "columns", "pipeline",
    (("Adds", "Context, not a free pass"), ("Docs server", "No write tools"), ("Still required", "Review the diff")),
    (
        ("Add one", "Each server widens what the model can read. Keep the trace."),
        ("Turn writes off", "A documentation server does not need them."),
        ("Same auth", "An internal API behind MCP needs the credential boundary you would demand of a script."),
        ("A logged-in browser", "Assume it can see what you can see. That is not a default-on tool."),
        ("Review remains", "MCP does not replace tests or a person on the diff."),
    ),
    ("Editor", "One reviewed server", "Trace", "Diff a person reads"),
    "Connecting an issue tracker adds context. It does not remove review.",
)
L(
    "08-01", "gate", "repo", "machine", "gates",
    (("Result", "A diff plus a test"), ("Not the result", "The summary"), ("Deny", "Secret files")),
    (
        ("Name directories", "What it may read, and what it may write."),
        ("Name the command", "Whether it may run tests, and which command."),
        ("Separate the risky verbs", "Installs, git config, and the network are their own decisions."),
        ("Deny secrets", "Include env files, key stores, and credential files."),
        ("Show a diff", "Applying the result is a reviewable change, not a silent commit to the main branch."),
    ),
    ("Read scope", "Write scope", "Test command", "Secret deny list", "Person reviews the diff"),
    "If you cannot answer those, you have a product default, and defaults drift.",
)
L(
    "08-02", "stack", "files", "desk", "stack",
    (("Point at", "Module and test"), ("If the command is unknown", "Stop before editing"), ("Search", "Inside a step cap")),
    (
        ("Point at the module", "The failing test and the interface it must not break."),
        ("Name the command", "That command is the done-check."),
        ("Write the deny list", "Say which directories stay untouched."),
        ("Cap the search", "Let it look when the file is unknown. Do not fund a tour."),
        ("Redirect at the list", "When it names the files it will change, correct it there."),
    ),
    ("Goal", "Read these files", "Do not edit", "Done when this command passes"),
    "A whole repository in the prompt is noise, not context.",
)
L(
    "08-03", "rail", "plan", "route", "pipeline",
    (("Cheap to reject", "A plan"), ("Then", "Edit inside the allowlist"), ("Always", "Stop and show the diff")),
    (
        ("Plan", "It states the files and what it thinks is wrong."),
        ("Accept or reject", "You correct the plan before the edits."),
        ("Edit", "Only inside the allowlist."),
        ("Run", "The test command you named."),
        ("Stop", "Pass or fail, it stops and shows the diff."),
    ),
    ("Plan", "Person accepts", "Edit", "Run the test", "Stop with the diff"),
    "A plan you can reject is cheaper than a pile of edits you have to unwind.",
)
L(
    "08-04", "split", "diff", "desk", "compare",
    (("Read", "Every hunk"), ("Rerun", "The same command"), ("Red flag", "A deleted assertion")),
    (
        ("Open the diff", "Read it as if a new teammate wrote it."),
        ("Check the goal", "Each hunk should serve the sentence you wrote."),
        ("Rerun", "Do not trust a reported green test you did not run."),
        ("Watch the tests", "A deleted assertion is not a cleanup."),
        ("Reject with a reason", "The next run should start from your note."),
    ),
    ("Read the diff like a teammate's", "Rerun the command they ran"),
    "The summary is a claim about the diff. The diff and the command are the evidence.",
)
L(
    "08-05", "gate", "secret", "shield", "gates",
    (("Expensive mistakes", "Secrets, git, network"), ("Not the focus", "Indentation"), ("Write", "The deny list")),
    (
        ("Secrets", "The agent does not read, print, or commit them."),
        ("Destructive git", "No force-push, no hard reset of shared history, no quiet config edits."),
        ("Network", "Installing and uploading are not part of running tests unless you said so."),
        ("Exfiltration", "A command that posts the repo somewhere is not a test."),
        ("Write it down", "If the deny list is blank, the product default decides."),
    ),
    ("Block secret files", "Block destructive git", "Block surprise network", "Person does those jobs"),
    "The expensive mistakes are not bad indentation.",
)
L(
    "08-06", "rail", "team", "desk", "pipeline",
    (("Agree", "Permissions and review"), ("Not an excuse", "The agent did it"), ("Keep", "Plan and test output")),
    (
        ("Agree permissions", "The team knows what the agent may do alone."),
        ("Agree review", "Who reads the diff, and which commands must be rerun."),
        ("Own the change", "A tool is not an author who skips responsibility."),
        ("Keep diffs small", "A reviewable change beats a branch nobody can read."),
        ("Attach the trace", "The plan, the commands, and the test output stay with the review."),
    ),
    ("Permissions", "Reviewer", "Rerun command", "Trace attached"),
    "Agree the permissions, the review, and what a tool does not excuse.",
)
L(
    "09-01", "rail", "tasks", "meters", "pipeline",
    (("Set", "Versioned"), ("Beside the score", "Prompt, model, index"), ("Not an eval", "One good screenshot")),
    (
        ("Version the tasks", "The set has an id. Changing it is its own release."),
        ("Pin the run", "Model id, prompt, and index version sit next to the score."),
        ("Score", "Quality, safety, latency, and cost."),
        ("Compare", "Against the baseline you named beforehand."),
        ("Gate", "Ship or fix. One impressive answer is not the gate."),
    ),
    ("Versioned tasks", "Pinned run", "Four scores", "Baseline", "Ship or fix"),
    "You cannot prefer a new prompt unless the same tasks were scored both times.",
)
L(
    "09-02", "stack", "ten", "desk", "stack",
    (("Start", "Ten you can explain"), ("Include", "Refusals and boring cases"), ("Drop", "Items you cannot defend")),
    (
        ("Ten you can explain", "Each task has an input and a reason it is in the set."),
        ("Include refusals", "Some items must not be answerable from the context."),
        ("Include the boring cases", "Empty input, extra fields, and the exact string keywords should catch."),
        ("Audit them", "If you cannot say why an item exists, drop it."),
        ("Grow later", "A large set nobody reads is weaker than a small set you trust."),
    ),
    ("Input", "Expected check", "Why this item exists", "Refusal or pass"),
    "A small set you trust beats a large set nobody can audit.",
)
L(
    "09-03", "rail", "four", "meters", "bars",
    (("Together", "Quality, safety, latency, cost"), ("A tradeoff", "A decision"), ("Denominator", "Successful tasks")),
    (
        ("Quality", "Did the task pass the check you wrote?"),
        ("Safety", "Did it refuse, leak, or take a forbidden action?"),
        ("Latency", "The time a person feels, including tools."),
        ("Cost", "Per successful task, not per hopeful call."),
        ("Decide in the open", "A quality gain that doubles the bill is a decision, not a silent ship."),
    ),
    ("Quality:80", "Safety passes:90", "Latency budget:55", "Cost budget:40"),
    "These lengths are a blank scorecard shape. Replace them with a real run. Higher is better only for quality and safety passes.",
    ("scorecard",),
)
L(
    "09-04", "gate", "rubric", "desk", "gates",
    (("Judge", "A second system"), ("Needs", "A written rubric"), ("Still", "A person owns the gate")),
    (
        ("Write the rubric", "The judge sees criteria, not a request to say if it is good."),
        ("Audit a slice", "Score some items yourself and compare. The judge has an error rate."),
        ("Pin the judge", "Record its model id the way you record any other model."),
        ("Watch the setup", "Do not hand the judge a channel that lets it cheat the rubric you wrote."),
        ("Person decides", "A judge score is evidence. It is not the release by itself."),
    ),
    ("Rubric", "Judge model", "Your audit slice", "Person at the gate"),
    "A judge model is a second system. It has its own failure rate.",
)
L(
    "09-05", "gate", "gate", "gate", "gates",
    (("Each is a release", "Prompt, model, index"), ("Tasks", "Change in their own commit"), ("Keep", "The previous score")),
    (
        ("Prompt release", "Same tasks, new score."),
        ("Model release", "Same tasks, new id, new score."),
        ("Index release", "Retrieval metrics first, then the answer."),
        ("Separate the set", "Do not edit the tasks and the prompt in one commit unless the set is the point."),
        ("Keep the baseline", "The previous score sits beside the new one."),
    ),
    ("Prompt change", "Model change", "Index change", "Compare to baseline", "Ship or fix"),
    "The tasks do not change in the same commit unless that change is the point.",
)
L(
    "09-06", "stack", "redteam", "shield", "stack",
    (("Whose system", "Yours"), ("Whose inputs", "Ones you control"), ("When", "Before the first limited release")),
    (
        ("Your boundaries", "Cases against your system, on inputs you control."),
        ("Injection fixture", "A document that tells the model to ignore the rules."),
        ("Tool misuse", "A request to send, delete, or read a secret."),
        ("Missing data", "A question the corpus cannot answer."),
        ("Put them in early", "These cases belong in the set before a limited release."),
    ),
    ("Injection fixture", "Forbidden tool call", "Secret file request", "Unanswerable question"),
    "You are checking your own system's boundaries. This is not a guide to attacking someone else.",
)
L(
    "09-07", "stack", "table", "desk", "stack",
    (("Lives beside", "The artifact"), ("Includes", "The failures"), ("Names", "Ids and the date")),
    (
        ("Attach it", "The scorecard names the prompt, the model id, and the index version."),
        ("Make it reopenable", "A table you can open next month."),
        ("Keep the failures", "The rows that failed stay visible."),
        ("Date it", "A score without a date will be quoted after the model has changed."),
        ("Write the gate", "Ship or not-yet, in a line a teammate can find."),
    ),
    ("Task id", "Pass or fail", "Model id", "Date", "Gate sentence"),
    "A table you can reopen beats a screenshot of one good answer.",
)
L(
    "10-01", "rail", "ladder", "route", "pipeline",
    (("Order", "Prompt, schema, retrieval, tools"), ("Train", "Only for the leftover gap"), ("Still", "Compare to the base")),
    (
        ("Prompt and schema", "Many gaps close here."),
        ("Retrieve or call a tool", "If the fact lives outside the model, fetch it."),
        ("Measure the rest", "The eval shows a gap those fixes did not close."),
        ("Then train", "Fine-tuning is for that remaining gap."),
        ("Compare again", "The adapter has to beat the base, including tasks that used to pass."),
    ),
    ("Prompt and schema", "Retrieval or a tool", "Eval the gap", "Only then LoRA", "Compare to base"),
    "Most reviews that start with a plan to fine-tune end earlier on this ladder.",
)
L(
    "10-02", "stack", "adapter", "layers", "layers",
    (("Train", "Small matrices"), ("Freeze", "The base"), ("QLoRA", "Quantized base, same adapter idea")),
    (
        ("Freeze the base", "Full fine-tuning updates every weight. That is expensive and easy to damage."),
        ("Train the adapter", "LoRA adds a low-rank update beside selected layers."),
        ("Save the adapter", "You do not save a second full copy of the model."),
        ("Record the base id", "An adapter without the matching base is not a model."),
        ("Say which you did", "QLoRA quantizes the frozen base so the job fits. You are still training the adapter."),
    ),
    ("Frozen layer", "Frozen layer", "Frozen layer", "Low-rank adapter", "Base id recorded"),
    "People mix the words quantize and fine-tune. In a review, say which one you did.",
    ("loss",),
)
L(
    "10-03", "gate", "dataset", "desk", "gates",
    (("Examples", "Teach the behavior"), ("Also teach", "Secrets left in the log"), ("Split", "Train is not the test")),
    (
        ("Match the job", "Input, output, and a refusal where refusal is correct."),
        ("Check the license", "You need the right to train on those rows."),
        ("Strip secrets", "Logs often contain secrets and personal data."),
        ("Keep the eval clean", "Training rows are not the scorecard."),
        ("Hold tasks out", "The score uses tasks the adapter did not memorize."),
    ),
    ("Format", "License", "Secret scan", "Held-out tasks"),
    "Examples teach the behavior. They also teach whatever you forgot was in the log.",
)
L(
    "10-04", "split", "compare", "meters", "compare",
    (("Same", "Tasks and grader"), ("Count", "Regressions"), ("Keep", "Only if the card says so")),
    (
        ("Same tasks", "The base and the adapter see the same set."),
        ("Same grader", "The rubric does not change between the runs."),
        ("Count regressions", "A win on a new task that breaks an old one is not an automatic ship."),
        ("Note the serve cost", "Latency and memory with the adapter loaded."),
        ("Keep or drop", "Only keep the adapter when the scorecard says so."),
    ),
    ("Base model on the golden set", "Adapter on the same set", "Regressions visible"),
    "Keep the adapter only if the card says so, including the tasks that used to pass.",
)
L(
    "10-05", "split", "prompt", "route", "compare",
    (("Usual end", "Schema, retrieval, or a smaller model"), ("Train for", "A pattern the index will not hold"), ("Do not train", "Facts you can update")),
    (
        ("Name the gap", "What fails today, and on which tasks?"),
        ("Try the cheap fix", "Prompt, schema, retrieval, or a tool."),
        ("Rescore", "If that fix passes, stop."),
        ("Train the rest", "A format or domain pattern that retrieval will not hold."),
        ("Do not memorize facts", "Facts belong in the index, where you can update them."),
    ),
    ("Stay with a prompt, schema, or tool", "Train only for the gap those left"),
    "Most we-should-fine-tune reviews end before training.",
)
L(
    "11-01", "stack", "policy", "desk", "stack",
    (("Length", "One page"), ("Names", "Data, tools, human actions"), ("Includes", "What you will not build")),
    (
        ("Data", "What you will send, store, and refuse to collect."),
        ("Tools", "What may run, and what is denied."),
        ("A person", "Send, pay, delete, and anything irreversible."),
        ("Out of scope", "What you will not build. That boundary is part of the policy."),
        ("Fit a page", "If it does not fit, the team will not apply it."),
    ),
    ("Data", "Tools", "Human approval", "Out of scope"),
    "Name the data, the tools, the actions that need a person, and what you will not build.",
)
L(
    "11-02", "rail", "retention", "desk", "pipeline",
    (("Prompts", "Often personal data"), ("A log", "A database"), ("Needs", "An end date")),
    (
        ("See the data", "Prompts are often personal. A debug log stores them."),
        ("Decide first", "Retention, access, and deletion before you turn logging on."),
        ("Keep the minimum", "Ids and metrics. Raw text only if the policy allows it."),
        ("Name access", "Who can read the log, and how you will know."),
        ("Set an end", "A log with no deletion date outlives the reason you kept it."),
    ),
    ("Decide retention", "Log ids and metrics", "Restrict access", "Delete on the date"),
    "Decide retention before you log the prompt.",
)
L(
    "11-03", "gate", "person", "shield", "gates",
    (("Drafting", "Is not doing"), ("Approve", "The exact arguments"), ("No", "Silent retry of a send")),
    (
        ("Draft", "The model may prepare the message."),
        ("Show the action", "Recipients, amount, path, or the row to delete."),
        ("Approve arguments", "Not a summary that hides a field."),
        ("Record it", "The trace names the person and the time."),
        ("No silent retry", "A failed send does not become a second send without a new approval."),
    ),
    ("Draft", "Show exact arguments", "Person approves", "Handler runs", "Trace records who"),
    "A person confirms the exact arguments of a side effect before the handler runs.",
)
L(
    "11-04", "stack", "incident", "desk", "stack",
    (("Better than", "A thread of screenshots"), ("Remove", "Secrets"), ("End with", "What you changed")),
    (
        ("What happened", "The input, the output, and the tool call, with secrets removed."),
        ("What you expected", "The check that failed."),
        ("Who is affected", "Data, a user, or a downstream system."),
        ("What you changed", "The prompt, the tool, the allowlist, or the task you added."),
        ("Where it lives", "A short note you can find again."),
    ),
    ("What happened", "Expected check", "Who is affected", "What changed"),
    "A short note beats a thread of screenshots.",
)
L(
    "11-05", "gate", "boundary", "shield", "gates",
    (("Will not", "Provide attack steps"), ("Will not", "Help evade a control"), ("Will", "Teach a refusal")),
    (
        ("No attack help", "The course does not provide exploit steps."),
        ("No evasion", "It does not help bypass a safety check, a license, or a person's consent."),
        ("Rules still apply", "The text is free to read. Your data rules still bind you."),
        ("Build a refusal", "The assistant you ship needs a way to say no."),
        ("Point at the boundary", "A student should be able to say what the system will not do."),
    ),
    ("No exploit steps", "No evasion help", "License and consent stand", "The product can refuse"),
    "The boundary is part of the teaching.",
)
L(
    "12-01", "stack", "job", "desk", "stack",
    (("Sentence", "Person, job, constraint"), ("Model", "After that"), ("Also", "A non-goal")),
    (
        ("A person", "Who is doing the job."),
        ("A job", "What they are trying to finish."),
        ("A constraint", "Time, money, privacy, or a risk they will not accept."),
        ("Then a model", "The model is an implementation choice."),
        ("Non-goals", "Say what version one will not do."),
    ),
    ("Person", "Job", "Constraint", "Non-goal", "Only then a model"),
    "A product sentence has a person, a job, and a constraint.",
)
L(
    "12-02", "stack", "spec", "desk", "stack",
    (("Fits", "One page"), ("Success", "Four numbers"), ("Milestone", "The smallest scored release")),
    (
        ("Problem", "The failure today, in the user's words."),
        ("User and non-goals", "Who it is for, and what you are not building."),
        ("Success", "Quality, safety, latency, and cost."),
        ("Risks", "Data, tools, and the actions that need a person."),
        ("First milestone", "The smallest release that can produce a scorecard."),
    ),
    ("Problem", "User and non-goals", "Success numbers", "Risks", "First milestone"),
    "Problem, user, non-goals, success, risks, and the first milestone.",
)
L(
    "12-03", "rail", "metrics", "meters", "bars",
    (("Share", "One table"), ("Quality", "Pass rate"), ("Cost", "Per success")),
    (
        ("Quality", "Pass rate on the versioned tasks."),
        ("Safety fails", "Leaks, bad actions, and missed refusals."),
        ("Latency", "What the person waits, at a percentile you name."),
        ("Cost per success", "Spend divided by tasks that passed."),
        ("One table", "Product and engineering read the same four numbers."),
    ),
    ("Quality:70", "Safety:85", "Latency:50", "Cost:45"),
    "A blank shape for the conversation, not a benchmark. Higher means more comfortable only after you define the direction of each number.",
    ("latency",),
)
L(
    "12-04", "gate", "states", "desk", "gates",
    (("Design", "Empty, slow, wrong, unsafe"), ("Wrong", "Shows the gap"), ("Unsafe", "Says what a person can do")),
    (
        ("Empty", "No data yet. Say what to add."),
        ("Slow", "Show that the model is working, and offer a way to cancel."),
        ("Wrong", "Show the citation gap or the parse error."),
        ("Unsafe", "The action was refused. Say what a person can do instead."),
        ("Cover all four", "The model will hit each of them."),
    ),
    ("Empty", "Slow", "Wrong", "Unsafe"),
    "The interface should say what happened. A spinner forever is not a design.",
)
L(
    "12-05", "rail", "release", "route", "pipeline",
    (("Order", "Prototype, eval, limited release"), ("Audience", "Named"), ("Off switch", "A kill switch")),
    (
        ("Prototype", "One path, on data you are allowed to use."),
        ("Eval", "The ten tasks, including refusals."),
        ("Limit the audience", "Name who has it."),
        ("Kill switch", "You can turn the feature off without a mystery deploy."),
        ("Read the card on a date", "Then expand, fix, or stop."),
    ),
    ("Prototype", "Eval", "Named audience", "Kill switch", "Read the scorecard"),
    "A limited release has a named audience, a kill switch, and a date you will read the scorecard.",
)
L(
    "12-06", "rail", "voice", "machine", "pipeline",
    (("Budget", "The whole wait"), ("Fallback", "Text and a person"), ("Evals", "Do not inherit the text score")),
    (
        ("Add the waits", "Recognition, the model, tools, and speech all spend the same latency budget."),
        ("Design handoff", "A person can take over, and the system can fall back to text."),
        ("Score speech apart", "Speech models fail in their own ways."),
        ("Decide silence", "Say what a pause means. Do not talk over the user."),
        ("Not a default", "Add voice when those designs exist."),
    ),
    ("Listen", "Model and tools", "Speak", "Handoff to a person"),
    "Speech recognition and speech synthesis do not replace the eval.",
)
L(
    "13-01", "gate", "folder", "folder", "gates",
    (("Corpus", "Notes you may use"), ("Questions", "Ones you wrote"), ("Tool", "One, read-only")),
    (
        ("Pick the folder", "A set whose license and privacy you can explain."),
        ("Write the questions", "Not a scraped set you do not have rights to."),
        ("Require citations", "Every factual claim points at a chunk id."),
        ("One read-only tool", "A calculator or a search over that folder."),
        ("Keep it small", "If you cannot name the folder, it is still a theme."),
    ),
    ("Allowed notes", "Your questions", "Citations", "One read-only tool"),
    "A folder you are allowed to use, questions you wrote, citations, and one read-only tool.",
)
L(
    "13-02", "stack", "tests", "desk", "stack",
    (("Write", "Tests before the prompt"), ("Include", "A refusal"), ("If awkward", "Narrow the capstone")),
    (
        ("Tests first", "Input, the expected citation or refusal, and the check."),
        ("Notice awkwardness", "If the test is hard to write, the capstone is still vague."),
        ("Include a refusal", "At least one question the notes do not answer."),
        ("Include the tool", "A case where it is required, and a case where it must not run."),
        ("Freeze them", "Prompt changes come after the tests exist."),
    ),
    ("Input", "Expected citation or refusal", "Tool used or not", "Check"),
    "If a test is awkward to write, the capstone is still too vague.",
)
L(
    "13-03", "stack", "log", "desk", "stack",
    (("Each entry", "Run, trace, metric, artifact"), ("Keep", "The failures"), ("One line", "The next decision")),
    (
        ("Four fields", "A run, a pointer to the trace, a metric, and an artifact."),
        ("Date and id", "So you know what produced the line."),
        ("Keep failures", "A broken run stays in the log."),
        ("One decision", "What you will change next, and why."),
        ("Stay short", "A page of entries beats a diary."),
    ),
    ("Date and model id", "Run", "Trace pointer", "Metric", "Next change"),
    "Each entry is a run, a trace pointer, a metric, and an artifact.",
)
L(
    "13-04", "rail", "demo", "route", "pipeline",
    (("Length", "Ten minutes"), ("Show", "Pass, refusal, trace, card"), ("Skip", "A tour of the code")),
    (
        ("A pass", "One question the notes answer, with the citation opened."),
        ("A refusal", "One question the notes do not answer."),
        ("The trace", "The tool call or the retrieval ids."),
        ("The scorecard", "The ten tasks, including failures."),
        ("The gate", "Say whether you would ship it, and why."),
    ),
    ("Pass with citation", "Refusal", "Trace", "Scorecard", "Ship or not yet"),
    "Show a pass, a refusal, the trace, and the scorecard. Do not show a tour of the code.",
)
L(
    "13-05", "gate", "next", "meters", "gates",
    (("Input", "The scorecard"), ("Output", "One change, or not yet"), ("Finished", "You can defend the gate")),
    (
        ("Read the rows", "Not the average alone."),
        ("Pick one change", "The failure with a clear fix."),
        ("Allow not yet", "A finished capstone can refuse to ship."),
        ("Name the owner", "Who would make the change, even if that is you."),
        ("Stop", "Defending the gate is the end of the capstone."),
    ),
    ("Read the failing rows", "Choose one fix", "Or say not yet", "Stop"),
    "The capstone is finished when you can defend the gate, including a gate that says not yet.",
)
