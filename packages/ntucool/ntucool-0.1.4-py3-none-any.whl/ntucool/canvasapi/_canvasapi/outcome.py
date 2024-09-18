from ..models.outcome_results import OutcomeResult as OutcomeResultModel
from ..models.outcome_groups import OutcomeLink as OutcomeLinkModel, OutcomeGroup as OutcomeGroupModel
from ..models.outcomes import Outcome as OutcomeModel
import httpx
import typing
if typing.TYPE_CHECKING:
    from .paginated_list import PaginatedList
from .canvas_object import CanvasObject
from .paginated_list import PaginatedList
from .util import combine_kwargs, obj_or_id

class Outcome(OutcomeModel):

    def __str__(self):
        return '{} ({})'.format(self.title, self.url)

    def update(self, **kwargs) -> 'bool':
        """
        Modify an existing outcome.

        Endpoint: PUT /api/v1/outcomes/:id

        Reference: https://canvas.instructure.com/doc/api/outcomes.html#method.outcomes_api.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'outcomes/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if 'id' in response.json():
            super(Outcome, self).set_attributes(response.json())
        return 'id' in response.json()

    async def update_async(self, **kwargs) -> 'bool':
        """
        Modify an existing outcome.

        Endpoint: PUT /api/v1/outcomes/:id

        Reference: https://canvas.instructure.com/doc/api/outcomes.html#method.outcomes_api.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'outcomes/{}'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        if 'id' in response.json():
            super(Outcome, self).set_attributes(response.json())
        return 'id' in response.json()

class OutcomeLink(OutcomeLinkModel):

    def __str__(self):
        return 'Group {} with Outcome {} ({})'.format(self.outcome_group, self.outcome, self.url)

    def context_ref(self):
        if self.context_type == 'Course':
            return 'courses/{}'.format(self.context_id)
        elif self.context_type == 'Account':
            return 'accounts/{}'.format(self.context_id)

    async def context_ref_async(self):
        if self.context_type == 'Course':
            return 'courses/{}'.format(self.context_id)
        elif self.context_type == 'Account':
            return 'accounts/{}'.format(self.context_id)

    def get_outcome(self, **kwargs) -> 'Outcome':
        """
        Return the linked outcome

        Endpoint: GET /api/v1/outcomes/:id

        Reference: https://canvas.instructure.com/doc/api/outcomes.html#method.outcomes_api.show
        """
        oid = self.outcome['id']
        response: 'httpx.Response' = self._requester.request('GET', 'outcomes/{}'.format(oid), _kwargs=combine_kwargs(**kwargs))
        return Outcome(self._requester, response.json())

    async def get_outcome_async(self, **kwargs) -> 'Outcome':
        """
        Return the linked outcome

        Endpoint: GET /api/v1/outcomes/:id

        Reference: https://canvas.instructure.com/doc/api/outcomes.html#method.outcomes_api.show
        """
        oid = self.outcome['id']
        response: 'httpx.Response' = await self._requester.request_async('GET', 'outcomes/{}'.format(oid), _kwargs=combine_kwargs(**kwargs))
        return Outcome(self._requester, response.json())

    def get_outcome_group(self, **kwargs) -> 'OutcomeGroup':
        """
        Return the linked outcome group

        Endpoint: GET /api/v1/global/outcome_groups/:id

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show
        """
        ogid = self.outcome_group['id']
        response: 'httpx.Response' = self._requester.request('GET', '{}/outcome_groups/{}'.format(self.context_ref(), ogid), _kwargs=combine_kwargs(**kwargs))
        return OutcomeGroup(self._requester, response.json())

    async def get_outcome_group_async(self, **kwargs) -> 'OutcomeGroup':
        """
        Return the linked outcome group

        Endpoint: GET /api/v1/global/outcome_groups/:id

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show
        """
        ogid = self.outcome_group['id']
        response: 'httpx.Response' = await self._requester.request_async('GET', '{}/outcome_groups/{}'.format(await self.context_ref_async(), ogid), _kwargs=combine_kwargs(**kwargs))
        return OutcomeGroup(self._requester, response.json())

class OutcomeGroup(OutcomeGroupModel):

    def __str__(self):
        return '{} ({})'.format(self.title, self.url)

    def context_ref(self):
        if self.context_type == 'Course':
            return 'courses/{}'.format(self.context_id)
        elif self.context_type == 'Account':
            return 'accounts/{}'.format(self.context_id)
        elif self.context_type is None:
            return 'global'

    async def context_ref_async(self):
        if self.context_type == 'Course':
            return 'courses/{}'.format(self.context_id)
        elif self.context_type == 'Account':
            return 'accounts/{}'.format(self.context_id)
        elif self.context_type is None:
            return 'global'

    def create_subgroup(self, title: 'str', **kwargs) -> 'OutcomeGroup':
        """
        Create a subgroup of the current group

        Endpoint: POST /api/v1/global/outcome_groups/:id/subgroups

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.create

        Parameters:
            title: str
        """
        response: 'httpx.Response' = self._requester.request('POST', '{}/outcome_groups/{}/subgroups'.format(self.context_ref(), self.id), title=title, _kwargs=combine_kwargs(**kwargs))
        return OutcomeGroup(self._requester, response.json())

    async def create_subgroup_async(self, title: 'str', **kwargs) -> 'OutcomeGroup':
        """
        Create a subgroup of the current group

        Endpoint: POST /api/v1/global/outcome_groups/:id/subgroups

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.create

        Parameters:
            title: str
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', '{}/outcome_groups/{}/subgroups'.format(await self.context_ref_async(), self.id), title=title, _kwargs=combine_kwargs(**kwargs))
        return OutcomeGroup(self._requester, response.json())

    def delete(self, **kwargs) -> 'bool':
        """
        Delete an outcome group.

        Endpoint: DELETE /api/v1/global/outcome_groups/:id

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', '{}/outcome_groups/{}'.format(self.context_ref(), self.id), _kwargs=combine_kwargs(**kwargs))
        if 'id' in response.json():
            super(OutcomeGroup, self).set_attributes(response.json())
        return 'id' in response.json()

    async def delete_async(self, **kwargs) -> 'bool':
        """
        Delete an outcome group.

        Endpoint: DELETE /api/v1/global/outcome_groups/:id

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', '{}/outcome_groups/{}'.format(await self.context_ref_async(), self.id), _kwargs=combine_kwargs(**kwargs))
        if 'id' in response.json():
            super(OutcomeGroup, self).set_attributes(response.json())
        return 'id' in response.json()

    def get_linked_outcomes(self, **kwargs) -> 'PaginatedList[OutcomeLink]':
        """
        List linked outcomes.

        Endpoint: GET /api/v1/global/outcome_groups/:id/outcomes

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.outcomes
        """
        return PaginatedList(OutcomeLink, self._requester, 'GET', '{}/outcome_groups/{}/outcomes'.format(self.context_ref(), self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_linked_outcomes_async(self, **kwargs) -> 'PaginatedList[OutcomeLink]':
        """
        List linked outcomes.

        Endpoint: GET /api/v1/global/outcome_groups/:id/outcomes

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.outcomes
        """
        return PaginatedList(OutcomeLink, self._requester, 'GET', '{}/outcome_groups/{}/outcomes'.format(await self.context_ref_async(), self.id), _kwargs=combine_kwargs(**kwargs))

    def get_subgroups(self, **kwargs) -> 'PaginatedList[OutcomeGroup]':
        """
        List subgroups.

        Endpoint: GET /api/v1/global/outcome_groups/:id/subgroups

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.subgroups
        """
        return PaginatedList(OutcomeGroup, self._requester, 'GET', '{}/outcome_groups/{}/subgroups'.format(self.context_ref(), self.id), {'context_type': self.context_type, 'context_id': self.context_id}, _kwargs=combine_kwargs(**kwargs))

    async def get_subgroups_async(self, **kwargs) -> 'PaginatedList[OutcomeGroup]':
        """
        List subgroups.

        Endpoint: GET /api/v1/global/outcome_groups/:id/subgroups

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.subgroups
        """
        return PaginatedList(OutcomeGroup, self._requester, 'GET', '{}/outcome_groups/{}/subgroups'.format(await self.context_ref_async(), self.id), {'context_type': self.context_type, 'context_id': self.context_id}, _kwargs=combine_kwargs(**kwargs))

    def import_outcome_group(self, outcome_group, **kwargs) -> 'OutcomeGroup':
        """
        Import an outcome group as a subgroup into the current outcome group

        Endpoint: POST /api/v1/global/outcome_groups/:id/import

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.import
        """
        source_outcome_group_id = obj_or_id(outcome_group, 'outcome_group', (OutcomeGroup,))
        response: 'httpx.Response' = self._requester.request('POST', '{}/outcome_groups/{}/import'.format(self.context_ref(), self.id), source_outcome_group_id=source_outcome_group_id, _kwargs=combine_kwargs(**kwargs))
        return OutcomeGroup(self._requester, response.json())

    async def import_outcome_group_async(self, outcome_group, **kwargs) -> 'OutcomeGroup':
        """
        Import an outcome group as a subgroup into the current outcome group

        Endpoint: POST /api/v1/global/outcome_groups/:id/import

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.import
        """
        source_outcome_group_id = obj_or_id(outcome_group, 'outcome_group', (OutcomeGroup,))
        response: 'httpx.Response' = await self._requester.request_async('POST', '{}/outcome_groups/{}/import'.format(await self.context_ref_async(), self.id), source_outcome_group_id=source_outcome_group_id, _kwargs=combine_kwargs(**kwargs))
        return OutcomeGroup(self._requester, response.json())

    def link_existing(self, outcome: 'Outcome | int', **kwargs) -> 'OutcomeLink':
        """
        Link to an existing Outcome.

        Endpoint: PUT /api/v1/global/outcome_groups/:id/outcomes/:outcome_id

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link

        Parameters:
            outcome: :class:`canvasapi.outcome.Outcome` or int
        """
        outcome_id = obj_or_id(outcome, 'outcome', (Outcome,))
        response: 'httpx.Response' = self._requester.request('PUT', '{}/outcome_groups/{}/outcomes/{}'.format(self.context_ref(), self.id, outcome_id), _kwargs=combine_kwargs(**kwargs))
        return OutcomeLink(self._requester, response.json())

    async def link_existing_async(self, outcome: 'Outcome | int', **kwargs) -> 'OutcomeLink':
        """
        Link to an existing Outcome.

        Endpoint: PUT /api/v1/global/outcome_groups/:id/outcomes/:outcome_id

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link

        Parameters:
            outcome: :class:`canvasapi.outcome.Outcome` or int
        """
        outcome_id = obj_or_id(outcome, 'outcome', (Outcome,))
        response: 'httpx.Response' = await self._requester.request_async('PUT', '{}/outcome_groups/{}/outcomes/{}'.format(await self.context_ref_async(), self.id, outcome_id), _kwargs=combine_kwargs(**kwargs))
        return OutcomeLink(self._requester, response.json())

    def link_new(self, title: 'str', **kwargs) -> 'OutcomeLink':
        """
        Create a new Outcome and link it to this OutcomeGroup

        Endpoint: POST /api/v1/global/outcome_groups/:id/outcomes

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link

        Parameters:
            title: str
        """
        response: 'httpx.Response' = self._requester.request('POST', '{}/outcome_groups/{}/outcomes'.format(self.context_ref(), self.id), title=title, _kwargs=combine_kwargs(**kwargs))
        return OutcomeLink(self._requester, response.json())

    async def link_new_async(self, title: 'str', **kwargs) -> 'OutcomeLink':
        """
        Create a new Outcome and link it to this OutcomeGroup

        Endpoint: POST /api/v1/global/outcome_groups/:id/outcomes

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link

        Parameters:
            title: str
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', '{}/outcome_groups/{}/outcomes'.format(await self.context_ref_async(), self.id), title=title, _kwargs=combine_kwargs(**kwargs))
        return OutcomeLink(self._requester, response.json())

    def unlink_outcome(self, outcome: 'Outcome | int', **kwargs) -> 'bool':
        """
        Remove an Outcome from and OutcomeLink

        Endpoint: DELETE /api/v1/global/outcome_groups/:id/outcomes/:outcome_id

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.unlink

        Parameters:
            outcome: :class:`canvasapi.outcome.Outcome` or int
        """
        outcome_id = obj_or_id(outcome, 'outcome', (Outcome,))
        response: 'httpx.Response' = self._requester.request('DELETE', '{}/outcome_groups/{}/outcomes/{}'.format(self.context_ref(), self.id, outcome_id), _kwargs=combine_kwargs(**kwargs))
        if 'context_id' in response.json():
            super(OutcomeGroup, self).set_attributes(response.json())
        return 'context_id' in response.json()

    async def unlink_outcome_async(self, outcome: 'Outcome | int', **kwargs) -> 'bool':
        """
        Remove an Outcome from and OutcomeLink

        Endpoint: DELETE /api/v1/global/outcome_groups/:id/outcomes/:outcome_id

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.unlink

        Parameters:
            outcome: :class:`canvasapi.outcome.Outcome` or int
        """
        outcome_id = obj_or_id(outcome, 'outcome', (Outcome,))
        response: 'httpx.Response' = await self._requester.request_async('DELETE', '{}/outcome_groups/{}/outcomes/{}'.format(await self.context_ref_async(), self.id, outcome_id), _kwargs=combine_kwargs(**kwargs))
        if 'context_id' in response.json():
            super(OutcomeGroup, self).set_attributes(response.json())
        return 'context_id' in response.json()

    def update(self, **kwargs) -> 'bool':
        """
        Update an outcome group.

        Endpoint: PUT /api/v1/global/outcome_groups/:id

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', '{}/outcome_groups/{}'.format(self.context_ref(), self.id), _kwargs=combine_kwargs(**kwargs))
        if 'id' in response.json():
            super(OutcomeGroup, self).set_attributes(response.json())
        return 'id' in response.json()

    async def update_async(self, **kwargs) -> 'bool':
        """
        Update an outcome group.

        Endpoint: PUT /api/v1/global/outcome_groups/:id

        Reference: https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', '{}/outcome_groups/{}'.format(await self.context_ref_async(), self.id), _kwargs=combine_kwargs(**kwargs))
        if 'id' in response.json():
            super(OutcomeGroup, self).set_attributes(response.json())
        return 'id' in response.json()

class OutcomeResult(OutcomeResultModel):

    def __str__(self):
        return '{} ({})'.format(self.id, self.score)