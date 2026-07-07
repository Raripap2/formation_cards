from imports import BaseModel, Optional, Field, Dict

class FormationCardData(BaseModel):
    """Валидация данных"""
    card_id: int = Field(None)
    fields: Optional[list[str]] = Field(None)
    order_id: str = Field(None)
    way: str = Field(None)
    params: Dict = Field(None)
    sheet_id: str = Field(None)
    sheet_ids: list[str] = Field(None)
    filters: dict = Field(None)
    order_by: str = Field(None)
    order_direction: str = Field(None)
    page_size: int = Field(None)
    page_number: int = Field(None)
    join_: dict = Field(None)
    worker_id: int = Field(None)
    message: str = Field(None)