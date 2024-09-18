from ..models.users import Avatar as AvatarModel
import httpx
import typing
from .canvas_object import CanvasObject

class Avatar(AvatarModel):

    def __str__(self):
        return '{}'.format(self.display_name)