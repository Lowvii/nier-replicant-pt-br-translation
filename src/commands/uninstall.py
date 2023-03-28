import typer
from rich.console import Console

from config import settings
from src.utils import remove, rename


console = Console()
app = typer.Typer(help=settings.TYPER.uninstall_help)
nier_replicant_path = settings.PATHS.nier_replicant_path
target_language = settings.ARGS.target_language
originals_folder_name = settings.ARGS.originals_folder_name


@app.command('uninstall', help=settings.TYPER.uninstall_help)
def uninstall_command():
    console.rule(settings.CLI.uninstalling_rule)

    with console.status(settings.CLI.uninstalling_status, spinner='moon'):
        uninstall()


def uninstall():
    try:
        build_path = f'{nier_replicant_path}\\..\\build_assets'

        try:
            remove(build_path)
        except ValueError:
            console.print(
                settings.CLI.uninstall_error_delete.replace('build_path_var', build_path)
            )

        try:
            rename(f'{nier_replicant_path}\\data.{originals_folder_name}', f'{nier_replicant_path}\\data')
        except ValueError:
            console.print(
                settings.CLI.uninstall_error_rename.replace('<name>', f'data.{originals_folder_name}')
            )

        console.print(settings.CLI.uninstall_finish)
        console.print(settings.CLI.thanks, justify='center')
    except Exception:
        console.print(settings.CLI.uninstall_failed)
        console.print_exception(show_locals=True)