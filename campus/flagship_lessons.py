"""Ecosystem and gap-audit track. Facts are teaching claims with a source or a limit."""

from __future__ import annotations

from campus.schema import CK, H, NT, OL, P, TB, UL, WN, lesson

LESSONS: list[dict] = []


def add(item: dict) -> None:
    LESSONS.append(item)


add(lesson(
    "EX-01", "EX", "core", 12,
    "The ecosystem around a system you ship",
    "A shipped assistant borrows a model, an index, a tool loop, a trace, a cloud account, and sometimes a voice stack. None of those own your policy.",
    [
        P("The center is the system you are accountable for: the app, the policy, and the trace. Sister technologies plug into that center. They do not replace the owner of the data or the owner of the call."),
        H("Six families"),
        UL([
            "Model providers compute the next token behind an API or a weight file.",
            "Vector stores return neighbors. They do not decide that a chunk is true.",
            "Orchestration is the loop: prompt, tool, observation, stop. MCP is a protocol inside that family.",
            "Observability and evals tell you what happened and whether the change may ship.",
            "Cloud accounts bill, isolate, and region-pin the run.",
            "Voice stacks turn audio into text and back. The contact platform still owns the call.",
        ]),
        TB(
            ["Family", "Job", "Does not own"],
            [
                ["Model", "Next-token scores", "Your corpus or your tools"],
                ["Vectors", "Nearest chunks under a filter", "The decision to trust a chunk"],
                ["Loop", "Tool calls until a stop rule", "Permission to send, pay, or delete"],
                ["Evals", "The same tasks, scored again", "A single pretty demo"],
                ["Cloud", "Identity, region, bill", "Your product policy"],
                ["Voice", "ASR, turn-taking, TTS", "Emergency calling or the queue"],
            ],
        ),
        NT("Snapshot, not a lineup", "Vendor model ids move. The 2026-10-14 study draft quoted specific ids from vendor pages. Those sentences stay in the rooms that cited them, and they were not re-fetched on 2026-10-15."),
        CK("What sits at the center of the map?", "The system you are accountable for: app, policy, and trace. The six families are neighbors, not owners."),
    ],
))

add(lesson(
    "EX-02", "EX", "core", 14,
    "Architecture from a prompt to a gate",
    "Draw the path before you pick a vendor: input, policy, retrieval, model, tools, trace, and a person at every side effect.",
    [
        P("A fundamentals path is tokens, context, and sampling. An advanced path is the same path with a schema, a retrieved span, a tool allowlist, and a gate. The pictures differ. The habit does not."),
        H("Boxes you should be able to point at"),
        OL([
            "Caller or user, and the channel they are actually on.",
            "Policy: what data may leave the machine, and which actions need a person.",
            "Retriever: chunk id, score, and the refusal when the span is missing.",
            "Model: a pinned id, a token budget, and a timeout.",
            "Tools: name, schema, permission, and an idempotent handler.",
            "Trace: prompt version, retrieval ids, tool calls, latency, cost.",
            "Gate: quality, safety, latency, and cost on a versioned task set.",
        ]),
        WN("Demo architecture", "A chat box with no retriever and no trace is a demo. Do not draw it as the production path."),
        CK("Where does a person sit in this architecture?", "On every side effect: send, pay, delete, and any cutover. The model does not approve itself."),
    ],
))

add(lesson(
    "EX-03", "EX", "practice", 16,
    "Deployment and configuration walkthrough",
    "Configure the run you can roll back: pinned ids, secrets outside the repo, a timeout, a log that omits raw private text, and a kill switch.",
    [
        P("Deployment here means the smallest hosted or local run that a second person can start from the README. It is not a cluster diagram."),
        H("Walkthrough"),
        OL([
            "Write the model id, the embedding id, and the prompt version in one config file.",
            "Put the API key in the environment or a secret store. Refuse to start if the key is inside the repo.",
            "Bind a local runner to loopback until you have a reason to expose it.",
            "Set a timeout and a retry cap. A retry must not double-send.",
            "Log request ids, token counts, retrieval ids, and tool names. Drop the key and the raw private text.",
            "Name the kill switch: the flag, the person who may throw it, and the old path you return to.",
        ]),
        TB(
            ["Setting", "Safe default", "Check"],
            [
                ["Model id", "Pinned snapshot, not a family name", "The id in the log matches the config"],
                ["Secrets", "Environment or secret store", "A repo search finds no key"],
                ["Timeout", "Shorter than the user's patience", "A hung call fails closed"],
                ["Log", "Ids and counts", "A sample line has no private paragraph"],
            ],
        ),
        NT("Unverified product screens", "Console click-paths for a specific host were not re-checked on 2026-10-15. Use this list as the checklist, then confirm the screen in the vendor doc."),
        CK("What must a log line leave out?", "The API key and the raw private text. Keep ids and counts."),
    ],
))

add(lesson(
    "EX-04", "EX", "practice", 16,
    "Migration and cutover from a legacy bot",
    "Move off a rules bot or a pasted FAQ only when the new path wins on a written task set, with a rollback to the old bot.",
    [
        P("Legacy here means the thing users already have: a decision tree, a keyword FAQ, a macro in the agent desktop, or a prompt with no eval. The cutover is a product change, not a model swap."),
        H("Checklist"),
        OL([
            "Inventory the answers the old bot gives and the source each answer is allowed to use.",
            "Write ten tasks the old bot fails, including a refusal and a boring case.",
            "Index only documents you are allowed to store. Record the embedding model id on the index.",
            "Run shadow mode: the new path answers beside the old one, and users still see the old one.",
            "Compare retrieval first. A better paragraph on the wrong chunk is not a win.",
            "Cut over a named audience. Keep the old bot one switch away.",
            "Stop the cutover if safety failures rise or if the trace goes blank.",
        ]),
        H("Cutover plan"),
        TB(
            ["Phase", "Users see", "Exit"],
            [
                ["Shadow", "The old bot", "Ten tasks scored, retrieval measured"],
                ["Limited", "The new path, one queue or one team", "No new safety failures, kill switch tested"],
                ["Wider", "The new path, with the old bot still deployed", "A written rollback owner"],
                ["Retire", "The new path", "The old bot's tasks still live in the eval set"],
            ],
        ),
        CK("When is the old bot allowed to leave?", "After the limited audience holds and the old bot's tasks are still in the eval set. Not on demo day."),
    ],
))

add(lesson(
    "EX-05", "EX", "practice", 14,
    "Troubleshooting playbook",
    "Split a bad answer into retrieval, the model, the tool, the policy, and the channel before you change a prompt.",
    [
        P("A playbook is a sequence you can follow at 2 a.m. Each step has a fact you can read in a log, not a hunch."),
        H("Order"),
        OL([
            "Read the trace. If there is no trace, stop and add one. You cannot debug a blank board.",
            "Check the retrieval pack. If the fact is absent, fix the index or refuse. Do not raise temperature.",
            "Check the tool result. If the handler erred, the model is quoting your bug.",
            "Check the policy. A refusal that should have fired is a gate bug, not a tone bug.",
            "Check latency by hop: network, retrieval, model, tool, and, on a phone, ASR and TTS.",
            "Change one thing. Rescore the same tasks. Write down the regression.",
        ]),
        TB(
            ["Symptom", "First place to look", "Do not"],
            [
                ["Confident wrong fact", "Was the span in the pack?", "Ask the model if it is sure"],
                ["Blank answers", "Timeouts and the token budget", "Fine-tune"],
                ["Double charge or double send", "Retry and idempotency", "Add another agent"],
                ["Slow phone turn", "ASR, model, TTS, separately", "Blame 'the AI' as one hop"],
            ],
        ),
        CK("What is the first move when the trace is empty?", "Stop and add a trace. A prompt edit on a blank board does not explain the next failure."),
    ],
))

add(lesson(
    "EX-06", "EX", "advanced", 18,
    "Ports, protocols, and a firewall study matrix",
    "Learn the ports this campus actually talks about, then confirm the listener on the host you run. This table is a study matrix, not an ACL to paste into production.",
    [
        P("Protocols here are the ones an AI system meets: HTTPS to a model API, a local runner, trace export, and, when the user is on a phone, SIP and RTP. MCP over stdio has no port. Remote MCP uses HTTP."),
        H("Study matrix"),
        TB(
            ["Name", "Port", "Transport", "Status of this row"],
            [
                ["HTTPS model API", "443", "TCP", "The usual web port. Confirm the vendor host."],
                ["DNS", "53", "UDP and TCP", "Name lookup. Standard, still confirm your resolver."],
                ["OTLP gRPC", "4317", "TCP", "OpenTelemetry's documented default. Not re-fetched 2026-10-15."],
                ["OTLP HTTP", "4318", "TCP", "OpenTelemetry's documented default. Not re-fetched 2026-10-15."],
                ["Ollama default", "11434", "TCP", "The project's widely published loopback default. Not re-fetched 2026-10-15. Bind it to localhost until you mean to share it."],
                ["SIP", "5060", "UDP and TCP", "RFC 3261. Confirm the listener you deploy."],
                ["SIP over TLS", "5061", "TCP", "The commonly assigned TLS port. Confirm in the IANA registry before you lock a firewall."],
                ["RTP media", "a configured range", "UDP", "Not one universal port. The range is a design choice on your SBC."],
                ["MCP stdio", "none", "local process", "MCP spec: a process, not a socket. This campus cites the 2025-06-18 revision."],
                ["Remote MCP", "443 or the port you choose", "TCP", "HTTP. Do not assume a secret default."],
            ],
        ),
        P("Sources to open: RFC 3261 at rfc-editor.org, the OpenTelemetry OTLP spec at opentelemetry.io, the MCP specification at modelcontextprotocol.io, and the Ollama project docs. The IANA service registry is the place to confirm 5060 and 5061. Those pages were not re-fetched on 2026-10-15."),
        H("Firewall matrix, for study"),
        TB(
            ["From", "To", "Allow", "Refuse"],
            [
                ["App server", "Model API", "443 to the pinned host", "Any host not on the list"],
                ["App server", "Trace collector", "4317 or 4318 to your collector", "A public collector you did not choose"],
                ["Laptop", "Local runner", "11434 on loopback", "11434 on every interface, by default"],
                ["SBC", "Voice platform", "SIP and the RTP range you designed", "A wide-open UDP any-to-any rule copied from a blog"],
                ["Model", "Your tools", "Nothing. The model does not open sockets.", "A tool the host did not allow"],
            ],
        ),
        WN("Not an ACL", "Pasting this matrix into a firewall is a mistake. It is a lesson. Your change ticket names the real hosts."),
        H("Ladder, for study"),
        {
            "t": "svg",
            "caption": "Study ladder. Emergency never enters the model. Confirm every port on the host you run.",
            "html": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 300" role="img" aria-labelledby="ex06ladder">
<title id="ex06ladder">App calls a model API on 443, exports a trace on 4318, and leaves emergency calls on the voice platform</title>
<rect width="720" height="300" rx="16" fill="#070b16"/>
<text x="80" y="36" fill="#67e8f9" font-family="system-ui,sans-serif" font-size="14" text-anchor="middle">App</text>
<text x="280" y="36" fill="#67e8f9" font-family="system-ui,sans-serif" font-size="14" text-anchor="middle">Model API</text>
<text x="480" y="36" fill="#67e8f9" font-family="system-ui,sans-serif" font-size="14" text-anchor="middle">Collector</text>
<text x="640" y="36" fill="#fb7185" font-family="system-ui,sans-serif" font-size="14" text-anchor="middle">Voice platform</text>
<line x1="80" y1="48" x2="80" y2="270" stroke="#1e3a52"/>
<line x1="280" y1="48" x2="280" y2="270" stroke="#1e3a52"/>
<line x1="480" y1="48" x2="480" y2="270" stroke="#1e3a52"/>
<line x1="640" y1="48" x2="640" y2="270" stroke="#fb7185" stroke-dasharray="4 4"/>
<line x1="80" y1="90" x2="280" y2="90" stroke="#34d399" marker-end="url(#ex06a)"/>
<text x="180" y="82" fill="#e7f6ff" font-family="system-ui,sans-serif" font-size="12" text-anchor="middle">443 HTTPS, pinned host</text>
<line x1="280" y1="140" x2="80" y2="140" stroke="#93b4c9"/>
<text x="180" y="132" fill="#93b4c9" font-family="system-ui,sans-serif" font-size="12" text-anchor="middle">response or timeout</text>
<line x1="80" y1="190" x2="480" y2="190" stroke="#22d3ee"/>
<text x="280" y="182" fill="#e7f6ff" font-family="system-ui,sans-serif" font-size="12" text-anchor="middle">4318 OTLP HTTP, your collector</text>
<text x="640" y="160" fill="#fb7185" font-family="system-ui,sans-serif" font-size="12" text-anchor="middle">emergency</text>
<text x="640" y="178" fill="#fb7185" font-family="system-ui,sans-serif" font-size="12" text-anchor="middle">stays here</text>
<defs><marker id="ex06a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6 Z" fill="#34d399"/></marker></defs>
</svg>""",
        },
        CK("Why is there no port on MCP stdio?", "Stdio is a local process with a command, an environment, and a root folder. A port appears only when you choose HTTP."),
    ],
))

add(lesson(
    "EX-07", "EX", "advanced", 16,
    "Voice bridge: SIP, PSTN, recording, WFM, and emergency calls",
    "The phone system owns the call. A model may transcribe, suggest, or speak only inside the path that system already recorded and routed.",
    [
        P("Bring-your-own-carrier and SIP trunking are decisions on the voice platform: who provides numbers, who handles signaling, and who carries media. This AI course does not design your dial plan. The UC, Webex, Connect, and SIP labs are the places for that craft."),
        H("What the model is allowed to touch"),
        UL([
            "A transcript, after the voice platform has the audio.",
            "A suggested reply a person can send, or a spoken reply the platform plays.",
            "A retrieval over notes you are allowed to store.",
            "A transfer back to a person, requested through the platform's tool, not by the model inventing a route.",
        ]),
        H("Sister systems"),
        TB(
            ["System", "Job", "AI course limit"],
            [
                ["SIP trunk / PSTN / BYOC", "Numbers and the carrier path", "Name the owner. Do not invent trunk groups here."],
                ["Recording and quality management", "What was said, and how it is scored", "Consent and retention are policy. Thresholds are product facts to read on that vendor's page."],
                ["Workforce management", "Forecast and schedule", "A model does not replace the forecast. Specific vendor windows in the contact-center rooms were not re-fetched on 2026-10-15."],
                ["E911 / emergency", "A telephony duty", "An assistant must not be the only path to emergency services. This course does not certify a deployment."],
            ],
        ),
        WN("Emergency calls", "If a caller needs emergency help, the voice platform's emergency path is the path. Do not send that turn to a model and hope."),
        CK("Who owns an emergency call?", "The voice platform's emergency path. The model is not that path."),
    ],
))

add(lesson(
    "EX-08", "EX", "practice", 14,
    "CRM, analytics, and API bridges",
    "Integrate by writing a ticket id, a retrieval id, and a tool result into the system of record. Do not paste a customer logo and call it a partnership.",
    [
        P("This campus claims no customer deployment. A real integration is a pattern you can test: the CRM already has the case, the assistant reads fields it is allowed to read, and it writes back only through a tool a person approved."),
        H("Pattern"),
        OL([
            "The system of record creates the id. The model does not invent the case number.",
            "The tool schema lists the fields. Extra fields are a bug.",
            "Analytics count tasks, refusals, handoffs, latency, and cost. A vanity 'containment' number without a definition is not a metric.",
            "Webhooks retry. The handler is idempotent.",
            "Cross-platform bridges (a contact desktop, a CRM, a chat channel) share the trace id. They do not share a single vendor's admin model.",
        ]),
        NT("No customer story", "No logo, no seat count, and no 'we did this for a bank' claim belongs in this course. If you have a deployment, the proof is your own trace, under your employer's rules."),
        CK("Who creates the case id?", "The system of record. The model reads it. It does not mint it."),
    ],
))

add(lesson(
    "EX-09", "EX", "advanced", 12,
    "AI agents beside a human queue",
    "An agent is a loop with a schema, a step cap, and a trace. In a contact center it sits beside the queue. It does not become the queue.",
    [
        P("The agents track teaches the loop. This page is the boundary: the queue still has an arrival, a wait, and a person. The bot may greet, retrieve, and draft. Transfer is a tool the platform runs."),
        UL([
            "Write the done-check before the loop starts.",
            "Cap the steps. A loop that will not stop is a bill.",
            "Ask before send, pay, delete, or a change to the customer's record.",
            "Put the handoff in the trace: why the person got the turn, and what the person received.",
        ]),
        CK("What does the queue still own?", "Arrival, wait, and the person. The agent loop does not replace that ownership."),
    ],
))

add(lesson(
    "EX-10", "EX", "advanced", 14,
    "Security, compliance, and the limits of this course",
    "Write the data you will store, the tools you will allow, and the actions that always need a person. This course is not a certification and not legal advice.",
    [
        P("Useful public anchors, which you should read yourself: the NIST AI Risk Management Framework (airc.nist.gov), the OWASP GenAI security project (genai.owasp.org), and the privacy law that actually applies to your users. Naming them is not compliance."),
        UL([
            "Treat retrieved text as untrusted. It can carry instructions.",
            "A debug log is a database. Retention is a decision.",
            "Card data, health data, and children's data need the regime that governs them. Do not guess the scope from a blog.",
            "A jailbreak story in a lesson is not permission to build the attack.",
        ]),
        WN("Not a certification", "Nothing in this campus makes you certified, and nothing here is a finding about your employer."),
        CK("Is this course legal advice or a certificate?", "No. It is a study text. The regime that applies to your users is a document you read, not a paragraph you memorize here."),
    ],
))

add(lesson(
    "EX-11", "EX", "core", 12,
    "Licensing, certification, and a career path",
    "This course issues no certificate. Vendor exams change. The portfolio that matters is a trace, a task set, and a written gate.",
    [
        P("Model weights and vendor docs keep their own licenses. The code in this repository is under the MIT file at the repo root. The footer states a content license the mission brief asked for. Those two statements are both visible; do not assume they have been reconciled by a lawyer."),
        H("A path you can show"),
        OL([
            "Fundamentals: explain a token, a window, and a sample without a product name.",
            "Build: a grounded assistant on notes you may use, with one read-only tool.",
            "Prove: ten tasks, a retrieval score, a safety count, latency, and cost.",
            "Interview: the drills in the interview track. Say the mechanism, the control, and the evidence.",
            "Optional: a vendor exam, read from that vendor's current page. This course will not guess the passing score.",
        ]),
        CK("What should you show instead of a certificate from this site?", "A trace, a versioned task set, and a gate you can defend."),
    ],
))

add(lesson(
    "EX-12", "EX", "core", 10,
    "Roadmap and what was not re-checked",
    "Study the mechanisms. Treat dated product claims as a snapshot unless you open the page.",
    [
        P("What is stable enough to learn: next-token prediction, retrieval then generation, tool schemas, eval gates, and the habit of pinning ids. Papers this campus already cites: Vaswani et al. 2017, Lewis et al. 2020, Hu et al. 2021."),
        P("What was not re-fetched on 2026-10-15: vendor model lists quoted in the 2026-10-14 rooms, contact-center product steps, prices, context-window numbers, and certification catalogs. Each of those rooms carries a note. If a sentence has no note and no link, do not treat it as a fresh fact."),
        UL([
            "Future hook: a new model id is a config change plus a rescore, not a new course.",
            "Future hook: a new channel (voice, chat, desktop) reuses the trace id and the same gate.",
            "Future hook: a sister lab (UC, Webex, Connect, SIP) owns the telephony. Link to it. Do not copy it into this course.",
        ]),
        CK("What do you do when a model id in a lesson looks stale?", "Open the cited page, pin the id you actually call, and rescore the same tasks."),
    ],
))
