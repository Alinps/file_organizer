from pathlib import Path
import shutil
import logging

FILE_CATEGORIES = {
    "Documents": {".pdf",".doc",".pptx",".docx",".ppt"},
    "Images":{".jpg",".jpeg",".png",".gif",".svg",".webp",".bmp"},
    "Spreadsheets":{".xls",".xlsx",".csv",".ods"},
    "Text Files":{".txt",".md",".log",".json",".xml"},
    "Programs":{".py",".java",".js",".c",".cpp",".html",".css"}
}


CATEGORIES = [
    "Documents",
    "Images",
    "Spreadsheets",
    "Text Files",
    "Programs",
    "Others"
]


def get_category(file_path:Path) -> str:
    """
    Identify the category of a file based on its extension.

    Args:
        file_path: Path object representing the file.

    Returns:
        The corresponding category name.
    """

    extension = file_path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():

        if extension in extensions:
            
            return category

    return "Others"



def get_folder_path() -> Path | None:

    """
    Get and validate the folder path provided by the user.

    Returns:
        A valid directory Path object, or None if invalid.
    """


    user_input = input("Enter the folder path to organize: ").strip()

    if not user_input:
        print("Error: Folder path cannot be empty.")
        return None
    folder_path = Path(user_input).expanduser()

    if not folder_path.exists():
        print("Error: The specified folder does not exists.")
        return None
    
    if not folder_path.is_dir():
        print("Error: The specified path is no a directory.")
        return None

    return folder_path




def create_category_folders(folder_path: Path) -> dict[str,Path]:
    """
    Create category folders inside the specified directory.

    Existing directories are reused.

    Args:
        folder_path: Root directory where category folders are created.

    Returns:
        Dictionary containing category names and their directory paths.
    """


    category_paths = {}

    for category in CATEGORIES:

        category_path = folder_path/category

        category_path.mkdir(exist_ok=True)

        category_paths[category] = category_path
        
    return category_paths



def get_files(folder_path: Path) -> list[Path]:

    """
    Retrieve all files directly inside the specified directory.

    Subdirectories are excluded.

    Args:
        folder_path: Directory to scan.

    Returns:
        A list containing Path objects for each file.
    """

    files = []

    for item in folder_path.iterdir():

        if item.is_file():
            files.append(item)
    
    return files


def move_file(file_path:Path, category_paths: dict[str, Path]) -> bool:
    """
    Move a file into its corresponding category directory.

    Args:
        file_path: Source file path.
        category_paths: Mapping of categories to destination paths.

    Returns:
        True if the file was moved successfully, otherwise False.
    """

    try:

        category = get_category(file_path)

        destination_folder = category_paths[category]

        destination_path = get_unique_destination(destination_folder, file_path.name)

        shutil.move(str(file_path), str(destination_path))

        logging.info("Moved '%s' to '%s'",file_path.name,category)

        return True

    except PermissionError as error:

        logging.exception(
            "Permission denied while moving '%s'",
            file_path.name
        )

    except FileNotFoundError as error:

        logging.exception(
            "File not found while moving '%s'",
            file_path.name
        )
    
    except OSError as error:

        logging.exception(
            "Unable to move '%s'",
            file_path.name
        )

    return False






def organize_files(
    files: List[Path], 
    category_paths:dict[str, Path]
    ) -> None:

    """
    Organize all files into their respective category directories.


    """

    summary = {
        category: 0
        for category  in CATEGORIES
    }

    logging.info("Starting file organization.")
    logging.info("Total files discovered: %d", len(files))

    for file_path in files:
        
        category = get_category(file_path)

        if move_file(file_path, category_paths):
            summary[category] += 1

    logging.info("File organization completed.")

    return summary  






        




def get_unique_destination(destination_folder: Path, filename: str) -> Path:

    """
    Generate a unique destination path to prevent filename collisions.

    Args:
        destination_folder: Target directory.
        filename: Original filename.

    Returns:
        An available destination path.
    """

    original_path = destination_folder/filename

    if not original_path.exists():
        return original_path

    file_path = Path(filename)

    counter = 1

    while True:

        new_filename = (f"{file_path.stem}_{counter}{file_path.suffix}")

        new_path = destination_folder / new_filename

        if not new_path.exists():
            return new_path


        counter += 1




def display_summary(summary: dict[str,int]) -> None:

    """
    Display the number of successfully moved files per category.
    """

    print("\n" + "=" * 40)
    print("       FILE ORGANIZATION SUMMARY")
    print("=" * 40)

    total_moved = 0

    for category, count in summary.items():

        print(f"{category:<20}: {count}")

        total_moved += count

    print("-" * 40)
    print(f"{'Total files moved':<20}: {total_moved}")
    print("=" * 40)










def main() -> None:
    """
    Main entry point of the File Organizer application.
    """
    configure_logging()

    logging.info("File Organizer application started.")

    folder = get_folder_path()

    if folder is None:
        logging.warning("Invalid folder path provided.")
        return 

    logging.info("Selected directory: %s", folder)

    category_paths = create_category_folders(folder)

    files = get_files(folder)

    if not files:

        logging.warning("No files found in the specified directory.")
        display_summary({category: 0 for category in CATEGORIES})
        return
    
    summary = organize_files(files, category_paths)

    display_summary(summary)

    logging.info("Application execution completed.")






def configure_logging() -> None:

    """
    Configure application logging.

    Logs are written to logs/file_organizer.log.
    """

    log_directory = Path("logs")

    log_directory.mkdir(exist_ok=True)

    log_file = log_directory / "file_organizer.log"

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file,encoding="utf-8"),
            logging.StreamHandler()
        ]
    )


    
if __name__ ==  "__main__":

    main()








    