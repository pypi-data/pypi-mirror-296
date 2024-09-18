from ..models.content_migrations import ContentMigration as ContentMigrationModel, MigrationIssue as MigrationIssueModel, Migrator as MigratorModel
import httpx
import typing
if typing.TYPE_CHECKING:
    from .progress import Progress
    from .user import User
    from .group import Group
    from .course import Course
    from .account import Account
from .canvas_object import CanvasObject
from .paginated_list import PaginatedList
from .util import combine_kwargs, obj_or_id

class ContentMigration(ContentMigrationModel):

    def __str__(self):
        return '{} {}'.format(self.migration_type_title, self.id)

    @property
    def _parent_id(self) -> 'int':
        """
        Return the id of the account, course, group, or user that spawned
        this content migration.
        """
        if hasattr(self, 'course_id'):
            return self.course_id
        elif hasattr(self, 'group_id'):
            return self.group_id
        elif hasattr(self, 'account_id'):
            return self.account_id
        elif hasattr(self, 'user_id'):
            return self.user_id
        else:
            raise ValueError('Content Migration does not have an account_id, course_id, group_id or user_id')

    @property
    def _parent_type(self) -> 'str':
        """
        Return whether the content migration was spawned from a course or group.
        """
        if hasattr(self, 'course_id'):
            return 'course'
        elif hasattr(self, 'group_id'):
            return 'group'
        elif hasattr(self, 'account_id'):
            return 'account'
        elif hasattr(self, 'user_id'):
            return 'user'
        else:
            raise ValueError('Content Migration does not have an account_id, course_id, group_id or user_id')

    def get_migration_issue(self, migration_issue: 'int | str | ContentMigration', **kwargs) -> 'MigrationIssue':
        """
        List a single issue for this content migration.

        Endpoint: GET /api/v1/accounts/:account_id/content_migrations/:content_migration_id/migration_issues/:id

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.migration_issues.show

        Parameters:
            migration_issue: int, str or :class:`canvasapi.content_migration.ContentMigration`
        """
        migration_issue_id = obj_or_id(migration_issue, 'migration_issue', (MigrationIssue,))
        response: 'httpx.Response' = self._requester.request('GET', '{}s/{}/content_migrations/{}/migration_issues/{}'.format(self._parent_type, self._parent_id, self.id, migration_issue_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'context_type': self._parent_type, 'context_id': self._parent_id, 'content_migration_id': self.id})
        return MigrationIssue(self._requester, response_json)

    async def get_migration_issue_async(self, migration_issue: 'int | str | ContentMigration', **kwargs) -> 'MigrationIssue':
        """
        List a single issue for this content migration.

        Endpoint: GET /api/v1/accounts/:account_id/content_migrations/:content_migration_id/migration_issues/:id

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.migration_issues.show

        Parameters:
            migration_issue: int, str or :class:`canvasapi.content_migration.ContentMigration`
        """
        migration_issue_id = obj_or_id(migration_issue, 'migration_issue', (MigrationIssue,))
        response: 'httpx.Response' = await self._requester.request_async('GET', '{}s/{}/content_migrations/{}/migration_issues/{}'.format(self._parent_type, self._parent_id, self.id, migration_issue_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'context_type': self._parent_type, 'context_id': self._parent_id, 'content_migration_id': self.id})
        return MigrationIssue(self._requester, response_json)

    def get_migration_issues(self, **kwargs) -> 'MigrationIssue':
        """
        List issues for this content migration

        Endpoint: GET /api/v1/accounts/:account_id/content_migrations/:content_migration_id/migration_issues

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.migration_issues.index
        """
        return PaginatedList(MigrationIssue, self._requester, 'GET', '{}s/{}/content_migrations/{}/migration_issues/'.format(self._parent_type, self._parent_id, self.id), {'context_type': self._parent_type, 'context_id': self._parent_id, 'content_migration_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_migration_issues_async(self, **kwargs) -> 'MigrationIssue':
        """
        List issues for this content migration

        Endpoint: GET /api/v1/accounts/:account_id/content_migrations/:content_migration_id/migration_issues

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.migration_issues.index
        """
        return PaginatedList(MigrationIssue, self._requester, 'GET', '{}s/{}/content_migrations/{}/migration_issues/'.format(self._parent_type, self._parent_id, self.id), {'context_type': self._parent_type, 'context_id': self._parent_id, 'content_migration_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_parent(self, **kwargs) -> 'Account | Course | Group | User':
        """
        Return the object that spawned this content migration.
        """
        from .account import Account
        from .course import Course
        from .group import Group
        from .user import User
        response: 'httpx.Response' = self._requester.request('GET', '{}s/{}'.format(self._parent_type, self._parent_id), _kwargs=combine_kwargs(**kwargs))
        if self._parent_type == 'group':
            return Group(self._requester, response.json())
        elif self._parent_type == 'course':
            return Course(self._requester, response.json())
        elif self._parent_type == 'account':
            return Account(self._requester, response.json())
        elif self._parent_type == 'user':
            return User(self._requester, response.json())

    async def get_parent_async(self, **kwargs) -> 'Account | Course | Group | User':
        """
        Return the object that spawned this content migration.
        """
        from .account import Account
        from .course import Course
        from .group import Group
        from .user import User
        response: 'httpx.Response' = await self._requester.request_async('GET', '{}s/{}'.format(self._parent_type, self._parent_id), _kwargs=combine_kwargs(**kwargs))
        if self._parent_type == 'group':
            return Group(self._requester, response.json())
        elif self._parent_type == 'course':
            return Course(self._requester, response.json())
        elif self._parent_type == 'account':
            return Account(self._requester, response.json())
        elif self._parent_type == 'user':
            return User(self._requester, response.json())

    def get_progress(self, **kwargs) -> 'Progress':
        """
        Get the progress of the current content migration.

        Endpoint: GET /api/v1/progress/:id

        Reference: https://canvas.instructure.com/doc/api/progress.html#method.progress.show
        """
        from .progress import Progress
        progress_id = self.progress_url.split('/')[-1]
        response: 'httpx.Response' = self._requester.request('GET', 'progress/{}'.format(progress_id), _kwargs=combine_kwargs(**kwargs))
        return Progress(self._requester, response.json())

    async def get_progress_async(self, **kwargs) -> 'Progress':
        """
        Get the progress of the current content migration.

        Endpoint: GET /api/v1/progress/:id

        Reference: https://canvas.instructure.com/doc/api/progress.html#method.progress.show
        """
        from .progress import Progress
        progress_id = self.progress_url.split('/')[-1]
        response: 'httpx.Response' = await self._requester.request_async('GET', 'progress/{}'.format(progress_id), _kwargs=combine_kwargs(**kwargs))
        return Progress(self._requester, response.json())

    def get_selective_data(self, **kwargs) -> 'ContentMigrationSelectionNode':
        """
        Return the selective data associated with this content migration. Use this to get a list
        of available objects to import for a migration created with 'waiting_for_select=True'.

        Endpoint: GET /api/v1/accounts/:account_id/content_migrations/:content_migration_id/selective_data

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.content_list
        """
        return PaginatedList(ContentMigrationSelectionNode, self._requester, 'GET', '{}s/{}/content_migrations/{}/selective_data'.format(self._parent_type, self._parent_id, self.id), {'context_type': self._parent_type, 'context_id': self._parent_id, 'content_migration_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_selective_data_async(self, **kwargs) -> 'ContentMigrationSelectionNode':
        """
        Return the selective data associated with this content migration. Use this to get a list
        of available objects to import for a migration created with 'waiting_for_select=True'.

        Endpoint: GET /api/v1/accounts/:account_id/content_migrations/:content_migration_id/selective_data

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.content_list
        """
        return PaginatedList(ContentMigrationSelectionNode, self._requester, 'GET', '{}s/{}/content_migrations/{}/selective_data'.format(self._parent_type, self._parent_id, self.id), {'context_type': self._parent_type, 'context_id': self._parent_id, 'content_migration_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def update(self, **kwargs) -> 'bool':
        """
        Update an existing content migration.

        Endpoint: PUT /api/v1/accounts/:account_id/content_migrations/:id

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', '{}s/{}/content_migrations/{}'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        if 'migration_type' in response.json():
            super(ContentMigration, self).set_attributes(response.json())
            return True
        else:
            return False

    async def update_async(self, **kwargs) -> 'bool':
        """
        Update an existing content migration.

        Endpoint: PUT /api/v1/accounts/:account_id/content_migrations/:id

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', '{}s/{}/content_migrations/{}'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        if 'migration_type' in response.json():
            super(ContentMigration, self).set_attributes(response.json())
            return True
        else:
            return False

class ContentMigrationSelectionNode(CanvasObject):

    def __str__(self):
        return '{}'.format(self.type)

class MigrationIssue(MigrationIssueModel):

    def __str__(self):
        return '{}: {}'.format(self.id, self.description)

    def update(self, **kwargs) -> 'bool':
        """
        Update an existing migration issue.

        Endpoint: PUT /api/v1/accounts/:account_id/content_migrations/:content_migration_id/migration_issues/:id

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.migration_issues.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', '{}s/{}/content_migrations/{}/migration_issues/{}'.format(self.context_type, self.context_id, self.content_migration_id, self.id), _kwargs=combine_kwargs(**kwargs))
        if 'workflow_state' in response.json():
            super(MigrationIssue, self).set_attributes(response.json())
            return True
        else:
            return False

    async def update_async(self, **kwargs) -> 'bool':
        """
        Update an existing migration issue.

        Endpoint: PUT /api/v1/accounts/:account_id/content_migrations/:content_migration_id/migration_issues/:id

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.migration_issues.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', '{}s/{}/content_migrations/{}/migration_issues/{}'.format(self.context_type, self.context_id, self.content_migration_id, self.id), _kwargs=combine_kwargs(**kwargs))
        if 'workflow_state' in response.json():
            super(MigrationIssue, self).set_attributes(response.json())
            return True
        else:
            return False

class Migrator(MigratorModel):

    def __str__(self):
        return '{}'.format(self.type)