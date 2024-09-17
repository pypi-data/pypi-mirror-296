import json

from typing_extensions import Tuple

from flashcommit import logger
from flashcommit.client import BaseClient


class ReviewClient(BaseClient):
    def send_file_query(self, diff: str, file_list: list[str]) -> Tuple[str, str]:
        self._send_msg("file_list", {"diff": diff, "file_list": file_list})
        recv = self.ws.recv()
        if not recv:
            raise ValueError("No response received")
        try:
            file_request = self.to_json(recv)
            files_requested = file_request["message"]["files"]
            return files_requested
        except:
            logger.error(f"Cannot process response '{recv}'", exc_info=True)
            raise

    def review_with_files(self, diff: str, files: dict[str, str]) -> str:
        self._send_msg("review", {"diff": diff, "files": files})
        recv = self.ws.recv()
        try:
            logger.debug(f"Answer: {recv}")
            answer_msg = json.loads(recv)
            return answer_msg["message"]["answer"]
        except:
            logger.error(f"Cannot parse answer {recv}")
            raise

    def review(self, diff):
        files_requested = self.send_file_query(diff, self.platform_adapter.get_file_list())
        file_contents = self.read_files_requested(files_requested)
        return self.review_with_files(diff, file_contents)
