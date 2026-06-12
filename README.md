# Simple Python Prolog Shell (SPPS)

### Version 0.2.0-dev

A command‑line interactive Prolog REPL shell built with [PySwip](https://pyswip.org/).
It supports lazy enumeration of solutions
and can load Prolog source files at startup.


## Requirements

- Python 3.10+
- Install dependencies:
  ```bash
  python3 -m pip install -r requirements.txt
  ```
  
- Ensure PySwip can find SWI-Prolog on your system.
  See [Installing SWI-Prolog](https://pyswip.readthedocs.io/en/stable/get_started.html#install-swi-prolog).


## CLI Arguments

```yaml
usage: main.py [-h] [-V] [files ...]

positional arguments:
  files          Prolog source files to consult at startup

options:
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit
```


## CLI Usage

| Command   | Action                                   |
|-----------|------------------------------------------|
| `<query>` | Execute a Prolog query.                  |
| `;`       | Get the next solution of the last query. |
| `exit`    | Exit the shell.                          |
| `?`       | Show help.                               |


## Notes

- The period at the end of a query is optional.
- Using `;` after a query that hasn't produced any solutions will cause an error message.
- The shell does **not** support `trace` or `debug` in interactive mode, but those predicates can still be called inside a query.
