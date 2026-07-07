from api.validator.rolling_task_validator import RollingTaskData
from imports import APIRouter
from utils.subprocesss import rolling_task_db

rolling_task_router = APIRouter()


@rolling_task_router.get("/rollingTaskTest")
async def root():
    return rolling_task_db.get_with_filters(
        fields=['DT_TASK_ROLL', 'TASK_POS'],
        filters={},
        order_by='DT_TASK_ROLL',
        order_direction='DESC',
        page_size=10,
        page_number=1
    )


@rolling_task_router.post("/api/rolling_task/get", tags=["RollingTask"])
async def get_with_filtres(
        rolling_task: RollingTaskData
):
    """
    Фильтрованный поиск наряд-задания
    Поля в словаре запроса: filters, order_by, order_direction, page_number, page_size, fields
    fields: DT_TASK_ROLL, TASK_POS, ORDERS, ORD_POS, GRADE_CODE, GRADE_NAME, PLATE_T, PLATE_W, PLATE_L, GOST_TT
    GOST_XA, GOST_SORT, HEAT, NUM_1, CNT_P, NUM_N, BATCH, INBATCH, KDUP
    """
    return rolling_task_db.get_with_filters(
        filters=rolling_task.filters,
        order_by=rolling_task.order_by,
        order_direction=rolling_task.order_direction,
        page_number=rolling_task.page_number,
        page_size=rolling_task.page_size,
        fields=rolling_task.fields
    )
