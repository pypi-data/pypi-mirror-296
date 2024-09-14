import re
from typing import Iterator


def remove_first_whitespace_from_line(line):
    if line and line[0].isspace():
        return line[1:]
    return line


class GitHunkLineInfo:

    def __init__(self, minus_context_start: int, minus_context_length: int,
                 plus_context_start: int, plus_context_length: int):
        super().__init__()
        self.minus_context_start: int = minus_context_start
        self.minus_context_length: int = minus_context_length
        # self.minus_nr_of_changed_lines: int = 0
        self.plus_context_start: int = plus_context_start
        self.plus_context_length: int = plus_context_length
        # self.plus_nr_of_changed_lines: int = 0

    def __str__(self):
        return f"@@ -{self.minus_context_start},{self.minus_context_length} +{self.plus_context_start},{self.plus_context_length} @@"


class GitHunkHeader:

    def __init__(self, minus_file: str, plus_file: str,
                 minus_context_start: int, minus_context_length: int,
                 plus_context_start: int, plus_context_length: int):
        super().__init__()
        self.minus_file: str = minus_file
        self.plus_file: str = plus_file
        self.hunk_line_info: GitHunkLineInfo = GitHunkLineInfo(minus_context_start, minus_context_length,
                                                               plus_context_start, plus_context_length)

    def get_diff_git_line(self) -> str:
        return f"diff --git a/{self.minus_file} b/{self.plus_file}"

    def __str__(self):
        return self.get_diff_git_line() + "\n" + f"--- a/{self.minus_file}\n" + f"+++ b/{self.plus_file}\n" + f"{self.hunk_line_info}\n"


class GitHunkContent:

    def __init__(self, self_new_file_content: str):
        super().__init__()
        self.new_file_content = self_new_file_content  # TODO not needed, maybe for context generation later
        # no intendation here, +1 whitespace added on serialization
        self.pre_context_lines: list[str] = list()
        self.post_context_lines: list[str] = list()
        self.changed_lines: list[str] = list()
        self.lines: list[str] = list()
        self.finish_called = False

    def __str__(self):
        result = []
        result.extend('' + line for line in self.pre_context_lines)
        result.extend('' + line for line in self.changed_lines)
        result.extend('' + line for line in self.post_context_lines)
        return '\n'.join(result)

    def add_line(self, line):
        if line.startswith("@@"):
            return  # ignore header
        self.lines.append(line)

    def finish(self):
        self.finish_called = True
        line_index = 0
        for line in self.lines:
            if line.startswith("+") or line.startswith("-"):
                self.changed_lines.append(line)
            elif len(self.changed_lines) == 0:  # assume we are still in pre-context
                self.pre_context_lines.append(line)
            else:  # this may be just a line inside changed lines, which has not changed
                # is there another line starting with plus or minus after this? I cannot tell yet
                if self.is_changed_lines_after(line_index):
                    self.changed_lines.append(line)
                else:
                    self.post_context_lines.append(line)
            line_index += 1

    def number_of_minus_lines(self):
        return sum(line.startswith("-") for line in self.changed_lines)

    def number_of_plus_lines(self):
        return sum(line.startswith("+") for line in self.changed_lines)

    def minus_context_length(self):
        return len(self.pre_context_lines) + self.number_of_minus_lines() + len(self.post_context_lines) - 1  # why ever

    def plus_context_length(self):
        return len(self.pre_context_lines) + self.number_of_plus_lines() + len(self.post_context_lines) - 1  # why ever

    def is_changed_lines_after(self, line_index) -> bool:
        for line in self.lines[:line_index]:
            if line.startswith("+") or line.startswith("-"):
                return True
        return False


class GitHunk:

    def __init__(self, hunk_content: GitHunkContent, filename: str, source: str):
        super().__init__()
        self.content: GitHunkContent = hunk_content
        self.header: GitHunkHeader = self.create_header(filename,
                                                        filename,  # TODO can not handle rename or new files
                                                        source)

    def __str__(self):
        return f"{self.header}{self.content}"

    def create_header(self, old_file: str, new_file: str, source: str) -> GitHunkHeader:
        minus_context_start = self.find_start_of_hunk_in_file(source)
        plus_context_start = minus_context_start  # TODO can not handle rename or new files
        return GitHunkHeader(old_file, new_file,
                             minus_context_start, self.content.minus_context_length(),
                             plus_context_start, self.content.plus_context_length())

    def find_start_of_hunk_in_file(self, source: str) -> int:
        return self.get_linenumber_of_context(source)

    def get_linenumber_of_context(self, source: str) -> int:

        context = "\n".join(self.content.pre_context_lines)
        first_changed_line_without_minus = self.content.changed_lines[0][1:]
        if not context.strip():
            # context before changes is empty, need to apply a different strategy
            context = "\n".join(self.content.post_context_lines)
            matching_lines = list(self.get_linenumbers_of_context(context, source))
            if len(matching_lines) == 0:
                raise ValueError("Lines not found")
            if len(matching_lines) == 1:
                print("found matching line")
                # calc differently - nr of minus lines + lines of pre context
                return matching_lines[0] - len(self.content.pre_context_lines) - self.content.number_of_minus_lines()
            else:
                for matching_line in matching_lines:
                    if list(filter(None, source.splitlines()[matching_line:]))[0] == first_changed_line_without_minus:
                        return matching_line
        else:
            matching_lines = list(self.get_linenumbers_of_context(context, source))
            if len(matching_lines) == 0:
                raise ValueError("Lines not found")
            if len(matching_lines) == 1:
                print("found matching line")
                return matching_lines[0]
            else:
                # multiple candidates, find the one where a matching change is immediatly following
                for matching_line in matching_lines:
                    first_changed_line_without_minus = self.content.changed_lines[0][1:]
                    if list(filter(None, source.splitlines()[matching_line:]))[0] == first_changed_line_without_minus:
                        return matching_line
        raise ValueError("Lines not found")

    def get_linenumbers_of_context(self, context: str, source: str) -> Iterator[int]:
        start = 0
        while True:
            # Find the index of the search string in the file content
            index = source.find(context, start)
            if index == -1:
                # try with first whitespace removed
                index = source.find(self.normalize_context(context), start)
                if index == -1:
                    # If no more occurrences are found, stop the iteration
                    break

            # Calculate the line number where the match starts
            line_number = source[:index].count('\n') + 1
            yield line_number

            # Move the start position to continue searching after this occurrence
            start = index + len(context)

    @staticmethod
    def normalize_context(context: str):
        def process_line(line):
            if line in ('\r\n', '\n'):
                return line  # Keep line breaks as they are
            return remove_first_whitespace_from_line(line)

        return ''.join(process_line(line) for line in re.split(r'(\r\n|\n)', context))


class GitPatch:

    def __init__(self):
        super().__init__()
        self.hunks: list[GitHunk] = []

    def add_hunk(self, h: GitHunk):
        self.hunks.append(h)

    def __str__(self):
        return "\n".join(map(str, self.hunks))


class GitDiffParser:

    def parse(self, diff: str, source: str, filename: str) -> str:
        patch = GitPatch()
        for hunk_content in self._parse(diff, source):
            hunk = GitHunk(hunk_content, filename, source)
            patch.add_hunk(hunk)
        return str(patch)

    @staticmethod
    def _parse(diff: str, source: str) -> list[GitHunkContent]:

        hunks: list[GitHunkContent] = list()
        hunk_found = False
        hunk_index = -1
        for line in diff.splitlines():
            if line.startswith("@@"):
                hunk_found = True
                hunk_index = len(hunks)
                hunks.append(GitHunkContent(source))
            if not hunk_found:
                pass  # assume we are still in the header, we drop it and regenerate later
            else:
                hunks[hunk_index].add_line(line)
        for hunk in hunks:
            hunk.finish()
        """
         TODO
         hunks need 3 lines of context a newline at the end and indentation for context lines plus one space (for +/-)
        """
        return hunks
