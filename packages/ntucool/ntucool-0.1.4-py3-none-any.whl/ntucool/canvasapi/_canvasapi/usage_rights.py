from ..models.files import UsageRights as UsageRightsModel
import httpx
import typing
from .canvas_object import CanvasObject

class UsageRights(UsageRightsModel):

    def __str__(self):
        return '{} {}'.format(self.use_justification, self.license)