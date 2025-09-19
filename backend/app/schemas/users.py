from pydantic import BaseModel, Field, field_validator


class UserLoginSchema(BaseModel):
    username: str = Field(..., max_length=250, description="username of the user")
    password: str = Field(..., description="password of the user")


class UserRegisterSchema(BaseModel):
    firstname: str = Field(..., max_length=250, description="firstname of the user")
    lastname: str = Field(..., max_length=250, description="lastname of the user")
    username: str = Field(..., max_length=250, description="username of the user")
    password: str = Field(..., description="password of the user")
    password_confirm: str = Field(..., description="confirm password of the user")

    @field_validator("password_confirm")
    def check_passwords_match(cls, password_confirm, validation):
        if not (password_confirm == validation.data.get("password")):
            raise ValueError("passwords doesnt match")
        return password_confirm


class UserRefreshTokenSchema(BaseModel):
    token: str = Field(..., description="refresh token of the user")