import tempfile
import json
from pathlib import Path
import aiofiles
from playwright.async_api import async_playwright
from typing import Any


async def create_user_dir_with_preferences():
    # Create a temporary directory
    playwright_temp_dir = tempfile.mkdtemp(prefix="pw-")
    user_dir = Path(playwright_temp_dir) / "userdir"
    default_dir = user_dir / "Default"

    # Create the default directory recursively
    default_dir.mkdir(parents=True, exist_ok=True)

    # Preferences data
    preferences = {
        "plugins": {
            "always_open_pdf_externally": True,
        }
    }

    # Write preferences to file
    async with aiofiles.open(default_dir / "Preferences", mode="w") as f:
        await f.write(json.dumps(preferences))

    absolute_path = user_dir.absolute().as_posix()

    return absolute_path


async def launch_chromium(headless: bool = True, **kwargs: Any):
    playwright = await async_playwright().start()
    dir = await create_user_dir_with_preferences()
    context = await playwright.chromium.launch_persistent_context(
        dir, headless=headless, **kwargs
    )
    return (context, context.pages[0])
