import httpx
import typing
if typing.TYPE_CHECKING:
    from .paginated_list import PaginatedList
    from .bookmark import Bookmark
    from .group import Group
    from .favorite import Favorite
    from .course import Course
from .bookmark import Bookmark
from .course import Course
from .favorite import Favorite
from .group import Group
from .paginated_list import PaginatedList
from .user import User
from .util import combine_kwargs, obj_or_id

class CurrentUser(User):

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)

    def add_favorite_course(self, course: 'Course | int', use_sis_id: 'bool'=False, **kwargs) -> 'Favorite':
        """
        Add a course to the current user's favorites. If the course is already
        in the user's favorites, nothing happens.

        Endpoint: POST /api/v1/users/self/favorites/courses/:id

        Reference: https://canvas.instructure.com/doc/api/favorites.html#method.favorites.add_favorite_course

        Parameters:
            course: :class:`canvasapi.course.Course` or int
            use_sis_id: bool
        """
        if use_sis_id:
            course_id = course
            uri_str = 'users/self/favorites/courses/sis_course_id:{}'
        else:
            course_id = obj_or_id(course, 'course', (Course,))
            uri_str = 'users/self/favorites/courses/{}'
        response: 'httpx.Response' = self._requester.request('POST', uri_str.format(course_id), _kwargs=combine_kwargs(**kwargs))
        return Favorite(self._requester, response.json())

    async def add_favorite_course_async(self, course: 'Course | int', use_sis_id: 'bool'=False, **kwargs) -> 'Favorite':
        """
        Add a course to the current user's favorites. If the course is already
        in the user's favorites, nothing happens.

        Endpoint: POST /api/v1/users/self/favorites/courses/:id

        Reference: https://canvas.instructure.com/doc/api/favorites.html#method.favorites.add_favorite_course

        Parameters:
            course: :class:`canvasapi.course.Course` or int
            use_sis_id: bool
        """
        if use_sis_id:
            course_id = course
            uri_str = 'users/self/favorites/courses/sis_course_id:{}'
        else:
            course_id = obj_or_id(course, 'course', (Course,))
            uri_str = 'users/self/favorites/courses/{}'
        response: 'httpx.Response' = await self._requester.request_async('POST', uri_str.format(course_id), _kwargs=combine_kwargs(**kwargs))
        return Favorite(self._requester, response.json())

    def add_favorite_group(self, group: 'Group | int', use_sis_id: 'bool'=False, **kwargs) -> 'Favorite':
        """
        Add a group to the current user's favorites. If the group is already
        in the user's favorites, nothing happens.

        Endpoint: POST /api/v1/users/self/favorites/groups/:id

        Reference: https://canvas.instructure.com/doc/api/favorites.html#method.favorites.add_favorite_groups

        Parameters:
            group: :class:`canvasapi.group.Group` or int
            use_sis_id: bool
        """
        if use_sis_id:
            group_id = group
            uri_str = 'users/self/favorites/groups/sis_group_id:{}'
        else:
            group_id = obj_or_id(group, 'group', (Group,))
            uri_str = 'users/self/favorites/groups/{}'
        response: 'httpx.Response' = self._requester.request('POST', uri_str.format(group_id), _kwargs=combine_kwargs(**kwargs))
        return Favorite(self._requester, response.json())

    async def add_favorite_group_async(self, group: 'Group | int', use_sis_id: 'bool'=False, **kwargs) -> 'Favorite':
        """
        Add a group to the current user's favorites. If the group is already
        in the user's favorites, nothing happens.

        Endpoint: POST /api/v1/users/self/favorites/groups/:id

        Reference: https://canvas.instructure.com/doc/api/favorites.html#method.favorites.add_favorite_groups

        Parameters:
            group: :class:`canvasapi.group.Group` or int
            use_sis_id: bool
        """
        if use_sis_id:
            group_id = group
            uri_str = 'users/self/favorites/groups/sis_group_id:{}'
        else:
            group_id = obj_or_id(group, 'group', (Group,))
            uri_str = 'users/self/favorites/groups/{}'
        response: 'httpx.Response' = await self._requester.request_async('POST', uri_str.format(group_id), _kwargs=combine_kwargs(**kwargs))
        return Favorite(self._requester, response.json())

    def create_bookmark(self, name: 'str', url: 'str', **kwargs) -> 'Bookmark':
        """
        Create a new Bookmark.

        Endpoint: POST /api/v1/users/self/bookmarks

        Reference: https://canvas.instructure.com/doc/api/bookmarks.html#method.bookmarks/bookmarks.create

        Parameters:
            name: `str`
            url: `str`
        """
        from .bookmark import Bookmark
        response: 'httpx.Response' = self._requester.request('POST', 'users/self/bookmarks', name=name, url=url, _kwargs=combine_kwargs(**kwargs))
        return Bookmark(self._requester, response.json())

    async def create_bookmark_async(self, name: 'str', url: 'str', **kwargs) -> 'Bookmark':
        """
        Create a new Bookmark.

        Endpoint: POST /api/v1/users/self/bookmarks

        Reference: https://canvas.instructure.com/doc/api/bookmarks.html#method.bookmarks/bookmarks.create

        Parameters:
            name: `str`
            url: `str`
        """
        from .bookmark import Bookmark
        response: 'httpx.Response' = await self._requester.request_async('POST', 'users/self/bookmarks', name=name, url=url, _kwargs=combine_kwargs(**kwargs))
        return Bookmark(self._requester, response.json())

    def get_bookmark(self, bookmark: 'Bookmark | int', **kwargs) -> 'Bookmark':
        """
        Return single Bookmark by id

        Endpoint: GET /api/v1/users/self/bookmarks/:id

        Reference: https://canvas.instructure.com/doc/api/bookmarks.html#method.bookmarks/bookmarks.show

        Parameters:
            bookmark: :class:`canvasapi.bookmark.Bookmark` or int
        """
        from .bookmark import Bookmark
        bookmark_id = obj_or_id(bookmark, 'bookmark', (Bookmark,))
        response: 'httpx.Response' = self._requester.request('GET', 'users/self/bookmarks/{}'.format(bookmark_id), _kwargs=combine_kwargs(**kwargs))
        return Bookmark(self._requester, response.json())

    async def get_bookmark_async(self, bookmark: 'Bookmark | int', **kwargs) -> 'Bookmark':
        """
        Return single Bookmark by id

        Endpoint: GET /api/v1/users/self/bookmarks/:id

        Reference: https://canvas.instructure.com/doc/api/bookmarks.html#method.bookmarks/bookmarks.show

        Parameters:
            bookmark: :class:`canvasapi.bookmark.Bookmark` or int
        """
        from .bookmark import Bookmark
        bookmark_id = obj_or_id(bookmark, 'bookmark', (Bookmark,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'users/self/bookmarks/{}'.format(bookmark_id), _kwargs=combine_kwargs(**kwargs))
        return Bookmark(self._requester, response.json())

    def get_bookmarks(self, **kwargs) -> 'PaginatedList[Bookmark]':
        """
        List bookmarks that the current user can view or manage.

        Endpoint: GET /api/v1/users/self/bookmarks

        Reference: https://canvas.instructure.com/doc/api/bookmarks.html#method.bookmarks/bookmarks.index
        """
        return PaginatedList(Bookmark, self._requester, 'GET', 'users/self/bookmarks')

    async def get_bookmarks_async(self, **kwargs) -> 'PaginatedList[Bookmark]':
        """
        List bookmarks that the current user can view or manage.

        Endpoint: GET /api/v1/users/self/bookmarks

        Reference: https://canvas.instructure.com/doc/api/bookmarks.html#method.bookmarks/bookmarks.index
        """
        return PaginatedList(Bookmark, self._requester, 'GET', 'users/self/bookmarks')

    def get_favorite_courses(self, **kwargs) -> 'PaginatedList[Course]':
        """
        Retrieve the paginated list of favorite courses for the current user.
        If the user has not chosen any favorites,
        then a selection of currently enrolled courses will be returned.

        Endpoint: GET /api/v1/users/self/favorites/courses

        Reference: https://canvas.instructure.com/doc/api/favorites.html#method.favorites.list_favorite_courses
        """
        return PaginatedList(Course, self._requester, 'GET', 'users/self/favorites/courses', _kwargs=combine_kwargs(**kwargs))

    async def get_favorite_courses_async(self, **kwargs) -> 'PaginatedList[Course]':
        """
        Retrieve the paginated list of favorite courses for the current user.
        If the user has not chosen any favorites,
        then a selection of currently enrolled courses will be returned.

        Endpoint: GET /api/v1/users/self/favorites/courses

        Reference: https://canvas.instructure.com/doc/api/favorites.html#method.favorites.list_favorite_courses
        """
        return PaginatedList(Course, self._requester, 'GET', 'users/self/favorites/courses', _kwargs=combine_kwargs(**kwargs))

    def get_favorite_groups(self, **kwargs) -> 'PaginatedList[Group]':
        """
        Retrieve the paginated list of favorite groups for the current user.
        If the user has not chosen any favorites, then a selection of groups
        that the user is a member of will be returned.

        Endpoint: GET /api/v1/users/self/favorites/groups

        Reference: https://canvas.instructure.com/doc/api/favorites.html#method.favorites.list_favorite_groups
        """
        return PaginatedList(Group, self._requester, 'GET', 'users/self/favorites/groups', _kwargs=combine_kwargs(**kwargs))

    async def get_favorite_groups_async(self, **kwargs) -> 'PaginatedList[Group]':
        """
        Retrieve the paginated list of favorite groups for the current user.
        If the user has not chosen any favorites, then a selection of groups
        that the user is a member of will be returned.

        Endpoint: GET /api/v1/users/self/favorites/groups

        Reference: https://canvas.instructure.com/doc/api/favorites.html#method.favorites.list_favorite_groups
        """
        return PaginatedList(Group, self._requester, 'GET', 'users/self/favorites/groups', _kwargs=combine_kwargs(**kwargs))

    def get_groups(self, **kwargs) -> 'PaginatedList[Group]':
        """
        Return the list of active groups for the user.

        Endpoint: GET /api/v1/users/self/groups

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.index
        """
        from .group import Group
        return PaginatedList(Group, self._requester, 'GET', 'users/self/groups', _kwargs=combine_kwargs(**kwargs))

    async def get_groups_async(self, **kwargs) -> 'PaginatedList[Group]':
        """
        Return the list of active groups for the user.

        Endpoint: GET /api/v1/users/self/groups

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.index
        """
        from .group import Group
        return PaginatedList(Group, self._requester, 'GET', 'users/self/groups', _kwargs=combine_kwargs(**kwargs))

    def reset_favorite_courses(self, **kwargs) -> 'bool':
        """
        Reset the current user's course favorites to the default
        automatically generated list of enrolled courses

        Endpoint: DELETE /api/v1/users/self/favorites/courses

        Reference: https://canvas.instructure.com/doc/api/favorites.html#method.favorites.reset_course_favorites
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'users/self/favorites/courses', _kwargs=combine_kwargs(**kwargs))
        return response.json().get('message') == 'OK'

    async def reset_favorite_courses_async(self, **kwargs) -> 'bool':
        """
        Reset the current user's course favorites to the default
        automatically generated list of enrolled courses

        Endpoint: DELETE /api/v1/users/self/favorites/courses

        Reference: https://canvas.instructure.com/doc/api/favorites.html#method.favorites.reset_course_favorites
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'users/self/favorites/courses', _kwargs=combine_kwargs(**kwargs))
        return response.json().get('message') == 'OK'

    def reset_favorite_groups(self, **kwargs) -> 'bool':
        """
        Reset the current user's group favorites to the default
        automatically generated list of enrolled groups

        Endpoint: DELETE /api/v1/users/self/favorites/groups

        Reference: https://canvas.instructure.com/doc/api/favorites.html#method.favorites.reset_groups_favorites
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'users/self/favorites/groups', _kwargs=combine_kwargs(**kwargs))
        return response.json().get('message') == 'OK'

    async def reset_favorite_groups_async(self, **kwargs) -> 'bool':
        """
        Reset the current user's group favorites to the default
        automatically generated list of enrolled groups

        Endpoint: DELETE /api/v1/users/self/favorites/groups

        Reference: https://canvas.instructure.com/doc/api/favorites.html#method.favorites.reset_groups_favorites
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'users/self/favorites/groups', _kwargs=combine_kwargs(**kwargs))
        return response.json().get('message') == 'OK'