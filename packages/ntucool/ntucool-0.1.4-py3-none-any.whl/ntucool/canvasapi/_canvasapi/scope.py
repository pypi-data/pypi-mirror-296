from ..models.api_token_scopes import Scope as ScopeModel
import httpx
import typing
from .canvas_object import CanvasObject

class Scope(ScopeModel):

    def __str__(self):
        return '{}'.format(self.resource)