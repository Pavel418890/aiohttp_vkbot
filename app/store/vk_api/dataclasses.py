import copy
from dataclasses import dataclass


# Базовые структуры, для выполнения задания их достаточно,
# поэтому постарайтесь не менять их пожалуйста из-за возможных проблем с тестами
from typing import Optional


@dataclass
class Message:
    user_id: int
    text: str
    peer_id: int


@dataclass
class UpdateMessage:
    id: int
    peer_id: int
    random_id: int
    text: str
    from_id: Optional[int] = None
    attachments: Optional[list] = None
    conversation_message_id: Optional[int] = None
    date: Optional[int] = None
    fwd_messages: Optional[list] = None
    important: Optional[bool] = None
    is_hidden: Optional[bool] = None
    out: Optional[int] = None


@dataclass
class UpdateObject:
    message: UpdateMessage
    client_info: dict

    def __post_init__(self):
        if isinstance(self.message, dict):
            raw_message = copy.deepcopy(self.message)
            self.message = UpdateMessage(**raw_message)

@dataclass
class Update:
    type: str
    event_id: str
    group_id: str
    object: UpdateObject
    v: str

    def __post_init__(self):
        if isinstance(self.object, dict):
            raw_object = copy.deepcopy(self.object)
            self.object = UpdateObject(**raw_object)
