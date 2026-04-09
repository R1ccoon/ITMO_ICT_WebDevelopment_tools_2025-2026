from pydantic import BaseModel


class TagModel(BaseModel):
    id: int
    user_id: int
    name: str


class TagCreateRequest(BaseModel):
    name: str


class TagListResponse(BaseModel):
    data: list[TagModel]


class TransactionTagBindRequest(BaseModel):
    transaction_id: int
    tag_id: int
    relevance_score: float = 1.0
