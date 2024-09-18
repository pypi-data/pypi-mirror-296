from ..models.admins import Admin as AdminModel
from ..models.authentication_providers import SSOSettings as SSOSettingsModel
from ..models.roles import Role as RoleModel
from ..models.account_notifications import AccountNotification as AccountNotificationModel
from ..models.accounts import Account as AccountModel
import httpx
import typing
if typing.TYPE_CHECKING:
    from .course_event import CourseEvent
    from .scope import Scope
    from .rubric import Rubric
    from .outcome_import import OutcomeImport
    from .feature import FeatureFlag, Feature
    from .enrollment import Enrollment
    from .authentication_event import AuthenticationEvent
    from .outcome import OutcomeLink, OutcomeGroup, OutcomeGroup
    from .paginated_list import PaginatedList
    from .account_calendar import AccountCalendar
    from .grading_period import GradingPeriod
    from .login import Login
    from .sis_import import SisImport
    from .group import Group, GroupCategory
    from .external_tool import ExternalTool
    from .enrollment_term import EnrollmentTerm
    from .course import Course
    from .content_migration import ContentMigration, Migrator
    from .user import User
    from .grading_standard import GradingStandard
    from .authentication_provider import AuthenticationProvider
from .account_calendar import AccountCalendar
from .authentication_event import AuthenticationEvent
from .authentication_provider import AuthenticationProvider
from .canvas_object import CanvasObject
from .content_migration import ContentMigration, Migrator
from .course import Course
from .course_event import CourseEvent
from .enrollment import Enrollment
from .enrollment_term import EnrollmentTerm
from .exceptions import CanvasException, RequiredFieldMissing
from .external_tool import ExternalTool
from .feature import Feature, FeatureFlag
from .grading_period import GradingPeriod
from .grading_standard import GradingStandard
from .group import Group, GroupCategory
from .login import Login
from .outcome import OutcomeGroup, OutcomeLink
from .outcome_import import OutcomeImport
from .paginated_list import PaginatedList
from .rubric import Rubric
from .scope import Scope
from .sis_import import SisImport
from .user import User
from .util import combine_kwargs, file_or_path, obj_or_id, obj_or_str

class Account(AccountModel):

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)

    def abort_sis_imports_pending(self, **kwargs) -> 'bool':
        """
        Aborts all pending (created, but not processed or processing)
        SIS imports for the current account.

        Endpoint: PUT /api/v1/accounts/:account_id/sis_imports/abort_all_pending

        Reference: https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.abort_all_pending
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'accounts/{}/sis_imports/abort_all_pending'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('aborted', False)

    async def abort_sis_imports_pending_async(self, **kwargs) -> 'bool':
        """
        Aborts all pending (created, but not processed or processing)
        SIS imports for the current account.

        Endpoint: PUT /api/v1/accounts/:account_id/sis_imports/abort_all_pending

        Reference: https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.abort_all_pending
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'accounts/{}/sis_imports/abort_all_pending'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('aborted', False)

    def activate_role(self, role: 'Role | int', **kwargs) -> 'Role':
        """
        Reactivate an inactive role.

        Endpoint: POST /api/v1/accounts/:account_id/roles/:id/activate

        Reference: https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.activate_role

        Parameters:
            role: :class:`canvasapi.account.Role` or int
        """
        role_id = obj_or_id(role, 'role', (Role,))
        response: 'httpx.Response' = self._requester.request('POST', 'accounts/{}/roles/{}/activate'.format(self.id, role_id), _kwargs=combine_kwargs(**kwargs))
        return Role(self._requester, response.json())

    async def activate_role_async(self, role: 'Role | int', **kwargs) -> 'Role':
        """
        Reactivate an inactive role.

        Endpoint: POST /api/v1/accounts/:account_id/roles/:id/activate

        Reference: https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.activate_role

        Parameters:
            role: :class:`canvasapi.account.Role` or int
        """
        role_id = obj_or_id(role, 'role', (Role,))
        response: 'httpx.Response' = await self._requester.request_async('POST', 'accounts/{}/roles/{}/activate'.format(self.id, role_id), _kwargs=combine_kwargs(**kwargs))
        return Role(self._requester, response.json())

    def add_authentication_providers(self, **kwargs) -> 'AuthenticationProvider':
        """
        Add external authentication providers for the account

        Endpoint: POST /api/v1/accounts/:account_id/authentication_providers

        Reference: https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.create
        """
        response: 'httpx.Response' = self._requester.request('POST', 'accounts/{}/authentication_providers'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        authentication_providers_json: 'dict' = response.json()
        authentication_providers_json.update({'account_id': self.id})
        return AuthenticationProvider(self._requester, authentication_providers_json)

    async def add_authentication_providers_async(self, **kwargs) -> 'AuthenticationProvider':
        """
        Add external authentication providers for the account

        Endpoint: POST /api/v1/accounts/:account_id/authentication_providers

        Reference: https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.create
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'accounts/{}/authentication_providers'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        authentication_providers_json: 'dict' = response.json()
        authentication_providers_json.update({'account_id': self.id})
        return AuthenticationProvider(self._requester, authentication_providers_json)

    def add_grading_standards(self, title: 'str', grading_scheme_entry: 'list[dict]', **kwargs) -> 'GradingStandard':
        """
        Create a new grading standard for the account.

        Endpoint: POST /api/v1/accounts/:account_id/grading_standards

        Reference: https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.create

        Parameters:
            title: str
            grading_scheme_entry: list[dict]
        """
        if not isinstance(grading_scheme_entry, list) or len(grading_scheme_entry) <= 0:
            raise ValueError('Param `grading_scheme_entry` must be a non-empty list.')
        for entry in grading_scheme_entry:
            if not isinstance(entry, dict):
                raise ValueError('grading_scheme_entry must consist of dictionaries.')
            if 'name' not in entry or 'value' not in entry:
                raise ValueError("Dictionaries with keys 'name' and 'value' are required.")
        kwargs['grading_scheme_entry'] = grading_scheme_entry
        response: 'httpx.Response' = self._requester.request('POST', 'accounts/%s/grading_standards' % self.id, title=title, _kwargs=combine_kwargs(**kwargs))
        return GradingStandard(self._requester, response.json())

    async def add_grading_standards_async(self, title: 'str', grading_scheme_entry: 'list[dict]', **kwargs) -> 'GradingStandard':
        """
        Create a new grading standard for the account.

        Endpoint: POST /api/v1/accounts/:account_id/grading_standards

        Reference: https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.create

        Parameters:
            title: str
            grading_scheme_entry: list[dict]
        """
        if not isinstance(grading_scheme_entry, list) or len(grading_scheme_entry) <= 0:
            raise ValueError('Param `grading_scheme_entry` must be a non-empty list.')
        for entry in grading_scheme_entry:
            if not isinstance(entry, dict):
                raise ValueError('grading_scheme_entry must consist of dictionaries.')
            if 'name' not in entry or 'value' not in entry:
                raise ValueError("Dictionaries with keys 'name' and 'value' are required.")
        kwargs['grading_scheme_entry'] = grading_scheme_entry
        response: 'httpx.Response' = await self._requester.request_async('POST', 'accounts/%s/grading_standards' % self.id, title=title, _kwargs=combine_kwargs(**kwargs))
        return GradingStandard(self._requester, response.json())

    def close_notification_for_user(self, user: 'User | int', notification: 'AccountNotification | int', **kwargs) -> 'AccountNotification':
        """
        If the user no long wants to see a notification, it can be
        excused with this call.

        Endpoint: DELETE /api/v1/accounts/:account_id/users/:user_id/account_notifications/:id

        Reference: https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.user_close_notification

        Parameters:
            user: :class:`canvasapi.user.User` or int
            notification: :class:`canvasapi.account.AccountNotification` or int
        """
        user_id = obj_or_id(user, 'user', (User,))
        notif_id = obj_or_id(notification, 'notification', (AccountNotification,))
        response: 'httpx.Response' = self._requester.request('DELETE', 'accounts/{}/users/{}/account_notifications/{}'.format(self.id, user_id, notif_id), _kwargs=combine_kwargs(**kwargs))
        return AccountNotification(self._requester, response.json())

    async def close_notification_for_user_async(self, user: 'User | int', notification: 'AccountNotification | int', **kwargs) -> 'AccountNotification':
        """
        If the user no long wants to see a notification, it can be
        excused with this call.

        Endpoint: DELETE /api/v1/accounts/:account_id/users/:user_id/account_notifications/:id

        Reference: https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.user_close_notification

        Parameters:
            user: :class:`canvasapi.user.User` or int
            notification: :class:`canvasapi.account.AccountNotification` or int
        """
        user_id = obj_or_id(user, 'user', (User,))
        notif_id = obj_or_id(notification, 'notification', (AccountNotification,))
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'accounts/{}/users/{}/account_notifications/{}'.format(self.id, user_id, notif_id), _kwargs=combine_kwargs(**kwargs))
        return AccountNotification(self._requester, response.json())

    def create_account(self, **kwargs) -> 'Account':
        """
        Create a new root account.

        Endpoint: POST /api/v1/accounts/:account_id/root_accounts

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.accounts.create
        """
        response: 'httpx.Response' = self._requester.request('POST', 'accounts/{}/root_accounts'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Account(self._requester, response.json())

    async def create_account_async(self, **kwargs) -> 'Account':
        """
        Create a new root account.

        Endpoint: POST /api/v1/accounts/:account_id/root_accounts

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.accounts.create
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'accounts/{}/root_accounts'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Account(self._requester, response.json())

    def create_admin(self, user: 'User | int', **kwargs) -> 'Admin':
        """
        Flag an existing user as an admin of the current account.

        Endpoint: POST /api/v1/accounts/:account_id/admins

        Reference: https://canvas.instructure.com/doc/api/admins.html#method.admins.create

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        user_id = obj_or_id(user, 'user', (User,))
        kwargs['user_id'] = user_id
        response: 'httpx.Response' = self._requester.request('POST', 'accounts/{}/admins'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Admin(self._requester, response.json())

    async def create_admin_async(self, user: 'User | int', **kwargs) -> 'Admin':
        """
        Flag an existing user as an admin of the current account.

        Endpoint: POST /api/v1/accounts/:account_id/admins

        Reference: https://canvas.instructure.com/doc/api/admins.html#method.admins.create

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        user_id = obj_or_id(user, 'user', (User,))
        kwargs['user_id'] = user_id
        response: 'httpx.Response' = await self._requester.request_async('POST', 'accounts/{}/admins'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Admin(self._requester, response.json())

    def create_content_migration(self, migration_type: 'str | Migrator', **kwargs) -> 'ContentMigration':
        """
        Create a content migration.

        Endpoint: POST /api/v1/accounts/:account_id/content_migrations

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
        response: 'httpx.Response' = self._requester.request('POST', 'accounts/{}/content_migrations'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'account_id': self.id})
        return ContentMigration(self._requester, response_json)

    async def create_content_migration_async(self, migration_type: 'str | Migrator', **kwargs) -> 'ContentMigration':
        """
        Create a content migration.

        Endpoint: POST /api/v1/accounts/:account_id/content_migrations

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
        response: 'httpx.Response' = await self._requester.request_async('POST', 'accounts/{}/content_migrations'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'account_id': self.id})
        return ContentMigration(self._requester, response_json)

    def create_course(self, **kwargs) -> 'Course':
        """
        Create a course.

        Endpoint: POST /api/v1/accounts/:account_id/courses

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.create
        """
        response: 'httpx.Response' = self._requester.request('POST', 'accounts/{}/courses'.format(self.id), account_id=self.id, _kwargs=combine_kwargs(**kwargs))
        return Course(self._requester, response.json())

    async def create_course_async(self, **kwargs) -> 'Course':
        """
        Create a course.

        Endpoint: POST /api/v1/accounts/:account_id/courses

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.create
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'accounts/{}/courses'.format(self.id), account_id=self.id, _kwargs=combine_kwargs(**kwargs))
        return Course(self._requester, response.json())

    def create_enrollment_term(self, **kwargs) -> 'EnrollmentTerm':
        """
        Create an enrollment term.

        Endpoint: POST /api/v1/accounts/:account_id/terms

        Reference: https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms.create
        """
        response: 'httpx.Response' = self._requester.request('POST', 'accounts/{}/terms'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        enrollment_term_json: 'dict' = response.json()
        enrollment_term_json.update({'account_id': self.id})
        return EnrollmentTerm(self._requester, enrollment_term_json)

    async def create_enrollment_term_async(self, **kwargs) -> 'EnrollmentTerm':
        """
        Create an enrollment term.

        Endpoint: POST /api/v1/accounts/:account_id/terms

        Reference: https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms.create
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'accounts/{}/terms'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        enrollment_term_json: 'dict' = response.json()
        enrollment_term_json.update({'account_id': self.id})
        return EnrollmentTerm(self._requester, enrollment_term_json)

    def create_external_tool(self, name: 'str', privacy_level: 'str', consumer_key: 'str', shared_secret: 'str', **kwargs) -> 'ExternalTool':
        """
        Create an external tool in the current account.

        Endpoint: POST /api/v1/accounts/:account_id/external_tools

        Reference: https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.create

        Parameters:
            name: str
            privacy_level: str
            consumer_key: str
            shared_secret: str
        """
        response: 'httpx.Response' = self._requester.request('POST', 'accounts/{}/external_tools'.format(self.id), name=name, privacy_level=privacy_level, consumer_key=consumer_key, shared_secret=shared_secret, _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'account_id': self.id})
        return ExternalTool(self._requester, response_json)

    async def create_external_tool_async(self, name: 'str', privacy_level: 'str', consumer_key: 'str', shared_secret: 'str', **kwargs) -> 'ExternalTool':
        """
        Create an external tool in the current account.

        Endpoint: POST /api/v1/accounts/:account_id/external_tools

        Reference: https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.create

        Parameters:
            name: str
            privacy_level: str
            consumer_key: str
            shared_secret: str
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'accounts/{}/external_tools'.format(self.id), name=name, privacy_level=privacy_level, consumer_key=consumer_key, shared_secret=shared_secret, _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'account_id': self.id})
        return ExternalTool(self._requester, response_json)

    def create_group_category(self, name: 'str', **kwargs) -> 'GroupCategory':
        """
        Create a Group Category

        Endpoint: POST /api/v1/accounts/:account_id/group_categories

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.create

        Parameters:
            name: str
        """
        response: 'httpx.Response' = self._requester.request('POST', 'accounts/{}/group_categories'.format(self.id), name=name, _kwargs=combine_kwargs(**kwargs))
        return GroupCategory(self._requester, response.json())

    async def create_group_category_async(self, name: 'str', **kwargs) -> 'GroupCategory':
        """
        Create a Group Category

        Endpoint: POST /api/v1/accounts/:account_id/group_categories

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.create

        Parameters:
            name: str
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'accounts/{}/group_categories'.format(self.id), name=name, _kwargs=combine_kwargs(**kwargs))
        return GroupCategory(self._requester, response.json())

    def create_notification(self, account_notification: 'dict', **kwargs) -> 'AccountNotification':
        """
        Create and return a new global notification for an account.

        Endpoint: POST /api/v1/accounts/:account_id/account_notifications

        Reference: https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.create

        Parameters:
            account_notification: dict
        """
        required_key_list = ['subject', 'message', 'start_at', 'end_at']
        required_keys_present = all((x in account_notification for x in required_key_list))
        if isinstance(account_notification, dict) and required_keys_present:
            kwargs['account_notification'] = account_notification
        else:
            raise RequiredFieldMissing("account_notification must be a dictionary with keys 'subject', 'message', 'start_at', and 'end_at'.")
        response: 'httpx.Response' = self._requester.request('POST', 'accounts/{}/account_notifications'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'account_id': self.id})
        return AccountNotification(self._requester, response_json)

    async def create_notification_async(self, account_notification: 'dict', **kwargs) -> 'AccountNotification':
        """
        Create and return a new global notification for an account.

        Endpoint: POST /api/v1/accounts/:account_id/account_notifications

        Reference: https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.create

        Parameters:
            account_notification: dict
        """
        required_key_list = ['subject', 'message', 'start_at', 'end_at']
        required_keys_present = all((x in account_notification for x in required_key_list))
        if isinstance(account_notification, dict) and required_keys_present:
            kwargs['account_notification'] = account_notification
        else:
            raise RequiredFieldMissing("account_notification must be a dictionary with keys 'subject', 'message', 'start_at', and 'end_at'.")
        response: 'httpx.Response' = await self._requester.request_async('POST', 'accounts/{}/account_notifications'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'account_id': self.id})
        return AccountNotification(self._requester, response_json)

    def create_report(self, report_type: 'str', **kwargs) -> 'AccountReport':
        """
        Generates a report of a specific type for the account.

        Endpoint: POST /api/v1/accounts/:account_id/reports/:report

        Reference: https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.create

        Parameters:
            report_type: str
        """
        response: 'httpx.Response' = self._requester.request('POST', 'accounts/{}/reports/{}'.format(self.id, report_type), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'account_id': self.id})
        return AccountReport(self._requester, response_json)

    async def create_report_async(self, report_type: 'str', **kwargs) -> 'AccountReport':
        """
        Generates a report of a specific type for the account.

        Endpoint: POST /api/v1/accounts/:account_id/reports/:report

        Reference: https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.create

        Parameters:
            report_type: str
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'accounts/{}/reports/{}'.format(self.id, report_type), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'account_id': self.id})
        return AccountReport(self._requester, response_json)

    def create_role(self, label: 'str', **kwargs) -> 'Role':
        """
        Create a new course-level or account-level role.

        Endpoint: POST /api/v1/accounts/:account_id/roles

        Reference: https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.add_role

        Parameters:
            label: str
        """
        response: 'httpx.Response' = self._requester.request('POST', 'accounts/{}/roles'.format(self.id), label=label, _kwargs=combine_kwargs(**kwargs))
        return Role(self._requester, response.json())

    async def create_role_async(self, label: 'str', **kwargs) -> 'Role':
        """
        Create a new course-level or account-level role.

        Endpoint: POST /api/v1/accounts/:account_id/roles

        Reference: https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.add_role

        Parameters:
            label: str
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'accounts/{}/roles'.format(self.id), label=label, _kwargs=combine_kwargs(**kwargs))
        return Role(self._requester, response.json())

    def create_sis_import(self, attachment: 'str', **kwargs) -> 'SisImport':
        """
        Create a new SIS import for the current account.

        Endpoint: POST /api/v1/accounts/:account_id/sis_imports

        Reference: https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.create

        Parameters:
            attachment: file or str
        """
        attachment, is_path = file_or_path(attachment)
        try:
            response: 'httpx.Response' = self._requester.request('POST', 'accounts/{}/sis_imports'.format(self.id), file={'attachment': attachment}, _kwargs=combine_kwargs(**kwargs))
            response_json: 'dict' = response.json()
            response_json.update({'account_id': self.id})
            return SisImport(self._requester, response_json)
        finally:
            if is_path:
                attachment.close()

    async def create_sis_import_async(self, attachment: 'str', **kwargs) -> 'SisImport':
        """
        Create a new SIS import for the current account.

        Endpoint: POST /api/v1/accounts/:account_id/sis_imports

        Reference: https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.create

        Parameters:
            attachment: file or str
        """
        attachment, is_path = file_or_path(attachment)
        try:
            response: 'httpx.Response' = await self._requester.request_async('POST', 'accounts/{}/sis_imports'.format(self.id), file={'attachment': attachment}, _kwargs=combine_kwargs(**kwargs))
            response_json: 'dict' = response.json()
            response_json.update({'account_id': self.id})
            return SisImport(self._requester, response_json)
        finally:
            if is_path:
                attachment.close()

    def create_subaccount(self, account: 'str', **kwargs) -> 'Account':
        """
        Add a new sub-account to a given account.

        Endpoint: POST /api/v1/accounts/:account_id/sub_accounts

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.sub_accounts.create

        Parameters:
            account: str
        """
        if isinstance(account, dict) and 'name' in account:
            kwargs['account'] = account
        else:
            raise RequiredFieldMissing("Dictionary with key 'name' is required.")
        response: 'httpx.Response' = self._requester.request('POST', 'accounts/{}/sub_accounts'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Account(self._requester, response.json())

    async def create_subaccount_async(self, account: 'str', **kwargs) -> 'Account':
        """
        Add a new sub-account to a given account.

        Endpoint: POST /api/v1/accounts/:account_id/sub_accounts

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.sub_accounts.create

        Parameters:
            account: str
        """
        if isinstance(account, dict) and 'name' in account:
            kwargs['account'] = account
        else:
            raise RequiredFieldMissing("Dictionary with key 'name' is required.")
        response: 'httpx.Response' = await self._requester.request_async('POST', 'accounts/{}/sub_accounts'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Account(self._requester, response.json())

    def create_user(self, pseudonym: 'dict', **kwargs) -> 'User':
        """
        Create and return a new user and pseudonym for an account.

        Endpoint: POST /api/v1/accounts/:account_id/users

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.create

        Parameters:
            pseudonym: dict
        """
        if isinstance(pseudonym, dict) and 'unique_id' in pseudonym:
            kwargs['pseudonym'] = pseudonym
        else:
            raise RequiredFieldMissing("Dictionary with key 'unique_id' is required.")
        response: 'httpx.Response' = self._requester.request('POST', 'accounts/{}/users'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return User(self._requester, response.json())

    async def create_user_async(self, pseudonym: 'dict', **kwargs) -> 'User':
        """
        Create and return a new user and pseudonym for an account.

        Endpoint: POST /api/v1/accounts/:account_id/users

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.create

        Parameters:
            pseudonym: dict
        """
        if isinstance(pseudonym, dict) and 'unique_id' in pseudonym:
            kwargs['pseudonym'] = pseudonym
        else:
            raise RequiredFieldMissing("Dictionary with key 'unique_id' is required.")
        response: 'httpx.Response' = await self._requester.request_async('POST', 'accounts/{}/users'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return User(self._requester, response.json())

    def create_user_login(self, user: 'dict', login: 'dict', **kwargs) -> 'Login':
        """
        Create a new login for an existing user in the given account

        Endpoint: POST /api/v1/accounts/:account_id/logins

        Reference: https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.create

        Parameters:
            user: `dict`
            login: `dict`
        """
        if isinstance(user, dict) and 'id' in user:
            kwargs['user'] = user
        else:
            raise RequiredFieldMissing("user must be a dictionary with keys 'id'.")
        if isinstance(login, dict) and 'unique_id' in login:
            kwargs['login'] = login
        else:
            raise RequiredFieldMissing("login must be a dictionary with keys 'unique_id'.")
        response: 'httpx.Response' = self._requester.request('POST', 'accounts/{}/logins'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Login(self._requester, response.json())

    async def create_user_login_async(self, user: 'dict', login: 'dict', **kwargs) -> 'Login':
        """
        Create a new login for an existing user in the given account

        Endpoint: POST /api/v1/accounts/:account_id/logins

        Reference: https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.create

        Parameters:
            user: `dict`
            login: `dict`
        """
        if isinstance(user, dict) and 'id' in user:
            kwargs['user'] = user
        else:
            raise RequiredFieldMissing("user must be a dictionary with keys 'id'.")
        if isinstance(login, dict) and 'unique_id' in login:
            kwargs['login'] = login
        else:
            raise RequiredFieldMissing("login must be a dictionary with keys 'unique_id'.")
        response: 'httpx.Response' = await self._requester.request_async('POST', 'accounts/{}/logins'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Login(self._requester, response.json())

    def deactivate_role(self, role: 'Role | int', **kwargs) -> 'Role':
        """
        Deactivate a custom role.

        Endpoint: DELETE /api/v1/accounts/:account_id/roles/:id

        Reference: https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.remove_role

        Parameters:
            role: :class:`canvasapi.account.Role` or int
        """
        role_id = obj_or_id(role, 'role', (Role,))
        response: 'httpx.Response' = self._requester.request('DELETE', 'accounts/{}/roles/{}'.format(self.id, role_id), _kwargs=combine_kwargs(**kwargs))
        return Role(self._requester, response.json())

    async def deactivate_role_async(self, role: 'Role | int', **kwargs) -> 'Role':
        """
        Deactivate a custom role.

        Endpoint: DELETE /api/v1/accounts/:account_id/roles/:id

        Reference: https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.remove_role

        Parameters:
            role: :class:`canvasapi.account.Role` or int
        """
        role_id = obj_or_id(role, 'role', (Role,))
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'accounts/{}/roles/{}'.format(self.id, role_id), _kwargs=combine_kwargs(**kwargs))
        return Role(self._requester, response.json())

    def delete(self, **kwargs) -> 'bool':
        """
        Delete the current account
        
        Note: Cannot delete an account with active courses or active
        sub accounts. Cannot delete a root account.

        Endpoint: DELETE /api/v1/accounts/:account_id/sub_accounts/:id

        Reference: https://canvas.beta.instructure.com/doc/api/accounts.html#method.sub_accounts.destroy
        """
        if not hasattr(self, 'parent_account_id') or not self.parent_account_id:
            raise CanvasException('Cannot delete a root account.')
        response: 'httpx.Response' = self._requester.request('DELETE', 'accounts/{}/sub_accounts/{}'.format(self.parent_account_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('workflow_state') == 'deleted'

    async def delete_async(self, **kwargs) -> 'bool':
        """
        Delete the current account
        
        Note: Cannot delete an account with active courses or active
        sub accounts. Cannot delete a root account.

        Endpoint: DELETE /api/v1/accounts/:account_id/sub_accounts/:id

        Reference: https://canvas.beta.instructure.com/doc/api/accounts.html#method.sub_accounts.destroy
        """
        if not hasattr(self, 'parent_account_id') or not self.parent_account_id:
            raise CanvasException('Cannot delete a root account.')
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'accounts/{}/sub_accounts/{}'.format(self.parent_account_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('workflow_state') == 'deleted'

    def delete_admin(self, user: 'User | int', **kwargs) -> 'Admin':
        """
        Remove an admin role from an existing user in the current account.

        Endpoint: DELETE /api/v1/accounts/:account_id/admins/:user_id

        Reference: https://canvas.instructure.com/doc/api/admins.html#method.admins.destroy

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        user_id = obj_or_id(user, 'user', (User,))
        kwargs['user_id'] = user_id
        response: 'httpx.Response' = self._requester.request('DELETE', 'accounts/{}/admins/{}'.format(self.id, user_id), _kwargs=combine_kwargs(**kwargs))
        return Admin(self._requester, response.json())

    async def delete_admin_async(self, user: 'User | int', **kwargs) -> 'Admin':
        """
        Remove an admin role from an existing user in the current account.

        Endpoint: DELETE /api/v1/accounts/:account_id/admins/:user_id

        Reference: https://canvas.instructure.com/doc/api/admins.html#method.admins.destroy

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        user_id = obj_or_id(user, 'user', (User,))
        kwargs['user_id'] = user_id
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'accounts/{}/admins/{}'.format(self.id, user_id), _kwargs=combine_kwargs(**kwargs))
        return Admin(self._requester, response.json())

    def delete_grading_period(self, grading_period: 'GradingPeriod | int', **kwargs) -> 'bool':
        """
        Delete a grading period for an account.

        Endpoint: DELETE /api/v1/accounts/:account_id/grading_periods/:id

        Reference: https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.destroy

        Parameters:
            grading_period: :class:`canvasapi.grading_period.GradingPeriod` or int
        """
        grading_period_id = obj_or_id(grading_period, 'grading_period', (GradingPeriod,))
        response: 'httpx.Response' = self._requester.request('DELETE', 'accounts/{}/grading_periods/{}'.format(self.id, grading_period_id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('delete')

    async def delete_grading_period_async(self, grading_period: 'GradingPeriod | int', **kwargs) -> 'bool':
        """
        Delete a grading period for an account.

        Endpoint: DELETE /api/v1/accounts/:account_id/grading_periods/:id

        Reference: https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.destroy

        Parameters:
            grading_period: :class:`canvasapi.grading_period.GradingPeriod` or int
        """
        grading_period_id = obj_or_id(grading_period, 'grading_period', (GradingPeriod,))
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'accounts/{}/grading_periods/{}'.format(self.id, grading_period_id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('delete')

    def delete_user(self, user: 'User | int', **kwargs) -> 'User':
        """
        Delete a user record from a Canvas root account.
        
        If a user is associated with multiple root accounts (in a
        multi-tenant instance of Canvas), this action will NOT remove
        them from the other accounts.
        
        WARNING: This API will allow a user to remove themselves from
        the account. If they do this, they won't be able to make API
        calls or log into Canvas at that account.

        Endpoint: DELETE /api/v1/accounts/:account_id/users/:user_id

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.accounts.remove_user

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = self._requester.request('DELETE', 'accounts/{}/users/{}'.format(self.id, user_id), _kwargs=combine_kwargs(**kwargs))
        return User(self._requester, response.json())

    async def delete_user_async(self, user: 'User | int', **kwargs) -> 'User':
        """
        Delete a user record from a Canvas root account.
        
        If a user is associated with multiple root accounts (in a
        multi-tenant instance of Canvas), this action will NOT remove
        them from the other accounts.
        
        WARNING: This API will allow a user to remove themselves from
        the account. If they do this, they won't be able to make API
        calls or log into Canvas at that account.

        Endpoint: DELETE /api/v1/accounts/:account_id/users/:user_id

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.accounts.remove_user

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'accounts/{}/users/{}'.format(self.id, user_id), _kwargs=combine_kwargs(**kwargs))
        return User(self._requester, response.json())

    def get_account_calendar(self, **kwargs) -> 'AccountCalendar':
        """
        Returns information about a single account calendar.

        Endpoint: GET /api/v1/account_calendars/:account_id

        Reference: https://canvas.instructure.com/doc/api/account_calendars.html#method.account_calendars_api.show
        """
        response: 'httpx.Response' = self._requester.request('GET', 'account_calendars/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return AccountCalendar(self._requester, response.json())

    async def get_account_calendar_async(self, **kwargs) -> 'AccountCalendar':
        """
        Returns information about a single account calendar.

        Endpoint: GET /api/v1/account_calendars/:account_id

        Reference: https://canvas.instructure.com/doc/api/account_calendars.html#method.account_calendars_api.show
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'account_calendars/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return AccountCalendar(self._requester, response.json())

    def get_admins(self, **kwargs) -> 'PaginatedList[Admin]':
        """
        Get the paginated list of admins for the current account.

        Endpoint: GET /api/v1/accounts/:account_id/admins

        Reference: https://canvas.instructure.com/doc/api/admins.html#method.admins.index
        """
        return PaginatedList(Admin, self._requester, 'GET', 'accounts/{}/admins'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_admins_async(self, **kwargs) -> 'PaginatedList[Admin]':
        """
        Get the paginated list of admins for the current account.

        Endpoint: GET /api/v1/accounts/:account_id/admins

        Reference: https://canvas.instructure.com/doc/api/admins.html#method.admins.index
        """
        return PaginatedList(Admin, self._requester, 'GET', 'accounts/{}/admins'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_all_account_calendars(self, **kwargs) -> 'PaginatedList[AccountCalendar]':
        """
        Lists all account calendars available to the account given.

        Endpoint: GET /api/v1/accounts/:account_id/account_calendars

        Reference: https://canvas.instructure.com/doc/api/account_calendars.html#method.account_calendars_api.all_calendars
        """
        return PaginatedList(AccountCalendar, self._requester, 'GET', 'accounts/{}/account_calendars'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_all_account_calendars_async(self, **kwargs) -> 'PaginatedList[AccountCalendar]':
        """
        Lists all account calendars available to the account given.

        Endpoint: GET /api/v1/accounts/:account_id/account_calendars

        Reference: https://canvas.instructure.com/doc/api/account_calendars.html#method.account_calendars_api.all_calendars
        """
        return PaginatedList(AccountCalendar, self._requester, 'GET', 'accounts/{}/account_calendars'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_all_outcome_links_in_context(self, **kwargs) -> 'PaginatedList[OutcomeLink]':
        """
        Get all outcome links for context - BETA

        Endpoint: GET /api/v1/accounts/:account_id/outcome_group_links

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link_index
        """
        return PaginatedList(OutcomeLink, self._requester, 'GET', 'accounts/{}/outcome_group_links'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_all_outcome_links_in_context_async(self, **kwargs) -> 'PaginatedList[OutcomeLink]':
        """
        Get all outcome links for context - BETA

        Endpoint: GET /api/v1/accounts/:account_id/outcome_group_links

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link_index
        """
        return PaginatedList(OutcomeLink, self._requester, 'GET', 'accounts/{}/outcome_group_links'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_authentication_events(self, **kwargs) -> 'PaginatedList[AuthenticationEvent]':
        """
        List authentication events for a given account.

        Endpoint: GET /api/v1/audit/authentication/accounts/:account_id

        Reference: https://canvas.instructure.com/doc/api/authentications_log.html#method.authentication_audit_api.for_account
        """
        return PaginatedList(AuthenticationEvent, self._requester, 'GET', 'audit/authentication/accounts/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_authentication_events_async(self, **kwargs) -> 'PaginatedList[AuthenticationEvent]':
        """
        List authentication events for a given account.

        Endpoint: GET /api/v1/audit/authentication/accounts/:account_id

        Reference: https://canvas.instructure.com/doc/api/authentications_log.html#method.authentication_audit_api.for_account
        """
        return PaginatedList(AuthenticationEvent, self._requester, 'GET', 'audit/authentication/accounts/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_authentication_provider(self, authentication_provider: 'AuthenticationProvider | int', **kwargs) -> 'AuthenticationProvider':
        """
        Get the specified authentication provider

        Endpoint: GET /api/v1/accounts/:account_id/authentication_providers/:id

        Reference: https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.show

        Parameters:
            authentication_provider: :class:`canvasapi.authentication_provider.AuthenticationProvider` or int
        """
        authentication_providers_id = obj_or_id(authentication_provider, 'authentication provider', (AuthenticationProvider,))
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/authentication_providers/{}'.format(self.id, authentication_providers_id), _kwargs=combine_kwargs(**kwargs))
        return AuthenticationProvider(self._requester, response.json())

    async def get_authentication_provider_async(self, authentication_provider: 'AuthenticationProvider | int', **kwargs) -> 'AuthenticationProvider':
        """
        Get the specified authentication provider

        Endpoint: GET /api/v1/accounts/:account_id/authentication_providers/:id

        Reference: https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.show

        Parameters:
            authentication_provider: :class:`canvasapi.authentication_provider.AuthenticationProvider` or int
        """
        authentication_providers_id = obj_or_id(authentication_provider, 'authentication provider', (AuthenticationProvider,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/authentication_providers/{}'.format(self.id, authentication_providers_id), _kwargs=combine_kwargs(**kwargs))
        return AuthenticationProvider(self._requester, response.json())

    def get_authentication_providers(self, **kwargs) -> 'PaginatedList[AuthenticationProvider]':
        """
        Return the list of authentication providers

        Endpoint: GET /api/v1/accounts/:account_id/authentication_providers

        Reference: https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.index
        """
        return PaginatedList(AuthenticationProvider, self._requester, 'GET', 'accounts/{}/authentication_providers'.format(self.id), {'account_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_authentication_providers_async(self, **kwargs) -> 'PaginatedList[AuthenticationProvider]':
        """
        Return the list of authentication providers

        Endpoint: GET /api/v1/accounts/:account_id/authentication_providers

        Reference: https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.index
        """
        return PaginatedList(AuthenticationProvider, self._requester, 'GET', 'accounts/{}/authentication_providers'.format(self.id), {'account_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_content_migration(self, content_migration, **kwargs) -> 'ContentMigration':
        """
        Retrive a content migration by its ID

        Endpoint: GET /api/v1/accounts/:account_id/content_migrations/:id

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.show
        """
        migration_id = obj_or_id(content_migration, 'content_migration', (ContentMigration,))
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/content_migrations/{}'.format(self.id, migration_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'account_id': self.id})
        return ContentMigration(self._requester, response_json)

    async def get_content_migration_async(self, content_migration, **kwargs) -> 'ContentMigration':
        """
        Retrive a content migration by its ID

        Endpoint: GET /api/v1/accounts/:account_id/content_migrations/:id

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.show
        """
        migration_id = obj_or_id(content_migration, 'content_migration', (ContentMigration,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/content_migrations/{}'.format(self.id, migration_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'account_id': self.id})
        return ContentMigration(self._requester, response_json)

    def get_content_migrations(self, **kwargs) -> 'PaginatedList[ContentMigration]':
        """
        List content migrations that the current account can view or manage.

        Endpoint: GET /api/v1/accounts/:account_id/content_migrations/

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.index
        """
        return PaginatedList(ContentMigration, self._requester, 'GET', 'accounts/{}/content_migrations'.format(self.id), {'account_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_content_migrations_async(self, **kwargs) -> 'PaginatedList[ContentMigration]':
        """
        List content migrations that the current account can view or manage.

        Endpoint: GET /api/v1/accounts/:account_id/content_migrations/

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.index
        """
        return PaginatedList(ContentMigration, self._requester, 'GET', 'accounts/{}/content_migrations'.format(self.id), {'account_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_courses(self, **kwargs) -> 'PaginatedList[Course]':
        """
        Retrieve the list of courses in this account.

        Endpoint: GET /api/v1/accounts/:account_id/courses

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.accounts.courses_api
        """
        return PaginatedList(Course, self._requester, 'GET', 'accounts/{}/courses'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_courses_async(self, **kwargs) -> 'PaginatedList[Course]':
        """
        Retrieve the list of courses in this account.

        Endpoint: GET /api/v1/accounts/:account_id/courses

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.accounts.courses_api
        """
        return PaginatedList(Course, self._requester, 'GET', 'accounts/{}/courses'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_department_level_grade_data_completed(self, **kwargs) -> 'dict':
        """
        Return the distribution of all concluded grades in the default term

        Endpoint: GET /api/v1/accounts/:account_id/analytics/completed/grades

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_grades
        """
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/analytics/completed/grades'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_department_level_grade_data_completed_async(self, **kwargs) -> 'dict':
        """
        Return the distribution of all concluded grades in the default term

        Endpoint: GET /api/v1/accounts/:account_id/analytics/completed/grades

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_grades
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/analytics/completed/grades'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_department_level_grade_data_current(self, **kwargs) -> 'dict':
        """
        Return the distribution of all available grades in the default term

        Endpoint: GET /api/v1/accounts/:account_id/analytics/current/grades

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_grades
        """
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/analytics/current/grades'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_department_level_grade_data_current_async(self, **kwargs) -> 'dict':
        """
        Return the distribution of all available grades in the default term

        Endpoint: GET /api/v1/accounts/:account_id/analytics/current/grades

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_grades
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/analytics/current/grades'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_department_level_grade_data_with_given_term(self, term_id: 'int | str', **kwargs) -> 'dict':
        """
        Return the distribution of all available or concluded grades with the given term

        Endpoint: GET /api/v1/accounts/:account_id/analytics/terms/:term_id/grades

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_grades

        Parameters:
            term_id: int or str
        """
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/analytics/terms/{}/grades'.format(self.id, term_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_department_level_grade_data_with_given_term_async(self, term_id: 'int | str', **kwargs) -> 'dict':
        """
        Return the distribution of all available or concluded grades with the given term

        Endpoint: GET /api/v1/accounts/:account_id/analytics/terms/:term_id/grades

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_grades

        Parameters:
            term_id: int or str
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/analytics/terms/{}/grades'.format(self.id, term_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_department_level_participation_data_completed(self, **kwargs) -> 'dict':
        """
        Return page view hits all concluded courses in the default term

        Endpoint: GET /api/v1/accounts/:account_id/analytics/completed/activity

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_participation
        """
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/analytics/completed/activity'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_department_level_participation_data_completed_async(self, **kwargs) -> 'dict':
        """
        Return page view hits all concluded courses in the default term

        Endpoint: GET /api/v1/accounts/:account_id/analytics/completed/activity

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_participation
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/analytics/completed/activity'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_department_level_participation_data_current(self, **kwargs) -> 'dict':
        """
        Return page view hits all available courses in the default term

        Endpoint: GET /api/v1/accounts/:account_id/analytics/current/activity

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_participation
        """
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/analytics/current/activity'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_department_level_participation_data_current_async(self, **kwargs) -> 'dict':
        """
        Return page view hits all available courses in the default term

        Endpoint: GET /api/v1/accounts/:account_id/analytics/current/activity

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_participation
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/analytics/current/activity'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_department_level_participation_data_with_given_term(self, term_id: 'int | str', **kwargs) -> 'dict':
        """
        Return page view hits all available or concluded courses in the given term

        Endpoint: GET /api/v1/accounts/:account_id/analytics/terms/:term_id/activity

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_participation

        Parameters:
            term_id: int or str
        """
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/analytics/terms/{}/activity'.format(self.id, term_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_department_level_participation_data_with_given_term_async(self, term_id: 'int | str', **kwargs) -> 'dict':
        """
        Return page view hits all available or concluded courses in the given term

        Endpoint: GET /api/v1/accounts/:account_id/analytics/terms/:term_id/activity

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_participation

        Parameters:
            term_id: int or str
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/analytics/terms/{}/activity'.format(self.id, term_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_department_level_statistics_completed(self, **kwargs) -> 'dict':
        """
        Return all available numeric statistics about the department in the default term

        Endpoint: GET /api/v1/accounts/:account_id/analytics/current/statistics

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_statistics
        """
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/analytics/completed/statistics'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_department_level_statistics_completed_async(self, **kwargs) -> 'dict':
        """
        Return all available numeric statistics about the department in the default term

        Endpoint: GET /api/v1/accounts/:account_id/analytics/current/statistics

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_statistics
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/analytics/completed/statistics'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_department_level_statistics_current(self, **kwargs) -> 'dict':
        """
        Return all available numeric statistics about the department in the default term

        Endpoint: GET /api/v1/accounts/:account_id/analytics/current/statistics

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_statistics
        """
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/analytics/current/statistics'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_department_level_statistics_current_async(self, **kwargs) -> 'dict':
        """
        Return all available numeric statistics about the department in the default term

        Endpoint: GET /api/v1/accounts/:account_id/analytics/current/statistics

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_statistics
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/analytics/current/statistics'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_department_level_statistics_with_given_term(self, term_id: 'int | str', **kwargs) -> 'dict':
        """
        Return numeric statistics about the department with the given term

        Endpoint: GET /api/v1/accounts/:account_id/analytics/terms/:term_id/statistics

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_statistics

        Parameters:
            term_id: int or str
        """
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/analytics/terms/{}/statistics'.format(self.id, term_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_department_level_statistics_with_given_term_async(self, term_id: 'int | str', **kwargs) -> 'dict':
        """
        Return numeric statistics about the department with the given term

        Endpoint: GET /api/v1/accounts/:account_id/analytics/terms/:term_id/statistics

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_statistics

        Parameters:
            term_id: int or str
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/analytics/terms/{}/statistics'.format(self.id, term_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_enabled_features(self, **kwargs) -> 'list[str]':
        """
        Lists all enabled features in an account.

        Endpoint: GET /api/v1/accounts/:account_id/features/enabled

        Reference: https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.enabled_features
        """
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/features/enabled'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_enabled_features_async(self, **kwargs) -> 'list[str]':
        """
        Lists all enabled features in an account.

        Endpoint: GET /api/v1/accounts/:account_id/features/enabled

        Reference: https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.enabled_features
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/features/enabled'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_enrollment(self, enrollment: 'Enrollment | int', **kwargs) -> 'Enrollment':
        """
        Get an enrollment object by ID.

        Endpoint: GET /api/v1/accounts/:account_id/enrollments/:id

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.show

        Parameters:
            enrollment: :class:`canvasapi.enrollment.Enrollment` or int
        """
        enrollment_id = obj_or_id(enrollment, 'enrollment', (Enrollment,))
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/enrollments/{}'.format(self.id, enrollment_id), _kwargs=combine_kwargs(**kwargs))
        return Enrollment(self._requester, response.json())

    async def get_enrollment_async(self, enrollment: 'Enrollment | int', **kwargs) -> 'Enrollment':
        """
        Get an enrollment object by ID.

        Endpoint: GET /api/v1/accounts/:account_id/enrollments/:id

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.show

        Parameters:
            enrollment: :class:`canvasapi.enrollment.Enrollment` or int
        """
        enrollment_id = obj_or_id(enrollment, 'enrollment', (Enrollment,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/enrollments/{}'.format(self.id, enrollment_id), _kwargs=combine_kwargs(**kwargs))
        return Enrollment(self._requester, response.json())

    def get_enrollment_term(self, term: 'EnrollmentTerm | int', **kwargs) -> 'EnrollmentTerm':
        """
        Retrieve the details for an enrollment term in the account. Includes overrides by default.

        Endpoint: GET /api/v1/accounts/:account_id/terms/:id

        Reference: https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms_api.show

        Parameters:
            term: :class:`canvasapi.enrollment_term.EnrollmentTerm` or int
        """
        term_id = obj_or_id(term, 'term', (EnrollmentTerm,))
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/terms/{}'.format(self.id, term_id))
        return EnrollmentTerm(self._requester, response.json())

    async def get_enrollment_term_async(self, term: 'EnrollmentTerm | int', **kwargs) -> 'EnrollmentTerm':
        """
        Retrieve the details for an enrollment term in the account. Includes overrides by default.

        Endpoint: GET /api/v1/accounts/:account_id/terms/:id

        Reference: https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms_api.show

        Parameters:
            term: :class:`canvasapi.enrollment_term.EnrollmentTerm` or int
        """
        term_id = obj_or_id(term, 'term', (EnrollmentTerm,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/terms/{}'.format(self.id, term_id))
        return EnrollmentTerm(self._requester, response.json())

    def get_enrollment_terms(self, **kwargs) -> 'PaginatedList[EnrollmentTerm]':
        """
        List enrollment terms for a context.

        Endpoint: GET /api/v1/accounts/:account_id/terms

        Reference: https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms_api.index
        """
        return PaginatedList(EnrollmentTerm, self._requester, 'GET', 'accounts/{}/terms'.format(self.id), {'account_id': self.id}, _root='enrollment_terms', _kwargs=combine_kwargs(**kwargs))

    async def get_enrollment_terms_async(self, **kwargs) -> 'PaginatedList[EnrollmentTerm]':
        """
        List enrollment terms for a context.

        Endpoint: GET /api/v1/accounts/:account_id/terms

        Reference: https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms_api.index
        """
        return PaginatedList(EnrollmentTerm, self._requester, 'GET', 'accounts/{}/terms'.format(self.id), {'account_id': self.id}, _root='enrollment_terms', _kwargs=combine_kwargs(**kwargs))

    def get_external_tool(self, tool: 'ExternalTool | int', **kwargs) -> 'ExternalTool':
        """
        

        Endpoint: GET /api/v1/accounts/:account_id/external_tools/:external_tool_id

        Reference: https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.show

        Parameters:
            tool: :class:`canvasapi.external_tool.ExternalTool` or int
        """
        tool_id = obj_or_id(tool, 'tool', (ExternalTool,))
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/external_tools/{}'.format(self.id, tool_id), _kwargs=combine_kwargs(**kwargs))
        tool_json: 'dict' = response.json()
        tool_json.update({'account_id': self.id})
        return ExternalTool(self._requester, tool_json)

    async def get_external_tool_async(self, tool: 'ExternalTool | int', **kwargs) -> 'ExternalTool':
        """
        

        Endpoint: GET /api/v1/accounts/:account_id/external_tools/:external_tool_id

        Reference: https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.show

        Parameters:
            tool: :class:`canvasapi.external_tool.ExternalTool` or int
        """
        tool_id = obj_or_id(tool, 'tool', (ExternalTool,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/external_tools/{}'.format(self.id, tool_id), _kwargs=combine_kwargs(**kwargs))
        tool_json: 'dict' = response.json()
        tool_json.update({'account_id': self.id})
        return ExternalTool(self._requester, tool_json)

    def get_external_tools(self, **kwargs) -> 'PaginatedList[ExternalTool]':
        """
        

        Endpoint: GET /api/v1/accounts/:account_id/external_tools

        Reference: https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.index
        """
        return PaginatedList(ExternalTool, self._requester, 'GET', 'accounts/{}/external_tools'.format(self.id), {'account_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_external_tools_async(self, **kwargs) -> 'PaginatedList[ExternalTool]':
        """
        

        Endpoint: GET /api/v1/accounts/:account_id/external_tools

        Reference: https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.index
        """
        return PaginatedList(ExternalTool, self._requester, 'GET', 'accounts/{}/external_tools'.format(self.id), {'account_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_feature_flag(self, feature: 'Feature | str', **kwargs) -> 'FeatureFlag':
        """
        Returns the feature flag that applies to the given account.

        Endpoint: GET /api/v1/accounts/:account_id/features/flags/:feature

        Reference: https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.show

        Parameters:
            feature: :class:`canvasapi.feature.Feature` or str
        """
        feature_name = obj_or_str(feature, 'name', (Feature,))
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/features/flags/{}'.format(self.id, feature_name), _kwargs=combine_kwargs(**kwargs))
        return FeatureFlag(self._requester, response.json())

    async def get_feature_flag_async(self, feature: 'Feature | str', **kwargs) -> 'FeatureFlag':
        """
        Returns the feature flag that applies to the given account.

        Endpoint: GET /api/v1/accounts/:account_id/features/flags/:feature

        Reference: https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.show

        Parameters:
            feature: :class:`canvasapi.feature.Feature` or str
        """
        feature_name = obj_or_str(feature, 'name', (Feature,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/features/flags/{}'.format(self.id, feature_name), _kwargs=combine_kwargs(**kwargs))
        return FeatureFlag(self._requester, response.json())

    def get_features(self, **kwargs) -> 'PaginatedList[Feature]':
        """
        Lists all of the features of an account.

        Endpoint: GET /api/v1/accounts/:account_id/features

        Reference: https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.index
        """
        return PaginatedList(Feature, self._requester, 'GET', 'accounts/{}/features'.format(self.id), {'account_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_features_async(self, **kwargs) -> 'PaginatedList[Feature]':
        """
        Lists all of the features of an account.

        Endpoint: GET /api/v1/accounts/:account_id/features

        Reference: https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.index
        """
        return PaginatedList(Feature, self._requester, 'GET', 'accounts/{}/features'.format(self.id), {'account_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_global_notification(self, notification_id: 'int', **kwargs) -> 'AccountNotification':
        """
        Returns a global notification for the current user.

        Endpoint: GET /api/v1/accounts/:account_id/account_notifications/:id

        Reference: https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.show

        Parameters:
            notification_id: `int`
        """
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/account_notifications/{}'.format(self.id, notification_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'account_id': self.id})
        return AccountNotification(self._requester, response_json)

    async def get_global_notification_async(self, notification_id: 'int', **kwargs) -> 'AccountNotification':
        """
        Returns a global notification for the current user.

        Endpoint: GET /api/v1/accounts/:account_id/account_notifications/:id

        Reference: https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.show

        Parameters:
            notification_id: `int`
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/account_notifications/{}'.format(self.id, notification_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'account_id': self.id})
        return AccountNotification(self._requester, response_json)

    def get_grading_periods(self, **kwargs) -> 'PaginatedList[GradingPeriod]':
        """
        Return a list of grading periods for the associated account.

        Endpoint: GET /api/v1/accounts/:account_id/grading_periods

        Reference: https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.index
        """
        return PaginatedList(GradingPeriod, self._requester, 'GET', 'accounts/{}/grading_periods'.format(self.id), {'account_id': self.id}, _root='grading_periods', kwargs=combine_kwargs(**kwargs))

    async def get_grading_periods_async(self, **kwargs) -> 'PaginatedList[GradingPeriod]':
        """
        Return a list of grading periods for the associated account.

        Endpoint: GET /api/v1/accounts/:account_id/grading_periods

        Reference: https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.index
        """
        return PaginatedList(GradingPeriod, self._requester, 'GET', 'accounts/{}/grading_periods'.format(self.id), {'account_id': self.id}, _root='grading_periods', kwargs=combine_kwargs(**kwargs))

    def get_grading_standards(self, **kwargs) -> 'PaginatedList[GradingStandard]':
        """
        Get a PaginatedList of the grading standards available for the account.

        Endpoint: GET /api/v1/accounts/:account_id/grading_standards

        Reference: https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_index
        """
        return PaginatedList(GradingStandard, self._requester, 'GET', 'accounts/%s/grading_standards' % self.id, _kwargs=combine_kwargs(**kwargs))

    async def get_grading_standards_async(self, **kwargs) -> 'PaginatedList[GradingStandard]':
        """
        Get a PaginatedList of the grading standards available for the account.

        Endpoint: GET /api/v1/accounts/:account_id/grading_standards

        Reference: https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_index
        """
        return PaginatedList(GradingStandard, self._requester, 'GET', 'accounts/%s/grading_standards' % self.id, _kwargs=combine_kwargs(**kwargs))

    def get_group_categories(self, **kwargs) -> 'PaginatedList[GroupCategory]':
        """
        List group categories for a context.

        Endpoint: GET /api/v1/accounts/:account_id/group_categories

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.index
        """
        return PaginatedList(GroupCategory, self._requester, 'GET', 'accounts/{}/group_categories'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_group_categories_async(self, **kwargs) -> 'PaginatedList[GroupCategory]':
        """
        List group categories for a context.

        Endpoint: GET /api/v1/accounts/:account_id/group_categories

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.index
        """
        return PaginatedList(GroupCategory, self._requester, 'GET', 'accounts/{}/group_categories'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_groups(self, **kwargs) -> 'PaginatedList[Group]':
        """
        Return a list of active groups for the specified account.

        Endpoint: GET /api/v1/accounts/:account_id/groups

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.context_index
        """
        return PaginatedList(Group, self._requester, 'GET', 'accounts/{}/groups'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_groups_async(self, **kwargs) -> 'PaginatedList[Group]':
        """
        Return a list of active groups for the specified account.

        Endpoint: GET /api/v1/accounts/:account_id/groups

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.context_index
        """
        return PaginatedList(Group, self._requester, 'GET', 'accounts/{}/groups'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_index_of_reports(self, report_type: 'str', **kwargs) -> 'PaginatedList[AccountReport]':
        """
        Retrieve all reports that have been run for the account of a specific type.

        Endpoint: GET /api/v1/accounts/:account_id/reports/:report

        Reference: https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.index

        Parameters:
            report_type: str
        """
        return PaginatedList(AccountReport, self._requester, 'GET', 'accounts/{}/reports/{}'.format(self.id, report_type), {'account_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_index_of_reports_async(self, report_type: 'str', **kwargs) -> 'PaginatedList[AccountReport]':
        """
        Retrieve all reports that have been run for the account of a specific type.

        Endpoint: GET /api/v1/accounts/:account_id/reports/:report

        Reference: https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.index

        Parameters:
            report_type: str
        """
        return PaginatedList(AccountReport, self._requester, 'GET', 'accounts/{}/reports/{}'.format(self.id, report_type), {'account_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_migration_systems(self, **kwargs) -> 'PaginatedList[Migrator]':
        """
        Return a list of migration systems.

        Endpoint: GET /api/v1/accounts/:account_id/content_migrations/migrators

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.available_migrators
        """
        return PaginatedList(Migrator, self._requester, 'GET', 'accounts/{}/content_migrations/migrators'.format(self.id), {'account_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_migration_systems_async(self, **kwargs) -> 'PaginatedList[Migrator]':
        """
        Return a list of migration systems.

        Endpoint: GET /api/v1/accounts/:account_id/content_migrations/migrators

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.available_migrators
        """
        return PaginatedList(Migrator, self._requester, 'GET', 'accounts/{}/content_migrations/migrators'.format(self.id), {'account_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_outcome_group(self, group: 'OutcomeGroup | int', **kwargs) -> 'OutcomeGroup':
        """
        Returns the details of the Outcome Group with the given id.

        Endpoint: GET /api/v1/accounts/:account_id/outcome_groups/:id

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show

        Parameters:
            group: :class:`canvasapi.outcome.OutcomeGroup` or int
        """
        outcome_group_id = obj_or_id(group, 'outcome group', (OutcomeGroup,))
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/outcome_groups/{}'.format(self.id, outcome_group_id), _kwargs=combine_kwargs(**kwargs))
        return OutcomeGroup(self._requester, response.json())

    async def get_outcome_group_async(self, group: 'OutcomeGroup | int', **kwargs) -> 'OutcomeGroup':
        """
        Returns the details of the Outcome Group with the given id.

        Endpoint: GET /api/v1/accounts/:account_id/outcome_groups/:id

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show

        Parameters:
            group: :class:`canvasapi.outcome.OutcomeGroup` or int
        """
        outcome_group_id = obj_or_id(group, 'outcome group', (OutcomeGroup,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/outcome_groups/{}'.format(self.id, outcome_group_id), _kwargs=combine_kwargs(**kwargs))
        return OutcomeGroup(self._requester, response.json())

    def get_outcome_groups_in_context(self, **kwargs) -> 'PaginatedList[OutcomeGroups]':
        """
        Get all outcome groups for context - BETA

        Endpoint: GET /api/v1/accounts/:account_id/outcome_groups

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.index
        """
        return PaginatedList(OutcomeGroup, self._requester, 'GET', 'accounts/{}/outcome_groups'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_outcome_groups_in_context_async(self, **kwargs) -> 'PaginatedList[OutcomeGroups]':
        """
        Get all outcome groups for context - BETA

        Endpoint: GET /api/v1/accounts/:account_id/outcome_groups

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.index
        """
        return PaginatedList(OutcomeGroup, self._requester, 'GET', 'accounts/{}/outcome_groups'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_outcome_import_status(self, outcome_import: 'OutcomeImport | int | Literal["latest"]', **kwargs) -> 'OutcomeImport':
        """
        Get the status of an already created Outcome import.
        Pass 'latest' for the outcome import id for the latest import.

        Endpoint: GET /api/v1/accounts/:account_id/outcome_imports/:id

        Reference: https://canvas.instructure.com/doc/api/outcome_imports.html#method.outcome_imports_api.show

        Parameters:
            outcome_import: :class:`canvasapi.outcome_import.OutcomeImport`,
int, or string: "latest"
        """
        if outcome_import == 'latest':
            outcome_import_id = 'latest'
        else:
            outcome_import_id = obj_or_id(outcome_import, 'outcome_import', (OutcomeImport,))
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/outcome_imports/{}'.format(self.id, outcome_import_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'account_id': self.id})
        return OutcomeImport(self._requester, response_json)

    async def get_outcome_import_status_async(self, outcome_import: 'OutcomeImport | int | Literal["latest"]', **kwargs) -> 'OutcomeImport':
        """
        Get the status of an already created Outcome import.
        Pass 'latest' for the outcome import id for the latest import.

        Endpoint: GET /api/v1/accounts/:account_id/outcome_imports/:id

        Reference: https://canvas.instructure.com/doc/api/outcome_imports.html#method.outcome_imports_api.show

        Parameters:
            outcome_import: :class:`canvasapi.outcome_import.OutcomeImport`,
int, or string: "latest"
        """
        if outcome_import == 'latest':
            outcome_import_id = 'latest'
        else:
            outcome_import_id = obj_or_id(outcome_import, 'outcome_import', (OutcomeImport,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/outcome_imports/{}'.format(self.id, outcome_import_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'account_id': self.id})
        return OutcomeImport(self._requester, response_json)

    def get_report(self, report_type: 'string', report_id: 'int', **kwargs) -> 'AccountReport':
        """
        Return a report which corresponds to the given report type and ID.

        Endpoint: GET /api/v1/accounts/:account_id/reports/:report/:id

        Reference: https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.show

        Parameters:
            report_type: `string`
            report_id: `int`
        """
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/reports/{}/{}'.format(self.id, report_type, report_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'account_id': self.id})
        return AccountReport(self._requester, response_json)

    async def get_report_async(self, report_type: 'string', report_id: 'int', **kwargs) -> 'AccountReport':
        """
        Return a report which corresponds to the given report type and ID.

        Endpoint: GET /api/v1/accounts/:account_id/reports/:report/:id

        Reference: https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.show

        Parameters:
            report_type: `string`
            report_id: `int`
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/reports/{}/{}'.format(self.id, report_type, report_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'account_id': self.id})
        return AccountReport(self._requester, response_json)

    def get_reports(self, **kwargs) -> 'PaginatedList[AccountReport]':
        """
        Return a list of reports for the current context.

        Endpoint: GET /api/v1/accounts/:account_id/reports

        Reference: https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.available_reports
        """
        return PaginatedList(AccountReport, self._requester, 'GET', 'accounts/{}/reports'.format(self.id), {'account_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_reports_async(self, **kwargs) -> 'PaginatedList[AccountReport]':
        """
        Return a list of reports for the current context.

        Endpoint: GET /api/v1/accounts/:account_id/reports

        Reference: https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.available_reports
        """
        return PaginatedList(AccountReport, self._requester, 'GET', 'accounts/{}/reports'.format(self.id), {'account_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_role(self, role: 'Role | int', **kwargs) -> 'Role':
        """
        Retrieve a role by ID.

        Endpoint: GET /api/v1/accounts/:account_id/roles/:id

        Reference: https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.show

        Parameters:
            role: :class:`canvasapi.account.Role` or int
        """
        role_id = obj_or_id(role, 'role', (Role,))
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/roles/{}'.format(self.id, role_id), _kwargs=combine_kwargs(**kwargs))
        return Role(self._requester, response.json())

    async def get_role_async(self, role: 'Role | int', **kwargs) -> 'Role':
        """
        Retrieve a role by ID.

        Endpoint: GET /api/v1/accounts/:account_id/roles/:id

        Reference: https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.show

        Parameters:
            role: :class:`canvasapi.account.Role` or int
        """
        role_id = obj_or_id(role, 'role', (Role,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/roles/{}'.format(self.id, role_id), _kwargs=combine_kwargs(**kwargs))
        return Role(self._requester, response.json())

    def get_roles(self, **kwargs) -> 'PaginatedList[Role]':
        """
        List the roles available to an account.

        Endpoint: GET /api/v1/accounts/:account_id/roles

        Reference: https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.api_index
        """
        return PaginatedList(Role, self._requester, 'GET', 'accounts/{}/roles'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_roles_async(self, **kwargs) -> 'PaginatedList[Role]':
        """
        List the roles available to an account.

        Endpoint: GET /api/v1/accounts/:account_id/roles

        Reference: https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.api_index
        """
        return PaginatedList(Role, self._requester, 'GET', 'accounts/{}/roles'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_root_outcome_group(self, **kwargs) -> 'OutcomeGroup':
        """
        Redirect to root outcome group for context

        Endpoint: GET /api/v1/accounts/:account_id/root_outcome_group

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.redirect
        """
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/root_outcome_group'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return OutcomeGroup(self._requester, response.json())

    async def get_root_outcome_group_async(self, **kwargs) -> 'OutcomeGroup':
        """
        Redirect to root outcome group for context

        Endpoint: GET /api/v1/accounts/:account_id/root_outcome_group

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.redirect
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/root_outcome_group'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return OutcomeGroup(self._requester, response.json())

    def get_rubric(self, rubric_id: 'int', **kwargs) -> 'Rubric':
        """
        Get a single rubric, based on rubric id.

        Endpoint: GET /api/v1/accounts/:account_id/rubrics/:id

        Reference: https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.show

        Parameters:
            rubric_id: int
        """
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/%s/rubrics/%s' % (self.id, rubric_id), _kwargs=combine_kwargs(**kwargs))
        return Rubric(self._requester, response.json())

    async def get_rubric_async(self, rubric_id: 'int', **kwargs) -> 'Rubric':
        """
        Get a single rubric, based on rubric id.

        Endpoint: GET /api/v1/accounts/:account_id/rubrics/:id

        Reference: https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.show

        Parameters:
            rubric_id: int
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/%s/rubrics/%s' % (self.id, rubric_id), _kwargs=combine_kwargs(**kwargs))
        return Rubric(self._requester, response.json())

    def get_rubrics(self, **kwargs) -> 'PaginatedList[Rubric]':
        """
        Get the paginated list of active rubrics for the current account.

        Endpoint: GET /api/v1/accounts/:account_id/rubrics

        Reference: https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.index
        """
        return PaginatedList(Rubric, self._requester, 'GET', 'accounts/%s/rubrics' % self.id, _kwargs=combine_kwargs(**kwargs))

    async def get_rubrics_async(self, **kwargs) -> 'PaginatedList[Rubric]':
        """
        Get the paginated list of active rubrics for the current account.

        Endpoint: GET /api/v1/accounts/:account_id/rubrics

        Reference: https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.index
        """
        return PaginatedList(Rubric, self._requester, 'GET', 'accounts/%s/rubrics' % self.id, _kwargs=combine_kwargs(**kwargs))

    def get_scopes(self, **kwargs) -> 'PaginatedList[Scope]':
        """
        Retrieve a paginated list of scopes.

        Endpoint: GET /api/v1/accounts/:account_id/scopes

        Reference: https://canvas.instructure.com/doc/api/api_token_scopes.html#method.scopes_api.index
        """
        return PaginatedList(Scope, self._requester, 'GET', 'accounts/{}/scopes'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_scopes_async(self, **kwargs) -> 'PaginatedList[Scope]':
        """
        Retrieve a paginated list of scopes.

        Endpoint: GET /api/v1/accounts/:account_id/scopes

        Reference: https://canvas.instructure.com/doc/api/api_token_scopes.html#method.scopes_api.index
        """
        return PaginatedList(Scope, self._requester, 'GET', 'accounts/{}/scopes'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_single_grading_standard(self, grading_standard_id: 'int', **kwargs) -> 'GradingStandard':
        """
        Get a single grading standard from the account.

        Endpoint: GET /api/v1/accounts/:account_id/grading_standards/:grading_standard_id

        Reference: https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_show

        Parameters:
            grading_standard_id: int
        """
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/%s/grading_standards/%d' % (self.id, grading_standard_id), _kwargs=combine_kwargs(**kwargs))
        return GradingStandard(self._requester, response.json())

    async def get_single_grading_standard_async(self, grading_standard_id: 'int', **kwargs) -> 'GradingStandard':
        """
        Get a single grading standard from the account.

        Endpoint: GET /api/v1/accounts/:account_id/grading_standards/:grading_standard_id

        Reference: https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_show

        Parameters:
            grading_standard_id: int
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/%s/grading_standards/%d' % (self.id, grading_standard_id), _kwargs=combine_kwargs(**kwargs))
        return GradingStandard(self._requester, response.json())

    def get_sis_import(self, sis_import: 'int | str | SisImport', **kwargs) -> 'SisImport':
        """
        Retrieve information on an individual SIS import from this account.

        Endpoint: GET /api/v1/accounts/:account_id/sis_imports/:id

        Reference: https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.show

        Parameters:
            sis_import: int, str or :class:`canvasapi.sis_import.SisImport`
        """
        sis_import_id = obj_or_id(sis_import, 'sis_import', (SisImport,))
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/sis_imports/{}'.format(self.id, sis_import_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'account_id': self.id})
        return SisImport(self._requester, response_json)

    async def get_sis_import_async(self, sis_import: 'int | str | SisImport', **kwargs) -> 'SisImport':
        """
        Retrieve information on an individual SIS import from this account.

        Endpoint: GET /api/v1/accounts/:account_id/sis_imports/:id

        Reference: https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.show

        Parameters:
            sis_import: int, str or :class:`canvasapi.sis_import.SisImport`
        """
        sis_import_id = obj_or_id(sis_import, 'sis_import', (SisImport,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/sis_imports/{}'.format(self.id, sis_import_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'account_id': self.id})
        return SisImport(self._requester, response_json)

    def get_sis_imports(self, **kwargs) -> 'PaginatedList[SisImport]':
        """
        Get the paginated list of SIS imports for the current account.

        Endpoint: GET /api/v1/accounts/:account_id/sis_imports

        Reference: https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.index
        """
        return PaginatedList(SisImport, self._requester, 'GET', 'accounts/{}/sis_imports'.format(self.id), {'account_id': self.id}, _root='sis_imports', _kwargs=combine_kwargs(**kwargs))

    async def get_sis_imports_async(self, **kwargs) -> 'PaginatedList[SisImport]':
        """
        Get the paginated list of SIS imports for the current account.

        Endpoint: GET /api/v1/accounts/:account_id/sis_imports

        Reference: https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.index
        """
        return PaginatedList(SisImport, self._requester, 'GET', 'accounts/{}/sis_imports'.format(self.id), {'account_id': self.id}, _root='sis_imports', _kwargs=combine_kwargs(**kwargs))

    def get_sis_imports_running(self, **kwargs) -> 'PaginatedList[SisImport]':
        """
        Get the paginated list of running SIS imports for the current account.

        Endpoint: GET /api/v1/accounts/:account_id/sis_imports/importing

        Reference: https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.importing
        """
        return PaginatedList(SisImport, self._requester, 'GET', 'accounts/{}/sis_imports/importing'.format(self.id), {'account_id': self.id}, _root='sis_imports', _kwargs=combine_kwargs(**kwargs))

    async def get_sis_imports_running_async(self, **kwargs) -> 'PaginatedList[SisImport]':
        """
        Get the paginated list of running SIS imports for the current account.

        Endpoint: GET /api/v1/accounts/:account_id/sis_imports/importing

        Reference: https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.importing
        """
        return PaginatedList(SisImport, self._requester, 'GET', 'accounts/{}/sis_imports/importing'.format(self.id), {'account_id': self.id}, _root='sis_imports', _kwargs=combine_kwargs(**kwargs))

    def get_subaccounts(self, recursive: 'bool'=False, **kwargs) -> 'PaginatedList[Account]':
        """
        List accounts that are sub-accounts of the given account.

        Endpoint: GET /api/v1/accounts/:account_id/sub_accounts

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.accounts.sub_accounts

        Parameters:
            recursive: bool
        """
        kwargs['recursive'] = recursive
        return PaginatedList(Account, self._requester, 'GET', 'accounts/{}/sub_accounts'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_subaccounts_async(self, recursive: 'bool'=False, **kwargs) -> 'PaginatedList[Account]':
        """
        List accounts that are sub-accounts of the given account.

        Endpoint: GET /api/v1/accounts/:account_id/sub_accounts

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.accounts.sub_accounts

        Parameters:
            recursive: bool
        """
        kwargs['recursive'] = recursive
        return PaginatedList(Account, self._requester, 'GET', 'accounts/{}/sub_accounts'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_user_logins(self, **kwargs) -> 'PaginatedList[Login]':
        """
        Given a user ID, return that user's logins for the given account.

        Endpoint: GET /api/v1/accounts/:account_id/logins

        Reference: https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.index
        """
        return PaginatedList(Login, self._requester, 'GET', 'accounts/{}/logins'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_user_logins_async(self, **kwargs) -> 'PaginatedList[Login]':
        """
        Given a user ID, return that user's logins for the given account.

        Endpoint: GET /api/v1/accounts/:account_id/logins

        Reference: https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.index
        """
        return PaginatedList(Login, self._requester, 'GET', 'accounts/{}/logins'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_user_notifications(self, user: 'User | int', **kwargs) -> 'PaginatedList[AccountNotification]':
        """
        Return a list of all global notifications in the account for
        this user. Any notifications that have been closed by the user
        will not be returned.

        Endpoint: GET /api/v1/accounts/:account_id/users/:user_id/account_notifications

        Reference: https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.user_index

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        user_id = obj_or_id(user, 'user', (User,))
        return PaginatedList(AccountNotification, self._requester, 'GET', 'accounts/{}/users/{}/account_notifications'.format(self.id, user_id), _kwargs=combine_kwargs(**kwargs))

    async def get_user_notifications_async(self, user: 'User | int', **kwargs) -> 'PaginatedList[AccountNotification]':
        """
        Return a list of all global notifications in the account for
        this user. Any notifications that have been closed by the user
        will not be returned.

        Endpoint: GET /api/v1/accounts/:account_id/users/:user_id/account_notifications

        Reference: https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.user_index

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        user_id = obj_or_id(user, 'user', (User,))
        return PaginatedList(AccountNotification, self._requester, 'GET', 'accounts/{}/users/{}/account_notifications'.format(self.id, user_id), _kwargs=combine_kwargs(**kwargs))

    def get_users(self, **kwargs) -> 'PaginatedList[User]':
        """
        Retrieve a list of users associated with this account.

        Endpoint: GET /api/v1/accounts/:account_id/users

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.index
        """
        return PaginatedList(User, self._requester, 'GET', 'accounts/{}/users'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_users_async(self, **kwargs) -> 'PaginatedList[User]':
        """
        Retrieve a list of users associated with this account.

        Endpoint: GET /api/v1/accounts/:account_id/users

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.index
        """
        return PaginatedList(User, self._requester, 'GET', 'accounts/{}/users'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def import_outcome(self, attachment: 'str', **kwargs) -> 'OutcomeImport':
        """
        Import outcome into canvas.

        Endpoint: POST /api/v1/accounts/:account_id/outcome_imports

        Reference: https://canvas.instructure.com/doc/api/outcome_imports.html#method.outcome_imports_api.create

        Parameters:
            attachment: file or str
        """
        attachment, is_path = file_or_path(attachment)
        try:
            response: 'httpx.Response' = self._requester.request('POST', 'accounts/{}/outcome_imports'.format(self.id), file={'attachment': attachment}, _kwargs=combine_kwargs(**kwargs))
            response_json: 'dict' = response.json()
            response_json.update({'account_id': self.id})
            return OutcomeImport(self._requester, response_json)
        finally:
            if is_path:
                attachment.close()

    async def import_outcome_async(self, attachment: 'str', **kwargs) -> 'OutcomeImport':
        """
        Import outcome into canvas.

        Endpoint: POST /api/v1/accounts/:account_id/outcome_imports

        Reference: https://canvas.instructure.com/doc/api/outcome_imports.html#method.outcome_imports_api.create

        Parameters:
            attachment: file or str
        """
        attachment, is_path = file_or_path(attachment)
        try:
            response: 'httpx.Response' = await self._requester.request_async('POST', 'accounts/{}/outcome_imports'.format(self.id), file={'attachment': attachment}, _kwargs=combine_kwargs(**kwargs))
            response_json: 'dict' = response.json()
            response_json.update({'account_id': self.id})
            return OutcomeImport(self._requester, response_json)
        finally:
            if is_path:
                attachment.close()

    def query_audit_by_account(self, **kwargs) -> 'list[CourseEvent]':
        """
        List course change events for a specific account.

        Endpoint: GET /api/v1/audit/course/accounts/:account_id

        Reference: https://canvas.instructure.com/doc/api/course_audit_log.html#method.course_audit_api.for_account
        """
        return PaginatedList(CourseEvent, self._requester, 'GET', 'audit/course/accounts/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def query_audit_by_account_async(self, **kwargs) -> 'list[CourseEvent]':
        """
        List course change events for a specific account.

        Endpoint: GET /api/v1/audit/course/accounts/:account_id

        Reference: https://canvas.instructure.com/doc/api/course_audit_log.html#method.course_audit_api.for_account
        """
        return PaginatedList(CourseEvent, self._requester, 'GET', 'audit/course/accounts/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def show_account_auth_settings(self, **kwargs) -> 'SSOSettings':
        """
        Return the current state of each account level setting

        Endpoint: GET /api/v1/accounts/:account_id/sso_settings

        Reference: https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.show_sso_settings
        """
        response: 'httpx.Response' = self._requester.request('GET', 'accounts/{}/sso_settings'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return SSOSettings(self._requester, response.json())

    async def show_account_auth_settings_async(self, **kwargs) -> 'SSOSettings':
        """
        Return the current state of each account level setting

        Endpoint: GET /api/v1/accounts/:account_id/sso_settings

        Reference: https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.show_sso_settings
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'accounts/{}/sso_settings'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return SSOSettings(self._requester, response.json())

    def update(self, **kwargs) -> 'bool':
        """
        Update an existing account.

        Endpoint: PUT /api/v1/accounts/:id

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.accounts.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'accounts/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if 'name' in response.json():
            super(Account, self).set_attributes(response.json())
            return True
        else:
            return False

    async def update_async(self, **kwargs) -> 'bool':
        """
        Update an existing account.

        Endpoint: PUT /api/v1/accounts/:id

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.accounts.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'accounts/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if 'name' in response.json():
            super(Account, self).set_attributes(response.json())
            return True
        else:
            return False

    def update_account_auth_settings(self, **kwargs) -> 'SSOSettings':
        """
        Return the current state of account level after updated

        Endpoint: PUT /api/v1/accounts/:account_id/sso_settings

        Reference: https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.update_sso_settings
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'accounts/{}/sso_settings'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return SSOSettings(self._requester, response.json())

    async def update_account_auth_settings_async(self, **kwargs) -> 'SSOSettings':
        """
        Return the current state of account level after updated

        Endpoint: PUT /api/v1/accounts/:account_id/sso_settings

        Reference: https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.update_sso_settings
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'accounts/{}/sso_settings'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return SSOSettings(self._requester, response.json())

    def update_account_calendar_visibility(self, **kwargs) -> 'AccountCalendar':
        """
        Update one account calendar's visibility.

        Endpoint: PUT /api/v1/account_calendars/:account_id

        Reference: https://canvas.instructure.com/doc/api/account_calendars.html#method.account_calendars_api.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'account_calendars/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return AccountCalendar(self._requester, response.json())

    async def update_account_calendar_visibility_async(self, **kwargs) -> 'AccountCalendar':
        """
        Update one account calendar's visibility.

        Endpoint: PUT /api/v1/account_calendars/:account_id

        Reference: https://canvas.instructure.com/doc/api/account_calendars.html#method.account_calendars_api.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'account_calendars/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return AccountCalendar(self._requester, response.json())

    def update_many_account_calendars_visibility(self, **kwargs) -> 'AccountCalendar':
        """
        Update many account calendars visibility at once.

        Endpoint: PUT /api/v1/accounts/:account_id/account_calendars

        Reference: https://canvas.instructure.com/doc/api/account_calendars.html#method.account_calendars_api.bulk_update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'accounts/{}/account_calendars'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return AccountCalendar(self._requester, response.json())

    async def update_many_account_calendars_visibility_async(self, **kwargs) -> 'AccountCalendar':
        """
        Update many account calendars visibility at once.

        Endpoint: PUT /api/v1/accounts/:account_id/account_calendars

        Reference: https://canvas.instructure.com/doc/api/account_calendars.html#method.account_calendars_api.bulk_update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'accounts/{}/account_calendars'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return AccountCalendar(self._requester, response.json())

    def update_role(self, role: 'Role | int', **kwargs) -> 'Role':
        """
        Update permissions for an existing role.

        Endpoint: PUT /api/v1/accounts/:account_id/roles/:id

        Reference: https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.update

        Parameters:
            role: :class:`canvasapi.account.Role` or int
        """
        role_id = obj_or_id(role, 'role', (Role,))
        response: 'httpx.Response' = self._requester.request('PUT', 'accounts/{}/roles/{}'.format(self.id, role_id), _kwargs=combine_kwargs(**kwargs))
        return Role(self._requester, response.json())

    async def update_role_async(self, role: 'Role | int', **kwargs) -> 'Role':
        """
        Update permissions for an existing role.

        Endpoint: PUT /api/v1/accounts/:account_id/roles/:id

        Reference: https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.update

        Parameters:
            role: :class:`canvasapi.account.Role` or int
        """
        role_id = obj_or_id(role, 'role', (Role,))
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'accounts/{}/roles/{}'.format(self.id, role_id), _kwargs=combine_kwargs(**kwargs))
        return Role(self._requester, response.json())

class AccountNotification(AccountNotificationModel):

    def __str__(self):
        return '{} ({})'.format(self.subject, self.id)

    def update_global_notification(self, account_notification: 'dict', **kwargs) -> 'AccountNotification':
        """
        Updates a global notification.

        Endpoint: PUT /api/v1/accounts/:account_id/account_notifications/:id

        Reference: https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.update

        Parameters:
            account_notification: dict
        """
        required_key_list = ['subject', 'message', 'start_at', 'end_at']
        required_keys_present = all((x in account_notification for x in required_key_list))
        if isinstance(account_notification, dict) and required_keys_present:
            kwargs['account_notification'] = account_notification
        else:
            raise RequiredFieldMissing("account_notification must be a dictionary with keys 'subject', 'message', 'start_at', and 'end_at'.")
        response: 'httpx.Response' = self._requester.request('PUT', 'accounts/{}/account_notifications/{}'.format(self.account_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return AccountNotification(self._requester, response.json())

    async def update_global_notification_async(self, account_notification: 'dict', **kwargs) -> 'AccountNotification':
        """
        Updates a global notification.

        Endpoint: PUT /api/v1/accounts/:account_id/account_notifications/:id

        Reference: https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.update

        Parameters:
            account_notification: dict
        """
        required_key_list = ['subject', 'message', 'start_at', 'end_at']
        required_keys_present = all((x in account_notification for x in required_key_list))
        if isinstance(account_notification, dict) and required_keys_present:
            kwargs['account_notification'] = account_notification
        else:
            raise RequiredFieldMissing("account_notification must be a dictionary with keys 'subject', 'message', 'start_at', and 'end_at'.")
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'accounts/{}/account_notifications/{}'.format(self.account_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return AccountNotification(self._requester, response.json())

class AccountReport(CanvasObject):

    def __str__(self):
        try:
            return '{} ({})'.format(self.report, self.id)
        except AttributeError:
            return '{} ({})'.format(self.report, self.parameters)

    def delete_report(self, **kwargs) -> 'AccountReport':
        """
        Delete this report.

        Endpoint: DELETE /api/v1/accounts/:account_id/reports/:report/:id

        Reference: https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'accounts/{}/reports/{}/{}'.format(self.account_id, self.report, self.id), _kwargs=combine_kwargs(**kwargs))
        return AccountReport(self._requester, response.json())

    async def delete_report_async(self, **kwargs) -> 'AccountReport':
        """
        Delete this report.

        Endpoint: DELETE /api/v1/accounts/:account_id/reports/:report/:id

        Reference: https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'accounts/{}/reports/{}/{}'.format(self.account_id, self.report, self.id), _kwargs=combine_kwargs(**kwargs))
        return AccountReport(self._requester, response.json())

class Role(RoleModel):

    def __str__(self):
        return '{} ({})'.format(self.label, self.base_role_type)

class SSOSettings(SSOSettingsModel):

    def __str__(self):
        return '{} ({})'.format(self.login_handle_name, self.change_password_url)

class Admin(AdminModel):

    def __str__(self):
        return '{} {} ({})'.format(self.user['name'], self.user['id'], self.id)