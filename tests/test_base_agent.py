import pytest
from unittest.mock import patch, MagicMock
from src.base_agent import BaseAgent, LLMAPIError, BlankHallucinationError, SchemaValidationError

class DummyAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Dummy", role="Testing", model_name="dummy-model", temperature=0.5)
        
    def _ai_handler(self, state: dict):
        return self._call_llm("test prompt")
        
    def _logic_handler(self, state: dict):
        return {"status": "logic_fallback"}

def test_circuit_breaker_fallback():
    agent = DummyAgent()
    with patch.object(agent, '_call_llm_with_retry', side_effect=Exception("API Down")):
        result = agent.execute({"test": 1})
        # Should fallback to _logic_handler when _ai_handler fails
        assert result == {"status": "logic_fallback"}

@patch("src.base_agent.ChatOpenAI")
def test_blank_hallucination(mock_chat):
    agent = DummyAgent()
    # Mock LLM to return empty string
    mock_llm_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "   "
    mock_llm_instance.invoke.return_value = mock_response
    agent.llm = mock_llm_instance

    with pytest.raises(BlankHallucinationError):
        # We need to bypass the @retry for testing or just catch the retry exception
        # Actually tenacity will retry 5 times and then raise the error
        try:
            agent._call_llm_with_retry("test prompt")
        except Exception as e:
            # Check if it's the RetryError wrapping our error, or our error directly
            if hasattr(e, 'last_attempt'):
                raise e.last_attempt.result()
            raise e

@patch("src.base_agent.ChatOpenAI")
def test_api_rate_limit(mock_chat):
    agent = DummyAgent()
    # Mock LLM to raise Exception with 429
    mock_llm_instance = MagicMock()
    mock_llm_instance.invoke.side_effect = Exception("429 rate limit exceeded")
    agent.llm = mock_llm_instance

    with pytest.raises(LLMAPIError):
        try:
            agent._call_llm_with_retry("test prompt")
        except Exception as e:
            if hasattr(e, 'last_attempt'):
                raise e.last_attempt.result()
            raise e
