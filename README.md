# Python File Organizer

A Python-based file organization utility that automatically organizes files into separate directories based on their file extensions. It helps maintain a clean folder structure by categorizing documents, images, spreadsheets, text files, programs, and other files.

## Features

- **Automatic File Detection:** Scans the specified directory and identifies files.
- **Extension-Based Classification:** Categorizes files based on their extensions.
- **Automatic Directory Creation:** Creates category folders if they don't already exist.
- **File Movement:** Moves files into their corresponding category directories.
- **Duplicate Filename Handling:** Prevents accidental overwriting by generating unique filenames.
- **Exception Handling:** Handles file movement failures and continues processing remaining files.
- **Logging:** Records application activities and errors in a log file.
- **Summary Report:** Displays the number of successfully moved files in each category.
- **Input Validation:** Validates the directory path provided by the user.

## File Categories

| Category | Supported Extensions |
|---|---|
| Documents | `.pdf`, `.doc`, `.docx`, `.ppt`, `.pptx` |
| Images | `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg` |
| Spreadsheets | `.xls`, `.xlsx`, `.csv`, `.ods` |
| Text Files | `.txt`, `.md`, `.log` |
| Programs | `.py`, `.js`, `.java`, `.c`, `.cpp`, `.html`, `.css` |
| Others | All remaining file extensions |

## Technologies Used

- Python 3.10+
- pathlib
- shutil
- logging
- pytest

## Project Structure

```text
python-file-organizer/
│
├── main.py
│
├── tests/
│   ├── __init__.py
│   └── test_main.py
│
├── logs/
│   └── file_organizer.log
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
```

### 2. Navigate to the project directory

```bash
cd python-file-organizer
```

### 3. Create a virtual environment

```bash
python3 -m venv venv
```

### 4. Activate the virtual environment

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run the application using:

```bash
python main.py
```

The application prompts the user to enter the directory path.

```text
Enter the folder path to organise: /home/user/Downloads
```

The program scans the directory, creates the required category folders, identifies file extensions, and moves files into their respective folders.

## Example Output

```text
============================================================
              FILE ORGANIZATION SUMMARY
============================================================

Documents           : 5
Images              : 8
Spreadsheets        : 3
Text Files          : 4
Programs            : 2
Others              : 3

------------------------------------------------------------
Total files moved   : 25
============================================================
```

*The output above is illustrative.*

## Duplicate File Handling

The application prevents files with identical names from accidentally overwriting existing files.

For example, if `report.pdf` already exists in the destination directory, the application generates a unique filename.

```text
Documents/
│
├── report.pdf
├── report_1.pdf
├── report_2.pdf
└── report_3.pdf
```

The original file extension is preserved.

## Logging

Application activities and errors are recorded in:

```text
logs/file_organizer.log
```

The logging system records:

- Application startup and completion.
- Selected directory.
- File movement operations.
- Failed file movements.
- Filesystem errors.

## Testing

The project uses pytest for automated testing.

Run all tests:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_main.py -v
```

## Design Principles

The application follows these software development practices:

- **PEP 8:** Python coding style conventions.
- **Single Responsibility Principle:** Functions are designed to perform specific tasks.
- **DRY Principle:** Avoids unnecessary code duplication.
- **Type Hints:** Improves code readability and maintainability.
- **Docstrings:** Documents function responsibilities.
- **Exception Handling:** Handles filesystem errors gracefully.
- **Modular Design:** Separates file classification, file operations, and application execution.

## Limitations

- The application scans only the specified directory's immediate contents, not nested subdirectories.
- Files are moved rather than copied.
- File classification is based on extensions.
- The application requires appropriate filesystem permissions to move files.

## Future Enhancements

- Recursive directory scanning.
- User-configurable file categories.
- File movement preview before execution.
- GUI using Tkinter or PyQt.
- Configurable logging and log rotation.
- Detailed success and failure reports.
- Atomic collision protection for concurrent operations.

## License

This project is intended for educational purposes and personal use.
