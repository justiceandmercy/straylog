"""Detection patterns for stray debug/log statements, keyed by file extension."""

import re

# Shared patterns reused across languages.
_CONSOLE = re.compile(r"\bconsole\.(log|debug|info|warn|error|trace|dir|table)\s*\(")
_DEBUGGER = re.compile(r"\bdebugger\b")
_PRINT_PY = re.compile(r"\bprint\s*\(")
_PDB = re.compile(r"\bpdb\.set_trace\s*\(")
_BREAKPOINT = re.compile(r"\bbreakpoint\s*\(\s*\)")
_LOG_DEBUG = re.compile(r"\.debug\s*\(")
_FMT_PRINT = re.compile(r"\bfmt\.Print(ln|f)?\s*\(")
_PRINTLN = re.compile(r"\bprintln!\s*\(")
_DBG_MACRO = re.compile(r"\bdbg!\s*\(")
_SYSTEM_OUT = re.compile(r"\bSystem\.out\.print(ln)?\s*\(")
_PUTS = re.compile(r"\bputs\b")
_PHP_DEBUG = re.compile(r"\b(var_dump|print_r|dd)\s*\(")

PATTERNS = {
    ".py": {
        "print": _PRINT_PY,
        "pdb": _PDB,
        "breakpoint": _BREAKPOINT,
        "logging-debug": _LOG_DEBUG,
    },
    ".js": {"console": _CONSOLE, "debugger": _DEBUGGER},
    ".jsx": {"console": _CONSOLE, "debugger": _DEBUGGER},
    ".ts": {"console": _CONSOLE, "debugger": _DEBUGGER},
    ".tsx": {"console": _CONSOLE, "debugger": _DEBUGGER},
    ".mjs": {"console": _CONSOLE, "debugger": _DEBUGGER},
    ".go": {"fmt-print": _FMT_PRINT, "log-debug": _LOG_DEBUG},
    ".rs": {"println": _PRINTLN, "dbg-macro": _DBG_MACRO},
    ".java": {"system-out": _SYSTEM_OUT, "log-debug": _LOG_DEBUG},
    ".rb": {"puts": _PUTS, "p-debug": re.compile(r"\bp\b\s*\(")},
    ".php": {"php-debug": _PHP_DEBUG, "echo-debug": re.compile(r"\becho\b")},
}

DEFAULT_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".mjs",
    ".go", ".rs", ".java", ".rb", ".php",
}

IGNORED_DIRS = {
    ".git", "node_modules", "venv", ".venv", "__pycache__",
    "dist", "build", "target", "vendor",
}


def patterns_for_ext(ext):
    return PATTERNS.get(ext.lower(), {})


def is_ignored_path(parts, ignores):
    return any(part in ignores for part in parts)
