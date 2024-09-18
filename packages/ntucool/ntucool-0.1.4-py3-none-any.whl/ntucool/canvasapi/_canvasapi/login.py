import httpx
import typing
if typing.TYPE_CHECKING:
    from .authentication_event import AuthenticationEvent
    from .paginated_list import PaginatedList
from .canvas_object import CanvasObject
from .paginated_list import PaginatedList
from .util import combine_kwargs

class Login(CanvasObject):

    def __str__(self):
        return '{} ({})'.format(self.id, self.unique_id)

    def delete(self, **kwargs) -> 'Login':
        """
        Delete an existing login.

        Endpoint: DELETE /api/v1/users/:user_id/logins/:id

        Reference: https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'users/{}/logins/{}'.format(self.user_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return Login(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'Login':
        """
        Delete an existing login.

        Endpoint: DELETE /api/v1/users/:user_id/logins/:id

        Reference: https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'users/{}/logins/{}'.format(self.user_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return Login(self._requester, response.json())

    def edit(self, **kwargs) -> 'Login':
        """
        Update an existing login for a user in the given account.

        Endpoint: PUT /api/v1/accounts/:account_id/logins/:id

        Reference: https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'accounts/{}/logins/{}'.format(self.account_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return Login(self._requester, response.json())

    async def edit_async(self, **kwargs) -> 'Login':
        """
        Update an existing login for a user in the given account.

        Endpoint: PUT /api/v1/accounts/:account_id/logins/:id

        Reference: https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'accounts/{}/logins/{}'.format(self.account_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return Login(self._requester, response.json())

    def get_authentication_events(self, **kwargs) -> 'PaginatedList[AuthenticationEvent]':
        """
        List authentication events for a given login.

        Endpoint: GET /api/v1/audit/authentication/logins/:login_id

        Reference: https://canvas.instructure.com/doc/api/authentications_log.html#method.authentication_audit_api.for_login
        """
        from .authentication_event import AuthenticationEvent
        return PaginatedList(AuthenticationEvent, self._requester, 'GET', 'audit/authentication/logins/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_authentication_events_async(self, **kwargs) -> 'PaginatedList[AuthenticationEvent]':
        """
        List authentication events for a given login.

        Endpoint: GET /api/v1/audit/authentication/logins/:login_id

        Reference: https://canvas.instructure.com/doc/api/authentications_log.html#method.authentication_audit_api.for_login
        """
        from .authentication_event import AuthenticationEvent
        return PaginatedList(AuthenticationEvent, self._requester, 'GET', 'audit/authentication/logins/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))