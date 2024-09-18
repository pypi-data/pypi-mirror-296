from ..models.files import File as FileModel
import httpx
import typing
from .canvas_object import CanvasObject
from .util import combine_kwargs

class File(FileModel):

    def __str__(self):
        return '{}'.format(self.display_name)

    def delete(self, **kwargs) -> 'File':
        """
        Delete this file.

        Endpoint: DELETE /api/v1/files/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'files/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return File(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'File':
        """
        Delete this file.

        Endpoint: DELETE /api/v1/files/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'files/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return File(self._requester, response.json())

    def download(self, location: 'str'):
        """
        Download the file to specified location.

        Parameters:
            location: str
        """
        response: 'httpx.Response' = self._requester.request('GET', _url=self.url)
        with open(location, 'wb') as file_out:
            file_out.write(response.content)

    async def download_async(self, location: 'str'):
        """
        Download the file to specified location.

        Parameters:
            location: str
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', _url=self.url)
        with open(location, 'wb') as file_out:
            file_out.write(response.content)

    def get_contents(self, binary=False) -> 'str | bytes':
        """
        Download the contents of this file.
        Pass binary=True to return a bytes object instead of a str.
        """
        response: 'httpx.Response' = self._requester.request('GET', _url=self.url)
        if binary:
            return response.content
        else:
            return response.text

    async def get_contents_async(self, binary=False) -> 'str | bytes':
        """
        Download the contents of this file.
        Pass binary=True to return a bytes object instead of a str.
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', _url=self.url)
        if binary:
            return response.content
        else:
            return response.text

    def update(self, **kwargs) -> 'File':
        """
        Update some settings on the specified file.

        Endpoint: PUT /api/v1/files/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'files/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return File(self._requester, response.json())

    async def update_async(self, **kwargs) -> 'File':
        """
        Update some settings on the specified file.

        Endpoint: PUT /api/v1/files/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'files/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return File(self._requester, response.json())