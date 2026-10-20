# straylog

Find stray debug and log statements left in source code before they ship.

`straylog` scans a repository for leftover debugging calls — `console.log`, `print()`,
`debugger`, `pdb.set_trace`, `breakpoint()`, and friends — and reports each hit with its
file and line number so you can clean them up before committing.

## Features

- Multi-language: Python, JavaScript/TypeScript, Go, Rust, Java, Ruby, PHP.
- Configurable extensions and ignore directories.
- Human-readable and JSON output for CI integration.
- Non-zero exit code when findings exist, so it works as a pre-commit / CI gate.
- Zero external dependencies — standard library only.

## Install

```sh
git clone https://github.com/yourname/straylog.git
cd straylog
pip install .
```

Or run directly:

```sh
python straylog.py .
```

## Usage

```sh
# Scan current directory
straylog .

# Scan a specific path
straylog src/

# Only certain extensions
straylog . --ext py,js,ts

# Extra ignore directories
straylog . --ignore vendor,generated

# JSON output for CI
straylog . --json
```

Exit status is `1` if any stray statement is found, `0` otherwise.

## License

MIT