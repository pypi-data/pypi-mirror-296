from ..models.grade_change_log import GradeChangeEvent as GradeChangeEventModel
import httpx
import typing
from .canvas_object import CanvasObject

class GradeChangeEvent(GradeChangeEventModel):

    def __str__(self):
        return '{} {} - {} ({})'.format(self.event_type, self.grade_before, self.grade_after, self.id)