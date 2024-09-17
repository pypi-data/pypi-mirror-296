import argparse
import os
import sys
from collections import defaultdict
from contextlib import contextmanager
from pathlib import Path
from typing import Optional
from xml.etree import ElementTree
from xml.etree.ElementTree import XML

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from prompt_toolkit.shortcuts import button_dialog, message_dialog
from rich.markdown import Markdown
from rich.progress import Progress
# noinspection PyProtectedMember
from websocket import _exceptions

from flashcommit import get_api_url, logger
from flashcommit.client import PlatformAdapter
from flashcommit.client.queryclient import QueryClient
from flashcommit.client.reviewclient import ReviewClient
from flashcommit.gitclient import GitClient
from flashcommit.prompt_generator import PromptGenerator
from flashcommit.version import version

NO_API_KEY_MSG = "CODEX_API_KEY environment variable not set"
NO_CHANGES_FOUND_MSG = "[yellow]No changes found.[/yellow]"
QUERY_PROGRESS_MSG = "[cyan]Thinking about your question..."
REVIEWING_PROGRESS_MSG = "[cyan]Reviewing your changes..."
COMMIT_MSG_PROGRESS_MSG = "[cyan]Generating your commit message..."


class LocalFilesystemAdapter(PlatformAdapter):
    def __init__(self, git_client: GitClient):
        self.git_client = git_client

    def read_file(self, file: str) -> Optional[str]:
        if self.is_readable(file):
            return Path(file).read_text()
        return None

    def get_file_list(self) -> list[str]:
        return [f for f in self.git_client.get_git_files() if self.is_readable(f)]

    @staticmethod
    def is_readable(file: str) -> bool:
        return os.path.isfile(file) and os.access(file, os.R_OK)


def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d


def from_xml(param) -> dict:
    xml_start = param.index("<")
    xml_end = param.rfind(">")
    xml_string = param[xml_start:xml_end + 1]
    soup = BeautifulSoup(xml_string, "xml")
    try:
        xml: XML = ElementTree.fromstring(str(soup))
    except:
        logger.error(f"Cannot parse xml {soup}")
        raise
    to_dict = etree_to_dict(xml)
    return to_dict


class FlashCommit:
    def __init__(self, batch_mode=False):
        load_dotenv()
        if not sys.stdin.isatty():
            batch_mode = True
        self.batch_mode = batch_mode
        self.git_client = GitClient()
        self.git_client.codex_client = self.create_client()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @contextmanager
    def show_progress(self, description: str):
        if self.batch_mode:
            yield
        else:
            with Progress(refresh_per_second=10) as progress:
                task = progress.add_task(description, total=None, transient=True)
                yield
                progress.update(task, completed=True)

    def review(self) -> None:
        try:
            diff = self.git_client.get_diff()
            if diff:
                with self.show_progress(REVIEWING_PROGRESS_MSG):
                    comments = self.create_review_client().review(diff)
                    review = from_xml(comments)
                if review is None:
                    raise ValueError(f"Cannot parse xml from {comments}")
                if "steps" in review:
                    self.parse_review(review)
                elif type(review) is list:
                    for r in review:
                        self.parse_review(r)
                # self.display_answer(str(review))
            else:
                logger.info(NO_CHANGES_FOUND_MSG)
        except Exception as e:
            logger.error(f"Error reviewing your changes", exc_info=True)
            sys.exit(3)

    def parse_review(self, review):
        if "steps" not in review:
            raise ValueError(f"Cannot parse review from {review}")
        for k in review["steps"]:
            if len(review["steps"][k]) == 0:
                continue
            if type(review["steps"][k]) is dict:
                step = review["steps"][k]
            else:
                step = review["steps"][k][0]
            file_ = step['file']
            comment_ = step['comment']
            diff_ = step['patch']

            if not self.batch_mode:
                result = button_dialog(
                    title=comment_,
                    text=diff_,
                    buttons=[
                        ('Apply', 1),
                        ('Skip now', 2),
                        ('Ignore forever', 3)
                    ],
                ).run()
            else:
                result = 1
            if result == 1:
                feedback = self._do_apply(file_, diff_, comment_)
                for f in feedback:
                    if not f[2]:
                        text = f'The patch for {comment_} failed to apply.\nerror: {f[3]}\nPress ENTER to continue.'
                        if not self.batch_mode:
                            message_dialog(
                                title=f"Could not apply patch",
                                text=text).run()
                        else:
                            logger.warn(text)
                    else:
                        logger.info(f"Successfully patched {file_}")
            elif result == 2:
                continue
            elif result == 3:
                self.send_ignore(file_, comment_, diff_)
            if result == 4:
                sys.exit(0)

    def create_client(self) -> QueryClient:
        apikey = self.get_api_key()
        platform_adapter = LocalFilesystemAdapter(self.git_client)
        try:
            client = QueryClient(get_api_url(), apikey, platform_adapter)
        except _exceptions.WebSocketBadStatusException as e:
            logger.error(f"Cannot connect to server: {e.status_code}")
            if e.status_code == 403:
                logger.error("You are not authorized to access this server, check your api key")
            sys.exit(3)
        client.auth()
        return client

    def create_review_client(self) -> ReviewClient:
        apikey = self.get_api_key()
        platform_adapter = LocalFilesystemAdapter(self.git_client)
        try:
            client = ReviewClient(get_api_url() + "/review", apikey, platform_adapter)
        except _exceptions.WebSocketBadStatusException as e:
            logger.error(f"Cannot connect to server: {e.status_code}")
            if e.status_code == 403:
                logger.error("You are not authorized to access this server, check your api key")
            sys.exit(3)
        client.auth()
        return client

    @staticmethod
    def get_api_key() -> Optional[str]:
        apikey = os.getenv("CODEX_API_KEY")
        if not apikey:
            raise ValueError(NO_API_KEY_MSG)
        return apikey

    def display_answer(self, comments: str) -> None:
        md = Markdown(comments)
        logger.info(md)

    def get_commit_message_prompt(self) -> Optional[str]:
        diff = self.git_client.get_diff()
        if not diff:
            return None
        return PromptGenerator.get_commit_message_prompt(diff)

    def generate_message(self) -> Optional[str]:
        try:
            prompt = self.get_commit_message_prompt()
            if prompt:
                with self.show_progress(COMMIT_MSG_PROGRESS_MSG):
                    client = self.create_client()
                    msg = client.to_json(client.query(prompt))["msg"]
                self.display_answer(msg)
                return msg
            else:
                logger.info(NO_CHANGES_FOUND_MSG)
                return None
        except Exception as e:
            logger.error("Error generating a commit message", exc_info=True)
            return None

    def commit(self, message: str) -> None:
        if not message:
            logger.error("No commit message provided.")
            return
        try:
            # TODO self.git_client.commit(message)
            logger.info("Changes committed successfully.")
        except Exception as e:
            logger.error("Error committing changes", exc_info=True)

    def query(self, query):
        try:
            with self.show_progress(QUERY_PROGRESS_MSG):
                msg = self.create_client().query(query)
            self.display_answer(msg)
            return msg
        except Exception as e:
            logger.error(f"Error processing your query", exc_info=True)
            return None

    def send_ignore(self, file_: str, comment_: str, diff_: str) -> None:
        pass

    def _do_apply(self, file: str, diff: str, comment: str) -> list[tuple[str, str, bool, str]]:
        try:
            return self.git_client.patch(comment, diff, file)
        except Exception as e:
            logger.exception(e)
            raise ValueError(f"Cannot apply: {diff} for {file}")


def main():
    parser = argparse.ArgumentParser(description='Flash Commit')
    parser.add_argument('-m', '--message', help='Generate a commit message', action='store_true')
    parser.add_argument('-c', '--commit', help='Generate a commit message and commit the changes (implies -m)',
                        action='store_true')
    parser.add_argument('-q', '--query', help='Submit a query about the whole codebase', action='store', type=str)
    parser.add_argument('-r', '--review', help='Review the current changes - the default action', action='store_true')
    parser.add_argument('-V', '--version', help='Show version information and exit', action='store_true')
    parser.add_argument('-b', '--batch', help='Batch mode, no interactive displays, assume yes on everything',
                        default=False,
                        action='store_true')
    args = parser.parse_args()

    if args.version:
        print(version)
        sys.exit(0)
    with FlashCommit(batch_mode=args.batch) as flash:
        if args.commit:
            flash.commit(flash.generate_message())
        elif args.message:
            flash.generate_message()
        elif args.query is not None:
            flash.query(args.query)
        elif args.review or (not args.commit and not args.message and args.query is None):
            flash.review()


if __name__ == "__main__":
    main()
