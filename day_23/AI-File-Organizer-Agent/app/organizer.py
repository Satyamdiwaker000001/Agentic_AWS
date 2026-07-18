from pathlib import Path
import shutil

from app.file_types import FILE_CATEGORIES


def get_category(file_extension: str) -> str:
    file_extension = file_extension.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if file_extension in extensions:
            return category

    return "Others"


def organize_folder(folder_path: str):
    folder = Path(folder_path).expanduser().resolve()

    print(f"\nScanning: {folder}")

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    if not folder.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {folder}")

    moved = 0
    moved_files = []

    for item in sorted(folder.iterdir()):
        if item.is_dir() or item.name.startswith("."):
            continue

        category = get_category(item.suffix)
        destination = folder / category
        destination.mkdir(exist_ok=True)

        target_path = destination / item.name
        if target_path.exists():
            stem = item.stem
            suffix = item.suffix
            counter = 1
            while target_path.exists():
                target_path = destination / f"{stem}_{counter}{suffix}"
                counter += 1

        shutil.move(str(item), str(target_path))
        moved_files.append(f"{item.name} -> {category}")
        print(f"Moved: {item.name} -> {category}")
        moved += 1

    print(f"Total Files Moved: {moved}")
    return moved, moved_files