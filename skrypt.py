import os
import shutil
from datetime import datetime
from pathlib import Path
from tqdm import tqdm
import atexit
import time
import sys

# CONFIGURATION
source_dir = r'C:\PATH'
target_dir = r'D:\PATH'

# Add support long path (NTFS long path)
def long_path(path):
    path = os.path.abspath(path)
    if not path.startswith('\\\\?\\'):
        if path.startswith('\\\\'):
            return '\\\\?\\UNC\\' + path[2:]
        return '\\\\?\\' + path
    return path

# Logs
log_file_name = f'log_kopiowania_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt'
log_file_path = Path(target_dir) / log_file_name
log_file = None

# value for stat
total_files_found = 0
total_files_copied = 0
total_source_size = 0
total_copied_size = 0
total_dirs_created = 0
total_errors = 0

# Support for unanticipated closure
def exit_handler():
    global total_files_found, total_files_copied, total_source_size, total_copied_size, total_dirs_created, total_errors
    print("\nSkrypt został zakończony lub przerwany.")

    # Tekst for Support for unanticipated closure
    summary = (
        "\n=== PODSUMOWANIE KOPIOWANIA ===\n"
        f"- Plików w źródle: {total_files_found}\n"
        f"- Plików skopiowanych: {total_files_copied}\n"
        f"- Rozmiar danych w źródle: {total_source_size / (1024 ** 3):.2f} GB\n"
        f"- Rozmiar danych skopiowanych: {total_copied_size / (1024 ** 3):.2f} GB\n"
        f"- Folderów utworzonych: {total_dirs_created}\n"
        f"- Błędów podczas kopiowania: {total_errors}\n"
    )

    if log_file:
        log_file.write(summary)
        log_file.write("Skrypt zakończony.\n")
        log_file.flush()
        log_file.close()

    print(summary)
    print("\nZakończono kopiowanie. Log zapisany w:", log_file_path)

atexit.register(exit_handler)

# MAIN function copy
def copy_files(src, dst):
    global total_files_found, total_files_copied, total_source_size, total_copied_size, total_dirs_created, total_errors, log_file
    src_path = Path(long_path(src))
    dst_path = Path(long_path(dst))

    files_list = []

    # Recursive traversal of the source directory
    for root, dirs, files in os.walk(src_path):
        root_path = Path(root)
        for dir in dirs:
            dir_path = root_path / dir
            files_list.append(dir_path)
        for file in files:
            file_path = root_path / file
            files_list.append(file_path)

    total_files_found = len(files_list)

    try:
        log_file = open(log_file_path, "w", encoding="utf-8")
        log_file.write(f"Rozpoczęto kopiowanie w dniu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        with tqdm(total=total_files_found, desc="Kopiowanie plików", unit="plik", file=sys.stdout, leave=True) as pbar:
            for file_path in files_list:
                relative_path = Path(str(file_path)[len(str(src_path)) + 1:])
                dest_file_path = dst_path / relative_path

                log_file.write(f'Rozpoczynam kopiowanie: {file_path}\n')
                log_file.flush()

                try:
                    if file_path.is_dir():
                        Path(long_path(dest_file_path)).mkdir(parents=True, exist_ok=True)
                        total_dirs_created += 1
                        log_file.write(f'SUKCES: Utworzono folder: {file_path} -> {dest_file_path}\n')
                    else:
                        Path(long_path(dest_file_path.parent)).mkdir(parents=True, exist_ok=True)
                        file_size = os.path.getsize(str(file_path))
                        total_source_size += file_size
                        log_file.write(f'Rozmiar pliku: {file_size / (1024 * 1024):.2f} MB\n')
                        log_file.flush()

                        with open(str(file_path), 'rb') as src_file, open(long_path(str(dest_file_path)), 'wb') as dst_file:
                            total_copied = 0
                            buffer_size = 1024 * 1024  # 1MB
                            last_logged_percent = 0
                            last_log_time = time.time()

                            while True:
                                chunk = src_file.read(buffer_size)
                                if not chunk:
                                    break
                                dst_file.write(chunk)
                                total_copied += len(chunk)

                                progress_percent = (total_copied / file_size) * 100
                                now = time.time()

                                if progress_percent - last_logged_percent >= 5 or (now - last_log_time) >= 30:
                                    msg = f'Postęp kopiowania {file_path.name}: {progress_percent:.2f}% ({total_copied}/{file_size} bajtów)'
                                    tqdm.write(msg)
                                    log_file.write(msg + '\n')
                                    log_file.flush()
                                    last_logged_percent = progress_percent
                                    last_log_time = now

                        total_copied_size += total_copied
                        total_files_copied += 1
                        log_file.write(f'SUKCES: {file_path} -> {dest_file_path}\n')
                        log_file.flush()

                except Exception as e:
                    total_errors += 1
                    log_file.write(f'BŁĄD: {file_path} -> {e}\n')
                    log_file.flush()

                pbar.update(1)

        log_file.write("Kopiowanie zakończone pomyślnie.\n")
        log_file.flush()
    except KeyboardInterrupt:
        # Supports user aborting the script (Ctrl+C)
        print("\nKopiowanie zostało przerwane przez użytkownika.")
        exit_handler()  # Wywołanie exit_handler w przypadku przerwania

    finally:
        if log_file:
            log_file.close()
    exit_handler()
    print(f"\nZakończono kopiowanie. Log zapisany w: {log_file_path}")

# ===== START =====
copy_files(source_dir, target_dir)
