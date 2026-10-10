"""read_attachment - extract text from a case attachment (PDF, text, JSON, CSV, image metadata).

Only files inside the loaded case folder can be read (no path traversal).
"""

from __future__ import annotations

import json
import mimetypes
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from pydantic import Field

from tools._common import CaseScopedInput, Tool, ToolFailure, load_context

TEXT_TYPES = {".txt", ".md", ".csv", ".log", ".eml", ".html", ".htm", ".xml", ".vtt", ".srt"}
IMAGE_TYPES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".heic", ".bmp"}
AUDIO_TYPES = {".mp3", ".wav", ".m4a", ".ogg", ".oga", ".flac", ".webm", ".mp4", ".aac", ".opus"}


class ReadAttachmentInput(CaseScopedInput):
    path: str = Field(
        ...,
        description="Attachment path relative to the case folder, e.g. 'attachments/attachment-02-estimate.pdf'.",
    )
    pages: Optional[str] = Field(
        None, pattern=r"^\d+(-\d+)?$", description="PDF page range, e.g. '1' or '2-4' (1-based)."
    )
    max_chars: int = Field(20_000, ge=500, le=200_000)


def _resolve(case_id: str, raw: str) -> Path:
    context = load_context(case_id)
    root = context.get("case_root")
    if not root:
        raise ToolFailure("no_case_folder", "This case was loaded from raw text and has no attachments.")
    root_path = Path(root).resolve()
    target = (root_path / raw).resolve()
    if root_path != target and root_path not in target.parents:
        raise ToolFailure("path_outside_case", "Attachments must be inside the case folder.")
    rel = target.relative_to(root_path).as_posix()
    if not target.is_file() or rel in context.get("hidden_files", []):
        available = [a["path"] for a in context.get("attachments", [])]
        raise ToolFailure("not_found", f"No attachment at {raw!r}.", details={"available": available})
    return target


def _pdf_text(path: Path, pages: Optional[str]) -> tuple[str, int, str]:
    first, last = None, None
    if pages:
        bounds = pages.split("-")
        first, last = int(bounds[0]), int(bounds[-1])
        if first < 1 or last < first:
            raise ToolFailure("invalid_pages", f"Invalid page range {pages!r}.")
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        count = len(reader.pages)
        lo = (first or 1) - 1
        hi = min(last or count, count)
        if lo >= count:
            raise ToolFailure("invalid_pages", f"PDF has only {count} page(s).")
        text = "\n\n".join(
            f"--- page {i + 1} ---\n{(reader.pages[i].extract_text() or '').strip()}" for i in range(lo, hi)
        )
        if text.replace("-", "").replace("page", "").strip(" \n0123456789"):
            return text, count, "pypdf"
    except ToolFailure:
        raise
    except Exception:  # noqa: BLE001 - fall back to poppler below
        count = 0
    if shutil.which("pdftotext"):
        cmd = ["pdftotext", "-layout"]
        if first:
            cmd += ["-f", str(first), "-l", str(last)]
        out = subprocess.run(cmd + [str(path), "-"], capture_output=True, text=True, timeout=60)
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout, count, "pdftotext"
    raise ToolFailure(
        "unreadable_pdf",
        "No text could be extracted (the PDF may be scanned images). Treat its contents as unknown.",
    )


def _handle(params: ReadAttachmentInput) -> tuple[dict, list[str]]:
    path = _resolve(params.case_id, params.path)
    suffix = path.suffix.lower()
    warnings: list[str] = []
    data: dict = {
        "path": params.path,
        "bytes": path.stat().st_size,
        "mime_type": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
    }

    if suffix == ".pdf":
        text, page_count, engine = _pdf_text(path, params.pages)
        data.update(kind="pdf", page_count=page_count, engine=engine)
    elif suffix == ".json":
        raw = path.read_text(encoding="utf-8", errors="replace")
        try:
            text = json.dumps(json.loads(raw), indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            text = raw
            warnings.append("File is not valid JSON; returned as plain text.")
        data["kind"] = "json"
    elif suffix in TEXT_TYPES:
        text = path.read_text(encoding="utf-8", errors="replace")
        data["kind"] = "text"
    elif suffix in IMAGE_TYPES:
        data.update(kind="image", absolute_path=str(path))
        data["text"] = None
        warnings.append("Image file: no text extracted. Pass absolute_path to a vision-capable model to inspect it.")
        return data, warnings
    elif suffix in AUDIO_TYPES:
        raise ToolFailure("audio_file", "This is an audio file; use transcribe_audio instead.")
    else:
        raise ToolFailure("unsupported_type", f"Unsupported attachment type {suffix or '(none)'}.")

    truncated = len(text) > params.max_chars
    data["text"] = text[: params.max_chars] + ("\n…[truncated]" if truncated else "")
    data["truncated"] = truncated
    data["chars"] = len(text)
    if truncated:
        warnings.append(f"Text truncated to {params.max_chars} characters; request specific pages for more.")
    return data, warnings


TOOL = Tool(
    name="read_attachment",
    description="""
Read a file attached to the loaded case and return its text. Works for PDFs (quotes, invoices,
checkout/inspection reports), text, markdown, CSV and JSON. Images return metadata only;
audio files must go through transcribe_audio. Paths are relative to the case folder, exactly
as listed by load_case. If extraction fails, treat the document's contents as unknown rather
than guessing.
""",
    input_model=ReadAttachmentInput,
    handler=_handle,
    side_effect=False,
)
