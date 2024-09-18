from ..models.authentications_log import AuthenticationEvent as AuthenticationEventModel
import httpx
import typing
from .canvas_object import CanvasObject

class AuthenticationEvent(AuthenticationEventModel):

    def __str__(self):
        return '{} {} ({})'.format(self.created_at, self.event_type, self.pseudonym_id)