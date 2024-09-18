import httpx
import typing
if typing.TYPE_CHECKING:
    from .section import Section
    from .outcome import Outcome, OutcomeGroup
    from .folder import Folder
    from .file import File
    from .course_epub_export import CourseEpubExport
    from .eportfolio import EPortfolio
    from .current_user import CurrentUser
    from .course import Course, CourseNickname
    from .comm_message import CommMessage
    from .user import User
    from .discussion_topic import DiscussionTopic
    from .account_calendar import AccountCalendar
    from .paginated_list import PaginatedList
    from .poll import Poll
    from .planner import PlannerNote, PlannerOverride
    from .jwt import JWT
    from .group import Group, GroupCategory
    from .conversation import Conversation
    from .calendar_event import CalendarEvent
    from .appointment_group import AppointmentGroup
    from .account import Account
    from .progress import Progress
import warnings
from .account import Account
from .account_calendar import AccountCalendar
from .appointment_group import AppointmentGroup
from .calendar_event import CalendarEvent
from .comm_message import CommMessage
from .conversation import Conversation
from .course import Course, CourseNickname
from .course_epub_export import CourseEpubExport
from .current_user import CurrentUser
from .discussion_topic import DiscussionTopic
from .eportfolio import EPortfolio
from .exceptions import RequiredFieldMissing
from .file import File
from .folder import Folder
from .group import Group, GroupCategory
from .jwt import JWT
from .outcome import Outcome, OutcomeGroup
from .paginated_list import PaginatedList
from .planner import PlannerNote, PlannerOverride
from .poll import Poll
from .progress import Progress
from .requester import Requester
from .section import Section
from .todo import Todo
from .user import User
from .util import combine_kwargs, get_institution_url, obj_or_id

class Canvas(object):
    """
    The main class to be instantiated to provide access to Canvas's API.
    """

    def __init__(self, base_url, access_token):
        """
        :param base_url: The base URL of the Canvas instance's API.
        :type base_url: str
        :param access_token: The API key to authenticate requests with.
        :type access_token: str
        """
        if 'api/v1' in base_url:
            raise ValueError('`base_url` should not specify an API version. Remove trailing /api/v1/')
        if 'http://' in base_url:
            warnings.warn('Canvas may respond unexpectedly when making requests to HTTP URLs. If possible, please use HTTPS.', UserWarning)
        if not base_url.strip():
            warnings.warn('Canvas needs a valid URL, please provide a non-blank `base_url`.', UserWarning)
        if '://' not in base_url:
            warnings.warn('An invalid `base_url` for the Canvas API Instance was used. Please provide a valid HTTP or HTTPS URL if possible.', UserWarning)
        access_token = access_token.strip()
        base_url = get_institution_url(base_url)
        self.__requester = Requester(base_url, access_token)

    def clear_course_nicknames(self, **kwargs) -> 'bool':
        """
        Remove all stored course nicknames.

        Endpoint: DELETE /api/v1/users/self/course_nicknames

        Reference: https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.clear
        """
        response: 'httpx.Response' = self.__requester.request('DELETE', 'users/self/course_nicknames', _kwargs=combine_kwargs(**kwargs))
        return response.json().get('message') == 'OK'

    async def clear_course_nicknames_async(self, **kwargs) -> 'bool':
        """
        Remove all stored course nicknames.

        Endpoint: DELETE /api/v1/users/self/course_nicknames

        Reference: https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.clear
        """
        response: 'httpx.Response' = await self.__requester.request_async('DELETE', 'users/self/course_nicknames', _kwargs=combine_kwargs(**kwargs))
        return response.json().get('message') == 'OK'

    def conversations_batch_update(self, conversation_ids: 'list[str]', event: 'str', **kwargs) -> 'Progress':
        """
        

        Endpoint: PUT /api/v1/conversations

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.batch_update

        Parameters:
            conversation_ids: `list` of `str`
            event: `str`
        """
        ALLOWED_EVENTS = ['mark_as_read', 'mark_as_unread', 'star', 'unstar', 'archive', 'destroy']
        if event not in ALLOWED_EVENTS:
            raise ValueError('{} is not a valid action. Please use one of the following: {}'.format(event, ','.join(ALLOWED_EVENTS)))
        if len(conversation_ids) > 500:
            raise ValueError('You have requested {} updates, which exceeds the limit of 500'.format(len(conversation_ids)))
        kwargs['conversation_ids'] = conversation_ids
        kwargs['event'] = event
        response: 'httpx.Response' = self.__requester.request('PUT', 'conversations', _kwargs=combine_kwargs(**kwargs))
        return_progress = Progress(self.__requester, response.json())
        return return_progress

    async def conversations_batch_update_async(self, conversation_ids: 'list[str]', event: 'str', **kwargs) -> 'Progress':
        """
        

        Endpoint: PUT /api/v1/conversations

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.batch_update

        Parameters:
            conversation_ids: `list` of `str`
            event: `str`
        """
        ALLOWED_EVENTS = ['mark_as_read', 'mark_as_unread', 'star', 'unstar', 'archive', 'destroy']
        if event not in ALLOWED_EVENTS:
            raise ValueError('{} is not a valid action. Please use one of the following: {}'.format(event, ','.join(ALLOWED_EVENTS)))
        if len(conversation_ids) > 500:
            raise ValueError('You have requested {} updates, which exceeds the limit of 500'.format(len(conversation_ids)))
        kwargs['conversation_ids'] = conversation_ids
        kwargs['event'] = event
        response: 'httpx.Response' = await self.__requester.request_async('PUT', 'conversations', _kwargs=combine_kwargs(**kwargs))
        return_progress = Progress(self.__requester, response.json())
        return return_progress

    def conversations_get_running_batches(self, **kwargs) -> 'dict':
        """
        Returns any currently running conversation batches for the current user.
        Conversation batches are created when a bulk private message is sent
        asynchronously.

        Endpoint: GET /api/v1/conversations/batches

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.batches
        """
        response: 'httpx.Response' = self.__requester.request('GET', 'conversations/batches', _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def conversations_get_running_batches_async(self, **kwargs) -> 'dict':
        """
        Returns any currently running conversation batches for the current user.
        Conversation batches are created when a bulk private message is sent
        asynchronously.

        Endpoint: GET /api/v1/conversations/batches

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.batches
        """
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'conversations/batches', _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def conversations_mark_all_as_read(self, **kwargs) -> 'bool':
        """
        Mark all conversations as read.

        Endpoint: POST /api/v1/conversations/mark_all_as_read

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.mark_all_as_read
        """
        response: 'httpx.Response' = self.__requester.request('POST', 'conversations/mark_all_as_read', _kwargs=combine_kwargs(**kwargs))
        return response.json() == {}

    async def conversations_mark_all_as_read_async(self, **kwargs) -> 'bool':
        """
        Mark all conversations as read.

        Endpoint: POST /api/v1/conversations/mark_all_as_read

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.mark_all_as_read
        """
        response: 'httpx.Response' = await self.__requester.request_async('POST', 'conversations/mark_all_as_read', _kwargs=combine_kwargs(**kwargs))
        return response.json() == {}

    def conversations_unread_count(self, **kwargs) -> 'dict':
        """
        Get the number of unread conversations for the current user

        Endpoint: GET /api/v1/conversations/unread_count

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.unread_count
        """
        response: 'httpx.Response' = self.__requester.request('GET', 'conversations/unread_count', _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def conversations_unread_count_async(self, **kwargs) -> 'dict':
        """
        Get the number of unread conversations for the current user

        Endpoint: GET /api/v1/conversations/unread_count

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.unread_count
        """
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'conversations/unread_count', _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def create_account(self, **kwargs) -> 'Account':
        """
        Create a new root account.

        Endpoint: POST /api/v1/accounts

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.accounts.create
        """
        response: 'httpx.Response' = self.__requester.request('POST', 'accounts', _kwargs=combine_kwargs(**kwargs))
        return Account(self.__requester, response.json())

    async def create_account_async(self, **kwargs) -> 'Account':
        """
        Create a new root account.

        Endpoint: POST /api/v1/accounts

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.accounts.create
        """
        response: 'httpx.Response' = await self.__requester.request_async('POST', 'accounts', _kwargs=combine_kwargs(**kwargs))
        return Account(self.__requester, response.json())

    def create_appointment_group(self, appointment_group: 'dict', **kwargs) -> 'AppointmentGroup':
        """
        Create a new Appointment Group.

        Endpoint: POST /api/v1/appointment_groups

        Reference: https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.create

        Parameters:
            appointment_group: `dict`
        """
        if isinstance(appointment_group, dict) and 'context_codes' in appointment_group and ('title' in appointment_group):
            kwargs['appointment_group'] = appointment_group
        elif isinstance(appointment_group, dict) and 'context_codes' not in appointment_group:
            raise RequiredFieldMissing("Dictionary with key 'context_codes' is missing.")
        elif isinstance(appointment_group, dict) and 'title' not in appointment_group:
            raise RequiredFieldMissing("Dictionary with key 'title' is missing.")
        response: 'httpx.Response' = self.__requester.request('POST', 'appointment_groups', _kwargs=combine_kwargs(**kwargs))
        return AppointmentGroup(self.__requester, response.json())

    async def create_appointment_group_async(self, appointment_group: 'dict', **kwargs) -> 'AppointmentGroup':
        """
        Create a new Appointment Group.

        Endpoint: POST /api/v1/appointment_groups

        Reference: https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.create

        Parameters:
            appointment_group: `dict`
        """
        if isinstance(appointment_group, dict) and 'context_codes' in appointment_group and ('title' in appointment_group):
            kwargs['appointment_group'] = appointment_group
        elif isinstance(appointment_group, dict) and 'context_codes' not in appointment_group:
            raise RequiredFieldMissing("Dictionary with key 'context_codes' is missing.")
        elif isinstance(appointment_group, dict) and 'title' not in appointment_group:
            raise RequiredFieldMissing("Dictionary with key 'title' is missing.")
        response: 'httpx.Response' = await self.__requester.request_async('POST', 'appointment_groups', _kwargs=combine_kwargs(**kwargs))
        return AppointmentGroup(self.__requester, response.json())

    def create_calendar_event(self, calendar_event: 'dict', **kwargs) -> 'CalendarEvent':
        """
        Create a new Calendar Event.

        Endpoint: POST /api/v1/calendar_events

        Reference: https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.create

        Parameters:
            calendar_event: `dict`
        """
        if isinstance(calendar_event, dict) and 'context_code' in calendar_event:
            kwargs['calendar_event'] = calendar_event
        else:
            raise RequiredFieldMissing("Dictionary with key 'context_code' is required.")
        response: 'httpx.Response' = self.__requester.request('POST', 'calendar_events', _kwargs=combine_kwargs(**kwargs))
        return CalendarEvent(self.__requester, response.json())

    async def create_calendar_event_async(self, calendar_event: 'dict', **kwargs) -> 'CalendarEvent':
        """
        Create a new Calendar Event.

        Endpoint: POST /api/v1/calendar_events

        Reference: https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.create

        Parameters:
            calendar_event: `dict`
        """
        if isinstance(calendar_event, dict) and 'context_code' in calendar_event:
            kwargs['calendar_event'] = calendar_event
        else:
            raise RequiredFieldMissing("Dictionary with key 'context_code' is required.")
        response: 'httpx.Response' = await self.__requester.request_async('POST', 'calendar_events', _kwargs=combine_kwargs(**kwargs))
        return CalendarEvent(self.__requester, response.json())

    def create_conversation(self, recipients: 'list[str]', body: 'str', **kwargs) -> 'list[Conversation]':
        """
        Create a new Conversation.

        Endpoint: POST /api/v1/conversations

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.create

        Parameters:
            recipients: `list` of `str`
            body: `str`
        """
        kwargs['recipients'] = recipients
        kwargs['body'] = body
        response: 'httpx.Response' = self.__requester.request('POST', 'conversations', _kwargs=combine_kwargs(**kwargs))
        return [Conversation(self.__requester, convo) for convo in response.json()]

    async def create_conversation_async(self, recipients: 'list[str]', body: 'str', **kwargs) -> 'list[Conversation]':
        """
        Create a new Conversation.

        Endpoint: POST /api/v1/conversations

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.create

        Parameters:
            recipients: `list` of `str`
            body: `str`
        """
        kwargs['recipients'] = recipients
        kwargs['body'] = body
        response: 'httpx.Response' = await self.__requester.request_async('POST', 'conversations', _kwargs=combine_kwargs(**kwargs))
        return [Conversation(self.__requester, convo) for convo in response.json()]

    def create_group(self, **kwargs) -> 'Group':
        """
        Create a group

        Endpoint: POST /api/v1/groups/

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.create
        """
        response: 'httpx.Response' = self.__requester.request('POST', 'groups', _kwargs=combine_kwargs(**kwargs))
        return Group(self.__requester, response.json())

    async def create_group_async(self, **kwargs) -> 'Group':
        """
        Create a group

        Endpoint: POST /api/v1/groups/

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.create
        """
        response: 'httpx.Response' = await self.__requester.request_async('POST', 'groups', _kwargs=combine_kwargs(**kwargs))
        return Group(self.__requester, response.json())

    def create_jwt(self, **kwargs) -> 'list[JWT]':
        """
        Creates a unique JWT to use with other Canvas services.

        Endpoint: POST /api/v1/jwts

        Reference: https://canvas.instructure.com/doc/api/jw_ts.html#method.jwts.create
        """
        response: 'httpx.Response' = self.__requester.request('POST', 'jwts', _kwargs=combine_kwargs(**kwargs))
        return JWT(self.__requester, response.json())

    async def create_jwt_async(self, **kwargs) -> 'list[JWT]':
        """
        Creates a unique JWT to use with other Canvas services.

        Endpoint: POST /api/v1/jwts

        Reference: https://canvas.instructure.com/doc/api/jw_ts.html#method.jwts.create
        """
        response: 'httpx.Response' = await self.__requester.request_async('POST', 'jwts', _kwargs=combine_kwargs(**kwargs))
        return JWT(self.__requester, response.json())

    def create_planner_note(self, **kwargs) -> 'PlannerNote':
        """
        Create a planner note for the current user

        Endpoint: POST /api/v1/planner_notes

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_notes.create
        """
        response: 'httpx.Response' = self.__requester.request('POST', 'planner_notes', _kwargs=combine_kwargs(**kwargs))
        return PlannerNote(self.__requester, response.json())

    async def create_planner_note_async(self, **kwargs) -> 'PlannerNote':
        """
        Create a planner note for the current user

        Endpoint: POST /api/v1/planner_notes

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_notes.create
        """
        response: 'httpx.Response' = await self.__requester.request_async('POST', 'planner_notes', _kwargs=combine_kwargs(**kwargs))
        return PlannerNote(self.__requester, response.json())

    def create_planner_override(self, plannable_type: 'str', plannable_id: 'int | PlannerOverride', **kwargs) -> 'PlannerOverride':
        """
        Create a planner override for the current user

        Endpoint: POST /api/v1/planner/overrides

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_overrides.create

        Parameters:
            plannable_type: str
            plannable_id: int or :class:`canvasapi.planner.PlannerOverride`
        """
        if isinstance(plannable_type, str):
            kwargs['plannable_type'] = plannable_type
        else:
            raise RequiredFieldMissing('plannable_type is required as a str.')
        if isinstance(plannable_id, int):
            kwargs['plannable_id'] = plannable_id
        else:
            raise RequiredFieldMissing('plannable_id is required as an int.')
        response: 'httpx.Response' = self.__requester.request('POST', 'planner/overrides', _kwargs=combine_kwargs(**kwargs))
        return PlannerOverride(self.__requester, response.json())

    async def create_planner_override_async(self, plannable_type: 'str', plannable_id: 'int | PlannerOverride', **kwargs) -> 'PlannerOverride':
        """
        Create a planner override for the current user

        Endpoint: POST /api/v1/planner/overrides

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_overrides.create

        Parameters:
            plannable_type: str
            plannable_id: int or :class:`canvasapi.planner.PlannerOverride`
        """
        if isinstance(plannable_type, str):
            kwargs['plannable_type'] = plannable_type
        else:
            raise RequiredFieldMissing('plannable_type is required as a str.')
        if isinstance(plannable_id, int):
            kwargs['plannable_id'] = plannable_id
        else:
            raise RequiredFieldMissing('plannable_id is required as an int.')
        response: 'httpx.Response' = await self.__requester.request_async('POST', 'planner/overrides', _kwargs=combine_kwargs(**kwargs))
        return PlannerOverride(self.__requester, response.json())

    def create_poll(self, polls: 'list[dict]', **kwargs) -> 'Poll':
        """
        Create a new poll for the current user.

        Endpoint: POST /api/v1/polls

        Reference: https://canvas.instructure.com/doc/api/polls.html#method.polling/polls.create

        Parameters:
            polls: list of dict
        """
        if isinstance(polls, list) and isinstance(polls[0], dict) and ('question' in polls[0]):
            kwargs['polls'] = polls
        else:
            raise RequiredFieldMissing("List of dictionaries each with key 'question' is required.")
        response: 'httpx.Response' = self.__requester.request('POST', 'polls', _kwargs=combine_kwargs(**kwargs))
        return Poll(self.__requester, response.json()['polls'][0])

    async def create_poll_async(self, polls: 'list[dict]', **kwargs) -> 'Poll':
        """
        Create a new poll for the current user.

        Endpoint: POST /api/v1/polls

        Reference: https://canvas.instructure.com/doc/api/polls.html#method.polling/polls.create

        Parameters:
            polls: list of dict
        """
        if isinstance(polls, list) and isinstance(polls[0], dict) and ('question' in polls[0]):
            kwargs['polls'] = polls
        else:
            raise RequiredFieldMissing("List of dictionaries each with key 'question' is required.")
        response: 'httpx.Response' = await self.__requester.request_async('POST', 'polls', _kwargs=combine_kwargs(**kwargs))
        return Poll(self.__requester, response.json()['polls'][0])

    def get_account(self, account: 'int | str | Account', use_sis_id: 'bool'=False, **kwargs) -> 'Account':
        """
        Retrieve information on an individual account.

        Endpoint: GET /api/v1/accounts/:id

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.accounts.show

        Parameters:
            account: int, str or :class:`canvasapi.account.Account`
            use_sis_id: bool
        """
        if use_sis_id:
            account_id = account
            uri_str = 'accounts/sis_account_id:{}'
        else:
            account_id = obj_or_id(account, 'account', (Account,))
            uri_str = 'accounts/{}'
        response: 'httpx.Response' = self.__requester.request('GET', uri_str.format(account_id), _kwargs=combine_kwargs(**kwargs))
        return Account(self.__requester, response.json())

    async def get_account_async(self, account: 'int | str | Account', use_sis_id: 'bool'=False, **kwargs) -> 'Account':
        """
        Retrieve information on an individual account.

        Endpoint: GET /api/v1/accounts/:id

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.accounts.show

        Parameters:
            account: int, str or :class:`canvasapi.account.Account`
            use_sis_id: bool
        """
        if use_sis_id:
            account_id = account
            uri_str = 'accounts/sis_account_id:{}'
        else:
            account_id = obj_or_id(account, 'account', (Account,))
            uri_str = 'accounts/{}'
        response: 'httpx.Response' = await self.__requester.request_async('GET', uri_str.format(account_id), _kwargs=combine_kwargs(**kwargs))
        return Account(self.__requester, response.json())

    def get_account_calendars(self, **kwargs) -> 'PaginatedList[AccountCalendar]':
        """
        Returns a paginated list of account calendars available to the user.

        Endpoint: GET /api/v1/account_calendars

        Reference: https://canvas.instructure.com/doc/api/account_calendars.html#method.account_calendars_api.index
        """
        return PaginatedList(AccountCalendar, self.__requester, 'GET', 'account_calendars', _kwargs=combine_kwargs(**kwargs))

    async def get_account_calendars_async(self, **kwargs) -> 'PaginatedList[AccountCalendar]':
        """
        Returns a paginated list of account calendars available to the user.

        Endpoint: GET /api/v1/account_calendars

        Reference: https://canvas.instructure.com/doc/api/account_calendars.html#method.account_calendars_api.index
        """
        return PaginatedList(AccountCalendar, self.__requester, 'GET', 'account_calendars', _kwargs=combine_kwargs(**kwargs))

    def get_accounts(self, **kwargs) -> 'PaginatedList[Account]':
        """
        List accounts that the current user can view or manage.
        
        Typically, students and teachers will get an empty list in
        response. Only account admins can view the accounts that they
        are in.

        Endpoint: GET /api/v1/accounts

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.accounts.index
        """
        return PaginatedList(Account, self.__requester, 'GET', 'accounts', _kwargs=combine_kwargs(**kwargs))

    async def get_accounts_async(self, **kwargs) -> 'PaginatedList[Account]':
        """
        List accounts that the current user can view or manage.
        
        Typically, students and teachers will get an empty list in
        response. Only account admins can view the accounts that they
        are in.

        Endpoint: GET /api/v1/accounts

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.accounts.index
        """
        return PaginatedList(Account, self.__requester, 'GET', 'accounts', _kwargs=combine_kwargs(**kwargs))

    def get_activity_stream_summary(self, **kwargs) -> 'dict':
        """
        Return a summary of the current user's global activity stream.

        Endpoint: GET /api/v1/users/self/activity_stream/summary

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.activity_stream_summary
        """
        response: 'httpx.Response' = self.__requester.request('GET', 'users/self/activity_stream/summary', _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_activity_stream_summary_async(self, **kwargs) -> 'dict':
        """
        Return a summary of the current user's global activity stream.

        Endpoint: GET /api/v1/users/self/activity_stream/summary

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.activity_stream_summary
        """
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'users/self/activity_stream/summary', _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_announcements(self, context_codes: 'list', **kwargs) -> 'PaginatedList[DiscussionTopic]':
        """
        List announcements.

        Endpoint: GET /api/v1/announcements

        Reference: https://canvas.instructure.com/doc/api/announcements.html#method.announcements_api.index

        Parameters:
            context_codes: list
        """
        if type(context_codes) is not list or len(context_codes) == 0:
            raise RequiredFieldMissing('context_codes need to be passed as a list')
        if isinstance(context_codes[0], str) and 'course_' in context_codes[0]:
            kwargs['context_codes'] = context_codes
        else:
            course_ids = [obj_or_id(course_id, 'context_codes', (Course,)) for course_id in context_codes]
            kwargs['context_codes'] = [f'course_{course_id}' for course_id in course_ids]
        return PaginatedList(DiscussionTopic, self.__requester, 'GET', 'announcements', _kwargs=combine_kwargs(**kwargs))

    async def get_announcements_async(self, context_codes: 'list', **kwargs) -> 'PaginatedList[DiscussionTopic]':
        """
        List announcements.

        Endpoint: GET /api/v1/announcements

        Reference: https://canvas.instructure.com/doc/api/announcements.html#method.announcements_api.index

        Parameters:
            context_codes: list
        """
        if type(context_codes) is not list or len(context_codes) == 0:
            raise RequiredFieldMissing('context_codes need to be passed as a list')
        if isinstance(context_codes[0], str) and 'course_' in context_codes[0]:
            kwargs['context_codes'] = context_codes
        else:
            course_ids = [obj_or_id(course_id, 'context_codes', (Course,)) for course_id in context_codes]
            kwargs['context_codes'] = [f'course_{course_id}' for course_id in course_ids]
        return PaginatedList(DiscussionTopic, self.__requester, 'GET', 'announcements', _kwargs=combine_kwargs(**kwargs))

    def get_appointment_group(self, appointment_group: 'AppointmentGroup | int', **kwargs) -> 'AppointmentGroup':
        """
        Return single Appointment Group by id

        Endpoint: GET /api/v1/appointment_groups/:id

        Reference: https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.show

        Parameters:
            appointment_group: :class:`canvasapi.appointment_group.AppointmentGroup` or int
        """
        appointment_group_id = obj_or_id(appointment_group, 'appointment_group', (AppointmentGroup,))
        response: 'httpx.Response' = self.__requester.request('GET', 'appointment_groups/{}'.format(appointment_group_id), _kwargs=combine_kwargs(**kwargs))
        return AppointmentGroup(self.__requester, response.json())

    async def get_appointment_group_async(self, appointment_group: 'AppointmentGroup | int', **kwargs) -> 'AppointmentGroup':
        """
        Return single Appointment Group by id

        Endpoint: GET /api/v1/appointment_groups/:id

        Reference: https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.show

        Parameters:
            appointment_group: :class:`canvasapi.appointment_group.AppointmentGroup` or int
        """
        appointment_group_id = obj_or_id(appointment_group, 'appointment_group', (AppointmentGroup,))
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'appointment_groups/{}'.format(appointment_group_id), _kwargs=combine_kwargs(**kwargs))
        return AppointmentGroup(self.__requester, response.json())

    def get_appointment_groups(self, **kwargs) -> 'PaginatedList[AppointmentGroup]':
        """
        List appointment groups.

        Endpoint: GET /api/v1/appointment_groups

        Reference: https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.index
        """
        return PaginatedList(AppointmentGroup, self.__requester, 'GET', 'appointment_groups', _kwargs=combine_kwargs(**kwargs))

    async def get_appointment_groups_async(self, **kwargs) -> 'PaginatedList[AppointmentGroup]':
        """
        List appointment groups.

        Endpoint: GET /api/v1/appointment_groups

        Reference: https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.index
        """
        return PaginatedList(AppointmentGroup, self.__requester, 'GET', 'appointment_groups', _kwargs=combine_kwargs(**kwargs))

    def get_brand_variables(self, **kwargs) -> 'dict':
        """
        Get account brand variables

        Endpoint: GET /api/v1/brand_variables

        Reference: https://canvas.instructure.com/doc/api/brand_configs.html
        """
        response: 'httpx.Response' = self.__requester.request('GET', 'brand_variables', _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_brand_variables_async(self, **kwargs) -> 'dict':
        """
        Get account brand variables

        Endpoint: GET /api/v1/brand_variables

        Reference: https://canvas.instructure.com/doc/api/brand_configs.html
        """
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'brand_variables', _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_calendar_event(self, calendar_event: 'CalendarEvent | int', **kwargs) -> 'CalendarEvent':
        """
        Return single Calendar Event by id

        Endpoint: GET /api/v1/calendar_events/:id

        Reference: https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.show

        Parameters:
            calendar_event: :class:`canvasapi.calendar_event.CalendarEvent` or int
        """
        calendar_event_id = obj_or_id(calendar_event, 'calendar_event', (CalendarEvent,))
        response: 'httpx.Response' = self.__requester.request('GET', 'calendar_events/{}'.format(calendar_event_id), _kwargs=combine_kwargs(**kwargs))
        return CalendarEvent(self.__requester, response.json())

    async def get_calendar_event_async(self, calendar_event: 'CalendarEvent | int', **kwargs) -> 'CalendarEvent':
        """
        Return single Calendar Event by id

        Endpoint: GET /api/v1/calendar_events/:id

        Reference: https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.show

        Parameters:
            calendar_event: :class:`canvasapi.calendar_event.CalendarEvent` or int
        """
        calendar_event_id = obj_or_id(calendar_event, 'calendar_event', (CalendarEvent,))
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'calendar_events/{}'.format(calendar_event_id), _kwargs=combine_kwargs(**kwargs))
        return CalendarEvent(self.__requester, response.json())

    def get_calendar_events(self, **kwargs) -> 'PaginatedList[CalendarEvent]':
        """
        List calendar events.

        Endpoint: GET /api/v1/calendar_events

        Reference: https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.index
        """
        return PaginatedList(CalendarEvent, self.__requester, 'GET', 'calendar_events', _kwargs=combine_kwargs(**kwargs))

    async def get_calendar_events_async(self, **kwargs) -> 'PaginatedList[CalendarEvent]':
        """
        List calendar events.

        Endpoint: GET /api/v1/calendar_events

        Reference: https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.index
        """
        return PaginatedList(CalendarEvent, self.__requester, 'GET', 'calendar_events', _kwargs=combine_kwargs(**kwargs))

    def get_comm_messages(self, user: 'User | int', **kwargs) -> 'PaginatedList[CommMessage]':
        """
        Retrieve a paginated list of messages sent to a user.

        Endpoint: GET /api/v1/comm_messages

        Reference: https://canvas.instructure.com/doc/api/comm_messages.html#method.comm_messages_api.index

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        kwargs['user_id'] = obj_or_id(user, 'user', (User,))
        return PaginatedList(CommMessage, self.__requester, 'GET', 'comm_messages', _kwargs=combine_kwargs(**kwargs))

    async def get_comm_messages_async(self, user: 'User | int', **kwargs) -> 'PaginatedList[CommMessage]':
        """
        Retrieve a paginated list of messages sent to a user.

        Endpoint: GET /api/v1/comm_messages

        Reference: https://canvas.instructure.com/doc/api/comm_messages.html#method.comm_messages_api.index

        Parameters:
            user: :class:`canvasapi.user.User` or int
        """
        kwargs['user_id'] = obj_or_id(user, 'user', (User,))
        return PaginatedList(CommMessage, self.__requester, 'GET', 'comm_messages', _kwargs=combine_kwargs(**kwargs))

    def get_conversation(self, conversation: 'Conversation | int', **kwargs) -> 'Conversation':
        """
        Return single Conversation

        Endpoint: GET /api/v1/conversations/:id

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.show

        Parameters:
            conversation: :class:`canvasapi.conversation.Conversation` or int
        """
        conversation_id = obj_or_id(conversation, 'conversation', (Conversation,))
        response: 'httpx.Response' = self.__requester.request('GET', 'conversations/{}'.format(conversation_id), _kwargs=combine_kwargs(**kwargs))
        return Conversation(self.__requester, response.json())

    async def get_conversation_async(self, conversation: 'Conversation | int', **kwargs) -> 'Conversation':
        """
        Return single Conversation

        Endpoint: GET /api/v1/conversations/:id

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.show

        Parameters:
            conversation: :class:`canvasapi.conversation.Conversation` or int
        """
        conversation_id = obj_or_id(conversation, 'conversation', (Conversation,))
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'conversations/{}'.format(conversation_id), _kwargs=combine_kwargs(**kwargs))
        return Conversation(self.__requester, response.json())

    def get_conversations(self, **kwargs) -> 'PaginatedList[Conversation]':
        """
        Return list of conversations for the current user, most resent ones first.

        Endpoint: GET /api/v1/conversations

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.index
        """
        return PaginatedList(Conversation, self.__requester, 'GET', 'conversations', _kwargs=combine_kwargs(**kwargs))

    async def get_conversations_async(self, **kwargs) -> 'PaginatedList[Conversation]':
        """
        Return list of conversations for the current user, most resent ones first.

        Endpoint: GET /api/v1/conversations

        Reference: https://canvas.instructure.com/doc/api/conversations.html#method.conversations.index
        """
        return PaginatedList(Conversation, self.__requester, 'GET', 'conversations', _kwargs=combine_kwargs(**kwargs))

    def get_course(self, course: 'int | str | Course', use_sis_id: 'bool'=False, **kwargs) -> 'Course':
        """
        Retrieve a course by its ID.

        Endpoint: GET /api/v1/courses/:id

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.show

        Parameters:
            course: int, str or :class:`canvasapi.course.Course`
            use_sis_id: bool
        """
        if use_sis_id:
            course_id = course
            uri_str = 'courses/sis_course_id:{}'
        else:
            course_id = obj_or_id(course, 'course', (Course,))
            uri_str = 'courses/{}'
        response: 'httpx.Response' = self.__requester.request('GET', uri_str.format(course_id), _kwargs=combine_kwargs(**kwargs))
        return Course(self.__requester, response.json())

    async def get_course_async(self, course: 'int | str | Course', use_sis_id: 'bool'=False, **kwargs) -> 'Course':
        """
        Retrieve a course by its ID.

        Endpoint: GET /api/v1/courses/:id

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.show

        Parameters:
            course: int, str or :class:`canvasapi.course.Course`
            use_sis_id: bool
        """
        if use_sis_id:
            course_id = course
            uri_str = 'courses/sis_course_id:{}'
        else:
            course_id = obj_or_id(course, 'course', (Course,))
            uri_str = 'courses/{}'
        response: 'httpx.Response' = await self.__requester.request_async('GET', uri_str.format(course_id), _kwargs=combine_kwargs(**kwargs))
        return Course(self.__requester, response.json())

    def get_course_accounts(self, **kwargs) -> 'PaginatedList[Account]':
        """
        List accounts that the current user can view through their
        admin course enrollments (Teacher, TA or designer enrollments).
        
        Only returns `id`, `name`, `workflow_state`, `root_account_id`
        and `parent_account_id`.

        Endpoint: GET /api/v1/course_accounts

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.accounts.course_accounts
        """
        return PaginatedList(Account, self.__requester, 'GET', 'course_accounts', _kwargs=combine_kwargs(**kwargs))

    async def get_course_accounts_async(self, **kwargs) -> 'PaginatedList[Account]':
        """
        List accounts that the current user can view through their
        admin course enrollments (Teacher, TA or designer enrollments).
        
        Only returns `id`, `name`, `workflow_state`, `root_account_id`
        and `parent_account_id`.

        Endpoint: GET /api/v1/course_accounts

        Reference: https://canvas.instructure.com/doc/api/accounts.html#method.accounts.course_accounts
        """
        return PaginatedList(Account, self.__requester, 'GET', 'course_accounts', _kwargs=combine_kwargs(**kwargs))

    def get_course_nickname(self, course: 'Course | int', **kwargs) -> 'CourseNickname':
        """
        Return the nickname for the given course.

        Endpoint: GET /api/v1/users/self/course_nicknames/:course_id

        Reference: https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.show

        Parameters:
            course: :class:`canvasapi.course.Course` or int
        """
        course_id = obj_or_id(course, 'course', (Course,))
        response: 'httpx.Response' = self.__requester.request('GET', 'users/self/course_nicknames/{}'.format(course_id), _kwargs=combine_kwargs(**kwargs))
        return CourseNickname(self.__requester, response.json())

    async def get_course_nickname_async(self, course: 'Course | int', **kwargs) -> 'CourseNickname':
        """
        Return the nickname for the given course.

        Endpoint: GET /api/v1/users/self/course_nicknames/:course_id

        Reference: https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.show

        Parameters:
            course: :class:`canvasapi.course.Course` or int
        """
        course_id = obj_or_id(course, 'course', (Course,))
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'users/self/course_nicknames/{}'.format(course_id), _kwargs=combine_kwargs(**kwargs))
        return CourseNickname(self.__requester, response.json())

    def get_course_nicknames(self, **kwargs) -> 'PaginatedList[CourseNickname]':
        """
        Return all course nicknames set by the current account.

        Endpoint: GET /api/v1/users/self/course_nicknames

        Reference: https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.index
        """
        return PaginatedList(CourseNickname, self.__requester, 'GET', 'users/self/course_nicknames', _kwargs=combine_kwargs(**kwargs))

    async def get_course_nicknames_async(self, **kwargs) -> 'PaginatedList[CourseNickname]':
        """
        Return all course nicknames set by the current account.

        Endpoint: GET /api/v1/users/self/course_nicknames

        Reference: https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.index
        """
        return PaginatedList(CourseNickname, self.__requester, 'GET', 'users/self/course_nicknames', _kwargs=combine_kwargs(**kwargs))

    def get_courses(self, **kwargs) -> 'PaginatedList[Course]':
        """
        Return a list of active courses for the current user.

        Endpoint: GET /api/v1/courses

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.index
        """
        return PaginatedList(Course, self.__requester, 'GET', 'courses', _kwargs=combine_kwargs(**kwargs))

    async def get_courses_async(self, **kwargs) -> 'PaginatedList[Course]':
        """
        Return a list of active courses for the current user.

        Endpoint: GET /api/v1/courses

        Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.index
        """
        return PaginatedList(Course, self.__requester, 'GET', 'courses', _kwargs=combine_kwargs(**kwargs))

    def get_current_user(self) -> 'CurrentUser':
        """
        Return a details of the current user.

        Endpoint: GET /api/v1/users/:user_id

        Reference: https://canvas.instructure.com/doc/api/users.html#method.current_user.show
        """
        response: 'httpx.Response' = self.__requester.request('GET', 'users/self')
        return CurrentUser(self.__requester, response.json())

    async def get_current_user_async(self) -> 'CurrentUser':
        """
        Return a details of the current user.

        Endpoint: GET /api/v1/users/:user_id

        Reference: https://canvas.instructure.com/doc/api/users.html#method.current_user.show
        """
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'users/self')
        return CurrentUser(self.__requester, response.json())

    def get_eportfolio(self, eportfolio: 'EPortfolio | int', **kwargs) -> 'EPortfolio':
        """
        Get an eportfolio by ID.

        Endpoint: GET /api/v1/eportfolios/:id`

        Reference: `<https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.show

        Parameters:
            eportfolio: :class: `canvasapi.eportfolio.EPortfolio` or int
        """
        eportfolio_id = obj_or_id(eportfolio, 'eportfolio', (EPortfolio,))
        response: 'httpx.Response' = self.__requester.request('GET', 'eportfolios/{}'.format(eportfolio_id), _kwargs=combine_kwargs(**kwargs))
        return EPortfolio(self.__requester, response.json())

    async def get_eportfolio_async(self, eportfolio: 'EPortfolio | int', **kwargs) -> 'EPortfolio':
        """
        Get an eportfolio by ID.

        Endpoint: GET /api/v1/eportfolios/:id`

        Reference: `<https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.show

        Parameters:
            eportfolio: :class: `canvasapi.eportfolio.EPortfolio` or int
        """
        eportfolio_id = obj_or_id(eportfolio, 'eportfolio', (EPortfolio,))
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'eportfolios/{}'.format(eportfolio_id), _kwargs=combine_kwargs(**kwargs))
        return EPortfolio(self.__requester, response.json())

    def get_epub_exports(self, **kwargs) -> 'PaginatedList[CourseEpubExport]':
        """
        Return a list of epub exports for the associated course.

        Endpoint: GET /api/v1/epub_exports

        Reference: https://canvas.instructure.com/doc/api/e_pub_exports.html#method.epub_exports.index
        """
        return PaginatedList(CourseEpubExport, self.__requester, 'GET', 'epub_exports', _root='courses', kwargs=combine_kwargs(**kwargs))

    async def get_epub_exports_async(self, **kwargs) -> 'PaginatedList[CourseEpubExport]':
        """
        Return a list of epub exports for the associated course.

        Endpoint: GET /api/v1/epub_exports

        Reference: https://canvas.instructure.com/doc/api/e_pub_exports.html#method.epub_exports.index
        """
        return PaginatedList(CourseEpubExport, self.__requester, 'GET', 'epub_exports', _root='courses', kwargs=combine_kwargs(**kwargs))

    def get_file(self, file: 'File | int', **kwargs) -> 'File':
        """
        Return the standard attachment json object for a file.

        Endpoint: GET /api/v1/files/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_show

        Parameters:
            file: :class:`canvasapi.file.File` or int
        """
        file_id = obj_or_id(file, 'file', (File,))
        response: 'httpx.Response' = self.__requester.request('GET', 'files/{}'.format(file_id), _kwargs=combine_kwargs(**kwargs))
        return File(self.__requester, response.json())

    async def get_file_async(self, file: 'File | int', **kwargs) -> 'File':
        """
        Return the standard attachment json object for a file.

        Endpoint: GET /api/v1/files/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.files.api_show

        Parameters:
            file: :class:`canvasapi.file.File` or int
        """
        file_id = obj_or_id(file, 'file', (File,))
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'files/{}'.format(file_id), _kwargs=combine_kwargs(**kwargs))
        return File(self.__requester, response.json())

    def get_folder(self, folder: 'Folder | int', **kwargs) -> 'Folder':
        """
        Return the details for a folder

        Endpoint: GET /api/v1/folders/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.show

        Parameters:
            folder: :class:`canvasapi.folder.Folder` or int
        """
        folder_id = obj_or_id(folder, 'folder', (Folder,))
        response: 'httpx.Response' = self.__requester.request('GET', 'folders/{}'.format(folder_id), _kwargs=combine_kwargs(**kwargs))
        return Folder(self.__requester, response.json())

    async def get_folder_async(self, folder: 'Folder | int', **kwargs) -> 'Folder':
        """
        Return the details for a folder

        Endpoint: GET /api/v1/folders/:id

        Reference: https://canvas.instructure.com/doc/api/files.html#method.folders.show

        Parameters:
            folder: :class:`canvasapi.folder.Folder` or int
        """
        folder_id = obj_or_id(folder, 'folder', (Folder,))
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'folders/{}'.format(folder_id), _kwargs=combine_kwargs(**kwargs))
        return Folder(self.__requester, response.json())

    def get_group(self, group: 'Group | int', use_sis_id: 'bool'=False, **kwargs) -> 'Group':
        """
        Return the data for a single group. If the caller does not
        have permission to view the group a 401 will be returned.

        Endpoint: GET /api/v1/groups/:group_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.show

        Parameters:
            group: :class:`canvasapi.group.Group` or int
            use_sis_id: bool
        """
        if use_sis_id:
            group_id = group
            uri_str = 'groups/sis_group_id:{}'
        else:
            group_id = obj_or_id(group, 'group', (Group,))
            uri_str = 'groups/{}'
        response: 'httpx.Response' = self.__requester.request('GET', uri_str.format(group_id), _kwargs=combine_kwargs(**kwargs))
        return Group(self.__requester, response.json())

    async def get_group_async(self, group: 'Group | int', use_sis_id: 'bool'=False, **kwargs) -> 'Group':
        """
        Return the data for a single group. If the caller does not
        have permission to view the group a 401 will be returned.

        Endpoint: GET /api/v1/groups/:group_id

        Reference: https://canvas.instructure.com/doc/api/groups.html#method.groups.show

        Parameters:
            group: :class:`canvasapi.group.Group` or int
            use_sis_id: bool
        """
        if use_sis_id:
            group_id = group
            uri_str = 'groups/sis_group_id:{}'
        else:
            group_id = obj_or_id(group, 'group', (Group,))
            uri_str = 'groups/{}'
        response: 'httpx.Response' = await self.__requester.request_async('GET', uri_str.format(group_id), _kwargs=combine_kwargs(**kwargs))
        return Group(self.__requester, response.json())

    def get_group_category(self, category: 'GroupCategory | int', **kwargs) -> 'GroupCategory':
        """
        Get a single group category.

        Endpoint: GET /api/v1/group_categories/:group_category_id

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.show

        Parameters:
            category: :class:`canvasapi.group.GroupCategory` or int
        """
        category_id = obj_or_id(category, 'category', (GroupCategory,))
        response: 'httpx.Response' = self.__requester.request('GET', 'group_categories/{}'.format(category_id), _kwargs=combine_kwargs(**kwargs))
        return GroupCategory(self.__requester, response.json())

    async def get_group_category_async(self, category: 'GroupCategory | int', **kwargs) -> 'GroupCategory':
        """
        Get a single group category.

        Endpoint: GET /api/v1/group_categories/:group_category_id

        Reference: https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.show

        Parameters:
            category: :class:`canvasapi.group.GroupCategory` or int
        """
        category_id = obj_or_id(category, 'category', (GroupCategory,))
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'group_categories/{}'.format(category_id), _kwargs=combine_kwargs(**kwargs))
        return GroupCategory(self.__requester, response.json())

    def get_group_participants(self, appointment_group: 'AppointmentGroup | int', **kwargs) -> 'PaginatedList[Group]':
        """
        List student group participants in this appointment group.

        Endpoint: GET /api/v1/appointment_groups/:id/groups

        Reference: https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.groups

        Parameters:
            appointment_group: :class:`canvasapi.appointment_group.AppointmentGroup` or int
        """
        appointment_group_id = obj_or_id(appointment_group, 'appointment_group', (AppointmentGroup,))
        return PaginatedList(Group, self.__requester, 'GET', 'appointment_groups/{}/groups'.format(appointment_group_id), _kwargs=combine_kwargs(**kwargs))

    async def get_group_participants_async(self, appointment_group: 'AppointmentGroup | int', **kwargs) -> 'PaginatedList[Group]':
        """
        List student group participants in this appointment group.

        Endpoint: GET /api/v1/appointment_groups/:id/groups

        Reference: https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.groups

        Parameters:
            appointment_group: :class:`canvasapi.appointment_group.AppointmentGroup` or int
        """
        appointment_group_id = obj_or_id(appointment_group, 'appointment_group', (AppointmentGroup,))
        return PaginatedList(Group, self.__requester, 'GET', 'appointment_groups/{}/groups'.format(appointment_group_id), _kwargs=combine_kwargs(**kwargs))

    def get_outcome(self, outcome: 'Outcome | int', **kwargs) -> 'Outcome':
        """
        Returns the details of the outcome with the given id.

        Endpoint: GET /api/v1/outcomes/:id

        Reference: https://canvas.instructure.com/doc/api/outcomes.html#method.outcomes_api.show

        Parameters:
            outcome: :class:`canvasapi.outcome.Outcome` or int
        """
        outcome_id = obj_or_id(outcome, 'outcome', (Outcome,))
        response: 'httpx.Response' = self.__requester.request('GET', 'outcomes/{}'.format(outcome_id), _kwargs=combine_kwargs(**kwargs))
        return Outcome(self.__requester, response.json())

    async def get_outcome_async(self, outcome: 'Outcome | int', **kwargs) -> 'Outcome':
        """
        Returns the details of the outcome with the given id.

        Endpoint: GET /api/v1/outcomes/:id

        Reference: https://canvas.instructure.com/doc/api/outcomes.html#method.outcomes_api.show

        Parameters:
            outcome: :class:`canvasapi.outcome.Outcome` or int
        """
        outcome_id = obj_or_id(outcome, 'outcome', (Outcome,))
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'outcomes/{}'.format(outcome_id), _kwargs=combine_kwargs(**kwargs))
        return Outcome(self.__requester, response.json())

    def get_outcome_group(self, group: 'OutcomeGroup | int', **kwargs) -> 'OutcomeGroup':
        """
        Returns the details of the Outcome Group with the given id.

        Endpoint: GET /api/v1/global/outcome_groups/:id

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show

        Parameters:
            group: :class:`canvasapi.outcome.OutcomeGroup` or int
        """
        outcome_group_id = obj_or_id(group, 'group', (OutcomeGroup,))
        response: 'httpx.Response' = self.__requester.request('GET', 'global/outcome_groups/{}'.format(outcome_group_id), _kwargs=combine_kwargs(**kwargs))
        return OutcomeGroup(self.__requester, response.json())

    async def get_outcome_group_async(self, group: 'OutcomeGroup | int', **kwargs) -> 'OutcomeGroup':
        """
        Returns the details of the Outcome Group with the given id.

        Endpoint: GET /api/v1/global/outcome_groups/:id

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show

        Parameters:
            group: :class:`canvasapi.outcome.OutcomeGroup` or int
        """
        outcome_group_id = obj_or_id(group, 'group', (OutcomeGroup,))
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'global/outcome_groups/{}'.format(outcome_group_id), _kwargs=combine_kwargs(**kwargs))
        return OutcomeGroup(self.__requester, response.json())

    def get_planner_note(self, planner_note: 'int | PlannerNote', **kwargs) -> 'PlannerNote':
        """
        Retrieve a planner note for the current user

        Endpoint: GET /api/v1/planner_notes/:id

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_notes.show

        Parameters:
            planner_note: int or :class:`canvasapi.planner.PlannerNote`
        """
        if isinstance(planner_note, int) or isinstance(planner_note, PlannerNote):
            planner_note_id = obj_or_id(planner_note, 'planner_note', (PlannerNote,))
        else:
            raise RequiredFieldMissing('planner_note is required as an object or as an int.')
        response: 'httpx.Response' = self.__requester.request('GET', 'planner_notes/{}'.format(planner_note_id), _kwargs=combine_kwargs(**kwargs))
        return PlannerNote(self.__requester, response.json())

    async def get_planner_note_async(self, planner_note: 'int | PlannerNote', **kwargs) -> 'PlannerNote':
        """
        Retrieve a planner note for the current user

        Endpoint: GET /api/v1/planner_notes/:id

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_notes.show

        Parameters:
            planner_note: int or :class:`canvasapi.planner.PlannerNote`
        """
        if isinstance(planner_note, int) or isinstance(planner_note, PlannerNote):
            planner_note_id = obj_or_id(planner_note, 'planner_note', (PlannerNote,))
        else:
            raise RequiredFieldMissing('planner_note is required as an object or as an int.')
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'planner_notes/{}'.format(planner_note_id), _kwargs=combine_kwargs(**kwargs))
        return PlannerNote(self.__requester, response.json())

    def get_planner_notes(self, **kwargs) -> 'PaginatedList[PlannerNote]':
        """
        Retrieve the paginated list of planner notes

        Endpoint: GET /api/v1/planner_notes

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_notes.index
        """
        return PaginatedList(PlannerNote, self.__requester, 'GET', 'planner_notes', _kwargs=combine_kwargs(**kwargs))

    async def get_planner_notes_async(self, **kwargs) -> 'PaginatedList[PlannerNote]':
        """
        Retrieve the paginated list of planner notes

        Endpoint: GET /api/v1/planner_notes

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_notes.index
        """
        return PaginatedList(PlannerNote, self.__requester, 'GET', 'planner_notes', _kwargs=combine_kwargs(**kwargs))

    def get_planner_override(self, planner_override: 'int | PlannerOverride', **kwargs) -> 'PlannerOverride':
        """
        Retrieve a planner override for the current user

        Endpoint: GET /api/v1/planner/overrides/:id

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_overrides.show

        Parameters:
            planner_override: int or :class:`canvasapi.planner.PlannerOverride`
        """
        if isinstance(planner_override, int) or isinstance(planner_override, PlannerOverride):
            planner_override_id = obj_or_id(planner_override, 'planner_override', (PlannerOverride,))
        else:
            raise RequiredFieldMissing('planner_override is required as an object or as an int.')
        response: 'httpx.Response' = self.__requester.request('GET', 'planner/overrides/{}'.format(planner_override_id), _kwargs=combine_kwargs(**kwargs))
        return PlannerOverride(self.__requester, response.json())

    async def get_planner_override_async(self, planner_override: 'int | PlannerOverride', **kwargs) -> 'PlannerOverride':
        """
        Retrieve a planner override for the current user

        Endpoint: GET /api/v1/planner/overrides/:id

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_overrides.show

        Parameters:
            planner_override: int or :class:`canvasapi.planner.PlannerOverride`
        """
        if isinstance(planner_override, int) or isinstance(planner_override, PlannerOverride):
            planner_override_id = obj_or_id(planner_override, 'planner_override', (PlannerOverride,))
        else:
            raise RequiredFieldMissing('planner_override is required as an object or as an int.')
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'planner/overrides/{}'.format(planner_override_id), _kwargs=combine_kwargs(**kwargs))
        return PlannerOverride(self.__requester, response.json())

    def get_planner_overrides(self, **kwargs) -> 'PaginatedList[PlannerOverride]':
        """
        Retrieve a planner override for the current user

        Endpoint: GET /api/v1/planner/overrides

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_overrides.index
        """
        return PaginatedList(PlannerOverride, self.__requester, 'GET', 'planner/overrides', _kwargs=combine_kwargs(**kwargs))

    async def get_planner_overrides_async(self, **kwargs) -> 'PaginatedList[PlannerOverride]':
        """
        Retrieve a planner override for the current user

        Endpoint: GET /api/v1/planner/overrides

        Reference: https://canvas.instructure.com/doc/api/planner.html#method.planner_overrides.index
        """
        return PaginatedList(PlannerOverride, self.__requester, 'GET', 'planner/overrides', _kwargs=combine_kwargs(**kwargs))

    def get_poll(self, poll: 'int', **kwargs) -> 'Poll':
        """
        Get a single poll, based on the poll id.

        Endpoint: GET /api/v1/polls/:id

        Reference: https://canvas.instructure.com/doc/api/polls.html#method.polling/polls.show

        Parameters:
            poll: int
        """
        poll_id = obj_or_id(poll, 'poll', (Poll,))
        response: 'httpx.Response' = self.__requester.request('GET', 'polls/{}'.format(poll_id), _kwargs=combine_kwargs(**kwargs))
        return Poll(self.__requester, response.json()['polls'][0])

    async def get_poll_async(self, poll: 'int', **kwargs) -> 'Poll':
        """
        Get a single poll, based on the poll id.

        Endpoint: GET /api/v1/polls/:id

        Reference: https://canvas.instructure.com/doc/api/polls.html#method.polling/polls.show

        Parameters:
            poll: int
        """
        poll_id = obj_or_id(poll, 'poll', (Poll,))
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'polls/{}'.format(poll_id), _kwargs=combine_kwargs(**kwargs))
        return Poll(self.__requester, response.json()['polls'][0])

    def get_polls(self, **kwargs) -> 'PaginatedList[Poll]':
        """
        Returns a paginated list of polls for the current user

        Endpoint: GET /api/1/polls

        Reference: https://canvas.instructure.com/doc/api/polls.html#method.polling/polls.index
        """
        return PaginatedList(Poll, self.__requester, 'GET', 'polls', _root='polls', _kwargs=combine_kwargs(**kwargs))

    async def get_polls_async(self, **kwargs) -> 'PaginatedList[Poll]':
        """
        Returns a paginated list of polls for the current user

        Endpoint: GET /api/1/polls

        Reference: https://canvas.instructure.com/doc/api/polls.html#method.polling/polls.index
        """
        return PaginatedList(Poll, self.__requester, 'GET', 'polls', _root='polls', _kwargs=combine_kwargs(**kwargs))

    def get_progress(self, progress: 'int | str | Progress', **kwargs) -> 'Progress':
        """
        Get a specific progress.

        Endpoint: GET /api/v1/progress/:id

        Reference: https://canvas.instructure.com/doc/api/progress.html#method.progress.show

        Parameters:
            progress: int, str or :class:`canvasapi.progress.Progress`
        """
        progress_id = obj_or_id(progress, 'progress', (Progress,))
        response: 'httpx.Response' = self.__requester.request('GET', 'progress/{}'.format(progress_id), _kwargs=combine_kwargs(**kwargs))
        return Progress(self.__requester, response.json())

    async def get_progress_async(self, progress: 'int | str | Progress', **kwargs) -> 'Progress':
        """
        Get a specific progress.

        Endpoint: GET /api/v1/progress/:id

        Reference: https://canvas.instructure.com/doc/api/progress.html#method.progress.show

        Parameters:
            progress: int, str or :class:`canvasapi.progress.Progress`
        """
        progress_id = obj_or_id(progress, 'progress', (Progress,))
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'progress/{}'.format(progress_id), _kwargs=combine_kwargs(**kwargs))
        return Progress(self.__requester, response.json())

    def get_root_outcome_group(self, **kwargs) -> 'OutcomeGroup':
        """
        Redirect to root outcome group for context

        Endpoint: GET /api/v1/global/root_outcome_group

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.redirect
        """
        response: 'httpx.Response' = self.__requester.request('GET', 'global/root_outcome_group', _kwargs=combine_kwargs(**kwargs))
        return OutcomeGroup(self.__requester, response.json())

    async def get_root_outcome_group_async(self, **kwargs) -> 'OutcomeGroup':
        """
        Redirect to root outcome group for context

        Endpoint: GET /api/v1/global/root_outcome_group

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.redirect
        """
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'global/root_outcome_group', _kwargs=combine_kwargs(**kwargs))
        return OutcomeGroup(self.__requester, response.json())

    def get_section(self, section: 'Section | int', use_sis_id: 'bool'=False, **kwargs) -> 'Section':
        """
        Get details about a specific section.

        Endpoint: GET /api/v1/sections/:id

        Reference: https://canvas.instructure.com/doc/api/sections.html#method.sections.show

        Parameters:
            section: :class:`canvasapi.section.Section` or int
            use_sis_id: bool
        """
        if use_sis_id:
            section_id = section
            uri_str = 'sections/sis_section_id:{}'
        else:
            section_id = obj_or_id(section, 'section', (Section,))
            uri_str = 'sections/{}'
        response: 'httpx.Response' = self.__requester.request('GET', uri_str.format(section_id), _kwargs=combine_kwargs(**kwargs))
        return Section(self.__requester, response.json())

    async def get_section_async(self, section: 'Section | int', use_sis_id: 'bool'=False, **kwargs) -> 'Section':
        """
        Get details about a specific section.

        Endpoint: GET /api/v1/sections/:id

        Reference: https://canvas.instructure.com/doc/api/sections.html#method.sections.show

        Parameters:
            section: :class:`canvasapi.section.Section` or int
            use_sis_id: bool
        """
        if use_sis_id:
            section_id = section
            uri_str = 'sections/sis_section_id:{}'
        else:
            section_id = obj_or_id(section, 'section', (Section,))
            uri_str = 'sections/{}'
        response: 'httpx.Response' = await self.__requester.request_async('GET', uri_str.format(section_id), _kwargs=combine_kwargs(**kwargs))
        return Section(self.__requester, response.json())

    def get_todo_items(self, **kwargs) -> 'dict':
        """
        Return the current user's list of todo items, as seen on the user dashboard.

        Endpoint: GET /api/v1/users/self/todo

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.todo_items
        """
        return PaginatedList(Todo, self.__requester, 'GET', 'users/self/todo', _kwargs=combine_kwargs(**kwargs))

    async def get_todo_items_async(self, **kwargs) -> 'dict':
        """
        Return the current user's list of todo items, as seen on the user dashboard.

        Endpoint: GET /api/v1/users/self/todo

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.todo_items
        """
        return PaginatedList(Todo, self.__requester, 'GET', 'users/self/todo', _kwargs=combine_kwargs(**kwargs))

    def get_upcoming_events(self, **kwargs) -> 'dict':
        """
        Return the current user's upcoming events, i.e. the same things shown
        in the dashboard 'Coming Up' sidebar.

        Endpoint: GET /api/v1/users/self/upcoming_events

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.upcoming_events
        """
        response: 'httpx.Response' = self.__requester.request('GET', 'users/self/upcoming_events', _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_upcoming_events_async(self, **kwargs) -> 'dict':
        """
        Return the current user's upcoming events, i.e. the same things shown
        in the dashboard 'Coming Up' sidebar.

        Endpoint: GET /api/v1/users/self/upcoming_events

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.upcoming_events
        """
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'users/self/upcoming_events', _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_user(self, user: 'User | int', id_type: 'str | None'=None, **kwargs) -> 'User':
        """
        Retrieve a user by their ID. `id_type` denotes which endpoint to try as there are
        several different IDs that can pull the same user record from Canvas.
        
        Refer to API documentation's
        `User <https://canvas.instructure.com/doc/api/users.html#User>`_
        example to see the ID types a user can be retrieved with.

        Endpoint: GET /api/v1/users/:id

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.api_show

        Parameters:
            user: :class:`canvasapi.user.User` or int
            id_type: str
        """
        if id_type:
            uri = 'users/{}:{}'.format(id_type, user)
        elif user == 'self':
            uri = 'users/self'
        else:
            user_id = obj_or_id(user, 'user', (User,))
            uri = 'users/{}'.format(user_id)
        response: 'httpx.Response' = self.__requester.request('GET', uri, _kwargs=combine_kwargs(**kwargs))
        return User(self.__requester, response.json())

    async def get_user_async(self, user: 'User | int', id_type: 'str | None'=None, **kwargs) -> 'User':
        """
        Retrieve a user by their ID. `id_type` denotes which endpoint to try as there are
        several different IDs that can pull the same user record from Canvas.
        
        Refer to API documentation's
        `User <https://canvas.instructure.com/doc/api/users.html#User>`_
        example to see the ID types a user can be retrieved with.

        Endpoint: GET /api/v1/users/:id

        Reference: https://canvas.instructure.com/doc/api/users.html#method.users.api_show

        Parameters:
            user: :class:`canvasapi.user.User` or int
            id_type: str
        """
        if id_type:
            uri = 'users/{}:{}'.format(id_type, user)
        elif user == 'self':
            uri = 'users/self'
        else:
            user_id = obj_or_id(user, 'user', (User,))
            uri = 'users/{}'.format(user_id)
        response: 'httpx.Response' = await self.__requester.request_async('GET', uri, _kwargs=combine_kwargs(**kwargs))
        return User(self.__requester, response.json())

    def get_user_participants(self, appointment_group: 'AppointmentGroup | int', **kwargs) -> 'PaginatedList[User]':
        """
        List user participants in this appointment group.

        Endpoint: GET /api/v1/appointment_groups/:id/users

        Reference: https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.users

        Parameters:
            appointment_group: :class:`canvasapi.appointment_group.AppointmentGroup` or int
        """
        appointment_group_id = obj_or_id(appointment_group, 'appointment_group', (AppointmentGroup,))
        return PaginatedList(User, self.__requester, 'GET', 'appointment_groups/{}/users'.format(appointment_group_id), _kwargs=combine_kwargs(**kwargs))

    async def get_user_participants_async(self, appointment_group: 'AppointmentGroup | int', **kwargs) -> 'PaginatedList[User]':
        """
        List user participants in this appointment group.

        Endpoint: GET /api/v1/appointment_groups/:id/users

        Reference: https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.users

        Parameters:
            appointment_group: :class:`canvasapi.appointment_group.AppointmentGroup` or int
        """
        appointment_group_id = obj_or_id(appointment_group, 'appointment_group', (AppointmentGroup,))
        return PaginatedList(User, self.__requester, 'GET', 'appointment_groups/{}/users'.format(appointment_group_id), _kwargs=combine_kwargs(**kwargs))

    def graphql(self, query: 'str', variables: 'dict | None'=None, **kwargs) -> 'dict':
        """
        Makes a GraphQL formatted request to Canvas

        Endpoint: POST /api/graphql

        Reference: https://canvas.instructure.com/doc/api/file.graphql.html

        Parameters:
            query: str
            variables: dict
        """
        response: 'httpx.Response' = self.__requester.request('POST', 'graphql', headers={'Content-Type': 'application/json'}, _kwargs=combine_kwargs(**kwargs) + [('query', query), ('variables', variables)], _url='graphql', json=True)
        return response.json()

    async def graphql_async(self, query: 'str', variables: 'dict | None'=None, **kwargs) -> 'dict':
        """
        Makes a GraphQL formatted request to Canvas

        Endpoint: POST /api/graphql

        Reference: https://canvas.instructure.com/doc/api/file.graphql.html

        Parameters:
            query: str
            variables: dict
        """
        response: 'httpx.Response' = await self.__requester.request_async('POST', 'graphql', headers={'Content-Type': 'application/json'}, _kwargs=combine_kwargs(**kwargs) + [('query', query), ('variables', variables)], _url='graphql', json=True)
        return response.json()

    def refresh_jwt(self, jwt: 'str | JWT', **kwargs) -> 'JWT':
        """
        Refreshes a JWT for reuse with other canvas services. It generates a
        different JWT each time it's called; expires after one hour.

        Endpoint: POST /api/v1/jwts/refresh

        Reference: https://canvas.instructure.com/doc/api/jw_ts.html#method.jwts.refresh

        Parameters:
            jwt: str or :class:`canvasapi.jwt.JWT`
        """
        if isinstance(jwt, JWT):
            jwt = jwt.token
        response: 'httpx.Response' = self.__requester.request('POST', 'jwts/refresh', jwt=jwt, _kwargs=combine_kwargs(**kwargs))
        return JWT(self.__requester, response.json())

    async def refresh_jwt_async(self, jwt: 'str | JWT', **kwargs) -> 'JWT':
        """
        Refreshes a JWT for reuse with other canvas services. It generates a
        different JWT each time it's called; expires after one hour.

        Endpoint: POST /api/v1/jwts/refresh

        Reference: https://canvas.instructure.com/doc/api/jw_ts.html#method.jwts.refresh

        Parameters:
            jwt: str or :class:`canvasapi.jwt.JWT`
        """
        if isinstance(jwt, JWT):
            jwt = jwt.token
        response: 'httpx.Response' = await self.__requester.request_async('POST', 'jwts/refresh', jwt=jwt, _kwargs=combine_kwargs(**kwargs))
        return JWT(self.__requester, response.json())

    def reserve_time_slot(self, calendar_event: 'CalendarEvent | int', participant_id: 'str | None'=None, **kwargs) -> 'CalendarEvent':
        """
        Return single Calendar Event by id

        Endpoint: POST /api/v1/calendar_events/:id/reservations

        Reference: https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.reserve

        Parameters:
            calendar_event: :class:`canvasapi.calendar_event.CalendarEvent` or int
            participant_id: str
        """
        calendar_event_id = obj_or_id(calendar_event, 'calendar_event', (CalendarEvent,))
        if participant_id:
            uri = 'calendar_events/{}/reservations/{}'.format(calendar_event_id, participant_id)
        else:
            uri = 'calendar_events/{}/reservations'.format(calendar_event_id)
        response: 'httpx.Response' = self.__requester.request('POST', uri, _kwargs=combine_kwargs(**kwargs))
        return CalendarEvent(self.__requester, response.json())

    async def reserve_time_slot_async(self, calendar_event: 'CalendarEvent | int', participant_id: 'str | None'=None, **kwargs) -> 'CalendarEvent':
        """
        Return single Calendar Event by id

        Endpoint: POST /api/v1/calendar_events/:id/reservations

        Reference: https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.reserve

        Parameters:
            calendar_event: :class:`canvasapi.calendar_event.CalendarEvent` or int
            participant_id: str
        """
        calendar_event_id = obj_or_id(calendar_event, 'calendar_event', (CalendarEvent,))
        if participant_id:
            uri = 'calendar_events/{}/reservations/{}'.format(calendar_event_id, participant_id)
        else:
            uri = 'calendar_events/{}/reservations'.format(calendar_event_id)
        response: 'httpx.Response' = await self.__requester.request_async('POST', uri, _kwargs=combine_kwargs(**kwargs))
        return CalendarEvent(self.__requester, response.json())

    def search_accounts(self, **kwargs) -> 'dict':
        """
        Return a list of up to 5 matching account domains. Partial matches on
        name and domain are supported.

        Endpoint: GET /api/v1/accounts/search

        Reference: https://canvas.instructure.com/doc/api/account_domain_lookups.html#method.account_domain_lookups.search
        """
        response: 'httpx.Response' = self.__requester.request('GET', 'accounts/search', _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def search_accounts_async(self, **kwargs) -> 'dict':
        """
        Return a list of up to 5 matching account domains. Partial matches on
        name and domain are supported.

        Endpoint: GET /api/v1/accounts/search

        Reference: https://canvas.instructure.com/doc/api/account_domain_lookups.html#method.account_domain_lookups.search
        """
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'accounts/search', _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def search_all_courses(self, **kwargs) -> 'list':
        """
        List all the courses visible in the public index.
        Returns a list of dicts, each containing a single course.

        Endpoint: GET /api/v1/search/all_courses

        Reference: https://canvas.instructure.com/doc/api/search.html#method.search.all_courses
        """
        response: 'httpx.Response' = self.__requester.request('GET', 'search/all_courses', _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def search_all_courses_async(self, **kwargs) -> 'list':
        """
        List all the courses visible in the public index.
        Returns a list of dicts, each containing a single course.

        Endpoint: GET /api/v1/search/all_courses

        Reference: https://canvas.instructure.com/doc/api/search.html#method.search.all_courses
        """
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'search/all_courses', _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def search_recipients(self, **kwargs) -> 'list':
        """
        Find valid recipients (users, courses and groups) that the current user
        can send messages to.
        Returns a list of mixed data types.

        Endpoint: GET /api/v1/search/recipients

        Reference: https://canvas.instructure.com/doc/api/search.html#method.search.recipients
        """
        if 'search' not in kwargs:
            kwargs['search'] = ' '
        response: 'httpx.Response' = self.__requester.request('GET', 'search/recipients', _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def search_recipients_async(self, **kwargs) -> 'list':
        """
        Find valid recipients (users, courses and groups) that the current user
        can send messages to.
        Returns a list of mixed data types.

        Endpoint: GET /api/v1/search/recipients

        Reference: https://canvas.instructure.com/doc/api/search.html#method.search.recipients
        """
        if 'search' not in kwargs:
            kwargs['search'] = ' '
        response: 'httpx.Response' = await self.__requester.request_async('GET', 'search/recipients', _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def set_course_nickname(self, course: 'Course | int', nickname: 'str', **kwargs) -> 'CourseNickname':
        """
        Set a nickname for the given course. This will replace the
        course's name in the output of subsequent API calls, as
        well as in selected places in the Canvas web user interface.

        Endpoint: PUT /api/v1/users/self/course_nicknames/:course_id

        Reference: https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.update

        Parameters:
            course: :class:`canvasapi.course.Course` or int
            nickname: str
        """
        course_id = obj_or_id(course, 'course', (Course,))
        kwargs['nickname'] = nickname
        response: 'httpx.Response' = self.__requester.request('PUT', 'users/self/course_nicknames/{}'.format(course_id), _kwargs=combine_kwargs(**kwargs))
        return CourseNickname(self.__requester, response.json())

    async def set_course_nickname_async(self, course: 'Course | int', nickname: 'str', **kwargs) -> 'CourseNickname':
        """
        Set a nickname for the given course. This will replace the
        course's name in the output of subsequent API calls, as
        well as in selected places in the Canvas web user interface.

        Endpoint: PUT /api/v1/users/self/course_nicknames/:course_id

        Reference: https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.update

        Parameters:
            course: :class:`canvasapi.course.Course` or int
            nickname: str
        """
        course_id = obj_or_id(course, 'course', (Course,))
        kwargs['nickname'] = nickname
        response: 'httpx.Response' = await self.__requester.request_async('PUT', 'users/self/course_nicknames/{}'.format(course_id), _kwargs=combine_kwargs(**kwargs))
        return CourseNickname(self.__requester, response.json())