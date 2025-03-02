import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ConsumerChat(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Build connection for user group
        """
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """
        Leave the Group
        """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print(f"Disconnected: {close_code}")
    async def receive(self, text_data):
        """
        Recieve messages from users
        """
        data = json.loads(text_data)
        message = data["message"]
        sender = data["sender"]

        # Publish message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message, "sender": sender},
        )

    async def chat_message(self, event):
        """
        Send message to Group
        """
        await self.send(text_data=json.dumps({"message": event["message"], "sender": event["sender"]}))    