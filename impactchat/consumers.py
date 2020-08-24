import json
import logging
# pylint: disable=import-error
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import translation

import django
# from pprint import pprint
from .models import Message, Channel

from .chat_consumers.notification_helper import NotificationProvider


notif = NotificationProvider()
log = logging.getLogger(__name__)


# pylint: disable=no-member
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        self.notification_room_group_name = "notifications.all"

        # Add client to his chatroom
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Add client to notification room
        await self.channel_layer.group_add(
            self.notification_room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room groups
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_discard(
            self.notification_room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        translation.activate(self.scope['user'].locale)

        data = json.loads(text_data)
        # get type of message (sent by client)
        etype = data['type']

        # new chat message
        if etype == 'chat.new':
            message = data['message']
            channel = data['channel']

            log.info(f"Handling message `{message}` from channel `{channel}`")

            # Create messageand then send notification to clients listening
            m = await self.createMessage(channel, message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.new',
                    'message': message,
                    'channel': channel,
                    'm': m.getJSON()
                }
            )
        # new channel created
        elif etype == 'chat.channel.new':
            channel = data['channel']

            log.info(f"Adding channel `{channel}`")

            # Check if user has `impactchat.manage_channels` perms
            if not (self.scope['user'].has_perm("impactchat.manage_channels")):
                log.warning(f"User {self.scope['user'].username} doesn't have perms to manage channels") # noqa
                return
            else:
                c = None
                # Try creating channel
                try:
                    c = await self.createChannel(channel)
                # Failed to commit to DB
                except django.db.utils.IntegrityError:
                    # Send personnal errror message
                    await notif.send(self,
                                     notif.messages[
                                         'channel.new.error.name_taken'
                                        ])
                    return

                # If successful, send new channel message
                await self.channel_layer.group_send(
                    self.notification_room_group_name,
                    {
                        'type': 'chat.channel.new.success',
                        'c': c.getJSON()
                    }
                )

                # Send personal success message
                await notif.send(self, notif.messages['channel.new.success'])
        elif etype == "chat.channel.delete":
            if not (self.scope['user'].has_perm("impactchat.manage_channels")):
                log.warning(f"User {self.scope['user'].username} doesn't have perms to manage channels") # noqa
                return
            else:
                try:
                    cs = await self.deleteChannels(data['channels'])
                except django.db.utils.IntegrityError:
                    await notif.send(self,
                                     notif.messages['channel.remove.error'])
                    return

                await notif.send(self,
                                 notif.messages['channel.remove.success'])

                await self.channel_layer.group_send(
                    self.notification_room_group_name,
                    {
                        'type': 'chat.channel.delete.success',
                        'cs': cs
                    }
                )
        else:
            log.warning(f"Unrecognixed type: {etype}")

    # Receive message from room group
    async def chat_new(self, event):
        m = event['m']
        await self.send(text_data=json.dumps({
            'new_message': m
        }))

    async def chat_channel_new_success(self, event):
        c = event['c']
        await self.send(text_data=json.dumps({
            'new_channel': c
        }))

    async def chat_channel_delete_success(self, event):
        cs = event['cs']
        await self.send(text_data=json.dumps({
            'channels_deleted': cs
        }))

    @database_sync_to_async
    def createMessage(self, channel_pk, message):
        channel_obj = Channel.objects.get(pk=channel_pk)  # `get_or_create`?
        m = Message.objects.create(channel=channel_obj,
                                   content=message,
                                   author=self.scope['user'])
        return m

    @database_sync_to_async
    def createChannel(self, channel):
        c = Channel.objects.create(name=channel)
        return c

    @database_sync_to_async
    def deleteChannels(self, channels):
        cs = Channel.objects.filter(pk__in=channels)
        cs.update(visible=False)
        return [i.getJSON() for i in cs]
