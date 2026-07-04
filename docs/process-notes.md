# Process Notes — Environment Setup & Troubleshooting

The pipeline in this repo required standing up a full Python data toolchain on Windows 11 from scratch. These notes document what actually happened, because the troubleshooting is as much the skill as the final chart.

## The stack

| Tool | Role |
|---|---|
| Visual Studio Build Tools | C/C++ compiler required by some Python packages |
| Microsoft ODBC Driver for SQL Server | Database connectivity layer |
| Anaconda Navigator | Python environment management |
| JupyterLab | Notebook development |
| pyodbc | Python ↔ SQL Server connector |
| pandas / matplotlib | Analysis and visualization |
| Tableau Public | Dashboard work (later course weeks) |

## Problems hit and fixed

### JupyterLab wouldn't launch (Windows redirect-file bug)
JupyterLab installed cleanly but failed to open in the browser. Root cause: JupyterLab's redirect-file mechanism misbehaving on Windows. Fix: disable it in the Jupyter config —

```python
# jupyter_lab_config.py
c.ServerApp.use_redirect_file = False
```

Documented this permanently so it never costs time again.

### Native package builds failing
Some packages needed compilation and failed on a bare Windows install. Fix: install Visual Studio Build Tools first, then retry — after which the environment built cleanly.

### Verifying the pipeline end to end
Rather than assuming the stack worked, I verified each link: ODBC driver visible to the system → pyodbc connects → query returns rows → DataFrame pivots → chart renders. The chart in this repo is that verification, kept as the proof.

## Working habits this project reinforced

- Read the error before searching for it; most failures named the missing layer directly.
- Fix once, document forever — every fix went into a reusable troubleshooting note.
- Keep credentials in environment variables from day one, even for a class server.
