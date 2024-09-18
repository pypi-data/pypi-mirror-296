from ..models.jw_ts import JWT as JWTModel
import httpx
import typing
from .canvas_object import CanvasObject

class JWT(JWTModel):

    def __str__(self):
        return '{}'.format(self.token)