"""Interactive demos and labeled audio clips. No network and no keys."""

from __future__ import annotations

import html



def esc(text: str) -> str:
    return html.escape(text, quote=True)


def _note(text: str) -> str:
    return f'<p class="widget-note">{esc(text)}</p>'


def tokenizer() -> str:
    return (
        '<section class="widget" data-widget="tokenizer">'
        "<h3>Toy tokenizer</h3>"
        + _note("Longest match against a tiny vocabulary, then one character at a time. A shipping model uses its own trained tokenizer. Count with that one before you budget a prompt.")
        + '<label>Text<textarea class="tok-in" rows="3">The model predicts the next token.</textarea></label>'
        '<p><button type="button" class="btn tok-go">Count tokens</button></p>'
        '<div class="tok-out" aria-live="polite"></div>'
        '<p class="tok-count"></p></section>'
    )


def cosine() -> str:
    return (
        '<section class="widget" data-widget="cosine">'
        "<h3>Cosine similarity</h3>"
        + _note("Cosine is the dot product divided by the two lengths. These vectors are hand-set teaching numbers, not the output of an embedding model.")
        + '<label>Preset <select class="cos-preset" aria-label="Vector preset">'
        '<option value="near">refund and return window</option>'
        '<option value="far">refund and gpu driver</option>'
        '<option value="same">identical vectors</option>'
        "</select></label>"
        '<div class="vec-grid"><fieldset><legend>Vector A</legend><span class="vec vec-a"></span></fieldset>'
        '<fieldset><legend>Vector B</legend><span class="vec vec-b"></span></fieldset></div>'
        '<p class="cos-out" aria-live="polite"></p></section>'
    )


def attention() -> str:
    return (
        '<section class="widget" data-widget="attention">'
        "<h3>Attention heatmap</h3>"
        + _note("Causal attention: a position may look at itself and earlier tokens only. The compute mode runs QKᵀ / √d and softmax on fixed toy vectors, with Wq and Wk as identity. The sketch mode is a hand-drawn pattern, not a trained model.")
        + '<label>Mode <select class="att-mode" aria-label="Attention mode">'
        '<option value="math">Compute from toy vectors</option>'
        '<option value="sketch">Hand-drawn pattern</option>'
        "</select></label>"
        '<div class="att-grid" aria-live="polite"></div></section>'
    )


def rag() -> str:
    return (
        '<section class="widget" data-widget="rag">'
        "<h3>Mini retrieval</h3>"
        + _note("Six sample notes live in the page. Keyword overlap always runs. Preset questions also have a hand-set vector so you can see hybrid ranking. The answer is a template that quotes the winning chunk, or refuses. No model is called.")
        + '<label>Question <input class="rag-q" type="text" value="How long do I have to return an item?"/></label>'
        '<p><button type="button" class="btn rag-go">Retrieve</button></p>'
        '<div class="rag-hits"></div><div class="rag-answer" aria-live="polite"></div></section>'
    )


def loss() -> str:
    return (
        '<section class="widget" data-widget="loss">'
        "<h3>Loss sketch</h3>"
        + _note("A sketch of a shape you will see in training write-ups. Training loss falls. Validation loss can rise when the run memorizes. This is not a log from a named model.")
        + '<label>Memorization pressure <input class="loss-over" type="range" min="0" max="100" value="18"/></label>'
        '<svg class="loss-svg fig" viewBox="0 0 640 260" role="img" aria-label="Sketch of training and validation loss">'
        '<text class="ns" x="48" y="24">Loss sketch</text>'
        '<line x1="48" y1="210" x2="600" y2="210" class="edge"/>'
        '<line x1="48" y1="30" x2="48" y2="210" class="edge"/>'
        '<path class="loss-train" d="" fill="none"/>'
        '<path class="loss-val" d="" fill="none"/>'
        '<text class="ns" x="520" y="48">train</text>'
        '<text class="ns" x="520" y="68">validation</text></svg>'
        '<p class="loss-read" aria-live="polite"></p></section>'
    )


def sample() -> str:
    return (
        '<section class="widget" data-widget="sample">'
        "<h3>Temperature and top-p</h3>"
        + _note("Eight fixed logits. Temperature divides them before softmax. Top-p keeps the smallest high-probability set that reaches p, then renormalizes. Neither knob checks facts. A temperature of 0.05 stands in for greedy decoding; many APIs treat 0 as argmax.")
        + '<label>Temperature <input class="temp" type="range" min="5" max="200" value="80"/></label>'
        '<label>Top-p <input class="topp" type="range" min="10" max="100" value="100"/></label>'
        '<div class="sample-bars" aria-live="polite"></div></section>'
    )


def context() -> str:
    return (
        '<section class="widget" data-widget="context">'
        "<h3>Context budget and a cost sketch</h3>"
        + _note("Instructions, retrieved text, conversation, and reserved answer tokens share one window. Prices start empty. The example button fills placeholders, not a quote. Read your provider's card.")
        + '<label>Instructions <input class="c-sys" type="range" min="50" max="4000" value="400"/></label>'
        '<label>Retrieved <input class="c-ret" type="range" min="0" max="20000" value="2000"/></label>'
        '<label>Conversation <input class="c-chat" type="range" min="0" max="20000" value="800"/></label>'
        '<label>Answer reserved <input class="c-out" type="range" min="50" max="8000" value="600"/></label>'
        '<label>Example window <select class="c-win" aria-label="Example context window">'
        '<option value="8192">8k example</option><option value="32768" selected>32k example</option>'
        '<option value="128000">128k example</option><option value="200000">200k example</option>'
        '<option value="1000000">1M example</option></select></label>'
        '<div class="price-row"><label>Input price / 1M <input class="c-pin" type="number" min="0" step="0.01" value=""/></label>'
        '<label>Output price / 1M <input class="c-pout" type="number" min="0" step="0.01" value=""/></label>'
        '<button type="button" class="btn c-example">Fill example prices</button></div>'
        '<div class="c-bar" aria-hidden="true"><i class="c-a"></i><i class="c-b"></i><i class="c-c"></i><i class="c-d"></i></div>'
        '<p class="c-read" aria-live="polite"></p></section>'
    )


def latency() -> str:
    return (
        '<section class="widget" data-widget="latency">'
        "<h3>Latency and quality, as a design sketch</h3>"
        + _note("Positions are for a design conversation. They are not a benchmark and they are not a ranking of vendors. A local model is not automatically more accurate. A long window is not automatically more careful.")
        + '<svg class="lat-svg fig" viewBox="0 0 640 320" role="img" aria-label="Illustrative latency and quality positions"></svg>'
        '<p class="lat-read" aria-live="polite"></p></section>'
    )


def scorecard() -> str:
    return (
        '<section class="widget" data-widget="scorecard">'
        "<h3>Eval scorecard</h3>"
        + _note("Move the candidate against a baseline you set. The gate ships only when quality is not worse, safety failures are not higher, and latency and cost stay inside the budgets.")
        + '<div class="score-grid"></div><p class="score-gate" aria-live="polite"></p></section>'
    )


def embed() -> str:
    return (
        '<section class="widget" data-widget="embed">'
        "<h3>Embedding space, drawn in 2D</h3>"
        + _note("A picture of a toy space. Real embedding vectors have hundreds or thousands of dimensions. Click a point to mark its nearest neighbors by ordinary distance in this drawing.")
        + '<svg class="emb-svg fig" viewBox="0 0 640 320" role="img" aria-label="Toy two dimensional embedding map"></svg>'
        '<p class="emb-read" aria-live="polite"></p></section>'
    )


WIDGETS = {
    "tokenizer": tokenizer,
    "cosine": cosine,
    "attention": attention,
    "rag": rag,
    "loss": loss,
    "sample": sample,
    "context": context,
    "latency": latency,
    "scorecard": scorecard,
    "embed": embed,
}


def widget_html(name: str) -> str:
    if name not in WIDGETS:
        raise SystemExit(f"Unknown widget {name}")
    return WIDGETS[name]()


def audio_html(index: int, total: int, title: str, transcript: str, key: str) -> str:
    return (
        f'<figure class="clip">'
        f"<figcaption><strong>Audio clip {index} of {total}.</strong> {esc(title)}. "
        f"A generated tone stored beside this page. No remote file.</figcaption>"
        f'<audio controls preload="none" src="assets/audio/{esc(key)}.wav" data-caption="{esc(transcript)}"></audio>'
        f'<p class="transcript"><span>Transcript.</span> {esc(transcript)}</p>'
        f'<p><button type="button" class="btn speak" data-transcript="{esc(transcript)}">Play spoken intro</button></p>'
        f'<p class="speak-note">Uses this device\'s speech engine when it has one. Nothing is uploaded.</p>'
        f"</figure>"
    )
