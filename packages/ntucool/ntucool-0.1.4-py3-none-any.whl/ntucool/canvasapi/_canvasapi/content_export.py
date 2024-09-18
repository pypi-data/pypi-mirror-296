from ..models.content_exports import ContentExport as ContentExportModel
import httpx
import typing
from .canvas_object import CanvasObject

class ContentExport(ContentExportModel):

    def __str__(self):
        return '{} {} ({})'.format(self.export_type, self.user_id, self.id)