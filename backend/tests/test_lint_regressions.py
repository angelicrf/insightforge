import sys
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
openai = types.ModuleType("openai")


class AsyncOpenAI: ...


openai.AsyncOpenAI = AsyncOpenAI
sys.modules.setdefault("openai", openai)

from app.agents.shared_context import SharedContext, ToolCall
from app.agents.supervisor_agent import SupervisorAgent
from app.api.routes.integrations import _load_cached_pkce_data
from app.config.settings import settings
from app.tools.salesforce_client import SalesforceTool


def test_salesforce_tool_ignores_invalid_cached_token(tmp_path, monkeypatch):
    token_file = tmp_path / "salesforce-token.json"
    token_file.write_text("{not-json", encoding="utf-8")
    monkeypatch.setattr(settings, "SALESFORCE_TOKEN_FILE", str(token_file))

    tool = SalesforceTool()

    assert tool.access_token is None
    assert tool.instance_url is None


def test_load_cached_pkce_data_returns_empty_dict_for_invalid_json(tmp_path, monkeypatch):
    cache_file = tmp_path / "pkce-cache.json"
    cache_file.write_text("{not-json", encoding="utf-8")
    monkeypatch.setattr(settings, "SALESFORCE_PKCE_CACHE_FILE", str(cache_file))

    assert _load_cached_pkce_data() == {}


@pytest.mark.asyncio
async def test_supervisor_agent_catches_value_error_from_tool_call(monkeypatch):
    class FailingSalesforceTool:
        async def broken(self):
            raise ValueError("bad tool input")

    monkeypatch.setattr(settings, "OPENAI_API_KEY", None)
    agent = SupervisorAgent(llm_provider=None)
    agent.salesforce_tool = FailingSalesforceTool()
    context = SharedContext(
        tool_call=ToolCall(tool_name="salesforce", function_name="broken", args={}),
    )

    result = await agent._execute_tool(context)

    assert result.tool_output == {"error": "bad tool input"}
