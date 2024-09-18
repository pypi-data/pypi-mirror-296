from ..models.submissions import Submission as SubmissionModel
import httpx
import typing
if typing.TYPE_CHECKING:
    from .paginated_list import PaginatedList
    from .peer_review import PeerReview
    from .user import User
from .canvas_object import CanvasObject
from .file import File
from .paginated_list import PaginatedList
from .peer_review import PeerReview
from .upload import FileOrPathLike, Uploader
from .util import combine_kwargs, obj_or_id

class Submission(SubmissionModel):

    def __init__(self, requester, attributes):
        super(Submission, self).__init__(requester, attributes)
        self.attachments = [File(requester, attachment) for attachment in attributes.get('attachments', [])]

    def __str__(self):
        return '{}-{}'.format(self.assignment_id, self.user_id)

    def create_submission_peer_review(self, user: 'User | int', **kwargs) -> 'PeerReview':
        """
        Create a peer review for this submission.

        Endpoint: POST /api/v1/courses/:course_id/assignments/:assignment_id/

        Reference: submissions/:submission_id/peer_reviews         <https://canvas.instructure.com/doc/api/peer_reviews.html#method.peer_reviews_api.index

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        kwargs['user_id'] = user_id
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/assignments/{}/submissions/{}/peer_reviews'.format(self.course_id, self.assignment_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return PeerReview(self._requester, response.json())

    async def create_submission_peer_review_async(self, user: 'User | int', **kwargs) -> 'PeerReview':
        """
        Create a peer review for this submission.

        Endpoint: POST /api/v1/courses/:course_id/assignments/:assignment_id/

        Reference: submissions/:submission_id/peer_reviews         <https://canvas.instructure.com/doc/api/peer_reviews.html#method.peer_reviews_api.index

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        kwargs['user_id'] = user_id
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/assignments/{}/submissions/{}/peer_reviews'.format(self.course_id, self.assignment_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return PeerReview(self._requester, response.json())

    def delete_submission_peer_review(self, user: 'User | int', **kwargs) -> 'PeerReview':
        """
        Delete a peer review for this submission.

        Endpoint: DELETE /api/v1/courses/:course_id/assignments/:assignment_id/

        Reference: submissions/:submission_id/peer_reviews         <https://canvas.instructure.com/doc/api/peer_reviews.html#method.peer_reviews_api.index

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        kwargs['user_id'] = user_id
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/assignments/{}/submissions/{}/peer_reviews'.format(self.course_id, self.assignment_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return PeerReview(self._requester, response.json())

    async def delete_submission_peer_review_async(self, user: 'User | int', **kwargs) -> 'PeerReview':
        """
        Delete a peer review for this submission.

        Endpoint: DELETE /api/v1/courses/:course_id/assignments/:assignment_id/

        Reference: submissions/:submission_id/peer_reviews         <https://canvas.instructure.com/doc/api/peer_reviews.html#method.peer_reviews_api.index

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        kwargs['user_id'] = user_id
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/assignments/{}/submissions/{}/peer_reviews'.format(self.course_id, self.assignment_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return PeerReview(self._requester, response.json())

    def edit(self, **kwargs) -> 'Submission':
        """
        Comment on and/or update the grading for a student's assignment submission.

        Endpoint: PUT /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/assignments/{}/submissions/{}'.format(self.course_id, self.assignment_id, self.user_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update(course_id=self.course_id)
        super(Submission, self).set_attributes(response_json)
        return self

    async def edit_async(self, **kwargs) -> 'Submission':
        """
        Comment on and/or update the grading for a student's assignment submission.

        Endpoint: PUT /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/assignments/{}/submissions/{}'.format(self.course_id, self.assignment_id, self.user_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update(course_id=self.course_id)
        super(Submission, self).set_attributes(response_json)
        return self

    def get_submission_peer_reviews(self, **kwargs) -> 'PaginatedList[PeerReview]':
        """
        Get a list of all Peer Reviews this submission.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:assignment_id/

        Reference: submissions/:submission_id/peer_reviews         <https://canvas.instructure.com/doc/api/peer_reviews.html#method.peer_reviews_api.index
        """
        return PaginatedList(PeerReview, self._requester, 'GET', 'courses/{}/assignments/{}/submissions/{}/peer_reviews'.format(self.course_id, self.assignment_id, self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_submission_peer_reviews_async(self, **kwargs) -> 'PaginatedList[PeerReview]':
        """
        Get a list of all Peer Reviews this submission.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:assignment_id/

        Reference: submissions/:submission_id/peer_reviews         <https://canvas.instructure.com/doc/api/peer_reviews.html#method.peer_reviews_api.index
        """
        return PaginatedList(PeerReview, self._requester, 'GET', 'courses/{}/assignments/{}/submissions/{}/peer_reviews'.format(self.course_id, self.assignment_id, self.id), _kwargs=combine_kwargs(**kwargs))

    def mark_read(self, **kwargs) -> 'bool':
        """
        Mark submission as read. No request fields are necessary.

        Endpoint: PUT /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/read

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.mark_submission_read
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/assignments/{}/submissions/{}/read'.format(self.course_id, self.assignment_id, self.user_id))
        return response.status_code == 204

    async def mark_read_async(self, **kwargs) -> 'bool':
        """
        Mark submission as read. No request fields are necessary.

        Endpoint: PUT /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/read

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.mark_submission_read
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/assignments/{}/submissions/{}/read'.format(self.course_id, self.assignment_id, self.user_id))
        return response.status_code == 204

    def mark_unread(self, **kwargs) -> 'bool':
        """
        Mark submission as unread. No request fields are necessary.

        Endpoint: DELETE /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/read

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.mark_submission_unread
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/assignments/{}/submissions/{}/read'.format(self.course_id, self.assignment_id, self.user_id))
        return response.status_code == 204

    async def mark_unread_async(self, **kwargs) -> 'bool':
        """
        Mark submission as unread. No request fields are necessary.

        Endpoint: DELETE /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/read

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.mark_submission_unread
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/assignments/{}/submissions/{}/read'.format(self.course_id, self.assignment_id, self.user_id))
        return response.status_code == 204

    def upload_comment(self, file: 'FileOrPathLike | str', **kwargs) -> 'tuple':
        """
        Upload a file to attach to this submission as a comment.

        Endpoint: POST /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/comments/files

        Reference: https://canvas.instructure.com/doc/api/submission_comments.html#method.submission_comments_api.create_file

        Parameters:
            file: file or str
        """
        response = Uploader(self._requester, 'courses/{}/assignments/{}/submissions/{}/comments/files'.format(self.course_id, self.assignment_id, self.user_id), file, **kwargs).start()
        if response[0]:
            self.edit(comment={'file_ids': [response[1]['id']]})
        return response

    async def upload_comment_async(self, file: 'FileOrPathLike | str', **kwargs) -> 'tuple':
        """
        Upload a file to attach to this submission as a comment.

        Endpoint: POST /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/comments/files

        Reference: https://canvas.instructure.com/doc/api/submission_comments.html#method.submission_comments_api.create_file

        Parameters:
            file: file or str
        """
        response = Uploader(self._requester, 'courses/{}/assignments/{}/submissions/{}/comments/files'.format(self.course_id, self.assignment_id, self.user_id), file, **kwargs).start()
        if response[0]:
            self.edit(comment={'file_ids': [response[1]['id']]})
        return response

class GroupedSubmission(CanvasObject):

    def __init__(self, requester, attributes):
        super(GroupedSubmission, self).__init__(requester, attributes)
        try:
            self.submissions = [Submission(requester, submission) for submission in attributes['submissions']]
        except KeyError:
            self.submissions = list()

    def __str__(self):
        return '{} submission(s) for User #{}'.format(len(self.submissions), self.user_id)