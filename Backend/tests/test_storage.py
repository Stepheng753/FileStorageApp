import pytest
from core.storage import (
    resolve_safe_path,
    format_bytes,
    get_file_category,
    create_folder,
    delete_item,
    get_directory_contents
)
from core.config import STORAGE_DIR


def test_format_bytes():
    assert format_bytes(500) == "500 B"
    assert format_bytes(2048) == "2.0 KB"
    assert format_bytes(1048576 * 5) == "5.0 MB"


def test_file_category():
    assert get_file_category("report.pdf") == "pdf"
    assert get_file_category("image.png") == "image"
    assert get_file_category("spreadsheet.xlsx") == "spreadsheet"
    assert get_file_category("unknown.xyz") == "file"


def test_path_traversal_prevention():
    # Attempting to break out with ../ should raise ValueError
    with pytest.raises(ValueError):
        resolve_safe_path("../../../etc/passwd")

    with pytest.raises(ValueError):
        resolve_safe_path("/etc/shadow")


def test_folder_creation_and_contents():
    folder_info = create_folder("", "Test_Unit_Folder")
    assert folder_info["name"] == "Test_Unit_Folder"

    contents = get_directory_contents("")
    folder_names = [f["name"] for f in contents["folders"]]
    assert "Test_Unit_Folder" in folder_names

    # Clean up
    delete_item("Test_Unit_Folder")
