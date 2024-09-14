import re
from typing import Iterator

from unidiff import PatchSet, UnidiffParseError

from flashcommit import logger


def nr_of_context_lines(lines: list[str]) -> int:
    return sum(1 for _line in lines if _line.strip() and not _line.strip().startswith(('+', '-')))


def increment_nr_of_lines(s: str) -> str:
    def match(m):
        lstart, lend, rstart, rend = m.groups()
        return f"@@ -{lstart},{int(lend) + 1} +{rstart},{int(rend) + 1} @@"

    return re.sub(r"@@ -(\d+),(\d+) \+(\d+),(\d+) @@", match, s)


def decrement_nr_of_lines(s: str) -> str:
    def match(m):
        lstart, lend, rstart, rend = m.groups()
        return f"@@ -{lstart},{int(lend) - 1} +{rstart},{int(rend) - 1} @@"

    return re.sub(r"@@ -(\d+),(\d+) \+(\d+),(\d+) @@", match, s)


def set_nr_of_lines(s: str, lines: list[str]) -> str:
    def match(m):
        lstart, lend, rstart, rend = m.groups()
        return f"@@ -{lstart},{nr_of_context_lines(lines)} +{rstart},{nr_of_context_lines(lines)} @@"

    return re.sub(r"@@ -(\d+),(\d+) \+(\d+),(\d+) @@", match, s)


def fix_nr_of_lines(s: str, hunk: str) -> str:
    def match(m):
        lstart, lend, rstart, rend = m.groups()
        return f"@@ -{lstart},{count_non_plus_lines(hunk)} +{rstart},{count_non_minus_lines(hunk)} @@"

    return re.sub(r"@@ -(\d+),(\d+) \+(\d+),(\d+) @@", match, s)


def lowest_nr_of_lines(s: str) -> int:
    pattern = r"@@ -\d+,(\d+) \+\d+,(\d+) @@"
    matches = re.search(pattern, s)
    if matches:
        first_number = int(matches.group(1))
        second_number = int(matches.group(2))
        return first_number if first_number < second_number else second_number
    else:
        return -1


def count_non_minus_lines(text: str) -> int:
    return sum(1 for line in text.split('\n')
               if not line.startswith('-') and not line.startswith('@@'))


def count_non_plus_lines(text: str) -> int:
    return sum(1 for line in text.split('\n')
               if not line.startswith('+') and not line.startswith('@@'))


def fix_hunk(_header: list[str], _hunk: list[str], tries=0):
    if tries > 3:
        return None
    _hunk[0] = fix_nr_of_lines(_hunk[0], "\n".join(_hunk))
    _diff = "\n".join(_header + _hunk)
    try:
        ps = PatchSet(_diff)
        return _hunk
    except UnidiffParseError as e:
        logger.warn(f"Cannot parse diff {_diff}", exc_info=True)
        return None


def parse_diff(diff: str, file: str) -> Iterator[str]:
    diff = diff.strip()
    header = list()
    hunks = list()
    hunk_found = False
    hunk_index = -1
    for line in diff.splitlines():
        if line.startswith("@@"):
            hunk_found = True
            hunk_index = len(hunks)
            hunks.append(list())

        if not hunk_found:
            header.append(line.rstrip())
        else:
            hunks[hunk_index].append(line.rstrip())

    if len(header) == 0:
        header.append(f"--- a/{file}")
        header.append(f"+++ b/{file}")
        """
        index ac37857..1234567 100644
        --- a/flashcommit/main.py
        +++ b/flashcommit/main.py
        """


    i = 0
    for hunk in hunks:
        hunks[i] = fix_hunk(header, hunk)
        i = i + 1

    for hunk in hunks:
        if hunk is not None:
            yield "\n".join(header + hunk)
