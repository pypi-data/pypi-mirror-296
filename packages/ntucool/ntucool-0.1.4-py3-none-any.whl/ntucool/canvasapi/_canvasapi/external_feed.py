from ..models.announcement_external_feeds import ExternalFeed as ExternalFeedModel
import httpx
import typing
from .canvas_object import CanvasObject

class ExternalFeed(ExternalFeedModel):

    def __str__(self):
        return '{}'.format(self.display_name)