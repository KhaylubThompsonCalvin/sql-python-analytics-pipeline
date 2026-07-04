# Data Analytics Pipeline — SQL Server → Python → Visualization

Portfolio project built from my coursework in **CIS277A (Data Analytics) at Portland Community College**, where I'm a full-time Computer Information Systems student.

This repo shows a working end-to-end analytics pipeline that I set up and verified from scratch on Windows: a SQL Server database queried from Python, results shaped with pandas, and a finished time-series visualization.

![Marc vs Mark, U.S. male births by year](screenshots/names-trend-chart.png)

## Project summary

The question: how did two spellings of the same name (*Marc* vs. *Mark*) trend across a century of U.S. births?

The pipeline:

1. **Query** — `pyodbc` connects to a SQL Server database (SSA baby-names dataset, public data) and runs a filtered, ordered SQL query.
2. **Shape** — results load into a pandas DataFrame and pivot from long format (one row per name per year) to one column per name.
3. **Visualize** — matplotlib renders the comparison; the chart above is the actual output.

The finding: *Mark* peaks near 59,000 births/year around 1960 and then declines; *Marc* follows the identical curve at about a tenth of the volume. The rise and fall belong to the name, not the spelling.

Full annotated code: [`notebooks/sql-to-python-pipeline.ipynb`](notebooks/sql-to-python-pipeline.ipynb)

> The course database server requires student access, so the notebook ships with saved output rather than live re-runs. The code pattern works against any SQL Server instance; connection settings load from environment variables.

## Skills demonstrated

- **SQL** — filtered, ordered queries against SQL Server
- **Python** — pandas (DataFrame handling, `pivot`), matplotlib (time-series plots)
- **Database connectivity** — pyodbc, Microsoft ODBC Driver, connection troubleshooting
- **Environment setup** — Anaconda, JupyterLab, Visual Studio Build Tools on Windows, including diagnosing and fixing a JupyterLab launch failure (documented in [docs/process-notes.md](docs/process-notes.md))
- **Security hygiene** — no hard-coded credentials; environment variables only

## Run it against your own SQL Server

The notebook reads connection settings from environment variables, so it runs against any SQL Server instance with a compatible table:

```powershell
pip install -r requirements.txt
$env:DB_SERVER   = "your-server"
$env:DB_NAME     = "your-database"
$env:DB_USER     = "your-user"
$env:DB_PASSWORD = "your-password"
jupyter lab notebooks/sql-to-python-pipeline.ipynb
```

The SSA baby-names data itself is public: [ssa.gov/oact/babynames](https://www.ssa.gov/oact/babynames/) — a planned upgrade is re-running this analysis directly from the public files so no database access is needed at all.

## Repo structure

```
├── README.md
├── requirements.txt
├── .gitignore
├── notebooks/
│   └── sql-to-python-pipeline.ipynb   # annotated pipeline notebook (sanitized)
├── screenshots/
│   └── names-trend-chart.png          # actual pipeline output
└── docs/
    └── process-notes.md               # setup story, problems hit, fixes found
```

## Honest framing

This is coursework turned into a portfolio artifact, and it's labeled that way on purpose. It contains only my own work and output derived from public data. No instructor materials, lab instructions, quiz content, or grades are included. I'm building toward IT support and data analytics roles; this repo is part of that transition.

## About me

- Portfolio: [khaylub.com](https://khaylub.com)
- LinkedIn: [khaylub-thompson-calvin](https://www.linkedin.com/in/khaylub-thompson-calvin-40543b294/)
