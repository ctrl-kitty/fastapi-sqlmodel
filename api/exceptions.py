from pydantic import EmailStr
from fastapi import Request


class BaseAPIException(Exception):
    def __init__(self, message: str):
        self.message = message

# todo exclude message from __dict__
class UserWithThatEmailExistException(BaseAPIException):
    def __init__(self, email: EmailStr):
        super().__init__('User with this email already exists.')
        self.email = email
