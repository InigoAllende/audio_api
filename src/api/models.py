from pydantic import BaseModel, validator


class VolumeAdjustRequest(BaseModel):
    volume_increase: int

    @validator("volume_increase")
    def prevent_zero(cls, v):
        if v == 0:
            raise ValueError(
                "0 is not an allowed value, it will not modify the files volume. Please provide a positive or negative integer."
            )
        return v
