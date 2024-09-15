from ..models.run import Run
from ..core.assistant_manager import AssistantManager
from ..core.thread_manager import ThreadManager
from datetime import datetime, timezone
from ..utils.exceptions import RunExecutionError, InvalidInputError
from typing import Any, Dict, List


class RunManager:
    def __init__(
        self,
        assistant_manager: AssistantManager,
        thread_manager: ThreadManager,
    ):
        self.assistant_manager = assistant_manager
        self.thread_manager = thread_manager
        self.runs: Dict[str, Run] = {}

    async def create_run(
        self,
        assistant_id: str,
        thread_id: str,
        **kwargs,
    ) -> Run:
        assistant = await self.assistant_manager.get_assistant(assistant_id)
        thread = await self.thread_manager.get_thread(thread_id)

        if not assistant or not thread:
            raise ValueError("Invalid assistant_id or thread_id")

        run = Run(assistant_id=assistant_id, thread_id=thread_id)
        self.runs[run.id] = run
        return run

    async def execute_run(self, run_id: str, **kwargs) -> str:
        run = self.runs.get(run_id)
        if not run:
            raise ValueError("Invalid run_id")

        assistant = await self.assistant_manager.get_assistant(run.assistant_id)
        thread = await self.thread_manager.get_thread(run.thread_id)

        if not assistant or not thread:
            raise ValueError("Invalid assistant or thread")

        run.status = "in_progress"
        run.started_at = datetime.now(timezone.utc)

        try:
            messages = await self.thread_manager.get_messages(thread.id)
            prompt = self._create_prompt(messages)

            if not self.assistant_manager.custom_llm_function:
                raise ValueError("Custom LLM function not set")

            response = await self.assistant_manager.custom_llm_function(
                assistant.model, prompt, **assistant.provider_config
            )

            content = self._extract_content(response)

            await self.thread_manager.add_message(thread.id, "assistant", content)

            run.status = "completed"
            run.completed_at = datetime.now(timezone.utc)
            return content
        except Exception as e:
            run.status = "failed"
            run.error = str(e)
            raise RunExecutionError(f"Run execution failed: {str(e)}")

    def _extract_content(self, response: Any) -> str:
        if isinstance(response, str):
            return response
        elif isinstance(response, dict) and "content" in response:
            return response["content"]
        else:
            raise InvalidInputError("Unsupported response format from provider")

    def _create_prompt(self, messages: List[Dict[str, Any]]) -> str:
        return "\n".join([f"{msg.role}: {msg.content}" for msg in messages])

    async def get_run(self, run_id: str) -> Run:
        run = self.runs.get(run_id)
        if run is None:
            raise ValueError(f"Run with id {run_id} not found")
        return run
