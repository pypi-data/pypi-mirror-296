from ..models.gradebook_history import Day as DayModel, Grader as GraderModel, SubmissionHistory as SubmissionHistoryModel, SubmissionVersion as SubmissionVersionModel
import httpx
import typing
from .canvas_object import CanvasObject

class Day(DayModel):

    def __str__(self):
        return '{}'.format(self.date)

class Grader(GraderModel):

    def __str__(self):
        return '{}'.format(self.id)

class SubmissionHistory(SubmissionHistoryModel):

    def __str__(self):
        return '{}'.format(self.submission_id)

class SubmissionVersion(SubmissionVersionModel):

    def __str__(self):
        return '{} {}'.format(self.assignment_id, self.id)