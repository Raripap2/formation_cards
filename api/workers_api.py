from api.validator.workers_validator import UserData
from imports import APIRouter
from utils.subprocesss import workers_db

workers_router = APIRouter()


@workers_router.get("/workersTest")
async def root():
    return workers_db._test()


@workers_router.post("/api/workers/create/", tags=["Workers"])
async def create_worker(user_data: UserData):
    """
    API создания рабочего
    Поля словаря запроса: login, hash_password, status_id, worker_id, user_data
    user_data: firstname, lastname, secondname, shift, brigade
    """

    return workers_db.create(
        login=user_data.login,
        hash_password=user_data.hash_password,
        status_id=user_data.status_id,
        user_data=user_data.user_data,
        worker_id=user_data.worker_id
    )


@workers_router.post("/api/workers/get/", tags=["Workers"])
async def get_worker(user_data: UserData):
    """
    API на получение данных рабочего
    Поля словаря запроса: worker_id
    """

    return (workers_db.get(fields=['worker_id', 'firstname', 'lastname', 'secondname', 'brigade', 'shift', 'status_id', 'status_name'],
                           worker_id=user_data.worker_id))


@workers_router.post("/api/workers/get_filtered/", tags=["Workers"])
async def get_worker_filtered(user_data: UserData):
    """
    API на получение данных рабочего
    Поля словаря запроса: worker_id, page_size, page_number, filters
    filters: firstname, lastname, secondname, shift, brigade
    """
    return workers_db.get(
        fields=['worker_id', 'firstname', 'lastname', 'secondname', 'brigade'],
        order_by='worker_id',
        order_direction='ASC',
        page_size=user_data.page_size,
        page_number=user_data.page_number,
        filters=user_data.filtres
    )


@workers_router.post("/api/workers/edit/", tags=["Workers"])
async def edit_worker(user_data: UserData):
    """
    API редактирования данных рабочего
    Поля словаря запроса: login, hash_password, status_id, worker_id, params, message, worker_id_to_edit
    params: firstname, lastname, secondname, shift, brigade
    """

    workers_db.edit(
        login=user_data.login,
        hash_password=user_data.hash_password,
        status_id=user_data.status_id,
        worker_id=user_data.worker_id,
        params=user_data.params,
        message=user_data.message,
        worker_id_to_edit=user_data.worker_id_to_edit
    )
    return {'success': True}


@workers_router.delete("/api/workers/delete", tags=["Workers"])
async def delete_worker(user_data: UserData):
    """
    API удаления рабочего
    Поля словаря запроса: worker_id, worker_id_to_delete
    """

    return workers_db.delete(
        worker_id=user_data.worker_id,
        worker_id_to_delete=user_data.worker_id_to_delete
    )
