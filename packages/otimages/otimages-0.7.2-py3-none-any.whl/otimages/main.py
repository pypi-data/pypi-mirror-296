import logging
from enum import Enum

import sys
import os
import typer
from docker import DockerClient
from rich import print
from typing_extensions import Annotated
from .utils import (
    AppworksImages,
    xECMImages,
    xECMMonImages,
    CSAIImages,
    AppworksGatewayImages,
)


logger = logging.getLogger("otimages")


class TyperLoggerHandler(logging.Handler):

    def emit(self, record: logging.LogRecord) -> None:
        fg = None
        bg = None
        if record.levelno == logging.DEBUG:
            fg = typer.colors.BLACK
        elif record.levelno == logging.INFO:
            fg = typer.colors.BRIGHT_BLUE
        elif record.levelno == logging.WARNING:
            fg = typer.colors.BRIGHT_MAGENTA
        elif record.levelno == logging.CRITICAL:
            fg = typer.colors.BRIGHT_RED
        elif record.levelno == logging.ERROR:
            fg = typer.colors.BLACK
            bg = typer.colors.RED
        typer.secho(self.format(record), bg=bg, fg=fg)


class HelmChart(str, Enum):
    otxecm = "otxecm"
    xecmmon = "xecm-mon"
    cmo = "cmo"
    otawp = "otawp"
    appworks = "appworks"
    csai = "csai"
    otag = "otag"


app = typer.Typer()

try:
    docker_client = DockerClient(base_url=os.getenv("DOCKER_HOST", None))
except Exception as exc:
    logger.error("Cannot connect to Docker Engine")
    sys.exit()

option_version = Annotated[
    str,
    typer.Option("--version", "-v", prompt=True, help="Version of the Helm Chart"),
]
option_chart = Annotated[
    HelmChart,
    typer.Option("--chart", "-c", case_sensitive=False, help="Which HelmChart to use"),
]
option_langpacks = Annotated[
    bool,
    typer.Option(
        "--langpacks", help="Include all available LanguagePack initContainers"
    ),
]
option_latest = Annotated[
    bool,
    typer.Option("--latest", help="Latest or by default Released images + HelmChart"),
]
option_confirm = Annotated[
    bool,
    typer.Option("--confirm", "-y", help="Assume all answers are yes"),
]
option_include = Annotated[
    str,
    typer.Option("--include", help="Include only images matching this filter"),
]
option_exclude = Annotated[
    str,
    typer.Option("--exclude", help="Exclude all images matchting this filter"),
]

option_debug = Annotated[
    bool,
    typer.Option(
        "--debug",
        "-d",
        help="Enable global DEBUG logging, must be put before command: 'otimages --debug list -c otxecm'",
    ),
]


@app.callback()
def debug_log(verbose: option_debug = False):
    lvl = logging.WARNING
    fmt = "%(message)s"
    if verbose:
        lvl = logging.DEBUG

    typer_handler = TyperLoggerHandler()

    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
        level=lvl,
        handlers=(typer_handler,),
    )


@app.command(name="list")
def list_images(
    version: option_version = "24.3.0",
    chart: option_chart = HelmChart.otxecm,
    langpacks: option_langpacks = False,
    latest: option_latest = False,
    include: option_include = None,
    exclude: option_exclude = None,
):
    match chart.value:
        case "otxecm":
            images = xECMImages(
                version=version,
                latest=latest,
                langpacks=langpacks,
                docker_client=docker_client,
            )

        case "xecm-mon" | "cmo":
            images = xECMMonImages(
                version=version, latest=latest, docker_client=docker_client
            )

        case "appworks" | "otawp":
            images = AppworksImages(version=version, docker_client=docker_client)

        case "csai":
            images = CSAIImages(
                version=version, latest=latest, docker_client=docker_client
            )

        case "otag":
            images = AppworksGatewayImages(
                version=version, latest=latest, docker_client=docker_client
            )

    if include:
        images.include(include)

    if exclude:
        images.exclude(exclude)

    images.list()

    return images


@app.command()
def pull(
    chart: option_chart = "otxecm",
    version: option_version = "24.3.0",
    langpacks: option_langpacks = False,
    latest: option_latest = False,
    confirm: option_confirm = False,
    include: option_include = None,
    exclude: option_exclude = None,
):
    # List images
    images = list_images(
        version=version,
        chart=chart,
        langpacks=langpacks,
        latest=latest,
        include=include,
        exclude=exclude,
    )

    # Ask for confirmation if not preconfrimed
    if not confirm:
        confirm = typer.confirm("Are you sure you want to pull?")
        if not confirm:
            raise typer.Abort()

    images.pull()


@app.command()
def push(
    chart: option_chart = HelmChart.otxecm,
    version: option_version = "24.3.0",
    repository: Annotated[
        str,
        typer.Option(
            "--repository",
            "-r",
            prompt=True,
            help="repository where the images will be pushed to",
        ),
    ] = "terrarium.azurecr.io",
    path: Annotated[
        str, typer.Option("-p", "--path", help="Root Path of the target repository")
    ] = "",
    langpacks: option_langpacks = False,
    latest: option_latest = False,
    confirm: option_confirm = False,
    include: option_include = None,
    exclude: option_exclude = None,
):
    # List images
    images = list_images(
        version=version,
        chart=chart,
        langpacks=langpacks,
        latest=latest,
        include=include,
        exclude=exclude,
    )

    print()
    print("Push Images to repository:")
    for image in images.images:
        print(image.targetPath(repository=repository, path=path))

    # Ask for confirmation if not preconfrimed
    if not confirm:
        confirm = typer.confirm(
            f"Are you sure you want to push to {repository}/{path}?"
        )
        if not confirm:
            raise typer.Abort()

    images.push(repository=repository, path=path)


if __name__ == "__main__":

    app()
