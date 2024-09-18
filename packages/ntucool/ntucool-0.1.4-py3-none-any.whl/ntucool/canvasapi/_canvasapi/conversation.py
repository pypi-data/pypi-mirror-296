from ..models.conversations import Conversation as ConversationModel
import httpx
import typing
from .canvas_object import CanvasObject
from .util import combine_kwargs

class Conversation(ConversationModel):

    def __str__(self):
        return '{} ({})'.format(self.subject, self.id)

    def add_message(self, body: 'str', **kwargs) -> 'Conversation':
        """
        Add a message to a conversation.

        Endpoint: POST /api/v1/conversations/:id/add_message

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.add_message

        Parameters:
            body: str
        """
        response: 'httpx.Response' = self._requester.request('POST', 'conversations/{}/add_message'.format(self.id), body=body, _kwargs=combine_kwargs(**kwargs))
        return Conversation(self._requester, response.json())

    async def add_message_async(self, body: 'str', **kwargs) -> 'Conversation':
        """
        Add a message to a conversation.

        Endpoint: POST /api/v1/conversations/:id/add_message

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.add_message

        Parameters:
            body: str
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'conversations/{}/add_message'.format(self.id), body=body, _kwargs=combine_kwargs(**kwargs))
        return Conversation(self._requester, response.json())

    def add_recipients(self, recipients: 'list[str]', **kwargs) -> 'Conversation':
        """
        Add a recipient to a conversation.

        Endpoint: POST /api/v1/conversations/:id/add_recipients

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.add_recipients

        Parameters:
            recipients: `list` of `str`
        """
        response: 'httpx.Response' = self._requester.request('POST', 'conversations/{}/add_recipients'.format(self.id), recipients=recipients, _kwargs=combine_kwargs(**kwargs))
        return Conversation(self._requester, response.json())

    async def add_recipients_async(self, recipients: 'list[str]', **kwargs) -> 'Conversation':
        """
        Add a recipient to a conversation.

        Endpoint: POST /api/v1/conversations/:id/add_recipients

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.add_recipients

        Parameters:
            recipients: `list` of `str`
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'conversations/{}/add_recipients'.format(self.id), recipients=recipients, _kwargs=combine_kwargs(**kwargs))
        return Conversation(self._requester, response.json())

    def delete(self, **kwargs) -> 'bool':
        """
        Delete a conversation.

        Endpoint: DELETE /api/v1/conversations/:id

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'conversations/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if response.json().get('id'):
            super(Conversation, self).set_attributes(response.json())
            return True
        else:
            return False

    async def delete_async(self, **kwargs) -> 'bool':
        """
        Delete a conversation.

        Endpoint: DELETE /api/v1/conversations/:id

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'conversations/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if response.json().get('id'):
            super(Conversation, self).set_attributes(response.json())
            return True
        else:
            return False

    def delete_messages(self, remove: 'list[str]', **kwargs) -> 'dict':
        """
        Delete messages from this conversation.
        
        Note that this only affects this user's view of the conversation.
        If all messages are deleted, the conversation will be as well.

        Endpoint: POST /api/v1/conversations/:id/remove_messages

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.remove_messages

        Parameters:
            remove: `list` of `str`
        """
        response: 'httpx.Response' = self._requester.request('POST', 'conversations/{}/remove_messages'.format(self.id), remove=remove, _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def delete_messages_async(self, remove: 'list[str]', **kwargs) -> 'dict':
        """
        Delete messages from this conversation.
        
        Note that this only affects this user's view of the conversation.
        If all messages are deleted, the conversation will be as well.

        Endpoint: POST /api/v1/conversations/:id/remove_messages

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.remove_messages

        Parameters:
            remove: `list` of `str`
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'conversations/{}/remove_messages'.format(self.id), remove=remove, _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def edit(self, **kwargs) -> 'bool':
        """
        Update a conversation.

        Endpoint: PUT /api/v1/conversations/:id

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'conversations/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if response.json().get('id'):
            super(Conversation, self).set_attributes(response.json())
            return True
        else:
            return False

    async def edit_async(self, **kwargs) -> 'bool':
        """
        Update a conversation.

        Endpoint: PUT /api/v1/conversations/:id

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'conversations/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if response.json().get('id'):
            super(Conversation, self).set_attributes(response.json())
            return True
        else:
            return False