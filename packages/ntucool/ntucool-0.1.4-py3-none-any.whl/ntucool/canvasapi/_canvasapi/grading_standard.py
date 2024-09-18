from ..models.grading_standards import GradingStandard as GradingStandardModel
import httpx
import typing
from .canvas_object import CanvasObject

class GradingStandard(GradingStandardModel):

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)