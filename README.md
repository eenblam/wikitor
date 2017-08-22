# wikitor
Basic wrapper around the MediaWiki API for scraping pages over Tor.

## Installation and Setup
To install the required libraries into your current environment:
```bash
pip install -r requirements.txt
```

Suppose we want to stash a bunch of WikiHow articles about sewing.
We can create a SQLite database `sewing.db` with a table called `sewing`
using the following:
```bash
python schema.py sewing
```
