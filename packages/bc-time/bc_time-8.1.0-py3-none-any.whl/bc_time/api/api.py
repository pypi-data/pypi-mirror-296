from os.path import exists as path_exists
from pathlib import Path
from json import dumps as json_dumps
from requests import post as requests_post, get as requests_get, codes as requests_status_codes
from configparser import ConfigParser
from bc_time.system.encryption.crypt import Crypt
from bc_time.system.validate import Validate
from bc_time.requests.base import Base as RequestsBase
from bc_time.oauth2.token import Token
from bc_time.api.constants.api import Api as ApiConstant
from bc_time.api.enumerators.content_type import ContentType

class Api(RequestsBase):
    # Private
    __crypt = None
    __token = None

    # Public
    client_id = None
    client_secret = None
    crypt_key = None
    grant_type = None
    code = None
    private_key_file_path = None
    time_domain = None

    @property
    def oauth2_token_url(self) -> str:
        return self.time_domain + ApiConstant.OAUTH2_TOKEN_URL_PATH

    @property
    def oauth2_authorise_url(self) -> str:
        return self.time_domain + ApiConstant.OAUTH2_AUTHORISE_URL_PATH

    @property
    def api_url(self) -> str:
        return self.time_domain + ApiConstant.API_URL_PATH

    @property
    def crypt(self) -> Crypt:
        if self.__crypt is None:
            self.__crypt = Crypt(key=self.crypt_key)
        return self.__crypt

    @property
    def token(self):
        if self.__token is None:
            self.__token = Token(
                client_id=self.client_id,
                client_secret=self.client_secret,
                crypt_key=self.crypt_key,
                grant_type=self.grant_type,
                code=self.code,
                private_key_file_path=self.private_key_file_path,
                oauth2_token_url=self.oauth2_token_url
            )
        return self.__token

    def __init__(self, client_id: str=None, client_secret: str=None, crypt_key: str=None, grant_type: str=None, code: str=None, private_key_file_path: str=None, time_domain: str=None) -> None:
        self.__init_config_from_file()
        if client_id is not None:
            self.client_id = client_id
        if client_secret is not None:
            self.client_secret = client_secret
        if crypt_key is not None:
            self.crypt_key = crypt_key
        if grant_type is not None:
            self.grant_type = grant_type
        if code is not None:
            self.code = code
        if private_key_file_path is not None:
            self.private_key_file_path = private_key_file_path
        if time_domain is not None:
            self.time_domain = time_domain
        self.__init_time_domain()
        self.token.crypt = self.crypt

    def __init_config_from_file(self, file_path: str='.bc_time/config', section: str='default') -> None:
        time_config_file_path = self.__get_time_config_file_path(file_path=file_path)
        if time_config_file_path is None:
            return
        config_parser = ConfigParser(inline_comment_prefixes=';')
        config_parser.read(time_config_file_path)
        if section not in config_parser:
            return
        config_data_keys_and_attributes = ['client_id', 'client_secret', 'crypt_key', 'grant_type', 'private_key_file_path', 'time_domain']
        for config_data_key_or_attribute in config_data_keys_and_attributes:
            if config_data_key_or_attribute in config_parser[section]:
                setattr(
                    self,
                    config_data_key_or_attribute,
                    config_parser[section][config_data_key_or_attribute]
                )

    def __get_time_config_file_path(self, file_path: str) -> str|None:
        time_config_file_path = f"{str(Path.home())}/{file_path}"
        if  path_exists(time_config_file_path):
            return time_config_file_path
        # Legacy code - accommodate previous config filename.
        time_config_file_path = f"{str(Path.home())}/.bc_time/credentials"
        return time_config_file_path if path_exists(time_config_file_path) else None

    def __init_time_domain(self) -> None:
        try:
            if self.time_domain is None:
                self.time_domain = ApiConstant.TIME_DOMAIN
            http_secure_type = {
                'type': self.__get_http_data(secure=True, qualified=True),
                'length': self.__get_http_data(secure=True, qualified=True, length=True),
            }
            http_unsecure_type = {
                'type': self.__get_http_data(secure=False, qualified=True),
                'length': self.__get_http_data(secure=False, qualified=True, length=True),
            }
            if self.time_domain[0:http_secure_type['length']] != http_secure_type['type'] \
            and self.time_domain[0:http_unsecure_type['length']] != http_unsecure_type['type']:
                self.time_domain = http_secure_type['type'] + self.time_domain
        finally:
            time_domain_length = len(self.time_domain)
            if self.time_domain[time_domain_length-1:1] == '/':
                self.time_domain = self.time_domain[0:time_domain_length-1]

    def __get_http_data(self, secure: bool=False, qualified: bool=True, length: bool=False) -> str|int:
        http_data = 'http'
        if secure:
            http_data += 's'
        if qualified:
            http_data += '://'
        return http_data if not length else len(http_data)

    def create(self, content_type_id: ContentType, payload: dict, content_uid: int=None) -> dict:
        request_token_result, request_token_response_data = self.token.request_token()
        if not request_token_result:
            return request_token_response_data
        create_payload = self.__get_create_or_update_data(
            content_type_id=content_type_id,
            payload=payload,
            content_uid=content_uid
        )
        post_response = requests_post(
            url=self.api_url,
            data=create_payload
        )
        return self._get_response_data(post_response.text) if post_response.status_code == requests_status_codes.ok else None

    def update(self, content_type_id: ContentType, content_uid: int, payload: dict) -> dict:
        request_token_result, request_token_response_data = self.token.request_token()
        if not request_token_result:
            return request_token_response_data
        update_payload = self.__get_create_or_update_data(
            content_type_id,
            content_uid=content_uid,
            payload=payload
        )
        post_response = requests_post(
            url=self.api_url,
            data=update_payload
        )
        return self._get_response_data(post_response.text) if post_response.status_code == requests_status_codes.ok else None

    def __get_create_or_update_data(self, content_type_id: ContentType, payload: dict, content_uid: int=None) -> dict:
        data = {'content_type_id': int(content_type_id)}
        if content_uid: # Will be omitted if performing POST (1 new object).
            data['content_uid'] = content_uid
        if payload:
            if content_uid != ApiConstant.UID_POST_MANY:
                data.update(payload)
            else:
                data['data'] = payload
        create_or_update_payload = {'access_token': self.token.token}
        if self.crypt_key is not None:
            self.crypt.data = json_dumps(data)
            create_or_update_payload['data'] = self.crypt.encrypt()
        else:
            create_or_update_payload.update(data)
        return create_or_update_payload

    def get_all_using_pagination(self, content_type_id: ContentType, content_uid: int=ApiConstant.UID_GET_ALL, filters: dict=None, page: int=1, row_count: int=ApiConstant.DEFAULT_ROW_COUNT) -> dict:
        if not self.token.request_token():
            return None
        request_params = self.__get_request_params(
            content_type_id=content_type_id,
            content_uids=[content_uid],
            filters=filters,
            page=page,
            row_count=row_count
        )
        request_response = requests_get(
            url=self.api_url,
            params=request_params
        )
        return self._get_response_data(request_response.text) if request_response.status_code == requests_status_codes.ok else None

    def get_one(self, content_type_id: ContentType, content_uid: int) -> dict:
        if not self.token.request_token():
            return None
        request_params = self.__get_request_params(content_type_id, content_uids=[content_uid])
        request_response = requests_get(
            url=self.api_url,
            params=request_params
        )
        return self._get_response_data(request_response.text) if request_response.status_code == requests_status_codes.ok else None

    def get_many(self, content_type_id: ContentType, content_uids: list) -> dict:
        if not self.token.request_token():
            return None
        request_params = self.__get_request_params(content_type_id, content_uids)
        request_response = requests_get(
            url=self.api_url,
            params=request_params
        )
        return self._get_response_data(request_response.text) if request_response.status_code == requests_status_codes.ok else None

    def __get_request_params(self, content_type_id: ContentType, content_uids: list=None, filters: dict=None, page: int=None, row_count: int=None) -> dict:
        data = {
            'content_type_id': int(content_type_id),
            'content_uid': content_uids[0] if len(content_uids) == 1 else ','.join([str(content_uid) for content_uid in content_uids]),
        }
        if self.__can_paginate(page, row_count):
            data['page'] = page
            data['row_count'] = row_count
        if filters is not None:
            data.update(filters)
        request_params = {'access_token': self.token.token}
        if self.crypt_key is not None:
            self.crypt.data = json_dumps(data)
            request_params['data'] = self.crypt.encrypt()
        else:
            request_params.update(data)
        return request_params

    def __can_paginate(self, page: int, row_count: int) -> bool:
        if not Validate.is_numeric(page, min=1):
            return False
        return Validate.is_numeric(row_count, min=1, max=ApiConstant.DEFAULT_ROW_COUNT)