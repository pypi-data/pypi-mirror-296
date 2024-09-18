from ..models.polls import Poll as PollModel
import httpx
import typing
if typing.TYPE_CHECKING:
    from .paginated_list import PaginatedList
    from .paginated_list import PaginatedList
    from .poll_session import PollSession
    from .poll_choice import PollChoice
from .canvas_object import CanvasObject
from .exceptions import RequiredFieldMissing
from .paginated_list import PaginatedList
from .poll_choice import PollChoice
from .poll_session import PollSession
from .util import combine_kwargs, obj_or_id

class Poll(PollModel):

    def __str__(self):
        return '{} ({})'.format(self.question, self.id)

    def create_choice(self, poll_choice: 'list', **kwargs) -> 'PollChoice':
        """
        Create a new choice for the current poll.

        Endpoint: POST /api/v1/polls/:poll_id/poll_choices

        Reference: https://canvas.instructure.com/doc/api/poll_choices.html#method.polling/poll_choices.create

        Parameters:
            poll_choice: list
        """
        if isinstance(poll_choice, list) and isinstance(poll_choice[0], dict) and ('text' in poll_choice[0]):
            kwargs['poll_choice'] = poll_choice
        else:
            raise RequiredFieldMissing("Dictionary with key 'text' is required.")
        response: 'httpx.Response' = self._requester.request('POST', 'polls/{}/poll_choices'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return PollChoice(self._requester, response.json()['poll_choices'][0])

    async def create_choice_async(self, poll_choice: 'list', **kwargs) -> 'PollChoice':
        """
        Create a new choice for the current poll.

        Endpoint: POST /api/v1/polls/:poll_id/poll_choices

        Reference: https://canvas.instructure.com/doc/api/poll_choices.html#method.polling/poll_choices.create

        Parameters:
            poll_choice: list
        """
        if isinstance(poll_choice, list) and isinstance(poll_choice[0], dict) and ('text' in poll_choice[0]):
            kwargs['poll_choice'] = poll_choice
        else:
            raise RequiredFieldMissing("Dictionary with key 'text' is required.")
        response: 'httpx.Response' = await self._requester.request_async('POST', 'polls/{}/poll_choices'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return PollChoice(self._requester, response.json()['poll_choices'][0])

    def create_session(self, poll_session: 'list', **kwargs) -> 'PollSession':
        """
        Create a new poll session for this poll

        Endpoint: POST /api/v1/polls/:poll_id/poll_sessions

        Reference: https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.create

        Parameters:
            poll_session: list
        """
        if isinstance(poll_session, list) and isinstance(poll_session[0], dict) and ('course_id' in poll_session[0]):
            kwargs['poll_session'] = poll_session
        else:
            raise RequiredFieldMissing("Dictionary with key 'course_id' is required.")
        response: 'httpx.Response' = self._requester.request('POST', 'polls/{}/poll_sessions'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return PollSession(self._requester, response.json()['poll_sessions'][0])

    async def create_session_async(self, poll_session: 'list', **kwargs) -> 'PollSession':
        """
        Create a new poll session for this poll

        Endpoint: POST /api/v1/polls/:poll_id/poll_sessions

        Reference: https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.create

        Parameters:
            poll_session: list
        """
        if isinstance(poll_session, list) and isinstance(poll_session[0], dict) and ('course_id' in poll_session[0]):
            kwargs['poll_session'] = poll_session
        else:
            raise RequiredFieldMissing("Dictionary with key 'course_id' is required.")
        response: 'httpx.Response' = await self._requester.request_async('POST', 'polls/{}/poll_sessions'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return PollSession(self._requester, response.json()['poll_sessions'][0])

    def delete(self, **kwargs) -> 'bool':
        """
        Delete a single poll, based on the poll id.

        Endpoint: DELETE /api/v1/polls/:id

        Reference: https://canvas.instructure.com/doc/api/polls.html#method.polling/polls.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'polls/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    async def delete_async(self, **kwargs) -> 'bool':
        """
        Delete a single poll, based on the poll id.

        Endpoint: DELETE /api/v1/polls/:id

        Reference: https://canvas.instructure.com/doc/api/polls.html#method.polling/polls.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'polls/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    def get_choice(self, poll_choice, **kwargs) -> 'PollChoice':
        """
        Returns the poll choice with the given id.

        Endpoint: GET /api/v1/polls/:poll_id/poll_choices/:id

        Reference: https://canvas.instructure.com/doc/api/poll_choices.html#method.polling/poll_choices.show
        """
        poll_choice_id = obj_or_id(poll_choice, 'poll_choice', (PollChoice,))
        response: 'httpx.Response' = self._requester.request('GET', 'polls/{}/poll_choices/{}'.format(self.id, poll_choice_id), _kwargs=combine_kwargs(**kwargs))
        return PollChoice(self._requester, response.json()['poll_choices'][0])

    async def get_choice_async(self, poll_choice, **kwargs) -> 'PollChoice':
        """
        Returns the poll choice with the given id.

        Endpoint: GET /api/v1/polls/:poll_id/poll_choices/:id

        Reference: https://canvas.instructure.com/doc/api/poll_choices.html#method.polling/poll_choices.show
        """
        poll_choice_id = obj_or_id(poll_choice, 'poll_choice', (PollChoice,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'polls/{}/poll_choices/{}'.format(self.id, poll_choice_id), _kwargs=combine_kwargs(**kwargs))
        return PollChoice(self._requester, response.json()['poll_choices'][0])

    def get_choices(self, **kwargs) -> 'PaginatedList[PollChoice]':
        """
        Returns a paginated list of PollChoices of a poll, based on poll id.

        Endpoint: GET /api/v1/polls/:poll_id/poll_choices

        Reference: https://canvas.instructure.com/doc/api/poll_choices.html#method.polling/poll_choices.index
        """
        return PaginatedList(PollChoice, self._requester, 'GET', 'polls/{}/poll_choices'.format(self.id), _root='poll_choices', _kwargs=combine_kwargs(**kwargs))

    async def get_choices_async(self, **kwargs) -> 'PaginatedList[PollChoice]':
        """
        Returns a paginated list of PollChoices of a poll, based on poll id.

        Endpoint: GET /api/v1/polls/:poll_id/poll_choices

        Reference: https://canvas.instructure.com/doc/api/poll_choices.html#method.polling/poll_choices.index
        """
        return PaginatedList(PollChoice, self._requester, 'GET', 'polls/{}/poll_choices'.format(self.id), _root='poll_choices', _kwargs=combine_kwargs(**kwargs))

    def get_session(self, poll_session, **kwargs) -> 'PollSession':
        """
        Returns the poll session with the given id.

        Endpoint: GET /api/v1/polls/:poll_id/poll_sessions/:id

        Reference: https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.show
        """
        poll_session_id = obj_or_id(poll_session, 'poll_session', (PollSession,))
        response: 'httpx.Response' = self._requester.request('GET', 'polls/{}/poll_sessions/{}'.format(self.id, poll_session_id), _kwargs=combine_kwargs(**kwargs))
        return PollSession(self._requester, response.json()['poll_sessions'][0])

    async def get_session_async(self, poll_session, **kwargs) -> 'PollSession':
        """
        Returns the poll session with the given id.

        Endpoint: GET /api/v1/polls/:poll_id/poll_sessions/:id

        Reference: https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.show
        """
        poll_session_id = obj_or_id(poll_session, 'poll_session', (PollSession,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'polls/{}/poll_sessions/{}'.format(self.id, poll_session_id), _kwargs=combine_kwargs(**kwargs))
        return PollSession(self._requester, response.json()['poll_sessions'][0])

    def get_sessions(self, **kwargs) -> 'PaginatedList[PollSession]':
        """
        Returns the paginated list of PollSessions in a poll.

        Endpoint: GET /api/v1/polls/:poll_id/poll_sessions

        Reference: https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.index
        """
        return PaginatedList(PollSession, self._requester, 'GET', 'polls/{}/poll_sessions'.format(self.id), _root='poll_sessions', _kwargs=combine_kwargs(**kwargs))

    async def get_sessions_async(self, **kwargs) -> 'PaginatedList[PollSession]':
        """
        Returns the paginated list of PollSessions in a poll.

        Endpoint: GET /api/v1/polls/:poll_id/poll_sessions

        Reference: https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.index
        """
        return PaginatedList(PollSession, self._requester, 'GET', 'polls/{}/poll_sessions'.format(self.id), _root='poll_sessions', _kwargs=combine_kwargs(**kwargs))

    def update(self, poll: 'list', **kwargs) -> 'Poll':
        """
        Update an existing poll belonging to the current user.

        Endpoint: PUT /api/v1/polls/:id

        Reference: https://canvas.instructure.com/doc/api/polls.html#method.polling/polls.update

        Parameters:
            poll: list
        """
        if isinstance(poll, list) and isinstance(poll[0], dict) and ('question' in poll[0]):
            kwargs['poll'] = poll
        else:
            raise RequiredFieldMissing("Dictionary with key 'question' is required.")
        response: 'httpx.Response' = self._requester.request('PUT', 'polls/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Poll(self._requester, response.json()['polls'][0])

    async def update_async(self, poll: 'list', **kwargs) -> 'Poll':
        """
        Update an existing poll belonging to the current user.

        Endpoint: PUT /api/v1/polls/:id

        Reference: https://canvas.instructure.com/doc/api/polls.html#method.polling/polls.update

        Parameters:
            poll: list
        """
        if isinstance(poll, list) and isinstance(poll[0], dict) and ('question' in poll[0]):
            kwargs['poll'] = poll
        else:
            raise RequiredFieldMissing("Dictionary with key 'question' is required.")
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'polls/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Poll(self._requester, response.json()['polls'][0])