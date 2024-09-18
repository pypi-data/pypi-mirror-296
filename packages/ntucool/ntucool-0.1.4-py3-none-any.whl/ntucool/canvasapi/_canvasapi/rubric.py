from ..models.rubrics import Rubric as RubricModel, RubricAssessment as RubricAssessmentModel, RubricAssociation as RubricAssociationModel
import httpx
import typing
from .canvas_object import CanvasObject
from .util import combine_kwargs

class Rubric(RubricModel):

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)

    def delete(self, **kwargs) -> 'Rubric':
        """
        Delete a Rubric.

        Endpoint: DELETE /api/v1/courses/:course_id/rubrics/:id

        Reference: https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/rubrics/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return Rubric(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'Rubric':
        """
        Delete a Rubric.

        Endpoint: DELETE /api/v1/courses/:course_id/rubrics/:id

        Reference: https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/rubrics/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return Rubric(self._requester, response.json())

class RubricAssessment(RubricAssessmentModel):

    def __str__(self):
        return '{}, {}'.format(self.id, self.artifact_type)

    def delete(self, **kwargs) -> 'RubricAssessment':
        """
        Delete a single RubricAssessment.

        Endpoint: DELETE /api/v1/courses/:course_id/rubric_associations

        Reference: /:rubric_association_id/rubric_assessments/:id         <https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_assessments.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/rubric_associations/{}/rubric_assessments/{}'.format(self.course_id, self.rubric_association_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return RubricAssessment(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'RubricAssessment':
        """
        Delete a single RubricAssessment.

        Endpoint: DELETE /api/v1/courses/:course_id/rubric_associations

        Reference: /:rubric_association_id/rubric_assessments/:id         <https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_assessments.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/rubric_associations/{}/rubric_assessments/{}'.format(self.course_id, self.rubric_association_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return RubricAssessment(self._requester, response.json())

    def update(self, **kwargs) -> 'RubricAssessment':
        """
        Update a single RubricAssessment.

        Endpoint: PUT /api/v1/courses/:course_id/rubric_associations

        Reference: /:rubric_association_id/rubric_assessments/:id         <https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_assessments.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/rubric_associations/{}/rubric_assessments/{}'.format(self.course_id, self.rubric_association_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return RubricAssessment(self._requester, response.json())

    async def update_async(self, **kwargs) -> 'RubricAssessment':
        """
        Update a single RubricAssessment.

        Endpoint: PUT /api/v1/courses/:course_id/rubric_associations

        Reference: /:rubric_association_id/rubric_assessments/:id         <https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_assessments.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/rubric_associations/{}/rubric_assessments/{}'.format(self.course_id, self.rubric_association_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return RubricAssessment(self._requester, response.json())

class RubricAssociation(RubricAssociationModel):

    def __str__(self):
        return '{}, {}'.format(self.id, self.association_type)

    def create_rubric_assessment(self, **kwargs) -> 'RubricAssessment':
        """
        Create a single RubricAssessment.

        Endpoint: POST /api/v1/courses/:course_id/rubric_associations

        Reference: /:rubric_association_id/rubric_assessments         <https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_assessments.create
        """
        response: 'httpx.Response' = self._requester.request('POST', 'courses/{}/rubric_associations/{}/rubric_assessments'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        assessment_json: 'dict' = response.json()
        assessment_json.update({'course_id': self.id})
        return RubricAssessment(self._requester, assessment_json)

    async def create_rubric_assessment_async(self, **kwargs) -> 'RubricAssessment':
        """
        Create a single RubricAssessment.

        Endpoint: POST /api/v1/courses/:course_id/rubric_associations

        Reference: /:rubric_association_id/rubric_assessments         <https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_assessments.create
        """
        response: 'httpx.Response' = await self._requester.request_async('POST', 'courses/{}/rubric_associations/{}/rubric_assessments'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        assessment_json: 'dict' = response.json()
        assessment_json.update({'course_id': self.id})
        return RubricAssessment(self._requester, assessment_json)

    def delete(self, **kwargs) -> 'RubricAssociation':
        """
        Delete a RubricAssociation.

        Endpoint: DELETE /api/v1/courses/:course_id/rubric_associations/:id

        Reference: https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_associations.destroy
        """
        response: 'httpx.Response' = self._requester.request('DELETE', 'courses/{}/rubric_associations/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return RubricAssociation(self._requester, response.json())

    async def delete_async(self, **kwargs) -> 'RubricAssociation':
        """
        Delete a RubricAssociation.

        Endpoint: DELETE /api/v1/courses/:course_id/rubric_associations/:id

        Reference: https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_associations.destroy
        """
        response: 'httpx.Response' = await self._requester.request_async('DELETE', 'courses/{}/rubric_associations/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        return RubricAssociation(self._requester, response.json())

    def update(self, **kwargs) -> 'RubricAssociation':
        """
        Update a RubricAssociation.

        Endpoint: PUT /api/v1/courses/:course_id/rubric_associations/:id

        Reference: https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_associations.update
        """
        response: 'httpx.Response' = self._requester.request('PUT', 'courses/{}/rubric_associations/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        if 'association_type' in response_json:
            super(RubricAssociation, self).set_attributes(response_json)
        return self

    async def update_async(self, **kwargs) -> 'RubricAssociation':
        """
        Update a RubricAssociation.

        Endpoint: PUT /api/v1/courses/:course_id/rubric_associations/:id

        Reference: https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_associations.update
        """
        response: 'httpx.Response' = await self._requester.request_async('PUT', 'courses/{}/rubric_associations/{}'.format(self.course_id, self.id), _kwargs=combine_kwargs(**kwargs))
        response_json: 'dict' = response.json()
        response_json.update({'course_id': self.course_id})
        if 'association_type' in response_json:
            super(RubricAssociation, self).set_attributes(response_json)
        return self