import httpx
import typing
import io
import json
import os
from typing import Union
from .util import combine_kwargs
FileOrPathLike = Union[os.PathLike, str, io.IOBase, io.FileIO]
'\nA path or file-like object. May be either a :class:`os.PathLike`, a `str`, or a file-like object\n'

class Uploader(object):
    """
    Upload a file to Canvas.
    """

    def __init__(self, requester, url, file: FileOrPathLike, **kwargs):
        """
        :param requester: The :class:`canvasapi.requester.Requester` to pass requests through.
        :type requester: :class:`canvasapi.requester.Requester`
        :param url: The URL to upload the file to.
        :type url: str
        :param file: A file handler or path of the file to upload.
        :type file: :class:`os.PathLike` or str
        """
        if isinstance(file, (os.PathLike, str)):
            if not os.path.exists(file):
                raise IOError('File {} does not exist.'.format(os.fspath(file)))
            self._using_filename = True
        else:
            self._using_filename = False
        self._requester = requester
        self.url = url
        self.file = file
        self.kwargs = kwargs

    def request_upload_token(self, file: io.FileIO) -> 'tuple':
        """
        Request an upload token.
        """
        self.kwargs['name'] = os.path.basename(file.name)
        self.kwargs['size'] = os.fstat(file.fileno()).st_size
        response: 'httpx.Response' = self._requester.request('POST', self.url, _kwargs=combine_kwargs(**self.kwargs))
        return self.upload(response, file)

    async def request_upload_token_async(self, file: io.FileIO) -> 'tuple':
        """
        Request an upload token.
        """
        self.kwargs['name'] = os.path.basename(file.name)
        self.kwargs['size'] = os.fstat(file.fileno()).st_size
        response: 'httpx.Response' = await self._requester.request_async('POST', self.url, _kwargs=combine_kwargs(**self.kwargs))
        return self.upload(response, file)

    def start(self) -> 'tuple':
        """
        Kick off uploading process. Handles open/closing file if a path
        is passed.
        """
        if self._using_filename:
            with open(self.file, 'rb') as file:
                return self.request_upload_token(file)
        else:
            return self.request_upload_token(self.file)

    async def start_async(self) -> 'tuple':
        """
        Kick off uploading process. Handles open/closing file if a path
        is passed.
        """
        if self._using_filename:
            with open(self.file, 'rb') as file:
                return self.request_upload_token(file)
        else:
            return self.request_upload_token(self.file)

    def upload(self, response: 'httpx.Response', file: FileOrPathLike) -> 'tuple':
        """
        Upload the file.

        Parameters:
            response: httpx.Response
        """
        response: 'dict' = response.json()
        if not response.get('upload_url'):
            raise ValueError('Bad API response. No upload_url.')
        if not response.get('upload_params'):
            raise ValueError('Bad API response. No upload_params.')
        kwargs = response.get('upload_params')
        response: 'httpx.Response' = self._requester.request('POST', use_auth=False, _url=response.get('upload_url'), file=file, _kwargs=combine_kwargs(**kwargs))
        response_json = json.loads(response.text.lstrip('while(1);'))
        return ('url' in response_json, response_json)

    async def upload_async(self, response: 'httpx.Response', file: FileOrPathLike) -> 'tuple':
        """
        Upload the file.

        Parameters:
            response: httpx.Response
        """
        response: 'dict' = response.json()
        if not response.get('upload_url'):
            raise ValueError('Bad API response. No upload_url.')
        if not response.get('upload_params'):
            raise ValueError('Bad API response. No upload_params.')
        kwargs = response.get('upload_params')
        response: 'httpx.Response' = await self._requester.request_async('POST', use_auth=False, _url=response.get('upload_url'), file=file, _kwargs=combine_kwargs(**kwargs))
        response_json = json.loads(response.text.lstrip('while(1);'))
        return ('url' in response_json, response_json)