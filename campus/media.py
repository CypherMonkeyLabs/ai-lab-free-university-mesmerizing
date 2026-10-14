"""Deterministic offline audio motifs. No network, no speech synthesis at build time."""

from __future__ import annotations

import base64
import math
import struct


def _seed(text: str) -> int:
    value = 2166136261
    for char in text:
        value ^= ord(char)
        value = (value * 16777619) & 0xFFFFFFFF
    return value


def wav_bytes(key: str, seconds: float = 2.4) -> bytes:
    """A short pentatonic motif. The same key always produces the same clip."""
    rate = 16000
    rng = _seed(key)
    scale = (196.00, 246.94, 293.66, 349.23, 392.00, 493.88, 587.33)
    count = int(rate * seconds)
    samples = [0.0] * count
    cursor = 0
    note_count = 7
    for index in range(note_count):
        rng = (rng * 1664525 + 1013904223) & 0xFFFFFFFF
        freq = scale[rng % len(scale)]
        if index == note_count - 1:
            freq = scale[0] * 2
        length = int(rate * (0.22 if index < note_count - 1 else 0.55))
        if cursor + length > count:
            length = count - cursor
        for i in range(length):
            t = i / rate
            attack = min(1.0, i / 180)
            release = min(1.0, (length - i) / 500)
            env = attack * release
            tone = (
                0.62 * math.sin(2 * math.pi * freq * t)
                + 0.22 * math.sin(2 * math.pi * freq * 2 * t)
                + 0.08 * math.sin(2 * math.pi * freq * 3 * t)
            )
            samples[cursor + i] += tone * env * 0.55
        cursor += int(length * 0.72)
        if cursor >= count:
            break
    pcm = bytearray()
    for sample in samples:
        clipped = max(-1.0, min(1.0, sample))
        pcm += struct.pack("<h", int(clipped * 32767))
    header = b"RIFF" + struct.pack("<I", 36 + len(pcm)) + b"WAVEfmt "
    header += struct.pack("<IHHIIHH", 16, 1, 1, rate, rate * 2, 2, 16)
    header += b"data" + struct.pack("<I", len(pcm))
    return header + pcm


def wav_data_uri(key: str, seconds: float = 2.4) -> str:
    encoded = base64.b64encode(wav_bytes(key, seconds)).decode("ascii")
    return "\n".join(encoded[i : i + 2] for i in range(0, len(encoded), 2))
