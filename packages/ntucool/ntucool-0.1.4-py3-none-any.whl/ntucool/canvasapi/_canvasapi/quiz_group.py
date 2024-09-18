from ..models.quiz_question_groups import QuizGroup as QuizGroupModel
import httpx
import typing
from .canvas_object import CanvasObject
from .exceptions import RequiredFieldMissing
from .util import combine_kwargs

class QuizGroup(QuizGroupModel):

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)

    def delete(self, **kwargs) -> 'bool':
        """
        Get details of the quiz group with the given id.

        Endpoint: DELETE /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/quizzes/{}/groups/{}'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    async def delete_async(self, **kwargs) -> 'bool':
        """
        Get details of the quiz group with the given id.

        Endpoint: DELETE /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/quizzes/{}/groups/{}'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    def reorder_question_group(self, order: 'list[dict]', **kwargs) -> 'bool':
        """
        Update the order of questions within a given group

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id/reorder

        Reference: https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.reorder

        Parameters:
            order: list[dict]
        """
        if not isinstance(order, list) or not order:
            raise ValueError('Param `order` must be a non-empty list.')
        for question in order:
            if not isinstance(question, dict):
                raise ValueError('`order` must consist only of dictionaries representing Question items.')
            if 'id' not in question:
                raise ValueError('Dictionaries in `order` must contain an `id` key.')
        kwargs['order'] = order
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/quizzes/{}/groups/{}/reorder'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    async def reorder_question_group_async(self, order: 'list[dict]', **kwargs) -> 'bool':
        """
        Update the order of questions within a given group

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id/reorder

        Reference: https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.reorder

        Parameters:
            order: list[dict]
        """
        if not isinstance(order, list) or not order:
            raise ValueError('Param `order` must be a non-empty list.')
        for question in order:
            if not isinstance(question, dict):
                raise ValueError('`order` must consist only of dictionaries representing Question items.')
            if 'id' not in question:
                raise ValueError('Dictionaries in `order` must contain an `id` key.')
        kwargs['order'] = order
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/quizzes/{}/groups/{}/reorder'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    def update(self, quiz_groups: 'list[dict]', **kwargs) -> 'bool':
        """
        Update a question group given by id.

        Endpoint: PUT /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.update

        Parameters:
            quiz_groups: list[dict]
        """
        if not isinstance(quiz_groups, list) or len(quiz_groups) <= 0:
            raise ValueError('Param `quiz_groups` must be a non-empty list.')
        if not isinstance(quiz_groups[0], dict):
            raise ValueError('Param `quiz_groups` must contain a dictionary')
        param_list = ['name', 'pick_count', 'question_points']
        if not any((param in quiz_groups[0] for param in param_list)):
            raise RequiredFieldMissing('quiz_groups must contain at least 1 parameter.')
        kwargs['quiz_groups'] = quiz_groups
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/quizzes/{}/groups/{}'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        successful = 'name' in response.json().get('quiz_groups')[0]
        if successful:
            super(QuizGroup, self).set_attributes(response.json().get('quiz_groups')[0])
        return successful

    async def update_async(self, quiz_groups: 'list[dict]', **kwargs) -> 'bool':
        """
        Update a question group given by id.

        Endpoint: PUT /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.update

        Parameters:
            quiz_groups: list[dict]
        """
        if not isinstance(quiz_groups, list) or len(quiz_groups) <= 0:
            raise ValueError('Param `quiz_groups` must be a non-empty list.')
        if not isinstance(quiz_groups[0], dict):
            raise ValueError('Param `quiz_groups` must contain a dictionary')
        param_list = ['name', 'pick_count', 'question_points']
        if not any((param in quiz_groups[0] for param in param_list)):
            raise RequiredFieldMissing('quiz_groups must contain at least 1 parameter.')
        kwargs['quiz_groups'] = quiz_groups
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/quizzes/{}/groups/{}'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        successful = 'name' in response.json().get('quiz_groups')[0]
        if successful:
            super(QuizGroup, self).set_attributes(response.json().get('quiz_groups')[0])
        return successful