# Intuned python sdk

how to publish to pypi:

1. update version in setup.py and pyproject.toml
2. clear dist
3. python setup.py sdist bdist_wheel
4. twine upload dist/*


how to run a test:

```bash
pytest tests/upload_file_to_s3_test_e2e.py
```

