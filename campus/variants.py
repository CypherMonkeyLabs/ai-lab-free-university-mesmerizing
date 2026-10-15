"""Failure and debugging flows. Each one names that lesson's own steps."""

from __future__ import annotations

# (short title, caption). {step} is this lesson's step title. {fact} is one of its facts.
FAIL = {
    "00": [
        ("Blocked file", "“{step}” fails in some in-app browsers. Open the HTML file in a full browser. Nothing is uploaded."),
        ("Lost mark", "“{step}” is stored in this browser only. A second browser, or cleared storage, starts again. {fact}."),
        ("Missed search", "“{step}” only matches lesson text. A vague word can hide the page you wanted."),
        ("Thin proof", "“{step}” is not done when the chat looked fluent. Save a run, a trace, a metric, and an artifact."),
        ("Skipped rule", "“{step}” does not waive the safety rules. Private data stays local. Sending, paying, and deleting wait."),
        ("Wrong route", "“{step}” is a short path, not a different course. The track map is the full sequence."),
    ],
    "01": [
        ("Fluent miss", "“{step}” can sound sure with nothing in reach to cite. {fact}. Fluency is not a source."),
        ("Wrong counter", "“{step}” is counted by that model's tokenizer. A word average is not a budget."),
        ("Front dropped", "“{step}” shares one window. Overflow errors or cuts, and early instructions are a common casualty."),
        ("Truth knob", "“{step}” reshapes likelihood. It does not check facts. Temperature 0 is not a promise of identical bytes."),
        ("Role mix", "“{step}” belongs to one role. Tool text and documents are data, not new standing orders."),
        ("Unpinned id", "“{step}” names a role. Record the model id and the date. A family name hides version changes."),
    ],
    "02": [
        ("No outside check", "“{step}” is unfinished if the only judge is the model that wrote the answer. {fact}."),
        ("Schema skipped", "“{step}” still needs your parser. Schema mode helps. It does not replace validation."),
        ("Shape drift", "“{step}” teaches the wrong shape when the example does not match the real task, including a refusal."),
        ("Hidden jobs", "“{step}” packed several jobs into one paragraph. Split them and pass an artifact, not a vibe."),
        ("Endless revise", "“{step}” should stop after one revision. Score both drafts. Do not loop on taste."),
        ("Data as orders", "“{step}” can carry instructions. Mark the source as data and keep the job in a separate channel."),
    ],
    "03": [
        ("Accuracy myth", "“{step}” is a privacy and control choice. It is not a claim that local is more accurate. {fact}."),
        ("Open listener", "“{step}” should bind to localhost. The smoke check in this course calls 127.0.0.1 port 11434."),
        ("Does not fit", "“{step}” swaps, crashes, or refuses when the weights do not fit. 8 GB starts smaller. 16 GB is the 7B or 8B Q4 or Q5 start."),
        ("Bit grade", "“{step}” changes storage, not the quality grade. Measure the same prompts before and after."),
        ("Unread license", "“{step}” is not shippable until the weight license is recorded. If you are unsure, do not ship."),
        ("Mixed folders", "“{step}” mixes weights, prompts, and private data. Logs are a database. Keep the piles apart."),
    ],
    "04": [
        ("Key in the tree", "“{step}” leaked the key into the repo, the prompt, or the log. Read it at runtime from the environment. {fact}."),
        ("Trust the text", "“{step}” returned prose where a schema was required. Your parser is the gate. Do not guess a missing field."),
        ("Retry storm", "“{step}” retried without a budget. Set a timeout, a small retry count, and backoff."),
        ("Mystery bill", "“{step}” hides cost in output tokens, cache misses, tools, and retries. Read those, not a single sticker price."),
        ("Moved tasks", "“{step}” changed the tasks and the client together. Freeze the ten tasks and swap only the client."),
        ("Private log", "“{step}” stored the prompt text. Keep the model id, latency, and token counts. Drop the key and private text."),
    ],
    "05": [
        ("Empty index", "“{step}” has nothing to return when the chunks were never stored. {fact}. Rebuild before you blame the prompt."),
        ("Wrong embedder", "“{step}” used a different embedding model than the index. Neighbors will look confident and be wrong."),
        ("Lost heading", "“{step}” split through a section. Keep the heading with the chunk and overlap on purpose."),
        ("Rerank miracle", "“{step}” cannot cite a passage that retrieval never fetched. Fix recall before you tune the reranker."),
        ("Closed citation", "“{step}” named a source the reader cannot open. A citation is an id plus a span."),
        ("Stale middle", "“{step}” can be the wrong chunk, a stale chunk, the lost middle, or a missing fact. Name which one."),
    ],
    "06": [
        ("No stop", "“{step}” ran until the window ended. A loop needs a step cap and a stop you can point at. {fact}."),
        ("Handler skipped", "“{step}” let the model run the tool. The model may only propose. Your code validates and runs."),
        ("Silent side effect", "“{step}” sent, paid, or deleted without a person seeing the arguments. That action is ask, not allow."),
        ("Secret memory", "“{step}” wrote a secret into the thread, the file, or the store. Hidden memory is a second database."),
        ("Vague handoff", "“{step}” added a second agent with no artifact. One loop first. Name the file the next agent reads."),
        ("Summary only", "“{step}” kept the closing paragraph and dropped the trace. The calls, results, and approvals are the record."),
    ],
    "07": [
        ("Server is the model", "“{step}” treated the server as the model. The server offers tools, resources, and prompts. {fact}."),
        ("Silent install", "“{step}” connected a server the way a plugin installs. Read the tool list before anything runs."),
        ("Write by default", "“{step}” left write tools on. A docs server should not have them. Turn writes off until you need them."),
        ("Wide stdio", "“{step}” started a local process with the whole environment. Narrow the env and the root folder."),
        ("No remote auth", "“{step}” called a remote server with no authentication. Older servers used server-sent events. Current remote uses streamable HTTP."),
        ("Description as orders", "“{step}” pasted a tool description into the prompt as instructions. Treat that text as data."),
    ],
    "08": [
        ("Summary as diff", "“{step}” accepted the agent's summary. The result is the diff and the test command. {fact}."),
        ("Unknown command", "“{step}” edited before the test command was named. If you cannot name the command, stop."),
        ("Secret read", "“{step}” could see secrets, destructive git, or the network. Those stay off unless you explicitly allow them."),
        ("Plan skipped", "“{step}” edited before a person accepted the plan. A plan is cheap to reject."),
        ("Unread hunk", "“{step}” merged without reading every hunk. Rerun the same command the agent ran."),
        ("Blame the agent", "“{step}” treated “the agent did it” as a review. You own the change. Keep diffs small."),
    ],
    "09": [
        ("One pretty answer", "“{step}” shipped on a single impressive answer. The set is versioned, and the score sits beside the prompt, model, and index. {fact}."),
        ("Happy tasks only", "“{step}” omitted refusals and boring cases. Start with ten you can explain."),
        ("Missing number", "“{step}” reported quality and hid safety, latency, or cost. The four numbers move together."),
        ("Unaudited judge", "“{step}” let a second model grade without a rubric. Audit a slice. A person owns the gate."),
        ("Tangled release", "“{step}” changed the prompt, the model, and the index in one commit. Each is its own release."),
        ("Lost card", "“{step}” left the score in a chat. Attach a card you can reopen, including the failures."),
    ],
    "10": [
        ("Train first", "“{step}” trained before the prompt, schema, retrieval, and tools were measured. Train the leftover gap only. {fact}."),
        ("Rewritten base", "“{step}” updated the base weights. LoRA freezes the base and trains a small adapter. Record the base id."),
        ("Quantized means trained", "“{step}” used quantization and called it fine-tuning. QLoRA quantizes the frozen base. The adapter is what you train."),
        ("Secrets in the set", "“{step}” learned a secret that was left in a log. Strip secrets. Keep the eval tasks out of the training text."),
        ("New grader", "“{step}” changed the grader with the adapter. Same tasks, same grader, then count regressions."),
        ("Memorized fact", "“{step}” trained a fact the index should hold. If a cheap fix scores the same, do not train."),
    ],
    "11": [
        ("Unwritten policy", "“{step}” lived in a chat. The policy is one page: data, tools, and the actions a person must approve. {fact}."),
        ("Log first", "“{step}” stored prompts before you decided retention. Prompts are often personal data. A log is a database."),
        ("Draft equals send", "“{step}” treated a draft as the action. Show the exact arguments. Approve, then the handler runs."),
        ("Screenshot incident", "“{step}” left the incident in a thread of pictures. Write what happened, what you expected, who is affected, and what changed."),
        ("Attack help", "“{step}” asked for exploit steps or a way around a control. This course will not provide those. Build a refusal instead."),
        ("Scope creep", "“{step}” added a tool the one-page policy does not name. Out of scope stays off."),
    ],
    "12": [
        ("Model first", "“{step}” named a model before the person, the job, and the constraint. {fact}."),
        ("No non-goal", "“{step}” listed features and not the non-goals. The spec fits on one page, with four numbers."),
        ("One metric", "“{step}” reported quality and not safety failures, latency, and cost per success."),
        ("Happy path only", "“{step}” designed the success screen and not empty, slow, wrong, and unsafe."),
        ("Unlimited release", "“{step}” opened the feature to everyone. Prototype, then eval, then a named audience, with a kill switch."),
        ("Voice as the product", "“{step}” scored the transcript and ignored the waits. Budget the whole wait. Text and a person are the fallback."),
    ],
    "13": [
        ("Unallowed notes", "“{step}” indexed notes you are not allowed to use. The corpus is a folder you can name. {fact}."),
        ("Tests after", "“{step}” wrote the prompt before the questions, including a refusal and the tool case."),
        ("Pretty log", "“{step}” dropped the failed runs. Each entry is a run, a trace, a metric, and an artifact."),
        ("Demo of one", "“{step}” showed only the pass. A ten-minute demo includes a refusal, the trace, and the scorecard."),
        ("Must ship", "“{step}” forbade “not yet”. The gate can finish as one change, or as not yet."),
        ("No owner", "“{step}” left the next change unnamed. A person owns the decision."),
    ],
    "GL": [
        ("Name only", "“{step}” was recited without the mechanism. {fact}. Point at the track that practices it."),
        ("Neighbor term", "“{step}” borrowed the definition of the neighboring word. Quantization is not LoRA. An embedding model is not the chat model."),
        ("Missing limit", "“{step}” skipped the failure mode the definition includes."),
        ("No track", "“{step}” ended without the lesson id where you would try it."),
        ("Slogan", "“{step}” used a vendor slogan in place of the mechanism."),
        ("Collapsed pair", "“{step}” treated two tools as one. Say which object you freeze, store, score, or approve."),
    ],
    "IV": [
        ("Brand answer", "“{step}” named a product and not the control. {fact}."),
        ("No evidence", "“{step}” had no task set, trace, or score to point at."),
        ("Skipped cheaper", "“{step}” jumped to training or a bigger model before the cheap fix."),
        ("One number", "“{step}” reported quality and hid safety, latency, or cost."),
        ("Unowned gate", "“{step}” let a judge model be the release. A person owns the gate."),
        ("Vague allow", "“{step}” said “the agent can use tools” with no allowlist, schema, or step cap."),
    ],
    "FQ": [
        ("Hidden fee", "“{step}” implied an account or a certificate. The text is free under MIT. There is no certificate."),
        ("Required key", "“{step}” said you need a key to study. You need a browser. A model or a key is for a later practice."),
        ("Phone home", "“{step}” assumed the page uploads progress. Progress is in this browser. There are no remote assets."),
        ("Crowned model", "“{step}” asked for the best model. Fit the memory, read the license, smoke it, then measure."),
        ("Vibe proof", "“{step}” accepted a feeling in place of an artifact with four fields."),
        ("Work data", "“{step}” treated the MIT text as permission to upload an employer's data. The model license and the workplace rules remain."),
    ],
    "14": [
        ("Model owns the call", "“{step}” let the model decide the route. The platform still owns the queue. {fact}."),
        ("Emergency in the prompt", "“{step}” sent an emergency turn to the model. That turn belongs on the platform's emergency path."),
        ("Missing span", "“{step}” spoke a fact that was not in the retrieved pack. Refuse or transfer."),
        ("Unlogged handoff", "“{step}” transferred without writing why the person received the turn."),
        ("One blob of latency", "“{step}” blamed the AI. Time ASR, the model, and TTS as separate hops."),
    ],
    "EX": [
        ("Pasted ACL", "“{step}” was copied into a firewall. The matrix is a lesson. The change ticket names the real hosts. {fact}."),
        ("Invented customer", "“{step}” claimed a logo or a seat count. This course has no customer deployment."),
        ("Certificate implied", "“{step}” was treated as a certification. It is a study page."),
        ("Stale id shipped", "“{step}” pinned a model id from a dated snapshot without opening the vendor page."),
        ("No rollback", "“{step}” retired the old bot before the kill switch was tested."),
    ],
}

DEBUG = {
    "00": [
        ("Open the file", "Reproduce “{step}” in a full browser. Confirm the address is a local file and the page did not ask for a network."),
        ("Read storage", "Inspect the local mark for “{step}”. It is this browser's storage, not an account. {fact}."),
        ("Retry search", "Search the lesson id, then a phrase from the lesson. “{step}” should appear as its own row."),
        ("Count fields", "Lay out the run, the trace, the metric, and the artifact for “{step}”. Write “not measured” if that is true."),
        ("Name the rule", "Say which rule “{step}” is testing: local data, a person before a side effect, or untrusted text."),
    ],
    "01": [
        ("Show the tokens", "Print the tokenizer output for “{step}” from the model you will call. Do not use a word count."),
        ("Mark the window", "Add the instruction, source, chat, and reserved answer for “{step}”. {fact}. See what would be cut first."),
        ("Freeze a seed note", "Run “{step}” at a low temperature twice. Different bytes can both be valid. Look at the source, not the wording."),
        ("Separate roles", "Put “{step}” into system, user, or tool. Tool text stays data."),
        ("Pin and date", "Write the model id next to “{step}”. A role name is not the pin."),
    ],
    "02": [
        ("Write the check", "For “{step}”, write a check that a person or a program can run without asking the model."),
        ("Break the schema", "Feed “{step}” one missing field and one extra field. The parser must reject both."),
        ("Match an example", "Put a real task beside “{step}”, including a case that should refuse."),
        ("Diff one change", "Change only “{step}”. Keep the task set. Record quality, safety, latency, and cost."),
        ("Mark the channel", "Label the text in “{step}” as data. Restate the job outside that text."),
    ],
    "03": [
        ("Smoke localhost", "Run the tags check against 127.0.0.1 port 11434 before “{step}”. Save the output."),
        ("Fit the weights", "Compare “{step}” to the memory start: smaller on 8 GB, 7B or 8B at Q4 or Q5 on 16 GB. {fact}."),
        ("Two prompts", "Run the same two prompts before and after “{step}”. The bit label is not the score."),
        ("Record the license", "Paste the license name you found for “{step}” into the build log. If you cannot find it, stop."),
        ("List the folders", "Show the paths for weights, prompts, and data used by “{step}”. They should differ."),
    ],
    "04": [
        ("Grep the key", "Search the repo and the log for the secret used by “{step}”. The runtime read is the only copy you want."),
        ("Fail the parser", "Remove a required field from “{step}”. The handler must not guess. {fact}."),
        ("Cap the retries", "Count attempts for “{step}”. A timeout and a small budget should stop a storm."),
        ("Split the bill", "Write input tokens, output tokens, cache, tools, and retries for “{step}”. Leave prices blank until you read your own card."),
        ("Freeze the ten", "Hash the task ids for “{step}”. Only the client changes between runs."),
    ],
    "05": [
        ("Print the ids", "List chunk ids for “{step}”. An empty list is an index failure, not a prompt failure. {fact}."),
        ("Split the scores", "Show the keyword score and the vector score for “{step}”. They are allowed to disagree."),
        ("Open the span", "Open the cited span from “{step}” as a reader would. If you cannot, it is not a citation."),
        ("Ablate retrieval", "Score whether the right chunk is in the top results for “{step}” before you score the prose."),
        ("Check the clock", "Compare the document time on “{step}” with the question. Stale and missing are different failures."),
    ],
    "06": [
        ("Read the trace", "For “{step}”, list every call, result, approval, and the stop. The summary is not enough. {fact}."),
        ("Show arguments", "Print the arguments “{step}” would send. A person sees them before a side effect."),
        ("Name allow or ask", "Mark “{step}” allow, ask, or deny. Read-only may run inside the cap. Send, pay, and delete wait."),
        ("Replay twice", "Run “{step}” again with the same idempotency key. The effect should happen once."),
        ("Point at the artifact", "If a second agent is involved in “{step}”, name the file it received. A shared chat is not a handoff."),
    ],
    "07": [
        ("List primitives", "From “{step}”, label each capability as a tool, a resource, or a prompt. The server is not the model. {fact}."),
        ("Read before run", "Print the tool list “{step}” would expose. Approve side effects one by one."),
        ("Check transport", "Say whether “{step}” is stdio on the machine or streamable HTTP on the network. Authenticate the remote case."),
        ("Narrow the process", "Write the command, the environment, and the root folder for “{step}”."),
        ("Treat the text", "Quote a tool description from “{step}” and mark it as data, not as a new system instruction."),
    ],
    "08": [
        ("Open the diff", "Review every hunk from “{step}”. Ignore the closing summary. {fact}."),
        ("Rerun the command", "Run the test command named for “{step}”. If it was never named, stop before editing."),
        ("Read the denylist", "Confirm “{step}” cannot touch secrets, destructive git, or the network unless you allowed that verb."),
        ("Reject the plan", "Practice saying no to the plan in “{step}” before any file changes."),
        ("Own the patch", "Sign the review of “{step}” yourself. Keep the diff small enough to read."),
    ],
    "09": [
        ("Version the set", "Hash the tasks used for “{step}”. Write the prompt, model id, and index version beside the score. {fact}."),
        ("Include a refusal", "Add one refusal and one boring case to “{step}”. You should be able to explain all ten."),
        ("Fill four cells", "Write quality, safety failures, latency, and cost for “{step}”. A blank cell is not a pass."),
        ("Audit the judge", "Grade a slice of “{step}” by hand against the rubric. Pin the judge id if you keep using one."),
        ("Separate the commit", "Show that “{step}” changed only one of prompt, model, or index."),
    ],
    "10": [
        ("Score the cheap fix", "Record the prompt, schema, retrieval, or tool result for “{step}” before any training. {fact}."),
        ("Match the base id", "Write the frozen base id next to the adapter from “{step}”. Loading the adapter on a different base is a different model."),
        ("Say which tool", "State whether “{step}” is quantization or training. QLoRA is a quantized frozen base plus a trained adapter."),
        ("Scan the rows", "Search the training rows for “{step}” for secrets and for copies of the eval tasks."),
        ("Count regressions", "On the same tasks and grader, count what “{step}” made worse, not only what it improved."),
    ],
    "11": [
        ("Fit one page", "Check that “{step}” names data, tools, and human actions, and names what is out of scope. {fact}."),
        ("Retention first", "Write what “{step}” stores, for how long, and who can read it, before you turn the log on."),
        ("Approve the arguments", "Show the exact payload “{step}” would send. The draft is not the approval."),
        ("Write the incident", "Replace the screenshots for “{step}” with what happened, what you expected, who is affected, and what you changed."),
        ("Point at the boundary", "For “{step}”, the allowed response is a refusal plus the boundary. No exploit steps and no evasion help."),
    ],
    "12": [
        ("Read the sentence", "Underline the person, the job, and the constraint in “{step}”. The model comes after. {fact}."),
        ("Find the non-goal", "List one thing “{step}” will not do. If you cannot, the spec is not done."),
        ("Share the table", "Put quality, safety failures, latency, and cost per success for “{step}” in one table."),
        ("Walk the states", "Open empty, slow, wrong, and unsafe for “{step}”. Wrong should show the gap, not invent a fact."),
        ("Name the switch", "Write the audience and the kill switch for “{step}” before a wider release."),
    ],
    "13": [
        ("Name the folder", "Point at the notes “{step}” is allowed to use. If you cannot, stop. {fact}."),
        ("Read the tests", "Confirm “{step}” has questions written first, including a refusal and the read-only tool."),
        ("Open a failure", "Reopen one failed entry from “{step}”. It should still have a run, a trace, a metric, and an artifact."),
        ("Time the demo", "Rehearse “{step}” in ten minutes: a pass, a refusal, the trace, and the scorecard."),
        ("Allow not yet", "Write the gate result for “{step}” as one change or as not yet, and name the owner."),
    ],
    "GL": [
        ("Point at the mechanism", "For “{step}”, say what object moves: a token, a weight, a chunk, a call, or a score. {fact}."),
        ("Name the neighbor", "Say what “{step}” is not. The usual collisions are tokenizer versus word count, and LoRA versus quantization."),
        ("Find the track", "Name the lesson id where you would practice “{step}”."),
        ("Add the limit", "State the failure “{step}” still has after the happy definition."),
        ("Use it once", "Write one sentence that uses “{step}” to make a decision, not to decorate a slide."),
    ],
    "IV": [
        ("Say the mechanism", "Answer “{step}” in one sentence about the mechanism, then stop. {fact}."),
        ("Name the control", "Add the knob a person can turn for “{step}”: the set, the allowlist, the cap, or the gate."),
        ("Point at evidence", "Name the artifact you would open for “{step}”. A product name is not evidence."),
        ("Exclude the cheap fix", "Say which cheaper change you tried before “{step}”."),
        ("Four cells", "If “{step}” is a release decision, state quality, safety, latency, and cost."),
    ],
    "FQ": [
        ("Answer first", "The first sentence of “{step}” should answer the question. Detail comes after. {fact}."),
        ("State the limit", "Add the limit that still applies to “{step}”: license, workplace rules, or safety."),
        ("Point at the track", "Name where in the course “{step}” is practiced."),
        ("No certificate", "If “{step}” asks for proof, point at the capstone folder, not a certificate."),
        ("Stay local", "If “{step}” is about the page itself, confirm progress stays in this browser."),
    ],
    "14": [
        ("Name the owner", "For “{step}”, write who owns the audio, the queue, and the emergency path. {fact}."),
        ("Read the pack", "List the chunk ids “{step}” was allowed to speak from. An empty list is a refusal."),
        ("Split the hops", "Time ASR, retrieval, the model, and TTS for “{step}” as four numbers."),
        ("Write the handoff", "Record why a person received “{step}” and what they were given."),
        ("Leave emergency", "Confirm “{step}” cannot be the only path to emergency services."),
    ],
    "EX": [
        ("Open the source", "For “{step}”, name the paper or the spec, and say whether it was re-fetched. {fact}."),
        ("Point at the center", "Draw app, policy, and trace. Put the sister system outside that box."),
        ("Write the rollback", "Name the old path and the person who may throw the kill switch for “{step}”."),
        ("Confirm the port", "Look up the listener for “{step}” on the host you run. Do not paste the study matrix."),
        ("State the limit", "Add the sentence “{step}” will not certify: legal advice, a customer story, or a vendor ACL."),
    ],
}

LAYOUTS = ("stack", "gate", "rail", "split", "loop", "funnel")


def _school(lid: str) -> str:
    if lid[:2] in FAIL:
        return lid[:2]
    head = lid.split("-", 1)[0]
    if head not in FAIL:
        raise SystemExit(f"No failure bank for {lid}")
    return head


def _pick(bank: dict, lid: str, steps: list, facts: list) -> list[tuple[str, str]]:
    school = _school(lid)
    patterns = bank[school]
    start = sum(ord(char) for char in lid) % len(patterns)
    fact = facts[start % len(facts)][1] if facts else school
    chosen = []
    for offset, (title, caption) in enumerate(steps):
        pattern_title, template = patterns[(start + offset) % len(patterns)]
        label = f"{pattern_title}"
        # Keep the box label short and unique to this step.
        short = title if len(title) <= 22 else title[:21] + "…"
        text = template.format(step=title, fact=fact)
        chosen.append((f"{label}: {short}" if len(label) + len(short) < 36 else short, text))
    return chosen


def extra_flows(lid: str, spec: dict) -> list[tuple[str, str, str, list[tuple[str, str]]]]:
    steps = list(spec["steps"])
    facts = list(spec["facts"])
    primary = spec["layout"]
    options = [item for item in LAYOUTS if item != primary]
    start = sum(ord(char) for char in lid)
    fail_layout = options[start % len(options)]
    debug_layout = options[(start + 2) % len(options)]
    fail_steps = _pick(FAIL, lid, steps, facts)
    debug_steps = _pick(DEBUG, lid, steps, facts)
    if len(fail_steps) < 4 or len(debug_steps) < 4:
        raise SystemExit(f"{lid} variant is too short")
    return [
        (f"{lid}-fail", f"When {lid} fails", fail_layout, fail_steps),
        (f"{lid}-debug", f"How to inspect {lid}", debug_layout, debug_steps),
    ]
