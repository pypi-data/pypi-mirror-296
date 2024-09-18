from ..models.e_pub_exports import CourseEpubExport as CourseEpubExportModel
import httpx
import typing
from .canvas_object import CanvasObject

class CourseEpubExport(CourseEpubExportModel):

    def __str__(self):
        return '{} course_id:({}) epub_id:({}) {} '.format(self.name, self.id, self.epub_export['id'], self.epub_export['workflow_state'])