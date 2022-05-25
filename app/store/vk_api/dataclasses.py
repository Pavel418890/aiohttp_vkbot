import copy
from dataclasses import dataclass
from pprint import pprint

from typing import Optional


@dataclass
class Message:
    user_id: int
    text: str
    peer_id: Optional[int] = None


@dataclass
class UpdateMessage:
    id: int
    from_id: int
    text: str
    peer_id: Optional[int] = None
    random_id: Optional[int] = None
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
    client_info: Optional[dict] = None

    def __post_init__(self):
        if isinstance(self.message, dict):
            raw_message = copy.deepcopy(self.message)
            self.message = UpdateMessage(**raw_message)


@dataclass
class Update:
    type: str
    object: UpdateObject
    event_id: Optional[str] = None
    group_id: Optional[str] = None
    v: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.object, dict):
            raw_object = copy.deepcopy(self.object)
            self.object = UpdateObject(**raw_object)
