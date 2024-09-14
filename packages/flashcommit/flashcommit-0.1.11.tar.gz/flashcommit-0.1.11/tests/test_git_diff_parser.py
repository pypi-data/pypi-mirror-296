import pathlib

from flashcommit.gitdiff import GitDiffParser
from util import last_hashes, assert_diff_applies

source_dir = pathlib.Path(__file__).parent.resolve()


def test_simple_with_git_parser():
    last_hashes.clear()
    with open(f"{source_dir}/fixtures/simple/diff_parser.py") as sf:
        source = sf.read()
        with open(f"{source_dir}/fixtures/simple/diff.txt") as df:
            bad_diff = df.read()
            git_diff = GitDiffParser().parse(bad_diff, source, "fixtures/simple/diff_parser.py")
            assert_diff_applies(git_diff, "fixtures/simple/diff_parser.py")


def test_complex_with_git_parser():
    last_hashes.clear()
    with open(f"{source_dir}/fixtures/not-so-simple/diff_parser.py") as sf:
        source = sf.read()
        with open(f"{source_dir}/fixtures/not-so-simple/diff.txt") as df:
            bad_diff = df.read()
            diff_soup = GitDiffParser().parse(bad_diff, source, "fixtures/not-so-simple/diff_parser.py")
            assert_diff_applies(diff_soup, "fixtures/not-so-simple/diff_parser.py")


def test_with_inbetween_context():
    last_hashes.clear()
    with open(f"{source_dir}/fixtures/diff-with-context-between-changed-lines/gitclient.py") as sf:
        source = sf.read()
        with open(f"{source_dir}/fixtures/diff-with-context-between-changed-lines/diff.txt") as df:
            bad_diff = df.read()
            diff_soup = GitDiffParser().parse(bad_diff, source,
                                              "fixtures/diff-with-context-between-changed-lines/gitclient.py")
            assert_diff_applies(diff_soup, "fixtures/diff-with-context-between-changed-lines/gitclient.py")
