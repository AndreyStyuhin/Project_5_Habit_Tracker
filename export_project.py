import os


# Имя файла, куда всё выгружается
OUTPUT_FILE = "project_dump.txt"

# Папки, которые нужно игнорировать
EXCLUDE_DIRS = {"venv", ".git", "__pycache__", ".idea", ".mypy_cache", ".pytest_cache"}

# Расширения файлов, которые включаем
INCLUDE_EXTENSIONS = (".py", ".html", ".css", ".js", ".json", ".txt", ".md", ".example", ".ini", ".txt")


def should_include(file_path):
    return file_path.endswith(INCLUDE_EXTENSIONS)


def export_project(root_dir="."):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        for root, dirs, files in os.walk(root_dir):
            # Убираем ненужные папки
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                if should_include(file):
                    file_path = os.path.join(root, file)
                    outfile.write(f"\n\n=== {file_path} ===\n\n")
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                            outfile.write(infile.read())
                    except Exception as e:
                        outfile.write(f"[Ошибка чтения файла: {e}]")

    print(f"✅ Все файлы выгружены в: {OUTPUT_FILE}")


if __name__ == "__main__":
    export_project()
