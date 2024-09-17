import json

import requests
from typing_extensions import Tuple

from flashcommit import logger, get_api_url
from flashcommit.client import ws_to_http_base, BaseClient


class QueryClient(BaseClient):

    def query(self, query) -> str:
        files_requested, original_query = self.send_file_query(query, self.platform_adapter.get_file_list())
        file_contents = self.read_files_requested(files_requested)
        return self.send_query_with_files(original_query, file_contents)

    def send_file_query(self, query: str, file_list: list[str]) -> Tuple[str, str]:
        self._send_msg("query", {"question": query, "file_list": file_list})
        recv = self.ws.recv()
        if not recv:
            raise ValueError("No response received")
        try:
            file_request = self.to_json(recv)
            files_requested = file_request["message"]["files"]
            original_query = file_request["message"]["original_query"]
            return files_requested, original_query
        except:
            logger.error(f"Cannot process response '{recv}'", exc_info=True)
            raise

    def send_query_with_files(self, query: str, files: dict[str, str]) -> str:
        self._send_msg("query", {"question": query, "files": files})
        recv = self.ws.recv()
        try:
            answer_msg = json.loads(recv)
            return answer_msg["message"]["answer"]
        except:
            logger.error(f"Cannot parse answer {recv}")
            raise
