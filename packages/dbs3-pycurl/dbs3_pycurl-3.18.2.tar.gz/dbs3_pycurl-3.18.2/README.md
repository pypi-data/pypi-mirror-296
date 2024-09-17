# PycurlClient
Build new release via:
```
python setup4pypi.py sdist bdist_wheel
```
and then upload to pypi via:
```
twine upload --verbose dist/*
```
