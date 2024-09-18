from ..models.new_quizzes import NewQuiz as NewQuizModel
import httpx
import typing
from .canvas_object import CanvasObject
from .util import combine_kwargs

class NewQuiz(NewQuizModel):

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)

    def delete(self, **kwargs) -> 'NewQuiz':
        """
        Delete a single new quiz.

        Endpoint: DELETE /api/quiz/v1/courses/:course_id/quizzes/:assignment_id

        Reference: https://canvas.instructure.com/doc/api/new_quizzes.html#method.new_quizzes/quizzes_api.destroy
        """
        endpoint = 'courses/{}/quizzes/{}'.format(self.course_id, self.id)
        response: 'httpx.Response' = self._requester.request('DELETE', endpoint, _url='new_quizzes', _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return NewQuiz(self._requester, response_json)

    async def delete_async(self, **kwargs) -> 'NewQuiz':
        """
        Delete a single new quiz.

        Endpoint: DELETE /api/quiz/v1/courses/:course_id/quizzes/:assignment_id

        Reference: https://canvas.instructure.com/doc/api/new_quizzes.html#method.new_quizzes/quizzes_api.destroy
        """
        endpoint = 'courses/{}/quizzes/{}'.format(self.course_id, self.id)
        response: 'httpx.Response' = await self._requester.request_async('DELETE', endpoint, _url='new_quizzes', _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return NewQuiz(self._requester, response_json)

    def update(self, **kwargs) -> 'NewQuiz':
        """
        Update a single New Quiz for the course.

        Endpoint: PATCH /api/quiz/v1/courses/:course_id/quizzes/:assignment_id

        Reference: https://canvas.instructure.com/doc/api/new_quizzes.html#method.new_quizzes/quizzes_api.update
        """
        endpoint = 'courses/{}/quizzes/{}'.format(self.course_id, self.id)
        response: 'httpx.Response' = self._requester.request('PATCH', endpoint, _url='new_quizzes', _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return NewQuiz(self._requester, response_json)

    async def update_async(self, **kwargs) -> 'NewQuiz':
        """
        Update a single New Quiz for the course.

        Endpoint: PATCH /api/quiz/v1/courses/:course_id/quizzes/:assignment_id

        Reference: https://canvas.instructure.com/doc/api/new_quizzes.html#method.new_quizzes/quizzes_api.update
        """
        endpoint = 'courses/{}/quizzes/{}'.format(self.course_id, self.id)
        response: 'httpx.Response' = await self._requester.request_async('PATCH', endpoint, _url='new_quizzes', _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return NewQuiz(self._requester, response_json)