from datetime import datetime

import pytest

from app.domain.exceptions.messages import TitleTooLongException
from app.domain.values.messages import Text, Title
from app.domain.entities.messages import Message, Chat


def test_create_message_success_short_text():

    text = Text("text")
    message = Message(text=text)

    assert message.text == text
    assert message.created_at.date() == datetime.today().date()


def test_create_message_success_long_text():

    text = Text("text" * 100)
    message = Message(text=text)

    assert message.text == text
    assert message.created_at.date() == datetime.today().date()


def test_create_chat_title_success():

    title = Title("title")
    chat = Chat(title=title)

    assert chat.title == title
    assert not chat.messages
    assert chat.created_at.date() == datetime.today().date()


def test_create_chat_title_too_long():

    with pytest.raises(TitleTooLongException):
        Title("title" * 100)


def test_add_chat_to_messages():

    title = Title("title")
    chat = Chat(title=title)

    message = Message(text=Text("text"))
    chat.add_message(message)

    assert message in chat.messages
