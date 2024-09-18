from ..models.bookmarks import Bookmark as BookmarkModel
import httpx
import typing
from .canvas_object import CanvasObject
from .util import combine_kwargs

class Bookmark(BookmarkModel):

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)

    def delete(self, **kwargs) -> 'Bookmark':
        """
        Delete this bookmark.

        Endpoint: DELETE /api/v1/users/self/bookmarks/:id

        Reference: https://canvas.instructure.com/doc/api/bookmarks.html#method.bookmarks/bookmarks.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'users/self/bookmarks/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Bookmark(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'Bookmark':
        """
        Delete this bookmark.

        Endpoint: DELETE /api/v1/users/self/bookmarks/:id

        Reference: https://canvas.instructure.com/doc/api/bookmarks.html#method.bookmarks/bookmarks.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'users/self/bookmarks/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Bookmark(self._requester, response.json())

    def edit(self, **kwargs) -> 'Bookmark':
        """
        Modify this bookmark.

        Endpoint: PUT /api/v1/users/self/bookmarks/:id

        Reference: https://canvas.instructure.com/doc/api/bookmarks.html#method.bookmarks/bookmarks.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'users/self/bookmarks/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if 'name' in response.json() and 'url' in response.json():
            super(Bookmark, self).set_attributes(response.json())
        return Bookmark(self._requester, response.json())

    async def edit_async(self, **kwargs) -> 'Bookmark':
        """
        Modify this bookmark.

        Endpoint: PUT /api/v1/users/self/bookmarks/:id

        Reference: https://canvas.instructure.com/doc/api/bookmarks.html#method.bookmarks/bookmarks.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'users/self/bookmarks/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if 'name' in response.json() and 'url' in response.json():
            super(Bookmark, self).set_attributes(response.json())
        return Bookmark(self._requester, response.json())