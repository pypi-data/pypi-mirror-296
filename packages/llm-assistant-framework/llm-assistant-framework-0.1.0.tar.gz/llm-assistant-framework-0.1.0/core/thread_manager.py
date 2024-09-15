from ..models.thread import Thread
from ..models.message import Message
from typing import List, Union, Literal, Dict


class ThreadManager:
    def __init__(self) -> None:
        self.threads: Dict[str, Thread] = {}

    async def create_thread(self) -> Thread:
        thread = Thread()
        self.threads[thread.id] = thread
        return thread

    async def get_thread(self, thread_id: str) -> Thread:
        thread = self.threads.get(thread_id)
        if thread is None:
            raise ValueError(f"Thread with id {thread_id} not found")
        return thread

    async def add_message(
        self,
        thread_id: str,
        role: Union[Literal["user"], Literal["assistant"]],
        content: str,
    ) -> Message:
        thread = await self.get_thread(thread_id)
        message = Message(role=role, content=content)
        thread.messages.append(message)
        return message

    async def get_messages(self, thread_id: str) -> List[Message]:
        thread = await self.get_thread(thread_id)
        return thread.messages
