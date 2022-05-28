from model.role import RoleBase


class IRoleCreate(RoleBase):
    pass


class IRoleRead(RoleBase):
    id: int


class IRoleUpdate(RoleBase):
    pass
