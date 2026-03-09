from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId

# Used to validate user's login
class LoginPayload(BaseModel):
    id: Optional[ObjectId] = Field(None, alias='_id')
    username: str
    password: str

    model_config = ConfigDict(
        populate_by_name = True,
        arbitrary_types_allowed = True
    )

# Reads the data from the DB and converts them into a JSON
class UserDBModel(LoginPayload):
    def model_dump(self, *, mode = 'python', include = None, exclude = None, context = None, by_alias = None, exclude_unset = False, exclude_defaults = False, exclude_none = False, exclude_computed_fields = False, round_trip = False, warnings = True, fallback = None, serialize_as_any = False):
        
        user_data =  super().model_dump(mode=mode, include=include, exclude=exclude, context=context, by_alias=by_alias, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none, exclude_computed_fields=exclude_computed_fields, round_trip=round_trip, warnings=warnings, fallback=fallback, serialize_as_any=serialize_as_any)
    
        # converts the id into a string
        if self.id:
            user_data['_id'] = str(user_data['_id'])
        
        return user_data

# Used to update user's login
class UpdateUser(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None