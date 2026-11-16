import os
import re
import uuid
import io
from typing import Tuple, Dict, Any, Optional
from fastapi import UploadFile
from PIL import Image, ImageOps
from app.Enum.UploadCategory import UploadCategory

UPLOAD_BASE_DIR = os.path.join(os.getcwd(), "uploads")

IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

CATEGORY_CONFIG = {
    UploadCategory.PROFILES.value: {
        "extensions": {"jpg", "jpeg", "png", "webp"},
        "mimes": {"image/jpeg", "image/png", "image/webp"},
        "max_size": 5 * 1024 * 1024,  # 5 MB
        "max_dim": (800, 800),
        "label": "Profile image (JPG, PNG, WEBP, max 5MB)",
    },
    UploadCategory.DOCUMENTS.value: {
        "extensions": {"jpg", "jpeg", "png", "pdf", "docx", "xlsx", "csv"},
        "mimes": {
            "image/jpeg",
            "image/png",
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "text/csv",
            "application/msword",
            "application/vnd.ms-excel",
        },
        "max_size": 15 * 1024 * 1024,  # 15 MB
        "max_dim": (1920, 1920),
        "label": "Document (PDF, Word, Excel, CSV, Image, max 15MB)",
    },
    UploadCategory.GENERAL.value: {
        "extensions": {"jpg", "jpeg", "png", "webp", "pdf"},
        "mimes": {"image/jpeg", "image/png", "image/webp", "application/pdf"},
        "max_size": 10 * 1024 * 1024,  # 10 MB
        "max_dim": (1920, 1920),
        "label": "Media file (max 10MB)",
    },
}


def sanitize_filename(filename: str) -> Tuple[str, str]:
    if not filename or "." not in filename:
        return "file", "bin"

    name_part, ext_part = filename.rsplit(".", 1)
    clean_ext = ext_part.lower().strip()
    clean_name = re.sub(r"[^a-zA-Z0-9_-]", "_", name_part)[:50]
    if not clean_name:
        clean_name = "file"

    return clean_name, clean_ext


def validate_file(file: UploadFile, category: str) -> Optional[str]:
    config = CATEGORY_CONFIG.get(category, CATEGORY_CONFIG[UploadCategory.GENERAL.value])

    if not file.filename:
        return "No file uploaded or filename missing"

    _, ext = sanitize_filename(file.filename)
    if ext not in config["extensions"]:
        return f"Invalid file format '.{ext}'. Allowed formats for {category}: {', '.join(sorted(config['extensions']))}"

    content_type = (file.content_type or "").lower()
    if content_type and content_type not in config["mimes"]:
        if content_type != "application/octet-stream":
            return f"Invalid MIME type '{content_type}'. Required: {config['label']}"

    return None


def _compress_image_to_webp(raw_bytes: bytes, max_dim: Tuple[int, int]) -> bytes:

    with Image.open(io.BytesIO(raw_bytes)) as img:
        img = ImageOps.exif_transpose(img)

        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")

        img.thumbnail(max_dim, Image.Resampling.LANCZOS)

        output_buffer = io.BytesIO()
        img.save(output_buffer, format="WEBP", quality=80, method=6)
        return output_buffer.getvalue()


async def save_upload_file(
    file: UploadFile,
    category: str,
    base_url: str = "",
) -> Tuple[bool, Dict[str, Any] | str]:
    category_val = category.lower() if category in CATEGORY_CONFIG else UploadCategory.GENERAL.value
    config = CATEGORY_CONFIG[category_val]

    validation_err = validate_file(file, category_val)
    if validation_err:
        return False, validation_err

    clean_name, ext = sanitize_filename(file.filename or "")
    dest_folder = os.path.join(UPLOAD_BASE_DIR, category_val)
    os.makedirs(dest_folder, exist_ok=True)

    is_image = ext in IMAGE_EXTENSIONS
    unique_id = uuid.uuid4().hex[:12]

    # Read uploaded bytes with size validation
    raw_bytes = bytearray()
    chunk_size = 1024 * 1024  # 1 MB

    try:
        while chunk := await file.read(chunk_size):
            raw_bytes.extend(chunk)
            if len(raw_bytes) > config["max_size"]:
                max_mb = config["max_size"] // (1024 * 1024)
                return False, f"File size exceeds maximum allowed limit of {max_mb} MB"
    except Exception as e:
        return False, f"Failed to read file: {str(e)}"
    finally:
        await file.close()

    try:
        if is_image:
            # Compress image to WebP
            compressed_bytes = _compress_image_to_webp(
                bytes(raw_bytes),
                config.get("max_dim", (1920, 1920)),
            )
            final_filename = f"{unique_id}_{clean_name}.webp"
            dest_path = os.path.join(dest_folder, final_filename)
            with open(dest_path, "wb") as f:
                f.write(compressed_bytes)

            file_size = len(compressed_bytes)
            mime_type = "image/webp"
        else:
            final_filename = f"{unique_id}_{clean_name}.{ext}"
            dest_path = os.path.join(dest_folder, final_filename)
            with open(dest_path, "wb") as f:
                f.write(raw_bytes)

            file_size = len(raw_bytes)
            mime_type = file.content_type or f"application/{ext}"

    except Exception as e:
        return False, f"Failed to process and save file: {str(e)}"

    relative_path = f"/uploads/{category_val}/{final_filename}"
    clean_base = base_url.rstrip("/") if base_url else ""
    full_url = f"{clean_base}{relative_path}"

    return True, {
        "file_name": final_filename,
        "file_path": relative_path,
        "file_url": full_url,
        "file_size": file_size,
        "mime_type": mime_type,
    }
