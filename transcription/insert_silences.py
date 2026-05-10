#!/usr/bin/env python3
"""
insert_silences.py — Take an audio recording plus a multi-line transcript,
find the timestamps at each line break, and splice silence in there.

Useful as a preprocessing step for manim's StitcherService (or any tool that
wants pre-baked silence "slots" in a single audio file).

Usage:
    python insert_silences.py audio.wav transcript.txt out.wav
    python insert_silences.py audio.mp3 lines.txt out.mp3 --silence 5.0 --model base

Install:
    pip install faster-whisper pydub
    # also needs ffmpeg on your PATH (for pydub)
"""

import argparse
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

from faster_whisper import WhisperModel # type: ignore
from pydub import AudioSegment


def normalize(word: str) -> str:
    """Lowercase, keep only word chars and apostrophes. Used for matching."""
    return re.sub(r"[^\w']", "", word).lower()


def transcribe(audio_path: str, model_size: str = "base") -> list[dict]:
    """Run faster-whisper and return a flat list of word-level dicts."""
    print(f"Loading whisper model '{model_size}'...", file=sys.stderr)
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    print("Transcribing...", file=sys.stderr)
    segments, _ = model.transcribe(audio_path, word_timestamps=True)

    words = []
    for seg in segments:
        if not seg.words:
            continue
        for w in seg.words:
            n = normalize(w.word)
            if n:
                words.append({"word": w.word, "norm": n, "start": w.start, "end": w.end})
    print(f"  detected {len(words)} words", file=sys.stderr)
    return words


def load_transcript(path: str) -> list[list[str]]:
    """Read transcript file -> list of lines, each a list of normalized words."""
    lines = []
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        words = [normalize(w) for w in raw.split()]
        words = [w for w in words if w]  # drop pure-punctuation tokens
        if words:
            lines.append(words)
    return lines


def find_breakpoints(lines: list[list[str]], whisper_words: list[dict]) -> list[dict]:
    """For each line break in the transcript, find the matching whisper word's end time."""
    # Flatten transcript with metadata
    flat = []
    for li, line in enumerate(lines):
        for pi, w in enumerate(line):
            flat.append({"norm": w, "line": li, "pos": pi, "line_len": len(line)})

    transcript_norm = [t["norm"] for t in flat]
    whisper_norm = [w["norm"] for w in whisper_words]

    # Sequence-align transcript -> whisper. Tolerates small mishearings/insertions/deletions.
    matcher = SequenceMatcher(a=transcript_norm, b=whisper_norm, autojunk=False)
    alignment: list[int | None] = [None] * len(flat)  # transcript idx -> whisper idx
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            for k in range(i2 - i1):
                alignment[i1 + k] = j1 + k

    n_aligned = sum(1 for a in alignment if a is not None)
    print(
        f"Aligned {n_aligned}/{len(flat)} transcript words to whisper output",
        file=sys.stderr,
    )

    # Find line endings (skip the very last line — nothing follows it)
    breakpoints = []
    n_lines = len(lines)
    for i, t in enumerate(flat):
        is_line_end = t["pos"] == t["line_len"] - 1
        if not is_line_end or t["line"] >= n_lines - 1:
            continue

        wi = alignment[i]

        # If this exact word wasn't aligned, walk backwards to nearest aligned word,
        # then forwards. This is a fallback for misheard line-final words.
        if wi is None:
            for back in range(i - 1, -1, -1):
                if alignment[back] is not None:
                    wi = alignment[back]
                    break
        if wi is None:
            for fwd in range(i + 1, len(flat)):
                if alignment[fwd] is not None:
                    wi = alignment[fwd]
                    break
        if wi is None:
            print(
                f"  ! could not locate end of line {t['line']+1} "
                f"(word '{t['norm']}'); skipping",
                file=sys.stderr,
            )
            continue

        ww = whisper_words[wi]
        breakpoints.append(
            {
                "line": t["line"],
                "transcript_word": t["norm"],
                "whisper_word": ww["norm"],
                "end_time": ww["end"],
                "matched": ww["norm"] == t["norm"],
            }
        )
    return breakpoints


def insert_silence(
    audio_path: str,
    output_path: str,
    breakpoints: list[dict],
    silence_seconds: float,
) -> None:
    """Load audio, splice silence in at each breakpoint, write out."""
    audio = AudioSegment.from_file(audio_path)
    silence = AudioSegment.silent(duration=int(silence_seconds * 1000))

    # Insert from latest to earliest so earlier offsets aren't shifted by inserts.
    bps_sorted = sorted(breakpoints, key=lambda b: b["end_time"], reverse=True)
    for bp in bps_sorted:
        cut_ms = int(bp["end_time"] * 1000)
        audio = audio[:cut_ms] + silence + audio[cut_ms:]

    fmt = Path(output_path).suffix.lstrip(".").lower() or "wav"
    audio.export(output_path, format=fmt)


def main():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("audio", help="Input audio file (any format ffmpeg can read)")
    p.add_argument("transcript", help="Plain-text transcript, one chunk per line")
    p.add_argument("output", help="Output audio file (extension picks format)")
    p.add_argument(
        "--silence",
        type=float,
        default=5.0,
        help="Seconds of silence to insert at each line break (default 5)",
    )
    p.add_argument(
        "--model",
        default="base",
        help="faster-whisper model size: tiny | base | small | medium | large-v3 (default base)",
    )
    args = p.parse_args()

    lines = load_transcript(args.transcript)
    print(f"Transcript: {len(lines)} lines", file=sys.stderr)
    if len(lines) < 2:
        print("Need at least 2 lines to have a break between them. Nothing to do.", file=sys.stderr)
        return 1

    words = transcribe(args.audio, args.model)
    breakpoints = find_breakpoints(lines, words)

    print("\nBreakpoints:", file=sys.stderr)
    for bp in breakpoints:
        flag = "✓" if bp["matched"] else "~"  # ~ = used a fallback word
        print(
            f"  {flag} after line {bp['line']+1} "
            f"('{bp['transcript_word']}' → whisper '{bp['whisper_word']}') "
            f"at {bp['end_time']:.3f}s",
            file=sys.stderr,
        )

    insert_silence(args.audio, args.output, breakpoints, args.silence)
    print(f"\nWrote {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())