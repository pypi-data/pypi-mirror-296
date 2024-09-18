from ..models.planner import PlannerNote as PlannerNoteModel, PlannerOverride as PlannerOverrideModel
import httpx
import typing
from .canvas_object import CanvasObject
from .util import combine_kwargs

class PlannerNote(PlannerNoteModel):

    def __str__(self):
        return '{} {} ({})'.format(self.title, self.todo_date, self.id)

    def delete(self, **kwargs) -> 'PlannerNote':
        """
        Delete a planner note for the current user

        Endpoint: DELETE /api/v1/planner_notes/:id

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_notes.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'planner_notes/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return PlannerNote(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'PlannerNote':
        """
        Delete a planner note for the current user

        Endpoint: DELETE /api/v1/planner_notes/:id

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_notes.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'planner_notes/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return PlannerNote(self._requester, response.json())

    def update(self, **kwargs) -> 'PlannerNote':
        """
        Update a planner note for the current user

        Endpoint: PUT /api/v1/planner_notes/:id

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_notes.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'planner_notes/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return PlannerNote(self._requester, response.json())

    async def update_async(self, **kwargs) -> 'PlannerNote':
        """
        Update a planner note for the current user

        Endpoint: PUT /api/v1/planner_notes/:id

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_notes.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'planner_notes/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return PlannerNote(self._requester, response.json())

class PlannerOverride(PlannerOverrideModel):

    def __str__(self):
        return '{} {} ({})'.format(self.plannable_id, self.marked_complete, self.id)

    def delete(self, **kwargs) -> 'PlannerOverride':
        """
        Delete a planner override for the current user

        Endpoint: DELETE /api/v1/planner/overrides/:id

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_overrides.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'planner/overrides/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return PlannerOverride(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'PlannerOverride':
        """
        Delete a planner override for the current user

        Endpoint: DELETE /api/v1/planner/overrides/:id

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_overrides.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'planner/overrides/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return PlannerOverride(self._requester, response.json())

    def update(self, **kwargs) -> 'PlannerOverride':
        """
        Update a planner override's visibilty for the current user

        Endpoint: PUT /api/v1/planner/overrides/:id

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_overrides.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'planner/overrides/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return PlannerOverride(self._requester, response.json())

    async def update_async(self, **kwargs) -> 'PlannerOverride':
        """
        Update a planner override's visibilty for the current user

        Endpoint: PUT /api/v1/planner/overrides/:id

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_overrides.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'planner/overrides/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return PlannerOverride(self._requester, response.json())