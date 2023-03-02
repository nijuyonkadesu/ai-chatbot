from datetime import datetime
from pydantic import BaseModel
import uuid


# For each message inside message[],
# this is the schema
class Message(BaseModel):
    id = str(uuid.uuid4())
    msg: str
    timestamp = str(datetime.now())
