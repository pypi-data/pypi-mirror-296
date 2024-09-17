"""Unit tests for the DialogManager class."""

import pytest


@pytest.mark.asyncio
async def test_process_user_message(dialog_manager):
    """Test the process_user_message method of DialogManager."""
    # Arrange
    user_message = "Hi!"
    context_dict = {
        "active_flow": None,
        "slots": {},
        "dialog_state": "waiting_for_user",
    }
    transcript = [
        {"role": "user", "content": "Hi!"},
    ]

    # Act
    responses = [
        response async for response in dialog_manager.process_user_message(user_message)
    ]

    # Assert
    dialog_manager.planner.assert_called_once_with(
        conversation_history=transcript,
        current_state=context_dict,
        users_latest_message=user_message,
    )

    assert isinstance(responses, list)
    assert len(responses) > 0
    assert all(isinstance(response, str) for response in responses)
    assert len(dialog_manager.history) == 2
    assert dialog_manager.dialog_context.active_flow is None


@pytest.mark.parametrize(
    "dialog_manager, expected_responses",
    [
        (["StartFlow(greeting)"], ["Hello, how are you?"]),
        (["StartFlow(farewell)"], ["Goodbye, have a great day!"]),
        (
            ["StartFlow(greeting)", "StartFlow(farewell)"],
            ["Hello, how are you?", "Goodbye, have a great day!"],
        ),
        (
            [
                "StartFlow(weather_forecast)",
            ],
            [
                "API call to http://localhost/get_weather executed",
                "The weather in {location} is {weather}.",
            ],
        ),
    ],
    indirect=["dialog_manager"],
)
@pytest.mark.asyncio
async def test_process_user_message_with_different_policies(
    dialog_manager, expected_responses
):
    """Test process_user_message with different policy configurations."""
    user_message = "Hi!"
    responses = [
        response async for response in dialog_manager.process_user_message(user_message)
    ]
    assert responses == expected_responses


# @pytest.mark.asyncio
# async def test_multi_turn_conversation(dialog_manager):
#     responses = []
#     async for response in dialog_manager.process_user_message("Hi!"):
#         responses.append(response)
#     async for response in dialog_manager.process_user_message("I'm doing well, thanks!"):
#         responses.append(response)
#     async for response in dialog_manager.process_user_message("Goodbye!"):
#         responses.append(response)

#     assert responses == [
#         "Hello, how are you?",
#         "That's great to hear!",
#         "Goodbye, have a great day!",
#     ]


# @pytest.mark.asyncio
# async def test_handle_unknown_flow(dialog_manager):
#     dialog_manager.planner.return_value = type("Prediction", (), {"policy": ["StartFlow(unknown_flow)"]})()
#     with pytest.raises(ValueError):
#         async for _ in dialog_manager.process_user_message("Hi!"):
#             pass


@pytest.mark.asyncio
async def test_context_updates(dialog_manager):
    """Test context updates after processing a user message."""
    async for _ in dialog_manager.process_user_message("Hi!"):
        pass
    assert dialog_manager.dialog_context.active_flow is None
    assert len(dialog_manager.history) == 2
    assert dialog_manager.history[-1]["role"] == "assistant"
