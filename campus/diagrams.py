"""Inline SVG figures. Colors come from CSS variables so light and dark both work."""

from __future__ import annotations


def _svg(title, body, viewbox):
    return (
        f'<svg class="fig" viewBox="{viewbox}" role="img" aria-label="{title}">'
        f"<title>{title}</title>{body}</svg>"
    )


def context_budget():
    body = """
    <rect x="24" y="36" width="712" height="36" rx="8" class="track"/>
    <rect x="24" y="36" width="110" height="36" rx="8" class="seg seg-a"/>
    <rect x="134" y="36" width="250" height="36" class="seg seg-b"/>
    <rect x="384" y="36" width="180" height="36" class="seg seg-c"/>
    <rect x="564" y="36" width="172" height="36" rx="8" class="seg seg-d"/>
    <text x="79" y="59" text-anchor="middle" class="onseg">Instructions</text>
    <text x="259" y="59" text-anchor="middle" class="onseg">Retrieved text</text>
    <text x="474" y="59" text-anchor="middle" class="onseg">Conversation</text>
    <text x="650" y="59" text-anchor="middle" class="onseg">Answer room</text>
    <text x="24" y="110" class="label">Input and output share one window. If you fill the left side, the model has no room to answer, and early instructions are the first thing to fall off.</text>
    <g transform="translate(24,150)">
      <rect width="12" height="12" rx="3" class="seg seg-a"/>
      <text x="20" y="11" class="label">Keep standing rules short.</text>
    </g>
    <g transform="translate(250,150)">
      <rect width="12" height="12" rx="3" class="seg seg-b"/>
      <text x="20" y="11" class="label">Pass only the passages you need.</text>
    </g>
    <g transform="translate(500,150)">
      <rect width="12" height="12" rx="3" class="seg seg-d"/>
      <text x="20" y="11" class="label">Reserve output tokens on purpose.</text>
    </g>
    """
    return _svg("Context window shared by instructions, retrieval, conversation, and the answer", body, "0 0 760 200")


def agent_loop():
    return _svg("Agent loop", _agent_clean(), "0 0 780 440")


def _agent_clean():
    return """
    <defs>
      <marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
        <path d="M 0 1 L 8 5 L 0 9 z" class="arrowhead"/>
      </marker>
    </defs>
    <text x="28" y="28" class="label">Call a tool, read what came back, and repeat. Stop on an answer, a cap, or an error.</text>

    <rect x="270" y="46" width="180" height="64" rx="14" class="node"/>
    <text x="360" y="74" text-anchor="middle" class="nt">Goal</text>
    <text x="360" y="94" text-anchor="middle" class="ns">what done means</text>

    <rect x="250" y="156" width="220" height="108" rx="14" class="node node-hot"/>
    <text x="360" y="196" text-anchor="middle" class="nt">Model</text>
    <text x="360" y="218" text-anchor="middle" class="ns">call a tool</text>
    <text x="360" y="238" text-anchor="middle" class="ns">or stop</text>

    <rect x="560" y="168" width="180" height="84" rx="14" class="node"/>
    <text x="650" y="202" text-anchor="middle" class="nt">Tool</text>
    <text x="650" y="224" text-anchor="middle" class="ns">schema and handler</text>

    <rect x="560" y="300" width="180" height="84" rx="14" class="node"/>
    <text x="650" y="334" text-anchor="middle" class="nt">Observation</text>
    <text x="650" y="356" text-anchor="middle" class="ns">result or error</text>

    <rect x="40" y="300" width="190" height="84" rx="14" class="node node-ok"/>
    <text x="135" y="334" text-anchor="middle" class="nt">Stop</text>
    <text x="135" y="356" text-anchor="middle" class="ns">answer, cap, or error</text>

    <line x1="360" y1="110" x2="360" y2="152" class="edge" marker-end="url(#ah)"/>
    <line x1="470" y1="200" x2="556" y2="200" class="edge" marker-end="url(#ah)"/>
    <line x1="650" y1="252" x2="650" y2="296" class="edge" marker-end="url(#ah)"/>
    <path d="M560 342 H500 V210 H474" class="edge" fill="none" marker-end="url(#ah)"/>
    <line x1="250" y1="230" x2="160" y2="300" class="edge" marker-end="url(#ah)"/>

    <rect x="478" y="138" width="84" height="24" rx="12" class="gate"/>
    <text x="520" y="155" text-anchor="middle" class="gs">Ask first</text>
    <text x="492" y="300" text-anchor="end" class="ns">loop</text>
    <text x="28" y="418" class="label">Side effects wait at Ask first. Read-only tools can run inside the step cap. The trace records every call.</text>
    """


def rag_pipeline():
    return _svg(
        "Retrieval pipeline: index once, then retrieve, rerank, and cite on every question",
        """
        <text x="28" y="28" class="label">Two clocks. Indexing happens when documents change. Answering happens on every question.</text>
        <text x="28" y="64" class="kicker">Index once</text>
        <rect x="28" y="80" width="150" height="64" rx="12" class="node"/>
        <text x="103" y="108" text-anchor="middle" class="nt">Documents</text>
        <text x="103" y="128" text-anchor="middle" class="ns">pages you trust</text>
        <rect x="214" y="80" width="150" height="64" rx="12" class="node"/>
        <text x="289" y="108" text-anchor="middle" class="nt">Chunk</text>
        <text x="289" y="128" text-anchor="middle" class="ns">keep headings whole</text>
        <rect x="400" y="80" width="150" height="64" rx="12" class="node"/>
        <text x="475" y="108" text-anchor="middle" class="nt">Embed</text>
        <text x="475" y="128" text-anchor="middle" class="ns">one model, pinned</text>
        <rect x="586" y="80" width="170" height="64" rx="12" class="node node-hot"/>
        <text x="671" y="108" text-anchor="middle" class="nt">Index</text>
        <text x="671" y="128" text-anchor="middle" class="ns">vectors + keywords</text>
        <line x1="178" y1="112" x2="210" y2="112" class="edge" marker-end="url(#ah2)"/>
        <line x1="364" y1="112" x2="396" y2="112" class="edge" marker-end="url(#ah2)"/>
        <line x1="550" y1="112" x2="582" y2="112" class="edge" marker-end="url(#ah2)"/>

        <text x="28" y="196" class="kicker">Every question</text>
        <rect x="28" y="212" width="130" height="64" rx="12" class="node"/>
        <text x="93" y="240" text-anchor="middle" class="nt">Question</text>
        <text x="93" y="260" text-anchor="middle" class="ns">as asked</text>
        <rect x="190" y="212" width="150" height="64" rx="12" class="node"/>
        <text x="265" y="240" text-anchor="middle" class="nt">Retrieve</text>
        <text x="265" y="260" text-anchor="middle" class="ns">hybrid search</text>
        <rect x="372" y="212" width="140" height="64" rx="12" class="node"/>
        <text x="442" y="240" text-anchor="middle" class="nt">Rerank</text>
        <text x="442" y="260" text-anchor="middle" class="ns">short list</text>
        <rect x="544" y="212" width="212" height="64" rx="12" class="node node-ok"/>
        <text x="650" y="240" text-anchor="middle" class="nt">Answer + citation</text>
        <text x="650" y="260" text-anchor="middle" class="ns">quote the chunk id</text>
        <line x1="158" y1="244" x2="186" y2="244" class="edge" marker-end="url(#ah2)"/>
        <line x1="340" y1="244" x2="368" y2="244" class="edge" marker-end="url(#ah2)"/>
        <line x1="512" y1="244" x2="540" y2="244" class="edge" marker-end="url(#ah2)"/>

        <path d="M671 144 C 671 180, 265 180, 265 208" class="edge edge-soft" fill="none" marker-end="url(#ah2)"/>
        <text x="28" y="312" class="label">If the right chunk is not in the short list, a better prompt will not save the answer. Fix retrieval first.</text>
        <defs>
          <marker id="ah2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 1.2 L 8.5 5 L 0 8.8 z" class="arrowhead"/>
          </marker>
        </defs>
        """,
        "0 0 800 340",
    )


def eval_workflow():
    return _svg(
        "Eval workflow from a versioned task set to a ship-or-fix gate",
        """
        <defs>
          <marker id="ah3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 1.2 L 8.5 5 L 0 8.8 z" class="arrowhead"/>
          </marker>
        </defs>
        <text x="24" y="28" class="label">Run the same tasks every time. Change one thing: prompt, model, index, or tool.</text>
        <rect x="24" y="78" width="128" height="86" rx="12" class="node"/>
        <text x="88" y="110" text-anchor="middle" class="nt">Tasks</text>
        <text x="88" y="132" text-anchor="middle" class="ns">versioned set</text>
        <rect x="180" y="78" width="120" height="86" rx="12" class="node"/>
        <text x="240" y="110" text-anchor="middle" class="nt">Run</text>
        <text x="240" y="132" text-anchor="middle" class="ns">pin the model</text>
        <rect x="328" y="78" width="140" height="86" rx="12" class="node node-hot"/>
        <text x="398" y="106" text-anchor="middle" class="nt">Score</text>
        <text x="398" y="128" text-anchor="middle" class="ns">quality · safety</text>
        <text x="398" y="146" text-anchor="middle" class="ns">latency · cost</text>
        <rect x="496" y="78" width="140" height="86" rx="12" class="node"/>
        <text x="566" y="110" text-anchor="middle" class="nt">Compare</text>
        <text x="566" y="132" text-anchor="middle" class="ns">to the baseline</text>
        <rect x="664" y="70" width="112" height="102" rx="12" class="node node-ok"/>
        <text x="720" y="108" text-anchor="middle" class="nt">Gate</text>
        <text x="720" y="130" text-anchor="middle" class="ns">ship or fix</text>
        <line x1="152" y1="121" x2="176" y2="121" class="edge" marker-end="url(#ah3)"/>
        <line x1="300" y1="121" x2="324" y2="121" class="edge" marker-end="url(#ah3)"/>
        <line x1="468" y1="121" x2="492" y2="121" class="edge" marker-end="url(#ah3)"/>
        <line x1="636" y1="121" x2="660" y2="121" class="edge" marker-end="url(#ah3)"/>
        <text x="24" y="210" class="label">Keep the score next to the exact prompt, model id, and index version. A screenshot of one good answer is not an eval.</text>
        """,
        "0 0 800 240",
    )


def mcp_architecture():
    return _svg(
        "MCP host, client, and server",
        """
        <defs>
          <marker id="ah4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 1.2 L 8.5 5 L 0 8.8 z" class="arrowhead"/>
          </marker>
        </defs>
        <rect x="28" y="48" width="230" height="250" rx="16" class="frame"/>
        <text x="44" y="76" class="kicker">Host</text>
        <text x="44" y="100" class="nt">The app a person uses</text>
        <text x="44" y="122" class="ns">editor, desktop app, your UI</text>
        <rect x="48" y="150" width="190" height="112" rx="12" class="node node-hot"/>
        <text x="143" y="188" text-anchor="middle" class="nt">MCP client</text>
        <text x="143" y="210" text-anchor="middle" class="ns">opens a session</text>
        <text x="143" y="230" text-anchor="middle" class="ns">asks before tools run</text>

        <rect x="300" y="130" width="150" height="86" rx="12" class="gate"/>
        <text x="375" y="162" text-anchor="middle" class="nt">Transport</text>
        <text x="375" y="184" text-anchor="middle" class="ns">stdio or HTTP</text>

        <rect x="492" y="48" width="280" height="250" rx="16" class="frame"/>
        <text x="508" y="76" class="kicker">Server</text>
        <text x="508" y="100" class="nt">A program you chose</text>
        <rect x="512" y="124" width="240" height="44" rx="10" class="node"/>
        <text x="632" y="152" text-anchor="middle" class="nt">Tools · actions</text>
        <rect x="512" y="178" width="240" height="44" rx="10" class="node"/>
        <text x="632" y="206" text-anchor="middle" class="nt">Resources · readable data</text>
        <rect x="512" y="232" width="240" height="44" rx="10" class="node"/>
        <text x="632" y="260" text-anchor="middle" class="nt">Prompts · templates</text>

        <line x1="258" y1="190" x2="296" y2="173" class="edge" marker-end="url(#ah4)"/>
        <line x1="450" y1="173" x2="488" y2="156" class="edge" marker-end="url(#ah4)"/>

        <text x="28" y="332" class="label">The server is not the model. It exposes capabilities. Treat its tool descriptions as untrusted text: they enter the prompt.</text>
        <text x="28" y="356" class="label">A remote server needs authentication. A local server still needs consent. Auto-approving every tool is how data leaves the machine.</text>
        """,
        "0 0 800 380",
    )


def lora_adapter():
    return _svg(
        "LoRA keeps base weights frozen and trains a small adapter",
        """
        <text x="28" y="32" class="label">You are not rewriting the model. You are adding a small trainable piece and leaving the rest fixed.</text>
        <text x="80" y="68" class="kicker">Base model</text>
        <text x="430" y="68" class="kicker">Base + LoRA</text>

        <rect x="70" y="88" width="200" height="48" rx="10" class="node"/>
        <text x="170" y="118" text-anchor="middle" class="nt">Layer · frozen</text>
        <rect x="70" y="148" width="200" height="48" rx="10" class="node"/>
        <text x="170" y="178" text-anchor="middle" class="nt">Layer · frozen</text>
        <rect x="70" y="208" width="200" height="48" rx="10" class="node"/>
        <text x="170" y="238" text-anchor="middle" class="nt">Layer · frozen</text>
        <text x="170" y="284" text-anchor="middle" class="ns">Same weights you started with</text>

        <rect x="400" y="88" width="200" height="48" rx="10" class="node"/>
        <text x="500" y="118" text-anchor="middle" class="nt">Layer · frozen</text>
        <rect x="612" y="88" width="130" height="48" rx="10" class="node node-hot"/>
        <text x="677" y="118" text-anchor="middle" class="nt">Adapter</text>

        <rect x="400" y="148" width="200" height="48" rx="10" class="node"/>
        <text x="500" y="178" text-anchor="middle" class="nt">Layer · frozen</text>
        <rect x="612" y="148" width="130" height="48" rx="10" class="node node-hot"/>
        <text x="677" y="178" text-anchor="middle" class="nt">Adapter</text>

        <rect x="400" y="208" width="200" height="48" rx="10" class="node"/>
        <text x="500" y="238" text-anchor="middle" class="nt">Layer · frozen</text>
        <rect x="612" y="208" width="130" height="48" rx="10" class="node node-hot"/>
        <text x="677" y="238" text-anchor="middle" class="nt">Adapter</text>
        <text x="560" y="284" text-anchor="middle" class="ns">Train these small matrices only</text>
        <text x="28" y="332" class="label">QLoRA stores the frozen base in a quantized form so the same idea fits on one GPU. The eval still compares adapter versus base on your tasks.</text>
        """,
        "0 0 780 360",
    )


FIGURES = {
    "context-budget": context_budget(),
    "agent-loop": agent_loop(),
    "rag-pipeline": rag_pipeline(),
    "eval-workflow": eval_workflow(),
    "mcp-architecture": mcp_architecture(),
    "lora": lora_adapter(),
}
