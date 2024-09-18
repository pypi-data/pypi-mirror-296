from ..models.discussion_topics import DiscussionTopic as DiscussionTopicModel
import httpx
import typing
if typing.TYPE_CHECKING:
    from .course import Course
    from .group import Group
    from .paginated_list import PaginatedList
from .canvas_object import CanvasObject
from .paginated_list import PaginatedList
from .util import combine_kwargs, obj_or_id

class DiscussionTopic(DiscussionTopicModel):

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)

    @property
    def _parent_id(self) -> 'int':
        """
        Return the id of the course or group that spawned this discussion topic.
        """
        if hasattr(self, 'course_id'):
            return self.course_id
        elif hasattr(self, 'group_id'):
            return self.group_id
        elif hasattr(self, 'context_code'):
            if self.context_code.startswith('course_'):
                self.course_id = self.context_code.split('_')[1]
                return self.course_id
            elif self.context_code.startswith('group_'):
                self.group_id = self.context_code.split('_')[1]
                return self.group_id
        else:
            raise ValueError('Discussion Topic does not have a course_id or group_id')

    @property
    def _parent_type(self) -> 'str':
        """
        Return whether the discussion topic was spawned from a course or group.
        """
        if hasattr(self, 'course_id'):
            return 'course'
        elif hasattr(self, 'group_id'):
            return 'group'
        elif hasattr(self, 'context_code'):
            if self.context_code.startswith('course'):
                return 'course'
            elif self.context_code.startswith('group'):
                return 'group'
        else:
            raise ValueError('Discussion Topic does not have a course_id or group_id')

    def delete(self, **kwargs) -> 'bool':
        """
        Deletes the discussion topic. This will also delete the assignment.

        Endpoint: DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', '{}s/{}/discussion_topics/{}'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return 'deleted_at' in response.json()

    async def delete_async(self, **kwargs) -> 'bool':
        """
        Deletes the discussion topic. This will also delete the assignment.

        Endpoint: DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', '{}s/{}/discussion_topics/{}'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return 'deleted_at' in response.json()

    def get_entries(self, ids: 'DiscussionEntry | list | tuple[int]', **kwargs) -> 'PaginatedList[DiscussionEntry]':
        """
        Retrieve a paginated list of discussion entries, given a list
        of ids. Entries will be returned in id order, smallest id first.

        Endpoint: GET /api/v1/courses/:course_id/discussion_topics/:topic_id/entry_list

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.entry_list

        Parameters:
            ids: :class:`canvasapi.discussion_topic.DiscussionEntry`, or list or tuple of int
        """
        entry_ids = [obj_or_id(item, 'ids', (DiscussionEntry,)) for item in ids]
        kwargs.update(ids=entry_ids)
        return PaginatedList(DiscussionEntry, self._requester, 'GET', '{}s/{}/discussion_topics/{}/entry_list'.format(self._parent_type, self._parent_id, self.id), {'discussion_id': self.id, '{}_id'.format(self._parent_type): self._parent_id}, _kwargs=combine_kwargs(**kwargs))

    async def get_entries_async(self, ids: 'DiscussionEntry | list | tuple[int]', **kwargs) -> 'PaginatedList[DiscussionEntry]':
        """
        Retrieve a paginated list of discussion entries, given a list
        of ids. Entries will be returned in id order, smallest id first.

        Endpoint: GET /api/v1/courses/:course_id/discussion_topics/:topic_id/entry_list

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.entry_list

        Parameters:
            ids: :class:`canvasapi.discussion_topic.DiscussionEntry`, or list or tuple of int
        """
        entry_ids = [obj_or_id(item, 'ids', (DiscussionEntry,)) for item in ids]
        kwargs.update(ids=entry_ids)
        return PaginatedList(DiscussionEntry, self._requester, 'GET', '{}s/{}/discussion_topics/{}/entry_list'.format(self._parent_type, self._parent_id, self.id), {'discussion_id': self.id, '{}_id'.format(self._parent_type): self._parent_id}, _kwargs=combine_kwargs(**kwargs))

    def get_parent(self, **kwargs) -> 'Group | Course':
        """
        Return the object that spawned this discussion topic.
        """
        from .course import Course
        from .group import Group
        response: 'httpx.Response' = self._requester.request('GET', '{}s/{}'.format(self._parent_type, self._parent_id), _kwargs=combine_kwargs(**kwargs))
        if self._parent_type == 'group':
            return Group(self._requester, response.json())
        elif self._parent_type == 'course':
            return Course(self._requester, response.json())

    async def get_parent_async(self, **kwargs) -> 'Group | Course':
        """
        Return the object that spawned this discussion topic.
        """
        from .course import Course
        from .group import Group
        response: 'httpx.Response' = await self._requester.request_async('GET', '{}s/{}'.format(self._parent_type, self._parent_id), _kwargs=combine_kwargs(**kwargs))
        if self._parent_type == 'group':
            return Group(self._requester, response.json())
        elif self._parent_type == 'course':
            return Course(self._requester, response.json())

    def get_topic_entries(self, **kwargs) -> 'PaginatedList[DiscussionEntry]':
        """
        Retreive the top-level entries in a discussion topic.

        Endpoint: GET /api/v1/courses/:course_id/discussion_topics/:topic_id/entries

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.entries
        """
        return PaginatedList(DiscussionEntry, self._requester, 'GET', '{}s/{}/discussion_topics/{}/entries'.format(self._parent_type, self._parent_id, self.id), {'discussion_id': self.id, '{}_id'.format(self._parent_type): self._parent_id}, _kwargs=combine_kwargs(**kwargs))

    async def get_topic_entries_async(self, **kwargs) -> 'PaginatedList[DiscussionEntry]':
        """
        Retreive the top-level entries in a discussion topic.

        Endpoint: GET /api/v1/courses/:course_id/discussion_topics/:topic_id/entries

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.entries
        """
        return PaginatedList(DiscussionEntry, self._requester, 'GET', '{}s/{}/discussion_topics/{}/entries'.format(self._parent_type, self._parent_id, self.id), {'discussion_id': self.id, '{}_id'.format(self._parent_type): self._parent_id}, _kwargs=combine_kwargs(**kwargs))

    def mark_as_read(self, **kwargs) -> 'bool':
        """
        Mark the initial text of the discussion topic as read.

        Endpoint: PUT /api/v1/courses/:course_id/discussion_topics/:topic_id/read

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_topic_read
        """
        response: 'httpx.Response' = self._requester.request('PUT', '{}s/{}/discussion_topics/{}/read'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    async def mark_as_read_async(self, **kwargs) -> 'bool':
        """
        Mark the initial text of the discussion topic as read.

        Endpoint: PUT /api/v1/courses/:course_id/discussion_topics/:topic_id/read

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_topic_read
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', '{}s/{}/discussion_topics/{}/read'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    def mark_as_unread(self, **kwargs) -> 'bool':
        """
        Mark the initial text of the discussion topic as unread.

        Endpoint: DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id/read

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_topic_unread
        """
        response: 'httpx.Response' = self._requester.request('DELETE', '{}s/{}/discussion_topics/{}/read'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    async def mark_as_unread_async(self, **kwargs) -> 'bool':
        """
        Mark the initial text of the discussion topic as unread.

        Endpoint: DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id/read

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_topic_unread
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', '{}s/{}/discussion_topics/{}/read'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    def mark_entries_as_read(self, **kwargs) -> 'bool':
        """
        Mark the discussion topic and all its entries as read.

        Endpoint: PUT /api/v1/courses/:course_id/discussion_topics/:topic_id/read_all

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_all_read
        """
        response: 'httpx.Response' = self._requester.request('PUT', '{}s/{}/discussion_topics/{}/read_all'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    async def mark_entries_as_read_async(self, **kwargs) -> 'bool':
        """
        Mark the discussion topic and all its entries as read.

        Endpoint: PUT /api/v1/courses/:course_id/discussion_topics/:topic_id/read_all

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_all_read
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', '{}s/{}/discussion_topics/{}/read_all'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    def mark_entries_as_unread(self, **kwargs) -> 'bool':
        """
        Mark the discussion topic and all its entries as unread.

        Endpoint: DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id/read_all

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_all_unread
        """
        response: 'httpx.Response' = self._requester.request('DELETE', '{}s/{}/discussion_topics/{}/read_all'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    async def mark_entries_as_unread_async(self, **kwargs) -> 'bool':
        """
        Mark the discussion topic and all its entries as unread.

        Endpoint: DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id/read_all

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_all_unread
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', '{}s/{}/discussion_topics/{}/read_all'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    def post_entry(self, **kwargs) -> 'DiscussionEntry':
        """
        Creates a new entry in a discussion topic.

        Endpoint: POST /api/v1/courses/:course_id/discussion_topics/:topic_id/entries

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.add_entry
        """
        response: 'httpx.Response' = self._requester.request('POST', '{}s/{}/discussion_topics/{}/entries'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'discussion_id': self.id, '{}_id'.format(self._parent_type): self._parent_id})
        return DiscussionEntry(self._requester, response_json)

    async def post_entry_async(self, **kwargs) -> 'DiscussionEntry':
        """
        Creates a new entry in a discussion topic.

        Endpoint: POST /api/v1/courses/:course_id/discussion_topics/:topic_id/entries

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.add_entry
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', '{}s/{}/discussion_topics/{}/entries'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'discussion_id': self.id, '{}_id'.format(self._parent_type): self._parent_id})
        return DiscussionEntry(self._requester, response_json)

    def subscribe(self, **kwargs) -> 'bool':
        """
        Subscribe to a topic to receive notifications about new entries.

        Endpoint: PUT /api/v1/courses/:course_id/discussion_topics/:topic_id/subscribed

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.subscribe_topic
        """
        response: 'httpx.Response' = self._requester.request('PUT', '{}s/{}/discussion_topics/{}/subscribed'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    async def subscribe_async(self, **kwargs) -> 'bool':
        """
        Subscribe to a topic to receive notifications about new entries.

        Endpoint: PUT /api/v1/courses/:course_id/discussion_topics/:topic_id/subscribed

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.subscribe_topic
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', '{}s/{}/discussion_topics/{}/subscribed'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    def unsubscribe(self, **kwargs) -> 'bool':
        """
        Unsubscribe from a topic to stop receiving notifications about new entries.

        Endpoint: DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id/subscribed

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.unsubscribe_topic
        """
        response: 'httpx.Response' = self._requester.request('DELETE', '{}s/{}/discussion_topics/{}/subscribed'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    async def unsubscribe_async(self, **kwargs) -> 'bool':
        """
        Unsubscribe from a topic to stop receiving notifications about new entries.

        Endpoint: DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id/subscribed

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.unsubscribe_topic
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', '{}s/{}/discussion_topics/{}/subscribed'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    def update(self, **kwargs) -> 'DiscussionTopic':
        """
        Updates an existing discussion topic for the course or group.

        Endpoint: PUT /api/v1/courses/:course_id/discussion_topics/:topic_id

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', '{}s/{}/discussion_topics/{}'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return DiscussionTopic(self._requester, response.json())

    async def update_async(self, **kwargs) -> 'DiscussionTopic':
        """
        Updates an existing discussion topic for the course or group.

        Endpoint: PUT /api/v1/courses/:course_id/discussion_topics/:topic_id

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', '{}s/{}/discussion_topics/{}'.format(self._parent_type, self._parent_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return DiscussionTopic(self._requester, response.json())

class DiscussionEntry(CanvasObject):

    def __str__(self):
        return '{} ({})'.format(self.message, self.id)

    @property
    def _discussion_parent_id(self) -> 'int':
        """
        Return the id of the course or group that spawned the discussion topic.
        """
        if hasattr(self, 'course_id'):
            return self.course_id
        elif hasattr(self, 'group_id'):
            return self.group_id
        else:
            raise ValueError('Discussion Topic does not have a course_id or group_id')

    @property
    def _discussion_parent_type(self) -> 'str':
        """
        Return whether the discussion topic was spawned from a course or group.
        """
        if hasattr(self, 'course_id'):
            return 'course'
        elif hasattr(self, 'group_id'):
            return 'group'
        else:
            raise ValueError('Discussion Topic does not have a course_id or group_id')

    def delete(self, **kwargs) -> 'bool':
        """
        Delete this discussion entry.

        Endpoint: DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:id

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_entries.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', '{}s/{}/discussion_topics/{}/entries/{}'.format(self._discussion_parent_type, self._discussion_parent_id, self.discussion_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return 'deleted_at' in response.json()

    async def delete_async(self, **kwargs) -> 'bool':
        """
        Delete this discussion entry.

        Endpoint: DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:id

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_entries.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', '{}s/{}/discussion_topics/{}/entries/{}'.format(self._discussion_parent_type, self._discussion_parent_id, self.discussion_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return 'deleted_at' in response.json()

    def get_discussion(self, **kwargs) -> 'DiscussionTopic':
        """
        Return the discussion topic object this entry is related to
        """
        response: 'httpx.Response' = self._requester.request('GET', '{}s/{}/discussion_topics/{}'.format(self._discussion_parent_type, self._discussion_parent_id, self.discussion_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'{}_id'.format(self._discussion_parent_type): self._discussion_parent_id})
        return DiscussionTopic(self._requester, response.json())

    async def get_discussion_async(self, **kwargs) -> 'DiscussionTopic':
        """
        Return the discussion topic object this entry is related to
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', '{}s/{}/discussion_topics/{}'.format(self._discussion_parent_type, self._discussion_parent_id, self.discussion_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'{}_id'.format(self._discussion_parent_type): self._discussion_parent_id})
        return DiscussionTopic(self._requester, response.json())

    def get_replies(self, **kwargs) -> 'PaginatedList[DiscussionEntry]':
        """
        Retrieves the replies to a top-level entry in a discussion topic.

        Endpoint: GET /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/replies

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.replies
        """
        return PaginatedList(DiscussionEntry, self._requester, 'GET', '{}s/{}/discussion_topics/{}/entries/{}/replies'.format(self._discussion_parent_type, self._discussion_parent_id, self.discussion_id, self.id), {'discussion_id': self.discussion_id, '{}_id'.format(self._discussion_parent_type): self._discussion_parent_id}, _kwargs=combine_kwargs(**kwargs))

    async def get_replies_async(self, **kwargs) -> 'PaginatedList[DiscussionEntry]':
        """
        Retrieves the replies to a top-level entry in a discussion topic.

        Endpoint: GET /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/replies

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.replies
        """
        return PaginatedList(DiscussionEntry, self._requester, 'GET', '{}s/{}/discussion_topics/{}/entries/{}/replies'.format(self._discussion_parent_type, self._discussion_parent_id, self.discussion_id, self.id), {'discussion_id': self.discussion_id, '{}_id'.format(self._discussion_parent_type): self._discussion_parent_id}, _kwargs=combine_kwargs(**kwargs))

    def mark_as_read(self, **kwargs) -> 'bool':
        """
        Mark a discussion entry as read.

        Endpoint: PUT /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/read

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_entry_read
        """
        response: 'httpx.Response' = self._requester.request('PUT', '{}s/{}/discussion_topics/{}/entries/{}/read'.format(self._discussion_parent_type, self._discussion_parent_id, self.discussion_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    async def mark_as_read_async(self, **kwargs) -> 'bool':
        """
        Mark a discussion entry as read.

        Endpoint: PUT /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/read

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_entry_read
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', '{}s/{}/discussion_topics/{}/entries/{}/read'.format(self._discussion_parent_type, self._discussion_parent_id, self.discussion_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    def mark_as_unread(self, **kwargs) -> 'bool':
        """
        Mark a discussion entry as unread.

        Endpoint: DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/read

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_entry_unread
        """
        response: 'httpx.Response' = self._requester.request('DELETE', '{}s/{}/discussion_topics/{}/entries/{}/read'.format(self._discussion_parent_type, self._discussion_parent_id, self.discussion_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    async def mark_as_unread_async(self, **kwargs) -> 'bool':
        """
        Mark a discussion entry as unread.

        Endpoint: DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/read

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_entry_unread
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', '{}s/{}/discussion_topics/{}/entries/{}/read'.format(self._discussion_parent_type, self._discussion_parent_id, self.discussion_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    def post_reply(self, **kwargs) -> 'DiscussionEntry':
        """
        Add a reply to this entry.

        Endpoint: POST /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/replies

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.add_reply
        """
        response: 'httpx.Response' = self._requester.request('POST', '{}s/{}/discussion_topics/{}/entries/{}/replies'.format(self._discussion_parent_type, self._discussion_parent_id, self.discussion_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update(discussion_id=self.discussion_id)
        return DiscussionEntry(self._requester, response_json)

    async def post_reply_async(self, **kwargs) -> 'DiscussionEntry':
        """
        Add a reply to this entry.

        Endpoint: POST /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/replies

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.add_reply
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', '{}s/{}/discussion_topics/{}/entries/{}/replies'.format(self._discussion_parent_type, self._discussion_parent_id, self.discussion_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update(discussion_id=self.discussion_id)
        return DiscussionEntry(self._requester, response_json)

    def rate(self, rating: 'int', **kwargs) -> 'bool':
        """
        Rate this discussion entry.

        Endpoint: POST /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/rating

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.rate_entry

        Parameters:
            rating: int
        """
        if rating not in (0, 1):
            raise ValueError('`rating` must be 0 or 1.')
        response: 'httpx.Response' = self._requester.request('POST', '{}s/{}/discussion_topics/{}/entries/{}/rating'.format(self._discussion_parent_type, self._discussion_parent_id, self.discussion_id, self.id), rating=rating, _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    async def rate_async(self, rating: 'int', **kwargs) -> 'bool':
        """
        Rate this discussion entry.

        Endpoint: POST /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/rating

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.rate_entry

        Parameters:
            rating: int
        """
        if rating not in (0, 1):
            raise ValueError('`rating` must be 0 or 1.')
        response: 'httpx.Response' = await self._requester.request_async('POST', '{}s/{}/discussion_topics/{}/entries/{}/rating'.format(self._discussion_parent_type, self._discussion_parent_id, self.discussion_id, self.id), rating=rating, _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    def update(self, **kwargs) -> 'bool':
        """
        Updates an existing discussion entry.

        Endpoint: PUT /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:id

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_entries.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', '{}s/{}/discussion_topics/{}/entries/{}'.format(self._discussion_parent_type, self._discussion_parent_id, self.discussion_id, self.id), _kwargs=combine_kwargs(**kwargs))
        if response.json().get('updated_at'):
            super(DiscussionEntry, self).set_attributes(response.json())
        return 'updated_at' in response.json()

    async def update_async(self, **kwargs) -> 'bool':
        """
        Updates an existing discussion entry.

        Endpoint: PUT /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:id

        Reference: https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_entries.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', '{}s/{}/discussion_topics/{}/entries/{}'.format(self._discussion_parent_type, self._discussion_parent_id, self.discussion_id, self.id), _kwargs=combine_kwargs(**kwargs))
        if response.json().get('updated_at'):
            super(DiscussionEntry, self).set_attributes(response.json())
        return 'updated_at' in response.json()