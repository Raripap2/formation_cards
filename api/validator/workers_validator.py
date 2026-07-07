from imports import BaseModel, Optional, Field, Dict

class UserData(BaseModel):
    """Валидация данных"""
    login: Optional[str] = Field(None)
    hash_password: Optional[str] = Field(None)
    order_by: Optional[str] = Field(None)
    page_size: Optional[int] = Field(None)
    page_number: Optional[int] = Field(None)
    status_id: Optional[int] = Field(None)
    user_data: Optional[Dict] = Field(None)
    filtres: Optional[Dict] = Field(None)
    worker_id: Optional[int] = Field(None)
    params: Optional[Dict] = Field(None)
    worker_id_to_edit: Optional[int] = Field(None)
    worker_id_to_delete: Optional[int] = Field(None)
    message: Optional[str] = Field(None)
    fields: Optional[list] = Field(None)
