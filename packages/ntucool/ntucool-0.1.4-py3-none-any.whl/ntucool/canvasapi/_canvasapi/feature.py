from ..models.feature_flags import Feature as FeatureModel, FeatureFlag as FeatureFlagModel
import httpx
import typing
from .canvas_object import CanvasObject
from .util import combine_kwargs, obj_or_str

class Feature(FeatureModel):

    def __str__(self):
        return '{} {}'.format(self.display_name, self.applies_to)

    @property
    def _parent_id(self) -> 'int':
        """
        Return the id of the account, course or user that spawned this feature
        """
        if hasattr(self, 'account_id'):
            return self.account_id
        elif hasattr(self, 'course_id'):
            return self.course_id
        elif hasattr(self, 'user_id'):
            return self.user_id
        else:
            raise ValueError('Feature Flag does not have account_id, course_id or user_id')

    @property
    def _parent_type(self) -> 'str':
        """
        Return whether the feature with the feature was spawned from an account,
        a course or a user.
        """
        if hasattr(self, 'account_id'):
            return 'account'
        elif hasattr(self, 'course_id'):
            return 'course'
        elif hasattr(self, 'user_id'):
            return 'user'
        else:
            raise ValueError('Feature Flag does not have account_id, course_id or user_id')

class FeatureFlag(FeatureFlagModel):

    def __str__(self):
        return '{} {} {} {}'.format(self.context_type, self.context_id, self.feature, self.state)

    def delete(self, feature, **kwargs) -> 'FeatureFlag':
        """
        Remove a feature flag for a given account, course or user.

        Endpoint: DELETE /api/v1/courses/:course_id/features/flags/:feature             <https://canvas.instructure.com/doc/api/

        Reference: feature_flags.html#method.feature_flags.delete
        """
        feature_name = obj_or_str(feature, 'name', (Feature,))
        response: 'httpx.Response' = self._requester.request('DELETE', '{}s/{}/features/flags/{}'.format(feature._parent_type, feature._parent_id, feature_name), _kwargs=combine_kwargs(**kwargs))
        return FeatureFlag(self._requester, response.json())

    async def delete_async(self, feature, **kwargs) -> 'FeatureFlag':
        """
        Remove a feature flag for a given account, course or user.

        Endpoint: DELETE /api/v1/courses/:course_id/features/flags/:feature             <https://canvas.instructure.com/doc/api/

        Reference: feature_flags.html#method.feature_flags.delete
        """
        feature_name = obj_or_str(feature, 'name', (Feature,))
        response: 'httpx.Response' = await self._requester.request_async('DELETE', '{}s/{}/features/flags/{}'.format(feature._parent_type, feature._parent_id, feature_name), _kwargs=combine_kwargs(**kwargs))
        return FeatureFlag(self._requester, response.json())

    def set_feature_flag(self, feature: 'Feature', **kwargs) -> 'FeatureFlag':
        """
        Set a feature flag for a given account, course or user.

        Endpoint: PUT /api/v1/courses/:course_id/features/flags/:feature             <https://canvas.instructure.com/doc/api/

        Reference: feature_flags.html#method.feature_flags.update

        Parameters:
            feature: :class:`canvasapi.feature.Feature`
        """
        feature_name = obj_or_str(feature, 'name', (Feature,))
        response: 'httpx.Response' = self._requester.request('PUT', '{}s/{}/features/flags/{}'.format(feature._parent_type, feature._parent_id, feature_name), _kwargs=combine_kwargs(**kwargs))
        return FeatureFlag(self._requester, response.json())

    async def set_feature_flag_async(self, feature: 'Feature', **kwargs) -> 'FeatureFlag':
        """
        Set a feature flag for a given account, course or user.

        Endpoint: PUT /api/v1/courses/:course_id/features/flags/:feature             <https://canvas.instructure.com/doc/api/

        Reference: feature_flags.html#method.feature_flags.update

        Parameters:
            feature: :class:`canvasapi.feature.Feature`
        """
        feature_name = obj_or_str(feature, 'name', (Feature,))
        response: 'httpx.Response' = await self._requester.request_async('PUT', '{}s/{}/features/flags/{}'.format(feature._parent_type, feature._parent_id, feature_name), _kwargs=combine_kwargs(**kwargs))
        return FeatureFlag(self._requester, response.json())