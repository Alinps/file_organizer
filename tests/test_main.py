
from pathlib import Path

import pytest

from main import (
    CATEGORIES,
    create_category_folders,
    get_category,
    get_files,
    get_unique_destination,
    organize_files,
    move_file,
)


# --------------------------------------------------
# Tests for get_category()
# --------------------------------------------------

def test_get_category_pdf():
    assert get_category(Path("report.pdf")) == "Documents"


def test_get_category_image():
    assert get_category(Path("photo.jpg")) == "Images"


def test_get_category_spreadsheet():
    assert get_category(Path("sales.xlsx")) == "Spreadsheets"


def test_get_category_text_file():
    assert get_category(Path("notes.txt")) == "Text Files"


def test_get_category_program():
    assert get_category(Path("script.py")) == "Programs"


def test_get_category_unknown():
    assert get_category(Path("archive.zip")) == "Others"


def test_get_category_uppercase_extension():
    assert get_category(Path("REPORT.PDF")) == "Documents"


def test_get_category_without_extension():
    assert get_category(Path("README")) == "Others"


# --------------------------------------------------
# Tests for create_category_folders()
# --------------------------------------------------

def test_create_category_folders(tmp_path):
    category_paths = create_category_folders(tmp_path)

    for category in CATEGORIES:
        assert (tmp_path / category).is_dir()
        assert category in category_paths


def test_create_category_folders_reuse_existing(tmp_path):
    existing_folder = tmp_path / "Documents"
    existing_folder.mkdir()

    category_paths = create_category_folders(tmp_path)

    assert existing_folder.is_dir()
    assert category_paths["Documents"] == existing_folder


# --------------------------------------------------
# Tests for get_files()
# --------------------------------------------------

def test_get_files_returns_only_files(tmp_path):
    file_one = tmp_path / "report.pdf"
    file_two = tmp_path / "photo.jpg"
    directory = tmp_path / "Documents"

    file_one.touch()
    file_two.touch()
    directory.mkdir()

    files = get_files(tmp_path)

    assert len(files) == 2
    assert file_one in files
    assert file_two in files
    assert directory not in files


def test_get_files_empty_directory(tmp_path):
    files = get_files(tmp_path)

    assert files == []


# --------------------------------------------------
# Tests for get_unique_destination()
# --------------------------------------------------

def test_unique_destination_without_duplicate(tmp_path):
    destination = get_unique_destination(
        tmp_path,
        "report.pdf"
    )

    assert destination.name == "report.pdf"


def test_unique_destination_with_duplicate(tmp_path):
    (tmp_path / "report.pdf").touch()

    destination = get_unique_destination(
        tmp_path,
        "report.pdf"
    )

    assert destination.name == "report_1.pdf"


def test_unique_destination_multiple_duplicates(tmp_path):
    (tmp_path / "report.pdf").touch()
    (tmp_path / "report_1.pdf").touch()

    destination = get_unique_destination(
        tmp_path,
        "report.pdf"
    )

    assert destination.name == "report_2.pdf"


# --------------------------------------------------
# Tests for move_file()
# --------------------------------------------------

def test_move_file_successfully(tmp_path):
    source_folder = tmp_path / "source"
    destination_folder = tmp_path / "Documents"

    source_folder.mkdir()
    destination_folder.mkdir()

    file_path = source_folder / "report.pdf"
    file_path.write_text("Sample PDF content")

    category_paths = {
        "Documents": destination_folder
    }

    result = move_file(file_path, category_paths)

    assert result is True
    assert not file_path.exists()
    assert (destination_folder / "report.pdf").exists()


def test_move_file_handles_duplicate_filename(tmp_path):
    source_folder = tmp_path / "source"
    destination_folder = tmp_path / "Documents"

    source_folder.mkdir()
    destination_folder.mkdir()

    file_path = source_folder / "report.pdf"
    file_path.write_text("New report")

    (destination_folder / "report.pdf").write_text(
        "Existing report"
    )

    category_paths = {
        "Documents": destination_folder
    }

    result = move_file(file_path, category_paths)

    assert result is True
    assert not file_path.exists()
    assert (destination_folder / "report.pdf").read_text() == (
        "Existing report"
    )
    assert (destination_folder / "report_1.pdf").read_text() == (
        "New report"
    )


# --------------------------------------------------
# Tests for organize_files()
# --------------------------------------------------

def test_organize_files_summary(tmp_path):
    source_folder = tmp_path / "source"
    source_folder.mkdir()

    files_to_create = [
        "report.pdf",
        "photo.jpg",
        "sales.xlsx",
        "notes.txt",
        "script.py",
        "archive.zip",
    ]

    for filename in files_to_create:
        (source_folder / filename).touch()

    category_paths = create_category_folders(tmp_path)

    files = get_files(source_folder)

    summary = organize_files(files, category_paths)

    assert summary["Documents"] == 1
    assert summary["Images"] == 1
    assert summary["Spreadsheets"] == 1
    assert summary["Text Files"] == 1
    assert summary["Programs"] == 1
    assert summary["Others"] == 1

    assert sum(summary.values()) == 6
