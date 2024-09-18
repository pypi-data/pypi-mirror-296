from ..models.collaborations import Collaboration as CollaborationModel, Collaborator as CollaboratorModel
import httpx
import typing
from .canvas_object import CanvasObject
from .paginated_list import PaginatedList
from .util import combine_kwargs

class Collaboration(CollaborationModel):

    def __str__(self):
        return '{} ({})'.format(self.document_id, self.id)

    def get_collaborators(self, **kwargs) -> 'Collaborator':
        """
        Return a list of collaborators for this collaboration.

        Endpoint: GET /api/v1/collaborations/:id/members

        Reference: https://canvas.instructure.com/doc/api/collaborations.html#method.collaborations.potential_collaborators
        """
        return PaginatedList(Collaborator, self._requester, 'GET', 'collaborations/{}/members'.format(self.id), _root='collaborators', kwargs=combine_kwargs(**kwargs))

    async def get_collaborators_async(self, **kwargs) -> 'Collaborator':
        """
        Return a list of collaborators for this collaboration.

        Endpoint: GET /api/v1/collaborations/:id/members

        Reference: https://canvas.instructure.com/doc/api/collaborations.html#method.collaborations.potential_collaborators
        """
        return PaginatedList(Collaborator, self._requester, 'GET', 'collaborations/{}/members'.format(self.id), _root='collaborators', kwargs=combine_kwargs(**kwargs))

class Collaborator(CollaboratorModel):

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)