#!/usr/bin/env python3
"""Acquire timestamped YouTube evidence without promoting it to historical fact.

The keyless path uses yt-dlp captions. If captions are absent, an explicit
--audio-fallback may use a Whisper-compatible Groq or OpenAI endpoint. Each URL
produces one typed JSON ledger, including degraded outcomes.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "video-evidence/v1"
VIDEO_ID_RE = re.compile(r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|shorts/|embed/))([A-Za-z0-9_-]{11})")
MAX_UPLOAD_BYTES = 24 * 1024 * 1024
CHUNK_SECONDS = 600


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def video_id_from_url(url: str) -> str | None:
    match = VIDEO_ID_RE.search(url)
    return match.group(1) if match else None


def run(command: list[str], timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)


def clean_text(text: str) -> str:
    return " ".join(text.replace("\u200b", "").split())


def parse_json3(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    segments: list[dict[str, Any]] = []
    for event in payload.get("events", []):
        text = clean_text("".join(str(part.get("utf8") or "") for part in event.get("segs", [])))
        if not text or text == "\n":
            continue
        start = round(float(event.get("tStartMs", 0)) / 1000, 3)
        duration = round(float(event.get("dDurationMs", 0)) / 1000, 3)
        segments.append({"start_s": start, "end_s": round(start + duration, 3), "text": text})
    return segments


def metadata(url: str, timeout: int) -> tuple[dict[str, Any], str | None]:
    result = run(["yt-dlp", "--ignore-config", "--dump-single-json", "--skip-download", "--no-warnings", url], timeout)
    if result.returncode != 0:
        return {}, (result.stderr or f"yt-dlp exited {result.returncode}").strip()[-500:]
    try:
        return json.loads(result.stdout), None
    except json.JSONDecodeError as exc:
        return {}, f"invalid metadata JSON: {exc}"


def caption_track(url: str, video_id: str, workdir: Path, languages: str, timeout: int) -> tuple[list[dict[str, Any]], str, list[str]]:
    errors: list[str] = []
    for kind, flag in (("manual_captions", "--write-subs"), ("automatic_captions", "--write-auto-subs")):
        for old in workdir.glob(f"{video_id}*.json3"):
            old.unlink()
        result = run([
            "yt-dlp", "--ignore-config", "--skip-download", flag,
            "--sub-langs", languages, "--sub-format", "json3", "--no-warnings",
            "-o", str(workdir / "%(id)s.%(ext)s"), url,
        ], timeout)
        files = sorted(workdir.glob(f"{video_id}*.json3"))
        if files:
            segments = parse_json3(files[0])
            if segments:
                return segments, kind, errors
        if result.returncode != 0:
            errors.append(f"{kind}: {(result.stderr or 'yt-dlp failure').strip()[-300:]}")
    return [], "", errors


def provider_config() -> tuple[str, str, str] | None:
    if os.environ.get("GROQ_API_KEY"):
        return "groq", "https://api.groq.com/openai/v1/audio/transcriptions", "whisper-large-v3"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai", "https://api.openai.com/v1/audio/transcriptions", "whisper-1"
    return None


def multipart_audio(path: Path, model: str) -> tuple[bytes, str]:
    boundary = f"----historicalEvidence{uuid.uuid4().hex}"
    fields = [("model", model), ("response_format", "verbose_json")]
    parts: list[bytes] = []
    for name, value in fields:
        parts.extend([
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode(),
        ])
    parts.extend([
        f"--{boundary}\r\n".encode(),
        b'Content-Disposition: form-data; name="file"; filename="audio.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n',
        path.read_bytes(), f"\r\n--{boundary}--\r\n".encode(),
    ])
    return b"".join(parts), boundary


def transcribe_chunk(path: Path, provider: tuple[str, str, str], timeout: int, offset: float) -> list[dict[str, Any]]:
    name, endpoint, model = provider
    key = os.environ["GROQ_API_KEY" if name == "groq" else "OPENAI_API_KEY"]
    body, boundary = multipart_audio(path, model)
    request = urllib.request.Request(endpoint, data=body, method="POST", headers={
        "Authorization": f"Bearer {key}", "Content-Type": f"multipart/form-data; boundary={boundary}",
    })
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if payload.get("segments"):
        return [{
            "start_s": round(offset + float(item.get("start", 0)), 3),
            "end_s": round(offset + float(item.get("end", item.get("start", 0))), 3),
            "text": clean_text(str(item.get("text") or "")),
        } for item in payload["segments"] if clean_text(str(item.get("text") or ""))]
    text = clean_text(str(payload.get("text") or ""))
    return [{"start_s": offset, "end_s": None, "text": text}] if text else []


def audio_fallback(url: str, workdir: Path, timeout: int) -> tuple[list[dict[str, Any]], str, list[str]]:
    provider = provider_config()
    if provider is None:
        return [], "", ["audio fallback requested but GROQ_API_KEY/OPENAI_API_KEY is absent"]
    if not shutil.which("ffmpeg"):
        return [], "", ["audio fallback requested but ffmpeg is absent"]
    output = workdir / "audio.mp3"
    result = run([
        "yt-dlp", "--ignore-config", "--no-playlist", "-x", "--audio-format", "mp3",
        "--audio-quality", "9", "-o", str(output), url,
    ], timeout)
    candidates = sorted(workdir.glob("audio*.mp3"))
    if result.returncode != 0 or not candidates:
        return [], "", [f"audio acquisition failed: {(result.stderr or '').strip()[-300:]}"]
    audio = candidates[0]
    chunks = [audio]
    if audio.stat().st_size > MAX_UPLOAD_BYTES:
        pattern = workdir / "chunk_%03d.mp3"
        split = run(["ffmpeg", "-y", "-i", str(audio), "-f", "segment", "-segment_time", str(CHUNK_SECONDS), "-c", "copy", str(pattern)], timeout)
        chunks = sorted(workdir.glob("chunk_*.mp3")) if split.returncode == 0 else []
    if not chunks:
        return [], "", ["audio chunking failed"]
    segments: list[dict[str, Any]] = []
    try:
        for index, chunk in enumerate(chunks):
            segments.extend(transcribe_chunk(chunk, provider, timeout, index * CHUNK_SECONDS))
    except (OSError, urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as exc:
        return [], "", [f"{provider[0]} transcription failed: {exc}"]
    return segments, f"audio_{provider[0]}", []


def acquire(url: str, languages: str, audio: bool, timeout: int) -> dict[str, Any]:
    vid = video_id_from_url(url)
    ledger: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION, "id": f"VE-YT-{vid or 'INVALID'}", "platform": "youtube",
        "url": url, "video_id": vid, "acquired_at": utc_now(), "status": "unresolved",
        "acquisition_method": None, "language_request": languages, "segments": [],
        "transcript_text": "", "transcript_sha256": None, "metadata": {}, "limitations": [], "errors": [],
    }
    if not vid:
        ledger["status"] = "invalid_url"; ledger["errors"].append("could not resolve an 11-character YouTube video id"); return ledger
    if not shutil.which("yt-dlp"):
        ledger["status"] = "missing_dependency"; ledger["errors"].append("yt-dlp is not installed"); return ledger
    with tempfile.TemporaryDirectory(prefix="yt-evidence-") as temp:
        workdir = Path(temp)
        meta, meta_error = metadata(url, timeout)
        ledger["metadata"] = {key: meta.get(key) for key in ("title", "channel", "channel_id", "upload_date", "duration", "webpage_url")}
        if meta_error:
            ledger["errors"].append(meta_error)
        segments, method, errors = caption_track(url, vid, workdir, languages, timeout)
        ledger["errors"].extend(errors)
        if not segments and audio:
            segments, method, errors = audio_fallback(url, workdir, timeout)
            ledger["errors"].extend(errors)
        if segments:
            transcript = " ".join(segment["text"] for segment in segments)
            ledger.update(status="success", acquisition_method=method, segments=segments,
                          transcript_text=transcript, transcript_sha256=hashlib.sha256(transcript.encode()).hexdigest())
            if method.startswith("audio_"):
                ledger["limitations"].append("speech-to-text output may contain recognition errors; verify names, dates and quotations")
        else:
            ledger["status"] = "no_transcript"
            ledger["limitations"].append("no caption or authorized audio transcription was recovered")
    return ledger


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("urls", nargs="+")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--languages", default="fr.*,en.*")
    parser.add_argument("--audio-fallback", action="store_true")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    failed = 0
    for url in args.urls:
        ledger = acquire(url, args.languages, args.audio_fallback, args.timeout)
        target = args.output / f"{ledger['id']}.json"
        target.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{ledger['status']}: {target}")
        failed += ledger["status"] != "success"
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
