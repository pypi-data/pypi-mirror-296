from ..models.peer_reviews import PeerReview as PeerReviewModel
import httpx
import typing
from .canvas_object import CanvasObject

class PeerReview(PeerReviewModel):

    def __str__(self):
        return '{} {} ({})'.format(self.asset_id, self.user_id, self.id)