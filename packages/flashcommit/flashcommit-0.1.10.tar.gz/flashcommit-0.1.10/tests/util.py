import hashlib
import subprocess

last_hashes = {}


def file_changed(filename):
    try:
        with open(filename, 'rb') as f:
            content_hash = hashlib.md5(f.read()).hexdigest()
        if filename in last_hashes:
            if content_hash != last_hashes[filename]:
                last_hashes[filename] = content_hash
                return True
        last_hashes[filename] = content_hash
        return False
    except FileNotFoundError:
        if filename in last_hashes:
            del last_hashes[filename]
        return True  # Consider a non-existent file as "changed"


def assert_diff_applies(git_diff: str, source_filename: str):
    with open("diff", "w") as text_file:
        text_file.write(git_diff)
        text_file.flush()
        assert not file_changed(source_filename)
        subprocess.run(["git", "apply", "--directory", "test", "diff"])
        assert file_changed(source_filename)
        subprocess.run(["git", "apply", "--directory", "test", "-R", "diff"])
        assert file_changed(source_filename)
