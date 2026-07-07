from imports import BaseModel, Field, Optional


class ShetsData(BaseModel):
    """Валидация данных"""
    sheet_ids: list[str] = Field(None)
    worker_id: int = Field(None)
    fields: Optional[list[str]] = Field(None)
    filters: dict = Field(None)
    order_by: str = Field(None)
    order_direction: str = Field(None)
    page_size: int = Field(None)
    page_number: int = Field(None)
