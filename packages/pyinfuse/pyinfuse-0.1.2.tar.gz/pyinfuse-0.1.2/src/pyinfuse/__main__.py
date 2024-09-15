"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """Pyinfuse."""


if __name__ == "__main__":
    main(prog_name="pyinfuse")  # pragma: no cover
