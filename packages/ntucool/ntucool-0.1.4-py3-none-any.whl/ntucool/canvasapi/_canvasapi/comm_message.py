from ..models.comm_messages import CommMessage as CommMessageModel
import httpx
import typing
from .canvas_object import CanvasObject

class CommMessage(CommMessageModel):

    def __str__(self):
        return '{} ({})'.format(self.subject, self.id)