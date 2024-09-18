# Intuned python sdk

how to publish to pypi:


1. update version in setup.py and pyproject.toml
2. run publish.sh

    ```bash
    sh ./publish.sh
    ```

how to run a test:

```bash
pytest --log-cli-level=DEBUG tests/extract_structured_data_from_page_test_e2e.py
```
