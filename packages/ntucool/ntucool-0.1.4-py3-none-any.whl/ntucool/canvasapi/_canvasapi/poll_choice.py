from ..models.poll_choices import PollChoice as PollChoiceModel
import httpx
import typing
from .canvas_object import CanvasObject
from .exceptions import RequiredFieldMissing
from .util import combine_kwargs

class PollChoice(PollChoiceModel):

    def __str__(self):
        return '{} ({})'.format(self.text, self.id)

    def delete(self, **kwargs) -> 'bool':
        """
        Delete a single poll, based on the poll id.

        Endpoint: DELETE /api/v1/polls/:poll_id/poll_choices/:id

        Reference: https://canvas.instructure.com/doc/api/poll_choices.html#method.polling/poll_choices.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'polls/{}/poll_choices/{}'.format(self.poll_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    async def delete_async(self, **kwargs) -> 'bool':
        """
        Delete a single poll, based on the poll id.

        Endpoint: DELETE /api/v1/polls/:poll_id/poll_choices/:id

        Reference: https://canvas.instructure.com/doc/api/poll_choices.html#method.polling/poll_choices.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'polls/{}/poll_choices/{}'.format(self.poll_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    def update(self, poll_choice: 'list', **kwargs) -> 'PollChoice':
        """
        Update an existing choice for this poll.

        Endpoint: PUT /api/v1/polls/:poll_id/poll_choices/:id

        Reference: https://canvas.instructure.com/doc/api/poll_choices.html#method.polling/poll_choices.update

        Parameters:
            poll_choice: list
        """
        if isinstance(poll_choice, list) and isinstance(poll_choice[0], dict) and ('text' in poll_choice[0]):
            kwargs['poll_choice'] = poll_choice
        else:
            raise RequiredFieldMissing("Dictionary with key 'text' is required.")
        response: 'httpx.Response' = self._requester.request('PUT', 'polls/{}/poll_choices/{}'.format(self.poll_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return PollChoice(self._requester, response.json()['poll_choices'][0])

    async def update_async(self, poll_choice: 'list', **kwargs) -> 'PollChoice':
        """
        Update an existing choice for this poll.

        Endpoint: PUT /api/v1/polls/:poll_id/poll_choices/:id

        Reference: https://canvas.instructure.com/doc/api/poll_choices.html#method.polling/poll_choices.update

        Parameters:
            poll_choice: list
        """
        if isinstance(poll_choice, list) and isinstance(poll_choice[0], dict) and ('text' in poll_choice[0]):
            kwargs['poll_choice'] = poll_choice
        else:
            raise RequiredFieldMissing("Dictionary with key 'text' is required.")
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'polls/{}/poll_choices/{}'.format(self.poll_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return PollChoice(self._requester, response.json()['poll_choices'][0])