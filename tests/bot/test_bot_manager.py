import uuid
from datetime import datetime

from app.store.vk_api.dataclasses import Update, UpdateObject, Message, UpdateMessage


class TestHandleUpdates:
    async def test_no_messages(self, store):
        await store.bots_manager.handle_updates(updates=[])
        assert store.vk_api.send_message.called is False

    async def test_new_message(self, store):
        await store.bots_manager.handle_updates(
            updates=[
                Update(
                    group_id="213467820",
                    event_id=uuid.uuid4().hex,
                    type="message_new",
                    v="5.131",
                    object=UpdateObject(
                        client_info={},
                        message=UpdateMessage(
                            id=1,
                            text="kek",
                            peer_id=1,
                            random_id=0,
                        ),

                    ),
                )
            ]
        )
            
        assert store.vk_api.send_message.call_count == 1
        message: Message = store.vk_api.send_message.mock_calls[0].args[0]
        assert message.peer_id == 1
        assert message.text
