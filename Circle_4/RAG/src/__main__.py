"""Entry point: ``uv run python -m src <command> [options]``."""

import sys

import fire

from .cli import CliError, RagCLI


def main() -> int:
    """Run the Fire CLI and turn any failure into a clean error message.

    Returns:
        The process exit code (0 on success).
    """
    try:
        fire.Fire(RagCLI)
    except CliError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        return 130
    except Exception as err:  # last safety net: never show a traceback
        print(f"Unexpected error: {type(err).__name__}: {err}",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
