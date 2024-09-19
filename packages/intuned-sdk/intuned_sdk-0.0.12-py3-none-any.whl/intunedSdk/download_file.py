from playwright.async_api import Page, Locator
from typing import Union, Callable
import asyncio

async def download_file(
    page: Page,
    trigger: Union[
        str,
        Locator,
        Callable[[Page], None],
    ],
):
    """
    Download a file from a web page using a trigger.

    This function supports three different ways to trigger a download:
    1. By URL
    2. By clicking on a playwright locator
    3. By executing a callback function that takes a page object as an argument and uses it to initiate the download.

    Args:
        page (Page): The Playwright Page object to use for the download.
        trigger (Union[str, Locator, Callable[[Page], None]]):
            - If str: URL to download from.
            - If Locator: playwright locator to click to download.
            - If Callable: callback function that takes a page object as an argument and uses it to initiate the download.

    Returns:
        Download: A Playwright Download object representing the downloaded file.

    Example:
    ```python
    from intunedSdk import download_file

    context, page = await launch_chromium(headless=False)
    await download_file(page, "https://sandbox.intuned.dev/pdfs")
    ```
    
    ```python
    from intunedSdk import download_file

    context, page = await launch_chromium(headless=False)
    await download_file(page, page.locator("button:has-text('Download')"))
    ```
    
    ```python
    from intunedSdk import download_file

    context, page = await launch_chromium(headless=False)
    await download_file(page, lambda page: page.locator("button:has-text('Download')").click())
    ```
    
    Note:
        If a URL is provided as the trigger, a new page will be created and closed
        after the download is complete.
        If a locator is provided as the trigger, the page will be used to click the element and initiate the download.
        If a callback function is provided as the trigger, the function will be called with the page object as an argument and will be responsible for initiating the download.
    """
    page_to_download_from = page
    should_close_after_download = False

    if isinstance(trigger, str):
        page_to_download_from = await page.context.new_page()
        should_close_after_download = True

    async with page_to_download_from.expect_download() as download_info:
        if isinstance(trigger, str):
            try:
                await page_to_download_from.goto(trigger, wait_until="load", timeout=5000)
            except Exception:
                pass

        if isinstance(trigger, Locator):
            await trigger.click()

        if callable(trigger):
            await trigger(page)

    download = await download_info.value

    if should_close_after_download:
        await page_to_download_from.close()

    return download
