from app.models.domain.rwmodel import RWModel


class RWSchema(RWModel):
    status: int

    class Config(RWModel.Config):
        orm_mode = True
