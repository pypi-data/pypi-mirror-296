from ..models.assignment_groups import AssignmentGroup as AssignmentGroupModel
from ..models.assignment_extensions import AssignmentExtension as AssignmentExtensionModel
from ..models.assignments import Assignment as AssignmentModel, AssignmentOverride as AssignmentOverrideModel
import httpx
import typing
if typing.TYPE_CHECKING:
    from .progress import Progress
    from .submission import Submission
    from .peer_review import PeerReview
    from .user import UserDisplay, User
    from .grade_change_log import GradeChangeEvent
    from .paginated_list import PaginatedList
from .canvas_object import CanvasObject
from .exceptions import CanvasException, RequiredFieldMissing
from .grade_change_log import GradeChangeEvent
from .paginated_list import PaginatedList
from .peer_review import PeerReview
from .progress import Progress
from .submission import Submission
from .upload import FileOrPathLike, Uploader
from .user import User, UserDisplay
from .util import combine_kwargs, obj_or_id

class Assignment(AssignmentModel):

    def __init__(self, requester, attributes):
        super(Assignment, self).__init__(requester, attributes)
        if 'overrides' in attributes:
            self.overrides = [AssignmentOverride(requester, override) for override in attributes['overrides']]

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)

    def create_override(self, **kwargs) -> 'AssignmentOverride':
        """
        Create an override for this assignment.

        Endpoint: POST /api/v1/courses/:course_id/assignments/:assignment_id/overrides

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.create
        """
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/assignments/{}/overrides'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update(course_id=self.course_id)
        return AssignmentOverride(self._requester, response_json)

    async def create_override_async(self, **kwargs) -> 'AssignmentOverride':
        """
        Create an override for this assignment.

        Endpoint: POST /api/v1/courses/:course_id/assignments/:assignment_id/overrides

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.create
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/assignments/{}/overrides'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update(course_id=self.course_id)
        return AssignmentOverride(self._requester, response_json)

    def delete(self, **kwargs) -> 'Assignment':
        """
        Delete this assignment.

        Endpoint: DELETE /api/v1/courses/:course_id/assignments/:id

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignments.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/assignments/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return Assignment(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'Assignment':
        """
        Delete this assignment.

        Endpoint: DELETE /api/v1/courses/:course_id/assignments/:id

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignments.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/assignments/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return Assignment(self._requester, response.json())

    def edit(self, **kwargs) -> 'Assignment':
        """
        Modify this assignment.

        Endpoint: PUT /api/v1/courses/:course_id/assignments/:id

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/assignments/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        if 'name' in response.json():
            super(Assignment, self).set_attributes(response.json())
        return Assignment(self._requester, response.json())

    async def edit_async(self, **kwargs) -> 'Assignment':
        """
        Modify this assignment.

        Endpoint: PUT /api/v1/courses/:course_id/assignments/:id

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/assignments/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        if 'name' in response.json():
            super(Assignment, self).set_attributes(response.json())
        return Assignment(self._requester, response.json())

    def get_grade_change_events(self, **kwargs) -> 'PaginatedList[GradeChangeEvent]':
        """
        Returns the grade change events for the assignment.

        Endpoint: /api/v1/audit/grade_change/assignments/:assignment_id  

        Reference: https://canvas.instructure.com/doc/api/grade_change_log.html#method.grade_change_audit_api.for_assignment
        """
        return PaginatedList(GradeChangeEvent, self._requester, 'GET', 'audit/grade_change/assignments/{}'.format(self.id), _root='events', _kwargs=combine_kwargs(**kwargs))

    async def get_grade_change_events_async(self, **kwargs) -> 'PaginatedList[GradeChangeEvent]':
        """
        Returns the grade change events for the assignment.

        Endpoint: /api/v1/audit/grade_change/assignments/:assignment_id  

        Reference: https://canvas.instructure.com/doc/api/grade_change_log.html#method.grade_change_audit_api.for_assignment
        """
        return PaginatedList(GradeChangeEvent, self._requester, 'GET', 'audit/grade_change/assignments/{}'.format(self.id), _root='events', _kwargs=combine_kwargs(**kwargs))

    def get_gradeable_students(self, **kwargs) -> 'PaginatedList[UserDisplay]':
        """
        List students eligible to submit the assignment.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:assignment_id/gradeable_students

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.gradeable_students
        """
        return PaginatedList(UserDisplay, self._requester, 'GET', 'courses/{}/assignments/{}/gradeable_students'.format(self.course_id, self.id), {'course_id': self.course_id}, _kwargs=combine_kwargs(**kwargs))

    async def get_gradeable_students_async(self, **kwargs) -> 'PaginatedList[UserDisplay]':
        """
        List students eligible to submit the assignment.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:assignment_id/gradeable_students

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.gradeable_students
        """
        return PaginatedList(UserDisplay, self._requester, 'GET', 'courses/{}/assignments/{}/gradeable_students'.format(self.course_id, self.id), {'course_id': self.course_id}, _kwargs=combine_kwargs(**kwargs))

    def get_override(self, override: 'AssignmentOverride | int', **kwargs) -> 'AssignmentOverride':
        """
        Get a single assignment override with the given override id.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:assignment_id/overrides/:id

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.show

        Parameters:
            override: :class:`canvasapi.assignment.AssignmentOverride` or int
        """
        override_id = obj_or_id(override, 'override', (AssignmentOverride,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/assignments/{}/overrides/{}'.format(self.course_id, self.id, override_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update(course_id=self.course_id)
        return AssignmentOverride(self._requester, response_json)

    async def get_override_async(self, override: 'AssignmentOverride | int', **kwargs) -> 'AssignmentOverride':
        """
        Get a single assignment override with the given override id.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:assignment_id/overrides/:id

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.show

        Parameters:
            override: :class:`canvasapi.assignment.AssignmentOverride` or int
        """
        override_id = obj_or_id(override, 'override', (AssignmentOverride,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/assignments/{}/overrides/{}'.format(self.course_id, self.id, override_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update(course_id=self.course_id)
        return AssignmentOverride(self._requester, response_json)

    def get_overrides(self, **kwargs) -> 'PaginatedList[AssignmentOverride]':
        """
        Get a paginated list of overrides for this assignment that target
        sections/groups/students visible to the current user.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:assignment_id/overrides

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.index
        """
        return PaginatedList(AssignmentOverride, self._requester, 'GET', 'courses/{}/assignments/{}/overrides'.format(self.course_id, self.id), {'course_id': self.course_id}, _kwargs=combine_kwargs(**kwargs))

    async def get_overrides_async(self, **kwargs) -> 'PaginatedList[AssignmentOverride]':
        """
        Get a paginated list of overrides for this assignment that target
        sections/groups/students visible to the current user.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:assignment_id/overrides

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.index
        """
        return PaginatedList(AssignmentOverride, self._requester, 'GET', 'courses/{}/assignments/{}/overrides'.format(self.course_id, self.id), {'course_id': self.course_id}, _kwargs=combine_kwargs(**kwargs))

    def get_peer_reviews(self, **kwargs) -> 'PaginatedList[PeerReview]':
        """
        Get a list of all Peer Reviews for this assignment.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:assignment_id/peer_reviews

        Reference: https://canvas.instructure.com/doc/api/peer_reviews.html#method.peer_reviews_api.index
        """
        return PaginatedList(PeerReview, self._requester, 'GET', 'courses/{}/assignments/{}/peer_reviews'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_peer_reviews_async(self, **kwargs) -> 'PaginatedList[PeerReview]':
        """
        Get a list of all Peer Reviews for this assignment.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:assignment_id/peer_reviews

        Reference: https://canvas.instructure.com/doc/api/peer_reviews.html#method.peer_reviews_api.index
        """
        return PaginatedList(PeerReview, self._requester, 'GET', 'courses/{}/assignments/{}/peer_reviews'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))

    def get_provisional_grades_status(self, student_id: 'User | int', **kwargs) -> 'bool':
        """
        Tell whether the student's submission needs one or more provisional grades.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:assignment_id/provisional_grades/

        Reference: status         <https://canvas.instructure.com/doc/api/all_resources.html#method.provisional_grades.status

        Parameters:
            student_id: :class:`canvasapi.user.User` or int
        """
        kwargs['student_id'] = obj_or_id(student_id, 'student_id', (User,))
        request: 'httpx.Response' = self._requester.request('GET', 'courses/{}/assignments/{}/provisional_grades/status'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        request_json: 'dict' = request.json()
        return request_json.get('needs_provisional_grade')

    async def get_provisional_grades_status_async(self, student_id: 'User | int', **kwargs) -> 'bool':
        """
        Tell whether the student's submission needs one or more provisional grades.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:assignment_id/provisional_grades/

        Reference: status         <https://canvas.instructure.com/doc/api/all_resources.html#method.provisional_grades.status

        Parameters:
            student_id: :class:`canvasapi.user.User` or int
        """
        kwargs['student_id'] = obj_or_id(student_id, 'student_id', (User,))
        request: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/assignments/{}/provisional_grades/status'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        request_json: 'dict' = request.json()
        return request_json.get('needs_provisional_grade')

    def get_students_selected_for_moderation(self, **kwargs) -> 'PaginatedList[User]':
        """
        Get a list of students selected for moderation.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:assignment_id/moderated_students

        Reference: https://canvas.instructure.com/doc/api/moderated_grading.html#method.moderation_set.index
        """
        return PaginatedList(User, self._requester, 'GET', 'courses/{}/assignments/{}/moderated_students'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_students_selected_for_moderation_async(self, **kwargs) -> 'PaginatedList[User]':
        """
        Get a list of students selected for moderation.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:assignment_id/moderated_students

        Reference: https://canvas.instructure.com/doc/api/moderated_grading.html#method.moderation_set.index
        """
        return PaginatedList(User, self._requester, 'GET', 'courses/{}/assignments/{}/moderated_students'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))

    def get_submission(self, user: 'User | int', **kwargs) -> 'Submission':
        """
        Get a single submission, based on user id.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.show

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/assignments/{}/submissions/{}'.format(self.course_id, self.id, user_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update(course_id=self.course_id)
        return Submission(self._requester, response_json)

    async def get_submission_async(self, user: 'User | int', **kwargs) -> 'Submission':
        """
        Get a single submission, based on user id.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.show

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/assignments/{}/submissions/{}'.format(self.course_id, self.id, user_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update(course_id=self.course_id)
        return Submission(self._requester, response_json)

    def get_submissions(self, **kwargs) -> 'PaginatedList[Submission]':
        """
        Get all existing submissions for this assignment.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:assignment_id/submissions

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.index
        """
        return PaginatedList(Submission, self._requester, 'GET', 'courses/{}/assignments/{}/submissions'.format(self.course_id, self.id), {'course_id': self.course_id}, _kwargs=combine_kwargs(**kwargs))

    async def get_submissions_async(self, **kwargs) -> 'PaginatedList[Submission]':
        """
        Get all existing submissions for this assignment.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:assignment_id/submissions

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.index
        """
        return PaginatedList(Submission, self._requester, 'GET', 'courses/{}/assignments/{}/submissions'.format(self.course_id, self.id), {'course_id': self.course_id}, _kwargs=combine_kwargs(**kwargs))

    def publish_provisional_grades(self, **kwargs) -> 'dict':
        """
        Publish the selected provisional grade for all submissions to an assignment.
        Use the “Select provisional grade” endpoint to choose which provisional grade to publish
        for a particular submission.
        
        Students not in the moderation set will have their one
        and only provisional grade published.
        
        WARNING: This is irreversible. This will overwrite existing grades in the gradebook.

        Endpoint: POST /api/v1/courses/:course_id/assignments/:assignment_id/provisional_grades

        Reference: /publish         <https://canvas.instructure.com/doc/api/all_resources.html#method.provisional_grades.publish
        """
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/assignments/{}/provisional_grades/publish'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def publish_provisional_grades_async(self, **kwargs) -> 'dict':
        """
        Publish the selected provisional grade for all submissions to an assignment.
        Use the “Select provisional grade” endpoint to choose which provisional grade to publish
        for a particular submission.
        
        Students not in the moderation set will have their one
        and only provisional grade published.
        
        WARNING: This is irreversible. This will overwrite existing grades in the gradebook.

        Endpoint: POST /api/v1/courses/:course_id/assignments/:assignment_id/provisional_grades

        Reference: /publish         <https://canvas.instructure.com/doc/api/all_resources.html#method.provisional_grades.publish
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/assignments/{}/provisional_grades/publish'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def select_students_for_moderation(self, **kwargs) -> 'PaginatedList[User]':
        """
        Select student(s) for moderation.

        Endpoint: POST /api/v1/courses/:course_id/assignments/:assignment_id/moderated_students

        Reference: https://canvas.instructure.com/doc/api/moderated_grading.html#method.moderation_set.create
        """
        return PaginatedList(User, self._requester, 'POST', 'courses/{}/assignments/{}/moderated_students'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))

    async def select_students_for_moderation_async(self, **kwargs) -> 'PaginatedList[User]':
        """
        Select student(s) for moderation.

        Endpoint: POST /api/v1/courses/:course_id/assignments/:assignment_id/moderated_students

        Reference: https://canvas.instructure.com/doc/api/moderated_grading.html#method.moderation_set.create
        """
        return PaginatedList(User, self._requester, 'POST', 'courses/{}/assignments/{}/moderated_students'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))

    def selected_provisional_grade(self, provisional_grade_id: 'int', **kwargs) -> 'dict':
        """
        Choose which provisional grade the student should receive for a submission.
        The caller must be the final grader for the assignment
        or an admin with :select_final_grade rights.

        Endpoint: PUT /api/v1/courses/:course_id/assignments/:assignment_id/provisional_grades/

        Reference: :provisonal_grade_id/select         <https://canvas.instructure.com/doc/api/all_resources.html#method.provisional_grades.select

        Parameters:
            provisional_grade_id: int
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/assignments/{}/provisional_grades/{}/select'.format(self.course_id, self.id, provisional_grade_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def selected_provisional_grade_async(self, provisional_grade_id: 'int', **kwargs) -> 'dict':
        """
        Choose which provisional grade the student should receive for a submission.
        The caller must be the final grader for the assignment
        or an admin with :select_final_grade rights.

        Endpoint: PUT /api/v1/courses/:course_id/assignments/:assignment_id/provisional_grades/

        Reference: :provisonal_grade_id/select         <https://canvas.instructure.com/doc/api/all_resources.html#method.provisional_grades.select

        Parameters:
            provisional_grade_id: int
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/assignments/{}/provisional_grades/{}/select'.format(self.course_id, self.id, provisional_grade_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def set_extensions(self, assignment_extensions: 'list', **kwargs) -> 'list[AssignmentExtension]':
        """
        Set extensions for student assignment submissions

        Endpoint: POST /api/v1/courses/:course_id/assignments/:assignment_id/extensions

        Reference: https://canvas.instructure.com/doc/api/assignment_extensions.html#method.assignment_extensions.create

        Parameters:
            assignment_extensions: list
        """
        if not isinstance(assignment_extensions, list) or not assignment_extensions:
            raise ValueError('Param `assignment_extensions` must be a non-empty list.')
        if any((not isinstance(extension, dict) for extension in assignment_extensions)):
            raise ValueError('Param `assignment_extensions` must only contain dictionaries')
        if any(('user_id' not in extension for extension in assignment_extensions)):
            raise RequiredFieldMissing('Dictionaries in `assignment_extensions` must contain key `user_id`')
        kwargs['assignment_extensions'] = assignment_extensions
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/assignments/{}/extensions'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        extension_list = response.json()['assignment_extensions']
        return [AssignmentExtension(self._requester, extension) for extension in extension_list]

    async def set_extensions_async(self, assignment_extensions: 'list', **kwargs) -> 'list[AssignmentExtension]':
        """
        Set extensions for student assignment submissions

        Endpoint: POST /api/v1/courses/:course_id/assignments/:assignment_id/extensions

        Reference: https://canvas.instructure.com/doc/api/assignment_extensions.html#method.assignment_extensions.create

        Parameters:
            assignment_extensions: list
        """
        if not isinstance(assignment_extensions, list) or not assignment_extensions:
            raise ValueError('Param `assignment_extensions` must be a non-empty list.')
        if any((not isinstance(extension, dict) for extension in assignment_extensions)):
            raise ValueError('Param `assignment_extensions` must only contain dictionaries')
        if any(('user_id' not in extension for extension in assignment_extensions)):
            raise RequiredFieldMissing('Dictionaries in `assignment_extensions` must contain key `user_id`')
        kwargs['assignment_extensions'] = assignment_extensions
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/assignments/{}/extensions'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        extension_list = response.json()['assignment_extensions']
        return [AssignmentExtension(self._requester, extension) for extension in extension_list]

    def show_provisonal_grades_for_student(self, anonymous_id: 'User | int', **kwargs) -> 'dict':
        """
        

        Parameters:
            anonymous_id: :class:`canvasapi.user.User` or int
        """
        kwargs['anonymous_id'] = obj_or_id(anonymous_id, 'anonymous_id', (User,))
        request: 'httpx.Response' = self._requester.request('GET', 'courses/{}/assignments/{}/anonymous_provisional_grades/status'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return request.json().get('needs_provisional_grade')

    async def show_provisonal_grades_for_student_async(self, anonymous_id: 'User | int', **kwargs) -> 'dict':
        """
        

        Parameters:
            anonymous_id: :class:`canvasapi.user.User` or int
        """
        kwargs['anonymous_id'] = obj_or_id(anonymous_id, 'anonymous_id', (User,))
        request: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/assignments/{}/anonymous_provisional_grades/status'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return request.json().get('needs_provisional_grade')

    def submissions_bulk_update(self, **kwargs) -> 'Progress':
        """
        Update the grading and comments on multiple student's assignment
        submissions in an asynchronous job.

        Endpoint: POST /api/v1/courses/:course_id/assignments/:assignment_id/

        Reference: submissions/update_grades         <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.bulk_update
        """
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/assignments/{}/submissions/update_grades'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return Progress(self._requester, response.json())

    async def submissions_bulk_update_async(self, **kwargs) -> 'Progress':
        """
        Update the grading and comments on multiple student's assignment
        submissions in an asynchronous job.

        Endpoint: POST /api/v1/courses/:course_id/assignments/:assignment_id/

        Reference: submissions/update_grades         <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.bulk_update
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/assignments/{}/submissions/update_grades'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return Progress(self._requester, response.json())

    def submit(self, submission: 'dict', file: 'str | None'=None, **kwargs) -> 'Submission':
        """
        Makes a submission for an assignment.

        Endpoint: POST /api/v1/courses/:course_id/assignments/:assignment_id/submissions

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions.create

        Parameters:
            submission: dict
            file: file or str
        """
        if isinstance(submission, dict) and 'submission_type' in submission:
            kwargs['submission'] = submission
        else:
            raise RequiredFieldMissing("Dictionary with key 'submission_type' is required.")
        if file:
            if submission.get('submission_type') != 'online_upload':
                raise ValueError("To upload a file, `submission['submission_type']` must be `online_upload`.")
            upload_response = self.upload_to_submission(file, **kwargs)
            if upload_response[0]:
                kwargs['submission']['file_ids'] = [upload_response[1]['id']]
            else:
                raise CanvasException('File upload failed. Not submitting.')
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/assignments/{}/submissions'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update(course_id=self.course_id)
        return Submission(self._requester, response_json)

    async def submit_async(self, submission: 'dict', file: 'str | None'=None, **kwargs) -> 'Submission':
        """
        Makes a submission for an assignment.

        Endpoint: POST /api/v1/courses/:course_id/assignments/:assignment_id/submissions

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions.create

        Parameters:
            submission: dict
            file: file or str
        """
        if isinstance(submission, dict) and 'submission_type' in submission:
            kwargs['submission'] = submission
        else:
            raise RequiredFieldMissing("Dictionary with key 'submission_type' is required.")
        if file:
            if submission.get('submission_type') != 'online_upload':
                raise ValueError("To upload a file, `submission['submission_type']` must be `online_upload`.")
            upload_response = self.upload_to_submission(file, **kwargs)
            if upload_response[0]:
                kwargs['submission']['file_ids'] = [upload_response[1]['id']]
            else:
                raise CanvasException('File upload failed. Not submitting.')
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/assignments/{}/submissions'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update(course_id=self.course_id)
        return Submission(self._requester, response_json)

    def upload_to_submission(self, file: 'FileOrPathLike | FileLike', user: 'User | int | str'='self', **kwargs) -> 'tuple':
        """
        Upload a file to a submission.

        Endpoint: POST /api/v1/courses/:course_id/assignments/:assignment_id/

        Reference: submissions/:user_id/files         <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.create_file

        Parameters:
            file: FileLike
            user: :class:`canvasapi.user.User`, int, or str
        """
        user_id = obj_or_id(user, 'user', (User,))
        return Uploader(self._requester, 'courses/{}/assignments/{}/submissions/{}/files'.format(self.course_id, self.id, user_id), file, **kwargs).start()

    async def upload_to_submission_async(self, file: 'FileOrPathLike | FileLike', user: 'User | int | str'='self', **kwargs) -> 'tuple':
        """
        Upload a file to a submission.

        Endpoint: POST /api/v1/courses/:course_id/assignments/:assignment_id/

        Reference: submissions/:user_id/files         <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.create_file

        Parameters:
            file: FileLike
            user: :class:`canvasapi.user.User`, int, or str
        """
        user_id = obj_or_id(user, 'user', (User,))
        return Uploader(self._requester, 'courses/{}/assignments/{}/submissions/{}/files'.format(self.course_id, self.id, user_id), file, **kwargs).start()

class AssignmentExtension(AssignmentExtensionModel):

    def __str__(self):
        return '{} ({})'.format(self.assignment_id, self.user_id)

class AssignmentGroup(AssignmentGroupModel):

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)

    def delete(self, **kwargs) -> 'AssignmentGroup':
        """
        Delete this assignment.

        Endpoint: DELETE /api/v1/courses/:course_id/assignment_groups/:assignment_group_id

        Reference: https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/assignment_groups/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return AssignmentGroup(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'AssignmentGroup':
        """
        Delete this assignment.

        Endpoint: DELETE /api/v1/courses/:course_id/assignment_groups/:assignment_group_id

        Reference: https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/assignment_groups/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return AssignmentGroup(self._requester, response.json())

    def edit(self, **kwargs) -> 'AssignmentGroup':
        """
        Modify this assignment group.

        Endpoint: PUT /api/v1/courses/:course_id/assignment_groups/:assignment_group_id

        Reference: https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/assignment_groups/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        if 'name' in response.json():
            super(AssignmentGroup, self).set_attributes(response.json())
        return AssignmentGroup(self._requester, response.json())

    async def edit_async(self, **kwargs) -> 'AssignmentGroup':
        """
        Modify this assignment group.

        Endpoint: PUT /api/v1/courses/:course_id/assignment_groups/:assignment_group_id

        Reference: https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/assignment_groups/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        if 'name' in response.json():
            super(AssignmentGroup, self).set_attributes(response.json())
        return AssignmentGroup(self._requester, response.json())

class AssignmentOverride(AssignmentOverrideModel):

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)

    def delete(self, **kwargs) -> 'AssignmentGroup':
        """
        Delete this assignment override.

        Endpoint: DELETE /api/v1/courses/:course_id/assignments/:assignment_id/overrides/:id

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/assignments/{}/overrides/{}'.format(self.course_id, self.assignment_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update(course_id=self.course_id)
        return AssignmentOverride(self._requester, response_json)

    async def delete_async(self, **kwargs) -> 'AssignmentGroup':
        """
        Delete this assignment override.

        Endpoint: DELETE /api/v1/courses/:course_id/assignments/:assignment_id/overrides/:id

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/assignments/{}/overrides/{}'.format(self.course_id, self.assignment_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update(course_id=self.course_id)
        return AssignmentOverride(self._requester, response_json)

    def edit(self, **kwargs) -> 'AssignmentOverride':
        """
        Update this assignment override.
        
        Note: All current overridden values must be supplied if they are to be retained.

        Endpoint: PUT /api/v1/courses/:course_id/assignments/:assignment_id/overrides/:id

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/assignments/{}/overrides/{}'.format(self.course_id, self.assignment_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update(course_id=self.course_id)
        if 'title' in response_json:
            super(AssignmentOverride, self).set_attributes(response_json)
        return self

    async def edit_async(self, **kwargs) -> 'AssignmentOverride':
        """
        Update this assignment override.
        
        Note: All current overridden values must be supplied if they are to be retained.

        Endpoint: PUT /api/v1/courses/:course_id/assignments/:assignment_id/overrides/:id

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/assignments/{}/overrides/{}'.format(self.course_id, self.assignment_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update(course_id=self.course_id)
        if 'title' in response_json:
            super(AssignmentOverride, self).set_attributes(response_json)
        return self