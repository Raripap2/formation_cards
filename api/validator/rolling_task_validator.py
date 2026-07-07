from imports import BaseModel, Field, Optional


class RollingTaskData(BaseModel):
    """Валидация данных"""
    filters: dict = Field(None)
    order_by: str = Field(None)
    order_direction: str = Field(None)
    page_size: int = Field(None)
    page_number: int = Field(None)
    fields: Optional[list[str]] = Field(None)
