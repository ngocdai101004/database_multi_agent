from dbma.native.domain.enum.sender_type import SenderType
from dbma.native.domain.message import Message
from langchain_core.messages import (AIMessage, BaseMessage, HumanMessage,
                                     SystemMessage)


def convert_message_to_langchain_message(message: Message) -> BaseMessage:
    if message.sender_type == SenderType.USER:
        return HumanMessage(content=message.content)
    elif message.sender_type == SenderType.AGENT:
        return AIMessage(content=message.content)
    else:
        return SystemMessage(content=message.content)