"""Flet desktop application entry point."""

from flet import AppBar, Page, Text, app

from packages.logging import get_logger

logger = get_logger(__name__)


def main(page: Page) -> None:
    """Create desktop application."""
    logger.info("Starting FDIA Desktop...")

    page.title = "Finance Document Intelligence Agent"
    page.window_width = 1200
    page.window_height = 800

    appbar = AppBar(title=Text("FDIA - Finance Document Intelligence"))
    page.appbar = appbar

    page.add(
        Text("Welcome to FDIA Dashboard", size=24, weight="bold"),
        Text("Application initialization in progress..."),
    )

    logger.info("Desktop application initialized successfully")


if __name__ == "__main__":
    logger.info("Launching Flet application...")
    app(target=main)
