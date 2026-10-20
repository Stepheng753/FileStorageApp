import os
import shutil
from datetime import datetime
from pathlib import Path
from core.config import STORAGE_DIR

# Document and media formats that may be uploaded
ALLOWED_EXTENSIONS = {"pdf", "docx", "doc", "xlsx", "xls", "pptx", "ppt", "png", "jpg", "jpeg", "txt", "csv"}

# Executable, script and system extensions. Checked against every dot-separated
# suffix so names such as "report.php.pdf" are also refused.
BLOCKED_EXTENSIONS = {
    "sh", "bash", "zsh", "py", "pyc", "elf", "bin", "exe", "dll", "so", "msi", "bat", "cmd",
    "ps1", "vbs", "com", "scr", "jar", "php", "phtml", "cgi", "pl", "rb", "js", "mjs",
    "service", "timer", "cron", "sys",
}

# Leading magic bytes expected for each binary format. Text formats are checked for NUL bytes instead.
MAGIC_SIGNATURES = {
    "pdf": (b"%PDF-",),
    "png": (b"\x89PNG\r\n\x1a\n",),
    "jpg": (b"\xff\xd8\xff",),
    "jpeg": (b"\xff\xd8\xff",),
    # OOXML containers are ZIP archives
    "docx": (b"PK\x03\x04",),
    "xlsx": (b"PK\x03\x04",),
    "pptx": (b"PK\x03\x04",),
    # Legacy Office documents use OLE2 compound files
    "doc": (b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1",),
    "xls": (b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1",),
    "ppt": (b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1",),
}
TEXT_EXTENSIONS = {"txt", "csv"}

# Extension category mapping for frontend icons and previews
CATEGORY_MAP = {
    # Documents
    "pdf": "pdf",
    "doc": "document",
    "docx": "document",
    "txt": "document",
    "rtf": "document",
    "odt": "document",
    # Spreadsheets
    "xls": "spreadsheet",
    "xlsx": "spreadsheet",
    "csv": "spreadsheet",
    # Images
    "png": "image",
    "jpg": "image",
    "jpeg": "image",
    "gif": "image",
    "svg": "image",
    "webp": "image",
    # Videos
    "mp4": "video",
    "mov": "video",
    "webm": "video",
    "mkv": "video",
    # Audio
    "mp3": "audio",
    "wav": "audio",
    "m4a": "audio",
}


def format_bytes(size: int) -> str:
    """Format bytes into human-readable string (KB, MB, GB)."""
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    elif size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} MB"
    else:
        return f"{size / (1024 * 1024 * 1024):.2f} GB"


def get_file_category(filename: str) -> str:
    """Get file category based on extension."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return CATEGORY_MAP.get(ext, "file")


def resolve_safe_path(relative_path: str) -> Path:
    """
    Resolve a user-provided relative path against STORAGE_DIR.
    Ensures that the resolved path is strictly contained within STORAGE_DIR.
    Raises ValueError if path traversal or absolute path is detected.
    """
    raw = relative_path.strip()
    if not raw:
        return STORAGE_DIR.resolve()

    if raw.startswith("/") or raw.startswith("\\") or os.path.isabs(raw):
        raise ValueError("Absolute paths are not permitted")

    # Check for parent traversal in path parts
    parts = Path(raw).parts
    if ".." in parts:
        raise ValueError("Parent directory traversal (..) is not permitted")

    target = (STORAGE_DIR / raw).resolve()
    storage_root = STORAGE_DIR.resolve()

    try:
        common = Path(os.path.commonpath([target, storage_root]))
        if common != storage_root:
            raise ValueError("Path traversal attempt detected")
    except Exception as e:
        raise ValueError(f"Invalid path: {e}")

    return target



def clean_relative_path(raw: str) -> str:
    """
    Normalise a user-supplied relative path before it reaches the filesystem.
    Removes null bytes, leading/trailing slashes and '.'/'..' navigation segments.
    Names are otherwise left exactly as the user supplied them.
    """
    raw = str(raw or "").replace("\x00", "").strip().replace("\\", "/")
    parts = [p for p in raw.split("/") if p not in ("", ".", "..")]
    return "/".join(parts)


def validate_upload_filename(raw_name: str) -> str:
    """
    Check an uploaded file name against the extension policy and return it unchanged.
    The name is only trimmed to its final path component to remove directory parts.
    """
    name = (raw_name or "").replace("\x00", "").replace("\\", "/").rsplit("/", 1)[-1]
    if not name or name in (".", ".."):
        raise ValueError("Invalid file name")
    if name.startswith("."):
        raise ValueError("Dotfiles cannot be uploaded")

    suffixes = [s.lower() for s in name.split(".")[1:]]
    if any(s in BLOCKED_EXTENSIONS for s in suffixes):
        raise ValueError("Executable and script files cannot be uploaded")

    ext = suffixes[-1] if suffixes else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"File type '.{ext}' is not permitted")
    return name


def validate_upload_content(file_storage, ext: str) -> None:
    """
    Verify the file's leading bytes match its extension, then rewind the stream.
    Text formats must not contain NUL bytes.
    """
    stream = file_storage.stream
    stream.seek(0)
    try:
        if ext in TEXT_EXTENSIONS:
            while chunk := stream.read(64 * 1024):
                if b"\x00" in chunk:
                    raise ValueError(f"File content does not match its '.{ext}' type")
            return

        signatures = MAGIC_SIGNATURES.get(ext)
        if signatures is None:
            raise ValueError(f"File type '.{ext}' is not permitted")
        head = stream.read(8)
        if not any(head.startswith(sig) for sig in signatures):
            raise ValueError(f"File content does not match its '.{ext}' type")
    finally:
        stream.seek(0)


def _make_dirs_secure(path: Path) -> None:
    """Create a directory and any missing parents, setting 0o755 on each new directory."""
    missing = []
    current = path
    while not current.exists():
        missing.append(current)
        current = current.parent
    for directory in reversed(missing):
        try:
            directory.mkdir()
        except FileExistsError:
            continue  # created concurrently by another request
        os.chmod(directory, 0o755)
    if not path.is_dir():
        raise ValueError("Path exists and is not a folder")


def create_folder(parent_path: str, folder_name: str) -> dict:
    """Create a new folder safely inside STORAGE_DIR."""
    clean_parent = clean_relative_path(parent_path)
    clean_name = (folder_name or "").replace("\x00", "").strip()

    # Replace path separators to prevent arbitrary sub-path injection in folder_name
    safe_folder_name = clean_name.replace("/", "_").replace("\\", "_")
    if not safe_folder_name or safe_folder_name in (".", "..") or safe_folder_name.startswith("."):
        raise ValueError("Invalid folder name")

    rel = os.path.join(clean_parent, safe_folder_name) if clean_parent else safe_folder_name
    target_dir = resolve_safe_path(rel)
    _make_dirs_secure(target_dir)

    rel_path = os.path.relpath(target_dir, STORAGE_DIR)
    return {
        "name": safe_folder_name,
        "path": "" if rel_path == "." else rel_path,
        "is_dir": True,
        "item_count": 0
    }


def save_uploaded_file(target_folder: str, file_storage) -> dict:
    """Validate and save an uploaded file safely into target_folder inside STORAGE_DIR."""
    clean_folder = clean_relative_path(target_folder)

    # Validate the name and content before any directory is created or file written
    safe_name = validate_upload_filename(file_storage.filename)
    ext = safe_name.rsplit(".", 1)[-1].lower()
    validate_upload_content(file_storage, ext)

    folder_path = resolve_safe_path(clean_folder)
    _make_dirs_secure(folder_path)

    # Resolve the final destination and confine it to STORAGE_DIR (also catches symlink escapes)
    dest_file = resolve_safe_path(os.path.join(clean_folder, safe_name) if clean_folder else safe_name)
    file_storage.save(str(dest_file))
    os.chmod(dest_file, 0o644)

    stat = dest_file.stat()
    rel_path = os.path.relpath(dest_file, STORAGE_DIR)
    return {
        "name": safe_name,
        "path": rel_path,
        "is_dir": False,
        "size_bytes": stat.st_size,
        "formatted_size": format_bytes(stat.st_size),
        "category": get_file_category(safe_name),
        "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
    }


def delete_item(relative_path: str) -> bool:
    """Safely delete a file or folder inside STORAGE_DIR."""
    target = resolve_safe_path(relative_path)
    storage_root = STORAGE_DIR.resolve()

    # Never delete the root storage directory
    if target == storage_root:
        raise ValueError("Cannot delete storage root directory")

    if not target.exists():
        raise FileNotFoundError("Target file or folder not found")

    if target.is_dir():
        shutil.rmtree(str(target))
    else:
        target.unlink()

    return True


def get_directory_contents(relative_path: str = "") -> dict:
    """
    Get items in a specific directory inside STORAGE_DIR with rich metadata.
    Returns:
    {
        "current_folder": relative_path,
        "parent_folder": parent_path,
        "breadcrumbs": [{"name": ..., "path": ...}],
        "folders": [...],
        "files": [...]
    }
    """
    target = resolve_safe_path(relative_path)
    if not target.exists() or not target.is_dir():
        raise FileNotFoundError(f"Folder '{relative_path}' not found")

    rel_current = "" if target == STORAGE_DIR.resolve() else os.path.relpath(target, STORAGE_DIR)
    parent_rel = ""
    if rel_current:
        parent_target = target.parent
        parent_rel = "" if parent_target == STORAGE_DIR.resolve() else os.path.relpath(parent_target, STORAGE_DIR)

    # Build breadcrumb list
    breadcrumbs = [{"name": "Home", "path": ""}]
    if rel_current:
        parts = Path(rel_current).parts
        accum = []
        for part in parts:
            accum.append(part)
            breadcrumbs.append({"name": part, "path": "/".join(accum)})

    folders = []
    files = []

    for entry in os.scandir(target):
        if entry.name.startswith("."):
            continue

        item_rel = os.path.relpath(entry.path, STORAGE_DIR)
        try:
            stat = entry.stat()
            modified = datetime.fromtimestamp(stat.st_mtime).isoformat()
        except Exception:
            modified = None

        if entry.is_dir():
            # Count items inside folder
            try:
                item_count = len([f for f in os.scandir(entry.path) if not f.name.startswith(".")])
            except Exception:
                item_count = 0

            folders.append({
                "name": entry.name,
                "path": item_rel,
                "is_dir": True,
                "item_count": item_count,
                "modified_at": modified
            })
        elif entry.is_file():
            size = stat.st_size if stat else 0
            files.append({
                "name": entry.name,
                "path": item_rel,
                "is_dir": False,
                "size_bytes": size,
                "formatted_size": format_bytes(size),
                "category": get_file_category(entry.name),
                "modified_at": modified
            })

    # Sort folders alphabetically, files alphabetically
    folders.sort(key=lambda x: x["name"].lower())
    files.sort(key=lambda x: x["name"].lower())

    return {
        "current_folder": rel_current,
        "parent_folder": parent_rel,
        "breadcrumbs": breadcrumbs,
        "folders": folders,
        "files": files,
        "total_items": len(folders) + len(files)
    }


def get_full_folder_tree(path=None) -> dict:
    """
    Recursively builds a tree dictionary for backward compatibility with legacy endpoints:
    { "folder_name": { "subfolder": {...}, "files": ["file1", "file2"] } }
    """
    if path is None:
        path = STORAGE_DIR

    folder_dict = {}
    try:
        for entry in os.scandir(path):
            if entry.name.startswith("."):
                continue
            if entry.is_dir():
                folder_dict[entry.name] = get_full_folder_tree(entry.path)
            elif entry.is_file():
                folder_dict.setdefault("files", []).append(entry.name)
    except Exception:
        pass

    return folder_dict
 
 
def get_all_folders_list(base_path=None) -> list:
    """
    Recursively get all directories in STORAGE_DIR as a flat list with clean display names.
    Returns: [{"path": "", "name": "🏠 / (Root)"}, {"path": "401k ADP", "name": "📁 401k ADP"}, ...]
    """
    if base_path is None:
        base_path = STORAGE_DIR

    results = []
    try:
        for entry in os.scandir(base_path):
            if entry.name.startswith("."):
                continue
            if entry.is_dir():
                rel = os.path.relpath(entry.path, STORAGE_DIR)
                display_parts = Path(rel).parts
                display_name = " / ".join(display_parts)
                results.append({
                    "path": rel,
                    "name": f"📁 {display_name}"
                })
                # Recurse into subdirectories
                results.extend(get_all_folders_list(entry.path))
    except Exception:
        pass

    if base_path == STORAGE_DIR:
        results.sort(key=lambda x: x["path"].lower())
        return [{"path": "", "name": "🏠 / (Root)"}] + results
    return results
