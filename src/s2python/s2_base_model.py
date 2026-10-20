from pydantic import BaseModel, ConfigDict


class S2BaseModel(BaseModel):
    """Base class of the generated S2 models.

    The validators and serializers of a model are built the first time the model
    is used, instead of when the class is defined. Most applications use only a
    small part of the S2 messages, and building them all costs several MB of
    memory.
    """

    model_config = ConfigDict(defer_build=True)
