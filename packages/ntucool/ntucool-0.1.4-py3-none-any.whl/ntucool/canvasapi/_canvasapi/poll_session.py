from ..models.poll_sessions import PollSession as PollSessionModel
import httpx
import typing
if typing.TYPE_CHECKING:
    from .poll_submission import PollSubmission
from .canvas_object import CanvasObject
from .exceptions import RequiredFieldMissing
from .poll_submission import PollSubmission
from .util import combine_kwargs, obj_or_id

class PollSession(PollSessionModel):

    def __str__(self):
        return '{} ({})'.format(self.poll_id, self.id)

    def close(self, **kwargs):
        """
        Close a poll session to answers based on the poll id.

        Endpoint: GET /api/v1/polls/:poll_id/poll_sessions/:id/close

        Reference: https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.close
        """
        response: 'httpx.Response' = self._requester.request('GET', 'polls/{}/poll_sessions/{}/close'.format(self.poll_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return PollSession(self._requester, response.json()['poll_sessions'][0])

    async def close_async(self, **kwargs):
        """
        Close a poll session to answers based on the poll id.

        Endpoint: GET /api/v1/polls/:poll_id/poll_sessions/:id/close

        Reference: https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.close
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'polls/{}/poll_sessions/{}/close'.format(self.poll_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return PollSession(self._requester, response.json()['poll_sessions'][0])

    def create_submission(self, poll_submissions: 'list', **kwargs) -> 'PollSubmission':
        """
        Create a new poll submission for this poll session.

        Endpoint: POST /api/v1/polls/:poll_id/poll_sessions/:poll_session_id/poll_submissions

        Reference: https://canvas.instructure.com/doc/api/poll_submissions.html#method.polling/poll_submissions.create

        Parameters:
            poll_submissions: list
        """
        if isinstance(poll_submissions, list) and isinstance(poll_submissions[0], dict) and ('poll_choice_id' in poll_submissions[0]):
            kwargs['poll_submissions'] = poll_submissions
        else:
            raise RequiredFieldMissing("Dictionary with key 'poll_choice_id is required.")
        response: 'httpx.Response' = self._requester.request('POST', 'polls/{}/poll_sessions/{}/poll_submissions'.format(self.poll_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return PollSubmission(self._requester, response.json()['poll_submissions'][0])

    async def create_submission_async(self, poll_submissions: 'list', **kwargs) -> 'PollSubmission':
        """
        Create a new poll submission for this poll session.

        Endpoint: POST /api/v1/polls/:poll_id/poll_sessions/:poll_session_id/poll_submissions

        Reference: https://canvas.instructure.com/doc/api/poll_submissions.html#method.polling/poll_submissions.create

        Parameters:
            poll_submissions: list
        """
        if isinstance(poll_submissions, list) and isinstance(poll_submissions[0], dict) and ('poll_choice_id' in poll_submissions[0]):
            kwargs['poll_submissions'] = poll_submissions
        else:
            raise RequiredFieldMissing("Dictionary with key 'poll_choice_id is required.")
        response: 'httpx.Response' = await self._requester.request_async('POST', 'polls/{}/poll_sessions/{}/poll_submissions'.format(self.poll_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return PollSubmission(self._requester, response.json()['poll_submissions'][0])

    def delete(self, **kwargs) -> 'bool':
        """
        Delete a single poll session, based on the session id.

        Endpoint: DELETE /api/v1/polls/:poll_id/poll_sessions/:id

        Reference: https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'polls/{}/poll_sessions/{}'.format(self.poll_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    async def delete_async(self, **kwargs) -> 'bool':
        """
        Delete a single poll session, based on the session id.

        Endpoint: DELETE /api/v1/polls/:poll_id/poll_sessions/:id

        Reference: https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'polls/{}/poll_sessions/{}'.format(self.poll_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    def get_submission(self, poll_submission: 'int | PollSubmission', **kwargs) -> 'PollSubmission':
        """
        Returns the poll submission with the given id.

        Endpoint: GET /api/v1/polls/:poll_id/poll_sessions/:poll_session_id/poll_submissions/:id

        Reference: https://canvas.instructure.com/doc/api/poll_submissions.html#method.polling/poll_submissions.show

        Parameters:
            poll_submission: int or :class:`canvasapi.poll_submission.PollSubmission`
        """
        poll_submission_id = obj_or_id(poll_submission, 'poll_submission', (PollSubmission,))
        response: 'httpx.Response' = self._requester.request('GET', 'polls/{}/poll_sessions/{}/poll_submissions/{}'.format(self.poll_id, self.id, poll_submission_id), _kwargs=combine_kwargs(**kwargs))
        return PollSubmission(self._requester, response.json()['poll_submissions'][0])

    async def get_submission_async(self, poll_submission: 'int | PollSubmission', **kwargs) -> 'PollSubmission':
        """
        Returns the poll submission with the given id.

        Endpoint: GET /api/v1/polls/:poll_id/poll_sessions/:poll_session_id/poll_submissions/:id

        Reference: https://canvas.instructure.com/doc/api/poll_submissions.html#method.polling/poll_submissions.show

        Parameters:
            poll_submission: int or :class:`canvasapi.poll_submission.PollSubmission`
        """
        poll_submission_id = obj_or_id(poll_submission, 'poll_submission', (PollSubmission,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'polls/{}/poll_sessions/{}/poll_submissions/{}'.format(self.poll_id, self.id, poll_submission_id), _kwargs=combine_kwargs(**kwargs))
        return PollSubmission(self._requester, response.json()['poll_submissions'][0])

    def open(self, **kwargs):
        """
        Open a poll session to answers based on the poll id.

        Endpoint: GET /api/v1/polls/:poll_id/poll_sessions/:id/open

        Reference: https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.open
        """
        response: 'httpx.Response' = self._requester.request('GET', 'polls/{}/poll_sessions/{}/open'.format(self.poll_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return PollSession(self._requester, response.json()['poll_sessions'][0])

    async def open_async(self, **kwargs):
        """
        Open a poll session to answers based on the poll id.

        Endpoint: GET /api/v1/polls/:poll_id/poll_sessions/:id/open

        Reference: https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.open
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'polls/{}/poll_sessions/{}/open'.format(self.poll_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return PollSession(self._requester, response.json()['poll_sessions'][0])

    def update(self, poll_session: 'list', **kwargs) -> 'PollSession':
        """
        Update an existing poll session for a poll based on poll id.

        Endpoint: PUT /api/v1/polls/:poll_id/poll_sessions/:id

        Reference: https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.update

        Parameters:
            poll_session: list
        """
        if isinstance(poll_session, list) and isinstance(poll_session[0], dict) and ('course_id' in poll_session[0]):
            kwargs['poll_session'] = poll_session
        else:
            raise RequiredFieldMissing("Dictionary with key 'course_id' is required.")
        response: 'httpx.Response' = self._requester.request('PUT', 'polls/{}/poll_sessions/{}'.format(self.poll_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return PollSession(self._requester, response.json()['poll_sessions'][0])

    async def update_async(self, poll_session: 'list', **kwargs) -> 'PollSession':
        """
        Update an existing poll session for a poll based on poll id.

        Endpoint: PUT /api/v1/polls/:poll_id/poll_sessions/:id

        Reference: https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.update

        Parameters:
            poll_session: list
        """
        if isinstance(poll_session, list) and isinstance(poll_session[0], dict) and ('course_id' in poll_session[0]):
            kwargs['poll_session'] = poll_session
        else:
            raise RequiredFieldMissing("Dictionary with key 'course_id' is required.")
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'polls/{}/poll_sessions/{}'.format(self.poll_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return PollSession(self._requester, response.json()['poll_sessions'][0])