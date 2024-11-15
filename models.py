from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class StudentInfo(BaseModel):
    name: str | None
    dob: str | None
    ad_no: str | None
    uni_reg_no: str | None
    aadhar: str | None
    img_src: str | None
