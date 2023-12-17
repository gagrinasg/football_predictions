from pydantic import BaseModel

class FootballAPIPlayer(BaseModel):
    id: int
    name: str
    position: str
    # Add more fields as needed

class FootballAPIResponse(BaseModel):
    players: list[FootballAPIPlayer]
    # Add more fields as needed
