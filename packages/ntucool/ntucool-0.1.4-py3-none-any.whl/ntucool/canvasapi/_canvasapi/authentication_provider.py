from ..models.authentication_providers import AuthenticationProvider as AuthenticationProviderModel
import httpx
import typing
from .canvas_object import CanvasObject
from .util import combine_kwargs

class AuthenticationProvider(AuthenticationProviderModel):

    def __str__(self):
        return '{} ({})'.format(self.auth_type, self.position)

    def delete(self, **kwargs) -> 'AuthenticationProvider':
        """
        Delete the config

        Endpoint: DELETE /api/v1/accounts/:account_id/authentication_providers/:id

        Reference: https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'accounts/{}/authentication_providers/{}'.format(self.account_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return AuthenticationProvider(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'AuthenticationProvider':
        """
        Delete the config

        Endpoint: DELETE /api/v1/accounts/:account_id/authentication_providers/:id

        Reference: https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'accounts/{}/authentication_providers/{}'.format(self.account_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return AuthenticationProvider(self._requester, response.json())

    def update(self, **kwargs) -> 'AuthenticationProvider':
        """
        Update an authentication provider using the same options as the create endpoint

        Endpoint: PUT /api/v1/accounts/:account_id/authentication_providers/:id

        Reference: https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'accounts/{}/authentication_providers/{}'.format(self.account_id, self.id), _kwargs=combine_kwargs(**kwargs))
        if response.json().get('auth_type'):
            super(AuthenticationProvider, self).set_attributes(response.json())
        return response.json().get('auth_type')

    async def update_async(self, **kwargs) -> 'AuthenticationProvider':
        """
        Update an authentication provider using the same options as the create endpoint

        Endpoint: PUT /api/v1/accounts/:account_id/authentication_providers/:id

        Reference: https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'accounts/{}/authentication_providers/{}'.format(self.account_id, self.id), _kwargs=combine_kwargs(**kwargs))
        if response.json().get('auth_type'):
            super(AuthenticationProvider, self).set_attributes(response.json())
        return response.json().get('auth_type')