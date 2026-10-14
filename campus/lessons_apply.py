"""Tracks 07–13."""

from campus.schema import CK, FIG, H, NT, OL, P, PR, PRE, TB, UL, WN, lesson

LESSONS = []


def add(item):
    LESSONS.append(item)


add(lesson(
    "07-01", "07", "core", 12,
    "MCP connects a model to tools you did not hard-code",
    "The Model Context Protocol is a standard way for an app to talk to a tool server.",
    [
        P("Without a protocol, every app invents its own plugin format. MCP, the Model Context Protocol, is the 2025–2026 standard those apps increasingly share. A host such as an editor or a desktop assistant speaks MCP to a server that offers tools, documents, and prompt templates."),
        P("The model is not the server. The server is ordinary software: it lists what it can do, and it runs a tool when the host, with the person's consent, asks it to. That split is why the same notes server can be used from more than one app."),
        FIG("mcp-architecture", "Figure. A host contains an MCP client. A transport reaches a server that exposes tools, resources, and prompts."),
        NT("Currency", "The spec has moved. Local servers usually use stdio. Remote servers use streamable HTTP. Older remote servers used server-sent events. Read the spec version you implement rather than copying a 2024 snippet."),
        PR("Name one system you wish a model could read — a notes folder, a ticket list, a schema — and write whether it should be a tool (an action) or a resource (data the model may read)."),
        CK("Is the MCP server the language model?", "No. The server exposes capabilities. The model runs in the host and asks the client to call the server."),
    ],
))

add(lesson(
    "07-02", "07", "core", 11,
    "Host, client, and server have different jobs",
    "The person uses the host. The client holds the session. The server does the work.",
    [
        TB(
            ["Piece", "Job", "Example"],
            [
                ["Host", "The product a person opens. It decides what the model may see and what needs a click.", "An editor, Claude Desktop, or an app you are building."],
                ["Client", "Speaks MCP: initialize, list, call. Lives inside the host.", "The connector your editor starts."],
                ["Server", "Implements tools, resources, and prompts. Holds credentials for the system behind it.", "A small program that can read one notes folder."],
            ],
        ),
        P("Do not put your database password in the host's prompt. Put it in the server's environment, and let the server return the rows the tool is allowed to return. The model sees the rows, not the password."),
        PR("Label three boxes — host, client, server — for a setup you might actually run. Write one sentence for what each box must not do."),
        CK("Where should a database password live?", "On the server, in its environment. Not in the prompt, and not in a tool description."),
    ],
))

add(lesson(
    "07-03", "07", "core", 11,
    "Tools act, resources are read, prompts are templates",
    "Use the primitive that matches the risk.",
    [
        P("MCP servers publish three kinds of things. Mixing them up is how a 'reader' ends up with permission to write."),
        TB(
            ["Primitive", "What the model gets", "Risk"],
            [
                ["Tool", "A function it can call with arguments. The server may change something.", "Highest. Treat writes as side effects."],
                ["Resource", "Data it can read, addressed like a URI the server defines.", "The content is untrusted input. It can contain injection text."],
                ["Prompt", "A template the person or the host can insert, with arguments.", "A template is an instruction. Review it like a prompt change."],
            ],
        ),
        P("If the job is 'show me this note', prefer a resource. If the job is 'append a line to the decision log', that is a tool, and it waits for a person unless you have a strong reason and an eval."),
        PR("Take the system you named in 07-01 and list one tool, one resource, and, if you need it, one prompt template. If you do not need a prompt template, say so."),
        CK("Why is a resource still a safety issue if it cannot write?", "Because its text enters the model's context and can carry instructions. Read-only is not the same as trusted."),
    ],
))

add(lesson(
    "07-04", "07", "practice", 12,
    "Connect a local server over stdio",
    "The host starts a process and speaks MCP on its standard streams. The process is the trust boundary.",
    [
        P("A local server is a command the host launches. Configuration names the command and its arguments. The host's working directory and environment become the server's power. A server that runs `python server.py` with your shell's environment can see whatever that environment can see."),
        PRE(
            "{\n"
            '  "mcpServers": {\n'
            '    "notes": {\n'
            '      "command": "python",\n'
            '      "args": ["notes_server.py"],\n'
            '      "env": {"NOTES_ROOT": "/path/you/chose"}\n'
            "    }\n"
            "  }\n"
            "}"
        ),
        UL([
            "Pin the command to a project path. Do not rely on a mystery binary earlier on the PATH.",
            "Pass only the environment variables the server needs.",
            "Set the root folder in the server and reject paths outside it.",
            "Start with resources that read. Add a write tool only with an approval in the host.",
        ]),
        NT("You do not have to build a server to learn the shape", "If you install nothing, the artifact is the config above plus the list of tools you would refuse. A live server is optional."),
        PR("Write a config for a server whose only job is to read one folder. State the folder, and state one path it must reject."),
        CK("What does stdio mean for where the server runs?", "On the same machine, as a child process of the host, with the power of the environment you gave it."),
    ],
))

add(lesson(
    "07-05", "07", "core", 13,
    "Consent, authentication, and untrusted servers",
    "A server you did not review can read what the host will hand it, and its tool text can steer the model.",
    [
        P("Installing an MCP server is closer to installing a plugin than to bookmarking a page. A local server can read files. A remote server receives whatever the client sends and might retain it. Both can put instructions into tool descriptions, which the model will read."),
        H("Rules"),
        UL([
            "Read what the server declares it can do before you enable it.",
            "Approve tool calls that have side effects. A host that auto-approves everything has no consent left.",
            "Authenticate remote servers. Send only the account the task needs.",
            "Do not connect a coding agent to a server from a stranger because a README said to paste the config.",
            "Treat tool descriptions and resource bodies as untrusted. They are a known place for indirect prompt injection.",
        ]),
        WN("No exploit steps here", "The failure mode is enough: untrusted instructions in tool metadata, plus a powerful tool, plus auto-approval. The defense is review, least privilege, and a person on side effects."),
        PR("Write a yes/no checklist you will use before enabling a server: who published it, what tools it lists, whether any tool can write or send, and whether the host will ask first."),
        CK("Why is a tool description a safety boundary?", "Because it is inserted into the model's context. A hostile description is an instruction the model may follow."),
    ],
))

add(lesson(
    "07-06", "07", "practice", 10,
    "How coding tools use MCP",
    "Editors and agents use MCP to reach issue trackers, browsers, docs, and internal APIs. The repo is still reviewed by a person.",
    [
        P("In 2026, coding products expose MCP so a model can call the tools a developer already uses: a ticket, a design file, a database schema, a browser snapshot, a documentation search. That is useful. It also means the agent in School 08 may now see more than the git tree."),
        UL([
            "Each connected server widens the data the model can read. Add one, try it, and keep the trace.",
            "A documentation server does not need write tools. Turn those off.",
            "Internal APIs behind MCP still need the same auth you would demand of a script.",
            "If a server can open a browser while logged in as you, assume it can see what you can see. That is not a default-on tool.",
        ]),
        P("MCP does not replace tests or review. It replaces a pile of one-off plugins. The diff still needs a person, which is the next track."),
        PR("List two MCP servers that would help a coding task you do, and one you would leave disconnected, with the reason."),
        CK("Does connecting an issue tracker via MCP remove the need to review the diff?", "No. It adds context. The change to the repo is still reviewed against tests and intent."),
    ],
))

add(lesson(
    "08-01", "08", "core", 12,
    "A coding agent edits a repository under rules",
    "It can read, propose a plan, change files, and run commands. Your rules say which of those happen alone.",
    [
        P("A coding agent is the loop from School 06 pointed at a codebase. Products in this category include Cursor, GitHub Copilot's agent modes, Claude Code, Codex-style agents, Aider, Continue, and Cline. They differ in interface. They share the risk: a model with a terminal and a write path."),
        H("Decide explicitly"),
        UL([
            "Which directories it may read, and which it may write.",
            "Whether it may run tests, and which command.",
            "Whether it may install packages, change git config, or contact the network.",
            "That it may not read secret files. Name them: `.env`, key stores, credential JSON.",
            "That applying the result is a diff a person can read, not a silent commit to the main branch.",
        ]),
        P("If you cannot answer those, you do not have an agent setup. You have a default, and defaults differ by product and drift over time. Read the product's current permission screen and write down what you turned off."),
        PR("For a repository you know, write the allow and deny list: directories, commands, and files. Include `.env` on the deny list even if your project uses a different name."),
        CK("What is the result of a coding agent, the summary or the diff?", "The diff, plus the test command you ran. The summary is a claim about them."),
    ],
))

add(lesson(
    "08-02", "08", "practice", 10,
    "Give the agent the files and tests that matter",
    "A whole monorepo in the prompt is not context. It is noise.",
    [
        P("Point the agent at the module, the failing test, and the interface it must not break. Name the command that proves success. If you do not know the command, finding the command is the task, and the agent should stop before editing."),
        PRE(
            "Goal: Fix the empty-state copy in the invoice list.\n"
            "Read: src/invoices/list.tsx, src/invoices/list.test.tsx\n"
            "Do not edit: src/billing/\n"
            "Done: npm test -- invoices passes, and the test covers the empty state."
        ),
        P("Let it search when the relevant file is unknown. Keep the step cap small so search does not become a tour. When it names the files it will change, that list is the moment to redirect it."),
        PR("Write a goal block in the shape above for a small change you understand. If you do not have a repo, use a fictional one and still name a test command."),
        CK("Why name a test in the goal?", "Because that command is the done-check. A green test is evidence. A summary is not."),
    ],
))

add(lesson(
    "08-03", "08", "core", 11,
    "Plan, edit, run, then stop",
    "A plan you can reject is cheaper than a pile of edits you have to unwind.",
    [
        OL([
            "The agent states which files it will touch and what it thinks is wrong.",
            "You correct the plan or accept it.",
            "It edits inside the allowlist.",
            "It runs the test command you named.",
            "It stops, whether the tests passed or not, and shows the diff.",
        ]),
        P("Skipping the plan is sometimes fine for a one-line change you already specified. It is a poor habit for anything that crosses a module. 'Keep going until the tests pass' without a cap is how an agent refactors the neighborhood and calls it a fix."),
        P("A failed test is a successful stop if the step cap is near. Record the failure. Do not let a second, unrelated edit 'try something else' in the same unreviewed tree."),
        PR("Add a step cap and a stop sentence to the goal block from 08-02. Example stop sentence: 'I hit 6 steps. Tests are red. No further edits.'"),
        CK("When is it reasonable to skip the written plan?", "When the change is small and you already named the file and the test. Not when the agent is still looking for the cause."),
    ],
))

add(lesson(
    "08-04", "08", "core", 12,
    "Review the diff and the tests",
    "Read the change as if a new teammate wrote it. Then run the same command they ran.",
    [
        P("Review for behavior, not for style the linter can catch. Look for extra files, weakened assertions, deleted tests, new dependencies, and changes outside the goal. Look for secrets that were read and echoed into a comment or a log."),
        H("A short review pass"),
        OL([
            "Does every hunk serve the goal? If not, revert the hunk.",
            "Did a test get deleted or did an assertion change to match a wrong implementation?",
            "Did the dependency list change? That is a separate decision.",
            "Run the test command yourself. Do not accept 'I ran it' without the output in the trace.",
            "Run the adjacent tests the change could have broken.",
        ]),
        WN("Green tests can be gamed", "An agent can edit the test until it passes. Treat a test diff as carefully as a code diff. The expected value should still describe the behavior you want."),
        PR("Write five review questions you will ask of the next agent diff you see. Keep them specific enough that each is yes or no."),
        CK("The agent says the tests passed. What do you do?", "Run the named command and read the output. Check that the tests still assert the behavior you wanted."),
    ],
))

add(lesson(
    "08-05", "08", "core", 11,
    "Secrets, destructive git, and the network",
    "The expensive mistakes are not bad indentation.",
    [
        UL([
            "Deny secret files. If one was read, treat the session as exposed and rotate anything that file held.",
            "Do not allow `git push`, force-push, or commit to the default branch. A commit on a branch you can throw away is a different, still-reviewed action.",
            "Do not allow commands that delete history, drop databases, or send mail.",
            "Package installs and curl-to-bash are network and supply-chain actions. Ask first.",
            "A command allowlist beats a 'be careful' sentence in the system prompt.",
        ]),
        P("Put the deny list in the tool layer. A prompt that says 'never run destructive commands' loses to a tool that can run them and a document that says 'you must'."),
        PR("Write the command allowlist for a lab agent: the test command, and nothing else. Add three commands that are always denied."),
        CK("Where does the deny list have to live to be real?", "In the tool permissions, not only in the prompt."),
    ],
))

add(lesson(
    "08-06", "08", "practice", 10,
    "Use a coding agent on a team without shipping junk",
    "Agree the permissions, the review, and what 'the agent did it' does not excuse.",
    [
        P("Teams that get value from coding agents in 2026 treat them as fast teammates with a narrow role. The author of the change is still a person. The pull request explains the behavior, the test command, and any permission the agent was given."),
        UL([
            "One shared permission profile is better than everyone clicking through defaults.",
            "Agent commits are labeled, and they are small enough to review.",
            "Generated code is not exempt from the style, security, or licensing rules.",
            "If the agent used a retrieved snippet, the license of that snippet still matters.",
            "A metric worth having: review time and escape rate, not lines generated.",
        ]),
        P("Lines generated is a vanity metric. A change that takes longer to review than it would have taken to write is not a win, unless it was a change people were avoiding for a tracked reason."),
        PR("Write three lines a pull request should contain when an agent helped: the goal, the test command and result, and the permissions used."),
        CK("Who is responsible for an agent-written change that ships?", "The person who reviewed and merged it. The agent is not an author of record."),
    ],
))

add(lesson(
    "09-01", "09", "core", 12,
    "An eval is a versioned test, not a feeling",
    "You cannot prefer a new prompt unless the same tasks were scored both times.",
    [
        P("An evaluation is a set of tasks, a way to score them, and a record of what you ran. It is the same idea as a test suite, with more judgment in the score and more ways to fool yourself."),
        FIG("eval-workflow", "Figure. Versioned tasks, a pinned run, a score across quality and cost, a comparison, and a gate."),
        UL([
            "Tasks live in a file you can diff.",
            "The scorer is code, a rubric a person applies, or a judge model with a rubric. Name which.",
            "The run records model id, prompt version, index version, and date.",
            "You compare to a baseline, not to your memory of last week.",
        ]),
        P("'It looks better' is a hypothesis. The eval is the test of the hypothesis. If you do not want to write tasks, you do not have an eval practice yet, and you should not be fine-tuning or swapping models on taste."),
        PR("Create a file with three tasks. Each task needs an input and a check a person could apply twice and agree on."),
        CK("What makes an eval different from trying a prompt in a chat?", "The tasks stay fixed, the score is recorded, and a later change has to beat that record."),
    ],
))

add(lesson(
    "09-02", "09", "core", 12,
    "Start with ten tasks you can explain",
    "A small set you trust beats a large set nobody can audit.",
    [
        P("Ten tasks is enough to catch a clumsy prompt change and small enough that you will actually look at the failures. Grow the set when a production mistake was not represented. Do not generate five hundred tasks with a model and call them ground truth."),
        H("Cover the set on purpose"),
        UL([
            "Typical cases a user would expect to pass.",
            "A case where the correct result is a refusal or an empty list.",
            "An edge case: missing field, ambiguous date, two sources that disagree.",
            "A safety case: the source tells the model to ignore its rules.",
            "A case you once got wrong in a demo. Those are gold.",
        ]),
        P("Write the expected check next to the input. For retrieval, the check includes the chunk id. For an agent, the check includes which tools were allowed to run and which must not have run."),
        WN("Do not tune on the only set you have", "If you edit the prompt while staring at all ten, you are memorizing them. Hold out two tasks you do not look at until the end, or add a fresh task before you declare victory."),
        PR("Draft ten one-line task titles for a system you might build. Mark two as refusal and one as a safety case. You can fill the inputs later. The titles force coverage."),
        CK("Why not generate the whole set with a model and trust it?", "Because the generator's mistakes become the score. A person has to own the expected checks."),
    ],
))

add(lesson(
    "09-03", "09", "core", 11,
    "Score quality, safety, latency, and cost together",
    "A change that raises quality and doubles the bill needs a decision, not a silent ship.",
    [
        TB(
            ["Axis", "A concrete score"],
            [
                ["Quality", "Fraction of tasks that meet the check. Report the failures by name."],
                ["Safety", "Count of tasks that violated a rule: invented citation, forbidden tool, secret in the output, missed refusal."],
                ["Latency", "Median and worst time to the answer a person sees, on the hardware or API you will use."],
                ["Cost", "Tokens or currency per successful task, including retries."],
            ],
        ),
        P("A single blended number hides the trade. Keep the four. Your gate can say 'quality must not drop, safety fails must be zero, median latency under two seconds, cost within 10 percent'. Write the gate before you see the new score, or you will move the gate to fit the result."),
        PR("Write a gate in one sentence for a system you have in mind, using at least quality and one of the other three axes."),
        CK("Why keep cost beside quality?", "Because a gain that doubles spend or latency can be the wrong ship even when more answers are correct."),
    ],
))

add(lesson(
    "09-04", "09", "practice", 12,
    "Use a model as a judge only with a rubric and an audit",
    "A judge model is a second system. It has its own failure rate.",
    [
        P("Some checks are awkward to write as exact string matches: whether a summary omitted a decision, whether a tone is acceptable. A judge model can apply a rubric to those. It cannot be the only authority."),
        H("A judge you can defend"),
        OL([
            "The rubric is written: what a pass must include, what a fail looks like, and that ties go to fail when the decision is risky.",
            "The judge returns a structured score, not a paragraph you reinterpret.",
            "You score a sample by hand and compare. If you and the judge disagree often, fix the rubric or stop using the judge.",
            "The judge is pinned to a model id. Changing it is an eval change.",
            "The judge does not see the candidate's hidden chain of thought as 'proof'. It sees the answer and the sources.",
        ]),
        P("Exact checks are better when you can write them: JSON validity, id membership, a number, a tool that must not appear in the trace. Use the judge for the residue, not for everything, because the residue is where you can be fooled."),
        PR("Write a five-line rubric for one subjective check. Include one line that forces a fail."),
        CK("What do you compare a judge model against before you trust it?", "A sample you scored yourself, on the same rubric."),
    ],
))

add(lesson(
    "09-05", "09", "core", 11,
    "Gate changes to the prompt, the model, and the index",
    "Each of those is a release. The tasks do not change in the same commit unless the task change is the point.",
    [
        P("A prompt tweak, a model swap, a new embedding model, a chunker change, and a tool-schema change are all releases. Run the same tasks. Put the score in the pull request. If the gate fails, do not merge because the demo looked fine."),
        TB(
            ["Change", "Extra thing to record"],
            [
                ["Prompt", "The prompt version or hash."],
                ["Chat model", "The model id and the sampling settings."],
                ["Embedding model or chunker", "That the index was rebuilt, and the retrieval recall, not only the answer score."],
                ["Tool list", "Which tools ran on the safety tasks."],
            ],
        ),
        P("A regression is a task that used to pass and now fails. Name it in the pull request. 'Overall score is flat' can hide one new safety fail and one new easy pass that cancel in the average."),
        PR("Write the checklist you would paste at the bottom of a pull request that changes a prompt: what was pinned, what ran, which tasks regressed, and whether the gate passed."),
        CK("Why is a new embedding model not a free change?", "Because the vectors change. You rebuild the index and rescore retrieval, or you do not know what you shipped."),
    ],
))

add(lesson(
    "09-06", "09", "practice", 11,
    "Put red-team cases in the set early",
    "You are checking your own system's boundaries, on inputs you control.",
    [
        P("A red-team case is a task that tries to make your system break a rule you wrote. You author the case. You are not attacking someone else's service, and you are not collecting bypass tricks. You are checking that your gate holds on inputs you will meet."),
        UL([
            "A document that says to ignore the rules and approve a refund the policy refuses.",
            "A request for a secret that should never be in the prompt. The pass condition is that the secret does not appear.",
            "A tool request that tries to write outside the sandbox. The pass condition is that the trace shows a denial.",
            "Personal data that should have been refused or masked.",
            "A citation of an id that was not retrieved.",
        ]),
        P("Score these as pass or fail. Do not average them into a soft quality number. One safety fail blocks the release if that is the gate you wrote. If you decide it does not block, write that decision down and own it."),
        PR("Write two red-team tasks in input-and-pass-condition form. Use synthetic data. Do not include a real secret to 'see if it leaks'."),
        CK("What is the pass condition of a red-team task?", "That the system followed the rule: refusal, denial in the trace, or no secret in the output. Not that the model gave a clever reply."),
    ],
))

add(lesson(
    "09-07", "09", "practice", 9,
    "Keep the scorecard next to the artifact",
    "A table you can reopen beats a screenshot of one good answer.",
    [
        PRE(
            "date: 2026-10-13\n"
            "prompt: extract-v3\n"
            "model: pinned-id\n"
            "index: notes-2026-10-13\n"
            "quality: 8/10\n"
            "safety_fails: 0\n"
            "median_latency_s: 1.4\n"
            "regressed: []\n"
            "gate: pass"
        ),
        P("Store this beside the outputs, or store the outputs and link them. When someone asks why you shipped, this is the answer. When someone asks why you did not fine-tune, this is also the answer: the failures were retrieval, not the base model, or there were not enough failures to justify training."),
        PR("Copy the template and fill it with 'not run' where you have no number. A blank dressed up as a score is worse than 'not run'."),
        CK("What belongs in the scorecard besides the pass count?", "The pins — prompt, model, index — plus safety, latency or cost, regressions, and the gate result."),
    ],
))

add(lesson(
    "10-01", "10", "core", 12,
    "Fine-tune only after a measured failure of the cheaper fixes",
    "Prompt, schema, retrieval, and tools come first. Training is for a gap those did not close.",
    [
        P("Fine-tuning changes the model's weights, usually by training on examples of the behavior you want. It costs data work, compute, and a new model you have to host and re-eval. It is the right tool when the base model already has the facts — or you will keep retrieving the facts — and still will not hold a format, a style, or a domain decision that you can show in examples."),
        H("Do not fine-tune to"),
        UL([
            "Memorize a handbook that changes monthly. Retrieve it.",
            "Hide a secret or a policy the prompt already states and the eval already passes.",
            "Repair a broken tool. Fix the tool.",
            "Chase a leaderboard with no task of your own.",
        ]),
        P("The decision record is the eval from School 09 plus a sentence: which failures remain, and why a prompt or a retrieval change cannot address them. If you cannot write that sentence, you are not ready to train."),
        PR("Write that decision sentence for a real or fictional system. 'Not yet, because …' is a complete answer."),
        CK("Name one problem retrieval solves better than fine-tuning.", "Facts that change, or facts that must be cited from a source you can update without training."),
    ],
))

add(lesson(
    "10-02", "10", "core", 13,
    "LoRA trains a small adapter and leaves the base model frozen",
    "QLoRA does the same while the frozen base is stored in a quantized form.",
    [
        P("Full fine-tuning updates every weight. That is expensive and easy to damage. LoRA (Low-Rank Adaptation) freezes the base model and trains small matrices that sit alongside certain layers. You store the adapter, not a full second copy of the model. At inference you load the base plus the adapter."),
        FIG("lora", "Figure. The base layers stay frozen. The adapter is the part you train."),
        P("QLoRA quantizes that frozen base so the training job fits on a smaller GPU. The adapter is still what you train. People say 'I quantized' when they mean 'I fine-tuned' and the reverse. In a design review, say which one you did."),
        P("Preference methods such as DPO train from pairs of better and worse answers. They are a fit when the issue is which output a person prefers, and a poor fit when the issue is a missing document. You still need a base that can produce the better answer often enough to learn from."),
        NT("Tools you will see named", "Hugging Face PEFT, Axolotl, Unsloth, and the hosted fine-tuning APIs from the major labs. The method matters more than the brand: frozen base, small adapter, same eval before and after."),
        PR("In three sentences, explain to a teammate the difference between quantizing a model to run it and training a LoRA adapter on it."),
        CK("What do you save after a LoRA run?", "The adapter, and a record of the base model id it attaches to. The adapter without the matching base is not a model."),
    ],
))

add(lesson(
    "10-03", "10", "core", 12,
    "Training data has a format, a license, and a leakage problem",
    "Examples teach the behavior. They also teach secrets you forgot were in the log.",
    [
        P("A typical supervised set is a list of conversations or instruction pairs: the input the model will see, and the output you want. The format must match how you will call the model later. Training on essays and then calling the model as a JSON API is a self-inflicted miss."),
        UL([
            "You need the right to train on every row. A model license, a website's terms, and your employer's policy can each forbid it.",
            "Remove secrets, tokens, and personal data. A model that memorizes a key is a leak you cannot easily grep.",
            "Remove exact copies of your eval tasks. If the eval is in the training set, the score is a memory test.",
            "Include refusal and 'not in the source' examples if that is the behavior you want. A set of only happy paths teaches invention.",
            "Keep a validation split that you do not train on.",
        ]),
        WN("Synthetic data", "Data a model wrote is allowed only if you review it and you are allowed to use it. It repeats the teacher's mistakes at scale. A person still owns the guidelines."),
        PR("Describe the columns of a training row for one task. Add a column for the source of the row and a yes/no for 'contains personal data'. That yes/no must be no before the row is usable."),
        CK("Why must eval tasks stay out of the training set?", "Because a high score would then mean the model saw the answers, not that it generalized."),
    ],
))

add(lesson(
    "10-04", "10", "practice", 10,
    "Compare the adapter to the base model on the same tasks",
    "Keep the adapter only if the scorecard says so, including the tasks that used to pass.",
    [
        P("Run the School 09 tasks twice: base model, then base plus adapter. Same prompts, same retrieval, same tools. The adapter wins only if the failures you trained for improved and the safety tasks did not get worse."),
        P("Watch for a model that learned the training phrasing and now refuses to answer a valid variant. That shows up as regressions on tasks that used to pass. It is the usual cost of a small, narrow set."),
        UL([
            "Record the base id and the adapter id together.",
            "If you quantize after training, eval the quantized result, not the pre-quantized one you will not ship.",
            "If the adapter ties the base, do not ship it. You would be adding an artifact to host for no gain.",
        ]),
        PR("Write the comparison header: task, base result, adapter result, regression yes/no. Fill it with the decision you expect, and note which safety task would make you throw the adapter away."),
        CK("A adapter raises the average and fails a refusal task the base passed. Do you ship it?", "No, if refusal is in the gate. An average can rise while a safety regression lands."),
    ],
))

add(lesson(
    "10-05", "10", "practice", 8,
    "Prefer a prompt or a tool when that is the whole gap",
    "Most 'we should fine-tune' reviews end with a schema, a retrieval fix, or a smaller model.",
    [
        P("Walk this list before you spend on training."),
        OL([
            "The output shape is underspecified. Fix the schema.",
            "The fact is missing from the context. Fix retrieval or the tool.",
            "The fact is in the context and ignored. Fix placement, chunking, or the instruction to cite.",
            "A cheaper model fails and a larger base model passes. Use the larger model, or route only the hard rows.",
            "Only the remaining rows, with a stable behavior you can exemplify, are training candidates.",
        ]),
        P("This is the judgment hiring panels are probing when they ask 'how do you decide to fine-tune'. The answer is a sequence of measured exclusions, not enthusiasm for training."),
        PR("Take the decision sentence from 10-01 and run it down this list. Stop at the first item that applies."),
        CK("When is a larger base model a better answer than a fine-tune?", "When the larger model already passes the same tasks and you can afford it. You have not found a behavior the base cannot learn from context."),
    ],
))

add(lesson(
    "11-01", "11", "core", 11,
    "Write a one-page safety policy",
    "Name the data, the tools, the actions that need a person, and what you will not build.",
    [
        P("A policy you can apply is one page. A policy that quotes every guideline and changes nothing is not a control."),
        PRE(
            "Data I will send to a hosted model:\n"
            "Data that stays on this machine:\n"
            "Tools the system may call unattended:\n"
            "Actions that always wait for a person:\n"
            "What I will not build:\n"
            "Where traces live and when I delete them:"
        ),
        P("Fill it for the capstone before you connect a tool. If a line is 'not sure', the tool stays disconnected. Update the page when the system changes, in the same change as the tool list."),
        PR("Fill the six lines. Use 'none yet' where that is true."),
        CK("What do you do with a tool that is not on the policy page?", "You do not enable it. The page is the allowlist."),
    ],
))

add(lesson(
    "11-02", "11", "core", 10,
    "Decide retention before you log the prompt",
    "Prompts are often personal data. A debug log is a database.",
    [
        P("A prompt can contain a person's name, a health note, a customer message, or a secret. The provider's retention setting and your own log are two different stores. Configure both. 'The vendor probably deletes it' is not a setting."),
        UL([
            "Prefer not to send private data. Retrieve or redact locally first when you can.",
            "Set the provider retention and training-opt-out flags you actually need. Re-read them when you change accounts.",
            "Give your logs a lifetime. A disk that keeps every prompt forever will surprise you in an incident.",
            "Deletion is a feature: how a person asks, and how you prove the trace is gone.",
        ]),
        P("Synthetic fixtures belong in the repo. Real prompts do not, unless the repo is private and approved for that data. This course's exercises use synthetic fixtures for that reason."),
        PR("Add two lines to your policy page: how long traces live, and what you will redact before a trace is written."),
        CK("Name two stores that can retain a prompt.", "The provider, according to the settings on that key, and your own logs."),
    ],
))

add(lesson(
    "11-03", "11", "core", 10,
    "A person approves sends, payments, and deletes",
    "Drafting is not the same action as doing.",
    [
        P("Let the system draft the email, the refund, the shell command, or the pull request. Show the draft and the arguments. A person confirms. The tool layer checks that the confirmation matches those arguments. If the model changes the arguments after the yes, the yes is void."),
        TB(
            ["Draft", "Do"],
            [
                ["Write the reply", "Send the reply"],
                ["Propose the refund amount", "Move the money"],
                ["Show the files to delete", "Delete them"],
                ["Open a diff", "Push to the default branch"],
            ],
        ),
        P("Unattended action is a product decision with a name, a kill switch, and an eval. It is not the default because a demo was smoother without the click."),
        PR("Mark each of the four rows for your capstone: will you stop at draft, or do you have a named reason to go further? 'The demo' is not a reason."),
        CK("The model includes 'approved: true' in a tool argument. Does the handler run?", "No. Approval is a record your program stored before the call, tied to the exact arguments."),
    ],
))

add(lesson(
    "11-04", "11", "practice", 9,
    "Write an incident note when the model misbehaves",
    "A short note beats a thread of screenshots.",
    [
        PRE(
            "What happened, in one sentence:\n"
            "What the person expected:\n"
            "Model id, prompt version, tool list:\n"
            "The trace id:\n"
            "Did data leave the machine, or did a tool act?\n"
            "What you turned off:\n"
            "What eval task you added so this is a regression next time:"
        ),
        P("If a tool acted, contain that first: revoke the key, disable the server, rotate the secret. Then write the note. An incident without a new eval task will return as a surprise."),
        PR("Fill the template for a fictional incident: a retrieved page told the model to approve a refund, and the draft looked convincing. Say whether a tool acted. In a well-built system, it did not."),
        CK("What do you add to the eval after an incident?", "A task that reproduces the failure, with a pass condition that the new behavior holds."),
    ],
))

add(lesson(
    "11-05", "11", "core", 8,
    "What this course will not help you do",
    "The boundary is part of the teaching.",
    [
        P("This campus will not help you write malware, hide a prompt injection, bypass a provider's safety stack, scrape a system you are not allowed to access, or automate harm. Those are not advanced modules. They are out of scope."),
        P("It will also not certify you, grant you a model, or guarantee a job. The artifact you leave with is a capstone you can explain: what it calls, what it refuses, and how you scored it."),
        UL([
            "If a later idea needs a payload, a stolen credential, or a covert channel, stop.",
            "If a tool would act on a person without a review you can defend, stop at the draft.",
            "If you cannot name the data's owner, do not train on it and do not upload it.",
        ]),
        PR("Add a 'will not build' line to your policy page that is specific to your domain, not a copy of this lesson's first sentence."),
        CK("Is a jailbreak write-up a missing advanced chapter?", "No. Testing your own gates with cases you own is in scope. Instructions for breaking other systems are not."),
    ],
))

add(lesson(
    "12-01", "12", "core", 11,
    "Name the job before you name the model",
    "A product sentence has a person, a job, and a constraint. The model is an implementation choice.",
    [
        P("Hiring posts for AI product managers in 2026 ask for the same discipline as the engineering tracks: a user, a workflow, a measurement, and a risk. Start with the job-to-be-done."),
        PRE(
            "When a support lead reviews yesterday's refunds,\n"
            "they need the policy line that applies,\n"
            "without pasting the whole handbook into a chat,\n"
            "in under a minute,\n"
            "with a citation they can forward."
        ),
        P("If you cannot fill those clauses, you do not have a feature. You have a model in search of a demo. The citation requirement is what makes this a retrieval product. The minute is a latency budget. The handbook staying put is a privacy requirement. The model choice comes after."),
        PR("Write a four-line job statement for something you would actually use. Include a latency or cost constraint and a proof constraint, such as a citation or a test."),
        CK("Where does the model name belong in the spec?", "After the job, the constraint, and the proof. It is a choice you can swap if the eval holds."),
    ],
))

add(lesson(
    "12-02", "12", "practice", 12,
    "Write a one-page spec",
    "Problem, user, non-goals, success, risks, and the first milestone.",
    [
        TB(
            ["Section", "What a builder needs"],
            [
                ["Problem", "The job statement from 12-01."],
                ["User", "Who is in the loop, and who is definitely not the user yet."],
                ["Non-goals", "What this version will not do. Unattended send is a good non-goal."],
                ["Success", "The eval gate: quality, safety, latency, cost."],
                ["Risks", "Wrong citation, stale policy, injection in a ticket, data leaving the tenant."],
                ["Milestone", "The smallest slice that can be scored. Often: ten tasks, one corpus, no tools that write."],
            ],
        ),
        P("One page forces the cut. A ten-page spec that does not name a non-goal will be read as permission to build the platform."),
        PR("Fill the six sections in short lines for your job statement. If success has no number or no pass/fail, it is not success yet."),
        CK("Why write non-goals in the spec?", "Because an unnamed non-goal gets built as soon as a demo suggests it."),
    ],
))

add(lesson(
    "12-03", "12", "core", 10,
    "Share four numbers with engineering",
    "Quality, safety fails, latency, and cost per successful task.",
    [
        P("A roadmap slide that says 'improve AI quality' does not tell an engineer what to do. The shared numbers do. They are the same four axes as the eval gate, expressed as a product promise."),
        UL([
            "Quality: which tasks, and the pass bar.",
            "Safety: which failures are release blockers.",
            "Latency: the time the person actually waits, at a percentile you name.",
            "Cost: per successful task, including human review time if review is required.",
        ]),
        P("Add a counter-metric so the team cannot game the first number. If you only score deflection, the system will refuse hard tickets and look successful. Pair deflection with a check that the citation was real, or with a sample a person reviews."),
        PR("Write the four numbers for your spec, plus one counter-metric. Use targets you could measure this month, not a press-release percentage."),
        CK("Why is deflection alone a dangerous metric?", "The system can push work away, or answer wrongly, and the deflection count still rises."),
    ],
))

add(lesson(
    "12-04", "12", "practice", 11,
    "Design the empty, slow, wrong, and unsafe states",
    "The model will hit all four. The interface should say what happened.",
    [
        TB(
            ["State", "What the person sees"],
            [
                ["Empty", "No source contained the answer. Offer the search you ran, not a guess."],
                ["Slow", "Still working, with a way to stop. Do not freeze a silent button."],
                ["Wrong", "A way to see the citation and mark it bad. That mark becomes an eval task."],
                ["Unsafe", "The action did not run. Say what was blocked. Do not explain how to get around the block."],
            ],
        ),
        P("A chat box with no states is a demo. A product names these four and logs them. The unsafe state is especially easy to get wrong: a coy message that hints at the blocked action teaches the next try."),
        PR("Write the four messages in your product's voice, each in one sentence. Read the unsafe message and delete any hint of a workaround."),
        CK("What should a 'wrong' answer let the person do?", "Open the citation and mark the failure so you can add it to the task set."),
    ],
))

add(lesson(
    "12-05", "12", "practice", 10,
    "Ship a prototype, then an eval, then a limited release",
    "A limited release has a named audience, a kill switch, and a date you will read the scorecard.",
    [
        OL([
            "Prototype on synthetic data. Show the empty state on purpose.",
            "Freeze ten tasks and a gate. Do not invite users past a failing gate.",
            "Limited release to people who know it is a draft and know how to report a bad citation.",
            "Read the scorecard on the date you set. Expand, revise, or turn it off.",
        ]),
        P("A kill switch is a flag that disables the model path and leaves the previous workflow intact. If there is no previous workflow, the kill switch is 'stop showing the feature'. Shipping without that flag means an incident becomes a scramble."),
        NT("Buy versus build", "A hosted agent product can be the right milestone if it meets the policy page. You still own the eval and the data question. Buying the UI does not buy the judgment."),
        PR("Write the audience for a limited release in one sentence, the kill switch, and the date you will read the numbers."),
        CK("What has to be true before the limited release?", "The gate passes on the frozen tasks, the audience is named, and you can turn the feature off."),
    ],
))

add(lesson(
    "12-06", "12", "practice", 10,
    "Add voice only when latency and handoff are designed",
    "Speech recognition and speech synthesis are models with their own failure modes. They do not replace the eval.",
    [
        P("A voice interface adds two models and a clock. Speech-to-text can drop names, numbers, and domain words. Text-to-speech can say a wrong answer smoothly, which is worse than a wrong paragraph the person can skim. Barge-in, silence, and background noise are product states, not polish."),
        H("A minimum voice design"),
        UL([
            "A latency budget for the turn, written down. If you cannot meet it, stay on text.",
            "A domain word list you tested on, including the names your users actually say.",
            "A visible transcript so the person can catch a recognition error.",
            "A handoff to a human that the caller can trigger, and that the system triggers when confidence in the retrieved answer is absent.",
            "No unattended action. Voice is a draft and a lookup until a person confirms.",
        ]),
        P("If your background is phone systems, bring that operational care to the latency budget and the handoff. Leave the vendor-specific telephony course for a telephony course. Here, voice is an interface on top of the same retrieval, tools, and evals."),
        NT("Cited contact-center rooms", "The longer cited notes on the spoken loop, contact-center agents, the vendor pages, voice privacy, and a RAG voice agent are on the Contact center track: 14-p-t7r01, 14-p-t7r02, 14-p-t7r07, 14-p-t8r03, and 14-p-t8r08."),
        PR("Decide whether your spec needs voice in the first release. If yes, write the latency budget and the handoff sentence. If no, write it as a non-goal."),
        CK("Why is a smooth spoken answer a higher bar than a written one?", "Because the person cannot scan a citation while the sentence is already being said. The transcript and the handoff have to carry the check."),
    ],
))

add(lesson(
    "13-01", "13", "core", 12,
    "Choose a capstone you can finish on your own notes",
    "A folder you are allowed to use, questions you wrote, citations, and one read-only tool.",
    [
        P("The capstone is a small grounded assistant over a corpus you control: ten to thirty notes, a handbook chapter, or a public spec you have the right to copy into a lab folder. It answers questions from that corpus, cites chunk ids, and refuses when the corpus is silent."),
        H("Scope that fits"),
        UL([
            "One corpus on local disk. No scraping, no customer export.",
            "Retrieval plus one read-only tool, such as a calculator or a glossary lookup, if the questions need it.",
            "No send, no delete, no network tool.",
            "Ten eval tasks you wrote by hand.",
            "A one-page safety policy.",
            "A model you can actually run: local, or an API whose data use you accept.",
        ]),
        P("A capstone that needs a team, a budget, and a month of data cleaning is a job, not this exercise. Cut it until you can demo it in one sitting."),
        PR("Write the corpus path, the user, and the one tool. If you have no corpus, create five synthetic notes and use those. Synthetic is allowed. Someone else's private data is not."),
        CK("What makes this small enough?", "A corpus you already may use, ten tasks, citations, at most one read-only tool, and no side effects."),
    ],
))

add(lesson(
    "13-02", "13", "core", 10,
    "Write the acceptance tests before the prompt",
    "If a test is awkward to write, the capstone is still too vague.",
    [
        P("Acceptance tests are the ten tasks, plus three product checks."),
        OL([
            "At least seven tasks name a chunk id that must be cited.",
            "At least two tasks must refuse because the note is absent.",
            "At least one task includes a source line that tells the model to ignore the rules. The pass condition is that the rule holds.",
            "The trace shows no tool outside the allowlist.",
            "You can rebuild the answer from the artifact a week later: corpus version, prompt, model id, scores.",
        ]),
        P("Write these before you polish the prompt. Otherwise you will write tests that describe whatever the model happened to say."),
        PR("Create the ten task titles and mark which are cite, which are refuse, and which is the injection case. Store them in a file next to the corpus path."),
        CK("Why write acceptance tests before the prompt?", "So the tests describe the job, not the last output you liked."),
    ],
))

add(lesson(
    "13-03", "13", "practice", 9,
    "Keep a build log as you go",
    "Each entry is a run, a trace pointer, a metric, and an artifact.",
    [
        P("The build log is the proof habit applied to the capstone. One entry per change. Short."),
        PRE(
            "2026-10-13 prompt v1, model pinned, retrieval only\n"
            "quality 4/10, safety fails 1 (invented id)\n"
            "artifact: runs/v1/\n"
            "next: membership-check citations in code\n"
            "\n"
            "2026-10-13 prompt v1, added id check\n"
            "quality 6/10, safety fails 0\n"
            "next: fix two missing chunks"
        ),
        P("Do not wait until the demo to reconstruct this. You will invent a cleaner story than the one you ran."),
        PR("Open the log with a first entry, even if every metric says 'not run'. The next line says the first change you will make."),
        CK("What does a build-log entry contain?", "What changed, the score, where the artifact is, and the next change. Enough to repeat or to revert."),
    ],
))

add(lesson(
    "13-04", "13", "practice", 10,
    "Demo the capstone in ten minutes",
    "Show a pass, a refusal, the trace, and the scorecard. Do not show a tour of the code.",
    [
        OL([
            "Say the job in two sentences, including what the system will not do.",
            "Ask a question that should cite a note. Open the note at the cited span.",
            "Ask a question the corpus cannot answer. Show the refusal.",
            "Show one trace: tools called, caps, model id.",
            "Show the scorecard: pass count, safety fails, and one task you still fail.",
            "Stop. Let the other person ask.",
        ]),
        P("The unfixed failure is part of the demo. Hiding it teaches the audience that the scorecard is decoration. Saying what you would change next teaches the loop."),
        PR("Write the six beats as speaker notes under your task file. Time the first two out loud. If they take five minutes, cut words, not the refusal."),
        CK("Why include a task you still fail?", "Because the scorecard is evidence, and a perfect live demo without a remaining failure is usually a choice of questions."),
    ],
))

add(lesson(
    "13-05", "13", "core", 8,
    "Decide the next change from the scorecard",
    "The capstone is finished when you can defend the gate, including a gate that says not yet.",
    [
        P("After the demo, pick one next change from the failures, using the order you already learned. Retrieval miss, then prompt or schema, then tool permissions, then model swap, then, only if the rest is done, a training experiment you can compare to the base."),
        P("If the gate fails, the honest close is 'not ready to share as a tool'. That is a finished capstone. An unfinished one is a demo with no tasks."),
        UL([
            "Leave the corpus path, the tasks, the policy page, and the latest scorecard in one folder.",
            "Remove any key from that folder before you zip it for a teacher or a teammate.",
            "If you share the folder, say what a person must not upload.",
        ]),
        PR("Write the next change in one line, the failure it addresses, and whether the gate currently passes. Archive the folder."),
        CK("Can a capstone be complete if the gate fails?", "Yes, if the tasks, the trace, the policy, and the decision not to ship are all written down."),
    ],
))
