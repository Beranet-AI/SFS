"""Thin entrypoint that delegates to the infrastructure worker loop."""

from infrastructure.app import run_worker


def main() -> None:
    run_worker()


if __name__ == "__main__":
    main()
