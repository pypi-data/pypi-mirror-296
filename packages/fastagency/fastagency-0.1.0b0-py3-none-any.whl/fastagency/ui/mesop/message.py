import json
from typing import Optional

import mesop as me

from ...base import (
    IOMessage,
    IOMessageVisitor,
    MultipleChoice,
    SystemMessage,
    TextInput,
    TextMessage,
)
from .components.ui_common import darken_hex_color


def message_box(message: str) -> None:
    message_dict = json.loads(message)
    level = message_dict["level"]
    conversation_id = message_dict["conversationId"]
    io_message_dict = message_dict["io_message"]
    io_message = IOMessage.create(**io_message_dict)
    visitor = MesopGUIMessageVisitor(level, conversation_id)
    visitor.process_message(io_message)


class MesopGUIMessageVisitor(IOMessageVisitor):
    def __init__(self, level: int, conversation_id: str) -> None:
        """Initialize the MesopGUIMessageVisitor object.

        Args:
            level (int): The level of the message.
            conversation_id (str): The ID of the conversation.
        """
        self._level = level
        self._conversation_id = conversation_id

    def visit_default(self, message: IOMessage) -> None:
        base_color = "#aff"
        with me.box(
            style=me.Style(
                background=base_color,
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            self._header(message, base_color)
            me.markdown(message.type)

    def visit_text_message(self, message: TextMessage) -> None:
        base_color = "#fff"
        with me.box(
            style=me.Style(
                background=base_color,
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            self._header(message, base_color, title="Text message")
            me.markdown(message.body)

    def visit_system_message(self, message: SystemMessage) -> None:
        base_color = "#bff"
        with me.box(
            style=me.Style(
                background=base_color,
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            self._header(message, base_color, title="System Message")
            me.markdown(json.dumps(message.message, indent=2))

    def visit_text_input(self, message: TextInput) -> str:
        text = message.prompt if message.prompt else "Please enter a value"
        if message.suggestions:
            suggestions = ",".join(suggestion for suggestion in message.suggestions)
            text += "\n" + suggestions

        base_color = "#bff"
        with me.box(
            style=me.Style(
                background=base_color,
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            self._header(message, base_color, title="Input requested")
            me.markdown(text)
        return ""

    def visit_multiple_choice(self, message: MultipleChoice) -> str:
        text = message.prompt if message.prompt else "Please enter a value"
        if message.choices:
            options = ",".join(
                f"{i+1}. {choice}" for i, choice in enumerate(message.choices)
            )
            text += "\n" + options
        base_color = "#cff"
        with me.box(
            style=me.Style(
                background=base_color,
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            self._header(message, base_color, title="Input requested")
            me.markdown(text)
        return ""

    def process_message(self, message: IOMessage) -> Optional[str]:
        return self.visit(message)

    def _header(
        self, message: IOMessage, base_color: str, title: Optional[str] = None
    ) -> None:
        you_want_it_darker = darken_hex_color(base_color, 0.8)
        with me.box(
            style=me.Style(
                background=you_want_it_darker,
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            h = title if title else message.type
            h += f" from: {message.sender}, to:{message.recipient}"
            if message.auto_reply:
                h += " (auto-reply)"
            me.markdown(h)
