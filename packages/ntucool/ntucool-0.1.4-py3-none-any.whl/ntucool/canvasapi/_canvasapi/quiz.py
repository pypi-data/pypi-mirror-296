from ..models.quiz_assignment_overrides import QuizAssignmentOverrideSet as QuizAssignmentOverrideSetModel
from ..models.quiz_submission_questions import QuizSubmissionQuestion as QuizSubmissionQuestionModel
from ..models.quiz_submission_events import QuizSubmissionEvent as QuizSubmissionEventModel
from ..models.quiz_reports import QuizReport as QuizReportModel
from ..models.quiz_questions import QuizQuestion as QuizQuestionModel
from ..models.quiz_extensions import QuizExtension as QuizExtensionModel
from ..models.quiz_submissions import QuizSubmission as QuizSubmissionModel
from ..models.quiz_statistics import QuizStatistics as QuizStatisticsModel
from ..models.quizzes import Quiz as QuizModel
import httpx
import typing
if typing.TYPE_CHECKING:
    from .paginated_list import PaginatedList
    from .quiz_group import QuizGroup
from .canvas_object import CanvasObject
from .exceptions import RequiredFieldMissing
from .paginated_list import PaginatedList
from .quiz_group import QuizGroup
from .submission import Submission
from .user import User
from .util import combine_kwargs, obj_or_id

class Quiz(QuizModel):

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)

    def broadcast_message(self, conversations: 'dict', **kwargs) -> 'bool':
        """
        Send a message to unsubmitted or submitted users for the quiz.

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:id/submission_users/message

        Reference: https://canvas.instructure.com/doc/api/quiz_submission_user_list.html#method.quizzes/quiz_submission_users.message

        Parameters:
            conversations: dict
        """
        required_key_list = ['body', 'recipients', 'subject']
        required_keys_present = all((x in conversations for x in required_key_list))
        if isinstance(conversations, dict) and required_keys_present:
            kwargs['conversations'] = conversations
        else:
            raise RequiredFieldMissing("conversations must be a dictionary with keys 'body', 'recipients', and 'subject'.")
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/quizzes/{}/submission_users/message'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 201

    async def broadcast_message_async(self, conversations: 'dict', **kwargs) -> 'bool':
        """
        Send a message to unsubmitted or submitted users for the quiz.

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:id/submission_users/message

        Reference: https://canvas.instructure.com/doc/api/quiz_submission_user_list.html#method.quizzes/quiz_submission_users.message

        Parameters:
            conversations: dict
        """
        required_key_list = ['body', 'recipients', 'subject']
        required_keys_present = all((x in conversations for x in required_key_list))
        if isinstance(conversations, dict) and required_keys_present:
            kwargs['conversations'] = conversations
        else:
            raise RequiredFieldMissing("conversations must be a dictionary with keys 'body', 'recipients', and 'subject'.")
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/quizzes/{}/submission_users/message'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 201

    def create_question(self, **kwargs) -> 'QuizQuestion':
        """
        Create a new quiz question for this quiz.

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:quiz_id/questions

        Reference: https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.create
        """
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/quizzes/{}/questions'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return QuizQuestion(self._requester, response_json)

    async def create_question_async(self, **kwargs) -> 'QuizQuestion':
        """
        Create a new quiz question for this quiz.

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:quiz_id/questions

        Reference: https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.create
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/quizzes/{}/questions'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return QuizQuestion(self._requester, response_json)

    def create_question_group(self, quiz_groups: 'list[dict]', **kwargs) -> 'QuizGroup':
        """
        Create a new question group for the given quiz id

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:quiz_id/groups

        Reference: https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.create

        Parameters:
            quiz_groups: list[dict]
        """
        if not isinstance(quiz_groups, list) or not quiz_groups:
            raise ValueError('Param `quiz_groups` must be a non-empty list.')
        if not isinstance(quiz_groups[0], dict):
            raise ValueError('Param `quiz_groups must contain a dictionary')
        param_list = ['name', 'pick_count', 'question_points', 'assessment_question_bank_id']
        if not any((param in quiz_groups[0] for param in param_list)):
            raise RequiredFieldMissing('quiz_groups must contain at least 1 parameter.')
        kwargs['quiz_groups'] = quiz_groups
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/quizzes/{}/groups'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json['quiz_groups'][0].update({'course_id': self.id})
        return QuizGroup(self._requester, response_json.get('quiz_groups')[0])

    async def create_question_group_async(self, quiz_groups: 'list[dict]', **kwargs) -> 'QuizGroup':
        """
        Create a new question group for the given quiz id

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:quiz_id/groups

        Reference: https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.create

        Parameters:
            quiz_groups: list[dict]
        """
        if not isinstance(quiz_groups, list) or not quiz_groups:
            raise ValueError('Param `quiz_groups` must be a non-empty list.')
        if not isinstance(quiz_groups[0], dict):
            raise ValueError('Param `quiz_groups must contain a dictionary')
        param_list = ['name', 'pick_count', 'question_points', 'assessment_question_bank_id']
        if not any((param in quiz_groups[0] for param in param_list)):
            raise RequiredFieldMissing('quiz_groups must contain at least 1 parameter.')
        kwargs['quiz_groups'] = quiz_groups
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/quizzes/{}/groups'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json['quiz_groups'][0].update({'course_id': self.id})
        return QuizGroup(self._requester, response_json.get('quiz_groups')[0])

    def create_report(self, report_type: 'str', **kwargs) -> 'QuizReport':
        """
        Create and return a new report for this quiz. If a previously generated report
        matches the arguments and is still current (i.e. there have been no new submissions),
        it will be returned.

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:quiz_id/reports

        Reference: https://canvas.instructure.com/doc/api/quiz_reports.html#method.quizzes/quiz_reports.create

        Parameters:
            report_type: str
        """
        if report_type not in ['student_analysis', 'item_analysis']:
            raise ValueError("Param `report_type` must be a either 'student_analysis' or 'item_analysis'")
        kwargs['quiz_report'] = {'report_type': report_type}
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/quizzes/{}/reports'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return QuizReport(self._requester, response_json)

    async def create_report_async(self, report_type: 'str', **kwargs) -> 'QuizReport':
        """
        Create and return a new report for this quiz. If a previously generated report
        matches the arguments and is still current (i.e. there have been no new submissions),
        it will be returned.

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:quiz_id/reports

        Reference: https://canvas.instructure.com/doc/api/quiz_reports.html#method.quizzes/quiz_reports.create

        Parameters:
            report_type: str
        """
        if report_type not in ['student_analysis', 'item_analysis']:
            raise ValueError("Param `report_type` must be a either 'student_analysis' or 'item_analysis'")
        kwargs['quiz_report'] = {'report_type': report_type}
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/quizzes/{}/reports'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return QuizReport(self._requester, response_json)

    def create_submission(self, **kwargs) -> 'QuizSubmission':
        """
        Start taking a Quiz by creating a QuizSubmission can be used to answer
        questions and submit answers.

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:quiz_id/submissions

        Reference: https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.create
        """
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/quizzes/{}/submissions'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json = response.json()['quiz_submissions'][0]
        response_json.update({'course_id': self.course_id})
        return QuizSubmission(self._requester, response_json)

    async def create_submission_async(self, **kwargs) -> 'QuizSubmission':
        """
        Start taking a Quiz by creating a QuizSubmission can be used to answer
        questions and submit answers.

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:quiz_id/submissions

        Reference: https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.create
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/quizzes/{}/submissions'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json = response.json()['quiz_submissions'][0]
        response_json.update({'course_id': self.course_id})
        return QuizSubmission(self._requester, response_json)

    def delete(self, **kwargs) -> 'Quiz':
        """
        Delete this quiz.

        Endpoint: DELETE /api/v1/courses/:course_id/quizzes/:id

        Reference: https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/quizzes/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        quiz_json: 'dict' = response.json()
        quiz_json.update({'course_id': self.course_id})
        return Quiz(self._requester, quiz_json)

    async def delete_async(self, **kwargs) -> 'Quiz':
        """
        Delete this quiz.

        Endpoint: DELETE /api/v1/courses/:course_id/quizzes/:id

        Reference: https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/quizzes/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        quiz_json: 'dict' = response.json()
        quiz_json.update({'course_id': self.course_id})
        return Quiz(self._requester, quiz_json)

    def edit(self, **kwargs) -> 'Quiz':
        """
        Modify this quiz.

        Endpoint: PUT /api/v1/courses/:course_id/quizzes/:id

        Reference: https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/quizzes/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        quiz_json: 'dict' = response.json()
        quiz_json.update({'course_id': self.course_id})
        return Quiz(self._requester, quiz_json)

    async def edit_async(self, **kwargs) -> 'Quiz':
        """
        Modify this quiz.

        Endpoint: PUT /api/v1/courses/:course_id/quizzes/:id

        Reference: https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/quizzes/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        quiz_json: 'dict' = response.json()
        quiz_json.update({'course_id': self.course_id})
        return Quiz(self._requester, quiz_json)

    def get_all_quiz_reports(self, **kwargs) -> 'PaginatedList[QuizReport]':
        """
        Get a list of all quiz reports for this quiz

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/reports

        Reference: https://canvas.instructure.com/doc/api/quiz_reports.html#method.quizzes/quiz_reports.index
        """
        return PaginatedList(QuizReport, self._requester, 'GET', 'courses/{}/quizzes/{}/reports'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))

    async def get_all_quiz_reports_async(self, **kwargs) -> 'PaginatedList[QuizReport]':
        """
        Get a list of all quiz reports for this quiz

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/reports

        Reference: https://canvas.instructure.com/doc/api/quiz_reports.html#method.quizzes/quiz_reports.index
        """
        return PaginatedList(QuizReport, self._requester, 'GET', 'courses/{}/quizzes/{}/reports'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))

    def get_question(self, question: 'int | str | QuizQuestion', **kwargs) -> 'QuizQuestion':
        """
        Get as single quiz question by ID.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/questions/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.show

        Parameters:
            question: int, str or :class:`canvasapi.quiz.QuizQuestion`
        """
        question_id = obj_or_id(question, 'question', (QuizQuestion,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/quizzes/{}/questions/{}'.format(self.course_id, self.id, question_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return QuizQuestion(self._requester, response_json)

    async def get_question_async(self, question: 'int | str | QuizQuestion', **kwargs) -> 'QuizQuestion':
        """
        Get as single quiz question by ID.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/questions/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.show

        Parameters:
            question: int, str or :class:`canvasapi.quiz.QuizQuestion`
        """
        question_id = obj_or_id(question, 'question', (QuizQuestion,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/quizzes/{}/questions/{}'.format(self.course_id, self.id, question_id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return QuizQuestion(self._requester, response_json)

    def get_questions(self, **kwargs) -> 'PaginatedList[QuizQuestion]':
        """
        List all questions for a quiz.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/questions

        Reference: https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.index
        """
        return PaginatedList(QuizQuestion, self._requester, 'GET', 'courses/{}/quizzes/{}/questions'.format(self.course_id, self.id), {'course_id': self.course_id}, _kwargs=combine_kwargs(**kwargs))

    async def get_questions_async(self, **kwargs) -> 'PaginatedList[QuizQuestion]':
        """
        List all questions for a quiz.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/questions

        Reference: https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.index
        """
        return PaginatedList(QuizQuestion, self._requester, 'GET', 'courses/{}/quizzes/{}/questions'.format(self.course_id, self.id), {'course_id': self.course_id}, _kwargs=combine_kwargs(**kwargs))

    def get_quiz_group(self, id: 'int', **kwargs) -> 'QuizGroup':
        """
        Get details of the quiz group with the given id

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.show

        Parameters:
            id: int
        """
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/quizzes/{}/groups/{}'.format(self.course_id, self.id, id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return QuizGroup(self._requester, response_json)

    async def get_quiz_group_async(self, id: 'int', **kwargs) -> 'QuizGroup':
        """
        Get details of the quiz group with the given id

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.show

        Parameters:
            id: int
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/quizzes/{}/groups/{}'.format(self.course_id, self.id, id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return QuizGroup(self._requester, response_json)

    def get_quiz_report(self, id: 'int | QuizReport', **kwargs) -> 'QuizReport':
        """
        Returns the data for a single quiz report.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/reports/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_reports.html#method.quizzes/quiz_reports.show

        Parameters:
            id: int or :class:`canvasapi.quiz.QuizReport`
        """
        id = obj_or_id(id, 'id', (QuizReport,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/quizzes/{}/reports/{}'.format(self.course_id, self.id, id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return QuizReport(self._requester, response_json)

    async def get_quiz_report_async(self, id: 'int | QuizReport', **kwargs) -> 'QuizReport':
        """
        Returns the data for a single quiz report.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/reports/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_reports.html#method.quizzes/quiz_reports.show

        Parameters:
            id: int or :class:`canvasapi.quiz.QuizReport`
        """
        id = obj_or_id(id, 'id', (QuizReport,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/quizzes/{}/reports/{}'.format(self.course_id, self.id, id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        return QuizReport(self._requester, response_json)

    def get_quiz_submission(self, quiz_submission: 'int | string | QuizSubmission', **kwargs) -> 'QuizSubmission':
        """
        Get a single quiz submission.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.show

        Parameters:
            quiz_submission: int, string, :class:`canvasapi.quiz.QuizSubmission`
        """
        quiz_submission_id = obj_or_id(quiz_submission, 'quiz_submission', (QuizSubmission,))
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/quizzes/{}/submissions/{}'.format(self.course_id, self.id, quiz_submission_id), _kwargs=combine_kwargs(**kwargs))
        response_json = response.json()['quiz_submissions'][0]
        response_json.update({'course_id': self.course_id})
        if len(response.json().get('quizzes', [])) > 0:
            response_json.update({'quiz': Quiz(self._requester, response.json()['quizzes'][0])})
        if len(response.json().get('submissions', [])) > 0:
            response_json.update({'submission': Submission(self._requester, response.json()['submissions'][0])})
        if len(response.json().get('users', [])) > 0:
            response_json.update({'user': User(self._requester, response.json()['users'][0])})
        return QuizSubmission(self._requester, response_json)

    async def get_quiz_submission_async(self, quiz_submission: 'int | string | QuizSubmission', **kwargs) -> 'QuizSubmission':
        """
        Get a single quiz submission.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.show

        Parameters:
            quiz_submission: int, string, :class:`canvasapi.quiz.QuizSubmission`
        """
        quiz_submission_id = obj_or_id(quiz_submission, 'quiz_submission', (QuizSubmission,))
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/quizzes/{}/submissions/{}'.format(self.course_id, self.id, quiz_submission_id), _kwargs=combine_kwargs(**kwargs))
        response_json = response.json()['quiz_submissions'][0]
        response_json.update({'course_id': self.course_id})
        if len(response.json().get('quizzes', [])) > 0:
            response_json.update({'quiz': Quiz(self._requester, response.json()['quizzes'][0])})
        if len(response.json().get('submissions', [])) > 0:
            response_json.update({'submission': Submission(self._requester, response.json()['submissions'][0])})
        if len(response.json().get('users', [])) > 0:
            response_json.update({'user': User(self._requester, response.json()['users'][0])})
        return QuizSubmission(self._requester, response_json)

    def get_statistics(self, **kwargs) -> 'PaginatedList[QuizStatistic]':
        """
        Get statistics for for all quiz versions, or the latest quiz version.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/statistics

        Reference: https://canvas.instructure.com/doc/api/quiz_statistics.html#method.quizzes/quiz_statistics.index
        """
        return PaginatedList(QuizStatistics, self._requester, 'GET', 'courses/{}/quizzes/{}/statistics'.format(self.course_id, self.id), {'course_id': self.course_id}, _root='quiz_statistics', _kwargs=combine_kwargs(**kwargs))

    async def get_statistics_async(self, **kwargs) -> 'PaginatedList[QuizStatistic]':
        """
        Get statistics for for all quiz versions, or the latest quiz version.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/statistics

        Reference: https://canvas.instructure.com/doc/api/quiz_statistics.html#method.quizzes/quiz_statistics.index
        """
        return PaginatedList(QuizStatistics, self._requester, 'GET', 'courses/{}/quizzes/{}/statistics'.format(self.course_id, self.id), {'course_id': self.course_id}, _root='quiz_statistics', _kwargs=combine_kwargs(**kwargs))

    def get_submissions(self, **kwargs) -> 'PaginatedList[QuizSubmission]':
        """
        Get a list of all submissions for this quiz.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions

        Reference: https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.index
        """
        return PaginatedList(QuizSubmission, self._requester, 'GET', 'courses/{}/quizzes/{}/submissions'.format(self.course_id, self.id), {'course_id': self.course_id}, _root='quiz_submissions', _kwargs=combine_kwargs(**kwargs))

    async def get_submissions_async(self, **kwargs) -> 'PaginatedList[QuizSubmission]':
        """
        Get a list of all submissions for this quiz.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions

        Reference: https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.index
        """
        return PaginatedList(QuizSubmission, self._requester, 'GET', 'courses/{}/quizzes/{}/submissions'.format(self.course_id, self.id), {'course_id': self.course_id}, _root='quiz_submissions', _kwargs=combine_kwargs(**kwargs))

    def set_extensions(self, quiz_extensions: 'list', **kwargs) -> 'list[QuizExtension]':
        """
        Set extensions for student quiz submissions.

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:quiz_id/extensions

        Reference: https://canvas.instructure.com/doc/api/quiz_extensions.html#method.quizzes/quiz_extensions.create

        Parameters:
            quiz_extensions: list
        """
        if not isinstance(quiz_extensions, list) or not quiz_extensions:
            raise ValueError('Param `quiz_extensions` must be a non-empty list.')
        if any((not isinstance(extension, dict) for extension in quiz_extensions)):
            raise ValueError('Param `quiz_extensions` must only contain dictionaries')
        if any(('user_id' not in extension for extension in quiz_extensions)):
            raise RequiredFieldMissing('Dictionaries in `quiz_extensions` must contain key `user_id`')
        kwargs['quiz_extensions'] = quiz_extensions
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/quizzes/{}/extensions'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        extension_list = response.json()['quiz_extensions']
        return [QuizExtension(self._requester, extension) for extension in extension_list]

    async def set_extensions_async(self, quiz_extensions: 'list', **kwargs) -> 'list[QuizExtension]':
        """
        Set extensions for student quiz submissions.

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:quiz_id/extensions

        Reference: https://canvas.instructure.com/doc/api/quiz_extensions.html#method.quizzes/quiz_extensions.create

        Parameters:
            quiz_extensions: list
        """
        if not isinstance(quiz_extensions, list) or not quiz_extensions:
            raise ValueError('Param `quiz_extensions` must be a non-empty list.')
        if any((not isinstance(extension, dict) for extension in quiz_extensions)):
            raise ValueError('Param `quiz_extensions` must only contain dictionaries')
        if any(('user_id' not in extension for extension in quiz_extensions)):
            raise RequiredFieldMissing('Dictionaries in `quiz_extensions` must contain key `user_id`')
        kwargs['quiz_extensions'] = quiz_extensions
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/quizzes/{}/extensions'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        extension_list = response.json()['quiz_extensions']
        return [QuizExtension(self._requester, extension) for extension in extension_list]

class QuizStatistics(QuizStatisticsModel):

    def __str__(self):
        return 'Quiz Statistics {}'.format(self.id)

class QuizSubmission(QuizSubmissionModel):

    def __str__(self):
        return 'Quiz {} - User {} ({})'.format(self.quiz_id, self.user_id, self.id)

    def answer_submission_questions(self, validation_token: 'str | None'=None, **kwargs) -> 'list[QuizSubmissionQuestion]':
        """
        Provide or update an answer to one or more quiz questions.

        Endpoint: POST /api/v1/quiz_submissions/:quiz_submission_id/questions

        Reference: https://canvas.instructure.com/doc/api/quiz_submission_questions.html#method.quizzes/quiz_submission_questions.answer

        Parameters:
            validation_token: str
        """
        try:
            kwargs['validation_token'] = validation_token or self.validation_token
        except AttributeError:
            raise RequiredFieldMissing('`validation_token` not set on this QuizSubmission, must be passed as a function argument.')
        kwargs['attempt'] = self.attempt
        response: 'httpx.Response' = self._requester.request('POST', 'quiz_submissions/{}/questions'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        questions = list()
        for question in response.json().get('quiz_submission_questions', []):
            question.update({'quiz_submission_id': self.id, 'validation_token': kwargs['validation_token'], 'attempt': self.attempt})
            questions.append(QuizSubmissionQuestion(self._requester, question))
        return questions

    async def answer_submission_questions_async(self, validation_token: 'str | None'=None, **kwargs) -> 'list[QuizSubmissionQuestion]':
        """
        Provide or update an answer to one or more quiz questions.

        Endpoint: POST /api/v1/quiz_submissions/:quiz_submission_id/questions

        Reference: https://canvas.instructure.com/doc/api/quiz_submission_questions.html#method.quizzes/quiz_submission_questions.answer

        Parameters:
            validation_token: str
        """
        try:
            kwargs['validation_token'] = validation_token or self.validation_token
        except AttributeError:
            raise RequiredFieldMissing('`validation_token` not set on this QuizSubmission, must be passed as a function argument.')
        kwargs['attempt'] = self.attempt
        response: 'httpx.Response' = await self._requester.request_async('POST', 'quiz_submissions/{}/questions'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        questions = list()
        for question in response.json().get('quiz_submission_questions', []):
            question.update({'quiz_submission_id': self.id, 'validation_token': kwargs['validation_token'], 'attempt': self.attempt})
            questions.append(QuizSubmissionQuestion(self._requester, question))
        return questions

    def complete(self, validation_token: 'str | None'=None, **kwargs) -> 'QuizSubmission':
        """
        Complete the quiz submission by marking it as complete and grading it. When the quiz
        submission has been marked as complete, no further modifications will be allowed.

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id/complete

        Reference: https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.complete

        Parameters:
            validation_token: str
        """
        try:
            kwargs['validation_token'] = validation_token or self.validation_token
        except AttributeError:
            raise RequiredFieldMissing('`validation_token` not set on this QuizSubmission, must be passed as a function argument.')
        kwargs['attempt'] = self.attempt
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/quizzes/{}/submissions/{}/complete'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json = response.json()['quiz_submissions'][0]
        return QuizSubmission(self._requester, response_json)

    async def complete_async(self, validation_token: 'str | None'=None, **kwargs) -> 'QuizSubmission':
        """
        Complete the quiz submission by marking it as complete and grading it. When the quiz
        submission has been marked as complete, no further modifications will be allowed.

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id/complete

        Reference: https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.complete

        Parameters:
            validation_token: str
        """
        try:
            kwargs['validation_token'] = validation_token or self.validation_token
        except AttributeError:
            raise RequiredFieldMissing('`validation_token` not set on this QuizSubmission, must be passed as a function argument.')
        kwargs['attempt'] = self.attempt
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/quizzes/{}/submissions/{}/complete'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json = response.json()['quiz_submissions'][0]
        return QuizSubmission(self._requester, response_json)

    def get_submission_events(self, **kwargs) -> 'PaginatedList[QuizSubmissionEvent]':
        """
        Retrieve the set of events captured during a specific submission attempt.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id/events

        Reference: https://canvas.instructure.com/doc/api/quiz_submission_events.html#method.quizzes/quiz_submission_events_api.index
        """
        return PaginatedList(QuizSubmissionEvent, self._requester, 'GET', 'courses/{}/quizzes/{}/submissions/{}/events'.format(self.course_id, self.quiz_id, self.id), _root='quiz_submission_events', _kwargs=combine_kwargs(**kwargs))

    async def get_submission_events_async(self, **kwargs) -> 'PaginatedList[QuizSubmissionEvent]':
        """
        Retrieve the set of events captured during a specific submission attempt.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id/events

        Reference: https://canvas.instructure.com/doc/api/quiz_submission_events.html#method.quizzes/quiz_submission_events_api.index
        """
        return PaginatedList(QuizSubmissionEvent, self._requester, 'GET', 'courses/{}/quizzes/{}/submissions/{}/events'.format(self.course_id, self.quiz_id, self.id), _root='quiz_submission_events', _kwargs=combine_kwargs(**kwargs))

    def get_submission_questions(self, **kwargs) -> 'list[QuizSubmissionQuestion]':
        """
        Get a list of all the question records for this quiz submission.

        Endpoint: GET /api/v1/quiz_submissions/:quiz_submission_id/questions

        Reference: https://canvas.instructure.com/doc/api/quiz_submission_questions.html#method.quizzes/quiz_submission_questions.index
        """
        response: 'httpx.Response' = self._requester.request('GET', 'quiz_submissions/{}/questions'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        questions = list()
        for question in response.json().get('quiz_submission_questions', []):
            question.update({'quiz_submission_id': self.id, 'attempt': self.attempt})
            questions.append(QuizSubmissionQuestion(self._requester, question))
        return questions

    async def get_submission_questions_async(self, **kwargs) -> 'list[QuizSubmissionQuestion]':
        """
        Get a list of all the question records for this quiz submission.

        Endpoint: GET /api/v1/quiz_submissions/:quiz_submission_id/questions

        Reference: https://canvas.instructure.com/doc/api/quiz_submission_questions.html#method.quizzes/quiz_submission_questions.index
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'quiz_submissions/{}/questions'.format(self.id), _kwargs=combine_kwargs(**kwargs))
        questions = list()
        for question in response.json().get('quiz_submission_questions', []):
            question.update({'quiz_submission_id': self.id, 'attempt': self.attempt})
            questions.append(QuizSubmissionQuestion(self._requester, question))
        return questions

    def get_times(self, **kwargs) -> 'dict':
        """
        Get the current timing data for the quiz attempt, both the end_at timestamp and the
        time_left parameter.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id/time

        Reference: https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.time
        """
        response: 'httpx.Response' = self._requester.request('GET', 'courses/{}/quizzes/{}/submissions/{}/time'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    async def get_times_async(self, **kwargs) -> 'dict':
        """
        Get the current timing data for the quiz attempt, both the end_at timestamp and the
        time_left parameter.

        Endpoint: GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id/time

        Reference: https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.time
        """
        response: 'httpx.Response' = await self._requester.request_async('GET', 'courses/{}/quizzes/{}/submissions/{}/time'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def submit_events(self, quiz_submission_events: 'list', **kwargs) -> 'bool':
        """
        Store a set of events which were captured during a quiz taking session.

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id/events

        Reference: https://canvas.instructure.com/doc/api/quiz_submission_events.html#method.quizzes/quiz_submission_events_api.create

        Parameters:
            quiz_submission_events: list
        """
        if isinstance(quiz_submission_events, list) and isinstance(quiz_submission_events[0], QuizSubmissionEvent):
            kwargs['quiz_submission_events'] = quiz_submission_events
        else:
            raise RequiredFieldMissing('Required parameter quiz_submission_events missing.')
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/quizzes/{}/submissions/{}/events'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    async def submit_events_async(self, quiz_submission_events: 'list', **kwargs) -> 'bool':
        """
        Store a set of events which were captured during a quiz taking session.

        Endpoint: POST /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id/events

        Reference: https://canvas.instructure.com/doc/api/quiz_submission_events.html#method.quizzes/quiz_submission_events_api.create

        Parameters:
            quiz_submission_events: list
        """
        if isinstance(quiz_submission_events, list) and isinstance(quiz_submission_events[0], QuizSubmissionEvent):
            kwargs['quiz_submission_events'] = quiz_submission_events
        else:
            raise RequiredFieldMissing('Required parameter quiz_submission_events missing.')
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/quizzes/{}/submissions/{}/events'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    def update_score_and_comments(self, **kwargs) -> 'QuizSubmission':
        """
        Update the amount of points a student has scored for questions they've answered, provide
        comments for the student about their answer(s), or simply fudge the total score by a
        specific amount of points.

        Endpoint: PUT /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/quizzes/{}/submissions/{}'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json = response.json()['quiz_submissions'][0]
        response_json.update({'course_id': self.course_id})
        return QuizSubmission(self._requester, response_json)

    async def update_score_and_comments_async(self, **kwargs) -> 'QuizSubmission':
        """
        Update the amount of points a student has scored for questions they've answered, provide
        comments for the student about their answer(s), or simply fudge the total score by a
        specific amount of points.

        Endpoint: PUT /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/quizzes/{}/submissions/{}'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json = response.json()['quiz_submissions'][0]
        response_json.update({'course_id': self.course_id})
        return QuizSubmission(self._requester, response_json)

class QuizExtension(QuizExtensionModel):

    def __str__(self):
        return '{}-{}'.format(self.quiz_id, self.user_id)

class QuizQuestion(QuizQuestionModel):

    def __str__(self):
        return '{} ({})'.format(self.question_name, self.id)

    def delete(self, **kwargs) -> 'bool':
        """
        Delete an existing quiz question.

        Endpoint: DELETE /api/v1/courses/:course_id/quizzes/:quiz_id/questions/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/quizzes/{}/questions/{}'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    async def delete_async(self, **kwargs) -> 'bool':
        """
        Delete an existing quiz question.

        Endpoint: DELETE /api/v1/courses/:course_id/quizzes/:quiz_id/questions/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/quizzes/{}/questions/{}'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    def edit(self, **kwargs) -> 'QuizQuestion':
        """
        Update an existing quiz question.

        Endpoint: PUT /api/v1/courses/:course_id/quizzes/:quiz_id/questions/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/quizzes/{}/questions/{}'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        super(QuizQuestion, self).set_attributes(response_json)
        return self

    async def edit_async(self, **kwargs) -> 'QuizQuestion':
        """
        Update an existing quiz question.

        Endpoint: PUT /api/v1/courses/:course_id/quizzes/:quiz_id/questions/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/quizzes/{}/questions/{}'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        super(QuizQuestion, self).set_attributes(response_json)
        return self

class QuizReport(QuizReportModel):

    def __str__(self):
        return '{} ({})'.format(self.report_type, self.id)

    def abort_or_delete(self, **kwargs) -> 'bool':
        """
        This API allows you to cancel a previous request you issued for a report to be generated.
        Or in the case of an already generated report, you'd like to remove it, perhaps to generate
        it another time with an updated version that provides new features.

        Endpoint: DELETE /api/v1/courses/:course_id/quizzes/:quiz_id/reports/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_reports.html#method.quizzes/quiz_reports.abort
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/quizzes/{}/reports/{}'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

    async def abort_or_delete_async(self, **kwargs) -> 'bool':
        """
        This API allows you to cancel a previous request you issued for a report to be generated.
        Or in the case of an already generated report, you'd like to remove it, perhaps to generate
        it another time with an updated version that provides new features.

        Endpoint: DELETE /api/v1/courses/:course_id/quizzes/:quiz_id/reports/:id

        Reference: https://canvas.instructure.com/doc/api/quiz_reports.html#method.quizzes/quiz_reports.abort
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/quizzes/{}/reports/{}'.format(self.course_id, self.quiz_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return response.status_code == 204

class QuizSubmissionEvent(QuizSubmissionEventModel):

    def __str__(self):
        return '{}'.format(self.event_type)

class QuizSubmissionQuestion(QuizSubmissionQuestionModel):

    def __str__(self):
        return 'QuizSubmissionQuestion #{}'.format(self.id)

    def flag(self, validation_token: 'str | None'=None, **kwargs) -> 'bool':
        """
        Set a flag on a quiz question to indicate that it should be returned to later.

        Endpoint: PUT /api/v1/quiz_submissions/:quiz_submission_id/questions/:id/flag

        Reference: https://canvas.instructure.com/doc/api/quiz_submission_questions.html#method.quizzes/quiz_submission_questions.flag

        Parameters:
            validation_token: str
        """
        try:
            kwargs['validation_token'] = validation_token or self.validation_token
        except AttributeError:
            raise RequiredFieldMissing('`validation_token` not set on this QuizSubmissionQuestion, must be passed as a function argument.')
        kwargs['attempt'] = self.attempt
        response: 'httpx.Response' = self._requester.request('PUT', 'quiz_submissions/{}/questions/{}/flag'.format(self.quiz_submission_id, self.id), _kwargs=combine_kwargs(**kwargs))
        question = response.json()['quiz_submission_questions'][0]
        question.update({'validation_token': kwargs['validation_token'], 'quiz_submission_id': self.quiz_submission_id})
        super(QuizSubmissionQuestion, self).set_attributes(question)
        return True

    async def flag_async(self, validation_token: 'str | None'=None, **kwargs) -> 'bool':
        """
        Set a flag on a quiz question to indicate that it should be returned to later.

        Endpoint: PUT /api/v1/quiz_submissions/:quiz_submission_id/questions/:id/flag

        Reference: https://canvas.instructure.com/doc/api/quiz_submission_questions.html#method.quizzes/quiz_submission_questions.flag

        Parameters:
            validation_token: str
        """
        try:
            kwargs['validation_token'] = validation_token or self.validation_token
        except AttributeError:
            raise RequiredFieldMissing('`validation_token` not set on this QuizSubmissionQuestion, must be passed as a function argument.')
        kwargs['attempt'] = self.attempt
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'quiz_submissions/{}/questions/{}/flag'.format(self.quiz_submission_id, self.id), _kwargs=combine_kwargs(**kwargs))
        question = response.json()['quiz_submission_questions'][0]
        question.update({'validation_token': kwargs['validation_token'], 'quiz_submission_id': self.quiz_submission_id})
        super(QuizSubmissionQuestion, self).set_attributes(question)
        return True

    def unflag(self, validation_token: 'str | None'=None, **kwargs) -> 'bool':
        """
        Remove a previously set flag on a quiz question.

        Endpoint: PUT /api/v1/quiz_submissions/:quiz_submission_id/questions/:id/unflag

        Reference: https://canvas.instructure.com/doc/api/quiz_submission_questions.html#method.quizzes/quiz_submission_questions.unflag

        Parameters:
            validation_token: str
        """
        try:
            kwargs['validation_token'] = validation_token or self.validation_token
        except AttributeError:
            raise RequiredFieldMissing('`validation_token` not set on this QuizSubmissionQuestion, must be passed as a function argument.')
        kwargs['attempt'] = self.attempt
        response: 'httpx.Response' = self._requester.request('PUT', 'quiz_submissions/{}/questions/{}/unflag'.format(self.quiz_submission_id, self.id), _kwargs=combine_kwargs(**kwargs))
        question = response.json()['quiz_submission_questions'][0]
        question.update({'validation_token': kwargs['validation_token'], 'quiz_submission_id': self.quiz_submission_id})
        super(QuizSubmissionQuestion, self).set_attributes(question)
        return True

    async def unflag_async(self, validation_token: 'str | None'=None, **kwargs) -> 'bool':
        """
        Remove a previously set flag on a quiz question.

        Endpoint: PUT /api/v1/quiz_submissions/:quiz_submission_id/questions/:id/unflag

        Reference: https://canvas.instructure.com/doc/api/quiz_submission_questions.html#method.quizzes/quiz_submission_questions.unflag

        Parameters:
            validation_token: str
        """
        try:
            kwargs['validation_token'] = validation_token or self.validation_token
        except AttributeError:
            raise RequiredFieldMissing('`validation_token` not set on this QuizSubmissionQuestion, must be passed as a function argument.')
        kwargs['attempt'] = self.attempt
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'quiz_submissions/{}/questions/{}/unflag'.format(self.quiz_submission_id, self.id), _kwargs=combine_kwargs(**kwargs))
        question = response.json()['quiz_submission_questions'][0]
        question.update({'validation_token': kwargs['validation_token'], 'quiz_submission_id': self.quiz_submission_id})
        super(QuizSubmissionQuestion, self).set_attributes(question)
        return True

class QuizAssignmentOverrideSet(QuizAssignmentOverrideSetModel):

    def __str__(self):
        return 'Overrides for quiz_id {}'.format(self.quiz_id)