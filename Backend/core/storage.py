import os
import shutil
from datetime import datetime
from pathlib import Path
from werkzeug.utils import secure_filename
from core.config import STORAGE_DIR

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



def create_folder(parent_path: str, folder_name: str) -> dict:
    """Create a new folder safely inside STORAGE_DIR."""
    safe_folder_name = secure_filename(folder_name.strip()) or folder_name.strip().replace("/", "_").replace("\\", "_")
    if not safe_folder_name:
        raise ValueError("Invalid folder name")

    target_dir = resolve_safe_path(os.path.join(parent_path, safe_folder_name))
    target_dir.mkdir(parents=True, exist_ok=True)

    rel_path = os.path.relpath(target_dir, STORAGE_DIR)
    return {
        "name": safe_folder_name,
        "path": "" if rel_path == "." else rel_path,
        "is_dir": True,
        "item_count": 0
    }


def save_uploaded_file(target_folder: str, file_storage) -> dict:
    """Save an uploaded file safely into target_folder inside STORAGE_DIR."""
    folder_path = resolve_safe_path(target_folder)
    folder_path.mkdir(parents=True, exist_ok=True)

    original_filename = file_storage.filename or "uploaded_file"
    # Keep filename readable while removing unsafe characters
    base_name = os.path.basename(original_filename).replace("\x00", "")
    safe_name = secure_filename(base_name)
    if not safe_name:
        safe_name = "file_" + str(int(datetime.now().timestamp()))

    dest_file = folder_path / safe_name
    file_storage.save(str(dest_file))

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
