from playwright.async_api import Page, Locator
from typing import Union, Callable


async def download_file(
    page: Page,
    trigger: Union[
        str,
        Locator,
        Callable[[Page], None],
    ],
):
    page_to_download_from = page
    should_close_after_download = False

    if isinstance(trigger, str):
        page_to_download_from = await page.context.new_page()
        await page_to_download_from.goto(trigger)
        should_close_after_download = True

    async with page.expect_download() as download_info:
        if isinstance(trigger, str):
            await page.goto(trigger)

        if isinstance(trigger, Locator):
            await trigger.click()

        if callable(trigger):
            await trigger(page)

    download = await download_info.value

    if should_close_after_download:
        await page_to_download_from.close()

    return download
