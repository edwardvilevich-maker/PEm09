from collections import defaultdict
from typing import Deque, Dict, List, Literal, Tuple
from collections import deque


Mode = Literal["text", "rag", "voice"]


class ConversationMemory:
    def __init__(self, max_messages: int = 15) -> None:
        self._history: Dict[int, Deque[Tuple[str, str]]] = defaultdict(
            lambda: deque(maxlen=max_messages)
        )
        self._modes: Dict[int, Mode] = defaultdict(lambda: "text")

    def add_message(self, user_id: int, role: str, content: str) -> None:
        self._history[user_id].append((role, content))

    def get_history(self, user_id: int) -> List[Tuple[str, str]]:
        return list(self._history[user_id])

    def reset(self, user_id: int) -> None:
        self._history.pop(user_id, None)
        self._modes[user_id] = "text"

    def set_mode(self, user_id: int, mode: Mode) -> None:
        self._modes[user_id] = mode

    def get_mode(self, user_id: int) -> Mode:
        return self._modes[user_id]


memory = ConversationMemory()

