"""Tests for orchestrator.py"""

from unittest.mock import patch

import pytest

from agent.orchestrator import Orchestrator
from agent.tools.readme_scorer import ReadmeScorer


@pytest.mark.unit
class TestOrchestrator:
    """Test Suite for Orchestrator agent."""

    def test_tool_executes_again_for_second_review(self) -> None:
        """Test that a new review does not reuse a previous tool result."""

        readme_scorer = ReadmeScorer()
        orchestrator = Orchestrator(
            tools={
                "readme_scorer": readme_scorer,
            }
        )

        profile_data = {
            "readme_content": "# Portfolio\nA sample portfolio README.",
        }

        with patch.object(
            readme_scorer,
            "execute",
            wraps=readme_scorer.execute,
        ) as mock_execute:
            # Simulate two separate reviews within the same orchestrator session
            orchestrator.run("profile-123", profile_data)
            orchestrator.run("profile-123", profile_data)

        assert mock_execute.call_count == 2
