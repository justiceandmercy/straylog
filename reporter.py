"""Output formatting for straylog findings."""


def format_human(findings):
    if not findings:
        return "No stray debug statements found."
    lines = []
    for f in findings:
        lines.append("{}:{}: [{}] {}".format(f["file"], f["line"], f["kind"], f["text"]))
    lines.append("")
    lines.append("{} finding(s).".format(len(findings)))
    return "\n".join(lines)
