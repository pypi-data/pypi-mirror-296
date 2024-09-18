from ..models.blueprint_courses import BlueprintTemplate as BlueprintTemplateModel, BlueprintMigration as BlueprintMigrationModel, ChangeRecord as ChangeRecordModel, BlueprintSubscription as BlueprintSubscriptionModel
import httpx
import typing
if typing.TYPE_CHECKING:
    from .course import Course
    from .paginated_list import PaginatedList
from .canvas_object import CanvasObject
from .paginated_list import PaginatedList
from .util import combine_kwargs, obj_or_id

class BlueprintTemplate(BlueprintTemplateModel):

    def __str__(self):
        return '{}'.format(self.id)

    def associated_course_migration(self, **kwargs) -> 'BlueprintMigration':
        """
        Start a migration to update content in all associated courses.

        Endpoint: POST /api/v1/courses/:course_id/blueprint_templates/:template_id/migrations

        Reference: https://canvas.instructure.com/doc/api/blueprint_courses.html#method.        master_courses/master_templates.queue_migration
        """
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/blueprint_templates/{}/migrations'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return BlueprintMigration(self._requester, response_json)

    async def associated_course_migration_async(self, **kwargs) -> 'BlueprintMigration':
        """
        Start a migration to update content in all associated courses.

        Endpoint: POST /api/v1/courses/:course_id/blueprint_templates/:template_id/migrations

        Reference: https://canvas.instructure.com/doc/api/blueprint_courses.html#method.        master_courses/master_templates.queue_migration
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/blueprint_templates/{}/migrations'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return BlueprintMigration(self._requester, response_json)

    def change_blueprint_restrictions(self, content_type: 'str', content_id: 'int', restricted: 'bool', **kwargs) -> 'bool':
        """
        Set or remove restrictions on a blueprint course object.
        Must have all three parameters for this function call to work.

        Endpoint: PUT /api/v1/courses/:course_id/blueprint_templates/:template_id/restrict_item

        Reference: https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses/master_templates.restrict_item

        Parameters:
            content_type: str
            content_id: int
            restricted: bool
        """
        kwargs['content_type'] = content_type
        kwargs['content_id'] = content_id
        kwargs['restricted'] = restricted
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/blueprint_templates/{}/restrict_item'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('success', False)

    async def change_blueprint_restrictions_async(self, content_type: 'str', content_id: 'int', restricted: 'bool', **kwargs) -> 'bool':
        """
        Set or remove restrictions on a blueprint course object.
        Must have all three parameters for this function call to work.

        Endpoint: PUT /api/v1/courses/:course_id/blueprint_templates/:template_id/restrict_item

        Reference: https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses/master_templates.restrict_item

        Parameters:
            content_type: str
            content_id: int
            restricted: bool
        """
        kwargs['content_type'] = content_type
        kwargs['content_id'] = content_id
        kwargs['restricted'] = restricted
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/blueprint_templates/{}/restrict_item'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('success', False)

    def get_associated_courses(self, **kwargs) -> 'PaginatedList[Course]':
        """
        Return a list of courses associated with the given blueprint.

        Endpoint: GET /api/v1/courses/:course_id/blueprint_templates/:template_id/

        Reference: associated_courses         <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses/master_templates.associated_courses
        """
        from .course import Course
        return PaginatedList(Course, self._requester, 'GET', 'courses/{}/blueprint_templates/{}/associated_courses'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_associated_courses_async(self, **kwargs) -> 'PaginatedList[Course]':
        """
        Return a list of courses associated with the given blueprint.

        Endpoint: GET /api/v1/courses/:course_id/blueprint_templates/:template_id/

        Reference: associated_courses         <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses/master_templates.associated_courses
        """
        from .course import Course
        return PaginatedList(Course, self._requester, 'GET', 'courses/{}/blueprint_templates/{}/associated_courses'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))

    def get_unsynced_changes(self, **kwargs) -> 'PaginatedList[ChangeRecord]':
        """
        Return changes made to associated courses of a blueprint course.

        Endpoint: GET /api/v1/courses/:course_id/blueprint_templates/:template_id/unsynced_changes

        Reference: https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses        /master_templates.unsynced_changes
        """
        return PaginatedList(ChangeRecord, self._requester, 'GET', 'courses/{}/blueprint_templates/{}/unsynced_changes'.format(self.course_id, self.id), kwargs=combine_kwargs(**kwargs))

    async def get_unsynced_changes_async(self, **kwargs) -> 'PaginatedList[ChangeRecord]':
        """
        Return changes made to associated courses of a blueprint course.

        Endpoint: GET /api/v1/courses/:course_id/blueprint_templates/:template_id/unsynced_changes

        Reference: https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses        /master_templates.unsynced_changes
        """
        return PaginatedList(ChangeRecord, self._requester, 'GET', 'courses/{}/blueprint_templates/{}/unsynced_changes'.format(self.course_id, self.id), kwargs=combine_kwargs(**kwargs))

    def list_blueprint_migrations(self, **kwargs) -> 'PaginatedList[BlueprintMigration]':
        """
        Return a paginated list of migrations for the template.

        Endpoint: GET api/v1/courses/:course_id/blueprint_templates/:template_id/migrations

        Reference: https://canvas.instructure.com/doc/api/blueprint_courses.html#method.         master_courses/master_templates.migrations_index
        """
        return PaginatedList(BlueprintMigration, self._requester, 'GET', 'courses/{}/blueprint_templates/{}/migrations'.format(self.course_id, self.id), {'course_id': self.course_id}, kwargs=combine_kwargs(**kwargs))

    async def list_blueprint_migrations_async(self, **kwargs) -> 'PaginatedList[BlueprintMigration]':
        """
        Return a paginated list of migrations for the template.

        Endpoint: GET api/v1/courses/:course_id/blueprint_templates/:template_id/migrations

        Reference: https://canvas.instructure.com/doc/api/blueprint_courses.html#method.         master_courses/master_templates.migrations_index
        """
        return PaginatedList(BlueprintMigration, self._requester, 'GET', 'courses/{}/blueprint_templates/{}/migrations'.format(self.course_id, self.id), {'course_id': self.course_id}, kwargs=combine_kwargs(**kwargs))

    def show_blueprint_migration(self, migration: 'int | BlueprintMigration', **kwargs) -> 'BlueprintMigration':
        """
        Return the status of a blueprint migration.

        Endpoint: GET /api/v1/courses/:course_id/blueprint_templates/:template_id

        Reference: /migrations/:id        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses/        master_templates.migrations_show

        Parameters:
            migration: int or :class:`canvasapi.blueprint.BlueprintMigration`
        """
        migration_id = obj_or_id(migration, 'migration', (BlueprintMigration,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/blueprint_templates/{}/migrations/{}'.format(self.course_id, self.id, migration_id), kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return BlueprintMigration(self._requester, response_json)

    async def show_blueprint_migration_async(self, migration: 'int | BlueprintMigration', **kwargs) -> 'BlueprintMigration':
        """
        Return the status of a blueprint migration.

        Endpoint: GET /api/v1/courses/:course_id/blueprint_templates/:template_id

        Reference: /migrations/:id        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses/        master_templates.migrations_show

        Parameters:
            migration: int or :class:`canvasapi.blueprint.BlueprintMigration`
        """
        migration_id = obj_or_id(migration, 'migration', (BlueprintMigration,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/blueprint_templates/{}/migrations/{}'.format(self.course_id, self.id, migration_id), kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return BlueprintMigration(self._requester, response_json)

    def update_associated_courses(self, **kwargs) -> 'bool':
        """
        Add or remove new associations for the blueprint template.

        Endpoint: PUT /api/v1/courses/:course_id/blueprint_templates/:template_id/update_associations

        Reference: https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses/master_templates.update_associations
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/blueprint_templates/{}/update_associations'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('success', False)

    async def update_associated_courses_async(self, **kwargs) -> 'bool':
        """
        Add or remove new associations for the blueprint template.

        Endpoint: PUT /api/v1/courses/:course_id/blueprint_templates/:template_id/update_associations

        Reference: https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses/master_templates.update_associations
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/blueprint_templates/{}/update_associations'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('success', False)

class BlueprintMigration(BlueprintMigrationModel):

    def __str__(self):
        return '{} {}'.format(self.id, self.template_id)

    def get_details(self, **kwargs) -> 'PaginatedList[ChangeRecord]':
        """
        Return the changes that were made in a blueprint migration.

        Endpoint: GET /api/v1/courses/:course_id/blueprint_templates/:template_id

        Reference: /migrations/:id/details        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.        master_courses/master_templates.migration_details
        """
        return PaginatedList(ChangeRecord, self._requester, 'GET', 'courses/{}/blueprint_templates/{}/migrations/{}/details'.format(self.course_id, self.template_id, self.id), kwargs=combine_kwargs(**kwargs))

    async def get_details_async(self, **kwargs) -> 'PaginatedList[ChangeRecord]':
        """
        Return the changes that were made in a blueprint migration.

        Endpoint: GET /api/v1/courses/:course_id/blueprint_templates/:template_id

        Reference: /migrations/:id/details        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.        master_courses/master_templates.migration_details
        """
        return PaginatedList(ChangeRecord, self._requester, 'GET', 'courses/{}/blueprint_templates/{}/migrations/{}/details'.format(self.course_id, self.template_id, self.id), kwargs=combine_kwargs(**kwargs))

    def get_import_details(self, **kwargs) -> 'PaginatedList[ChangeRecord]':
        """
        Return changes that were made to a course with a blueprint.

        Endpoint: GET /api/v1/courses/:course_id/blueprint_subscriptions/

        Reference: :subscription_id/migrations/:id/details        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.        master_courses/master_templates.import_details
        """
        return PaginatedList(ChangeRecord, self._requester, 'GET', 'courses/{}/blueprint_subscriptions/{}/migrations/{}/details'.format(self.course_id, self.subscription_id, self.id), kwargs=combine_kwargs(**kwargs))

    async def get_import_details_async(self, **kwargs) -> 'PaginatedList[ChangeRecord]':
        """
        Return changes that were made to a course with a blueprint.

        Endpoint: GET /api/v1/courses/:course_id/blueprint_subscriptions/

        Reference: :subscription_id/migrations/:id/details        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.        master_courses/master_templates.import_details
        """
        return PaginatedList(ChangeRecord, self._requester, 'GET', 'courses/{}/blueprint_subscriptions/{}/migrations/{}/details'.format(self.course_id, self.subscription_id, self.id), kwargs=combine_kwargs(**kwargs))

class ChangeRecord(ChangeRecordModel):

    def __str__(self):
        return '{} {}'.format(self.asset_id, self.asset_name)

class BlueprintSubscription(BlueprintSubscriptionModel):

    def __str__(self):
        return '{} {}'.format(self.id, self.template_id)

    def list_blueprint_imports(self, **kwargs) -> 'PaginatedList[BlueprintMigration]':
        """
        Return a list of migrations imported into a course associated with a blueprint.

        Endpoint: GET /api/v1/courses/:course_id/blueprint_subscriptions/:subscription_id/

        Reference: migrations        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.        master_courses/master_templates.imports_index
        """
        return PaginatedList(BlueprintMigration, self._requester, 'GET', 'courses/{}/blueprint_subscriptions/{}/migrations'.format(self.course_id, self.id), {'course_id': self.id}, kwargs=combine_kwargs(**kwargs))

    async def list_blueprint_imports_async(self, **kwargs) -> 'PaginatedList[BlueprintMigration]':
        """
        Return a list of migrations imported into a course associated with a blueprint.

        Endpoint: GET /api/v1/courses/:course_id/blueprint_subscriptions/:subscription_id/

        Reference: migrations        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.        master_courses/master_templates.imports_index
        """
        return PaginatedList(BlueprintMigration, self._requester, 'GET', 'courses/{}/blueprint_subscriptions/{}/migrations'.format(self.course_id, self.id), {'course_id': self.id}, kwargs=combine_kwargs(**kwargs))

    def show_blueprint_import(self, migration: 'int | BlueprintMigration', **kwargs) -> 'BlueprintMigration':
        """
        Return the status of an import into a course associated with a blueprint.

        Endpoint: GET /api/v1/courses/:course_id/blueprint_subscriptions/:subscription_id/

        Reference: migrations/:id        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.        master_courses/master_templates.imports_show

        Parameters:
            migration: int or :class:`canvasapi.blueprint.BlueprintMigration`
        """
        migration_id = obj_or_id(migration, 'migration', (BlueprintMigration,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/blueprint_subscriptions/{}/migrations/{}'.format(self.course_id, self.id, migration_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return BlueprintMigration(self._requester, response_json)

    async def show_blueprint_import_async(self, migration: 'int | BlueprintMigration', **kwargs) -> 'BlueprintMigration':
        """
        Return the status of an import into a course associated with a blueprint.

        Endpoint: GET /api/v1/courses/:course_id/blueprint_subscriptions/:subscription_id/

        Reference: migrations/:id        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.        master_courses/master_templates.imports_show

        Parameters:
            migration: int or :class:`canvasapi.blueprint.BlueprintMigration`
        """
        migration_id = obj_or_id(migration, 'migration', (BlueprintMigration,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/blueprint_subscriptions/{}/migrations/{}'.format(self.course_id, self.id, migration_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return BlueprintMigration(self._requester, response_json)