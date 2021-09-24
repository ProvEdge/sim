# from typing import List
# from pydantic import BaseModel

# from .generic import ResponseBase

# class OrgUserBase(BaseModel):
#     org_id: int
#     user_id: int

# class OrgUserCreate(OrgUserBase):
#     pass

# class OrgUser(OrgUserBase):

#     class Config:
#         orm_mode = True

# class ListParticipations(ResponseBase):
#     data: List[OrgUser]

# class ParticipationResponse(ResponseBase):
#     data: OrgUser

# class IsMemberData(BaseModel):
#     is_member: bool
#     participation: OrgUser

# class IsMemberResponse(ResponseBase):
#     data: IsMemberData