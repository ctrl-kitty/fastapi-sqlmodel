from typing import List
from pydantic import EmailStr


class BaseAPIException(Exception):
    def __init__(self, message: str):
        self.message = message
        self.status_code = 501


class UserWithThatEmailExistException(BaseAPIException):
    def __init__(self, email: EmailStr):
        super().__init__('User with this email already exists.')
        self.email = email
        self.status_code = 400


class UserWithThatEmailNotFoundException(BaseAPIException):
    def __init__(self, email: EmailStr):
        super().__init__('User with that email not found.')
        self.email = email
        self.status_code = 400


class UserWithThatUserIdNotFoundException(BaseAPIException):
    def __init__(self, user_id: int):
        super().__init__('User with that id not found.')
        self.user_id = user_id
        self.status_code = 400


class IncorrectPasswordException(BaseAPIException):
    def __init__(self, email: EmailStr):
        super().__init__('Invalid password.')
        self.email = email
        self.status_code = 401


class InvalidCredentialsException(BaseAPIException):
    def __init__(self, token: str):
        super().__init__('Could not validate credentials.')
        self.token = token
        self.status_code = 403


class InactiveUserException(BaseAPIException):
    def __init__(self, user_id: int):
        super().__init__('Inactive user.')
        self.user_id = user_id
        self.status_code = 400


class InvalidRoleException(BaseAPIException):
    def __init__(self, req_roles: List[str]):
        super().__init__(f'Role "{req_roles}" is required to perform this action.')
        self.required_roles = req_roles
        self.status_code = 403


