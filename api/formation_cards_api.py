from api.validator.formation_cards_validator import FormationCardData
from imports import APIRouter, Query, HTTPException, Path
from utils.subprocesss import formation_cards_db


formation_cards_router = APIRouter()


@formation_cards_router.get("/formationCardsTest")
async def root():
    return formation_cards_db.get_with_filters(
        fields=['card_id', 'order_id'],
        filters={},
        order_by='card_id',
        order_direction='asc',
        page_size=100,
        page_number=1
    )


@formation_cards_router.post("/api/formation_cards/get", tags=["Formation_cards"])
async def get_formation_cards_with_filtres(
        card_data: FormationCardData
):
    """
    Поиск фк по фильтрам
    Поля в словаре запроса: fields, filters, order_by, order_direction, page_size, page_number
    Возвращает массив словарей с переданными полями
    """
    return formation_cards_db.get_with_filters(
        fields=card_data.fields,
        filters=card_data.filters,
        order_by=card_data.order_by,
        order_direction=card_data.order_direction,
        page_size=card_data.page_size,
        page_number=card_data.page_number,
        join_={'formation_cards_info': 'card_id'}
    )


@formation_cards_router.post("/api/formation_cards/create", tags=["Formation_cards"])
async def create_formation_card(
        card_data: FormationCardData
):
    """
    Создание фк.
    Поля в словаре запроса: order_id, way, worker_id, params.
    params: fc_gost_tt, fc_gost_xa, fc_gost_sort, shipment_date, wagon_num, group_num, certificate, position.
    """
    return {"card_id": formation_cards_db.create(
        order_id=card_data.order_id,
        way=card_data.way,
        worker_id=card_data.worker_id,
        params=card_data.params
    )}


@formation_cards_router.post("/api/formation_cards/get/{card_id}", tags=["Formation_cards"])
async def get_formation_card(
        card_data: FormationCardData,
        card_id: int = Path()
):
    """
    Получение данных о конкретной ФК.
    Поля в словаре запроса: fields.
    Возвращает словарь с переданными полями.
    """
    return formation_cards_db.get_card(
        card_id=card_id,
        fields=card_data.fields
    )


@formation_cards_router.post("/api/formation_cards/get/{card_id}/sheets", tags=["Formation_cards"])
async def get_formation_card(
        card_id: int,
):
    """
    Получение данных о конкретной ФК.
    Возвращает словарь с переданными полями.
    """
    return formation_cards_db.get_sheets_by_card(
        card_id=card_id,
        fields=['sheet_id', 'marking_time', 'sb_order', 'cut_part_num', 'heat',
                'batch', 'tech_violation_code', 'num_1', 'grade', 'carb_eqiv',
                'crack_resist', 'plate_t', 'plate_w', 'plate_l', 'departed']
    )


@formation_cards_router.put("/api/formation_cards/edit/{card_id}", tags=["Formation_cards"])
async def edit_formation_card(
        card_id: int,
        card_data: FormationCardData
):
    """
    Редактирование фк.
    Поля в словаре запроса: card_id, worker_id, params, message.
    params: fc_gost_tt, fc_gost_xa, fc_gost_sort, shipment_date, wagon_num, group_num, certificate, position.
    """
    formation_cards_db.edit(
        card_id=card_id,
        worker_id=card_data.worker_id,
        message=card_data.message,
        params=card_data.params
    )
    return {"message": f"Карточка {card_id} отредактирована."}


@formation_cards_router.put("/api/formation_cards/add_sheet/{card_id}", tags=["Formation_cards"])
async def add_sheet_to_card(
        card_id: int,
        sheet_data: FormationCardData,
        worker_id: int = Query(None)
):
    """
    Привязка листа к ФК.
    Поля в словаре запроса: sheet_ids
    """
    if not sheet_data.sheet_ids:
        raise HTTPException(
            status_code=400,
            detail="Параметр sheet_id не может быть пустым.",
            headers={"X-Error": "Bad Request"}
        )
    formation_cards_db.add_sheet(
        card_id=card_id,
        sheet_ids=sheet_data.sheet_ids,
        worker_id=worker_id
    )
    if len(sheet_data.sheet_ids) > 1:
        return {"message": f"Листы {', '.join(str(i) for i in sheet_data.sheet_ids)} привязаны к карточке {card_id}."}
    return {"message": f"Лист {', '.join(str(i) for i in sheet_data.sheet_ids)} привязан к карточке {card_id}."}


@formation_cards_router.delete("/api/formation_cards/delete_sheet", tags=["Formation_cards"])
async def delete_sheet_from_card(
        card_id: int = Query(None),
        sheet_id: str = Query(None),
        worker_id: int = Query(None)
):
    """
    Отвязка листа от ФК.
    """
    if card_id and not sheet_id:
        formation_cards_db.delete_sheets_by_card(
            card_id=card_id,
            worker_id=worker_id
        )
        return {"message": f"Все листы отвязаны от карточки {card_id}."}
    elif card_id and sheet_id:
        formation_cards_db.delete_sheet(
            sheet_id=sheet_id,
            card_id=card_id,
            worker_id=worker_id
        )
        return {"message": f"Лист {sheet_id} отвязан от карточки"}
    raise HTTPException(
        status_code=400,
        detail="Должен быть передан или card_id или sheet_id.",
        headers={"X-Error": "Bad Request"}
    )


@formation_cards_router.put("/api/formation_cards/close/{card_id}", tags=["Formation_cards"])
async def close_card(
        card_id: int,
        worker_id: int = Query(None)
):
    """
    Закрытие ФК
    """
    formation_cards_db.close_card(
        card_id=card_id,
        worker_id=worker_id
    )
    return {"message": f"Карточка {card_id} закрыта."}


@formation_cards_router.delete("/api/formation_cards/delete/{card_id}", tags=["Formation_cards"])
async def delete_card(
        card_id: int,
        worker_id: int = Query(None)
):
    """
    Отвязка всех листов и удаление карточки
    """
    formation_cards_db.delete_sheets_by_card(
        card_id=card_id,
        worker_id=worker_id
    )
    formation_cards_db.delete(
        card_id=card_id,
        worker_id=worker_id
    )
    return {"message": f"Карточка {card_id} удалена."}
