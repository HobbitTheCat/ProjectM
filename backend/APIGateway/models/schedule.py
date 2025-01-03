
    class Config:
        schema_extra = {
            "example": {
                "teacher": "GILLET ANNABELLE"
            }
        }

class Group(BaseModel):
    group: str

    class Config:
        schema_extra = {
            "example": {
                "group": "PC3"
            }
        }

class Schedule(BaseModel):
    summary: str
    location: List[Location]
    teacher: Optional[List[Teacher]] = None
    group: Optional[List[Group]] = None

    class Config:
        schema_extra = {
            "examples": {
                "summary": "Phys3B",
                "location": ["A104", "A105"],
                "teacher": ["GILLET ANNABELLE"],
                "group": ["PC3"]
            }
        }