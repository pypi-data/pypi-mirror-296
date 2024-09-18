from ..models.pages import Page as PageModel, PageRevision as PageRevisionModel
import httpx
import typing
if typing.TYPE_CHECKING:
    from .paginated_list import PaginatedList
    from .pagerevision import PageRevision
    from .course import Course
    from .group import Group
from .canvas_object import CanvasObject
from .paginated_list import PaginatedList
from .util import combine_kwargs, obj_or_id

class Page(PageModel):

    def __str__(self):
        return '{} ({})'.format(self.title, self.url)

    def delete(self, **kwargs) -> 'Page':
        """
        Delete this page.

        Endpoint: DELETE /api/v1/courses/:course_id/pages/:url

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', '{}s/{}/pages/{}'.format(self.parent_type, self.parent_id, self.url), _kwargs=combine_kwargs(**kwargs))
        return Page(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'Page':
        """
        Delete this page.

        Endpoint: DELETE /api/v1/courses/:course_id/pages/:url

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', '{}s/{}/pages/{}'.format(self.parent_type, self.parent_id, self.url), _kwargs=combine_kwargs(**kwargs))
        return Page(self._requester, response.json())

    def edit(self, **kwargs) -> 'Page':
        """
        Update the title or the contents of a specified wiki
        page.

        Endpoint: PUT /api/v1/courses/:course_id/pages/:url

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', '{}s/{}/pages/{}'.format(self.parent_type, self.parent_id, self.url), _kwargs=combine_kwargs(**kwargs))
        page_json: 'dict' = response.json()
        page_json.update({'course_id': self.course_id})
        super(Page, self).set_attributes(page_json)
        return self

    async def edit_async(self, **kwargs) -> 'Page':
        """
        Update the title or the contents of a specified wiki
        page.

        Endpoint: PUT /api/v1/courses/:course_id/pages/:url

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', '{}s/{}/pages/{}'.format(self.parent_type, self.parent_id, self.url), _kwargs=combine_kwargs(**kwargs))
        page_json: 'dict' = response.json()
        page_json.update({'course_id': self.course_id})
        super(Page, self).set_attributes(page_json)
        return self

    def get_parent(self, **kwargs) -> 'Group | Course':
        """
        Return the object that spawned this page.

        Endpoint: GET /api/v1/groups/:group_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.show
        """
        from .course import Course
        from .group import Group
        response: 'httpx.Response' = self._requester.request('GET', '{}s/{}'.format(self.parent_type, self.parent_id), _kwargs=combine_kwargs(**kwargs))
        if self.parent_type == 'group':
            return Group(self._requester, response.json())
        elif self.parent_type == 'course':
            return Course(self._requester, response.json())

    async def get_parent_async(self, **kwargs) -> 'Group | Course':
        """
        Return the object that spawned this page.

        Endpoint: GET /api/v1/groups/:group_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.show
        """
        from .course import Course
        from .group import Group
        response: 'httpx.Response' = await self._requester.request_async('GET', '{}s/{}'.format(self.parent_type, self.parent_id), _kwargs=combine_kwargs(**kwargs))
        if self.parent_type == 'group':
            return Group(self._requester, response.json())
        elif self.parent_type == 'course':
            return Course(self._requester, response.json())

    def get_revision_by_id(self, revision: 'PageRevision | int', **kwargs) -> 'PageRevision':
        """
        Retrieve the contents of the revision by the id.

        Endpoint: GET /api/v1/courses/:course_id/pages/:url/revisions/:revision_id

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_revision

        Parameters:
            revision: :class:`canvasapi.pagerevision.PageRevision` or int
        """
        revision_id = obj_or_id(revision, 'revision', (PageRevision,))
        response: 'httpx.Response' = self._requester.request('GET', '{}s/{}/pages/{}/revisions/{}'.format(self.parent_type, self.parent_id, self.url, revision_id), _kwargs=combine_kwargs(**kwargs))
        pagerev_json: 'dict' = response.json()
        if self.parent_type == 'group':
            pagerev_json.update({'group_id': self.id})
        elif self.parent_type == 'course':
            pagerev_json.update({'course_id': self.id})
        return PageRevision(self._requester, pagerev_json)

    async def get_revision_by_id_async(self, revision: 'PageRevision | int', **kwargs) -> 'PageRevision':
        """
        Retrieve the contents of the revision by the id.

        Endpoint: GET /api/v1/courses/:course_id/pages/:url/revisions/:revision_id

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_revision

        Parameters:
            revision: :class:`canvasapi.pagerevision.PageRevision` or int
        """
        revision_id = obj_or_id(revision, 'revision', (PageRevision,))
        response: 'httpx.Response' = await self._requester.request_async('GET', '{}s/{}/pages/{}/revisions/{}'.format(self.parent_type, self.parent_id, self.url, revision_id), _kwargs=combine_kwargs(**kwargs))
        pagerev_json: 'dict' = response.json()
        if self.parent_type == 'group':
            pagerev_json.update({'group_id': self.id})
        elif self.parent_type == 'course':
            pagerev_json.update({'course_id': self.id})
        return PageRevision(self._requester, pagerev_json)

    def get_revisions(self, **kwargs) -> 'PaginatedList[PageRevision]':
        """
        List the revisions of a page.

        Endpoint: GET /api/v1/courses/:course_id/pages/:url/revisions

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.revisions
        """
        return PaginatedList(PageRevision, self._requester, 'GET', '{}s/{}/pages/{}/revisions'.format(self.parent_type, self.parent_id, self.url), _kwargs=combine_kwargs(**kwargs))

    async def get_revisions_async(self, **kwargs) -> 'PaginatedList[PageRevision]':
        """
        List the revisions of a page.

        Endpoint: GET /api/v1/courses/:course_id/pages/:url/revisions

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.revisions
        """
        return PaginatedList(PageRevision, self._requester, 'GET', '{}s/{}/pages/{}/revisions'.format(self.parent_type, self.parent_id, self.url), _kwargs=combine_kwargs(**kwargs))

    @property
    def parent_id(self) -> 'int':
        """
        Return the id of the course or group that spawned this page.
        """
        if hasattr(self, 'course_id'):
            return self.course_id
        elif hasattr(self, 'group_id'):
            return self.group_id
        else:
            raise ValueError('Page does not have a course_id or group_id')

    @property
    async def parent_id_async(self) -> 'int':
        """
        Return the id of the course or group that spawned this page.
        """
        if hasattr(self, 'course_id'):
            return self.course_id
        elif hasattr(self, 'group_id'):
            return self.group_id
        else:
            raise ValueError('Page does not have a course_id or group_id')

    @property
    def parent_type(self) -> 'str':
        """
        Return whether the page was spawned from a course or group.
        """
        if hasattr(self, 'course_id'):
            return 'course'
        elif hasattr(self, 'group_id'):
            return 'group'
        else:
            raise ValueError('ExternalTool does not have a course_id or group_id')

    @property
    async def parent_type_async(self) -> 'str':
        """
        Return whether the page was spawned from a course or group.
        """
        if hasattr(self, 'course_id'):
            return 'course'
        elif hasattr(self, 'group_id'):
            return 'group'
        else:
            raise ValueError('ExternalTool does not have a course_id or group_id')

    def revert_to_revision(self, revision: 'PageRevision | int', **kwargs) -> 'PageRevision':
        """
        Revert the page back to a specified revision.

        Endpoint: POST /api/v1/courses/:course_id/pages/:url/revisions/:revision_id

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.revert

        Parameters:
            revision: :class:`canvasapi.pagerevision.PageRevision` or int
        """
        revision_id = obj_or_id(revision, 'revision', (PageRevision,))
        response: 'httpx.Response' = self._requester.request('POST', '{}s/{}/pages/{}/revisions/{}'.format(self.parent_type, self.parent_id, self.url, revision_id), _kwargs=combine_kwargs(**kwargs))
        pagerev_json: 'dict' = response.json()
        pagerev_json.update({'{self.parent_type}_id': self.parent_id})
        return PageRevision(self._requester, pagerev_json)

    async def revert_to_revision_async(self, revision: 'PageRevision | int', **kwargs) -> 'PageRevision':
        """
        Revert the page back to a specified revision.

        Endpoint: POST /api/v1/courses/:course_id/pages/:url/revisions/:revision_id

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.revert

        Parameters:
            revision: :class:`canvasapi.pagerevision.PageRevision` or int
        """
        revision_id = obj_or_id(revision, 'revision', (PageRevision,))
        response: 'httpx.Response' = await self._requester.request_async('POST', '{}s/{}/pages/{}/revisions/{}'.format(self.parent_type, self.parent_id, self.url, revision_id), _kwargs=combine_kwargs(**kwargs))
        pagerev_json: 'dict' = response.json()
        pagerev_json.update({'{self.parent_type}_id': self.parent_id})
        return PageRevision(self._requester, pagerev_json)

    def show_latest_revision(self, **kwargs) -> 'PageRevision':
        """
        Retrieve the contents of the latest revision.

        Endpoint: GET /api/v1/courses/:course_id/pages/:url/revisions/latest

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_revision
        """
        response: 'httpx.Response' = self._requester.request('GET', '{}s/{}/pages/{}/revisions/latest'.format(self.parent_type, self.parent_id, self.url), _kwargs=combine_kwargs(**kwargs))
        return PageRevision(self._requester, response.json())

    async def show_latest_revision_async(self, **kwargs) -> 'PageRevision':
        """
        Retrieve the contents of the latest revision.

        Endpoint: GET /api/v1/courses/:course_id/pages/:url/revisions/latest

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_revision
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', '{}s/{}/pages/{}/revisions/latest'.format(self.parent_type, self.parent_id, self.url), _kwargs=combine_kwargs(**kwargs))
        return PageRevision(self._requester, response.json())

class PageRevision(PageRevisionModel):

    def __str__(self):
        return '{} ({})'.format(self.updated_at, self.revision_id)

    def get_parent(self, **kwargs) -> 'Group | Course':
        """
        Return the object that spawned this page.

        Endpoint: GET /api/v1/groups/:group_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.show
        """
        from .course import Course
        from .group import Group
        response: 'httpx.Response' = self._requester.request('GET', '{}s/{}'.format(self.parent_type, self.parent_id), _kwargs=combine_kwargs(**kwargs))
        if self.parent_type == 'group':
            return Group(self._requester, response.json())
        elif self.parent_type == 'course':
            return Course(self._requester, response.json())

    async def get_parent_async(self, **kwargs) -> 'Group | Course':
        """
        Return the object that spawned this page.

        Endpoint: GET /api/v1/groups/:group_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.show
        """
        from .course import Course
        from .group import Group
        response: 'httpx.Response' = await self._requester.request_async('GET', '{}s/{}'.format(self.parent_type, self.parent_id), _kwargs=combine_kwargs(**kwargs))
        if self.parent_type == 'group':
            return Group(self._requester, response.json())
        elif self.parent_type == 'course':
            return Course(self._requester, response.json())

    @property
    def parent_id(self) -> 'int':
        """
        Return the id of the course or group that spawned this page.
        """
        if hasattr(self, 'course_id'):
            return self.course_id
        elif hasattr(self, 'group_id'):
            return self.group_id
        else:
            raise ValueError('Page does not have a course_id or group_id')

    @property
    async def parent_id_async(self) -> 'int':
        """
        Return the id of the course or group that spawned this page.
        """
        if hasattr(self, 'course_id'):
            return self.course_id
        elif hasattr(self, 'group_id'):
            return self.group_id
        else:
            raise ValueError('Page does not have a course_id or group_id')

    @property
    def parent_type(self) -> 'str':
        """
        Return whether the page was spawned from a course or group.
        """
        if hasattr(self, 'course_id'):
            return 'course'
        elif hasattr(self, 'group_id'):
            return 'group'
        else:
            raise ValueError('ExternalTool does not have a course_id or group_id')

    @property
    async def parent_type_async(self) -> 'str':
        """
        Return whether the page was spawned from a course or group.
        """
        if hasattr(self, 'course_id'):
            return 'course'
        elif hasattr(self, 'group_id'):
            return 'group'
        else:
            raise ValueError('ExternalTool does not have a course_id or group_id')