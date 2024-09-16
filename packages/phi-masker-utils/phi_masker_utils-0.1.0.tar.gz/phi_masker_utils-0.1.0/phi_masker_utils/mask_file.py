"""Mask PHI values in a delimited file or an Excel worksheet."""
import click
import logging
import os
import pathlib
import sys
import yaml

from rich.console import Console

from phi_masker_utils import constants
from phi_masker_utils.console_helper import print_green, print_red, print_yellow
from phi_masker_utils.file_utils import check_infile_status

from phi_masker_utils.masker import Masker


DEFAULT_OUTDIR = os.path.join(
    constants.DEFAULT_OUTDIR_BASE,
    os.path.basename(__file__).replace(".py", ""),
    constants.DEFAULT_TIMESTAMP,
)

console = Console()


def validate_verbose(ctx, param, value):
    """Validate the validate option.

    Args:
        ctx (Context): The click context.
        param (str): The parameter.
        value (bool): The value.

    Returns:
        bool: The value.
    """

    if value is None:
        click.secho(
            "--verbose was not specified and therefore was set to 'True'", fg="yellow"
        )
        return constants.DEFAULT_VERBOSE
    return value


@click.command()  # type: ignore
@click.option(
    "--config_file",
    type=click.Path(exists=True),
    help=f"Optional: The configuration file for this project - default is '{constants.DEFAULT_CONFIG_FILE}'.",
)  # type: ignore
@click.option(
    "--infile",
    help="Required: The input file to be processed.",
)  # type: ignore
@click.option("--logfile", help="Optional: The log file.")  # type: ignore
@click.option(
    "--outdir",
    help=f"Optional: The default is the current working directory - default is '{DEFAULT_OUTDIR}'.",
)  # type: ignore
@click.option("--outfile", help="Optional: The output file that will have all PHI values masked.")  # type: ignore
@click.option(
    "--verbose",
    is_flag=True,
    help=f"Will print more info to STDOUT - default is '{constants.DEFAULT_VERBOSE}'.",
    callback=validate_verbose,
)  # type: ignore
def main(
    config_file: str,
    infile: str,
    logfile: str,
    outdir: str,
    outfile: str,
    verbose: bool,
) -> None:
    """Mask PHI values in a delimited file or an Excel worksheet."""
    error_ctr = 0

    if infile is None:
        print_red("--infile was not specified")
        error_ctr += 1

    if error_ctr > 0:
        sys.exit(1)

    check_infile_status(infile)

    infile = os.path.abspath(infile)

    if config_file is None:
        config_file = constants.DEFAULT_CONFIG_FILE
        print_yellow(
            f"--config_file was not specified and therefore was set to '{config_file}'"
        )

    check_infile_status(config_file, extension="yaml")

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        print_yellow(f"--outdir was not specified and therefore was set to '{outdir}'")

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)

        print_yellow(f"Created output directory '{outdir}'")

    if logfile is None:
        logfile = os.path.join(
            outdir, os.path.splitext(os.path.basename(__file__))[0] + ".log"
        )
        print_yellow(
            f"--logfile was not specified and therefore was set to '{logfile}'"
        )

    if outfile is None:
        basename = os.path.splitext(os.path.basename(infile))[0]
        extension = os.path.splitext(infile)[1]
        outfile = os.path.join(
            outdir,
            f"{basename}{extension}"
        )
        if infile == outfile:
            outfile = os.path.join(
                outdir,
                f"{basename}_masked{extension}"
            )
        print_yellow(
            f"--outfile was not specified and therefore was set to '{outfile}'"
        )

    logging.basicConfig(
        format=constants.DEFAULT_LOGGING_FORMAT,
        level=constants.DEFAULT_LOGGING_LEVEL,
        filename=logfile,
    )

    logging.info(f"Will load contents of config file '{config_file}'")
    config = yaml.safe_load(pathlib.Path(config_file).read_text())

    masker = Masker(
        config=config,
        config_file=config_file,
        infile=infile,
        logfile=logfile,
        outdir=outdir,
        outfile=outfile,
        verbose=verbose,
    )

    masker.mask_phi_values()

    if verbose:
        print_yellow(f"The log file is '{logfile}'")
        print_green(f"Execution of '{os.path.abspath(__file__)}' completed")


if __name__ == "__main__":
    main()
