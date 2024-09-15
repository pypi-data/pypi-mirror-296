from ..models.assistant import Assistant
from ..utils.exceptions import InvalidProviderError
from typing import Dict, Any, Callable, Optional
import uuid


class AssistantManager:
    def __init__(self) -> None:
        self.assistants: Dict[str, Assistant] = {}
        self.custom_llm_function: Optional[Callable] = None

    def set_custom_llm_function(self, custom_function: Callable):
        self.custom_llm_function = custom_function

    async def create_assistant(
        self,
        name: str,
        instructions: str,
        model: str,
        custom_llm_function: Optional[Callable] = None,
        **kwargs,
    ) -> Assistant:
        if custom_llm_function:
            self.set_custom_llm_function(custom_llm_function)

        if not self.custom_llm_function:
            raise InvalidProviderError("Custom LLM function not set")

        assistant = Assistant(
            id=str(uuid.uuid4()),
            name=name,
            instructions=instructions,
            model=model,
            provider_config=kwargs,
        )
        self.assistants[assistant.id] = assistant
        return assistant

    async def get_assistant(self, assistant_id: str) -> Assistant:
        assistant = self.assistants.get(assistant_id)
        if assistant is None:
            raise ValueError(f"Assistant with id {assistant_id} not found")
        return assistant
