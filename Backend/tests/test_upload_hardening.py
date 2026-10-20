import io
import os
import stat

import pytest
from werkzeug.datastructures import FileStorage

import core.storage as storage
from core.storage import (
    clean_relative_path,
    create_folder,
    resolve_safe_path,
    save_uploaded_file,
    validate_upload_filename,
)


@pytest.fixture
def root(tmp_path, monkeypatch):
    """Point storage at an isolated temporary directory."""
    storage_root = tmp_path / "static"
    storage_root.mkdir()
    monkeypatch.setattr(storage, "STORAGE_DIR", storage_root)
    return storage_root


def upload(name, data):
    return FileStorage(stream=io.BytesIO(data), filename=name)


PDF = b"%PDF-1.7\n%test\n"
PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 16


def test_clean_relative_path_strips_traversal_without_renaming():
    assert clean_relative_path("../../etc/passwd") == "etc/passwd"
    assert clean_relative_path("/abs/path") == "abs/path"
    assert clean_relative_path("a\\..\\b") == "a/b"
    assert clean_relative_path("Dr. Smith\x00/ X-Rays") == "Dr. Smith/ X-Rays"


def test_resolve_safe_path_rejects_escape():
    with pytest.raises(ValueError):
        resolve_safe_path("../outside")


def test_resolve_safe_path_rejects_symlink_escape(root, tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    (root / "link").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError):
        save_uploaded_file("link", upload("x.pdf", PDF))
    assert not (outside / "x.pdf").exists()


def test_upload_preserves_original_name(root):
    name = "Smith, John - X-Ray 2024 (final).PDF"
    info = save_uploaded_file("", upload(name, PDF))
    assert info["name"] == name
    assert (root / name).read_bytes() == PDF


@pytest.mark.parametrize("name", [
    "shell.sh", "payload.exe", "x.py", "x.elf", "x.bin", "x.php", "x.js",
    "x.so", "x.service", "x.timer", "x.cron", "report.php.pdf", "noextension",
    ".bashrc", ".htaccess", "..", "",
])
def test_rejects_blocked_and_unlisted_names(name):
    with pytest.raises(ValueError):
        validate_upload_filename(name)


def test_strips_directory_part_of_upload_name():
    assert validate_upload_filename("C:\\Users\\me\\scan.png") == "scan.png"
    assert validate_upload_filename("../../scan.png") == "scan.png"


def test_rejects_magic_byte_mismatch(root):
    with pytest.raises(ValueError):
        save_uploaded_file("", upload("fake.pdf", PNG))
    assert not (root / "fake.pdf").exists()


def test_rejects_nul_bytes_in_text(root):
    with pytest.raises(ValueError):
        save_uploaded_file("", upload("notes.txt", b"hello\x00world"))


def test_accepts_plain_text_and_csv(root):
    save_uploaded_file("", upload("notes.txt", b"hello world"))
    save_uploaded_file("", upload("data.csv", b"a,b\n1,2\n"))
    assert (root / "notes.txt").exists()
    assert (root / "data.csv").exists()


def test_uploaded_file_is_mode_0644(root):
    save_uploaded_file("", upload("scan.png", PNG))
    mode = stat.S_IMODE(os.stat(root / "scan.png").st_mode)
    assert mode == 0o644


def test_new_subdirectories_are_mode_0755(root):
    save_uploaded_file("Clinic/2026", upload("scan.png", PNG))
    for d in (root / "Clinic", root / "Clinic" / "2026"):
        assert stat.S_IMODE(os.stat(d).st_mode) == 0o755


def test_rejected_upload_does_not_create_folders(root):
    with pytest.raises(ValueError):
        save_uploaded_file("NewFolder", upload("bad.exe", b"MZ"))
    assert not (root / "NewFolder").exists()


def test_create_folder_rejects_dot_names(root):
    for name in (".hidden", ".", ".."):
        with pytest.raises(ValueError):
            create_folder("", name)


def test_create_folder_sets_0755(root):
    create_folder("", "Patients")
    assert stat.S_IMODE(os.stat(root / "Patients").st_mode) == 0o755
