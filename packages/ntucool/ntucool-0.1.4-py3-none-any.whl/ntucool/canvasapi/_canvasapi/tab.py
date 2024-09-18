from ..models.tabs import Tab as TabModel
import httpx
import typing
from .canvas_object import CanvasObject
from .util import combine_kwargs

class Tab(TabModel):

    def __str__(self):
        return '{} ({})'.format(self.label, self.id)

    def update(self, **kwargs) -> 'Tab':
        """
        Update a tab for a course.
        
        Note: Home and Settings tabs are not manageable, and can't be
        hidden or moved.

        Endpoint: PUT /api/v1/courses/:course_id/tabs/:tab_id

        Reference: https://canvas.instructure.com/doc/api/tabs.html#method.tabs.update
        """
        if not hasattr(self, 'course_id'):
            raise ValueError('Can only update tabs from a Course.')
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/tabs/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        super(Tab, self).set_attributes(response_json)
        return self

    async def update_async(self, **kwargs) -> 'Tab':
        """
        Update a tab for a course.
        
        Note: Home and Settings tabs are not manageable, and can't be
        hidden or moved.

        Endpoint: PUT /api/v1/courses/:course_id/tabs/:tab_id

        Reference: https://canvas.instructure.com/doc/api/tabs.html#method.tabs.update
        """
        if not hasattr(self, 'course_id'):
            raise ValueError('Can only update tabs from a Course.')
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/tabs/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        super(Tab, self).set_attributes(response_json)
        return self