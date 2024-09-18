from ..models.appointment_groups import AppointmentGroup as AppointmentGroupModel
import httpx
import typing
from .canvas_object import CanvasObject
from .exceptions import RequiredFieldMissing
from .util import combine_kwargs

class AppointmentGroup(AppointmentGroupModel):

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)

    def delete(self, **kwargs) -> 'AppointmentGroup':
        """
        Delete this appointment group.

        Endpoint: DELETE /api/v1/appointment_groups/:id

        Reference: https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'appointment_groups/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return AppointmentGroup(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'AppointmentGroup':
        """
        Delete this appointment group.

        Endpoint: DELETE /api/v1/appointment_groups/:id

        Reference: https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'appointment_groups/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return AppointmentGroup(self._requester, response.json())

    def edit(self, appointment_group: 'dict', **kwargs) -> 'AppointmentGroup':
        """
        Modify this appointment group.

        Endpoint: PUT /api/v1/appointment_groups/:id

        Reference: https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.update

        Parameters:
            appointment_group: dict
        """
        if isinstance(appointment_group, dict) and 'context_codes' in appointment_group:
            kwargs['appointment_group'] = appointment_group
        else:
            raise RequiredFieldMissing("Dictionary with key 'context_code' is required.")
        response: 'httpx.Response' = self._requester.request('PUT', 'appointment_groups/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if 'title' in response.json():
            super(AppointmentGroup, self).set_attributes(response.json())
        return AppointmentGroup(self._requester, response.json())

    async def edit_async(self, appointment_group: 'dict', **kwargs) -> 'AppointmentGroup':
        """
        Modify this appointment group.

        Endpoint: PUT /api/v1/appointment_groups/:id

        Reference: https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.update

        Parameters:
            appointment_group: dict
        """
        if isinstance(appointment_group, dict) and 'context_codes' in appointment_group:
            kwargs['appointment_group'] = appointment_group
        else:
            raise RequiredFieldMissing("Dictionary with key 'context_code' is required.")
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'appointment_groups/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if 'title' in response.json():
            super(AppointmentGroup, self).set_attributes(response.json())
        return AppointmentGroup(self._requester, response.json())