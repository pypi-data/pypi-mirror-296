"""Pytest fixtures for dialog management testing."""

from unittest.mock import AsyncMock, Mock

import pytest

from eloqent.engine.context import DialogContext
from eloqent.engine.manager import DialogManager


@pytest.fixture
def dialog_manager(request):
    """
    Fixture to create a DialogManager instance for testing.

    Args:
        request: The pytest request object.

    Returns:
        DialogManager: An instance of DialogManager with mock components.
    """
    policy = request.param if hasattr(request, "param") else ["StartFlow(greeting)"]
    mock_planner = Mock()
    mock_planner.return_value = AsyncMock(policy=policy)
    context = DialogContext()
    domain = {
        "flows": {
            "greeting": {
                "description": "Greet the user",
                "steps": [
                    {
                        "respond": "greeting",
                    }
                ],
            },
            "farewell": {
                "description": "Say goodbye to the user",
                "steps": [
                    {
                        "respond": "farewell",
                    }
                ],
            },
            "doing_well": {
                "description": "Respond to the user's positive statement",
                "steps": [
                    {
                        "respond": "doing_well",
                    }
                ],
            },
            "weather_forecast": {
                "description": "Get the weather forecast",
                "steps": [
                    {
                        "execute": "get_weather",
                    },
                    {
                        "respond": "forecast",
                    },
                ],
            },
        },
        "slots": {
            "location": {
                "type": "text",
                "description": "",
                "ask": "",
            }
        },
        "responses": {
            "greeting": ["Hello, how are you?"],
            "farewell": ["Goodbye, have a great day!"],
            "doing_well": ["That's great to hear!"],
            "forecast": ["The weather in {location} is {weather}."],
        },
        "actions": {
            "get_weather": {
                "type": "http",
                "description": "Get the weather forecase for the city",
                "endpoint": "http://localhost/get_weather",
                "required_slots": ["location"],
                "data": {"location": "{location}"},
                "response_mapping": {
                    "type": "json",
                    "items": [
                        {
                            "weather": {
                                "type": "text",
                                "description": "",
                                "key": "$.weather",
                            }
                        }
                    ],
                },
            }
        },
    }
    return DialogManager(domain, mock_planner, context)
