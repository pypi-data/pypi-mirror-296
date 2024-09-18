from ..models.course_audit_log import CourseEvent as CourseEventModel
import httpx
import typing
from .canvas_object import CanvasObject

class CourseEvent(CourseEventModel):

    def __str__(self):
        return '{} {} ({})'.format(self.name, self.start_at, self.conclude_at)