import typer
import shutil
import subprocess
from rich.console import Console

from config.config import settings, ROOT_DIR
from src.utils import get_all_files_path, make_dir, filter_files_from_lang, \
    check_if_has_unziped, has_folder, get_folders_name, get_folders_with_same_name


console = Console()
app = typer.Typer(callback=lambda: console.rule(settings.CLI.extracting_rule), help=settings.TYPER.extractor_help)
target_language = settings.ARGS.target_language
source_language = settings.ARGS.source_language
raw_texts_folder_name = settings.ARGS.raw_texts_folder_name
nier_replicant_path = settings.PATHS.nier_replicant_path
originals_folder_name = settings.ARGS.originals_folder_name


@app.command('extract-assets', help=settings.TYPER.extract_assets_help)
def extract_assets():
    emil_exe = f'{ROOT_DIR}\\tools\\emil-kaine\\emil.exe'
    build_path = f'{nier_replicant_path}\\..\\build_assets\\rom\\pc'

    check_if_has_unziped(emil_exe, 'emil-kaine', f'{ROOT_DIR}\\tools')

    subprocess.run(
        [f'{ROOT_DIR}\\tools\\emil-kaine\\emil.exe', '-i', nier_replicant_path, '-o', build_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        encoding='utf-8'
    )

    return has_folder(build_path)


@app.command('extract-texts', help=settings.TYPER.extract_texts_help)
def extract_texts():
    ntt_exe = f'{ROOT_DIR}\\tools\\text-tool\\ntt.exe'
    texts_path = f'{nier_replicant_path}\\..\\build_assets\\rom\\pc\\snow\\text'

    if has_folder(f'{texts_path}.{originals_folder_name}'):
        texts_path += f'.{originals_folder_name}'

    check_if_has_unziped(ntt_exe, 'text-tool', f'{ROOT_DIR}\\tools')

    for file in get_all_files_path(texts_path):
        file_folder_name = file.split('\\')[-1]
        output_path = f"{ROOT_DIR}\\texts\\{raw_texts_folder_name}\\{file_folder_name}"

        make_dir(output_path)
        subprocess.run(
            [ntt_exe, '-e', file, output_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            encoding='utf-8'
        )

    create_target_language_folder()


def create_target_language_folder():
    texts_path = f'{ROOT_DIR}\\texts'
    target_language_folder = f'{texts_path}\\{target_language}'
    raw_texts_files_path = f'{texts_path}\\{raw_texts_folder_name}'
    files_to_copy = filter_files_from_lang(get_all_files_path(raw_texts_files_path), source_language)

    if has_folder(target_language_folder):
        target_language_folder += f"-{len(get_folders_with_same_name(texts_path, target_language))}"

    make_dir(target_language_folder)

    for file in files_to_copy:
        folder_name = file.split('\\')[-2]
        folder_file = f'{target_language_folder}\\{folder_name}'

        make_dir(folder_file)
        shutil.copy(file, folder_file)
