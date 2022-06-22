from enum import Enum

from model.role import RoleBase


class IRoleCreate(RoleBase):
    pass


class IRoleRead(RoleBase):
    id: int


class IRoleUpdate(RoleBase):
    pass


class IRoleEnum(str, Enum):
    admin = 'admin'
    user = 'user'
