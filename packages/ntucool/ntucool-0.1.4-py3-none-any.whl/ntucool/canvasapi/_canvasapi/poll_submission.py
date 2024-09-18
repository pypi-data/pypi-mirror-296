from ..models.poll_submissions import PollSubmission as PollSubmissionModel
import httpx
import typing
from .canvas_object import CanvasObject

class PollSubmission(PollSubmissionModel):

    def __str__(self):
        return '{} ({})'.format(self.poll_choice_id, self.id)