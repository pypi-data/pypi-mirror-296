from ..models.enrollments import Enrollment as EnrollmentModel
import httpx
import typing
from .canvas_object import CanvasObject
from .util import combine_kwargs

class Enrollment(EnrollmentModel):

    def __str__(self):
        return '{} ({})'.format(self.type, self.id)

    def accept(self, **kwargs) -> 'bool':
        """
        Accept a pending course invitation.

        Endpoint: POST /api/v1/courses/:course_id/enrollments/:id/accept

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.accept
        """
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/enrollments/{}/accept'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('success', False)

    async def accept_async(self, **kwargs) -> 'bool':
        """
        Accept a pending course invitation.

        Endpoint: POST /api/v1/courses/:course_id/enrollments/:id/accept

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.accept
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/enrollments/{}/accept'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('success', False)

    def deactivate(self, task: 'str', **kwargs) -> 'Enrollment':
        """
        Delete, conclude, or deactivate an enrollment.
        
        The following tasks can be performed on an enrollment: conclude, delete,         inactivate, deactivate.

        Endpoint: DELETE /api/v1/courses/:course_id/enrollments/:id

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.destroy

        Parameters:
            task: str
        """
        ALLOWED_TASKS = ['conclude', 'delete', 'inactivate', 'deactivate']
        if task not in ALLOWED_TASKS:
            raise ValueError('{} is not a valid task. Please use one of the following: {}'.format(task, ','.join(ALLOWED_TASKS)))
        kwargs['task'] = task
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/enrollments/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return Enrollment(self._requester, response.json())

    async def deactivate_async(self, task: 'str', **kwargs) -> 'Enrollment':
        """
        Delete, conclude, or deactivate an enrollment.
        
        The following tasks can be performed on an enrollment: conclude, delete,         inactivate, deactivate.

        Endpoint: DELETE /api/v1/courses/:course_id/enrollments/:id

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.destroy

        Parameters:
            task: str
        """
        ALLOWED_TASKS = ['conclude', 'delete', 'inactivate', 'deactivate']
        if task not in ALLOWED_TASKS:
            raise ValueError('{} is not a valid task. Please use one of the following: {}'.format(task, ','.join(ALLOWED_TASKS)))
        kwargs['task'] = task
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/enrollments/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return Enrollment(self._requester, response.json())

    def reactivate(self, **kwargs) -> 'Enrollment':
        """
        Activate an inactive enrollment.

        Endpoint: PUT /api/v1/courses/:course_id/enrollments/:id/reactivate

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.reactivate
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/enrollments/{}/reactivate'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return Enrollment(self._requester, response.json())

    async def reactivate_async(self, **kwargs) -> 'Enrollment':
        """
        Activate an inactive enrollment.

        Endpoint: PUT /api/v1/courses/:course_id/enrollments/:id/reactivate

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.reactivate
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/enrollments/{}/reactivate'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return Enrollment(self._requester, response.json())

    def reject(self, **kwargs) -> 'bool':
        """
        Reject a pending course invitation.

        Endpoint: POST /api/v1/courses/:course_id/enrollments/:id/reject

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.reject
        """
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/enrollments/{}/reject'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('success', False)

    async def reject_async(self, **kwargs) -> 'bool':
        """
        Reject a pending course invitation.

        Endpoint: POST /api/v1/courses/:course_id/enrollments/:id/reject

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.reject
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/enrollments/{}/reject'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('success', False)