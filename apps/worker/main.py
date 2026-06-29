"""Worker service entry point."""

import asyncio

from packages.logging import get_logger

logger = get_logger(__name__)


async def main() -> None:
    """Run worker service."""
    logger.info("Starting FDIA Worker...")

    try:
        # TODO: Implement worker logic
        # - Monitor WhatsApp
        # - Download files
        # - Process OCR
        # - Extract fields
        # - Update database
        # - Generate exports

        logger.info("Worker initialized successfully")

        # Keep running
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        logger.info("Worker stopped by user")
    except Exception as e:
        logger.error(f"Worker error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
