from ..models.grading_periods import GradingPeriod as GradingPeriodModel
import httpx
import typing
from .canvas_object import CanvasObject
from .exceptions import RequiredFieldMissing
from .util import combine_kwargs

class GradingPeriod(GradingPeriodModel):

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)

    def delete(self, **kwargs) -> 'int':
        """
        Delete a grading period for a course.

        Endpoint: DELETE /api/v1/courses/:course_id/grading_periods/:id

        Reference: https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.update
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/grading_periods/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code

    async def delete_async(self, **kwargs) -> 'int':
        """
        Delete a grading period for a course.

        Endpoint: DELETE /api/v1/courses/:course_id/grading_periods/:id

        Reference: https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.update
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/grading_periods/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code

    def update(self, grading_period: 'list[dict]', **kwargs) -> 'GradingPeriod':
        """
        Update a grading period for a course.

        Endpoint: PUT /api/v1/courses/:course_id/grading_periods/:id

        Reference: https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.update

        Parameters:
            grading_period: list[dict]
        """
        if isinstance(grading_period, list):
            kwargs['grading_periods'] = grading_period
        else:
            raise RequiredFieldMissing('List is required')
        if 'start_date' not in kwargs['grading_periods'][0]:
            raise RequiredFieldMissing('start_date is missing')
        if 'end_date' not in kwargs['grading_periods'][0]:
            raise RequiredFieldMissing('end_date is missing')
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/grading_periods/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        grading_period = response_json['grading_periods'][0]
        grading_period.update({'course_id': self.course_id})
        return GradingPeriod(self._requester, grading_period)

    async def update_async(self, grading_period: 'list[dict]', **kwargs) -> 'GradingPeriod':
        """
        Update a grading period for a course.

        Endpoint: PUT /api/v1/courses/:course_id/grading_periods/:id

        Reference: https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.update

        Parameters:
            grading_period: list[dict]
        """
        if isinstance(grading_period, list):
            kwargs['grading_periods'] = grading_period
        else:
            raise RequiredFieldMissing('List is required')
        if 'start_date' not in kwargs['grading_periods'][0]:
            raise RequiredFieldMissing('start_date is missing')
        if 'end_date' not in kwargs['grading_periods'][0]:
            raise RequiredFieldMissing('end_date is missing')
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/grading_periods/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        grading_period = response_json['grading_periods'][0]
        grading_period.update({'course_id': self.course_id})
        return GradingPeriod(self._requester, grading_period)