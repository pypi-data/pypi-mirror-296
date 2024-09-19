# Intuned python sdk
https://pypi.org/project/intuned-sdk

## Environment variables
1. copy .env example to .env and fill in the values.
2. for TWINE_PASSWORD find it in [1 password](https://start.1password.com/open/i?a=LSGDSRBLLBDVTNTXSRB4PDRBS4&v=usfd3to6mz3p5ws2wu4seqqs4u&i=6yashi36b7twrepbvh5uc4iiwy&h=intuned.1password.com)
   
## How to publish to pypi
1. update version in setup.py and pyproject.toml
2. make sure you have TWINE_PASSWORD set correctly in the .env file.
3. run publish.sh

    ```bash
    sh ./publish.sh
    ```

## How to run a test
1. install dev dependencies
```bash
pip install -e '.[dev]'   
```

2. run the test
```bash
pytest --log-cli-level=DEBUG tests/extract_structured_data_from_page_test_e2e.py
```

## Examples
1. launch_chromium
```python
from intunedSdk import launch_chromium

async def func():
    [context, page] = await launch_chromium(headless=False)
    await page.goto("https://sandbox.intuned.dev/pdfs")
```

2. download_file
```python
from intunedSdk.download_file import download_file

async def func():
    ...
    download = await download_file(
        page,
        page.locator(
            "#root > div > main > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(4) > a"
        ),
    )

```

3. upload_file_to_s3
```python

 async def test_upload_file_to_s3():
    ...
    # first parameter could be a text, bytes, playwright download
    uploaded_file = await upload_file_to_s3(
        "sample text", fileNameOverride="optionalName.pdf"
    )
```

4. extract_structured_data_from_page
```python

from intunedSdk.launch_chromium import launch_chromium
from intunedSdk import extract_structured_data_from_page

async def func():
    [_, page] = await launch_chromium(headless=False)
    await page.goto("https://sandbox.intuned.dev/pdfs")
    res = await extract_structured_data_from_page(
        page,
        {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"name": {"type": "string"}},
            },
        },
        model="gpt-4o-mini-2024-07-18",
    )

```
