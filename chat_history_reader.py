import re
from datetime import datetime
from dataclasses import dataclass

from typing import List

REGEX_CHAT_DATE_PATTERN = r'\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2}'
REGEX_PATTERN_UID_NUMERIC = r'\((\d{5,12})\)'
# https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
REGEX_PATTERN_UID_MAIL = r'<([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7})>'


@dataclass
class ChatMessage:
    date: datetime
    sender_id: str
    message: str

    def serialize(self):
        return {
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
            'sender_id': self.sender_id,
            'message': self.message
        }


class TxtChatHistoryReader:

    def __init__(self) -> None:
        self.cursor: int = 0
        self.msgs: List[ChatMessage] = []
        self.lines: List[str] = []

    def _get_current_line(self):
        return self.lines[self.cursor]

    def _has_next_line(self):
        return self.cursor + 1 < len(self.lines)

    def _is_message_header(self, line: str) -> bool:
        return re.match(REGEX_CHAT_DATE_PATTERN, line) is not None

    def _next_line(self) -> str:
        assert self._has_next_line()
        self.cursor += 1
        return self._get_current_line()

    def _get_date(self, line: str) -> datetime:
        dt_match = re.match(REGEX_CHAT_DATE_PATTERN, line)

        if dt_match is None:
            raise ValueError(f'No date in line {self.cursor}: {line}')

        return datetime.strptime(dt_match.group(), '%Y-%m-%d %H:%M:%S')

    def _get_uid(self, line: str) -> str:
        uid_match = re.search(REGEX_PATTERN_UID_NUMERIC, line)
        if uid_match is None:
            uid_match = re.search(REGEX_PATTERN_UID_MAIL, line)
        if uid_match is None:
            raise ValueError(f'No uid in line {self.cursor}: {line}')
        return uid_match.group(1)

    def _process_message(self) -> ChatMessage:
        header = self._get_current_line()
        body = self._next_line().strip()

        date = self._get_date(header)
        uid = self._get_uid(header)

        return ChatMessage(date, uid, body)

    def read(self, path: str) -> List[ChatMessage]:
        self.cursor = 0
        with open(path, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

        while self._has_next_line():
            if self._is_message_header(self._get_current_line()):
                self.msgs.append(self._process_message())
            self._next_line()

        return self.msgs
