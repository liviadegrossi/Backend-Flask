from pydantic import BaseModel

# Used for the user's login
class LoginPayload(BaseModel):
    username: str
    password: str