from api.validator.sheets_validator import ShetsData
from imports import APIRouter
from utils.subprocesss import sheets_db

sheets_router = APIRouter()


@sheets_router.get("/sheetsTest")
async def root():
    return sheets_db.get_with_filters(
        fields=['sheet_id', 'marking_time'],
        filters={},
        order_by='sheet_id',
        order_direction='asc',
        page_size=100,
        page_number=1
    )


@sheets_router.post('/api/sheets/get', tags=["Sheets"])
async def get_sheet(
        sheet_data: ShetsData
):
    """
    Получение данных по листам.
    Поля словаря запроса: sheet_ids, fields.
    fields: sheet_id, marking_time, sb_order, cut_part_num, heat, batch, tech_violation_code,
            num_1, grade, carb_eqiv, crack_resist, plate_t, plate_w, plate_l
    Возвращает список словарей.
    """
    return sheets_db.get(
        sheet_ids=sheet_data.sheet_ids,
        fields=sheet_data.fields
    )


@sheets_router.post("/api/sheets/get_with_filtres", tags=["Sheets"])
async def get_sheet_with_filtres(
        sheet_data: ShetsData
):
    """
    Получение данных по листам c фильтрами.
    Поля словаря запроса: filters, order_by, order_direction, page_size, page_number, fields.
    fields: sheet_id, marking_time, sb_order, cut_part_num, heat, batch, tech_violation_code,
            num_1, grade, carb_eqiv, crack_resist, plate_t, plate_w, plate_l
    Возвращает список словарей.
    """
    return sheets_db.get_with_filters(
        filters=sheet_data.filters,
        order_by=sheet_data.order_by,
        order_direction=sheet_data.order_direction,
        page_size=sheet_data.page_size,
        page_number=sheet_data.page_number,
        fields=sheet_data.fields
    )
