import json
from abc import ABC, abstractmethod

from typing_extensions import Tuple
from websocket import create_connection

from flashcommit import CodexJsonEncoder, logger


class PlatformAdapter(ABC):
    @abstractmethod
    def get_file_list(self) -> list[str]:
        pass

    @abstractmethod
    def read_file(self, file: str) -> str:
        pass


class WSClient:

    def __init__(self, url: str, api_key: str, platform_adapter: PlatformAdapter):
        self.platform_adapter = platform_adapter
        self.authenticated = False
        self.url = url
        self.api_key = api_key
        self.ws = create_connection(url)

    def disconnect(self):
        self.ws.close()

    def query(self, query) -> str:
        files_requested, original_query = self.send_file_query(query, self.platform_adapter.get_file_list())
        file_contents = self.read_files_requested(files_requested)
        return self.send_query_with_files(original_query, file_contents)

    def read_files_requested(self, files_requested):
        file_contents = dict()
        for f in files_requested:
            logger.info(f"Codex is asking for file {f}")
            file_contents[f] = self.platform_adapter.read_file(f)
        return file_contents

    def _send_msg(self, type_: str, message: dict) -> None:
        msg = self._get_msg(type_, message)
        self.ws.send(msg)

    def send_file_query(self, query: str, file_list: list[str]) -> Tuple[str, str]:
        self._send_msg("query", {"question": query, "file_list": file_list})
        file_request = json.loads(self.ws.recv())
        files_requested = file_request["message"]["files"]
        original_query = file_request["message"]["original_query"]
        return files_requested, original_query

    def send_query_with_files(self, query: str, files: dict[str, str]) -> str:
        self._send_msg("query", {"question": query, "files": files})
        recv = self.ws.recv()
        try:
            answer_msg = json.loads(recv)
            return answer_msg["message"]["answer"]
        except:
            logger.error(f"Cannot parse answer {recv}")
            raise

    def auth(self):
        auth_msg = self._get_msg("auth", {"apiKey": self.api_key})
        self.ws.send(auth_msg)
        auth_result = json.loads(self.ws.recv())
        if "message" in auth_result:
            if "status" in auth_result["message"]:
                if auth_result["message"]["status"] == "authenticated":
                    self.authenticated = True
        return self.authenticated

    @staticmethod
    def _get_msg(type_: str, message: dict) -> str:
        return json.dumps({"type": type_, "message": message}, cls=CodexJsonEncoder)
