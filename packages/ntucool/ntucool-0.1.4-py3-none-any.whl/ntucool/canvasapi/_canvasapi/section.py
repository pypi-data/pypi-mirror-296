from ..models.sections import Section as SectionModel
import httpx
import typing
if typing.TYPE_CHECKING:
    from .progress import Progress
    from .submission import Submission
    from .paginated_list import PaginatedList
    from .assignment import Assignment, AssignmentOverride
    from .enrollment import Enrollment
    from .user import User
    from .course import Course
from .canvas_object import CanvasObject
from .enrollment import Enrollment
from .paginated_list import PaginatedList
from .progress import Progress
from .submission import GroupedSubmission, Submission
from .user import User
from .util import combine_kwargs, normalize_bool, obj_or_id

class Section(SectionModel):

    def __str__(self):
        return '{} - {} ({})'.format(self.name, self.course_id, self.id)

    def cross_list_section(self, new_course: 'Course | int', **kwargs) -> 'Section':
        """
        Move the Section to another course.

        Endpoint: POST /api/v1/sections/:id/crosslist/:new_course_id

        Reference: https://canvas.instructure.com/doc/api/sections.html#method.sections.crosslist

        Parameters:
            new_course: :class:`canvasapi.course.Course` or int
        """
        from .course import Course
        new_course_id = obj_or_id(new_course, 'new_course', (Course,))
        response: 'httpx.Response' = self._requester.request('POST', 'sections/{}/crosslist/{}'.format(self.id, new_course_id), _kwargs=combine_kwargs(**kwargs))
        return Section(self._requester, response.json())

    async def cross_list_section_async(self, new_course: 'Course | int', **kwargs) -> 'Section':
        """
        Move the Section to another course.

        Endpoint: POST /api/v1/sections/:id/crosslist/:new_course_id

        Reference: https://canvas.instructure.com/doc/api/sections.html#method.sections.crosslist

        Parameters:
            new_course: :class:`canvasapi.course.Course` or int
        """
        from .course import Course
        new_course_id = obj_or_id(new_course, 'new_course', (Course,))
        response: 'httpx.Response' = await self._requester.request_async('POST', 'sections/{}/crosslist/{}'.format(self.id, new_course_id), _kwargs=combine_kwargs(**kwargs))
        return Section(self._requester, response.json())

    def decross_list_section(self, **kwargs) -> 'Section':
        """
        Undo cross-listing of a section.

        Endpoint: DELETE /api/v1/sections/:id/crosslist

        Reference: https://canvas.instructure.com/doc/api/sections.html#method.sections.uncrosslist
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'sections/{}/crosslist'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Section(self._requester, response.json())

    async def decross_list_section_async(self, **kwargs) -> 'Section':
        """
        Undo cross-listing of a section.

        Endpoint: DELETE /api/v1/sections/:id/crosslist

        Reference: https://canvas.instructure.com/doc/api/sections.html#method.sections.uncrosslist
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'sections/{}/crosslist'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Section(self._requester, response.json())

    def delete(self, **kwargs) -> 'Section':
        """
        Delete a target section.

        Endpoint: DELETE /api/v1/sections/:id

        Reference: https://canvas.instructure.com/doc/api/sections.html#method.sections.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'sections/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Section(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'Section':
        """
        Delete a target section.

        Endpoint: DELETE /api/v1/sections/:id

        Reference: https://canvas.instructure.com/doc/api/sections.html#method.sections.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'sections/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Section(self._requester, response.json())

    def edit(self, **kwargs) -> 'Section':
        """
        Edit contents of a target section.

        Endpoint: PUT /api/v1/sections/:id

        Reference: https://canvas.instructure.com/doc/api/sections.html#method.sections.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'sections/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if 'name' in response.json():
            super(Section, self).set_attributes(response.json())
        return self

    async def edit_async(self, **kwargs) -> 'Section':
        """
        Edit contents of a target section.

        Endpoint: PUT /api/v1/sections/:id

        Reference: https://canvas.instructure.com/doc/api/sections.html#method.sections.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'sections/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if 'name' in response.json():
            super(Section, self).set_attributes(response.json())
        return self

    def enroll_user(self, user: 'User | int', **kwargs) -> 'Enrollment':
        """
        Create a new user enrollment for a course or a section.

        Endpoint: POST /api/v1/section/:section_id/enrollments

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.create

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        kwargs['enrollment[user_id]'] = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = self._requester.request('POST', 'sections/{}/enrollments'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Enrollment(self._requester, response.json())

    async def enroll_user_async(self, user: 'User | int', **kwargs) -> 'Enrollment':
        """
        Create a new user enrollment for a course or a section.

        Endpoint: POST /api/v1/section/:section_id/enrollments

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.create

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        kwargs['enrollment[user_id]'] = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = await self._requester.request_async('POST', 'sections/{}/enrollments'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Enrollment(self._requester, response.json())

    def get_assignment_override(self, assignment: 'Assignment | int', **kwargs) -> 'AssignmentOverride':
        """
        Return override for the specified assignment for this section.

        Endpoint: GET /api/v1/sections/:course_section_id/assignments/:assignment_id/override

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.section_alias

        Parameters:
            assignment: :class:`canvasapi.assignment.Assignment` or int
        """
        from .assignment import Assignment, AssignmentOverride
        assignment_id = obj_or_id(assignment, 'assignment', (Assignment,))
        response: 'httpx.Response' = self._requester.request('GET', 'sections/{}/assignments/{}/override'.format(self.id, assignment_id))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return AssignmentOverride(self._requester, response_json)

    async def get_assignment_override_async(self, assignment: 'Assignment | int', **kwargs) -> 'AssignmentOverride':
        """
        Return override for the specified assignment for this section.

        Endpoint: GET /api/v1/sections/:course_section_id/assignments/:assignment_id/override

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.section_alias

        Parameters:
            assignment: :class:`canvasapi.assignment.Assignment` or int
        """
        from .assignment import Assignment, AssignmentOverride
        assignment_id = obj_or_id(assignment, 'assignment', (Assignment,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'sections/{}/assignments/{}/override'.format(self.id, assignment_id))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return AssignmentOverride(self._requester, response_json)

    def get_enrollments(self, **kwargs) -> 'PaginatedList[Enrollment]':
        """
        List all of the enrollments for the current user.

        Endpoint: GET /api/v1/sections/:section_id/enrollments

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index
        """
        from .enrollment import Enrollment
        return PaginatedList(Enrollment, self._requester, 'GET', 'sections/{}/enrollments'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_enrollments_async(self, **kwargs) -> 'PaginatedList[Enrollment]':
        """
        List all of the enrollments for the current user.

        Endpoint: GET /api/v1/sections/:section_id/enrollments

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index
        """
        from .enrollment import Enrollment
        return PaginatedList(Enrollment, self._requester, 'GET', 'sections/{}/enrollments'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_multiple_submissions(self, **kwargs) -> 'PaginatedList[Submission]':
        """
        List submissions for multiple assignments.
        Get all existing submissions for a given set of students and assignments.

        Endpoint: GET /api/v1/sections/:section_id/students/submissions

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.for_students
        """
        is_grouped = kwargs.get('grouped', False)
        if normalize_bool(is_grouped, 'grouped'):
            cls = GroupedSubmission
        else:
            cls = Submission
        return PaginatedList(cls, self._requester, 'GET', 'sections/{}/students/submissions'.format(self.id), {'section_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_multiple_submissions_async(self, **kwargs) -> 'PaginatedList[Submission]':
        """
        List submissions for multiple assignments.
        Get all existing submissions for a given set of students and assignments.

        Endpoint: GET /api/v1/sections/:section_id/students/submissions

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.for_students
        """
        is_grouped = kwargs.get('grouped', False)
        if normalize_bool(is_grouped, 'grouped'):
            cls = GroupedSubmission
        else:
            cls = Submission
        return PaginatedList(cls, self._requester, 'GET', 'sections/{}/students/submissions'.format(self.id), {'section_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def submissions_bulk_update(self, **kwargs) -> 'Progress':
        """
        Update the grading and comments on multiple student's assignment
        submissions in an asynchronous job.

        Endpoint: POST /api/v1/sections/:section_id/submissions/update_grades

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.bulk_update
        """
        response: 'httpx.Response' = self._requester.request('POST', 'sections/{}/submissions/update_grades'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Progress(self._requester, response.json())

    async def submissions_bulk_update_async(self, **kwargs) -> 'Progress':
        """
        Update the grading and comments on multiple student's assignment
        submissions in an asynchronous job.

        Endpoint: POST /api/v1/sections/:section_id/submissions/update_grades

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.bulk_update
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'sections/{}/submissions/update_grades'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Progress(self._requester, response.json())