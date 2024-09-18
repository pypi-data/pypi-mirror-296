from ..models.calendar_events import CalendarEvent as CalendarEventModel
import httpx
import typing
from .canvas_object import CanvasObject
from .util import combine_kwargs

class CalendarEvent(CalendarEventModel):

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)

    def delete(self, **kwargs) -> 'CalendarEvent':
        """
        Delete this calendar event.

        Endpoint: DELETE /api/v1/calendar_events/:id

        Reference: https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'calendar_events/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return CalendarEvent(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'CalendarEvent':
        """
        Delete this calendar event.

        Endpoint: DELETE /api/v1/calendar_events/:id

        Reference: https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'calendar_events/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return CalendarEvent(self._requester, response.json())

    def edit(self, **kwargs) -> 'CalendarEvent':
        """
        Modify this calendar event.

        Endpoint: PUT /api/v1/calendar_events/:id

        Reference: https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'calendar_events/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if 'title' in response.json():
            super(CalendarEvent, self).set_attributes(response.json())
        return CalendarEvent(self._requester, response.json())

    async def edit_async(self, **kwargs) -> 'CalendarEvent':
        """
        Modify this calendar event.

        Endpoint: PUT /api/v1/calendar_events/:id

        Reference: https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'calendar_events/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if 'title' in response.json():
            super(CalendarEvent, self).set_attributes(response.json())
        return CalendarEvent(self._requester, response.json())