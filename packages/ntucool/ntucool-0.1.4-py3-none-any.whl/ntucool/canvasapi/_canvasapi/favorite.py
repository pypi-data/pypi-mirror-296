from ..models.favorites import Favorite as FavoriteModel
import httpx
import typing
from .canvas_object import CanvasObject
from .util import combine_kwargs

class Favorite(FavoriteModel):

    def __str__(self):
        return '{} ({})'.format(self.context_type, self.context_id)

    def remove(self, **kwargs) -> 'Favorite':
        """
        Remove a course or group from the current user's favorites.

        Endpoint: DELETE /api/v1/users/self/favorites/courses/:id

        Reference: https://canvas.instructure.com/doc/api/favorites.html#method.favorites.remove_favorite_course
        """
        if self.context_type.lower() == 'course':
            id = self.context_id
            uri_str = 'users/self/favorites/courses/{}'
        elif self.context_type.lower() == 'group':
            id = self.context_id
            uri_str = 'users/self/favorites/groups/{}'
        response: 'httpx.Response' = self._requester.request('DELETE', uri_str.format(id), _kwargs=combine_kwargs(**kwargs))
        return Favorite(self._requester, response.json())

    async def remove_async(self, **kwargs) -> 'Favorite':
        """
        Remove a course or group from the current user's favorites.

        Endpoint: DELETE /api/v1/users/self/favorites/courses/:id

        Reference: https://canvas.instructure.com/doc/api/favorites.html#method.favorites.remove_favorite_course
        """
        if self.context_type.lower() == 'course':
            id = self.context_id
            uri_str = 'users/self/favorites/courses/{}'
        elif self.context_type.lower() == 'group':
            id = self.context_id
            uri_str = 'users/self/favorites/groups/{}'
        response: 'httpx.Response' = await self._requester.request_async('DELETE', uri_str.format(id), _kwargs=combine_kwargs(**kwargs))
        return Favorite(self._requester, response.json())