import logging
import os
import subprocess
import typer

logger = logging.getLogger("otimages." + os.path.basename(__file__))


def run_helm_command(command: str) -> list:
    logger.debug("%s", command)
    result = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    images = result.stdout.splitlines()

    try:
        assert images != []
    except AssertionError:
        for error in result.stderr.splitlines():
            logger.error("%s", error)
        logger.critical("Could not read images from helm -> %s", command)

        raise typer.Exit(code=1)

    return images
