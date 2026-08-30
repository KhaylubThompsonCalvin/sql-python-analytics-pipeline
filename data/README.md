# Data

This directory holds the public dataset the analysis runs on. **The data itself is not committed to this
repository** — it is downloaded from the official source instead.

## Why the data isn't in the repo

The SSA archive expands to ~145 yearly files. Committing a public dataset that anyone can fetch in one
command adds weight to the repo without adding evidence of anything. Downloading it from the source also
keeps the analysis honestly reproducible: you get the data from SSA, not from me.

## Source

| | |
|---|---|
| Dataset | U.S. baby names, national totals by year |
| Publisher | U.S. Social Security Administration |
| Archive | https://www.ssa.gov/oact/babynames/names.zip |
| Landing page | https://www.ssa.gov/oact/babynames/limits.html |
| License | Public domain |

## Get the data

```bash
python scripts/download_ssa_data.py
```

That downloads the archive, extracts the yearly files into `data/raw/`, and writes
`data/raw/PROVENANCE.json` recording the source URL, retrieval timestamp, SHA-256 of the archive, file
count, and year range — so any figure produced later can be traced back to a specific download.

Running it again is safe; it skips the download if the data is already there (`--force` to override).

### If the download is blocked

Some networks and hosting providers are blocked by ssa.gov's CDN and receive `HTTP 403`. If that happens,
download `names.zip` manually from the landing page above and unzip it into `data/raw/`. The analysis
notebook only cares that the files are present.

## File format

One file per year, `yob1880.txt` onward. No header row; three comma-separated columns:

```
Name,Sex,Count
Mary,F,7065
Anna,F,2604
```

`Count` is the number of U.S. births registered with that name and sex in that year. SSA applies a
privacy floor — names with fewer than 5 occurrences in a year are omitted entirely, which matters when
reading any early-year or rare-name trend.

## Layout

```
data/
├── README.md          # this file (committed)
└── raw/               # downloaded data (NOT committed - see .gitignore)
    ├── yob1880.txt
    ├── ...
    └── PROVENANCE.json
```
