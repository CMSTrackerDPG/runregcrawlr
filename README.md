[![Build Status](https://travis-ci.com/ptrstn/runregcrawlr.svg?branch=master)](https://travis-ci.com/ptrstn/runregcrawlr)

# runregcrawlr

Tool used to crawl a few runs from the CERN CMS Run Registry

## Installation

```bash
pip install git+https://github.com/ptrstn/runregcrawlr
```

### lxplus

Make sure that your Python version is at least ```2.7``` or ```3.4```. If not then [enable a newer version](https://cern.service-now.com/service-portal/article.do?n=KB0000730) with:

```bash
scl enable python27 bash
```

or 

```bash
scl enable rh-python36 bash
```

Then you can install runregcrawlr it with:

```bash
virtualenv venv
. venv/bin/activate
pip install git+https://github.com/ptrstn/runregcrawlr
```

## Usage

After you have installed ```runregcrawlr``` with pip the ```runregcrawl``` cli script should be available.

```bash
runregcrawl --help
```

```
usage: runregcrawl [-h] [--min MIN] [--max MAX] [--run RUN]
                   [--list [LIST [LIST ...]]]

CMS Run Registry crawler.

optional arguments:
  -h, --help                show this help message and exit
  --min MIN                 Minimum run number
  --max MAX                 Maximum run number
  --run RUN                 Single run number
  --list [LIST [LIST ...]]  Multiple run numbers
```

### Example

```bash
runregcrawl --min 326941 --max 327489
```

Output:
```
Stored 61 entries in file 'runregcrawlr-output.json'
```

## Development

```bash
git clone https://github.com/ptrstn/runregcrawlr
cd runregcrawlr
python3 -m venv venv
. venv/bin/active
pip install -e .
```
