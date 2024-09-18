from ..models.users import User as UserModel, UserDisplay as UserDisplayModel
import httpx
import typing
if typing.TYPE_CHECKING:
    from .usage_rights import UsageRights
    from .login import Login
    from .page_view import PageView
    from .license import License
    from .grade_change_log import GradeChangeEvent
    from .file import File
    from .feature import FeatureFlag, Feature
    from .eportfolio import EPortfolio
    from .enrollment import Enrollment
    from .poll_session import PollSession
    from .calendar_event import CalendarEvent
    from .avatar import Avatar
    from .authentication_event import AuthenticationEvent
    from .assignment import Assignment
    from .paginated_list import PaginatedList
    from .course import Course
    from .content_export import ContentExport
    from .pairing_code import PairingCode
    from .folder import Folder
    from .content_migration import ContentMigration, Migrator
    from .communication_channel import CommunicationChannel
from .authentication_event import AuthenticationEvent
from .avatar import Avatar
from .calendar_event import CalendarEvent
from .canvas_object import CanvasObject
from .communication_channel import CommunicationChannel
from .content_export import ContentExport
from .content_migration import ContentMigration, Migrator
from .feature import Feature, FeatureFlag
from .folder import Folder
from .grade_change_log import GradeChangeEvent
from .license import License
from .page_view import PageView
from .paginated_list import PaginatedList
from .pairing_code import PairingCode
from .upload import FileOrPathLike, Uploader
from .usage_rights import UsageRights
from .util import combine_kwargs, obj_or_id, obj_or_str

class User(UserModel):

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)

    def add_observee(self, observee_id: 'int', **kwargs) -> 'User':
        """
        Registers a user as being observed by the given user.

        Endpoint: PUT /api/v1/users/:user_id/observees/:observee_id

        Reference: https://canvas.instructure.com/doc/api/user_observees.html#method.user_observees.update

        Parameters:
            observee_id: int
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'users/{}/observees/{}'.format(self.id, observee_id), _kwargs=combine_kwargs(**kwargs))
        return User(self._requester, response.json())

    async def add_observee_async(self, observee_id: 'int', **kwargs) -> 'User':
        """
        Registers a user as being observed by the given user.

        Endpoint: PUT /api/v1/users/:user_id/observees/:observee_id

        Reference: https://canvas.instructure.com/doc/api/user_observees.html#method.user_observees.update

        Parameters:
            observee_id: int
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'users/{}/observees/{}'.format(self.id, observee_id), _kwargs=combine_kwargs(**kwargs))
        return User(self._requester, response.json())

    def add_observee_with_credentials(self, **kwargs) -> 'User':
        """
        Register the given user to observe another user, given the observee's credentials.

        Endpoint: POST /api/v1/users/:user_id/observees

        Reference: https://canvas.instructure.com/doc/api/user_observees.html#method.user_observees.create
        """
        response: 'httpx.Response' = self._requester.request('POST', 'users/{}/observees'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return User(self._requester, response.json())

    async def add_observee_with_credentials_async(self, **kwargs) -> 'User':
        """
        Register the given user to observe another user, given the observee's credentials.

        Endpoint: POST /api/v1/users/:user_id/observees

        Reference: https://canvas.instructure.com/doc/api/user_observees.html#method.user_observees.create
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'users/{}/observees'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return User(self._requester, response.json())

    def create_communication_channel(self, **kwargs) -> 'CommunicationChannel':
        """
        Create a communication channel for this user

        Endpoint: POST /api/v1/users/:user_id/communication_channels

        Reference: https://canvas.instructure.com/doc/api/communication_channels.html#method.communication_channels.create
        """
        response: 'httpx.Response' = self._requester.request('POST', 'users/{}/communication_channels'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return CommunicationChannel(self._requester, response.json())

    async def create_communication_channel_async(self, **kwargs) -> 'CommunicationChannel':
        """
        Create a communication channel for this user

        Endpoint: POST /api/v1/users/:user_id/communication_channels

        Reference: https://canvas.instructure.com/doc/api/communication_channels.html#method.communication_channels.create
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'users/{}/communication_channels'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return CommunicationChannel(self._requester, response.json())

    def create_content_migration(self, migration_type: 'str | Migrator', **kwargs) -> 'ContentMigration':
        """
        Create a content migration.

        Endpoint: POST /api/v1/users/:user_id/content_migrations

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.create

        Parameters:
            migration_type: str or :class:`canvasapi.content_migration.Migrator`
        """
        if isinstance(migration_type, Migrator):
            kwargs['migration_type'] = migration_type.type
        elif isinstance(migration_type, str):
            kwargs['migration_type'] = migration_type
        else:
            raise TypeError('Parameter migration_type must be of type Migrator or str')
        response: 'httpx.Response' = self._requester.request('POST', 'users/{}/content_migrations'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'user_id': self.id})
        return ContentMigration(self._requester, response_json)

    async def create_content_migration_async(self, migration_type: 'str | Migrator', **kwargs) -> 'ContentMigration':
        """
        Create a content migration.

        Endpoint: POST /api/v1/users/:user_id/content_migrations

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.create

        Parameters:
            migration_type: str or :class:`canvasapi.content_migration.Migrator`
        """
        if isinstance(migration_type, Migrator):
            kwargs['migration_type'] = migration_type.type
        elif isinstance(migration_type, str):
            kwargs['migration_type'] = migration_type
        else:
            raise TypeError('Parameter migration_type must be of type Migrator or str')
        response: 'httpx.Response' = await self._requester.request_async('POST', 'users/{}/content_migrations'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'user_id': self.id})
        return ContentMigration(self._requester, response_json)

    def create_folder(self, name: 'str', **kwargs) -> 'Folder':
        """
        Creates a folder in this user.

        Endpoint: POST /api/v1/users/:user_id/folders

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.create

        Parameters:
            name: str
        """
        response: 'httpx.Response' = self._requester.request('POST', 'users/{}/folders'.format(self.id), name=name, _kwargs=combine_kwargs(**kwargs))
        return Folder(self._requester, response.json())

    async def create_folder_async(self, name: 'str', **kwargs) -> 'Folder':
        """
        Creates a folder in this user.

        Endpoint: POST /api/v1/users/:user_id/folders

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.create

        Parameters:
            name: str
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'users/{}/folders'.format(self.id), name=name, _kwargs=combine_kwargs(**kwargs))
        return Folder(self._requester, response.json())

    def create_pairing_code(self, **kwargs) -> 'PairingCode':
        """
        Create a pairing code for this user.

        Endpoint: POST /api/v1/users/:user_id/observer_pairing_codes

        Reference: https://canvas.instructure.com/doc/api/user_observees.html#method.observer_pairing_codes_api.create
        """
        response: 'httpx.Response' = self._requester.request('POST', 'users/{}/observer_pairing_codes'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return PairingCode(self._requester, response.json())

    async def create_pairing_code_async(self, **kwargs) -> 'PairingCode':
        """
        Create a pairing code for this user.

        Endpoint: POST /api/v1/users/:user_id/observer_pairing_codes

        Reference: https://canvas.instructure.com/doc/api/user_observees.html#method.observer_pairing_codes_api.create
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'users/{}/observer_pairing_codes'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return PairingCode(self._requester, response.json())

    def edit(self, **kwargs) -> 'User':
        """
        Modify this user's information.

        Endpoint: PUT /api/v1/users/:id

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'users/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        super(User, self).set_attributes(response.json())
        return self

    async def edit_async(self, **kwargs) -> 'User':
        """
        Modify this user's information.

        Endpoint: PUT /api/v1/users/:id

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'users/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        super(User, self).set_attributes(response.json())
        return self

    def export_content(self, export_type: 'str', **kwargs) -> 'ContentExport':
        """
        Begin a content export job for a user.

        Endpoint: POST /api/v1/users/:user_id/content_exports

        Reference: https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.create

        Parameters:
            export_type: str
        """
        kwargs['export_type'] = export_type
        response: 'httpx.Response' = self._requester.request('POST', 'users/{}/content_exports'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return ContentExport(self._requester, response.json())

    async def export_content_async(self, export_type: 'str', **kwargs) -> 'ContentExport':
        """
        Begin a content export job for a user.

        Endpoint: POST /api/v1/users/:user_id/content_exports

        Reference: https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.create

        Parameters:
            export_type: str
        """
        kwargs['export_type'] = export_type
        response: 'httpx.Response' = await self._requester.request_async('POST', 'users/{}/content_exports'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return ContentExport(self._requester, response.json())

    def get_assignments(self, course: 'Course | int', **kwargs) -> 'PaginatedList[Assignment]':
        """
        Return the list of assignments for this user if the current
        user (the API key owner) has rights to view. See List assignments for valid arguments.

        Endpoint: GET /api/v1/users/:user_id/courses/:course_id/assignments

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.user_index

        Parameters:
            course: :class:`canvasapi.course.Course` or int
        """
        from .assignment import Assignment
        from .course import Course
        course_id = obj_or_id(course, 'course', (Course,))
        return PaginatedList(Assignment, self._requester, 'GET', 'users/{}/courses/{}/assignments'.format(self.id, course_id), _kwargs=combine_kwargs(**kwargs))

    async def get_assignments_async(self, course: 'Course | int', **kwargs) -> 'PaginatedList[Assignment]':
        """
        Return the list of assignments for this user if the current
        user (the API key owner) has rights to view. See List assignments for valid arguments.

        Endpoint: GET /api/v1/users/:user_id/courses/:course_id/assignments

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.user_index

        Parameters:
            course: :class:`canvasapi.course.Course` or int
        """
        from .assignment import Assignment
        from .course import Course
        course_id = obj_or_id(course, 'course', (Course,))
        return PaginatedList(Assignment, self._requester, 'GET', 'users/{}/courses/{}/assignments'.format(self.id, course_id), _kwargs=combine_kwargs(**kwargs))

    def get_authentication_events(self, **kwargs) -> 'PaginatedList[AuthenticationEvent]':
        """
        List authentication events for a given user.

        Endpoint: GET /api/v1/audit/authentication/users/:user_id

        Reference: https://canvas.instructure.com/doc/api/authentications_log.html#method.authentication_audit_api.for_user
        """
        return PaginatedList(AuthenticationEvent, self._requester, 'GET', 'audit/authentication/users/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_authentication_events_async(self, **kwargs) -> 'PaginatedList[AuthenticationEvent]':
        """
        List authentication events for a given user.

        Endpoint: GET /api/v1/audit/authentication/users/:user_id

        Reference: https://canvas.instructure.com/doc/api/authentications_log.html#method.authentication_audit_api.for_user
        """
        return PaginatedList(AuthenticationEvent, self._requester, 'GET', 'audit/authentication/users/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_avatars(self, **kwargs) -> 'PaginatedList[Avatar]':
        """
        Retrieve the possible user avatar options that can be set with the user update endpoint.

        Endpoint: GET /api/v1/users/:user_id/avatars

        Reference: https://canvas.instructure.com/doc/api/users.html#method.profile.profile_pics
        """
        return PaginatedList(Avatar, self._requester, 'GET', 'users/{}/avatars'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_avatars_async(self, **kwargs) -> 'PaginatedList[Avatar]':
        """
        Retrieve the possible user avatar options that can be set with the user update endpoint.

        Endpoint: GET /api/v1/users/:user_id/avatars

        Reference: https://canvas.instructure.com/doc/api/users.html#method.profile.profile_pics
        """
        return PaginatedList(Avatar, self._requester, 'GET', 'users/{}/avatars'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_calendar_events_for_user(self, **kwargs) -> 'PaginatedList[CalendarEvent]':
        """
        List calendar events that the current user can view or manage.

        Endpoint: GET /api/v1/users/:user_id/calendar_events

        Reference: https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.user_index
        """
        return PaginatedList(CalendarEvent, self._requester, 'GET', 'users/{}/calendar_events'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_calendar_events_for_user_async(self, **kwargs) -> 'PaginatedList[CalendarEvent]':
        """
        List calendar events that the current user can view or manage.

        Endpoint: GET /api/v1/users/:user_id/calendar_events

        Reference: https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.user_index
        """
        return PaginatedList(CalendarEvent, self._requester, 'GET', 'users/{}/calendar_events'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_closed_poll_sessions(self, **kwargs) -> 'PaginatedList[PollSession]':
        """
        Returns a paginated list of all closed poll sessions available to the current user.

        Endpoint: GET /api/v1/poll_sessions/closed

        Reference: https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.closed
        """
        from .poll_session import PollSession
        return PaginatedList(PollSession, self._requester, 'GET', 'poll_sessions/closed', _root='poll_sessions', _kwargs=combine_kwargs(**kwargs))

    async def get_closed_poll_sessions_async(self, **kwargs) -> 'PaginatedList[PollSession]':
        """
        Returns a paginated list of all closed poll sessions available to the current user.

        Endpoint: GET /api/v1/poll_sessions/closed

        Reference: https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.closed
        """
        from .poll_session import PollSession
        return PaginatedList(PollSession, self._requester, 'GET', 'poll_sessions/closed', _root='poll_sessions', _kwargs=combine_kwargs(**kwargs))

    def get_color(self, asset_string: 'str', **kwargs) -> 'dict':
        """
        Return the custom colors that have been saved by this user for a given context.
        
        The `asset_string` parameter should be in the format 'context_id', for example 'course_42'.

        Endpoint: GET /api/v1/users/:id/colors/:asset_string

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.get_custom_color

        Parameters:
            asset_string: str
        """
        response: 'httpx.Response' = self._requester.request('GET', 'users/{}/colors/{}'.format(self.id, asset_string), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_color_async(self, asset_string: 'str', **kwargs) -> 'dict':
        """
        Return the custom colors that have been saved by this user for a given context.
        
        The `asset_string` parameter should be in the format 'context_id', for example 'course_42'.

        Endpoint: GET /api/v1/users/:id/colors/:asset_string

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.get_custom_color

        Parameters:
            asset_string: str
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'users/{}/colors/{}'.format(self.id, asset_string), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_colors(self, **kwargs) -> 'dict':
        """
        Return all custom colors that have been saved by this user.

        Endpoint: GET /api/v1/users/:id/colors

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.get_custom_colors
        """
        response: 'httpx.Response' = self._requester.request('GET', 'users/{}/colors'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_colors_async(self, **kwargs) -> 'dict':
        """
        Return all custom colors that have been saved by this user.

        Endpoint: GET /api/v1/users/:id/colors

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.get_custom_colors
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'users/{}/colors'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_communication_channels(self, **kwargs) -> 'PaginatedList[CommunicationChannel]':
        """
        List communication channels for the specified user, sorted by
        position.

        Endpoint: GET /api/v1/users/:user_id/communication_channels

        Reference: https://canvas.instructure.com/doc/api/communication_channels.html#method.communication_channels.index
        """
        return PaginatedList(CommunicationChannel, self._requester, 'GET', 'users/{}/communication_channels'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_communication_channels_async(self, **kwargs) -> 'PaginatedList[CommunicationChannel]':
        """
        List communication channels for the specified user, sorted by
        position.

        Endpoint: GET /api/v1/users/:user_id/communication_channels

        Reference: https://canvas.instructure.com/doc/api/communication_channels.html#method.communication_channels.index
        """
        return PaginatedList(CommunicationChannel, self._requester, 'GET', 'users/{}/communication_channels'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_content_export(self, content_export: 'int | ContentExport', **kwargs) -> 'ContentExport':
        """
        Return information about a single content export.

        Endpoint: GET /api/v1/users/:user_id/content_exports/:id

        Reference: https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.show

        Parameters:
            content_export: int or :class:`canvasapi.content_export.ContentExport`
        """
        export_id = obj_or_id(content_export, 'content_export', (ContentExport,))
        response: 'httpx.Response' = self._requester.request('GET', 'users/{}/content_exports/{}'.format(self.id, export_id), _kwargs=combine_kwargs(**kwargs))
        return ContentExport(self._requester, response.json())

    async def get_content_export_async(self, content_export: 'int | ContentExport', **kwargs) -> 'ContentExport':
        """
        Return information about a single content export.

        Endpoint: GET /api/v1/users/:user_id/content_exports/:id

        Reference: https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.show

        Parameters:
            content_export: int or :class:`canvasapi.content_export.ContentExport`
        """
        export_id = obj_or_id(content_export, 'content_export', (ContentExport,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'users/{}/content_exports/{}'.format(self.id, export_id), _kwargs=combine_kwargs(**kwargs))
        return ContentExport(self._requester, response.json())

    def get_content_exports(self, **kwargs) -> 'PaginatedList[ContentExport]':
        """
        Return a paginated list of the past and pending content export jobs for a user.

        Endpoint: GET /api/v1/users/:user_id/content_exports

        Reference: https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.index
        """
        return PaginatedList(ContentExport, self._requester, 'GET', 'users/{}/content_exports'.format(self.id), kwargs=combine_kwargs(**kwargs))

    async def get_content_exports_async(self, **kwargs) -> 'PaginatedList[ContentExport]':
        """
        Return a paginated list of the past and pending content export jobs for a user.

        Endpoint: GET /api/v1/users/:user_id/content_exports

        Reference: https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.index
        """
        return PaginatedList(ContentExport, self._requester, 'GET', 'users/{}/content_exports'.format(self.id), kwargs=combine_kwargs(**kwargs))

    def get_content_migration(self, content_migration: 'int | str | ContentMigration', **kwargs) -> 'ContentMigration':
        """
        Retrive a content migration by its ID

        Endpoint: GET /api/v1/users/:user_id/content_migrations/:id

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.show

        Parameters:
            content_migration: int, str or :class:`canvasapi.content_migration.ContentMigration`
        """
        from .content_migration import ContentMigration
        migration_id = obj_or_id(content_migration, 'content_migration', (ContentMigration,))
        response: 'httpx.Response' = self._requester.request('GET', 'users/{}/content_migrations/{}'.format(self.id, migration_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'user_id': self.id})
        return ContentMigration(self._requester, response_json)

    async def get_content_migration_async(self, content_migration: 'int | str | ContentMigration', **kwargs) -> 'ContentMigration':
        """
        Retrive a content migration by its ID

        Endpoint: GET /api/v1/users/:user_id/content_migrations/:id

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.show

        Parameters:
            content_migration: int, str or :class:`canvasapi.content_migration.ContentMigration`
        """
        from .content_migration import ContentMigration
        migration_id = obj_or_id(content_migration, 'content_migration', (ContentMigration,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'users/{}/content_migrations/{}'.format(self.id, migration_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'user_id': self.id})
        return ContentMigration(self._requester, response_json)

    def get_content_migrations(self, **kwargs) -> 'PaginatedList[ContentMigration]':
        """
        List content migrations that the current account can view or manage.

        Endpoint: GET /api/v1/users/:user_id/content_migrations/

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.index
        """
        from .content_migration import ContentMigration
        return PaginatedList(ContentMigration, self._requester, 'GET', 'users/{}/content_migrations'.format(self.id), {'user_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_content_migrations_async(self, **kwargs) -> 'PaginatedList[ContentMigration]':
        """
        List content migrations that the current account can view or manage.

        Endpoint: GET /api/v1/users/:user_id/content_migrations/

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.index
        """
        from .content_migration import ContentMigration
        return PaginatedList(ContentMigration, self._requester, 'GET', 'users/{}/content_migrations'.format(self.id), {'user_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_courses(self, **kwargs) -> 'PaginatedList[Course]':
        """
        Retrieve all courses this user is enrolled in.

        Endpoint: GET /api/v1/users/:user_id/courses

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.user_index
        """
        from .course import Course
        return PaginatedList(Course, self._requester, 'GET', 'users/{}/courses'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_courses_async(self, **kwargs) -> 'PaginatedList[Course]':
        """
        Retrieve all courses this user is enrolled in.

        Endpoint: GET /api/v1/users/:user_id/courses

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.user_index
        """
        from .course import Course
        return PaginatedList(Course, self._requester, 'GET', 'users/{}/courses'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_enabled_features(self, **kwargs) -> 'list[str]':
        """
        Lists all of the enabled features for a user.

        Endpoint: GET /api/v1/users/:user_id/features/enabled

        Reference: https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.enabled_features
        """
        response: 'httpx.Response' = self._requester.request('GET', 'users/{}/features/enabled'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_enabled_features_async(self, **kwargs) -> 'list[str]':
        """
        Lists all of the enabled features for a user.

        Endpoint: GET /api/v1/users/:user_id/features/enabled

        Reference: https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.enabled_features
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'users/{}/features/enabled'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_enrollments(self, **kwargs) -> 'PaginatedList[Enrollment]':
        """
        List all of the enrollments for this user.

        Endpoint: GET /api/v1/users/:user_id/enrollments

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index
        """
        from .enrollment import Enrollment
        return PaginatedList(Enrollment, self._requester, 'GET', 'users/{}/enrollments'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_enrollments_async(self, **kwargs) -> 'PaginatedList[Enrollment]':
        """
        List all of the enrollments for this user.

        Endpoint: GET /api/v1/users/:user_id/enrollments

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index
        """
        from .enrollment import Enrollment
        return PaginatedList(Enrollment, self._requester, 'GET', 'users/{}/enrollments'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_eportfolios(self, **kwargs) -> 'PaginatedList[EPortfolio]':
        """
        Returns a list of ePortfolios for a user.

        Endpoint: GET /api/v1/users/:user_id/eportfolios

        Reference: https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.index
        """
        from .eportfolio import EPortfolio
        return PaginatedList(EPortfolio, self._requester, 'GET', 'users/{}/eportfolios'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_eportfolios_async(self, **kwargs) -> 'PaginatedList[EPortfolio]':
        """
        Returns a list of ePortfolios for a user.

        Endpoint: GET /api/v1/users/:user_id/eportfolios

        Reference: https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.index
        """
        from .eportfolio import EPortfolio
        return PaginatedList(EPortfolio, self._requester, 'GET', 'users/{}/eportfolios'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_feature_flag(self, feature: 'Feature | str', **kwargs) -> 'FeatureFlag':
        """
        Returns the feature flag that applies to the given user.

        Endpoint: GET /api/v1/users/:user_id/features/flags/:feature

        Reference: https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.show

        Parameters:
            feature: :class:`canvasapi.feature.Feature` or str
        """
        feature_name = obj_or_str(feature, 'name', (Feature,))
        response: 'httpx.Response' = self._requester.request('GET', 'users/{}/features/flags/{}'.format(self.id, feature_name), _kwargs=combine_kwargs(**kwargs))
        return FeatureFlag(self._requester, response.json())

    async def get_feature_flag_async(self, feature: 'Feature | str', **kwargs) -> 'FeatureFlag':
        """
        Returns the feature flag that applies to the given user.

        Endpoint: GET /api/v1/users/:user_id/features/flags/:feature

        Reference: https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.show

        Parameters:
            feature: :class:`canvasapi.feature.Feature` or str
        """
        feature_name = obj_or_str(feature, 'name', (Feature,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'users/{}/features/flags/{}'.format(self.id, feature_name), _kwargs=combine_kwargs(**kwargs))
        return FeatureFlag(self._requester, response.json())

    def get_features(self, **kwargs) -> 'PaginatedList[Feature]':
        """
        Lists all of the features for this user.

        Endpoint: GET /api/v1/users/:user_id/features

        Reference: https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.index
        """
        return PaginatedList(Feature, self._requester, 'GET', 'users/{}/features'.format(self.id), {'user_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_features_async(self, **kwargs) -> 'PaginatedList[Feature]':
        """
        Lists all of the features for this user.

        Endpoint: GET /api/v1/users/:user_id/features

        Reference: https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.index
        """
        return PaginatedList(Feature, self._requester, 'GET', 'users/{}/features'.format(self.id), {'user_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_file(self, file: 'File | int', **kwargs) -> 'File':
        """
        Return the standard attachment json object for a file.

        Endpoint: GET /api/v1/users/:user_id/files/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_show

        Parameters:
            file: :class:`canvasapi.file.File` or int
        """
        from .file import File
        file_id = obj_or_id(file, 'file', (File,))
        response: 'httpx.Response' = self._requester.request('GET', 'users/{}/files/{}'.format(self.id, file_id), _kwargs=combine_kwargs(**kwargs))
        return File(self._requester, response.json())

    async def get_file_async(self, file: 'File | int', **kwargs) -> 'File':
        """
        Return the standard attachment json object for a file.

        Endpoint: GET /api/v1/users/:user_id/files/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_show

        Parameters:
            file: :class:`canvasapi.file.File` or int
        """
        from .file import File
        file_id = obj_or_id(file, 'file', (File,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'users/{}/files/{}'.format(self.id, file_id), _kwargs=combine_kwargs(**kwargs))
        return File(self._requester, response.json())

    def get_file_quota(self, **kwargs) -> 'dict':
        """
        Returns the total and used storage quota for the user.

        Endpoint: GET /api/v1/users/:user_id/files/quota

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_quota
        """
        response: 'httpx.Response' = self._requester.request('GET', 'users/{}/files/quota'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_file_quota_async(self, **kwargs) -> 'dict':
        """
        Returns the total and used storage quota for the user.

        Endpoint: GET /api/v1/users/:user_id/files/quota

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_quota
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'users/{}/files/quota'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_files(self, **kwargs) -> 'PaginatedList[File]':
        """
        Returns the paginated list of files for the user.

        Endpoint: GET /api/v1/users/:user_id/files

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_index
        """
        from .file import File
        return PaginatedList(File, self._requester, 'GET', 'users/{}/files'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_files_async(self, **kwargs) -> 'PaginatedList[File]':
        """
        Returns the paginated list of files for the user.

        Endpoint: GET /api/v1/users/:user_id/files

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_index
        """
        from .file import File
        return PaginatedList(File, self._requester, 'GET', 'users/{}/files'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_folder(self, folder: 'Folder | int', **kwargs) -> 'Folder':
        """
        Returns the details for a user's folder

        Endpoint: GET /api/v1/users/:user_id/folders/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.show

        Parameters:
            folder: :class:`canvasapi.folder.Folder` or int
        """
        from .folder import Folder
        folder_id = obj_or_id(folder, 'folder', (Folder,))
        response: 'httpx.Response' = self._requester.request('GET', 'users/{}/folders/{}'.format(self.id, folder_id), _kwargs=combine_kwargs(**kwargs))
        return Folder(self._requester, response.json())

    async def get_folder_async(self, folder: 'Folder | int', **kwargs) -> 'Folder':
        """
        Returns the details for a user's folder

        Endpoint: GET /api/v1/users/:user_id/folders/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.show

        Parameters:
            folder: :class:`canvasapi.folder.Folder` or int
        """
        from .folder import Folder
        folder_id = obj_or_id(folder, 'folder', (Folder,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'users/{}/folders/{}'.format(self.id, folder_id), _kwargs=combine_kwargs(**kwargs))
        return Folder(self._requester, response.json())

    def get_folders(self, **kwargs) -> 'PaginatedList[Folder]':
        """
        Returns the paginated list of all folders for the given user. This will be returned as a
        flat list containing all subfolders as well.

        Endpoint: GET /api/v1/users/:user_id/folders

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.list_all_folders
        """
        return PaginatedList(Folder, self._requester, 'GET', 'users/{}/folders'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_folders_async(self, **kwargs) -> 'PaginatedList[Folder]':
        """
        Returns the paginated list of all folders for the given user. This will be returned as a
        flat list containing all subfolders as well.

        Endpoint: GET /api/v1/users/:user_id/folders

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.list_all_folders
        """
        return PaginatedList(Folder, self._requester, 'GET', 'users/{}/folders'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_grade_change_events_for_grader(self, **kwargs) -> 'PaginatedList[GradeChangeEvent]':
        """
        Returns the grade change events for a grader.

        Endpoint: /api/v1/audit/grade_change/graders/:grader_id  

        Reference: https://canvas.instructure.com/doc/api/grade_change_log.html#method.grade_change_audit_api.for_grader
        """
        return PaginatedList(GradeChangeEvent, self._requester, 'GET', 'audit/grade_change/graders/{}'.format(self.id), _root='events', _kwargs=combine_kwargs(**kwargs))

    async def get_grade_change_events_for_grader_async(self, **kwargs) -> 'PaginatedList[GradeChangeEvent]':
        """
        Returns the grade change events for a grader.

        Endpoint: /api/v1/audit/grade_change/graders/:grader_id  

        Reference: https://canvas.instructure.com/doc/api/grade_change_log.html#method.grade_change_audit_api.for_grader
        """
        return PaginatedList(GradeChangeEvent, self._requester, 'GET', 'audit/grade_change/graders/{}'.format(self.id), _root='events', _kwargs=combine_kwargs(**kwargs))

    def get_grade_change_events_for_student(self, **kwargs) -> 'PaginatedList[GradeChangeEvent]':
        """
        Returns the grade change events for the current student.

        Endpoint: /api/v1/audit/grade_change/students/:student_id  

        Reference: https://canvas.instructure.com/doc/api/grade_change_log.html#method.grade_change_audit_api.for_student
        """
        return PaginatedList(GradeChangeEvent, self._requester, 'GET', 'audit/grade_change/students/{}'.format(self.id), _root='events', _kwargs=combine_kwargs(**kwargs))

    async def get_grade_change_events_for_student_async(self, **kwargs) -> 'PaginatedList[GradeChangeEvent]':
        """
        Returns the grade change events for the current student.

        Endpoint: /api/v1/audit/grade_change/students/:student_id  

        Reference: https://canvas.instructure.com/doc/api/grade_change_log.html#method.grade_change_audit_api.for_student
        """
        return PaginatedList(GradeChangeEvent, self._requester, 'GET', 'audit/grade_change/students/{}'.format(self.id), _root='events', _kwargs=combine_kwargs(**kwargs))

    def get_licenses(self, **kwargs) -> 'PaginatedList[License]':
        """
        Returns a paginated list of the licenses that can be applied to the
        files under the user scope

        Endpoint: GET /api/v1/users/:user_id/content_licenses

        Reference: https://canvas.instructure.com/doc/api/files.html#method.usage_rights.licenses
        """
        return PaginatedList(License, self._requester, 'GET', 'users/{}/content_licenses'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_licenses_async(self, **kwargs) -> 'PaginatedList[License]':
        """
        Returns a paginated list of the licenses that can be applied to the
        files under the user scope

        Endpoint: GET /api/v1/users/:user_id/content_licenses

        Reference: https://canvas.instructure.com/doc/api/files.html#method.usage_rights.licenses
        """
        return PaginatedList(License, self._requester, 'GET', 'users/{}/content_licenses'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_migration_systems(self, **kwargs) -> 'PaginatedList[Migrator]':
        """
        Return a list of migration systems.

        Endpoint: GET /api/v1/users/:user_id/content_migrations/migrators

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.available_migrators
        """
        from .content_migration import Migrator
        return PaginatedList(Migrator, self._requester, 'GET', 'users/{}/content_migrations/migrators'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_migration_systems_async(self, **kwargs) -> 'PaginatedList[Migrator]':
        """
        Return a list of migration systems.

        Endpoint: GET /api/v1/users/:user_id/content_migrations/migrators

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.available_migrators
        """
        from .content_migration import Migrator
        return PaginatedList(Migrator, self._requester, 'GET', 'users/{}/content_migrations/migrators'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_missing_submissions(self, **kwargs) -> 'PaginatedList[Assignment]':
        """
        Retrieve all past-due assignments for which the student does not
        have a submission.

        Endpoint: GET /api/v1/users/:user_id/missing_submissions

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.missing_submissions
        """
        from .assignment import Assignment
        return PaginatedList(Assignment, self._requester, 'GET', 'users/{}/missing_submissions'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_missing_submissions_async(self, **kwargs) -> 'PaginatedList[Assignment]':
        """
        Retrieve all past-due assignments for which the student does not
        have a submission.

        Endpoint: GET /api/v1/users/:user_id/missing_submissions

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.missing_submissions
        """
        from .assignment import Assignment
        return PaginatedList(Assignment, self._requester, 'GET', 'users/{}/missing_submissions'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_observees(self, **kwargs) -> 'PaginatedList[User]':
        """
        List the users that the given user is observing

        Endpoint: GET /api/v1/users/:user_id/observees

        Reference: https://canvas.instructure.com/doc/api/user_observees.html#method.user_observees.index
        """
        return PaginatedList(User, self._requester, 'GET', 'users/{}/observees'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_observees_async(self, **kwargs) -> 'PaginatedList[User]':
        """
        List the users that the given user is observing

        Endpoint: GET /api/v1/users/:user_id/observees

        Reference: https://canvas.instructure.com/doc/api/user_observees.html#method.user_observees.index
        """
        return PaginatedList(User, self._requester, 'GET', 'users/{}/observees'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_observers(self, **kwargs) -> 'PaginatedList[User]':
        """
        List the users that are observing the given user.

        Endpoint: GET /api/v1/users/:user_id/observers

        Reference: https://canvas.instructure.com/doc/api/user_observees.html#method.user_observees.observers
        """
        return PaginatedList(User, self._requester, 'GET', 'users/{}/observers'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_observers_async(self, **kwargs) -> 'PaginatedList[User]':
        """
        List the users that are observing the given user.

        Endpoint: GET /api/v1/users/:user_id/observers

        Reference: https://canvas.instructure.com/doc/api/user_observees.html#method.user_observees.observers
        """
        return PaginatedList(User, self._requester, 'GET', 'users/{}/observers'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_open_poll_sessions(self, **kwargs) -> 'PaginatedList[PollSession]':
        """
        Returns a paginated list of all opened poll sessions available to the current user.

        Endpoint: GET /api/v1/poll_sessions/opened

        Reference: https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.opened
        """
        from .poll_session import PollSession
        return PaginatedList(PollSession, self._requester, 'GET', 'poll_sessions/opened', _root='poll_sessions', _kwargs=combine_kwargs(**kwargs))

    async def get_open_poll_sessions_async(self, **kwargs) -> 'PaginatedList[PollSession]':
        """
        Returns a paginated list of all opened poll sessions available to the current user.

        Endpoint: GET /api/v1/poll_sessions/opened

        Reference: https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.opened
        """
        from .poll_session import PollSession
        return PaginatedList(PollSession, self._requester, 'GET', 'poll_sessions/opened', _root='poll_sessions', _kwargs=combine_kwargs(**kwargs))

    def get_page_views(self, **kwargs) -> 'PaginatedList[PageView]':
        """
        Retrieve this user's page views.

        Endpoint: GET /api/v1/users/:user_id/page_views

        Reference: https://canvas.instructure.com/doc/api/users.html#method.page_views.index
        """
        return PaginatedList(PageView, self._requester, 'GET', 'users/{}/page_views'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_page_views_async(self, **kwargs) -> 'PaginatedList[PageView]':
        """
        Retrieve this user's page views.

        Endpoint: GET /api/v1/users/:user_id/page_views

        Reference: https://canvas.instructure.com/doc/api/users.html#method.page_views.index
        """
        return PaginatedList(PageView, self._requester, 'GET', 'users/{}/page_views'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_profile(self, **kwargs) -> 'dict':
        """
        Retrieve this user's profile.

        Endpoint: GET /api/v1/users/:user_id/profile

        Reference: https://canvas.instructure.com/doc/api/users.html#method.profile.settings
        """
        response: 'httpx.Response' = self._requester.request('GET', 'users/{}/profile'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_profile_async(self, **kwargs) -> 'dict':
        """
        Retrieve this user's profile.

        Endpoint: GET /api/v1/users/:user_id/profile

        Reference: https://canvas.instructure.com/doc/api/users.html#method.profile.settings
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'users/{}/profile'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_user_logins(self, **kwargs) -> 'PaginatedList[Login]':
        """
        Given a user ID, return that user's logins for the given account.

        Endpoint: GET /api/v1/users/:user_id/logins

        Reference: https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.index
        """
        from .login import Login
        return PaginatedList(Login, self._requester, 'GET', 'users/{}/logins'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_user_logins_async(self, **kwargs) -> 'PaginatedList[Login]':
        """
        Given a user ID, return that user's logins for the given account.

        Endpoint: GET /api/v1/users/:user_id/logins

        Reference: https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.index
        """
        from .login import Login
        return PaginatedList(Login, self._requester, 'GET', 'users/{}/logins'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def merge_into(self, destination_user: 'User | int', **kwargs) -> 'User':
        """
        Merge this user into another user.

        Endpoint: PUT /api/v1/users/:id/merge_into/:destination_user_id

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.merge_into

        Parameters:
            destination_user: :class:`canvasapi.user.User` or int
        """
        dest_user_id = obj_or_id(destination_user, 'destination_user', (User,))
        response: 'httpx.Response' = self._requester.request('PUT', 'users/{}/merge_into/{}'.format(self.id, dest_user_id), _kwargs=combine_kwargs(**kwargs))
        super(User, self).set_attributes(response.json())
        return self

    async def merge_into_async(self, destination_user: 'User | int', **kwargs) -> 'User':
        """
        Merge this user into another user.

        Endpoint: PUT /api/v1/users/:id/merge_into/:destination_user_id

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.merge_into

        Parameters:
            destination_user: :class:`canvasapi.user.User` or int
        """
        dest_user_id = obj_or_id(destination_user, 'destination_user', (User,))
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'users/{}/merge_into/{}'.format(self.id, dest_user_id), _kwargs=combine_kwargs(**kwargs))
        super(User, self).set_attributes(response.json())
        return self

    def moderate_all_eportfolios(self, **kwargs) -> 'PaginatedList[EPortfolio]':
        """
        Update the spam_status for all active eportfolios of a user.
        Only available to admins who can moderate_user_content.

        Endpoint: PUT /api/v1/users/:user_id/eportfolios

        Reference: https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.moderate_all
        """
        from .eportfolio import EPortfolio
        return PaginatedList(EPortfolio, self._requester, 'PUT', 'users/{}/eportfolios'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def moderate_all_eportfolios_async(self, **kwargs) -> 'PaginatedList[EPortfolio]':
        """
        Update the spam_status for all active eportfolios of a user.
        Only available to admins who can moderate_user_content.

        Endpoint: PUT /api/v1/users/:user_id/eportfolios

        Reference: https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.moderate_all
        """
        from .eportfolio import EPortfolio
        return PaginatedList(EPortfolio, self._requester, 'PUT', 'users/{}/eportfolios'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def remove_observee(self, observee_id: 'int', **kwargs) -> 'User':
        """
        Unregisters a user as being observed by the given user.

        Endpoint: DELETE /api/v1/users/:user_id/observees/:observee_id

        Reference: https://canvas.instructure.com/doc/api/user_observees.html#method.user_observees.destroy

        Parameters:
            observee_id: int
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'users/{}/observees/{}'.format(self.id, observee_id), _kwargs=combine_kwargs(**kwargs))
        return User(self._requester, response.json())

    async def remove_observee_async(self, observee_id: 'int', **kwargs) -> 'User':
        """
        Unregisters a user as being observed by the given user.

        Endpoint: DELETE /api/v1/users/:user_id/observees/:observee_id

        Reference: https://canvas.instructure.com/doc/api/user_observees.html#method.user_observees.destroy

        Parameters:
            observee_id: int
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'users/{}/observees/{}'.format(self.id, observee_id), _kwargs=combine_kwargs(**kwargs))
        return User(self._requester, response.json())

    def remove_usage_rights(self, **kwargs) -> 'dict':
        """
        Changes the usage rights for specified files that are under the user scope

        Endpoint: DELETE /api/v1/users/:user_id/usage_rights

        Reference: https://canvas.instructure.com/doc/api/files.html#method.usage_rights.remove_usage_rights
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'users/{}/usage_rights'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def remove_usage_rights_async(self, **kwargs) -> 'dict':
        """
        Changes the usage rights for specified files that are under the user scope

        Endpoint: DELETE /api/v1/users/:user_id/usage_rights

        Reference: https://canvas.instructure.com/doc/api/files.html#method.usage_rights.remove_usage_rights
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'users/{}/usage_rights'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def resolve_path(self, full_path: 'string | None'=None, **kwargs) -> 'PaginatedList[Folder]':
        """
        Returns the paginated list of all of the folders in the given
        path starting at the user root folder. Returns root folder if called
        with no arguments.

        Endpoint: GET /api/v1/users/:user_id/folders/by_path/*full_path

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.resolve_path

        Parameters:
            full_path: string
        """
        if full_path:
            return PaginatedList(Folder, self._requester, 'GET', 'users/{0}/folders/by_path/{1}'.format(self.id, full_path), _kwargs=combine_kwargs(**kwargs))
        else:
            return PaginatedList(Folder, self._requester, 'GET', 'users/{0}/folders/by_path'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def resolve_path_async(self, full_path: 'string | None'=None, **kwargs) -> 'PaginatedList[Folder]':
        """
        Returns the paginated list of all of the folders in the given
        path starting at the user root folder. Returns root folder if called
        with no arguments.

        Endpoint: GET /api/v1/users/:user_id/folders/by_path/*full_path

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.resolve_path

        Parameters:
            full_path: string
        """
        if full_path:
            return PaginatedList(Folder, self._requester, 'GET', 'users/{0}/folders/by_path/{1}'.format(self.id, full_path), _kwargs=combine_kwargs(**kwargs))
        else:
            return PaginatedList(Folder, self._requester, 'GET', 'users/{0}/folders/by_path'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def set_usage_rights(self, **kwargs) -> 'UsageRights':
        """
        Changes the usage rights for specified files that are under the user scope

        Endpoint: PUT /api/v1/users/:user_id/usage_rights

        Reference: https://canvas.instructure.com/doc/api/files.html#method.usage_rights.set_usage_rights
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'users/{}/usage_rights'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return UsageRights(self._requester, response.json())

    async def set_usage_rights_async(self, **kwargs) -> 'UsageRights':
        """
        Changes the usage rights for specified files that are under the user scope

        Endpoint: PUT /api/v1/users/:user_id/usage_rights

        Reference: https://canvas.instructure.com/doc/api/files.html#method.usage_rights.set_usage_rights
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'users/{}/usage_rights'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return UsageRights(self._requester, response.json())

    def show_observee(self, observee_id: 'int', **kwargs) -> 'User':
        """
        Gets information about an observed user.

        Endpoint: GET /api/v1/users/:user_id/observees/:observee_id

        Reference: https://canvas.instructure.com/doc/api/user_observees.html#method.user_observees.show

        Parameters:
            observee_id: int
        """
        response: 'httpx.Response' = self._requester.request('GET', 'users/{}/observees/{}'.format(self.id, observee_id), _kwargs=combine_kwargs(**kwargs))
        return User(self._requester, response.json())

    async def show_observee_async(self, observee_id: 'int', **kwargs) -> 'User':
        """
        Gets information about an observed user.

        Endpoint: GET /api/v1/users/:user_id/observees/:observee_id

        Reference: https://canvas.instructure.com/doc/api/user_observees.html#method.user_observees.show

        Parameters:
            observee_id: int
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'users/{}/observees/{}'.format(self.id, observee_id), _kwargs=combine_kwargs(**kwargs))
        return User(self._requester, response.json())

    def terminate_sessions(self, **kwargs) -> 'str':
        """
        Terminate all sessions for a user.
        
        This includes all browser-based sessions and all access tokens,
        including manually generated ones.

        Endpoint: DELETE /api/v1/users/:id/sessions

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.terminate_sessions
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'users/{}/sessions'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def terminate_sessions_async(self, **kwargs) -> 'str':
        """
        Terminate all sessions for a user.
        
        This includes all browser-based sessions and all access tokens,
        including manually generated ones.

        Endpoint: DELETE /api/v1/users/:id/sessions

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.terminate_sessions
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'users/{}/sessions'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def update_color(self, asset_string: 'str', hexcode: 'str', **kwargs) -> 'dict':
        """
        Update a custom color for this user for a given context.
        
        This allows colors for the calendar and elsewhere to be customized on a user basis.
        
        The `asset_string` parameter should be in the format 'context_id', for example 'course_42'.
        The `hexcode` parameter need not include the '#'.

        Endpoint: PUT /api/v1/users/:id/colors/:asset_string

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.set_custom_color

        Parameters:
            asset_string: str
            hexcode: str
        """
        kwargs['hexcode'] = hexcode
        response: 'httpx.Response' = self._requester.request('PUT', 'users/{}/colors/{}'.format(self.id, asset_string), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def update_color_async(self, asset_string: 'str', hexcode: 'str', **kwargs) -> 'dict':
        """
        Update a custom color for this user for a given context.
        
        This allows colors for the calendar and elsewhere to be customized on a user basis.
        
        The `asset_string` parameter should be in the format 'context_id', for example 'course_42'.
        The `hexcode` parameter need not include the '#'.

        Endpoint: PUT /api/v1/users/:id/colors/:asset_string

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.set_custom_color

        Parameters:
            asset_string: str
            hexcode: str
        """
        kwargs['hexcode'] = hexcode
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'users/{}/colors/{}'.format(self.id, asset_string), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def update_settings(self, **kwargs) -> 'dict':
        """
        Update this user's settings.

        Endpoint: PUT /api/v1/users/:id/settings

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.settings
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'users/{}/settings'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def update_settings_async(self, **kwargs) -> 'dict':
        """
        Update this user's settings.

        Endpoint: PUT /api/v1/users/:id/settings

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.settings
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'users/{}/settings'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def upload(self, file: 'FileOrPathLike | str', **kwargs) -> 'tuple':
        """
        Upload a file for a user.
        
        NOTE: You *must* have authenticated with this user's API key to
        upload on their behalf no matter what permissions the issuer of the
        request has.

        Endpoint: POST /api/v1/users/:user_id/files

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.create_file

        Parameters:
            file: file or str
        """
        return Uploader(self._requester, 'users/{}/files'.format(self.id), file, **kwargs).start()

    async def upload_async(self, file: 'FileOrPathLike | str', **kwargs) -> 'tuple':
        """
        Upload a file for a user.
        
        NOTE: You *must* have authenticated with this user's API key to
        upload on their behalf no matter what permissions the issuer of the
        request has.

        Endpoint: POST /api/v1/users/:user_id/files

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.create_file

        Parameters:
            file: file or str
        """
        return Uploader(self._requester, 'users/{}/files'.format(self.id), file, **kwargs).start()

class UserDisplay(UserDisplayModel):

    def __str__(self):
        return '{}'.format(self.display_name)