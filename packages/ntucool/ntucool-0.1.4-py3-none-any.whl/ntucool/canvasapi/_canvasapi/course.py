from ..models.late_policy import LatePolicy as LatePolicyModel
from ..models.users import CourseNickname as CourseNicknameModel
from ..models.courses import Course as CourseModel
import httpx
import typing
if typing.TYPE_CHECKING:
    from .usage_rights import UsageRights
    from .course_event import CourseEvent
    from .todo import Todo
    from .tab import Tab
    from .section import Section
    from .outcome_import import OutcomeImport
    from .submission import Submission
    from .license import License
    from .grading_period import GradingPeriod
    from .gradebook_history import SubmissionVersion, SubmissionHistory, Grader
    from .gradebook_history import Day
    from .grade_change_log import GradeChangeEvent
    from .file import File
    from .feature import FeatureFlag, Feature
    from .collaboration import Collaboration
    from .blueprint import BlueprintTemplate, BlueprintSubscription
    from .outcome import OutcomeLink, OutcomeGroup, OutcomeGroup
    from .content_export import ContentExport
    from .enrollment import Enrollment
    from .user import User
    from .rubric import Rubric, RubricAssociation
    from .quiz import QuizAssignmentOverrideSet, QuizExtension, Quiz
    from .page import Page
    from .new_quiz import NewQuiz
    from .module import Module
    from .group import GroupCategory
    from .folder import Folder
    from .external_tool import ExternalTool
    from .external_feed import ExternalFeed
    from .course_epub_export import CourseEpubExport
    from .discussion_topic import DiscussionTopic
    from .custom_gradebook_columns import CustomGradebookColumn
    from .content_migration import ContentMigration, Migrator
    from .paginated_list import PaginatedList
    from .assignment import Assignment, AssignmentOverride, AssignmentGroup
    from .progress import Progress
    from .grading_standard import GradingStandard
import warnings
from .assignment import Assignment, AssignmentGroup
from .blueprint import BlueprintSubscription
from .canvas_object import CanvasObject
from .collaboration import Collaboration
from .content_export import ContentExport
from .course_epub_export import CourseEpubExport
from .course_event import CourseEvent
from .custom_gradebook_columns import CustomGradebookColumn
from .discussion_topic import DiscussionTopic
from .exceptions import RequiredFieldMissing
from .external_feed import ExternalFeed
from .feature import Feature, FeatureFlag
from .folder import Folder
from .grade_change_log import GradeChangeEvent
from .gradebook_history import Day, Grader, SubmissionHistory, SubmissionVersion
from .grading_period import GradingPeriod
from .grading_standard import GradingStandard
from .license import License
from .module import Module
from .new_quiz import NewQuiz
from .outcome_import import OutcomeImport
from .page import Page
from .paginated_list import PaginatedList
from .progress import Progress
from .quiz import QuizExtension
from .rubric import Rubric, RubricAssociation
from .submission import GroupedSubmission, Submission
from .tab import Tab
from .todo import Todo
from .upload import FileOrPathLike, Uploader
from .usage_rights import UsageRights
from .util import combine_kwargs, file_or_path, is_multivalued, normalize_bool, obj_or_id, obj_or_str

class Course(CourseModel):

    def __str__(self):
        return '{} {} ({})'.format(self.course_code, self.name, self.id)

    def add_grading_standards(self, title: 'str', grading_scheme_entry: 'list[dict]', **kwargs) -> 'GradingStandard':
        """
        Create a new grading standard for the course.

        Endpoint: POST /api/v1/courses/:course_id/grading_standards

        Reference: https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.create

        Parameters:
            title: str
            grading_scheme_entry: list of dict
        """
        if not isinstance(grading_scheme_entry, list) or len(grading_scheme_entry) <= 0:
            raise ValueError('Param `grading_scheme_entry` must be a non-empty list.')
        for entry in grading_scheme_entry:
            if not isinstance(entry, dict):
                raise ValueError('grading_scheme_entry must consist of dictionaries.')
            if 'name' not in entry or 'value' not in entry:
                raise ValueError("Dictionaries with keys 'name' and 'value' are required.")
        kwargs['grading_scheme_entry'] = grading_scheme_entry
        response: 'httpx.Response' = self._requester.request('POST', 'courses/%s/grading_standards' % self.id, title=title, _kwargs=combine_kwargs(**kwargs))
        return GradingStandard(self._requester, response.json())

    async def add_grading_standards_async(self, title: 'str', grading_scheme_entry: 'list[dict]', **kwargs) -> 'GradingStandard':
        """
        Create a new grading standard for the course.

        Endpoint: POST /api/v1/courses/:course_id/grading_standards

        Reference: https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.create

        Parameters:
            title: str
            grading_scheme_entry: list of dict
        """
        if not isinstance(grading_scheme_entry, list) or len(grading_scheme_entry) <= 0:
            raise ValueError('Param `grading_scheme_entry` must be a non-empty list.')
        for entry in grading_scheme_entry:
            if not isinstance(entry, dict):
                raise ValueError('grading_scheme_entry must consist of dictionaries.')
            if 'name' not in entry or 'value' not in entry:
                raise ValueError("Dictionaries with keys 'name' and 'value' are required.")
        kwargs['grading_scheme_entry'] = grading_scheme_entry
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/%s/grading_standards' % self.id, title=title, _kwargs=combine_kwargs(**kwargs))
        return GradingStandard(self._requester, response.json())

    def column_data_bulk_update(self, column_data: 'list', **kwargs) -> 'Progress':
        """
        Set the content of custom columns.

        Endpoint: PUT /api/v1/courses/:course_id/custom_gradebook_column_data

        Reference: https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_column_data_api.bulk_update

        Parameters:
            column_data: list
        """
        kwargs['column_data'] = column_data
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/custom_gradebook_column_data'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Progress(self._requester, response.json())

    async def column_data_bulk_update_async(self, column_data: 'list', **kwargs) -> 'Progress':
        """
        Set the content of custom columns.

        Endpoint: PUT /api/v1/courses/:course_id/custom_gradebook_column_data

        Reference: https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_column_data_api.bulk_update

        Parameters:
            column_data: list
        """
        kwargs['column_data'] = column_data
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/custom_gradebook_column_data'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Progress(self._requester, response.json())

    def conclude(self, **kwargs) -> 'bool':
        """
        Mark this course as concluded.

        Endpoint: DELETE /api/v1/courses/:id

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.destroy
        """
        kwargs['event'] = 'conclude'
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('conclude')

    async def conclude_async(self, **kwargs) -> 'bool':
        """
        Mark this course as concluded.

        Endpoint: DELETE /api/v1/courses/:id

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.destroy
        """
        kwargs['event'] = 'conclude'
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('conclude')

    def create_assignment(self, assignment: 'dict', **kwargs) -> 'Assignment':
        """
        Create a new assignment for this course.
        
        Note: The assignment is created in the active state.

        Endpoint: POST /api/v1/courses/:course_id/assignments

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.create

        Parameters:
            assignment: dict
        """
        from .assignment import Assignment
        if isinstance(assignment, dict) and 'name' in assignment:
            kwargs['assignment'] = assignment
        else:
            raise RequiredFieldMissing("Dictionary with key 'name' is required.")
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/assignments'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Assignment(self._requester, response.json())

    async def create_assignment_async(self, assignment: 'dict', **kwargs) -> 'Assignment':
        """
        Create a new assignment for this course.
        
        Note: The assignment is created in the active state.

        Endpoint: POST /api/v1/courses/:course_id/assignments

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.create

        Parameters:
            assignment: dict
        """
        from .assignment import Assignment
        if isinstance(assignment, dict) and 'name' in assignment:
            kwargs['assignment'] = assignment
        else:
            raise RequiredFieldMissing("Dictionary with key 'name' is required.")
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/assignments'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Assignment(self._requester, response.json())

    def create_assignment_group(self, **kwargs) -> 'AssignmentGroup':
        """
        Create a new assignment group for this course.

        Endpoint: POST /api/v1/courses/:course_id/assignment_groups

        Reference: https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.create
        """
        from .assignment import AssignmentGroup
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/assignment_groups'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return AssignmentGroup(self._requester, response_json)

    async def create_assignment_group_async(self, **kwargs) -> 'AssignmentGroup':
        """
        Create a new assignment group for this course.

        Endpoint: POST /api/v1/courses/:course_id/assignment_groups

        Reference: https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.create
        """
        from .assignment import AssignmentGroup
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/assignment_groups'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return AssignmentGroup(self._requester, response_json)

    def create_assignment_overrides(self, assignment_overrides: 'list', **kwargs) -> 'PaginatedList[AssignmentOverride]':
        """
        Create the specified overrides for each assignment.

        Endpoint: POST /api/v1/courses/:course_id/assignments/overrides

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.batch_create

        Parameters:
            assignment_overrides: list
        """
        from .assignment import AssignmentOverride
        kwargs['assignment_overrides'] = assignment_overrides
        return PaginatedList(AssignmentOverride, self._requester, 'POST', 'courses/{}/assignments/overrides'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def create_assignment_overrides_async(self, assignment_overrides: 'list', **kwargs) -> 'PaginatedList[AssignmentOverride]':
        """
        Create the specified overrides for each assignment.

        Endpoint: POST /api/v1/courses/:course_id/assignments/overrides

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.batch_create

        Parameters:
            assignment_overrides: list
        """
        from .assignment import AssignmentOverride
        kwargs['assignment_overrides'] = assignment_overrides
        return PaginatedList(AssignmentOverride, self._requester, 'POST', 'courses/{}/assignments/overrides'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def create_content_migration(self, migration_type: 'str | Migrator', **kwargs) -> 'ContentMigration':
        """
        Create a content migration.

        Endpoint: POST /api/v1/courses/:course_id/content_migrations

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
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/content_migrations'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return ContentMigration(self._requester, response_json)

    async def create_content_migration_async(self, migration_type: 'str | Migrator', **kwargs) -> 'ContentMigration':
        """
        Create a content migration.

        Endpoint: POST /api/v1/courses/:course_id/content_migrations

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
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/content_migrations'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return ContentMigration(self._requester, response_json)

    def create_course_section(self, **kwargs) -> 'Section':
        """
        Create a new section for this course.

        Endpoint: POST /api/v1/courses/:course_id/sections

        Reference: https://canvas.instructure.com/doc/api/sections.html#method.sections.create
        """
        from .section import Section
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/sections'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Section(self._requester, response.json())

    async def create_course_section_async(self, **kwargs) -> 'Section':
        """
        Create a new section for this course.

        Endpoint: POST /api/v1/courses/:course_id/sections

        Reference: https://canvas.instructure.com/doc/api/sections.html#method.sections.create
        """
        from .section import Section
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/sections'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Section(self._requester, response.json())

    def create_custom_column(self, column: 'dict', **kwargs) -> 'CustomGradebookColumn':
        """
        Create a custom gradebook column.

        Endpoint: POST /api/v1/courses/:course_id/custom_gradebook_columns

        Reference: https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.create

        Parameters:
            column: dict
        """
        if isinstance(column, dict) and 'title' in column:
            kwargs['column'] = column
        else:
            raise RequiredFieldMissing("Dictionary with key 'title' is required.")
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/custom_gradebook_columns'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        column_json: 'dict' = response.json()
        column_json.update({'course_id': self.id})
        return CustomGradebookColumn(self._requester, column_json)

    async def create_custom_column_async(self, column: 'dict', **kwargs) -> 'CustomGradebookColumn':
        """
        Create a custom gradebook column.

        Endpoint: POST /api/v1/courses/:course_id/custom_gradebook_columns

        Reference: https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.create

        Parameters:
            column: dict
        """
        if isinstance(column, dict) and 'title' in column:
            kwargs['column'] = column
        else:
            raise RequiredFieldMissing("Dictionary with key 'title' is required.")
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/custom_gradebook_columns'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        column_json: 'dict' = response.json()
        column_json.update({'course_id': self.id})
        return CustomGradebookColumn(self._requester, column_json)

    def create_discussion_topic(self, attachment: 'str | None'=None, **kwargs) -> 'DiscussionTopic':
        """
        Creates a new discussion topic for the course or group.

        Endpoint: POST /api/v1/courses/:course_id/discussion_topics

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.create

        Parameters:
            attachment: file or str
        """
        if attachment is not None:
            attachment_file, is_path = file_or_path(attachment)
            attachment = {'attachment': attachment_file}
        try:
            response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/discussion_topics'.format(self.id), file=attachment, _kwargs=combine_kwargs(**kwargs))
            response_json: 'dict' = response.json()
            response_json.update({'course_id': self.id})
            return DiscussionTopic(self._requester, response_json)
        finally:
            if attachment is not None and is_path:
                attachment_file.close()

    async def create_discussion_topic_async(self, attachment: 'str | None'=None, **kwargs) -> 'DiscussionTopic':
        """
        Creates a new discussion topic for the course or group.

        Endpoint: POST /api/v1/courses/:course_id/discussion_topics

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.create

        Parameters:
            attachment: file or str
        """
        if attachment is not None:
            attachment_file, is_path = file_or_path(attachment)
            attachment = {'attachment': attachment_file}
        try:
            response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/discussion_topics'.format(self.id), file=attachment, _kwargs=combine_kwargs(**kwargs))
            response_json: 'dict' = response.json()
            response_json.update({'course_id': self.id})
            return DiscussionTopic(self._requester, response_json)
        finally:
            if attachment is not None and is_path:
                attachment_file.close()

    def create_epub_export(self, **kwargs) -> 'CourseEpubExport':
        """
        Create an ePub export for a course.

        Endpoint: POST /api/v1/courses/:course_id/epub_exports/:id

        Reference: https://canvas.instructure.com/doc/api/e_pub_exports.html#method.epub_exports.create
        """
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/epub_exports/'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return CourseEpubExport(self._requester, response.json())

    async def create_epub_export_async(self, **kwargs) -> 'CourseEpubExport':
        """
        Create an ePub export for a course.

        Endpoint: POST /api/v1/courses/:course_id/epub_exports/:id

        Reference: https://canvas.instructure.com/doc/api/e_pub_exports.html#method.epub_exports.create
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/epub_exports/'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return CourseEpubExport(self._requester, response.json())

    def create_external_feed(self, url: 'str', **kwargs) -> 'ExternalFeed':
        """
        Create a new external feed for the course.

        Endpoint: POST /api/v1/courses/:course_id/external_feeds

        Reference: https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.create

        Parameters:
            url: str
        """
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/external_feeds'.format(self.id), url=url, _kwargs=combine_kwargs(**kwargs))
        return ExternalFeed(self._requester, response.json())

    async def create_external_feed_async(self, url: 'str', **kwargs) -> 'ExternalFeed':
        """
        Create a new external feed for the course.

        Endpoint: POST /api/v1/courses/:course_id/external_feeds

        Reference: https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.create

        Parameters:
            url: str
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/external_feeds'.format(self.id), url=url, _kwargs=combine_kwargs(**kwargs))
        return ExternalFeed(self._requester, response.json())

    def create_external_tool(self, **kwargs) -> 'ExternalTool':
        """
        Create an external tool in the current course.

        Endpoint: POST /api/v1/courses/:course_id/external_tools

        Reference: https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.create
        """
        from .external_tool import ExternalTool
        required_params = ('name', 'privacy_level', 'consumer_key', 'shared_secret')
        if 'client_id' not in kwargs and (not all((x in kwargs for x in required_params))):
            raise RequiredFieldMissing('Must pass either `client_id` parameter or `name`, `privacy_level`, `consumer_key`, and `shared_secret` parameters.')
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/external_tools'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return ExternalTool(self._requester, response_json)

    async def create_external_tool_async(self, **kwargs) -> 'ExternalTool':
        """
        Create an external tool in the current course.

        Endpoint: POST /api/v1/courses/:course_id/external_tools

        Reference: https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.create
        """
        from .external_tool import ExternalTool
        required_params = ('name', 'privacy_level', 'consumer_key', 'shared_secret')
        if 'client_id' not in kwargs and (not all((x in kwargs for x in required_params))):
            raise RequiredFieldMissing('Must pass either `client_id` parameter or `name`, `privacy_level`, `consumer_key`, and `shared_secret` parameters.')
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/external_tools'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return ExternalTool(self._requester, response_json)

    def create_folder(self, name: 'str', **kwargs) -> 'Folder':
        """
        Creates a folder in this course.

        Endpoint: POST /api/v1/courses/:course_id/folders

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.create

        Parameters:
            name: str
        """
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/folders'.format(self.id), name=name, _kwargs=combine_kwargs(**kwargs))
        return Folder(self._requester, response.json())

    async def create_folder_async(self, name: 'str', **kwargs) -> 'Folder':
        """
        Creates a folder in this course.

        Endpoint: POST /api/v1/courses/:course_id/folders

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.create

        Parameters:
            name: str
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/folders'.format(self.id), name=name, _kwargs=combine_kwargs(**kwargs))
        return Folder(self._requester, response.json())

    def create_group_category(self, name: 'str', **kwargs) -> 'GroupCategory':
        """
        Create a group category.

        Endpoint: POST /api/v1/courses/:course_id/group_categories

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.create

        Parameters:
            name: str
        """
        from .group import GroupCategory
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/group_categories'.format(self.id), name=name, _kwargs=combine_kwargs(**kwargs))
        return GroupCategory(self._requester, response.json())

    async def create_group_category_async(self, name: 'str', **kwargs) -> 'GroupCategory':
        """
        Create a group category.

        Endpoint: POST /api/v1/courses/:course_id/group_categories

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.create

        Parameters:
            name: str
        """
        from .group import GroupCategory
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/group_categories'.format(self.id), name=name, _kwargs=combine_kwargs(**kwargs))
        return GroupCategory(self._requester, response.json())

    def create_late_policy(self, **kwargs) -> 'LatePolicy':
        """
        Create a late policy. If the course already has a late policy, a bad_request
        is returned since there can only be one late policy per course.

        Endpoint: POST /api/v1/courses/:id/late_policy

        Reference: https://canvas.instructure.com/doc/api/late_policy.html#method.late_policy.create
        """
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/late_policy'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        late_policy_json: 'dict' = response.json()
        return LatePolicy(self._requester, late_policy_json['late_policy'])

    async def create_late_policy_async(self, **kwargs) -> 'LatePolicy':
        """
        Create a late policy. If the course already has a late policy, a bad_request
        is returned since there can only be one late policy per course.

        Endpoint: POST /api/v1/courses/:id/late_policy

        Reference: https://canvas.instructure.com/doc/api/late_policy.html#method.late_policy.create
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/late_policy'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        late_policy_json: 'dict' = response.json()
        return LatePolicy(self._requester, late_policy_json['late_policy'])

    def create_module(self, module: 'dict', **kwargs) -> 'Module':
        """
        Create a new module.

        Endpoint: POST /api/v1/courses/:course_id/modules

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.create

        Parameters:
            module: dict
        """
        if isinstance(module, dict) and 'name' in module:
            kwargs['module'] = module
        else:
            raise RequiredFieldMissing("Dictionary with key 'name' is required.")
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/modules'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        module_json: 'dict' = response.json()
        module_json.update({'course_id': self.id})
        return Module(self._requester, module_json)

    async def create_module_async(self, module: 'dict', **kwargs) -> 'Module':
        """
        Create a new module.

        Endpoint: POST /api/v1/courses/:course_id/modules

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.create

        Parameters:
            module: dict
        """
        if isinstance(module, dict) and 'name' in module:
            kwargs['module'] = module
        else:
            raise RequiredFieldMissing("Dictionary with key 'name' is required.")
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/modules'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        module_json: 'dict' = response.json()
        module_json.update({'course_id': self.id})
        return Module(self._requester, module_json)

    def create_new_quiz(self, **kwargs) -> 'NewQuiz':
        """
        Create a new quiz for the course.

        Endpoint: POST /api/quiz/v1/courses/:course_id/quizzes

        Reference: https://canvas.instructure.com/doc/api/new_quizzes.html#method.new_quizzes/quizzes_api.create
        """
        endpoint = 'courses/{}/quizzes'.format(self.id)
        response: 'httpx.Response' = self._requester.request('POST', endpoint, _url='new_quizzes', _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return NewQuiz(self._requester, response_json)

    async def create_new_quiz_async(self, **kwargs) -> 'NewQuiz':
        """
        Create a new quiz for the course.

        Endpoint: POST /api/quiz/v1/courses/:course_id/quizzes

        Reference: https://canvas.instructure.com/doc/api/new_quizzes.html#method.new_quizzes/quizzes_api.create
        """
        endpoint = 'courses/{}/quizzes'.format(self.id)
        response: 'httpx.Response' = await self._requester.request_async('POST', endpoint, _url='new_quizzes', _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return NewQuiz(self._requester, response_json)

    def create_page(self, wiki_page: 'dict', **kwargs) -> 'Page':
        """
        Create a new wiki page.

        Endpoint: POST /api/v1/courses/:course_id/pages

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.create

        Parameters:
            wiki_page: dict
        """
        if isinstance(wiki_page, dict) and 'title' in wiki_page:
            kwargs['wiki_page'] = wiki_page
        else:
            raise RequiredFieldMissing("Dictionary with key 'title' is required.")
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/pages'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        page_json: 'dict' = response.json()
        page_json.update({'course_id': self.id})
        return Page(self._requester, page_json)

    async def create_page_async(self, wiki_page: 'dict', **kwargs) -> 'Page':
        """
        Create a new wiki page.

        Endpoint: POST /api/v1/courses/:course_id/pages

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.create

        Parameters:
            wiki_page: dict
        """
        if isinstance(wiki_page, dict) and 'title' in wiki_page:
            kwargs['wiki_page'] = wiki_page
        else:
            raise RequiredFieldMissing("Dictionary with key 'title' is required.")
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/pages'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        page_json: 'dict' = response.json()
        page_json.update({'course_id': self.id})
        return Page(self._requester, page_json)

    def create_quiz(self, quiz: 'dict', **kwargs) -> 'Quiz':
        """
        Create a new quiz in this course.

        Endpoint: POST /api/v1/courses/:course_id/quizzes

        Reference: https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.create

        Parameters:
            quiz: dict
        """
        from .quiz import Quiz
        if isinstance(quiz, dict) and 'title' in quiz:
            kwargs['quiz'] = quiz
        else:
            raise RequiredFieldMissing("Dictionary with key 'title' is required.")
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/quizzes'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        quiz_json: 'dict' = response.json()
        quiz_json.update({'course_id': self.id})
        return Quiz(self._requester, quiz_json)

    async def create_quiz_async(self, quiz: 'dict', **kwargs) -> 'Quiz':
        """
        Create a new quiz in this course.

        Endpoint: POST /api/v1/courses/:course_id/quizzes

        Reference: https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.create

        Parameters:
            quiz: dict
        """
        from .quiz import Quiz
        if isinstance(quiz, dict) and 'title' in quiz:
            kwargs['quiz'] = quiz
        else:
            raise RequiredFieldMissing("Dictionary with key 'title' is required.")
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/quizzes'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        quiz_json: 'dict' = response.json()
        quiz_json.update({'course_id': self.id})
        return Quiz(self._requester, quiz_json)

    def create_rubric(self, **kwargs) -> 'dict':
        """
        Create a new rubric.

        Endpoint: POST /api/v1/courses/:course_id/rubrics

        Reference: https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics.create
        """
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/rubrics'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        dictionary: 'dict' = response.json()
        rubric_dict = {}
        if 'rubric' in dictionary:
            r_dict = dictionary['rubric']
            r_dict.update({'course_id': self.id})
            rubric = Rubric(self._requester, r_dict)
            rubric_dict = {'rubric': rubric}
        if 'rubric_association' in dictionary:
            ra_dict = dictionary['rubric_association']
            rubric_association = RubricAssociation(self._requester, ra_dict)
            rubric_dict.update({'rubric_association': rubric_association})
        return rubric_dict

    async def create_rubric_async(self, **kwargs) -> 'dict':
        """
        Create a new rubric.

        Endpoint: POST /api/v1/courses/:course_id/rubrics

        Reference: https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics.create
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/rubrics'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        dictionary: 'dict' = response.json()
        rubric_dict = {}
        if 'rubric' in dictionary:
            r_dict = dictionary['rubric']
            r_dict.update({'course_id': self.id})
            rubric = Rubric(self._requester, r_dict)
            rubric_dict = {'rubric': rubric}
        if 'rubric_association' in dictionary:
            ra_dict = dictionary['rubric_association']
            rubric_association = RubricAssociation(self._requester, ra_dict)
            rubric_dict.update({'rubric_association': rubric_association})
        return rubric_dict

    def create_rubric_association(self, **kwargs) -> 'RubricAssociation':
        """
        Create a new RubricAssociation.

        Endpoint: POST /api/v1/courses/:course_id/rubric_associations

        Reference: https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_associations.create
        """
        from .rubric import RubricAssociation
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/rubric_associations'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        quiz_json: 'dict' = response.json()
        quiz_json.update({'course_id': self.id})
        return RubricAssociation(self._requester, quiz_json)

    async def create_rubric_association_async(self, **kwargs) -> 'RubricAssociation':
        """
        Create a new RubricAssociation.

        Endpoint: POST /api/v1/courses/:course_id/rubric_associations

        Reference: https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_associations.create
        """
        from .rubric import RubricAssociation
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/rubric_associations'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        quiz_json: 'dict' = response.json()
        quiz_json.update({'course_id': self.id})
        return RubricAssociation(self._requester, quiz_json)

    def delete(self, **kwargs) -> 'bool':
        """
        Permanently delete this course.

        Endpoint: DELETE /api/v1/courses/:id

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.destroy
        """
        kwargs['event'] = 'delete'
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('delete')

    async def delete_async(self, **kwargs) -> 'bool':
        """
        Permanently delete this course.

        Endpoint: DELETE /api/v1/courses/:id

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.destroy
        """
        kwargs['event'] = 'delete'
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('delete')

    def delete_external_feed(self, feed: 'ExternalFeed | int', **kwargs) -> 'ExternalFeed':
        """
        Deletes the external feed.

        Endpoint: DELETE /api/v1/courses/:course_id/external_feeds/:external_feed_id

        Reference: https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.destroy

        Parameters:
            feed: :class:`canvasapi.external_feed.ExternalFeed` or int
        """
        feed_id = obj_or_id(feed, 'feed', (ExternalFeed,))
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/external_feeds/{}'.format(self.id, feed_id), _kwargs=combine_kwargs(**kwargs))
        return ExternalFeed(self._requester, response.json())

    async def delete_external_feed_async(self, feed: 'ExternalFeed | int', **kwargs) -> 'ExternalFeed':
        """
        Deletes the external feed.

        Endpoint: DELETE /api/v1/courses/:course_id/external_feeds/:external_feed_id

        Reference: https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.destroy

        Parameters:
            feed: :class:`canvasapi.external_feed.ExternalFeed` or int
        """
        feed_id = obj_or_id(feed, 'feed', (ExternalFeed,))
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/external_feeds/{}'.format(self.id, feed_id), _kwargs=combine_kwargs(**kwargs))
        return ExternalFeed(self._requester, response.json())

    def edit_front_page(self, **kwargs) -> 'Course':
        """
        Update the title or contents of the front page.

        Endpoint: PUT /api/v1/courses/:course_id/front_page

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.update_front_page
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/front_page'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        page_json: 'dict' = response.json()
        page_json.update({'course_id': self.id})
        return Page(self._requester, page_json)

    async def edit_front_page_async(self, **kwargs) -> 'Course':
        """
        Update the title or contents of the front page.

        Endpoint: PUT /api/v1/courses/:course_id/front_page

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.update_front_page
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/front_page'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        page_json: 'dict' = response.json()
        page_json.update({'course_id': self.id})
        return Page(self._requester, page_json)

    def edit_late_policy(self, **kwargs) -> 'bool':
        """
        Patch a late policy. No body is returned upon success.

        Endpoint: PATCH /api/v1/courses/:id/late_policy

        Reference: https://canvas.instructure.com/doc/api/late_policy.html#method.late_policy.update
        """
        response: 'httpx.Response' = self._requester.request('PATCH', 'courses/{}/late_policy'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    async def edit_late_policy_async(self, **kwargs) -> 'bool':
        """
        Patch a late policy. No body is returned upon success.

        Endpoint: PATCH /api/v1/courses/:id/late_policy

        Reference: https://canvas.instructure.com/doc/api/late_policy.html#method.late_policy.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PATCH', 'courses/{}/late_policy'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    def enroll_user(self, user: 'User | int', enrollment_type: 'str | optional | None'=None, **kwargs) -> 'Enrollment':
        """
        Create a new user enrollment for a course or a section.

        Endpoint: POST /api/v1/courses/:course_id/enrollments

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.create

        Parameters:
            user: :class:`canvasapi.user.User` or int
            enrollment_type: str, optional
        """
        from .enrollment import Enrollment
        from .user import User
        kwargs['enrollment[user_id]'] = obj_or_id(user, 'user', (User,))
        if enrollment_type:
            warnings.warn("The `enrollment_type` argument is deprecated and will be removed in a future version.\nUse `enrollment[type]` as a keyword argument instead. e.g. `enroll_user(enrollment={'type': 'StudentEnrollment'})`", DeprecationWarning)
            kwargs['enrollment[type]'] = enrollment_type
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/enrollments'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Enrollment(self._requester, response.json())

    async def enroll_user_async(self, user: 'User | int', enrollment_type: 'str | optional | None'=None, **kwargs) -> 'Enrollment':
        """
        Create a new user enrollment for a course or a section.

        Endpoint: POST /api/v1/courses/:course_id/enrollments

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.create

        Parameters:
            user: :class:`canvasapi.user.User` or int
            enrollment_type: str, optional
        """
        from .enrollment import Enrollment
        from .user import User
        kwargs['enrollment[user_id]'] = obj_or_id(user, 'user', (User,))
        if enrollment_type:
            warnings.warn("The `enrollment_type` argument is deprecated and will be removed in a future version.\nUse `enrollment[type]` as a keyword argument instead. e.g. `enroll_user(enrollment={'type': 'StudentEnrollment'})`", DeprecationWarning)
            kwargs['enrollment[type]'] = enrollment_type
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/enrollments'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Enrollment(self._requester, response.json())

    def export_content(self, export_type: 'str', **kwargs) -> 'ContentExport':
        """
        Begin a content export job for a course.

        Endpoint: POST /api/v1/courses/:course_id/content_exports

        Reference: https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.create

        Parameters:
            export_type: str
        """
        kwargs['export_type'] = export_type
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/content_exports'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return ContentExport(self._requester, response.json())

    async def export_content_async(self, export_type: 'str', **kwargs) -> 'ContentExport':
        """
        Begin a content export job for a course.

        Endpoint: POST /api/v1/courses/:course_id/content_exports

        Reference: https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.create

        Parameters:
            export_type: str
        """
        kwargs['export_type'] = export_type
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/content_exports'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return ContentExport(self._requester, response.json())

    def get_all_outcome_links_in_context(self, **kwargs) -> 'PaginatedList[OutcomeLink]':
        """
        Get all outcome links for context - BETA

        Endpoint: GET /api/v1/courses/:course_id/outcome_group_links

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link_index
        """
        from .outcome import OutcomeLink
        return PaginatedList(OutcomeLink, self._requester, 'GET', 'courses/{}/outcome_group_links'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_all_outcome_links_in_context_async(self, **kwargs) -> 'PaginatedList[OutcomeLink]':
        """
        Get all outcome links for context - BETA

        Endpoint: GET /api/v1/courses/:course_id/outcome_group_links

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link_index
        """
        from .outcome import OutcomeLink
        return PaginatedList(OutcomeLink, self._requester, 'GET', 'courses/{}/outcome_group_links'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_assignment(self, assignment: 'Assignment | int', **kwargs) -> 'Assignment':
        """
        Return the assignment with the given ID.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:id

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.show

        Parameters:
            assignment: :class:`canvasapi.assignment.Assignment` or int
        """
        from .assignment import Assignment
        assignment_id = obj_or_id(assignment, 'assignment', (Assignment,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/assignments/{}'.format(self.id, assignment_id), _kwargs=combine_kwargs(**kwargs))
        return Assignment(self._requester, response.json())

    async def get_assignment_async(self, assignment: 'Assignment | int', **kwargs) -> 'Assignment':
        """
        Return the assignment with the given ID.

        Endpoint: GET /api/v1/courses/:course_id/assignments/:id

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.show

        Parameters:
            assignment: :class:`canvasapi.assignment.Assignment` or int
        """
        from .assignment import Assignment
        assignment_id = obj_or_id(assignment, 'assignment', (Assignment,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/assignments/{}'.format(self.id, assignment_id), _kwargs=combine_kwargs(**kwargs))
        return Assignment(self._requester, response.json())

    def get_assignment_group(self, assignment_group: 'AssignmentGroup | int', **kwargs) -> 'AssignmentGroup':
        """
        Retrieve specified assignment group for the specified course.

        Endpoint: GET /api/v1/courses/:course_id/assignment_groups/:assignment_group_id

        Reference: https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.show

        Parameters:
            assignment_group: :class:`canvasapi.assignment.AssignmentGroup` or int
        """
        from .assignment import AssignmentGroup
        assignment_group_id = obj_or_id(assignment_group, 'assignment_group', (AssignmentGroup,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/assignment_groups/{}'.format(self.id, assignment_group_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return AssignmentGroup(self._requester, response_json)

    async def get_assignment_group_async(self, assignment_group: 'AssignmentGroup | int', **kwargs) -> 'AssignmentGroup':
        """
        Retrieve specified assignment group for the specified course.

        Endpoint: GET /api/v1/courses/:course_id/assignment_groups/:assignment_group_id

        Reference: https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.show

        Parameters:
            assignment_group: :class:`canvasapi.assignment.AssignmentGroup` or int
        """
        from .assignment import AssignmentGroup
        assignment_group_id = obj_or_id(assignment_group, 'assignment_group', (AssignmentGroup,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/assignment_groups/{}'.format(self.id, assignment_group_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return AssignmentGroup(self._requester, response_json)

    def get_assignment_groups(self, **kwargs) -> 'PaginatedList[AssignmentGroup]':
        """
        List assignment groups for the specified course.

        Endpoint: GET /api/v1/courses/:course_id/assignment_groups

        Reference: https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups.index
        """
        from .assignment import AssignmentGroup
        return PaginatedList(AssignmentGroup, self._requester, 'GET', 'courses/{}/assignment_groups'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_assignment_groups_async(self, **kwargs) -> 'PaginatedList[AssignmentGroup]':
        """
        List assignment groups for the specified course.

        Endpoint: GET /api/v1/courses/:course_id/assignment_groups

        Reference: https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups.index
        """
        from .assignment import AssignmentGroup
        return PaginatedList(AssignmentGroup, self._requester, 'GET', 'courses/{}/assignment_groups'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_assignment_overrides(self, assignment_overrides, **kwargs) -> 'PaginatedList[AssignmentOverride]':
        """
        List the specified overrides in this course, providing they target
        sections/groups/students visible to the current user.

        Endpoint: GET /api/v1/courses/:course_id/assignments/overrides

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.batch_retrieve
        """
        from .assignment import AssignmentOverride
        kwargs['assignment_overrides'] = assignment_overrides
        return PaginatedList(AssignmentOverride, self._requester, 'GET', 'courses/{}/assignments/overrides'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_assignment_overrides_async(self, assignment_overrides, **kwargs) -> 'PaginatedList[AssignmentOverride]':
        """
        List the specified overrides in this course, providing they target
        sections/groups/students visible to the current user.

        Endpoint: GET /api/v1/courses/:course_id/assignments/overrides

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.batch_retrieve
        """
        from .assignment import AssignmentOverride
        kwargs['assignment_overrides'] = assignment_overrides
        return PaginatedList(AssignmentOverride, self._requester, 'GET', 'courses/{}/assignments/overrides'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_assignments(self, **kwargs) -> 'PaginatedList[Assignment]':
        """
        List all of the assignments in this course.

        Endpoint: GET /api/v1/courses/:course_id/assignments

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.index
        """
        from .assignment import Assignment
        return PaginatedList(Assignment, self._requester, 'GET', 'courses/{}/assignments'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_assignments_async(self, **kwargs) -> 'PaginatedList[Assignment]':
        """
        List all of the assignments in this course.

        Endpoint: GET /api/v1/courses/:course_id/assignments

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.index
        """
        from .assignment import Assignment
        return PaginatedList(Assignment, self._requester, 'GET', 'courses/{}/assignments'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_assignments_for_group(self, assignment_group: 'AssignmentGroup | int', **kwargs) -> 'PaginatedList[Assignment]':
        """
        Returns a paginated list of assignments for the given assignment group

        Endpoint: GET /api/v1/courses/:course_id/assignment_groups/:assignment_group_id/assignments

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.index

        Parameters:
            assignment_group: :class: `canvasapi.assignment.AssignmentGroup` or int
        """
        assignment_group_id = obj_or_id(assignment_group, 'assignment_group', (AssignmentGroup,))
        return PaginatedList(Assignment, self._requester, 'GET', 'courses/{}/assignment_groups/{}/assignments'.format(self.id, assignment_group_id), _kwargs=combine_kwargs(**kwargs))

    async def get_assignments_for_group_async(self, assignment_group: 'AssignmentGroup | int', **kwargs) -> 'PaginatedList[Assignment]':
        """
        Returns a paginated list of assignments for the given assignment group

        Endpoint: GET /api/v1/courses/:course_id/assignment_groups/:assignment_group_id/assignments

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.index

        Parameters:
            assignment_group: :class: `canvasapi.assignment.AssignmentGroup` or int
        """
        assignment_group_id = obj_or_id(assignment_group, 'assignment_group', (AssignmentGroup,))
        return PaginatedList(Assignment, self._requester, 'GET', 'courses/{}/assignment_groups/{}/assignments'.format(self.id, assignment_group_id), _kwargs=combine_kwargs(**kwargs))

    def get_blueprint(self, template: 'int | BlueprintTemplate'='default', **kwargs) -> 'BlueprintTemplate':
        """
        Return the blueprint of a given ID.

        Endpoint: GET /api/v1/courses/:course_id/blueprint_templates/:template_id

        Reference: https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses/master_templates.show

        Parameters:
            template: int or :class:`canvasapi.blueprint.BlueprintTemplate`
        """
        from .blueprint import BlueprintTemplate
        if template == 'default':
            template_id = template
        else:
            template_id = obj_or_id(template, 'template', (BlueprintTemplate,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/blueprint_templates/{}'.format(self.id, template_id), _kwargs=combine_kwargs(**kwargs))
        return BlueprintTemplate(self._requester, response.json())

    async def get_blueprint_async(self, template: 'int | BlueprintTemplate'='default', **kwargs) -> 'BlueprintTemplate':
        """
        Return the blueprint of a given ID.

        Endpoint: GET /api/v1/courses/:course_id/blueprint_templates/:template_id

        Reference: https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses/master_templates.show

        Parameters:
            template: int or :class:`canvasapi.blueprint.BlueprintTemplate`
        """
        from .blueprint import BlueprintTemplate
        if template == 'default':
            template_id = template
        else:
            template_id = obj_or_id(template, 'template', (BlueprintTemplate,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/blueprint_templates/{}'.format(self.id, template_id), _kwargs=combine_kwargs(**kwargs))
        return BlueprintTemplate(self._requester, response.json())

    def get_collaborations(self, **kwargs) -> 'Collaboration':
        """
        Return a list of collaborations for a given course ID.

        Endpoint: GET /api/v1/courses/:course_id/collaborations

        Reference: https://canvas.instructure.com/doc/api/collaborations.html#method.collaborations.api_index
        """
        return PaginatedList(Collaboration, self._requester, 'GET', 'courses/{}/collaborations'.format(self.id), _root='collaborations', kwargs=combine_kwargs(**kwargs))

    async def get_collaborations_async(self, **kwargs) -> 'Collaboration':
        """
        Return a list of collaborations for a given course ID.

        Endpoint: GET /api/v1/courses/:course_id/collaborations

        Reference: https://canvas.instructure.com/doc/api/collaborations.html#method.collaborations.api_index
        """
        return PaginatedList(Collaboration, self._requester, 'GET', 'courses/{}/collaborations'.format(self.id), _root='collaborations', kwargs=combine_kwargs(**kwargs))

    def get_content_export(self, content_export: 'int | ContentExport', **kwargs) -> 'ContentExport':
        """
        Return information about a single content export.

        Endpoint: GET /api/v1/courses/:course_id/content_exports/:id

        Reference: https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.show

        Parameters:
            content_export: int or :class:`canvasapi.content_export.ContentExport`
        """
        export_id = obj_or_id(content_export, 'content_export', (ContentExport,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/content_exports/{}'.format(self.id, export_id), _kwargs=combine_kwargs(**kwargs))
        return ContentExport(self._requester, response.json())

    async def get_content_export_async(self, content_export: 'int | ContentExport', **kwargs) -> 'ContentExport':
        """
        Return information about a single content export.

        Endpoint: GET /api/v1/courses/:course_id/content_exports/:id

        Reference: https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.show

        Parameters:
            content_export: int or :class:`canvasapi.content_export.ContentExport`
        """
        export_id = obj_or_id(content_export, 'content_export', (ContentExport,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/content_exports/{}'.format(self.id, export_id), _kwargs=combine_kwargs(**kwargs))
        return ContentExport(self._requester, response.json())

    def get_content_exports(self, **kwargs) -> 'PaginatedList[ContentExport]':
        """
        Return a paginated list of the past and pending content export jobs for a course.

        Endpoint: GET /api/v1/courses/:course_id/content_exports

        Reference: https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.index
        """
        return PaginatedList(ContentExport, self._requester, 'GET', 'courses/{}/content_exports'.format(self.id), kwargs=combine_kwargs(**kwargs))

    async def get_content_exports_async(self, **kwargs) -> 'PaginatedList[ContentExport]':
        """
        Return a paginated list of the past and pending content export jobs for a course.

        Endpoint: GET /api/v1/courses/:course_id/content_exports

        Reference: https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.index
        """
        return PaginatedList(ContentExport, self._requester, 'GET', 'courses/{}/content_exports'.format(self.id), kwargs=combine_kwargs(**kwargs))

    def get_content_migration(self, content_migration: 'int | str | ContentMigration', **kwargs) -> 'ContentMigration':
        """
        Retrive a content migration by its ID

        Endpoint: GET /api/v1/courses/:course_id/content_migrations/:id

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.show

        Parameters:
            content_migration: int, str or :class:`canvasapi.content_migration.ContentMigration`
        """
        from .content_migration import ContentMigration
        migration_id = obj_or_id(content_migration, 'content_migration', (ContentMigration,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/content_migrations/{}'.format(self.id, migration_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return ContentMigration(self._requester, response_json)

    async def get_content_migration_async(self, content_migration: 'int | str | ContentMigration', **kwargs) -> 'ContentMigration':
        """
        Retrive a content migration by its ID

        Endpoint: GET /api/v1/courses/:course_id/content_migrations/:id

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.show

        Parameters:
            content_migration: int, str or :class:`canvasapi.content_migration.ContentMigration`
        """
        from .content_migration import ContentMigration
        migration_id = obj_or_id(content_migration, 'content_migration', (ContentMigration,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/content_migrations/{}'.format(self.id, migration_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return ContentMigration(self._requester, response_json)

    def get_content_migrations(self, **kwargs) -> 'PaginatedList[ContentMigration]':
        """
        List content migrations that the current account can view or manage.

        Endpoint: GET /api/v1/courses/:course_id/content_migrations/

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.index
        """
        from .content_migration import ContentMigration
        return PaginatedList(ContentMigration, self._requester, 'GET', 'courses/{}/content_migrations'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_content_migrations_async(self, **kwargs) -> 'PaginatedList[ContentMigration]':
        """
        List content migrations that the current account can view or manage.

        Endpoint: GET /api/v1/courses/:course_id/content_migrations/

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.index
        """
        from .content_migration import ContentMigration
        return PaginatedList(ContentMigration, self._requester, 'GET', 'courses/{}/content_migrations'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_course_level_assignment_data(self, **kwargs) -> 'dict':
        """
        Return a list of assignments for the course sorted by due date

        Endpoint: GET /api/v1/courses/:course_id/analytics/assignments

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.course_assignments
        """
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/analytics/assignments'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_course_level_assignment_data_async(self, **kwargs) -> 'dict':
        """
        Return a list of assignments for the course sorted by due date

        Endpoint: GET /api/v1/courses/:course_id/analytics/assignments

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.course_assignments
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/analytics/assignments'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_course_level_participation_data(self, **kwargs) -> 'dict':
        """
        Return page view hits and participation numbers grouped by day through the course's history

        Endpoint: GET /api/v1/courses/:course_id/analytics/activity

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.course_participation
        """
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/analytics/activity'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_course_level_participation_data_async(self, **kwargs) -> 'dict':
        """
        Return page view hits and participation numbers grouped by day through the course's history

        Endpoint: GET /api/v1/courses/:course_id/analytics/activity

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.course_participation
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/analytics/activity'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_course_level_student_summary_data(self, **kwargs) -> 'PaginatedList[CourseStudentSummary]':
        """
        Return a summary of per-user access information for all students in a course

        Endpoint: GET /api/v1/courses/:course_id/analytics/student_summaries

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.course_student_summaries
        """
        return PaginatedList(CourseStudentSummary, self._requester, 'GET', 'courses/{}/analytics/student_summaries'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_course_level_student_summary_data_async(self, **kwargs) -> 'PaginatedList[CourseStudentSummary]':
        """
        Return a summary of per-user access information for all students in a course

        Endpoint: GET /api/v1/courses/:course_id/analytics/student_summaries

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.course_student_summaries
        """
        return PaginatedList(CourseStudentSummary, self._requester, 'GET', 'courses/{}/analytics/student_summaries'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_custom_columns(self, **kwargs) -> 'PaginatedList[CustomGradebookColumn]':
        """
        List of all the custom gradebook columns for a course.

        Endpoint: GET /api/v1/courses/:course_id/custom_gradebook_columns

        Reference: https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.index
        """
        return PaginatedList(CustomGradebookColumn, self._requester, 'GET', 'courses/{}/custom_gradebook_columns'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_custom_columns_async(self, **kwargs) -> 'PaginatedList[CustomGradebookColumn]':
        """
        List of all the custom gradebook columns for a course.

        Endpoint: GET /api/v1/courses/:course_id/custom_gradebook_columns

        Reference: https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.index
        """
        return PaginatedList(CustomGradebookColumn, self._requester, 'GET', 'courses/{}/custom_gradebook_columns'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_discussion_topic(self, topic: 'DiscussionTopic | int', **kwargs) -> 'DiscussionTopic':
        """
        Return data on an individual discussion topic.

        Endpoint: GET /api/v1/courses/:course_id/discussion_topics/:topic_id

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.show

        Parameters:
            topic: :class:`canvasapi.discussion_topic.DiscussionTopic` or int
        """
        topic_id = obj_or_id(topic, 'topic', (DiscussionTopic,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/discussion_topics/{}'.format(self.id, topic_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return DiscussionTopic(self._requester, response_json)

    async def get_discussion_topic_async(self, topic: 'DiscussionTopic | int', **kwargs) -> 'DiscussionTopic':
        """
        Return data on an individual discussion topic.

        Endpoint: GET /api/v1/courses/:course_id/discussion_topics/:topic_id

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.show

        Parameters:
            topic: :class:`canvasapi.discussion_topic.DiscussionTopic` or int
        """
        topic_id = obj_or_id(topic, 'topic', (DiscussionTopic,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/discussion_topics/{}'.format(self.id, topic_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return DiscussionTopic(self._requester, response_json)

    def get_discussion_topics(self, **kwargs) -> 'PaginatedList[DiscussionTopic]':
        """
        Returns the paginated list of discussion topics for this course or group.

        Endpoint: GET /api/v1/courses/:course_id/discussion_topics

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.index
        """
        return PaginatedList(DiscussionTopic, self._requester, 'GET', 'courses/{}/discussion_topics'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_discussion_topics_async(self, **kwargs) -> 'PaginatedList[DiscussionTopic]':
        """
        Returns the paginated list of discussion topics for this course or group.

        Endpoint: GET /api/v1/courses/:course_id/discussion_topics

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.index
        """
        return PaginatedList(DiscussionTopic, self._requester, 'GET', 'courses/{}/discussion_topics'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_enabled_features(self, **kwargs) -> 'list[str]':
        """
        Lists all enabled features in a course.

        Endpoint: GET /api/v1/courses/:course_id/features/enabled

        Reference: https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.enabled_features
        """
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/features/enabled'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_enabled_features_async(self, **kwargs) -> 'list[str]':
        """
        Lists all enabled features in a course.

        Endpoint: GET /api/v1/courses/:course_id/features/enabled

        Reference: https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.enabled_features
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/features/enabled'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_enrollments(self, **kwargs) -> 'PaginatedList[Enrollment]':
        """
        List all of the enrollments in this course.

        Endpoint: GET /api/v1/courses/:course_id/enrollments

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index
        """
        from .enrollment import Enrollment
        return PaginatedList(Enrollment, self._requester, 'GET', 'courses/{}/enrollments'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_enrollments_async(self, **kwargs) -> 'PaginatedList[Enrollment]':
        """
        List all of the enrollments in this course.

        Endpoint: GET /api/v1/courses/:course_id/enrollments

        Reference: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index
        """
        from .enrollment import Enrollment
        return PaginatedList(Enrollment, self._requester, 'GET', 'courses/{}/enrollments'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_epub_export(self, epub: 'int | CourseEpubExport', **kwargs) -> 'CourseEpubExport':
        """
        Get information about a single epub export.

        Endpoint: GET /api/v1/courses/:course_id/epub_exports/:id

        Reference: https://canvas.instructure.com/doc/api/e_pub_exports.html#method.epub_exports.show

        Parameters:
            epub: int or :class:`canvasapi.course_epub_export.CourseEpubExport`
        """
        epub_id = obj_or_id(epub, 'epub', (CourseEpubExport,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/epub_exports/{}'.format(self.id, epub_id), _kwargs=combine_kwargs(**kwargs))
        return CourseEpubExport(self._requester, response.json())

    async def get_epub_export_async(self, epub: 'int | CourseEpubExport', **kwargs) -> 'CourseEpubExport':
        """
        Get information about a single epub export.

        Endpoint: GET /api/v1/courses/:course_id/epub_exports/:id

        Reference: https://canvas.instructure.com/doc/api/e_pub_exports.html#method.epub_exports.show

        Parameters:
            epub: int or :class:`canvasapi.course_epub_export.CourseEpubExport`
        """
        epub_id = obj_or_id(epub, 'epub', (CourseEpubExport,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/epub_exports/{}'.format(self.id, epub_id), _kwargs=combine_kwargs(**kwargs))
        return CourseEpubExport(self._requester, response.json())

    def get_external_feeds(self, **kwargs) -> 'PaginatedList[ExternalFeed]':
        """
        Returns the list of External Feeds this course.

        Endpoint: GET /api/v1/courses/:course_id/external_feeds

        Reference: https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.index
        """
        return PaginatedList(ExternalFeed, self._requester, 'GET', 'courses/{}/external_feeds'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_external_feeds_async(self, **kwargs) -> 'PaginatedList[ExternalFeed]':
        """
        Returns the list of External Feeds this course.

        Endpoint: GET /api/v1/courses/:course_id/external_feeds

        Reference: https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.index
        """
        return PaginatedList(ExternalFeed, self._requester, 'GET', 'courses/{}/external_feeds'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_external_tool(self, tool: 'ExternalTool | int', **kwargs) -> 'ExternalTool':
        """
        

        Endpoint: GET /api/v1/courses/:course_id/external_tools/:external_tool_id

        Reference: https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.show

        Parameters:
            tool: :class:`canvasapi.external_tool.ExternalTool` or int
        """
        from .external_tool import ExternalTool
        tool_id = obj_or_id(tool, 'tool', (ExternalTool,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/external_tools/{}'.format(self.id, tool_id), _kwargs=combine_kwargs(**kwargs))
        tool_json: 'dict' = response.json()
        tool_json.update({'course_id': self.id})
        return ExternalTool(self._requester, tool_json)

    async def get_external_tool_async(self, tool: 'ExternalTool | int', **kwargs) -> 'ExternalTool':
        """
        

        Endpoint: GET /api/v1/courses/:course_id/external_tools/:external_tool_id

        Reference: https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.show

        Parameters:
            tool: :class:`canvasapi.external_tool.ExternalTool` or int
        """
        from .external_tool import ExternalTool
        tool_id = obj_or_id(tool, 'tool', (ExternalTool,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/external_tools/{}'.format(self.id, tool_id), _kwargs=combine_kwargs(**kwargs))
        tool_json: 'dict' = response.json()
        tool_json.update({'course_id': self.id})
        return ExternalTool(self._requester, tool_json)

    def get_external_tools(self, **kwargs) -> 'PaginatedList[ExternalTool]':
        """
        

        Endpoint: GET /api/v1/courses/:course_id/external_tools

        Reference: https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.index
        """
        from .external_tool import ExternalTool
        return PaginatedList(ExternalTool, self._requester, 'GET', 'courses/{}/external_tools'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_external_tools_async(self, **kwargs) -> 'PaginatedList[ExternalTool]':
        """
        

        Endpoint: GET /api/v1/courses/:course_id/external_tools

        Reference: https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.index
        """
        from .external_tool import ExternalTool
        return PaginatedList(ExternalTool, self._requester, 'GET', 'courses/{}/external_tools'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_feature_flag(self, feature: 'Feature | str', **kwargs) -> 'FeatureFlag':
        """
        Return the feature flag that applies to given course.

        Endpoint: GET /api/v1/courses/:course_id/features/flags/:feature

        Reference: https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.show

        Parameters:
            feature: :class:`canvasapi.feature.Feature` or str
        """
        feature_name = obj_or_str(feature, 'name', (Feature,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/features/flags/{}'.format(self.id, feature_name), _kwargs=combine_kwargs(**kwargs))
        return FeatureFlag(self._requester, response.json())

    async def get_feature_flag_async(self, feature: 'Feature | str', **kwargs) -> 'FeatureFlag':
        """
        Return the feature flag that applies to given course.

        Endpoint: GET /api/v1/courses/:course_id/features/flags/:feature

        Reference: https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.show

        Parameters:
            feature: :class:`canvasapi.feature.Feature` or str
        """
        feature_name = obj_or_str(feature, 'name', (Feature,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/features/flags/{}'.format(self.id, feature_name), _kwargs=combine_kwargs(**kwargs))
        return FeatureFlag(self._requester, response.json())

    def get_features(self, **kwargs) -> 'PaginatedList[Feature]':
        """
        Lists all features of a course.

        Endpoint: GET /api/v1/courses/:course_id/features

        Reference: https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.index
        """
        return PaginatedList(Feature, self._requester, 'GET', 'courses/{}/features'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_features_async(self, **kwargs) -> 'PaginatedList[Feature]':
        """
        Lists all features of a course.

        Endpoint: GET /api/v1/courses/:course_id/features

        Reference: https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.index
        """
        return PaginatedList(Feature, self._requester, 'GET', 'courses/{}/features'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_file(self, file: 'File | int', **kwargs) -> 'File':
        """
        Return the standard attachment json object for a file.

        Endpoint: GET /api/v1/courses/:course_id/files/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_show

        Parameters:
            file: :class:`canvasapi.file.File` or int
        """
        from .file import File
        file_id = obj_or_id(file, 'file', (File,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/files/{}'.format(self.id, file_id), _kwargs=combine_kwargs(**kwargs))
        return File(self._requester, response.json())

    async def get_file_async(self, file: 'File | int', **kwargs) -> 'File':
        """
        Return the standard attachment json object for a file.

        Endpoint: GET /api/v1/courses/:course_id/files/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_show

        Parameters:
            file: :class:`canvasapi.file.File` or int
        """
        from .file import File
        file_id = obj_or_id(file, 'file', (File,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/files/{}'.format(self.id, file_id), _kwargs=combine_kwargs(**kwargs))
        return File(self._requester, response.json())

    def get_file_quota(self, **kwargs) -> 'dict':
        """
        Returns the total and used storage quota for the course.

        Endpoint: GET /api/v1/courses/:course_id/files/quota

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_quota
        """
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/files/quota'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_file_quota_async(self, **kwargs) -> 'dict':
        """
        Returns the total and used storage quota for the course.

        Endpoint: GET /api/v1/courses/:course_id/files/quota

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_quota
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/files/quota'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_files(self, **kwargs) -> 'PaginatedList[File]':
        """
        Returns the paginated list of files for the course.

        Endpoint: GET /api/v1/courses/:course_id/files

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_index
        """
        from .file import File
        return PaginatedList(File, self._requester, 'GET', 'courses/{}/files'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_files_async(self, **kwargs) -> 'PaginatedList[File]':
        """
        Returns the paginated list of files for the course.

        Endpoint: GET /api/v1/courses/:course_id/files

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_index
        """
        from .file import File
        return PaginatedList(File, self._requester, 'GET', 'courses/{}/files'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_folder(self, folder: 'Folder | int', **kwargs) -> 'Folder':
        """
        Returns the details for a course folder

        Endpoint: GET /api/v1/courses/:course_id/folders/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.show

        Parameters:
            folder: :class:`canvasapi.folder.Folder` or int
        """
        folder_id = obj_or_id(folder, 'folder', (Folder,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/folders/{}'.format(self.id, folder_id), _kwargs=combine_kwargs(**kwargs))
        return Folder(self._requester, response.json())

    async def get_folder_async(self, folder: 'Folder | int', **kwargs) -> 'Folder':
        """
        Returns the details for a course folder

        Endpoint: GET /api/v1/courses/:course_id/folders/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.show

        Parameters:
            folder: :class:`canvasapi.folder.Folder` or int
        """
        folder_id = obj_or_id(folder, 'folder', (Folder,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/folders/{}'.format(self.id, folder_id), _kwargs=combine_kwargs(**kwargs))
        return Folder(self._requester, response.json())

    def get_folders(self, **kwargs) -> 'PaginatedList[Folder]':
        """
        Returns the paginated list of all folders for the given course. This will be returned as a
        flat list containing all subfolders as well.

        Endpoint: GET /api/v1/courses/:course_id/folders

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.list_all_folders
        """
        return PaginatedList(Folder, self._requester, 'GET', 'courses/{}/folders'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_folders_async(self, **kwargs) -> 'PaginatedList[Folder]':
        """
        Returns the paginated list of all folders for the given course. This will be returned as a
        flat list containing all subfolders as well.

        Endpoint: GET /api/v1/courses/:course_id/folders

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.list_all_folders
        """
        return PaginatedList(Folder, self._requester, 'GET', 'courses/{}/folders'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_full_discussion_topic(self, topic: 'DiscussionTopic | int', **kwargs) -> 'dict':
        """
        Return a cached structure of the discussion topic.

        Endpoint: GET /api/v1/courses/:course_id/discussion_topics/:topic_id/view

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.view

        Parameters:
            topic: :class:`canvasapi.discussion_topic.DiscussionTopic` or int
        """
        topic_id = obj_or_id(topic, 'topic', (DiscussionTopic,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/discussion_topics/{}/view'.format(self.id, topic_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_full_discussion_topic_async(self, topic: 'DiscussionTopic | int', **kwargs) -> 'dict':
        """
        Return a cached structure of the discussion topic.

        Endpoint: GET /api/v1/courses/:course_id/discussion_topics/:topic_id/view

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.view

        Parameters:
            topic: :class:`canvasapi.discussion_topic.DiscussionTopic` or int
        """
        topic_id = obj_or_id(topic, 'topic', (DiscussionTopic,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/discussion_topics/{}/view'.format(self.id, topic_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_grade_change_events(self, **kwargs) -> 'PaginatedList[GradeChangeEvent]':
        """
        Returns the grade change events for the course.

        Endpoint: GET /api/v1/audit/grade_change/courses/:course_id

        Reference: https://canvas.instructure.com/doc/api/grade_change_log.html#method.grade_change_audit_api.for_course
        """
        return PaginatedList(GradeChangeEvent, self._requester, 'GET', 'audit/grade_change/courses/{}'.format(self.id), _root='events', _kwargs=combine_kwargs(**kwargs))

    async def get_grade_change_events_async(self, **kwargs) -> 'PaginatedList[GradeChangeEvent]':
        """
        Returns the grade change events for the course.

        Endpoint: GET /api/v1/audit/grade_change/courses/:course_id

        Reference: https://canvas.instructure.com/doc/api/grade_change_log.html#method.grade_change_audit_api.for_course
        """
        return PaginatedList(GradeChangeEvent, self._requester, 'GET', 'audit/grade_change/courses/{}'.format(self.id), _root='events', _kwargs=combine_kwargs(**kwargs))

    def get_gradebook_history_dates(self, **kwargs) -> 'PaginatedList[Day]':
        """
        Returns a map of dates to grader/assignment groups

        Endpoint: GET /api/v1/courses/:course_id/gradebook_history/days

        Reference: https://canvas.instructure.com/doc/api/gradebook_history.html#method.gradebook_history_api.days
        """
        return PaginatedList(Day, self._requester, 'GET', 'courses/{}/gradebook_history/days'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_gradebook_history_dates_async(self, **kwargs) -> 'PaginatedList[Day]':
        """
        Returns a map of dates to grader/assignment groups

        Endpoint: GET /api/v1/courses/:course_id/gradebook_history/days

        Reference: https://canvas.instructure.com/doc/api/gradebook_history.html#method.gradebook_history_api.days
        """
        return PaginatedList(Day, self._requester, 'GET', 'courses/{}/gradebook_history/days'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_gradebook_history_details(self, date: 'int', **kwargs) -> 'PaginatedList[Grader]':
        """
        Returns the graders who worked on this day, along with the
        assignments they worked on. More details can be obtained by
        selecting a grader and assignment and calling the 'submissions'
        api endpoint for a given date.

        Endpoint: GET /api/v1/courses/:course_id/gradebook_history/:date

        Reference: https://canvas.instructure.com/doc/api/gradebook_history.html#method.        gradebook_history_api.day_details

        Parameters:
            date: int
        """
        return PaginatedList(Grader, self._requester, 'GET', 'courses/{}/gradebook_history/{}'.format(self.id, date), kwargs=combine_kwargs(**kwargs))

    async def get_gradebook_history_details_async(self, date: 'int', **kwargs) -> 'PaginatedList[Grader]':
        """
        Returns the graders who worked on this day, along with the
        assignments they worked on. More details can be obtained by
        selecting a grader and assignment and calling the 'submissions'
        api endpoint for a given date.

        Endpoint: GET /api/v1/courses/:course_id/gradebook_history/:date

        Reference: https://canvas.instructure.com/doc/api/gradebook_history.html#method.        gradebook_history_api.day_details

        Parameters:
            date: int
        """
        return PaginatedList(Grader, self._requester, 'GET', 'courses/{}/gradebook_history/{}'.format(self.id, date), kwargs=combine_kwargs(**kwargs))

    def get_grading_period(self, grading_period, **kwargs) -> 'GradingPeriod':
        """
        Return a single grading period for the associated course and id.

        Endpoint: GET /api/v1/courses/:course_id/grading_periods/:id

        Reference: https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.index
        """
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/grading_periods/{}'.format(self.id, grading_period), _kwargs=combine_kwargs(**kwargs))
        response_grading_period = response.json()['grading_periods'][0]
        response_grading_period.update({'course_id': self.id})
        return GradingPeriod(self._requester, response_grading_period)

    async def get_grading_period_async(self, grading_period, **kwargs) -> 'GradingPeriod':
        """
        Return a single grading period for the associated course and id.

        Endpoint: GET /api/v1/courses/:course_id/grading_periods/:id

        Reference: https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.index
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/grading_periods/{}'.format(self.id, grading_period), _kwargs=combine_kwargs(**kwargs))
        response_grading_period = response.json()['grading_periods'][0]
        response_grading_period.update({'course_id': self.id})
        return GradingPeriod(self._requester, response_grading_period)

    def get_grading_periods(self, **kwargs) -> 'PaginatedList[GradingPeriod]':
        """
        Return a list of grading periods for the associated course.

        Endpoint: GET /api/v1/courses/:course_id/grading_periods

        Reference: https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.index
        """
        return PaginatedList(GradingPeriod, self._requester, 'GET', 'courses/{}/grading_periods'.format(self.id), {'course_id': self.id}, _root='grading_periods', kwargs=combine_kwargs(**kwargs))

    async def get_grading_periods_async(self, **kwargs) -> 'PaginatedList[GradingPeriod]':
        """
        Return a list of grading periods for the associated course.

        Endpoint: GET /api/v1/courses/:course_id/grading_periods

        Reference: https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.index
        """
        return PaginatedList(GradingPeriod, self._requester, 'GET', 'courses/{}/grading_periods'.format(self.id), {'course_id': self.id}, _root='grading_periods', kwargs=combine_kwargs(**kwargs))

    def get_grading_standards(self, **kwargs) -> 'PaginatedList[GradingStandard]':
        """
        Get a PaginatedList of the grading standards available for the course

        Endpoint: GET /api/v1/courses/:course_id/grading_standards

        Reference: https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_index
        """
        return PaginatedList(GradingStandard, self._requester, 'GET', 'courses/%s/grading_standards' % self.id, _kwargs=combine_kwargs(**kwargs))

    async def get_grading_standards_async(self, **kwargs) -> 'PaginatedList[GradingStandard]':
        """
        Get a PaginatedList of the grading standards available for the course

        Endpoint: GET /api/v1/courses/:course_id/grading_standards

        Reference: https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_index
        """
        return PaginatedList(GradingStandard, self._requester, 'GET', 'courses/%s/grading_standards' % self.id, _kwargs=combine_kwargs(**kwargs))

    def get_group_categories(self, **kwargs) -> 'PaginatedList[GroupCategory]':
        """
        List group categories for a context.

        Endpoint: GET /api/v1/courses/:course_id/group_categories

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.index
        """
        from .group import GroupCategory
        return PaginatedList(GroupCategory, self._requester, 'GET', 'courses/{}/group_categories'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_group_categories_async(self, **kwargs) -> 'PaginatedList[GroupCategory]':
        """
        List group categories for a context.

        Endpoint: GET /api/v1/courses/:course_id/group_categories

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.index
        """
        from .group import GroupCategory
        return PaginatedList(GroupCategory, self._requester, 'GET', 'courses/{}/group_categories'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_groups(self, **kwargs) -> 'PaginatedList[Course]':
        """
        Return list of active groups for the specified course.

        Endpoint: GET /api/v1/courses/:course_id/groups

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.context_index
        """
        from .group import Group
        return PaginatedList(Group, self._requester, 'GET', 'courses/{}/groups'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_groups_async(self, **kwargs) -> 'PaginatedList[Course]':
        """
        Return list of active groups for the specified course.

        Endpoint: GET /api/v1/courses/:course_id/groups

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.context_index
        """
        from .group import Group
        return PaginatedList(Group, self._requester, 'GET', 'courses/{}/groups'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_late_policy(self, **kwargs) -> 'LatePolicy':
        """
        Returns the late policy for a course.

        Endpoint: GET /api/v1/courses/:id/late_policy

        Reference: https://canvas.instructure.com/doc/api/late_policy.html#method.late_policy.show
        """
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/late_policy'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        late_policy_json: 'dict' = response.json()
        return LatePolicy(self._requester, late_policy_json['late_policy'])

    async def get_late_policy_async(self, **kwargs) -> 'LatePolicy':
        """
        Returns the late policy for a course.

        Endpoint: GET /api/v1/courses/:id/late_policy

        Reference: https://canvas.instructure.com/doc/api/late_policy.html#method.late_policy.show
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/late_policy'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        late_policy_json: 'dict' = response.json()
        return LatePolicy(self._requester, late_policy_json['late_policy'])

    def get_licenses(self, **kwargs) -> 'PaginatedList[License]':
        """
        Returns a paginated list of the licenses that can be applied to the
        files under the course scope

        Endpoint: GET /api/v1/course/:course_id/content_licenses

        Reference: https://canvas.instructure.com/doc/api/files.html#method.usage_rights.licenses
        """
        return PaginatedList(License, self._requester, 'GET', 'courses/{}/content_licenses'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_licenses_async(self, **kwargs) -> 'PaginatedList[License]':
        """
        Returns a paginated list of the licenses that can be applied to the
        files under the course scope

        Endpoint: GET /api/v1/course/:course_id/content_licenses

        Reference: https://canvas.instructure.com/doc/api/files.html#method.usage_rights.licenses
        """
        return PaginatedList(License, self._requester, 'GET', 'courses/{}/content_licenses'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_migration_systems(self, **kwargs) -> 'PaginatedList[Migrator]':
        """
        Return a list of migration systems.

        Endpoint: GET /api/v1/courses/:course_id/content_migrations/migrators

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.available_migrators
        """
        from .content_migration import Migrator
        return PaginatedList(Migrator, self._requester, 'GET', 'courses/{}/content_migrations/migrators'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_migration_systems_async(self, **kwargs) -> 'PaginatedList[Migrator]':
        """
        Return a list of migration systems.

        Endpoint: GET /api/v1/courses/:course_id/content_migrations/migrators

        Reference: https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.available_migrators
        """
        from .content_migration import Migrator
        return PaginatedList(Migrator, self._requester, 'GET', 'courses/{}/content_migrations/migrators'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_module(self, module: 'Module | int', **kwargs) -> 'Module':
        """
        Retrieve a single module by ID.

        Endpoint: GET /api/v1/courses/:course_id/modules/:id

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.show

        Parameters:
            module: :class:`canvasapi.module.Module` or int
        """
        module_id = obj_or_id(module, 'module', (Module,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/modules/{}'.format(self.id, module_id), _kwargs=combine_kwargs(**kwargs))
        module_json: 'dict' = response.json()
        module_json.update({'course_id': self.id})
        return Module(self._requester, module_json)

    async def get_module_async(self, module: 'Module | int', **kwargs) -> 'Module':
        """
        Retrieve a single module by ID.

        Endpoint: GET /api/v1/courses/:course_id/modules/:id

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.show

        Parameters:
            module: :class:`canvasapi.module.Module` or int
        """
        module_id = obj_or_id(module, 'module', (Module,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/modules/{}'.format(self.id, module_id), _kwargs=combine_kwargs(**kwargs))
        module_json: 'dict' = response.json()
        module_json.update({'course_id': self.id})
        return Module(self._requester, module_json)

    def get_modules(self, **kwargs) -> 'PaginatedList[Module]':
        """
        Return a list of modules in this course.

        Endpoint: GET /api/v1/courses/:course_id/modules

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.index
        """
        return PaginatedList(Module, self._requester, 'GET', 'courses/{}/modules'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_modules_async(self, **kwargs) -> 'PaginatedList[Module]':
        """
        Return a list of modules in this course.

        Endpoint: GET /api/v1/courses/:course_id/modules

        Reference: https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.index
        """
        return PaginatedList(Module, self._requester, 'GET', 'courses/{}/modules'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_multiple_submissions(self, **kwargs) -> 'PaginatedList[Submission]':
        """
        List submissions for multiple assignments.
        Get all existing submissions for a given set of students and assignments.

        Endpoint: GET /api/v1/courses/:course_id/students/submissions

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.for_students
        """
        is_grouped = kwargs.get('grouped', False)
        if normalize_bool(is_grouped, 'grouped'):
            cls = GroupedSubmission
        else:
            cls = Submission
        return PaginatedList(cls, self._requester, 'GET', 'courses/{}/students/submissions'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_multiple_submissions_async(self, **kwargs) -> 'PaginatedList[Submission]':
        """
        List submissions for multiple assignments.
        Get all existing submissions for a given set of students and assignments.

        Endpoint: GET /api/v1/courses/:course_id/students/submissions

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.for_students
        """
        is_grouped = kwargs.get('grouped', False)
        if normalize_bool(is_grouped, 'grouped'):
            cls = GroupedSubmission
        else:
            cls = Submission
        return PaginatedList(cls, self._requester, 'GET', 'courses/{}/students/submissions'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_new_quiz(self, assignment: 'Assignment | NewQuiz | int', **kwargs) -> 'NewQuiz':
        """
        Get details about a single new quiz.

        Endpoint: GET /api/quiz/v1/courses/:course_id/quizzes/:assignment_id

        Reference: https://canvas.instructure.com/doc/api/new_quizzes.html#method.new_quizzes/quizzes_api.show

        Parameters:
            assignment: :class:`canvasapi.assignment.Assignment`
or :class:`canvasapi.new_quiz.NewQuiz` or int
        """
        assignment_id = obj_or_id(assignment, 'assignment', (Assignment, NewQuiz))
        endpoint = 'courses/{}/quizzes/{}'.format(self.id, assignment_id)
        response: 'httpx.Response' = self._requester.request('GET', endpoint, _url='new_quizzes', _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return NewQuiz(self._requester, response_json)

    async def get_new_quiz_async(self, assignment: 'Assignment | NewQuiz | int', **kwargs) -> 'NewQuiz':
        """
        Get details about a single new quiz.

        Endpoint: GET /api/quiz/v1/courses/:course_id/quizzes/:assignment_id

        Reference: https://canvas.instructure.com/doc/api/new_quizzes.html#method.new_quizzes/quizzes_api.show

        Parameters:
            assignment: :class:`canvasapi.assignment.Assignment`
or :class:`canvasapi.new_quiz.NewQuiz` or int
        """
        assignment_id = obj_or_id(assignment, 'assignment', (Assignment, NewQuiz))
        endpoint = 'courses/{}/quizzes/{}'.format(self.id, assignment_id)
        response: 'httpx.Response' = await self._requester.request_async('GET', endpoint, _url='new_quizzes', _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return NewQuiz(self._requester, response_json)

    def get_new_quizzes(self, **kwargs) -> 'PaginatedList[NewQuiz]':
        """
        Get a list of new quizzes.

        Endpoint: GET /api/quiz/v1/courses/:course_id/quizzes

        Reference: https://canvas.instructure.com/doc/api/new_quizzes.html#method.new_quizzes/quizzes_api.index
        """
        endpoint = 'courses/{}/quizzes'.format(self.id)
        return PaginatedList(NewQuiz, self._requester, 'GET', endpoint, _url_override='new_quizzes', _kwargs=combine_kwargs(**kwargs))

    async def get_new_quizzes_async(self, **kwargs) -> 'PaginatedList[NewQuiz]':
        """
        Get a list of new quizzes.

        Endpoint: GET /api/quiz/v1/courses/:course_id/quizzes

        Reference: https://canvas.instructure.com/doc/api/new_quizzes.html#method.new_quizzes/quizzes_api.index
        """
        endpoint = 'courses/{}/quizzes'.format(self.id)
        return PaginatedList(NewQuiz, self._requester, 'GET', endpoint, _url_override='new_quizzes', _kwargs=combine_kwargs(**kwargs))

    def get_outcome_group(self, group: 'OutcomeGroup | int', **kwargs) -> 'OutcomeGroup':
        """
        Returns the details of the Outcome Group with the given id.

        Endpoint: GET /api/v1/courses/:course_id/outcome_groups/:id

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show

        Parameters:
            group: :class:`canvasapi.outcome.OutcomeGroup` or int
        """
        from .outcome import OutcomeGroup
        outcome_group_id = obj_or_id(group, 'group', (OutcomeGroup,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/outcome_groups/{}'.format(self.id, outcome_group_id), _kwargs=combine_kwargs(**kwargs))
        return OutcomeGroup(self._requester, response.json())

    async def get_outcome_group_async(self, group: 'OutcomeGroup | int', **kwargs) -> 'OutcomeGroup':
        """
        Returns the details of the Outcome Group with the given id.

        Endpoint: GET /api/v1/courses/:course_id/outcome_groups/:id

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show

        Parameters:
            group: :class:`canvasapi.outcome.OutcomeGroup` or int
        """
        from .outcome import OutcomeGroup
        outcome_group_id = obj_or_id(group, 'group', (OutcomeGroup,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/outcome_groups/{}'.format(self.id, outcome_group_id), _kwargs=combine_kwargs(**kwargs))
        return OutcomeGroup(self._requester, response.json())

    def get_outcome_groups_in_context(self, **kwargs) -> 'PaginatedList[OutcomeGroups]':
        """
        Get all outcome groups for context - BETA

        Endpoint: GET /api/v1/courses/:course_id/outcome_groups

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.index
        """
        from .outcome import OutcomeGroup
        return PaginatedList(OutcomeGroup, self._requester, 'GET', 'courses/{}/outcome_groups'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_outcome_groups_in_context_async(self, **kwargs) -> 'PaginatedList[OutcomeGroups]':
        """
        Get all outcome groups for context - BETA

        Endpoint: GET /api/v1/courses/:course_id/outcome_groups

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.index
        """
        from .outcome import OutcomeGroup
        return PaginatedList(OutcomeGroup, self._requester, 'GET', 'courses/{}/outcome_groups'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_outcome_import_status(self, outcome_import: 'OutcomeImport | int | Literal["latest"]', **kwargs) -> 'OutcomeImport':
        """
        Get the status of an already created Outcome import.
        Pass 'latest' for the outcome import id for the latest import.

        Endpoint: GET /api/v1/courses/:course_id/outcome_imports/:id

        Reference: https://canvas.instructure.com/doc/api/outcome_imports.html#method.outcome_imports_api.show

        Parameters:
            outcome_import: :class:`canvasapi.outcome_import.OutcomeImport`,
int, or string: "latest"
        """
        if outcome_import == 'latest':
            outcome_import_id = 'latest'
        else:
            outcome_import_id = obj_or_id(outcome_import, 'outcome_import', (OutcomeImport,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/outcome_imports/{}'.format(self.id, outcome_import_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return OutcomeImport(self._requester, response_json)

    async def get_outcome_import_status_async(self, outcome_import: 'OutcomeImport | int | Literal["latest"]', **kwargs) -> 'OutcomeImport':
        """
        Get the status of an already created Outcome import.
        Pass 'latest' for the outcome import id for the latest import.

        Endpoint: GET /api/v1/courses/:course_id/outcome_imports/:id

        Reference: https://canvas.instructure.com/doc/api/outcome_imports.html#method.outcome_imports_api.show

        Parameters:
            outcome_import: :class:`canvasapi.outcome_import.OutcomeImport`,
int, or string: "latest"
        """
        if outcome_import == 'latest':
            outcome_import_id = 'latest'
        else:
            outcome_import_id = obj_or_id(outcome_import, 'outcome_import', (OutcomeImport,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/outcome_imports/{}'.format(self.id, outcome_import_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return OutcomeImport(self._requester, response_json)

    def get_outcome_result_rollups(self, **kwargs) -> 'dict':
        """
        Get all outcome result rollups for context - BETA

        Endpoint: GET /api/v1/courses/:course_id/outcome_rollups

        Reference: https://canvas.instructure.com/doc/api/outcome_results.html#method.outcome_results.rollups
        """
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/outcome_rollups'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_outcome_result_rollups_async(self, **kwargs) -> 'dict':
        """
        Get all outcome result rollups for context - BETA

        Endpoint: GET /api/v1/courses/:course_id/outcome_rollups

        Reference: https://canvas.instructure.com/doc/api/outcome_results.html#method.outcome_results.rollups
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/outcome_rollups'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_outcome_results(self, **kwargs):
        """
        Get all outcome results for context - BETA

        Endpoint: GET /api/v1/courses/:course_id/outcome_results

        Reference: https://canvas.instructure.com/doc/api/outcome_results.html#method.outcome_results.index
        """
        from .outcome import OutcomeResult
        return PaginatedList(OutcomeResult, self._requester, 'GET', 'courses/{}/outcome_results'.format(self.id), _root='outcome_results', _kwargs=combine_kwargs(**kwargs))

    async def get_outcome_results_async(self, **kwargs):
        """
        Get all outcome results for context - BETA

        Endpoint: GET /api/v1/courses/:course_id/outcome_results

        Reference: https://canvas.instructure.com/doc/api/outcome_results.html#method.outcome_results.index
        """
        from .outcome import OutcomeResult
        return PaginatedList(OutcomeResult, self._requester, 'GET', 'courses/{}/outcome_results'.format(self.id), _root='outcome_results', _kwargs=combine_kwargs(**kwargs))

    def get_page(self, url: 'str', **kwargs) -> 'Page':
        """
        Retrieve the contents of a wiki page.

        Endpoint: GET /api/v1/courses/:course_id/pages/:url

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show

        Parameters:
            url: str
        """
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/pages/{}'.format(self.id, url), _kwargs=combine_kwargs(**kwargs))
        page_json: 'dict' = response.json()
        page_json.update({'course_id': self.id})
        return Page(self._requester, page_json)

    async def get_page_async(self, url: 'str', **kwargs) -> 'Page':
        """
        Retrieve the contents of a wiki page.

        Endpoint: GET /api/v1/courses/:course_id/pages/:url

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show

        Parameters:
            url: str
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/pages/{}'.format(self.id, url), _kwargs=combine_kwargs(**kwargs))
        page_json: 'dict' = response.json()
        page_json.update({'course_id': self.id})
        return Page(self._requester, page_json)

    def get_pages(self, **kwargs) -> 'PaginatedList[Page]':
        """
        List the wiki pages associated with a course.

        Endpoint: GET /api/v1/courses/:course_id/pages

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.index
        """
        return PaginatedList(Page, self._requester, 'GET', 'courses/{}/pages'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_pages_async(self, **kwargs) -> 'PaginatedList[Page]':
        """
        List the wiki pages associated with a course.

        Endpoint: GET /api/v1/courses/:course_id/pages

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.index
        """
        return PaginatedList(Page, self._requester, 'GET', 'courses/{}/pages'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_quiz(self, quiz: 'Quiz | int', **kwargs) -> 'Quiz':
        """
        Return the quiz with the given id.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:id

        Reference: https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.show

        Parameters:
            quiz: :class:`canvasapi.quiz.Quiz` or int
        """
        from .quiz import Quiz
        quiz_id = obj_or_id(quiz, 'quiz', (Quiz,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/quizzes/{}'.format(self.id, quiz_id), _kwargs=combine_kwargs(**kwargs))
        quiz_json: 'dict' = response.json()
        quiz_json.update({'course_id': self.id})
        return Quiz(self._requester, quiz_json)

    async def get_quiz_async(self, quiz: 'Quiz | int', **kwargs) -> 'Quiz':
        """
        Return the quiz with the given id.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:id

        Reference: https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.show

        Parameters:
            quiz: :class:`canvasapi.quiz.Quiz` or int
        """
        from .quiz import Quiz
        quiz_id = obj_or_id(quiz, 'quiz', (Quiz,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/quizzes/{}'.format(self.id, quiz_id), _kwargs=combine_kwargs(**kwargs))
        quiz_json: 'dict' = response.json()
        quiz_json.update({'course_id': self.id})
        return Quiz(self._requester, quiz_json)

    def get_quiz_overrides(self, **kwargs) -> 'PaginatedList[QuizAssignmentOverrideSet]':
        """
        Retrieve the actual due-at, unlock-at,
        and available-at dates for quizzes based on
        the assignment overrides active for the current API user.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/assignment_overrides

        Reference: https://canvas.instructure.com/doc/api/quiz_assignment_overrides.html#method.quizzes/quiz_assignment_overrides.index
        """
        from .quiz import QuizAssignmentOverrideSet
        return PaginatedList(QuizAssignmentOverrideSet, self._requester, 'GET', 'courses/{}/quizzes/assignment_overrides'.format(self.id), _root='quiz_assignment_overrides', _kwargs=combine_kwargs(**kwargs))

    async def get_quiz_overrides_async(self, **kwargs) -> 'PaginatedList[QuizAssignmentOverrideSet]':
        """
        Retrieve the actual due-at, unlock-at,
        and available-at dates for quizzes based on
        the assignment overrides active for the current API user.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/assignment_overrides

        Reference: https://canvas.instructure.com/doc/api/quiz_assignment_overrides.html#method.quizzes/quiz_assignment_overrides.index
        """
        from .quiz import QuizAssignmentOverrideSet
        return PaginatedList(QuizAssignmentOverrideSet, self._requester, 'GET', 'courses/{}/quizzes/assignment_overrides'.format(self.id), _root='quiz_assignment_overrides', _kwargs=combine_kwargs(**kwargs))

    def get_quizzes(self, **kwargs) -> 'PaginatedList[Quiz]':
        """
        Return a list of quizzes belonging to this course.

        Endpoint: GET /api/v1/courses/:course_id/quizzes

        Reference: https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.index
        """
        from .quiz import Quiz
        return PaginatedList(Quiz, self._requester, 'GET', 'courses/{}/quizzes'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_quizzes_async(self, **kwargs) -> 'PaginatedList[Quiz]':
        """
        Return a list of quizzes belonging to this course.

        Endpoint: GET /api/v1/courses/:course_id/quizzes

        Reference: https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.index
        """
        from .quiz import Quiz
        return PaginatedList(Quiz, self._requester, 'GET', 'courses/{}/quizzes'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_recent_students(self, **kwargs) -> 'PaginatedList[User]':
        """
        Return a list of students in the course ordered by how recently they
        have logged in.

        Endpoint: GET /api/v1/courses/:course_id/recent_students

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.recent_students
        """
        from .user import User
        return PaginatedList(User, self._requester, 'GET', 'courses/{}/recent_students'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_recent_students_async(self, **kwargs) -> 'PaginatedList[User]':
        """
        Return a list of students in the course ordered by how recently they
        have logged in.

        Endpoint: GET /api/v1/courses/:course_id/recent_students

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.recent_students
        """
        from .user import User
        return PaginatedList(User, self._requester, 'GET', 'courses/{}/recent_students'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_root_outcome_group(self, **kwargs) -> 'OutcomeGroup':
        """
        Redirect to root outcome group for context

        Endpoint: GET /api/v1/courses/:course_id/root_outcome_group

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.redirect
        """
        from .outcome import OutcomeGroup
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/root_outcome_group'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return OutcomeGroup(self._requester, response.json())

    async def get_root_outcome_group_async(self, **kwargs) -> 'OutcomeGroup':
        """
        Redirect to root outcome group for context

        Endpoint: GET /api/v1/courses/:course_id/root_outcome_group

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.redirect
        """
        from .outcome import OutcomeGroup
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/root_outcome_group'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return OutcomeGroup(self._requester, response.json())

    def get_rubric(self, rubric_id: 'int', **kwargs) -> 'Rubric':
        """
        Get a single rubric, based on rubric id.

        Endpoint: GET /api/v1/courses/:course_id/rubrics/:id

        Reference: https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.show

        Parameters:
            rubric_id: int
        """
        response: 'httpx.Response' = self._requester.request('GET', 'courses/%s/rubrics/%s' % (self.id, rubric_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return Rubric(self._requester, response_json)

    async def get_rubric_async(self, rubric_id: 'int', **kwargs) -> 'Rubric':
        """
        Get a single rubric, based on rubric id.

        Endpoint: GET /api/v1/courses/:course_id/rubrics/:id

        Reference: https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.show

        Parameters:
            rubric_id: int
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/%s/rubrics/%s' % (self.id, rubric_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.id})
        return Rubric(self._requester, response_json)

    def get_rubrics(self, **kwargs) -> 'PaginatedList[Rubric]':
        """
        Get the paginated list of active rubrics for the current course.

        Endpoint: GET /api/v1/courses/:course_id/rubrics

        Reference: https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.index
        """
        return PaginatedList(Rubric, self._requester, 'GET', 'courses/%s/rubrics' % self.id, {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_rubrics_async(self, **kwargs) -> 'PaginatedList[Rubric]':
        """
        Get the paginated list of active rubrics for the current course.

        Endpoint: GET /api/v1/courses/:course_id/rubrics

        Reference: https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.index
        """
        return PaginatedList(Rubric, self._requester, 'GET', 'courses/%s/rubrics' % self.id, {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_section(self, section: 'Section | int', **kwargs) -> 'Section':
        """
        Retrieve a section.

        Endpoint: GET /api/v1/courses/:course_id/sections/:id

        Reference: https://canvas.instructure.com/doc/api/sections.html#method.sections.show

        Parameters:
            section: :class:`canvasapi.section.Section` or int
        """
        from .section import Section
        section_id = obj_or_id(section, 'section', (Section,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/sections/{}'.format(self.id, section_id), _kwargs=combine_kwargs(**kwargs))
        return Section(self._requester, response.json())

    async def get_section_async(self, section: 'Section | int', **kwargs) -> 'Section':
        """
        Retrieve a section.

        Endpoint: GET /api/v1/courses/:course_id/sections/:id

        Reference: https://canvas.instructure.com/doc/api/sections.html#method.sections.show

        Parameters:
            section: :class:`canvasapi.section.Section` or int
        """
        from .section import Section
        section_id = obj_or_id(section, 'section', (Section,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/sections/{}'.format(self.id, section_id), _kwargs=combine_kwargs(**kwargs))
        return Section(self._requester, response.json())

    def get_sections(self, **kwargs) -> 'PaginatedList[Section]':
        """
        List all sections in a course.

        Endpoint: GET /api/v1/courses/:course_id/sections

        Reference: https://canvas.instructure.com/doc/api/sections.html#method.sections.index
        """
        from .section import Section
        return PaginatedList(Section, self._requester, 'GET', 'courses/{}/sections'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_sections_async(self, **kwargs) -> 'PaginatedList[Section]':
        """
        List all sections in a course.

        Endpoint: GET /api/v1/courses/:course_id/sections

        Reference: https://canvas.instructure.com/doc/api/sections.html#method.sections.index
        """
        from .section import Section
        return PaginatedList(Section, self._requester, 'GET', 'courses/{}/sections'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_settings(self, **kwargs) -> 'dict':
        """
        Returns this course's settings.

        Endpoint: GET /api/v1/courses/:course_id/settings

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.settings
        """
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/settings'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_settings_async(self, **kwargs) -> 'dict':
        """
        Returns this course's settings.

        Endpoint: GET /api/v1/courses/:course_id/settings

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.settings
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/settings'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_single_grading_standard(self, grading_standard_id: 'int', **kwargs) -> 'GradingStandard':
        """
        Get a single grading standard from the course.

        Endpoint: GET /api/v1/courses/:course_id/grading_standards/:grading_standard_id

        Reference: https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_show

        Parameters:
            grading_standard_id: int
        """
        response: 'httpx.Response' = self._requester.request('GET', 'courses/%s/grading_standards/%d' % (self.id, grading_standard_id), _kwargs=combine_kwargs(**kwargs))
        return GradingStandard(self._requester, response.json())

    async def get_single_grading_standard_async(self, grading_standard_id: 'int', **kwargs) -> 'GradingStandard':
        """
        Get a single grading standard from the course.

        Endpoint: GET /api/v1/courses/:course_id/grading_standards/:grading_standard_id

        Reference: https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_show

        Parameters:
            grading_standard_id: int
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/%s/grading_standards/%d' % (self.id, grading_standard_id), _kwargs=combine_kwargs(**kwargs))
        return GradingStandard(self._requester, response.json())

    def get_submission_history(self, date, grader_id: 'int', assignment_id: 'int', **kwargs) -> 'PaginatedList[SubmissionHistory]':
        """
        Gives a nested list of submission versions.

        Endpoint: GET /api/v1/courses/:course_id/gradebook_history/:date/graders

        Reference: /:grader_id/assignments/:assignment_id/submissions        <https://canvas.instructure.com/doc/api/gradebook_history.html#method.        gradebook_history_api.submissions

        Parameters:
            grader_id: int
            assignment_id: int
        """
        return PaginatedList(SubmissionHistory, self._requester, 'GET', 'courses/{}/gradebook_history/{}/graders/{}/assignments/{}/submissions'.format(self.id, date, grader_id, assignment_id), kwargs=combine_kwargs(**kwargs))

    async def get_submission_history_async(self, date, grader_id: 'int', assignment_id: 'int', **kwargs) -> 'PaginatedList[SubmissionHistory]':
        """
        Gives a nested list of submission versions.

        Endpoint: GET /api/v1/courses/:course_id/gradebook_history/:date/graders

        Reference: /:grader_id/assignments/:assignment_id/submissions        <https://canvas.instructure.com/doc/api/gradebook_history.html#method.        gradebook_history_api.submissions

        Parameters:
            grader_id: int
            assignment_id: int
        """
        return PaginatedList(SubmissionHistory, self._requester, 'GET', 'courses/{}/gradebook_history/{}/graders/{}/assignments/{}/submissions'.format(self.id, date, grader_id, assignment_id), kwargs=combine_kwargs(**kwargs))

    def get_tabs(self, **kwargs) -> 'PaginatedList[Tab]':
        """
        List available tabs for a course.
        Returns a list of navigation tabs available in the current context.

        Endpoint: GET /api/v1/courses/:course_id/tabs

        Reference: https://canvas.instructure.com/doc/api/tabs.html#method.tabs.index
        """
        return PaginatedList(Tab, self._requester, 'GET', 'courses/{}/tabs'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def get_tabs_async(self, **kwargs) -> 'PaginatedList[Tab]':
        """
        List available tabs for a course.
        Returns a list of navigation tabs available in the current context.

        Endpoint: GET /api/v1/courses/:course_id/tabs

        Reference: https://canvas.instructure.com/doc/api/tabs.html#method.tabs.index
        """
        return PaginatedList(Tab, self._requester, 'GET', 'courses/{}/tabs'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def get_todo_items(self, **kwargs) -> 'PaginatedList[Todo]':
        """
        Returns the current user's course-specific todo items.

        Endpoint: GET /api/v1/courses/:course_id/todo

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.todo_items
        """
        return PaginatedList(Todo, self._requester, 'GET', 'courses/{}/todo'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_todo_items_async(self, **kwargs) -> 'PaginatedList[Todo]':
        """
        Returns the current user's course-specific todo items.

        Endpoint: GET /api/v1/courses/:course_id/todo

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.todo_items
        """
        return PaginatedList(Todo, self._requester, 'GET', 'courses/{}/todo'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def get_uncollated_submissions(self, **kwargs) -> 'PaginatedList[SubmissionVersion]':
        """
        Gives a paginated, uncollated list of submission versions for all matching
        submissions in the context. This SubmissionVersion objects will not include
        the new_grade or previous_grade keys, only the grade; same for graded_at
        and grader.

        Endpoint: GET /api/v1/courses/:course_id/gradebook_history/feed

        Reference: https://canvas.instructure.com/doc/api/gradebook_history.html#method        .gradebook_history_api.feed
        """
        return PaginatedList(SubmissionVersion, self._requester, 'GET', 'courses/{}/gradebook_history/feed'.format(self.id), kwargs=combine_kwargs(**kwargs))

    async def get_uncollated_submissions_async(self, **kwargs) -> 'PaginatedList[SubmissionVersion]':
        """
        Gives a paginated, uncollated list of submission versions for all matching
        submissions in the context. This SubmissionVersion objects will not include
        the new_grade or previous_grade keys, only the grade; same for graded_at
        and grader.

        Endpoint: GET /api/v1/courses/:course_id/gradebook_history/feed

        Reference: https://canvas.instructure.com/doc/api/gradebook_history.html#method        .gradebook_history_api.feed
        """
        return PaginatedList(SubmissionVersion, self._requester, 'GET', 'courses/{}/gradebook_history/feed'.format(self.id), kwargs=combine_kwargs(**kwargs))

    def get_user(self, user: 'User | int', user_id_type: 'str | None'=None, **kwargs) -> 'User':
        """
        Retrieve a user by their ID. `user_id_type` denotes which endpoint to try as there are
        several different ids that can pull the same user record from Canvas.

        Endpoint: GET /api/v1/courses/:course_id/users/:id

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.user

        Parameters:
            user: :class:`canvasapi.user.User` or int
            user_id_type: str
        """
        from .user import User
        if user_id_type:
            uri = 'courses/{}/users/{}:{}'.format(self.id, user_id_type, user)
        else:
            user_id = obj_or_id(user, 'user', (User,))
            uri = 'courses/{}/users/{}'.format(self.id, user_id)
        response: 'httpx.Response' = self._requester.request('GET', uri, _kwargs=combine_kwargs(**kwargs))
        return User(self._requester, response.json())

    async def get_user_async(self, user: 'User | int', user_id_type: 'str | None'=None, **kwargs) -> 'User':
        """
        Retrieve a user by their ID. `user_id_type` denotes which endpoint to try as there are
        several different ids that can pull the same user record from Canvas.

        Endpoint: GET /api/v1/courses/:course_id/users/:id

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.user

        Parameters:
            user: :class:`canvasapi.user.User` or int
            user_id_type: str
        """
        from .user import User
        if user_id_type:
            uri = 'courses/{}/users/{}:{}'.format(self.id, user_id_type, user)
        else:
            user_id = obj_or_id(user, 'user', (User,))
            uri = 'courses/{}/users/{}'.format(self.id, user_id)
        response: 'httpx.Response' = await self._requester.request_async('GET', uri, _kwargs=combine_kwargs(**kwargs))
        return User(self._requester, response.json())

    def get_user_in_a_course_level_assignment_data(self, user: 'User | int', **kwargs) -> 'dict':
        """
        Return a list of assignments for the course sorted by due date

        Endpoint: GET /api/v1/courses/:course_id/analytics/users/:student_id/assignments

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_assignments

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/analytics/users/{}/assignments'.format(self.id, user_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_user_in_a_course_level_assignment_data_async(self, user: 'User | int', **kwargs) -> 'dict':
        """
        Return a list of assignments for the course sorted by due date

        Endpoint: GET /api/v1/courses/:course_id/analytics/users/:student_id/assignments

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_assignments

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/analytics/users/{}/assignments'.format(self.id, user_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_user_in_a_course_level_messaging_data(self, user: 'User | int', **kwargs) -> 'dict':
        """
        Return messaging hits grouped by day through the entire history of the course

        Endpoint: GET /api/v1/courses/:course_id/analytics/users/:student_id/communication

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_messaging

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/analytics/users/{}/communication'.format(self.id, user_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_user_in_a_course_level_messaging_data_async(self, user: 'User | int', **kwargs) -> 'dict':
        """
        Return messaging hits grouped by day through the entire history of the course

        Endpoint: GET /api/v1/courses/:course_id/analytics/users/:student_id/communication

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_messaging

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/analytics/users/{}/communication'.format(self.id, user_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_user_in_a_course_level_participation_data(self, user: 'User | int', **kwargs) -> 'dict':
        """
        Return page view hits grouped by hour and participation details through course's history

        Endpoint: GET /api/v1/courses/:course_id/analytics/users/:student_id/activity

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_participation

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/analytics/users/{}/activity'.format(self.id, user_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_user_in_a_course_level_participation_data_async(self, user: 'User | int', **kwargs) -> 'dict':
        """
        Return page view hits grouped by hour and participation details through course's history

        Endpoint: GET /api/v1/courses/:course_id/analytics/users/:student_id/activity

        Reference: https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_participation

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        from .user import User
        user_id = obj_or_id(user, 'user', (User,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/analytics/users/{}/activity'.format(self.id, user_id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_users(self, **kwargs) -> 'PaginatedList[User]':
        """
        List all users in a course.

        Endpoint: GET /api/v1/courses/:course_id/search_users

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.users
        """
        from .user import User
        return PaginatedList(User, self._requester, 'GET', 'courses/{}/search_users'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_users_async(self, **kwargs) -> 'PaginatedList[User]':
        """
        List all users in a course.

        Endpoint: GET /api/v1/courses/:course_id/search_users

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.users
        """
        from .user import User
        return PaginatedList(User, self._requester, 'GET', 'courses/{}/search_users'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def import_outcome(self, attachment: 'str', **kwargs) -> 'OutcomeImport':
        """
        Import outcome into canvas.

        Endpoint: POST /api/v1/courses/:course_id/outcome_imports

        Reference: https://canvas.instructure.com/doc/api/outcome_imports.html#method.outcome_imports_api.create

        Parameters:
            attachment: file or str
        """
        attachment, is_path = file_or_path(attachment)
        try:
            response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/outcome_imports'.format(self.id), file={'attachment': attachment}, _kwargs=combine_kwargs(**kwargs))
            response_json: 'dict' = response.json()
            response_json.update({'course_id': self.id})
            return OutcomeImport(self._requester, response_json)
        finally:
            if is_path:
                attachment.close()

    async def import_outcome_async(self, attachment: 'str', **kwargs) -> 'OutcomeImport':
        """
        Import outcome into canvas.

        Endpoint: POST /api/v1/courses/:course_id/outcome_imports

        Reference: https://canvas.instructure.com/doc/api/outcome_imports.html#method.outcome_imports_api.create

        Parameters:
            attachment: file or str
        """
        attachment, is_path = file_or_path(attachment)
        try:
            response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/outcome_imports'.format(self.id), file={'attachment': attachment}, _kwargs=combine_kwargs(**kwargs))
            response_json: 'dict' = response.json()
            response_json.update({'course_id': self.id})
            return OutcomeImport(self._requester, response_json)
        finally:
            if is_path:
                attachment.close()

    def list_blueprint_subscriptions(self, **kwargs) -> 'PaginatedList[BlueprintSubscription]':
        """
        Return a list of blueprint subscriptions for the given course.

        Endpoint: GET /api/v1/courses/:course_id/blueprint_subscriptions

        Reference: https://canvas.instructure.com/doc/api/blueprint_courses.html#method.        master_courses/master_templates.subscriptions_index
        """
        return PaginatedList(BlueprintSubscription, self._requester, 'GET', 'courses/{}/blueprint_subscriptions'.format(self.id), {'course_id': self.id}, kwargs=combine_kwargs(**kwargs))

    async def list_blueprint_subscriptions_async(self, **kwargs) -> 'PaginatedList[BlueprintSubscription]':
        """
        Return a list of blueprint subscriptions for the given course.

        Endpoint: GET /api/v1/courses/:course_id/blueprint_subscriptions

        Reference: https://canvas.instructure.com/doc/api/blueprint_courses.html#method.        master_courses/master_templates.subscriptions_index
        """
        return PaginatedList(BlueprintSubscription, self._requester, 'GET', 'courses/{}/blueprint_subscriptions'.format(self.id), {'course_id': self.id}, kwargs=combine_kwargs(**kwargs))

    def preview_html(self, html: 'str', **kwargs) -> 'str':
        """
        Preview HTML content processed for this course.

        Endpoint: POST /api/v1/courses/:course_id/preview_html

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.preview_html

        Parameters:
            html: str
        """
        kwargs['html'] = html
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/preview_html'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('html', '')

    async def preview_html_async(self, html: 'str', **kwargs) -> 'str':
        """
        Preview HTML content processed for this course.

        Endpoint: POST /api/v1/courses/:course_id/preview_html

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.preview_html

        Parameters:
            html: str
        """
        kwargs['html'] = html
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/preview_html'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('html', '')

    def query_audit_by_course(self, **kwargs) -> 'list[CourseEvent]':
        """
        Lists course change events for a specific course.

        Endpoint: GET /api/v1/audit/course/courses/:course_id

        Reference: https://canvas.instructure.com/doc/api/course_audit_log.html#method.course_audit_api.for_course
        """
        return PaginatedList(CourseEvent, self._requester, 'GET', 'audit/course/courses/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def query_audit_by_course_async(self, **kwargs) -> 'list[CourseEvent]':
        """
        Lists course change events for a specific course.

        Endpoint: GET /api/v1/audit/course/courses/:course_id

        Reference: https://canvas.instructure.com/doc/api/course_audit_log.html#method.course_audit_api.for_course
        """
        return PaginatedList(CourseEvent, self._requester, 'GET', 'audit/course/courses/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def remove_usage_rights(self, **kwargs) -> 'dict':
        """
        Removes the usage rights for specified files that are under the current course scope

        Endpoint: DELETE /api/v1/courses/:course_id/usage_rights

        Reference: https://canvas.instructure.com/doc/api/files.html#method.usage_rights.remove_usage_rights
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/usage_rights'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def remove_usage_rights_async(self, **kwargs) -> 'dict':
        """
        Removes the usage rights for specified files that are under the current course scope

        Endpoint: DELETE /api/v1/courses/:course_id/usage_rights

        Reference: https://canvas.instructure.com/doc/api/files.html#method.usage_rights.remove_usage_rights
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/usage_rights'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def reorder_pinned_topics(self, order: 'string | iterable sequence[values]', **kwargs) -> 'PaginatedList[DiscussionTopic]':
        """
        Puts the pinned discussion topics in the specified order.
        All pinned topics should be included.

        Endpoint: POST /api/v1/courses/:course_id/discussion_topics/reorder

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.reorder

        Parameters:
            order: string or iterable sequence of values
        """
        if is_multivalued(order):
            order = ','.join([str(topic_id) for topic_id in order])
        if not isinstance(order, str) or ',' not in order:
            raise ValueError('Param `order` must be a list, tuple, or string.')
        kwargs['order'] = order
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/discussion_topics/reorder'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('reorder')

    async def reorder_pinned_topics_async(self, order: 'string | iterable sequence[values]', **kwargs) -> 'PaginatedList[DiscussionTopic]':
        """
        Puts the pinned discussion topics in the specified order.
        All pinned topics should be included.

        Endpoint: POST /api/v1/courses/:course_id/discussion_topics/reorder

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.reorder

        Parameters:
            order: string or iterable sequence of values
        """
        if is_multivalued(order):
            order = ','.join([str(topic_id) for topic_id in order])
        if not isinstance(order, str) or ',' not in order:
            raise ValueError('Param `order` must be a list, tuple, or string.')
        kwargs['order'] = order
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/discussion_topics/reorder'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json().get('reorder')

    def reset(self, **kwargs) -> 'Course':
        """
        Delete the current course and create a new equivalent course
        with no content, but all sections and users moved over.

        Endpoint: POST /api/v1/courses/:course_id/reset_content

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.reset_content
        """
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/reset_content'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Course(self._requester, response.json())

    async def reset_async(self, **kwargs) -> 'Course':
        """
        Delete the current course and create a new equivalent course
        with no content, but all sections and users moved over.

        Endpoint: POST /api/v1/courses/:course_id/reset_content

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.reset_content
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/reset_content'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Course(self._requester, response.json())

    def resolve_path(self, full_path: 'string | None'=None, **kwargs) -> 'PaginatedList[Folder]':
        """
        Returns the paginated list of all of the folders in the given
        path starting at the course root folder. Returns root folder if called
        with no arguments.

        Endpoint: GET /api/v1/courses/:course_id/folders/by_path/*full_path

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.resolve_path

        Parameters:
            full_path: string
        """
        if full_path:
            return PaginatedList(Folder, self._requester, 'GET', 'courses/{0}/folders/by_path/{1}'.format(self.id, full_path), _kwargs=combine_kwargs(**kwargs))
        else:
            return PaginatedList(Folder, self._requester, 'GET', 'courses/{0}/folders/by_path'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    async def resolve_path_async(self, full_path: 'string | None'=None, **kwargs) -> 'PaginatedList[Folder]':
        """
        Returns the paginated list of all of the folders in the given
        path starting at the course root folder. Returns root folder if called
        with no arguments.

        Endpoint: GET /api/v1/courses/:course_id/folders/by_path/*full_path

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.resolve_path

        Parameters:
            full_path: string
        """
        if full_path:
            return PaginatedList(Folder, self._requester, 'GET', 'courses/{0}/folders/by_path/{1}'.format(self.id, full_path), _kwargs=combine_kwargs(**kwargs))
        else:
            return PaginatedList(Folder, self._requester, 'GET', 'courses/{0}/folders/by_path'.format(self.id), _kwargs=combine_kwargs(**kwargs))

    def set_quiz_extensions(self, quiz_extensions: 'list', **kwargs) -> 'list[QuizExtension]':
        """
        Set extensions for student all quiz submissions in a course.

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:quiz_id/extensions

        Reference: https://canvas.instructure.com/doc/api/quiz_extensions.html#method.quizzes/quiz_extensions.create

        Parameters:
            quiz_extensions: list
        """
        if not isinstance(quiz_extensions, list) or not quiz_extensions:
            raise ValueError('Param `quiz_extensions` must be a non-empty list.')
        if any((not isinstance(extension, dict) for extension in quiz_extensions)):
            raise ValueError('Param `quiz_extensions` must only contain dictionaries')
        if any(('user_id' not in extension for extension in quiz_extensions)):
            raise RequiredFieldMissing('Dictionaries in `quiz_extensions` must contain key `user_id`')
        kwargs['quiz_extensions'] = quiz_extensions
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/quiz_extensions'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        extension_list = response.json()['quiz_extensions']
        return [QuizExtension(self._requester, extension) for extension in extension_list]

    async def set_quiz_extensions_async(self, quiz_extensions: 'list', **kwargs) -> 'list[QuizExtension]':
        """
        Set extensions for student all quiz submissions in a course.

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:quiz_id/extensions

        Reference: https://canvas.instructure.com/doc/api/quiz_extensions.html#method.quizzes/quiz_extensions.create

        Parameters:
            quiz_extensions: list
        """
        if not isinstance(quiz_extensions, list) or not quiz_extensions:
            raise ValueError('Param `quiz_extensions` must be a non-empty list.')
        if any((not isinstance(extension, dict) for extension in quiz_extensions)):
            raise ValueError('Param `quiz_extensions` must only contain dictionaries')
        if any(('user_id' not in extension for extension in quiz_extensions)):
            raise RequiredFieldMissing('Dictionaries in `quiz_extensions` must contain key `user_id`')
        kwargs['quiz_extensions'] = quiz_extensions
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/quiz_extensions'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        extension_list = response.json()['quiz_extensions']
        return [QuizExtension(self._requester, extension) for extension in extension_list]

    def set_usage_rights(self, **kwargs) -> 'UsageRights':
        """
        Changes the usage rights for specified files that are under the current course scope

        Endpoint: PUT /api/v1/courses/:course_id/usage_rights

        Reference: https://canvas.instructure.com/doc/api/files.html#method.usage_rights.set_usage_rights
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/usage_rights'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return UsageRights(self._requester, response.json())

    async def set_usage_rights_async(self, **kwargs) -> 'UsageRights':
        """
        Changes the usage rights for specified files that are under the current course scope

        Endpoint: PUT /api/v1/courses/:course_id/usage_rights

        Reference: https://canvas.instructure.com/doc/api/files.html#method.usage_rights.set_usage_rights
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/usage_rights'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return UsageRights(self._requester, response.json())

    def show_front_page(self, **kwargs) -> 'Course':
        """
        Retrieve the content of the front page.

        Endpoint: GET /api/v1/courses/:course_id/front_page

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_front_page
        """
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/front_page'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        page_json: 'dict' = response.json()
        page_json.update({'course_id': self.id})
        return Page(self._requester, page_json)

    async def show_front_page_async(self, **kwargs) -> 'Course':
        """
        Retrieve the content of the front page.

        Endpoint: GET /api/v1/courses/:course_id/front_page

        Reference: https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_front_page
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/front_page'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        page_json: 'dict' = response.json()
        page_json.update({'course_id': self.id})
        return Page(self._requester, page_json)

    def submissions_bulk_update(self, **kwargs) -> 'Progress':
        """
        Update the grading and comments on multiple student's assignment
        submissions in an asynchronous job.

        Endpoint: POST /api/v1/courses/:course_id/submissions/update_grades

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.bulk_update
        """
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/submissions/update_grades'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Progress(self._requester, response.json())

    async def submissions_bulk_update_async(self, **kwargs) -> 'Progress':
        """
        Update the grading and comments on multiple student's assignment
        submissions in an asynchronous job.

        Endpoint: POST /api/v1/courses/:course_id/submissions/update_grades

        Reference: https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.bulk_update
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/submissions/update_grades'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        return Progress(self._requester, response.json())

    def update(self, **kwargs) -> 'bool':
        """
        Update this course.

        Endpoint: PUT /api/v1/courses/:id

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if response.json().get('name'):
            super(Course, self).set_attributes(response.json())
        return response.json().get('name')

    async def update_async(self, **kwargs) -> 'bool':
        """
        Update this course.

        Endpoint: PUT /api/v1/courses/:id

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if response.json().get('name'):
            super(Course, self).set_attributes(response.json())
        return response.json().get('name')

    def update_assignment_overrides(self, assignment_overrides: 'list', **kwargs) -> 'PaginatedList[AssignmentOverride]':
        """
        Update a list of specified overrides for each assignment.
        
        Note: All current overridden values must be supplied if they are to be retained.

        Endpoint: PUT /api/v1/courses/:course_id/assignments/overrides

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.batch_update

        Parameters:
            assignment_overrides: list
        """
        from .assignment import AssignmentOverride
        kwargs['assignment_overrides'] = assignment_overrides
        return PaginatedList(AssignmentOverride, self._requester, 'PUT', 'courses/{}/assignments/overrides'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    async def update_assignment_overrides_async(self, assignment_overrides: 'list', **kwargs) -> 'PaginatedList[AssignmentOverride]':
        """
        Update a list of specified overrides for each assignment.
        
        Note: All current overridden values must be supplied if they are to be retained.

        Endpoint: PUT /api/v1/courses/:course_id/assignments/overrides

        Reference: https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.batch_update

        Parameters:
            assignment_overrides: list
        """
        from .assignment import AssignmentOverride
        kwargs['assignment_overrides'] = assignment_overrides
        return PaginatedList(AssignmentOverride, self._requester, 'PUT', 'courses/{}/assignments/overrides'.format(self.id), {'course_id': self.id}, _kwargs=combine_kwargs(**kwargs))

    def update_settings(self, **kwargs) -> 'dict':
        """
        Update a course's settings.

        Endpoint: PUT /api/v1/courses/:course_id/settings

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.update_settings
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/settings'.format(self.id), **kwargs)
        return response.json()

    async def update_settings_async(self, **kwargs) -> 'dict':
        """
        Update a course's settings.

        Endpoint: PUT /api/v1/courses/:course_id/settings

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.update_settings
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/settings'.format(self.id), **kwargs)
        return response.json()

    def upload(self, file: 'FileOrPathLike | str', **kwargs) -> 'tuple':
        """
        Upload a file to this course.

        Endpoint: POST /api/v1/courses/:course_id/files

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.create_file

        Parameters:
            file: file or str
        """
        return Uploader(self._requester, 'courses/{}/files'.format(self.id), file, **kwargs).start()

    async def upload_async(self, file: 'FileOrPathLike | str', **kwargs) -> 'tuple':
        """
        Upload a file to this course.

        Endpoint: POST /api/v1/courses/:course_id/files

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.create_file

        Parameters:
            file: file or str
        """
        return Uploader(self._requester, 'courses/{}/files'.format(self.id), file, **kwargs).start()

class CourseNickname(CourseNicknameModel):

    def __str__(self):
        return '{} ({})'.format(self.nickname, self.course_id)

    def remove(self, **kwargs) -> 'CourseNickname':
        """
        Remove the nickname for the given course. Subsequent course API
        calls will return the actual name for the course.

        Endpoint: DELETE /api/v1/users/self/course_nicknames/:course_id

        Reference: https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.delete
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'users/self/course_nicknames/{}'.format(self.course_id), _kwargs=combine_kwargs(**kwargs))
        return CourseNickname(self._requester, response.json())

    async def remove_async(self, **kwargs) -> 'CourseNickname':
        """
        Remove the nickname for the given course. Subsequent course API
        calls will return the actual name for the course.

        Endpoint: DELETE /api/v1/users/self/course_nicknames/:course_id

        Reference: https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.delete
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'users/self/course_nicknames/{}'.format(self.course_id), _kwargs=combine_kwargs(**kwargs))
        return CourseNickname(self._requester, response.json())

class CourseStudentSummary(CanvasObject):

    def __str__(self):
        return 'Course Student Summary {}'.format(self.id)

class LatePolicy(LatePolicyModel):

    def __str__(self):
        return 'Late Policy {}'.format(self.id)