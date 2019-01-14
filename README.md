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
                   [--list [LIST [LIST ...]]] [--workspace {global,tracker}]
                   [--out OUT] [--add-lumis | --runs-txt]
                   [--exclude-non-regular] [--exclude-cosmics]

CMS Run Registry crawler.

optional arguments:
  -h, --help                    show this help message and exit
  --min MIN                     Minimum run number
  --max MAX                     Maximum run number
  --run RUN                     Single run number
  --list [LIST [LIST ...]]      Multiple run numbers
  --workspace {global,tracker}
  --out OUT                     Output file name
  --add-lumis                   Add lumisection and luminosity information.
  --runs-txt                    Generate a runs.txt file containing run number
                                and reconstruction.
  --exclude-non-regular         Exclude commissioning and special runs
  --exclude-cosmics             Exclude cosmics runs
```

### Example

```bash
runregcrawl --min 326941 --max 327489
```

Output:

```
Using Global workspace
Stored 313 entries in file 'runregcrawlr-global-output.json'
```

#### Tracker Workspace

Accesses the Tracker workspaces instead of the Global workspace.

```bash
runregcrawl --workspace tracker --min 326941 --max 327489
```

Output:

```
Using Tracker workspace
Stored 400 entries in file 'runregcrawlr-tracker-output.json'
```

To get all non special collision runs of the year 2018 do:

```bash
runregcrawl --workspace tracker --add-lumis --exclude-cosmics --exclude-non-regular --min 313052 --max 327564
```

```
Using Tracker workspace
Stored 2201 entries in file 'runregcrawlr-tracker-output.json'
```

To get all runs of the year 2018 do:

```bash
runregcrawl --workspace tracker --add-lumis --min 313052 --max 327564
```

```
Using Tracker workspace
Stored 9352 entries in file 'runregcrawlr-tracker-output.json'
```

#### Generating runs.txt

A ```runs.txt``` can be generated with the ```--runs-txt``` parameter.

For example to generate a runs.txt with all non special collisions runs from 2018 do this:
 
```bash
runregcrawl --runs-txt --workspace tracker --min 313052 --max 327564 --exclude-cosmics --exclude-non-regular
```

Output:

```
Using Tracker workspace
Stored 2201 entries in file 'runs.txt'
```

Note: The 2018 run number range should be ```313052``` - ```327744``` for cosmics and ```314472``` - ```327564``` for collisions.

## Development

```bash
git clone https://github.com/ptrstn/runregcrawlr
cd runregcrawlr
python3 -m venv venv
. venv/bin/active
pip install -e .
```
