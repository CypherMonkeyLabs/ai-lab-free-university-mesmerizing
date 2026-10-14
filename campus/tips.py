"""Per-track tips, interview traps, and cheat sheets for the settings layer."""

from __future__ import annotations

import html
import json

# id -> name, tips, traps, sheet rows (term, line)
TIPS: dict[str, dict] = {
    "00": {
        "name": "Start here",
        "tips": [
            "Save four fields for every practice: what you ran, the trace, a metric, and a file you can reopen.",
            "Mark a lesson complete only when you can teach it without the page.",
            "Serve the folder or open the published site. A disk path cannot load the tracks.",
        ],
        "traps": [
            "Treating a fluent tour of product names as the skill. The check is a mechanism plus an artifact.",
            "Studying from an in-app browser. Scripts and the track files often never load.",
        ],
        "sheet": [
            ["Proof", "Run, trace, metric, artifact."],
            ["Progress", "Stored in this browser only."],
            ["Order", "Models, prompts, grounding, tools, then evals."],
            ["Stop", "Side effects wait for a person."],
        ],
    },
    "01": {
        "name": "How models work",
        "tips": [
            "Say next-token prediction before you say the model 'knows' something.",
            "Count with that model's tokenizer. A word count is not a token count.",
            "Temperature and top-p change variety. They do not add facts.",
        ],
        "traps": [
            "Calling a family name a version. Pin the model id and the date.",
            "Treating a longer context window as proof the model read the middle.",
        ],
        "sheet": [
            ["Token", "The unit the model scores, not a word."],
            ["Window", "Instructions, sources, chat, and the answer share it."],
            ["Sample", "Temperature and top-p reshape a fixed distribution."],
            ["Hallucination", "Fluent text with no source you can open."],
        ],
    },
    "02": {
        "name": "Prompting",
        "tips": [
            "Write the job, the output shape, and a check that does not ask the model.",
            "Change one thing and keep both outputs.",
            "Put untrusted text in a data channel. The job does not have to obey it.",
        ],
        "traps": [
            "Grading a prompt by whether the prose sounds better.",
            "Trusting schema mode without a parser you wrote.",
        ],
        "sheet": [
            ["Job", "One sentence a stranger can test."],
            ["Done", "A schema, a citation, or a refusal."],
            ["Injection", "Source text can carry instructions."],
            ["Diff", "One variable, both outputs saved."],
        ],
    },
    "03": {
        "name": "Local models",
        "tips": [
            "Local is a privacy and latency choice, not an accuracy claim.",
            "Start with a size the machine can hold. Label a mock run as mock.",
            "Keep weights, prompts, and private notes in separate folders.",
        ],
        "traps": [
            "Assuming a quantized model is the same model. Rescore the tasks.",
            "Binding a runner on a public interface. Localhost is the smoke check.",
        ],
        "sheet": [
            ["Why local", "Data stays on the machine."],
            ["Fit", "Memory first, then quality."],
            ["Quantize", "Fewer bits are a storage choice."],
            ["License", "The weight license is not this course's license."],
        ],
    },
    "04": {
        "name": "APIs and cost",
        "tips": [
            "Keep the key in the environment or a secret store, never in the repository.",
            "Read input, output, cache, and tool calls as separate lines.",
            "Log ids and counts. Drop the key and the raw private text.",
        ],
        "traps": [
            "Retrying a hung call until the bill arrives.",
            "Trusting a structured-output flag without validating the JSON yourself.",
        ],
        "sheet": [
            ["Key", "Outside the repo. Spend cap on."],
            ["Bill", "Input, output, cache, tools."],
            ["Timeout", "A hung call and a retry storm are both defects."],
            ["Log", "Ids and counts, not secrets."],
        ],
    },
    "05": {
        "name": "Retrieval",
        "tips": [
            "Measure whether the right chunk was found before you score the prose.",
            "Cite an id and a span a person can open. If the span is absent, refuse.",
            "Keep keywords for exact strings and vectors for paraphrase.",
        ],
        "traps": [
            "Letting the chat model double as the embedding model.",
            "Asking a reranker to cite a passage the first stage never fetched.",
        ],
        "sheet": [
            ["Chunk", "Split on structure. Stable id."],
            ["Embed", "Pin the embedding model on the index."],
            ["Cite", "Id plus a span, or refuse."],
            ["Score", "Recall on the right chunk first."],
        ],
    },
    "06": {
        "name": "Agents",
        "tips": [
            "Name done before the loop starts, with a check that does not ask the model.",
            "The model proposes a call. Your code checks the schema and runs the handler.",
            "A step cap, a done-check, or a person. A loop without a stop is not a design.",
        ],
        "traps": [
            "Treating 'approved: true' inside a tool argument as approval.",
            "Retrying a payment or an email without an idempotency key.",
        ],
        "sheet": [
            ["Propose", "The model does not run the handler."],
            ["Schema", "Missing fields are a reject, not a guess."],
            ["Allow", "Read-only may run. Send, pay, and delete wait."],
            ["Trace", "Calls, results, approvals, and the stop."],
        ],
    },
    "07": {
        "name": "MCP",
        "tips": [
            "The host decides what may run. The client opens the session. The server exposes tools.",
            "A tool description is data the model will read, not a new order.",
            "Stdio is a local process. Narrow its command, environment, and root folder.",
        ],
        "traps": [
            "Installing a server the way you bookmark a page. A local server can read files.",
            "Auto-approving every tool because the handshake succeeded.",
        ],
        "sheet": [
            ["Host", "The app a person uses."],
            ["Tool", "An action with a description and a schema."],
            ["Resource", "Readable data. Still untrusted text."],
            ["Transport", "Stdio locally. Streamable HTTP remotely."],
        ],
    },
    "08": {
        "name": "Coding agents",
        "tips": [
            "Review the diff and the tests, not the agent's closing summary.",
            "Point the agent at a repository you trust, with a branch you can throw away.",
            "A human gate sits before push, deploy, or a change to auth.",
        ],
        "traps": [
            "Accepting a green summary when the tests were not run.",
            "Letting the agent widen its own permissions mid-task.",
        ],
        "sheet": [
            ["Plan", "Say the files before the edits."],
            ["Diff", "Read the patch."],
            ["Tests", "The command and the result."],
            ["Gate", "A person before push."],
        ],
    },
    "09": {
        "name": "Evals",
        "tips": [
            "Version the task file. Changing it is its own commit.",
            "Score quality, safety, latency, and cost on the same tasks.",
            "Not yet is a finished result. A person owns the gate.",
        ],
        "traps": [
            "Shipping on one pretty answer.",
            "Comparing two runs that did not share the task set or the grader.",
        ],
        "sheet": [
            ["Tasks", "Ten you can explain, including a refusal."],
            ["Pin", "Prompt, model id, and index version."],
            ["Baseline", "Same tasks, same grader."],
            ["Gate", "Ship or fix. Write the decision."],
        ],
    },
    "10": {
        "name": "Fine-tuning",
        "tips": [
            "LoRA is a low-rank update, not a new base model. Compare it on the same tasks.",
            "Train only after evals say prompting and retrieval are the wrong shape.",
            "Keep the base model. The adapter is the thing you can turn off.",
        ],
        "traps": [
            "Picking a rank because it sounds large. Rank is a budget.",
            "Calling a better demo a fine-tune win without the baseline score.",
        ],
        "sheet": [
            ["When", "The score says the base model is the wrong shape."],
            ["LoRA", "Low-rank matrices, frozen base weights."],
            ["Compare", "Same tasks as the base model."],
            ["Stop", "Most readers should not train yet."],
        ],
    },
    "11": {
        "name": "Safety",
        "tips": [
            "Write the policy as a page: data you may send, tools you allow, actions that wait.",
            "Model output is untrusted text, including text that claims to be instructions.",
            "A refusal you can test belongs in the eval set.",
        ],
        "traps": [
            "Letting a tool send, pay, delete, or push because the draft looked correct.",
            "Pasting secrets or customer data into a hosted model because a lesson mentioned an API.",
        ],
        "sheet": [
            ["Data", "Name what may leave the machine."],
            ["Tools", "Allow, ask, deny."],
            ["Person", "Send, pay, delete, and push wait."],
            ["Output", "Untrusted, even when it cites a policy."],
        ],
    },
    "12": {
        "name": "Product skills",
        "tips": [
            "Specify the job, the user, the failure states, and the number you will watch.",
            "A feature a product manager and an engineer can both measure is the goal.",
            "Say when not to use a model. That is part of the spec.",
        ],
        "traps": [
            "Shipping a demo as a product because the happy path was fluent.",
            "Hiding latency and cost in a single quality score.",
        ],
        "sheet": [
            ["Job", "Who it is for and what done means."],
            ["Failure", "Empty, wrong, refused, and slow."],
            ["Number", "Quality, safety, latency, and cost."],
            ["Kill", "Name the audience and the switch."],
        ],
    },
    "13": {
        "name": "Capstone",
        "tips": [
            "Use notes you are allowed to store. If you cannot name the folder, stop.",
            "One tool, citations, ten eval tasks, and a safety page.",
            "A stranger should open the artifact without you in the room.",
        ],
        "traps": [
            "Building the assistant on customer data because it makes a better demo.",
            "Skipping the eval set because the sample answers looked right.",
        ],
        "sheet": [
            ["Notes", "A folder you may use."],
            ["Cite", "An id a person can open."],
            ["Tool", "One, with a schema and a stop."],
            ["Show", "Task, artifact, and the falsifier."],
        ],
    },
    "GL": {
        "name": "Glossary",
        "tips": [
            "Use the course's definition, then check it against the spec or the paper.",
            "If two lessons use a word differently, the later mechanism wins.",
        ],
        "traps": [
            "Reciting a vendor's marketing gloss as the definition.",
        ],
        "sheet": [
            ["Token", "What the model counts."],
            ["Tool", "A named action with a schema."],
            ["Trace", "The record, not the summary."],
            ["Gate", "A decision a person owns."],
        ],
    },
    "IV": {
        "name": "Interview practice",
        "tips": [
            "Answer in three beats: the mechanism, the evidence, the failure you watch.",
            "Say the step cap before you say the model name.",
            "Bring a lab file a stranger can open.",
        ],
        "traps": [
            "Listing product names when the question asked how you would stop the loop.",
            "Claiming a score you cannot show.",
        ],
        "sheet": [
            ["30 seconds", "Mechanism in plain language."],
            ["90 seconds", "Add the artifact and the failure."],
            ["Local or hosted", "Where the prompt goes, and where the key lives."],
            ["Stop", "Step cap, done-check, or a person."],
        ],
    },
    "FQ": {
        "name": "Questions",
        "tips": [
            "The campus does not issue a certificate. The capstone folder is the evidence.",
            "A current browser is enough to study. A key is optional and comes later.",
        ],
        "traps": [
            "Opening the HTML as a local file and concluding the course is empty.",
        ],
        "sheet": [
            ["Open", "A static server, or the published site."],
            ["Offline", "After one visit, the service worker keeps the files."],
            ["Key", "Not required to read or to run the labs."],
            ["License", "MIT for the course text. Not for model weights."],
        ],
    },
}


def tips_payload() -> str:
    return json.dumps(TIPS, ensure_ascii=True).replace("<", "\\u003c")


def tips_drawer() -> str:
    options = []
    for key, pack in TIPS.items():
        options.append(f'<option value="{html.escape(key)}">{html.escape(pack["name"])}</option>')
    return f"""
<dialog id="tipsDrawer" class="sheet" aria-labelledby="tipsTitle">
  <h2 id="tipsTitle">Tips and tricks</h2>
  <p class="lede">Pro tips, interview traps, and a cheat sheet for the track you are in.</p>
  <label class="set-row">Track
    <select id="tipsTrack">{''.join(options)}</select>
  </label>
  <div id="tipsBody"></div>
  <p><button type="button" class="btn" data-close>Close</button></p>
  <script type="application/json" id="tipsData">{tips_payload()}</script>
</dialog>
"""
