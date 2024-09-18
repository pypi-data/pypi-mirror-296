from ..models.user_observees import PairingCode as PairingCodeModel
import httpx
import typing
from .canvas_object import CanvasObject

class PairingCode(PairingCodeModel):

    def __str__(self):
        return '{} - {}'.format(self.user_id, self.code)