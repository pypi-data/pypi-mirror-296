from ..models.communication_channels import CommunicationChannel as CommunicationChannelModel
import httpx
import typing
if typing.TYPE_CHECKING:
    from .notification_preference import NotificationPreference
from .canvas_object import CanvasObject
from .notification_preference import NotificationPreference
from .util import combine_kwargs

class CommunicationChannel(CommunicationChannelModel):

    def __str__(self):
        return '{} ({})'.format(self.address, self.id)

    def delete(self, **kwargs) -> 'bool':
        """
        Delete the current communication_channel

        Endpoint: DELETE /api/v1/users/:user_id/communication_channels/:id

        Reference: https://canvas.instructure.com/doc/api/communication_channels.html#method.communication_channels.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'users/{}/communication_channels/{}'.format(self.user_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('workflow_state') == 'deleted'

    async def delete_async(self, **kwargs) -> 'bool':
        """
        Delete the current communication_channel

        Endpoint: DELETE /api/v1/users/:user_id/communication_channels/:id

        Reference: https://canvas.instructure.com/doc/api/communication_channels.html#method.communication_channels.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'users/{}/communication_channels/{}'.format(self.user_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('workflow_state') == 'deleted'

    def get_preference(self, notification: 'str', **kwargs) -> 'NotificationPreference':
        """
        Fetch the preference for the given notification for the given
        communication channel.

        Endpoint: GET /api/v1/users/:user_id/communication_channels/

        Reference: :communication_channel_id/notification_preferences/:notification         <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.show

        Parameters:
            notification: str
        """
        response: 'httpx.Response' = self._requester.request('GET', 'users/{}/communication_channels/{}/notification_preferences/{}'.format(self.user_id, self.id, notification), _kwargs=combine_kwargs(**kwargs))
        data = response.json()['notification_preferences'][0]
        return NotificationPreference(self._requester, data)

    async def get_preference_async(self, notification: 'str', **kwargs) -> 'NotificationPreference':
        """
        Fetch the preference for the given notification for the given
        communication channel.

        Endpoint: GET /api/v1/users/:user_id/communication_channels/

        Reference: :communication_channel_id/notification_preferences/:notification         <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.show

        Parameters:
            notification: str
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'users/{}/communication_channels/{}/notification_preferences/{}'.format(self.user_id, self.id, notification), _kwargs=combine_kwargs(**kwargs))
        data = response.json()['notification_preferences'][0]
        return NotificationPreference(self._requester, data)

    def get_preference_categories(self, **kwargs) -> 'list':
        """
        Fetch all notification preference categories for the given communication
        channel.

        Endpoint: GET /api/v1/users/:user_id/communication_channels/

        Reference: :communication_channel_id/notification_preference_categories         <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.category_index
        """
        response: 'httpx.Response' = self._requester.request('GET', 'users/{}/communication_channels/{}/notification_preference_categories'.format(self.user_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()['categories']

    async def get_preference_categories_async(self, **kwargs) -> 'list':
        """
        Fetch all notification preference categories for the given communication
        channel.

        Endpoint: GET /api/v1/users/:user_id/communication_channels/

        Reference: :communication_channel_id/notification_preference_categories         <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.category_index
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'users/{}/communication_channels/{}/notification_preference_categories'.format(self.user_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()['categories']

    def get_preferences(self, **kwargs) -> 'list':
        """
        Fetch all preferences for the given communication channel.

        Endpoint: GET /api/v1/users/:user_id/communication_channels/:communication_channel_id/

        Reference: notification_preferences         <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.index
        """
        response: 'httpx.Response' = self._requester.request('GET', 'users/{}/communication_channels/{}/notification_preferences'.format(self.user_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()['notification_preferences']

    async def get_preferences_async(self, **kwargs) -> 'list':
        """
        Fetch all preferences for the given communication channel.

        Endpoint: GET /api/v1/users/:user_id/communication_channels/:communication_channel_id/

        Reference: notification_preferences         <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.index
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'users/{}/communication_channels/{}/notification_preferences'.format(self.user_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()['notification_preferences']

    def update_multiple_preferences(self, notification_preferences, **kwargs) -> 'NotificationPreference':
        """
        Change preferences for multiple notifications based on the category
        for a single communication channel.

        Endpoint: PUT /api/v1/users/self/communication_channels/:communication_channel_id/

        Reference: notification_preferences         <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.update_all
        """
        if isinstance(notification_preferences, dict) and notification_preferences:
            for key, value in notification_preferences.items():
                try:
                    if not value['frequency']:
                        return False
                except KeyError:
                    return False
            kwargs['notification_preferences'] = notification_preferences
            response: 'httpx.Response' = self._requester.request('PUT', 'users/self/communication_channels/{}/notification_preferences'.format(self.id), _kwargs=combine_kwargs(**kwargs))
            return response.json()['notification_preferences']
        return False

    async def update_multiple_preferences_async(self, notification_preferences, **kwargs) -> 'NotificationPreference':
        """
        Change preferences for multiple notifications based on the category
        for a single communication channel.

        Endpoint: PUT /api/v1/users/self/communication_channels/:communication_channel_id/

        Reference: notification_preferences         <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.update_all
        """
        if isinstance(notification_preferences, dict) and notification_preferences:
            for key, value in notification_preferences.items():
                try:
                    if not value['frequency']:
                        return False
                except KeyError:
                    return False
            kwargs['notification_preferences'] = notification_preferences
            response: 'httpx.Response' = await self._requester.request_async('PUT', 'users/self/communication_channels/{}/notification_preferences'.format(self.id), _kwargs=combine_kwargs(**kwargs))
            return response.json()['notification_preferences']
        return False

    def update_preference(self, notification: 'str', frequency: "str Can be 'immediately' | 'daily' | 'weekly' | 'never'", **kwargs) -> 'NotificationPreference':
        """
        Update the preference for the given notification for the given communication channel.

        Endpoint: PUT /api/v1/users/self/communication_channels/:communication_channel_id/

        Reference: notification_preferences/:notification         <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.update

        Parameters:
            notification: str
            frequency: str
Can be 'immediately', 'daily', 'weekly', or 'never'
        """
        kwargs['notification_preferences[frequency]'] = frequency
        response: 'httpx.Response' = self._requester.request('PUT', 'users/self/communication_channels/{}/notification_preferences/{}'.format(self.id, notification), _kwargs=combine_kwargs(**kwargs))
        data = response.json()['notification_preferences'][0]
        return NotificationPreference(self._requester, data)

    async def update_preference_async(self, notification: 'str', frequency: "str Can be 'immediately' | 'daily' | 'weekly' | 'never'", **kwargs) -> 'NotificationPreference':
        """
        Update the preference for the given notification for the given communication channel.

        Endpoint: PUT /api/v1/users/self/communication_channels/:communication_channel_id/

        Reference: notification_preferences/:notification         <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.update

        Parameters:
            notification: str
            frequency: str
Can be 'immediately', 'daily', 'weekly', or 'never'
        """
        kwargs['notification_preferences[frequency]'] = frequency
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'users/self/communication_channels/{}/notification_preferences/{}'.format(self.id, notification), _kwargs=combine_kwargs(**kwargs))
        data = response.json()['notification_preferences'][0]
        return NotificationPreference(self._requester, data)

    def update_preferences_by_catagory(self, category: 'str', frequency: "str Can be 'immediately' | 'daily' | 'weekly' | 'never'", **kwargs) -> 'NotificationPreference':
        """
        Change preferences for multiple notifications based on the category
        for a single communication channel.

        Endpoint: PUT /api/v1/users/self/communication_channels/:communication_channel_id/

        Reference: notification_preference_categories/:category         <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.update_preferences_by_category

        Parameters:
            category: str
            frequency: str
Can be 'immediately', 'daily', 'weekly', or 'never'
        """
        kwargs['notification_preferences[frequency]'] = frequency
        response: 'httpx.Response' = self._requester.request('PUT', 'users/self/communication_channels/{}/notification_preference_categories/{}'.format(self.id, category), _kwargs=combine_kwargs(**kwargs))
        return response.json()['notification_preferences']

    async def update_preferences_by_catagory_async(self, category: 'str', frequency: "str Can be 'immediately' | 'daily' | 'weekly' | 'never'", **kwargs) -> 'NotificationPreference':
        """
        Change preferences for multiple notifications based on the category
        for a single communication channel.

        Endpoint: PUT /api/v1/users/self/communication_channels/:communication_channel_id/

        Reference: notification_preference_categories/:category         <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.update_preferences_by_category

        Parameters:
            category: str
            frequency: str
Can be 'immediately', 'daily', 'weekly', or 'never'
        """
        kwargs['notification_preferences[frequency]'] = frequency
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'users/self/communication_channels/{}/notification_preference_categories/{}'.format(self.id, category), _kwargs=combine_kwargs(**kwargs))
        return response.json()['notification_preferences']