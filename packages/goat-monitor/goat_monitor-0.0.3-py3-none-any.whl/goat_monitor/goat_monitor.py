# %% imports
import subprocess
import sys
from pathlib import Path
from typing import List

import click
import gotify
import numpy as np
import toml

from goat_monitor._version import __version__


# %% commands
@click.command()
@click.argument("command", nargs=-1, required=False, type=str)
@click.option(
    "--config",
    default="~/.config/goat_monitor.toml",
    type=click.Path(path_type=Path),
    help="Use a .toml configuration file",
)
@click.option(
    "--retries",
    default=0,
    type=int,
    help="Number of times to try re-running failed command. -1 to retry indefinitely until success",
)
@click.option(
    "--version",
    is_flag=True,
    default=False,
    help="Print version and exit",
)
def wrap(command: List[str], config: Path, retries: int, version):
    """Wrap an arbitrary command with gotify notifications"""

    if version:
        print(__version__)
        sys.exit(0)

    # read settings first
    with open(config, "r") as f:
        settings = toml.load(f)

    # gotify configuration
    url = settings["server"]
    app_token = settings["app_token"]
    with gotify.Gotify(base_url=url, app_token=app_token) as gotify_connection:
        # this is just to test configuration.
        # I don't know how long a gotify connection will stay up so rather than thinking about it
        # I'm just creating a new one whenever I need to send a message
        pass

    if retries == -1:
        retries = np.inf
    if retries < 0:
        raise ValueError("Invalid number of retries specified")

    for attempt in range(retries + 1):
        # run the command
        result = subprocess.run(
            " ".join(command),
            shell=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            encoding="utf-8",
        )

        # TODO: print lines real time as the subprocess runs
        print(result.stdout, end="")

        if result.returncode:
            # failed
            title = f"Command failed with exit code {result.returncode}"
            if attempt < retries:
                title += f" - Retrying (attempt {attempt+1}/{retries})"
            else:
                title += " - Aborting"

        else:
            title = "Command succeeded"

        MAX_LINES = 20
        lines = result.stdout.splitlines()
        if len(lines) > MAX_LINES:
            lines = lines[-MAX_LINES:]
        message = (
            "Command:\n"
            + " ".join(command)
            + f'\n\nResult{ " (truncated)" if len(lines) > MAX_LINES else ""}:\n'
            + "\n".join(lines)
        )

        with gotify.Gotify(base_url=url, app_token=app_token) as gotify_connection:
            gotify_connection.create_message(message=message, title=title)

    sys.exit(result.returncode)


# %% main
def main():
    wrap()


if __name__ == "__main__":
    main()
