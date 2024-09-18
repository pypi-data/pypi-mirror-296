import httpx
import typing
if typing.TYPE_CHECKING:
    from .account import Course, Account
from .canvas_object import CanvasObject
from .exceptions import CanvasException
from .util import combine_kwargs

class ExternalTool(CanvasObject):

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)

    @property
    def parent_id(self) -> 'int':
        """
        Return the id of the course or account that spawned this tool.
        """
        if hasattr(self, 'course_id'):
            return self.course_id
        elif hasattr(self, 'account_id'):
            return self.account_id
        else:
            raise ValueError('ExternalTool does not have a course_id or account_id')

    @property
    async def parent_id_async(self) -> 'int':
        """
        Return the id of the course or account that spawned this tool.
        """
        if hasattr(self, 'course_id'):
            return self.course_id
        elif hasattr(self, 'account_id'):
            return self.account_id
        else:
            raise ValueError('ExternalTool does not have a course_id or account_id')

    @property
    def parent_type(self) -> 'str':
        """
        Return whether the tool was spawned from a course or account.
        """
        if hasattr(self, 'course_id'):
            return 'course'
        elif hasattr(self, 'account_id'):
            return 'account'
        else:
            raise ValueError('ExternalTool does not have a course_id or account_id')

    @property
    async def parent_type_async(self) -> 'str':
        """
        Return whether the tool was spawned from a course or account.
        """
        if hasattr(self, 'course_id'):
            return 'course'
        elif hasattr(self, 'account_id'):
            return 'account'
        else:
            raise ValueError('ExternalTool does not have a course_id or account_id')

    def delete(self, **kwargs) -> 'ExternalTool':
        """
        Remove the specified external tool.

        Endpoint: DELETE /api/v1/courses/:course_id/external_tools/:external_tool_id

        Reference: https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', '{}s/{}/external_tools/{}'.format(self.parent_type, self.parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return ExternalTool(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'ExternalTool':
        """
        Remove the specified external tool.

        Endpoint: DELETE /api/v1/courses/:course_id/external_tools/:external_tool_id

        Reference: https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', '{}s/{}/external_tools/{}'.format(self.parent_type, self.parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return ExternalTool(self._requester, response.json())

    def edit(self, **kwargs) -> 'ExternalTool':
        """
        Update the specified external tool.

        Endpoint: PUT /api/v1/courses/:course_id/external_tools/:external_tool_id

        Reference: https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', '{}s/{}/external_tools/{}'.format(self.parent_type, self.parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        if 'name' in response_json:
            super(ExternalTool, self).set_attributes(response_json)
        return ExternalTool(self._requester, response_json)

    async def edit_async(self, **kwargs) -> 'ExternalTool':
        """
        Update the specified external tool.

        Endpoint: PUT /api/v1/courses/:course_id/external_tools/:external_tool_id

        Reference: https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', '{}s/{}/external_tools/{}'.format(self.parent_type, self.parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        if 'name' in response_json:
            super(ExternalTool, self).set_attributes(response_json)
        return ExternalTool(self._requester, response_json)

    def get_parent(self, **kwargs) -> 'Account | Course':
        """
        Return the object that spawned this tool.
        """
        from .account import Account
        from .course import Course
        response: 'httpx.Response' = self._requester.request('GET', '{}s/{}'.format(self.parent_type, self.parent_id), _kwargs=combine_kwargs(**kwargs))
        if self.parent_type == 'account':
            return Account(self._requester, response.json())
        elif self.parent_type == 'course':
            return Course(self._requester, response.json())

    async def get_parent_async(self, **kwargs) -> 'Account | Course':
        """
        Return the object that spawned this tool.
        """
        from .account import Account
        from .course import Course
        response: 'httpx.Response' = await self._requester.request_async('GET', '{}s/{}'.format(self.parent_type, self.parent_id), _kwargs=combine_kwargs(**kwargs))
        if self.parent_type == 'account':
            return Account(self._requester, response.json())
        elif self.parent_type == 'course':
            return Course(self._requester, response.json())

    def get_sessionless_launch_url(self, **kwargs) -> 'str':
        """
        Return a sessionless launch url for an external tool.

        Endpoint: GET /api/v1/courses/:course_id/external_tools/sessionless_launch

        Reference: https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.generate_sessionless_launch
        """
        kwargs['id'] = self.id
        response: 'httpx.Response' = self._requester.request('GET', '{}s/{}/external_tools/sessionless_launch'.format(self.parent_type, self.parent_id), _kwargs=combine_kwargs(**kwargs))
        try:
            return response.json()['url']
        except KeyError:
            raise CanvasException('Canvas did not respond with a valid URL')

    async def get_sessionless_launch_url_async(self, **kwargs) -> 'str':
        """
        Return a sessionless launch url for an external tool.

        Endpoint: GET /api/v1/courses/:course_id/external_tools/sessionless_launch

        Reference: https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.generate_sessionless_launch
        """
        kwargs['id'] = self.id
        response: 'httpx.Response' = await self._requester.request_async('GET', '{}s/{}/external_tools/sessionless_launch'.format(self.parent_type, self.parent_id), _kwargs=combine_kwargs(**kwargs))
        try:
            return response.json()['url']
        except KeyError:
            raise CanvasException('Canvas did not respond with a valid URL')