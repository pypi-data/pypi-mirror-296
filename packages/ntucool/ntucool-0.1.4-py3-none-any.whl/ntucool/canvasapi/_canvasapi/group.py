from ..models.group_categories import GroupCategory as GroupCategoryModel
from ..models.groups import Group as GroupModel, GroupMembership as GroupMembershipModel
import httpx
import typing
if typing.TYPE_CHECKING:
    from .progress import Progress
    from .usage_rights import UsageRights
    from .tab import Tab
    from .group import Group
    from .license import License
    from .file import File
    from .paginated_list import PaginatedList
    from .collaboration import Collaboration
    from .assignment import Assignment, AssignmentOverride
    from .content_export import ContentExport
    from .page import Page
    from .user import User
    from .folder import Folder
    from .external_feed import ExternalFeed
    from .discussion_topic import DiscussionTopic
    from .content_migration import ContentMigration, Migrator
from .canvas_object import CanvasObject
from .collaboration import Collaboration
from .discussion_topic import DiscussionTopic
from .exceptions import RequiredFieldMissing
from .external_feed import ExternalFeed
from .folder import Folder
from .license import License
from .paginated_list import PaginatedList
from .tab import Tab
from .upload import FileOrPathLike, Uploader
from .usage_rights import UsageRights
from .util import combine_kwargs, is_multivalued, obj_or_id

class Group(GroupModel):

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)

    def create_content_migration(self, migration_type: 'str | Migrator', **kwargs) -> 'ContentMigration':
        """
        Create a content migration.

        Endpoint: POST /api/v1/groups/:group_id/content_migrations

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.create

        Parameters:
            migration_type: str or :class:`canvasapi.content_migration.Migrator`
        """
        from .content_migration import ContentMigration, Migrator
        if isinstance(migration_type, Migrator):
            kwargs['migration_type'] = migration_type.type
        elif isinstance(migration_type, str):
            kwargs['migration_type'] = migration_type
        else:
            raise TypeError('Parameter migration_type must be of type Migrator or str')
        response: 'httpx.Response' = self._requester.request('POST', 'groups/{}/content_migrations'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'group_id': self.id})
        return ContentMigration(self._requester, response_json)

    async def create_content_migration_async(self, migration_type: 'str | Migrator', **kwargs) -> 'ContentMigration':
        """
        Create a content migration.

        Endpoint: POST /api/v1/groups/:group_id/content_migrations

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.create

        Parameters:
            migration_type: str or :class:`canvasapi.content_migration.Migrator`
        """
        from .content_migration import ContentMigration, Migrator
        if isinstance(migration_type, Migrator):
            kwargs['migration_type'] = migration_type.type
        elif isinstance(migration_type, str):
            kwargs['migration_type'] = migration_type
        else:
            raise TypeError('Parameter migration_type must be of type Migrator or str')
        response: 'httpx.Response' = await self._requester.request_async('POST', 'groups/{}/content_migrations'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'group_id': self.id})
        return ContentMigration(self._requester, response_json)

    def create_discussion_topic(self, **kwargs) -> 'DiscussionTopic':
        """
        Creates a new discussion topic for the course or group.

        Endpoint: POST /api/v1/groups/:group_id/discussion_topics

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.create
        """
        response: 'httpx.Response' = self._requester.request('POST', 'groups/{}/discussion_topics'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'group_id': self.id})
        return DiscussionTopic(self._requester, response_json)

    async def create_discussion_topic_async(self, **kwargs) -> 'DiscussionTopic':
        """
        Creates a new discussion topic for the course or group.

        Endpoint: POST /api/v1/groups/:group_id/discussion_topics

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.create
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'groups/{}/discussion_topics'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'group_id': self.id})
        return DiscussionTopic(self._requester, response_json)

    def create_external_feed(self, url: 'str', **kwargs) -> 'ExternalFeed':
        """
        Create a new external feed for the group.

        Endpoint: POST /api/v1/groups/:group_id/external_feeds

        Reference: https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.create

        Parameters:
            url: str
        """
        response: 'httpx.Response' = self._requester.request('POST', 'groups/{}/external_feeds'.format(self.id), url=url, _kwargs=combine_kwargs(**kwargs))
        return ExternalFeed(self._requester, response.json())

    async def create_external_feed_async(self, url: 'str', **kwargs) -> 'ExternalFeed':
        """
        Create a new external feed for the group.

        Endpoint: POST /api/v1/groups/:group_id/external_feeds

        Reference: https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.create

        Parameters:
            url: str
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'groups/{}/external_feeds'.format(self.id), url=url, _kwargs=combine_kwargs(**kwargs))
        return ExternalFeed(self._requester, response.json())

    def create_folder(self, name: 'str', **kwargs) -> 'Folder':
        """
        Creates a folder in this group.

        Endpoint: POST /api/v1/groups/:group_id/folders

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.create

        Parameters:
            name: str
        """
        response: 'httpx.Response' = self._requester.request('POST', 'groups/{}/folders'.format(self.id), name=name, _kwargs=combine_kwargs(**kwargs))
        return Folder(self._requester, response.json())

    async def create_folder_async(self, name: 'str', **kwargs) -> 'Folder':
        """
        Creates a folder in this group.

        Endpoint: POST /api/v1/groups/:group_id/folders

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.create

        Parameters:
            name: str
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'groups/{}/folders'.format(self.id), name=name, _kwargs=combine_kwargs(**kwargs))
        return Folder(self._requester, response.json())

    def create_membership(self, user: 'User | int', **kwargs) -> 'GroupMembership':
        """
        Join, or request to join, a group, depending on the join_level of the group.
        If the membership or join request already exists, then it is simply returned.

        Endpoint: POST /api/v1/groups/:group_id/memberships

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.create

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = self._requester.request('POST', 'groups/{}/memberships'.format(self.id), user_id=user_id, _kwargs=combine_kwargs(**kwargs))
        return GroupMembership(self._requester, response.json())

    async def create_membership_async(self, user: 'User | int', **kwargs) -> 'GroupMembership':
        """
        Join, or request to join, a group, depending on the join_level of the group.
        If the membership or join request already exists, then it is simply returned.

        Endpoint: POST /api/v1/groups/:group_id/memberships

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.create

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = await self._requester.request_async('POST', 'groups/{}/memberships'.format(self.id), user_id=user_id, _kwargs=combine_kwargs(**kwargs))
        return GroupMembership(self._requester, response.json())

    def create_page(self, wiki_page: 'dict', **kwargs) -> 'Page':
        """
        Create a new wiki page.

        Endpoint: POST /api/v1/groups/:group_id/pages

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.create

        Parameters:
            wiki_page: dict
        """
        from .course import Page
        if isinstance(wiki_page, dict) and 'title' in wiki_page:
            kwargs['wiki_page'] = wiki_page
        else:
            raise RequiredFieldMissing("Dictionary with key 'title' is required.")
        response: 'httpx.Response' = self._requester.request('POST', 'groups/{}/pages'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        page_json: 'dict' = response.json()
        page_json.update({'group_id': self.id})
        return Page(self._requester, page_json)

    async def create_page_async(self, wiki_page: 'dict', **kwargs) -> 'Page':
        """
        Create a new wiki page.

        Endpoint: POST /api/v1/groups/:group_id/pages

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.create

        Parameters:
            wiki_page: dict
        """
        from .course import Page
        if isinstance(wiki_page, dict) and 'title' in wiki_page:
            kwargs['wiki_page'] = wiki_page
        else:
            raise RequiredFieldMissing("Dictionary with key 'title' is required.")
        response: 'httpx.Response' = await self._requester.request_async('POST', 'groups/{}/pages'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        page_json: 'dict' = response.json()
        page_json.update({'group_id': self.id})
        return Page(self._requester, page_json)

    def delete(self, **kwargs) -> 'Group':
        """
        Delete a group.

        Endpoint: DELETE /api/v1/groups/:group_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'groups/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Group(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'Group':
        """
        Delete a group.

        Endpoint: DELETE /api/v1/groups/:group_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'groups/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Group(self._requester, response.json())

    def delete_external_feed(self, feed: 'ExternalFeed | int', **kwargs) -> 'ExternalFeed':
        """
        Deletes the external feed.

        Endpoint: DELETE /api/v1/groups/:group_id/external_feeds/:external_feed_id

        Reference: https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.destroy

        Parameters:
            feed: :class:`canvasapi.external_feed.ExternalFeed` or int
        """
        from .external_feed import ExternalFeed
        feed_id = obj_or_id(feed, 'feed', (ExternalFeed,))
        response: 'httpx.Response' = self._requester.request('DELETE', 'groups/{}/external_feeds/{}'.format(self.id, feed_id), _kwargs=combine_kwargs(**kwargs))
        return ExternalFeed(self._requester, response.json())

    async def delete_external_feed_async(self, feed: 'ExternalFeed | int', **kwargs) -> 'ExternalFeed':
        """
        Deletes the external feed.

        Endpoint: DELETE /api/v1/groups/:group_id/external_feeds/:external_feed_id

        Reference: https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.destroy

        Parameters:
            feed: :class:`canvasapi.external_feed.ExternalFeed` or int
        """
        from .external_feed import ExternalFeed
        feed_id = obj_or_id(feed, 'feed', (ExternalFeed,))
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'groups/{}/external_feeds/{}'.format(self.id, feed_id), _kwargs=combine_kwargs(**kwargs))
        return ExternalFeed(self._requester, response.json())

    def edit(self, **kwargs) -> 'Group':
        """
        Edit a group.

        Endpoint: PUT /api/v1/groups/:group_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'groups/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Group(self._requester, response.json())

    async def edit_async(self, **kwargs) -> 'Group':
        """
        Edit a group.

        Endpoint: PUT /api/v1/groups/:group_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'groups/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Group(self._requester, response.json())

    def edit_front_page(self, **kwargs) -> 'Page':
        """
        Update the title or contents of the front page.

        Endpoint: PUT /api/v1/groups/:group_id/front_page

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.update_front_page
        """
        from .course import Page
        response: 'httpx.Response' = self._requester.request('PUT', 'groups/{}/front_page'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        page_json: 'dict' = response.json()
        page_json.update({'group_id': self.id})
        return Page(self._requester, page_json)

    async def edit_front_page_async(self, **kwargs) -> 'Page':
        """
        Update the title or contents of the front page.

        Endpoint: PUT /api/v1/groups/:group_id/front_page

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.update_front_page
        """
        from .course import Page
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'groups/{}/front_page'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        page_json: 'dict' = response.json()
        page_json.update({'group_id': self.id})
        return Page(self._requester, page_json)

    def export_content(self, export_type: 'str', **kwargs) -> 'ContentExport':
        """
        Begin a content export job for a group.

        Endpoint: POST /api/v1/groups/:group_id/content_exports

        Reference: https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.create

        Parameters:
            export_type: str
        """
        from .content_export import ContentExport
        kwargs['export_type'] = export_type
        response: 'httpx.Response' = self._requester.request('POST', 'groups/{}/content_exports'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return ContentExport(self._requester, response.json())

    async def export_content_async(self, export_type: 'str', **kwargs) -> 'ContentExport':
        """
        Begin a content export job for a group.

        Endpoint: POST /api/v1/groups/:group_id/content_exports

        Reference: https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.create

        Parameters:
            export_type: str
        """
        from .content_export import ContentExport
        kwargs['export_type'] = export_type
        response: 'httpx.Response' = await self._requester.request_async('POST', 'groups/{}/content_exports'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return ContentExport(self._requester, response.json())

    def get_activity_stream_summary(self, **kwargs) -> 'dict':
        """
        Return a summary of the current user's global activity stream.

        Endpoint: GET /api/v1/groups/:group_id/activity_stream/summary

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.activity_stream_summary
        """
        response: 'httpx.Response' = self._requester.request('GET', 'groups/{}/activity_stream/summary'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_activity_stream_summary_async(self, **kwargs) -> 'dict':
        """
        Return a summary of the current user's global activity stream.

        Endpoint: GET /api/v1/groups/:group_id/activity_stream/summary

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.activity_stream_summary
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'groups/{}/activity_stream/summary'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_assignment_override(self, assignment: 'Assignment | int', **kwargs) -> 'AssignmentOverride':
        """
        Return override for the specified assignment for this group.

        Endpoint: GET /api/v1/groups/:group_id/assignments/:assignment_id/override

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.group_alias

        Parameters:
            assignment: :class:`canvasapi.assignment.Assignment` or int
        """
        from .assignment import Assignment, AssignmentOverride
        assignment_id = obj_or_id(assignment, 'assignment', (Assignment,))
        response: 'httpx.Response' = self._requester.request('GET', 'groups/{}/assignments/{}/override'.format(self.id, assignment_id))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return AssignmentOverride(self._requester, response_json)

    async def get_assignment_override_async(self, assignment: 'Assignment | int', **kwargs) -> 'AssignmentOverride':
        """
        Return override for the specified assignment for this group.

        Endpoint: GET /api/v1/groups/:group_id/assignments/:assignment_id/override

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.group_alias

        Parameters:
            assignment: :class:`canvasapi.assignment.Assignment` or int
        """
        from .assignment import Assignment, AssignmentOverride
        assignment_id = obj_or_id(assignment, 'assignment', (Assignment,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'groups/{}/assignments/{}/override'.format(self.id, assignment_id))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return AssignmentOverride(self._requester, response_json)

    def get_collaborations(self, **kwargs) -> 'Collaboration':
        """
        Return a list of collaborations for a given course ID.

        Endpoint: GET /api/v1/groups/:group_id/collaborations

        Reference: https://canvas.instructure.com/doc/api/collaborations.html#method.collaborations.api_index
        """
        return PaginatedList(Collaboration, self._requester, 'GET', 'groups/{}/collaborations'.format(self.id), _root='collaborations', kwargs=combine_kwargs(**kwargs))

    async def get_collaborations_async(self, **kwargs) -> 'Collaboration':
        """
        Return a list of collaborations for a given course ID.

        Endpoint: GET /api/v1/groups/:group_id/collaborations

        Reference: https://canvas.instructure.com/doc/api/collaborations.html#method.collaborations.api_index
        """
        return PaginatedList(Collaboration, self._requester, 'GET', 'groups/{}/collaborations'.format(self.id), _root='collaborations', kwargs=combine_kwargs(**kwargs))

    def get_content_export(self, content_export: 'int | ContentExport', **kwargs) -> 'ContentExport':
        """
        Return information about a single content export.

        Endpoint: GET /api/v1/groups/:group_id/content_exports/:id

        Reference: https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.show

        Parameters:
            content_export: int or :class:`canvasapi.content_export.ContentExport`
        """
        from .content_export import ContentExport
        export_id = obj_or_id(content_export, 'content_export', (ContentExport,))
        response: 'httpx.Response' = self._requester.request('GET', 'groups/{}/content_exports/{}'.format(self.id, export_id), _kwargs=combine_kwargs(**kwargs))
        return ContentExport(self._requester, response.json())

    async def get_content_export_async(self, content_export: 'int | ContentExport', **kwargs) -> 'ContentExport':
        """
        Return information about a single content export.

        Endpoint: GET /api/v1/groups/:group_id/content_exports/:id

        Reference: https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.show

        Parameters:
            content_export: int or :class:`canvasapi.content_export.ContentExport`
        """
        from .content_export import ContentExport
        export_id = obj_or_id(content_export, 'content_export', (ContentExport,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'groups/{}/content_exports/{}'.format(self.id, export_id), _kwargs=combine_kwargs(**kwargs))
        return ContentExport(self._requester, response.json())

    def get_content_exports(self, **kwargs) -> 'PaginatedList[ContentExport]':
        """
        Return a paginated list of the past and pending content export jobs for a group.

        Endpoint: GET /api/v1/groups/:group_id/content_exports

        Reference: https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.index
        """
        from .content_export import ContentExport
        return PaginatedList(ContentExport, self._requester, 'GET', 'groups/{}/content_exports'.format(self.id), kwargs=combine_kwargs(**kwargs))

    async def get_content_exports_async(self, **kwargs) -> 'PaginatedList[ContentExport]':
        """
        Return a paginated list of the past and pending content export jobs for a group.

        Endpoint: GET /api/v1/groups/:group_id/content_exports

        Reference: https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.index
        """
        from .content_export import ContentExport
        return PaginatedList(ContentExport, self._requester, 'GET', 'groups/{}/content_exports'.format(self.id), kwargs=combine_kwargs(**kwargs))

    def get_content_migration(self, content_migration: 'int | str | ContentMigration', **kwargs) -> 'ContentMigration':
        """
        Retrive a content migration by its ID

        Endpoint: GET /api/v1/groups/:group_id/content_migrations/:id

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.show

        Parameters:
            content_migration: int, str or :class:`canvasapi.content_migration.ContentMigration`
        """
        from .content_migration import ContentMigration
        migration_id = obj_or_id(content_migration, 'content_migration', (ContentMigration,))
        response: 'httpx.Response' = self._requester.request('GET', 'groups/{}/content_migrations/{}'.format(self.id, migration_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'group_id': self.id})
        return ContentMigration(self._requester, response_json)

    async def get_content_migration_async(self, content_migration: 'int | str | ContentMigration', **kwargs) -> 'ContentMigration':
        """
        Retrive a content migration by its ID

        Endpoint: GET /api/v1/groups/:group_id/content_migrations/:id

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.show

        Parameters:
            content_migration: int, str or :class:`canvasapi.content_migration.ContentMigration`
        """
        from .content_migration import ContentMigration
        migration_id = obj_or_id(content_migration, 'content_migration', (ContentMigration,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'groups/{}/content_migrations/{}'.format(self.id, migration_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'group_id': self.id})
        return ContentMigration(self._requester, response_json)

    def get_content_migrations(self, **kwargs) -> 'PaginatedList[ContentMigration]':
        """
        List content migrations that the current account can view or manage.

        Endpoint: GET /api/v1/groups/:group_id/content_migrations/

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.index
        """
        from .content_migration import ContentMigration
        return PaginatedList(ContentMigration, self._requester, 'GET', 'groups/{}/content_migrations'.format(self.id), {'group_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_content_migrations_async(self, **kwargs) -> 'PaginatedList[ContentMigration]':
        """
        List content migrations that the current account can view or manage.

        Endpoint: GET /api/v1/groups/:group_id/content_migrations/

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.index
        """
        from .content_migration import ContentMigration
        return PaginatedList(ContentMigration, self._requester, 'GET', 'groups/{}/content_migrations'.format(self.id), {'group_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_discussion_topic(self, topic: 'DiscussionTopic | int', **kwargs) -> 'DiscussionTopic':
        """
        Return data on an individual discussion topic.

        Endpoint: GET /api/v1/groups/:group_id/discussion_topics/:topic_id

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.show

        Parameters:
            topic: :class:`canvasapi.discussion_topic.DiscussionTopic` or int
        """
        topic_id = obj_or_id(topic, 'topic', (DiscussionTopic,))
        response: 'httpx.Response' = self._requester.request('GET', 'groups/{}/discussion_topics/{}'.format(self.id, topic_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'group_id': self.id})
        return DiscussionTopic(self._requester, response_json)

    async def get_discussion_topic_async(self, topic: 'DiscussionTopic | int', **kwargs) -> 'DiscussionTopic':
        """
        Return data on an individual discussion topic.

        Endpoint: GET /api/v1/groups/:group_id/discussion_topics/:topic_id

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.show

        Parameters:
            topic: :class:`canvasapi.discussion_topic.DiscussionTopic` or int
        """
        topic_id = obj_or_id(topic, 'topic', (DiscussionTopic,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'groups/{}/discussion_topics/{}'.format(self.id, topic_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'group_id': self.id})
        return DiscussionTopic(self._requester, response_json)

    def get_discussion_topics(self, **kwargs) -> 'PaginatedList[DiscussionTopic]':
        """
        Returns the paginated list of discussion topics for this course or group.

        Endpoint: GET /api/v1/groups/:group_id/discussion_topics

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.index
        """
        return PaginatedList(DiscussionTopic, self._requester, 'GET', 'groups/{}/discussion_topics'.format(self.id), {'group_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_discussion_topics_async(self, **kwargs) -> 'PaginatedList[DiscussionTopic]':
        """
        Returns the paginated list of discussion topics for this course or group.

        Endpoint: GET /api/v1/groups/:group_id/discussion_topics

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.index
        """
        return PaginatedList(DiscussionTopic, self._requester, 'GET', 'groups/{}/discussion_topics'.format(self.id), {'group_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_external_feeds(self, **kwargs) -> 'PaginatedList[ExternalFeed]':
        """
        Returns the list of External Feeds this group.

        Endpoint: GET /api/v1/groups/:group_id/external_feeds

        Reference: https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.index
        """
        from .external_feed import ExternalFeed
        return PaginatedList(ExternalFeed, self._requester, 'GET', 'groups/{}/external_feeds'.format(self.id))

    async def get_external_feeds_async(self, **kwargs) -> 'PaginatedList[ExternalFeed]':
        """
        Returns the list of External Feeds this group.

        Endpoint: GET /api/v1/groups/:group_id/external_feeds

        Reference: https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.index
        """
        from .external_feed import ExternalFeed
        return PaginatedList(ExternalFeed, self._requester, 'GET', 'groups/{}/external_feeds'.format(self.id))

    def get_file(self, file: 'File | int', **kwargs) -> 'File':
        """
        Return the standard attachment json object for a file.

        Endpoint: GET /api/v1/groups/:group_id/files/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_show

        Parameters:
            file: :class:`canvasapi.file.File` or int
        """
        from .file import File
        file_id = obj_or_id(file, 'file', (File,))
        response: 'httpx.Response' = self._requester.request('GET', 'groups/{}/files/{}'.format(self.id, file_id), _kwargs=combine_kwargs(**kwargs))
        return File(self._requester, response.json())

    async def get_file_async(self, file: 'File | int', **kwargs) -> 'File':
        """
        Return the standard attachment json object for a file.

        Endpoint: GET /api/v1/groups/:group_id/files/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_show

        Parameters:
            file: :class:`canvasapi.file.File` or int
        """
        from .file import File
        file_id = obj_or_id(file, 'file', (File,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'groups/{}/files/{}'.format(self.id, file_id), _kwargs=combine_kwargs(**kwargs))
        return File(self._requester, response.json())

    def get_file_quota(self, **kwargs) -> 'dict':
        """
        Returns the total and used storage quota for the group.

        Endpoint: GET /api/v1/groups/:group_id/files/quota

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_quota
        """
        response: 'httpx.Response' = self._requester.request('GET', 'groups/{}/files/quota'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_file_quota_async(self, **kwargs) -> 'dict':
        """
        Returns the total and used storage quota for the group.

        Endpoint: GET /api/v1/groups/:group_id/files/quota

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_quota
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'groups/{}/files/quota'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_files(self, **kwargs) -> 'PaginatedList[File]':
        """
        Returns the paginated list of files for the group.

        Endpoint: GET /api/v1/groups/:group_id/files

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_index
        """
        from .file import File
        return PaginatedList(File, self._requester, 'GET', 'groups/{}/files'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_files_async(self, **kwargs) -> 'PaginatedList[File]':
        """
        Returns the paginated list of files for the group.

        Endpoint: GET /api/v1/groups/:group_id/files

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_index
        """
        from .file import File
        return PaginatedList(File, self._requester, 'GET', 'groups/{}/files'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_folder(self, folder: 'Folder | int', **kwargs) -> 'Folder':
        """
        Returns the details for a group's folder

        Endpoint: GET /api/v1/groups/:group_id/folders/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.show

        Parameters:
            folder: :class:`canvasapi.folder.Folder` or int
        """
        folder_id = obj_or_id(folder, 'folder', (Folder,))
        response: 'httpx.Response' = self._requester.request('GET', 'groups/{}/folders/{}'.format(self.id, folder_id), _kwargs=combine_kwargs(**kwargs))
        return Folder(self._requester, response.json())

    async def get_folder_async(self, folder: 'Folder | int', **kwargs) -> 'Folder':
        """
        Returns the details for a group's folder

        Endpoint: GET /api/v1/groups/:group_id/folders/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.show

        Parameters:
            folder: :class:`canvasapi.folder.Folder` or int
        """
        folder_id = obj_or_id(folder, 'folder', (Folder,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'groups/{}/folders/{}'.format(self.id, folder_id), _kwargs=combine_kwargs(**kwargs))
        return Folder(self._requester, response.json())

    def get_folders(self, **kwargs) -> 'PaginatedList[Folder]':
        """
        Returns the paginated list of all folders for the given group. This will be returned as a
        flat list containing all subfolders as well.

        Endpoint: GET /api/v1/groups/:group_id/folders

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.list_all_folders
        """
        return PaginatedList(Folder, self._requester, 'GET', 'groups/{}/folders'.format(self.id))

    async def get_folders_async(self, **kwargs) -> 'PaginatedList[Folder]':
        """
        Returns the paginated list of all folders for the given group. This will be returned as a
        flat list containing all subfolders as well.

        Endpoint: GET /api/v1/groups/:group_id/folders

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.list_all_folders
        """
        return PaginatedList(Folder, self._requester, 'GET', 'groups/{}/folders'.format(self.id))

    def get_full_discussion_topic(self, topic: 'DiscussionTopic | int', **kwargs) -> 'dict':
        """
        Return a cached structure of the discussion topic.

        Endpoint: GET /api/v1/groups/:group_id/discussion_topics/:topic_id/view

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.view

        Parameters:
            topic: :class:`canvasapi.discussion_topic.DiscussionTopic` or int
        """
        topic_id = obj_or_id(topic, 'topic', (DiscussionTopic,))
        response: 'httpx.Response' = self._requester.request('GET', 'groups/{}/discussion_topics/{}/view'.format(self.id, topic_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_full_discussion_topic_async(self, topic: 'DiscussionTopic | int', **kwargs) -> 'dict':
        """
        Return a cached structure of the discussion topic.

        Endpoint: GET /api/v1/groups/:group_id/discussion_topics/:topic_id/view

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.view

        Parameters:
            topic: :class:`canvasapi.discussion_topic.DiscussionTopic` or int
        """
        topic_id = obj_or_id(topic, 'topic', (DiscussionTopic,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'groups/{}/discussion_topics/{}/view'.format(self.id, topic_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_licenses(self, **kwargs) -> 'PaginatedList[License]':
        """
        Returns a paginated list of the licenses that can be applied to the
        files under the group scope

        Endpoint: GET /api/v1/groups/:group_id/content_licenses

        Reference: https://canvas.instructure.com/doc/api/files.html#method.usage_rights.licenses
        """
        return PaginatedList(License, self._requester, 'GET', 'groups/{}/content_licenses'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_licenses_async(self, **kwargs) -> 'PaginatedList[License]':
        """
        Returns a paginated list of the licenses that can be applied to the
        files under the group scope

        Endpoint: GET /api/v1/groups/:group_id/content_licenses

        Reference: https://canvas.instructure.com/doc/api/files.html#method.usage_rights.licenses
        """
        return PaginatedList(License, self._requester, 'GET', 'groups/{}/content_licenses'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_membership(self, user: 'User | int', membership_type, **kwargs) -> 'GroupMembership':
        """
        List users in a group.

        Endpoint: GET /api/v1/groups/:group_id/users/:user_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.show

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = self._requester.request('GET', 'groups/{}/{}/{}'.format(self.id, membership_type, user_id), _kwargs=combine_kwargs(**kwargs))
        return GroupMembership(self._requester, response.json())

    async def get_membership_async(self, user: 'User | int', membership_type, **kwargs) -> 'GroupMembership':
        """
        List users in a group.

        Endpoint: GET /api/v1/groups/:group_id/users/:user_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.show

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'groups/{}/{}/{}'.format(self.id, membership_type, user_id), _kwargs=combine_kwargs(**kwargs))
        return GroupMembership(self._requester, response.json())

    def get_memberships(self, **kwargs) -> 'PaginatedList[GroupMembership]':
        """
        List users in a group.

        Endpoint: GET /api/v1/groups/:group_id/memberships

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.index
        """
        return PaginatedList(GroupMembership, self._requester, 'GET', 'groups/{}/memberships'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_memberships_async(self, **kwargs) -> 'PaginatedList[GroupMembership]':
        """
        List users in a group.

        Endpoint: GET /api/v1/groups/:group_id/memberships

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.index
        """
        return PaginatedList(GroupMembership, self._requester, 'GET', 'groups/{}/memberships'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_migration_systems(self, **kwargs) -> 'PaginatedList[Migrator]':
        """
        Return a list of migration systems.

        Endpoint: GET /api/v1/groups/:group_id/content_migrations/migrators

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.available_migrators
        """
        from .content_migration import Migrator
        return PaginatedList(Migrator, self._requester, 'GET', 'groups/{}/content_migrations/migrators'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_migration_systems_async(self, **kwargs) -> 'PaginatedList[Migrator]':
        """
        Return a list of migration systems.

        Endpoint: GET /api/v1/groups/:group_id/content_migrations/migrators

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.available_migrators
        """
        from .content_migration import Migrator
        return PaginatedList(Migrator, self._requester, 'GET', 'groups/{}/content_migrations/migrators'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_page(self, url: 'str', **kwargs) -> 'Group':
        """
        Retrieve the contents of a wiki page.

        Endpoint: GET /api/v1/groups/:group_id/pages/:url

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show

        Parameters:
            url: str
        """
        from .course import Page
        response: 'httpx.Response' = self._requester.request('GET', 'groups/{}/pages/{}'.format(self.id, url), _kwargs=combine_kwargs(**kwargs))
        page_json: 'dict' = response.json()
        page_json.update({'group_id': self.id})
        return Page(self._requester, page_json)

    async def get_page_async(self, url: 'str', **kwargs) -> 'Group':
        """
        Retrieve the contents of a wiki page.

        Endpoint: GET /api/v1/groups/:group_id/pages/:url

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show

        Parameters:
            url: str
        """
        from .course import Page
        response: 'httpx.Response' = await self._requester.request_async('GET', 'groups/{}/pages/{}'.format(self.id, url), _kwargs=combine_kwargs(**kwargs))
        page_json: 'dict' = response.json()
        page_json.update({'group_id': self.id})
        return Page(self._requester, page_json)

    def get_pages(self, **kwargs) -> 'PaginatedList[Page]':
        """
        List the wiki pages associated with a group.

        Endpoint: GET /api/v1/groups/:group_id/pages

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.index
        """
        from .course import Page
        return PaginatedList(Page, self._requester, 'GET', 'groups/{}/pages'.format(self.id), {'group_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_pages_async(self, **kwargs) -> 'PaginatedList[Page]':
        """
        List the wiki pages associated with a group.

        Endpoint: GET /api/v1/groups/:group_id/pages

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.index
        """
        from .course import Page
        return PaginatedList(Page, self._requester, 'GET', 'groups/{}/pages'.format(self.id), {'group_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_tabs(self, **kwargs) -> 'PaginatedList[Tab]':
        """
        List available tabs for a group.
        Returns a list of navigation tabs available in the current context.

        Endpoint: GET /api/v1/groups/:group_id/tabs

        Reference: https://canvas.instructure.com/doc/api/tabs.html#method.tabs.index
        """
        return PaginatedList(Tab, self._requester, 'GET', 'groups/{}/tabs'.format(self.id), {'group_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_tabs_async(self, **kwargs) -> 'PaginatedList[Tab]':
        """
        List available tabs for a group.
        Returns a list of navigation tabs available in the current context.

        Endpoint: GET /api/v1/groups/:group_id/tabs

        Reference: https://canvas.instructure.com/doc/api/tabs.html#method.tabs.index
        """
        return PaginatedList(Tab, self._requester, 'GET', 'groups/{}/tabs'.format(self.id), {'group_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_users(self, **kwargs) -> 'PaginatedList[User]':
        """
        List users in a group.

        Endpoint: GET /api/v1/groups/:group_id/users

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.users
        """
        from .user import User
        return PaginatedList(User, self._requester, 'GET', 'groups/{}/users'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_users_async(self, **kwargs) -> 'PaginatedList[User]':
        """
        List users in a group.

        Endpoint: GET /api/v1/groups/:group_id/users

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.users
        """
        from .user import User
        return PaginatedList(User, self._requester, 'GET', 'groups/{}/users'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def invite(self, invitees: 'integer list', **kwargs) -> 'PaginatedList[GroupMembership]':
        """
        Invite users to group.

        Endpoint: POST /api/v1/groups/:group_id/invite

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.invite

        Parameters:
            invitees: integer list
        """
        kwargs['invitees'] = invitees
        return PaginatedList(GroupMembership, self._requester, 'POST', 'groups/{}/invite'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def invite_async(self, invitees: 'integer list', **kwargs) -> 'PaginatedList[GroupMembership]':
        """
        Invite users to group.

        Endpoint: POST /api/v1/groups/:group_id/invite

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.invite

        Parameters:
            invitees: integer list
        """
        kwargs['invitees'] = invitees
        return PaginatedList(GroupMembership, self._requester, 'POST', 'groups/{}/invite'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def preview_html(self, html: 'str', **kwargs) -> 'str':
        """
        Preview HTML content processed for this course.

        Endpoint: POST /api/v1/groups/:group_id/preview_html

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.preview_html

        Parameters:
            html: str
        """
        response: 'httpx.Response' = self._requester.request('POST', 'groups/{}/preview_html'.format(self.id), html=html, _kwargs=combine_kwargs(**kwargs))
        return response.json().get('html', '')

    async def preview_html_async(self, html: 'str', **kwargs) -> 'str':
        """
        Preview HTML content processed for this course.

        Endpoint: POST /api/v1/groups/:group_id/preview_html

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.preview_html

        Parameters:
            html: str
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'groups/{}/preview_html'.format(self.id), html=html, _kwargs=combine_kwargs(**kwargs))
        return response.json().get('html', '')

    def remove_usage_rights(self, **kwargs) -> 'dict':
        """
        Removes the usage rights for specified files that are under the current group scope

        Endpoint: DELETE /api/v1/groups/:group_id/usage_rights

        Reference: https://canvas.instructure.com/doc/api/files.html#method.usage_rights.remove_usage_rights
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'groups/{}/usage_rights'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def remove_usage_rights_async(self, **kwargs) -> 'dict':
        """
        Removes the usage rights for specified files that are under the current group scope

        Endpoint: DELETE /api/v1/groups/:group_id/usage_rights

        Reference: https://canvas.instructure.com/doc/api/files.html#method.usage_rights.remove_usage_rights
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'groups/{}/usage_rights'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def remove_user(self, user: 'User | int', **kwargs) -> 'User':
        """
        Leave a group if allowed.

        Endpoint: DELETE /api/v1/groups/:group_id/users/:user_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.destroy

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = self._requester.request('DELETE', 'groups/{}/users/{}'.format(self.id, user_id), _kwargs=combine_kwargs(**kwargs))
        return User(self._requester, response.json())

    async def remove_user_async(self, user: 'User | int', **kwargs) -> 'User':
        """
        Leave a group if allowed.

        Endpoint: DELETE /api/v1/groups/:group_id/users/:user_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.destroy

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'groups/{}/users/{}'.format(self.id, user_id), _kwargs=combine_kwargs(**kwargs))
        return User(self._requester, response.json())

    def reorder_pinned_topics(self, order: 'iterable sequence[values]', **kwargs) -> 'PaginatedList[DiscussionTopic]':
        """
        Puts the pinned discussion topics in the specified order.
        All pinned topics should be included.

        Endpoint: POST /api/v1/groups/:group_id/discussion_topics/reorder

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.reorder

        Parameters:
            order: iterable sequence of values
        """
        if is_multivalued(order):
            order = ','.join([str(topic_id) for topic_id in order])
        if not isinstance(order, str) or ',' not in order:
            raise ValueError('Param `order` must be a list, tuple, or string.')
        kwargs['order'] = order
        response: 'httpx.Response' = self._requester.request('POST', 'groups/{}/discussion_topics/reorder'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('reorder')

    async def reorder_pinned_topics_async(self, order: 'iterable sequence[values]', **kwargs) -> 'PaginatedList[DiscussionTopic]':
        """
        Puts the pinned discussion topics in the specified order.
        All pinned topics should be included.

        Endpoint: POST /api/v1/groups/:group_id/discussion_topics/reorder

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.reorder

        Parameters:
            order: iterable sequence of values
        """
        if is_multivalued(order):
            order = ','.join([str(topic_id) for topic_id in order])
        if not isinstance(order, str) or ',' not in order:
            raise ValueError('Param `order` must be a list, tuple, or string.')
        kwargs['order'] = order
        response: 'httpx.Response' = await self._requester.request_async('POST', 'groups/{}/discussion_topics/reorder'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('reorder')

    def resolve_path(self, full_path: 'string | None'=None, **kwargs) -> 'PaginatedList[Folder]':
        """
        Returns the paginated list of all of the folders in the given
        path starting at the group root folder. Returns root folder if called
        with no arguments.

        Endpoint: GET /api/v1/groups/group_id/folders/by_path/*full_path

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.resolve_path

        Parameters:
            full_path: string
        """
        if full_path:
            return PaginatedList(Folder, self._requester, 'GET', 'groups/{0}/folders/by_path/{1}'.format(self.id, full_path), _kwargs=combine_kwargs(**kwargs))
        else:
            return PaginatedList(Folder, self._requester, 'GET', 'groups/{0}/folders/by_path'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def resolve_path_async(self, full_path: 'string | None'=None, **kwargs) -> 'PaginatedList[Folder]':
        """
        Returns the paginated list of all of the folders in the given
        path starting at the group root folder. Returns root folder if called
        with no arguments.

        Endpoint: GET /api/v1/groups/group_id/folders/by_path/*full_path

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.resolve_path

        Parameters:
            full_path: string
        """
        if full_path:
            return PaginatedList(Folder, self._requester, 'GET', 'groups/{0}/folders/by_path/{1}'.format(self.id, full_path), _kwargs=combine_kwargs(**kwargs))
        else:
            return PaginatedList(Folder, self._requester, 'GET', 'groups/{0}/folders/by_path'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def set_usage_rights(self, **kwargs) -> 'UsageRights':
        """
        Changes the usage rights for specified files that are under the current group scope

        Endpoint: PUT /api/v1/groups/:group_id/usage_rights

        Reference: https://canvas.instructure.com/doc/api/files.html#method.usage_rights.set_usage_rights
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'groups/{}/usage_rights'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return UsageRights(self._requester, response.json())

    async def set_usage_rights_async(self, **kwargs) -> 'UsageRights':
        """
        Changes the usage rights for specified files that are under the current group scope

        Endpoint: PUT /api/v1/groups/:group_id/usage_rights

        Reference: https://canvas.instructure.com/doc/api/files.html#method.usage_rights.set_usage_rights
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'groups/{}/usage_rights'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return UsageRights(self._requester, response.json())

    def show_front_page(self, **kwargs) -> 'Group':
        """
        Retrieve the content of the front page.

        Endpoint: GET /api/v1/groups/:group_id/front_page

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_front_page
        """
        from .course import Page
        response: 'httpx.Response' = self._requester.request('GET', 'groups/{}/front_page'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        page_json: 'dict' = response.json()
        page_json.update({'group_id': self.id})
        return Page(self._requester, page_json)

    async def show_front_page_async(self, **kwargs) -> 'Group':
        """
        Retrieve the content of the front page.

        Endpoint: GET /api/v1/groups/:group_id/front_page

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_front_page
        """
        from .course import Page
        response: 'httpx.Response' = await self._requester.request_async('GET', 'groups/{}/front_page'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        page_json: 'dict' = response.json()
        page_json.update({'group_id': self.id})
        return Page(self._requester, page_json)

    def update_membership(self, user: 'User | int', **kwargs) -> 'GroupMembership':
        """
        Accept a membership request, or add/remove moderator rights.

        Endpoint: PUT /api/v1/groups/:group_id/users/:user_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.update

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = self._requester.request('PUT', 'groups/{}/users/{}'.format(self.id, user_id), _kwargs=combine_kwargs(**kwargs))
        return GroupMembership(self._requester, response.json())

    async def update_membership_async(self, user: 'User | int', **kwargs) -> 'GroupMembership':
        """
        Accept a membership request, or add/remove moderator rights.

        Endpoint: PUT /api/v1/groups/:group_id/users/:user_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.update

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'groups/{}/users/{}'.format(self.id, user_id), _kwargs=combine_kwargs(**kwargs))
        return GroupMembership(self._requester, response.json())

    def upload(self, file: 'FileOrPathLike | str', **kwargs) -> 'tuple':
        """
        Upload a file to the group.
        Only those with the 'Manage Files' permission on a group can upload files to the group.
        By default, this is anybody participating in the group, or any admin over the group.

        Endpoint: POST /api/v1/groups/:group_id/files

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.create_file

        Parameters:
            file: file or str
        """
        return Uploader(self._requester, 'groups/{}/files'.format(self.id), file, **kwargs).start()

    async def upload_async(self, file: 'FileOrPathLike | str', **kwargs) -> 'tuple':
        """
        Upload a file to the group.
        Only those with the 'Manage Files' permission on a group can upload files to the group.
        By default, this is anybody participating in the group, or any admin over the group.

        Endpoint: POST /api/v1/groups/:group_id/files

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.create_file

        Parameters:
            file: file or str
        """
        return Uploader(self._requester, 'groups/{}/files'.format(self.id), file, **kwargs).start()

class GroupMembership(GroupMembershipModel):

    def __str__(self):
        return '{} - {} ({})'.format(self.user_id, self.group_id, self.id)

    def remove_self(self, **kwargs) -> 'dict':
        """
        Leave a group if allowed.

        Endpoint: DELETE /api/v1/groups/:group_id/memberships/:membership_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'groups/{}/memberships/self'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def remove_self_async(self, **kwargs) -> 'dict':
        """
        Leave a group if allowed.

        Endpoint: DELETE /api/v1/groups/:group_id/memberships/:membership_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'groups/{}/memberships/self'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def remove_user(self, user: 'User | int', **kwargs) -> 'dict':
        """
        Remove user from membership.

        Endpoint: DELETE /api/v1/groups/:group_id/users/:user_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.destroy

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = self._requester.request('DELETE', 'groups/{}/users/{}'.format(self.id, user_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def remove_user_async(self, user: 'User | int', **kwargs) -> 'dict':
        """
        Remove user from membership.

        Endpoint: DELETE /api/v1/groups/:group_id/users/:user_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.destroy

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'groups/{}/users/{}'.format(self.id, user_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def update(self, **kwargs) -> 'GroupMembership':
        """
        Accept a membership request, or add/remove moderator rights.

        Endpoint: PUT /api/v1/groups/:group_id/memberships/:membership_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'groups/{}/memberships/{}'.format(self.group_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return GroupMembership(self._requester, response.json())

    async def update_async(self, **kwargs) -> 'GroupMembership':
        """
        Accept a membership request, or add/remove moderator rights.

        Endpoint: PUT /api/v1/groups/:group_id/memberships/:membership_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'groups/{}/memberships/{}'.format(self.group_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return GroupMembership(self._requester, response.json())

class GroupCategory(GroupCategoryModel):

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)

    def assign_members(self, sync=False, **kwargs) -> 'PaginatedList[User] | Progress':
        """
        Assign unassigned members.

        Endpoint: POST /api/v1/group_categories/:group_category_id/assign_unassigned_members

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.assign_unassigned_members
        """
        from .progress import Progress
        from .user import User
        if sync:
            return PaginatedList(User, self._requester, 'POST', 'group_categories/{}/assign_unassigned_members'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        else:
            response: 'httpx.Response' = self._requester.request('POST', 'group_categories/{}/assign_unassigned_members'.format(self.id), _kwargs=combine_kwargs(**kwargs))
            return Progress(self._requester, response.json())

    async def assign_members_async(self, sync=False, **kwargs) -> 'PaginatedList[User] | Progress':
        """
        Assign unassigned members.

        Endpoint: POST /api/v1/group_categories/:group_category_id/assign_unassigned_members

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.assign_unassigned_members
        """
        from .progress import Progress
        from .user import User
        if sync:
            return PaginatedList(User, self._requester, 'POST', 'group_categories/{}/assign_unassigned_members'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        else:
            response: 'httpx.Response' = await self._requester.request_async('POST', 'group_categories/{}/assign_unassigned_members'.format(self.id), _kwargs=combine_kwargs(**kwargs))
            return Progress(self._requester, response.json())

    def create_group(self, **kwargs) -> 'Group':
        """
        Create a group.

        Endpoint: POST /api/v1/group_categories/:group_category_id/groups

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.create
        """
        response: 'httpx.Response' = self._requester.request('POST', 'group_categories/{}/groups'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Group(self._requester, response.json())

    async def create_group_async(self, **kwargs) -> 'Group':
        """
        Create a group.

        Endpoint: POST /api/v1/group_categories/:group_category_id/groups

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.create
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'group_categories/{}/groups'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Group(self._requester, response.json())

    def delete(self, **kwargs) -> 'empty dict':
        """
        Delete a group category.

        Endpoint: DELETE /api/v1/group_categories/:group_category_id

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'group_categories/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def delete_async(self, **kwargs) -> 'empty dict':
        """
        Delete a group category.

        Endpoint: DELETE /api/v1/group_categories/:group_category_id

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'group_categories/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_groups(self, **kwargs) -> 'PaginatedList[Group]':
        """
        List groups in group category.

        Endpoint: GET /api/v1/group_categories/:group_category_id/groups

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.groups
        """
        return PaginatedList(Group, self._requester, 'GET', 'group_categories/{}/groups'.format(self.id))

    async def get_groups_async(self, **kwargs) -> 'PaginatedList[Group]':
        """
        List groups in group category.

        Endpoint: GET /api/v1/group_categories/:group_category_id/groups

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.groups
        """
        return PaginatedList(Group, self._requester, 'GET', 'group_categories/{}/groups'.format(self.id))

    def get_users(self, **kwargs) -> 'PaginatedList[User]':
        """
        List users in group category.

        Endpoint: GET /api/v1/group_categories/:group_category_id/users

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.users
        """
        from .user import User
        return PaginatedList(User, self._requester, 'GET', 'group_categories/{}/users'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_users_async(self, **kwargs) -> 'PaginatedList[User]':
        """
        List users in group category.

        Endpoint: GET /api/v1/group_categories/:group_category_id/users

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.users
        """
        from .user import User
        return PaginatedList(User, self._requester, 'GET', 'group_categories/{}/users'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def update(self, **kwargs) -> 'GroupCategory':
        """
        Update a group category.

        Endpoint: PUT /api/v1/group_categories/:group_category_id

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'group_categories/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return GroupCategory(self._requester, response.json())

    async def update_async(self, **kwargs) -> 'GroupCategory':
        """
        Update a group category.

        Endpoint: PUT /api/v1/group_categories/:group_category_id

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'group_categories/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return GroupCategory(self._requester, response.json())