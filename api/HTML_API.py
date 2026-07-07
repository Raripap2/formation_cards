from imports import APIRouter, json
import os
from pathlib import Path
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, APIRouter, Request
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path as FilePath
pages_router = APIRouter()



@pages_router.get("/html/allusers/", response_class=HTMLResponse, tags=["HTML"])
async def get_all_users_page():
    """Endpoint для получения HTML страницы"""
    html_file = Path(f"api/templates/All_user.html")

    if not html_file.exists():
        error_content = "<h1>404 - Page not found</h1><p>All_user.html not found in templates directory</p>"
        return HTMLResponse(content=error_content, status_code=404)

    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    return HTMLResponse(content=html_content, status_code=200)


@pages_router.get("/html/current_user/", response_class=HTMLResponse, tags=["HTML"])
async def get_user_page(request: Request, id: int):
    """Endpoint для страницы конкретного пользователя"""
    html_file = Path(f"api/templates/current_user.html")

    if not html_file.exists():
        return HTMLResponse(
            content="<h1>404 - Страница не найдена</h1>",
            status_code=404
        )

    # Читаем HTML шаблон
    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    return HTMLResponse(content=html_content)


@pages_router.get("/html/allsheets/", response_class=HTMLResponse, tags=["HTML"])
async def get_all_sheets_page():
    """Endpoint для получения HTML страницы"""
    html_file = Path(f"api/templates/All_sheets.html")

    if not html_file.exists():
        error_content = "<h1>404 - Page not found</h1><p>All_user.html not found in templates directory</p>"
        return HTMLResponse(content=error_content, status_code=404)

    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    return HTMLResponse(content=html_content, status_code=200)

@pages_router.get("/html/current_sheet/", response_class=HTMLResponse, tags=["HTML"])
async def get_sheet_page(request: Request, id: str):
    """Endpoint для страницы конкретного пользователя"""
    html_file = Path(f"api/templates/current_sheet.html")

    if not html_file.exists():
        return HTMLResponse(
            content="<h1>404 - Страница не найдена</h1>",
            status_code=404
        )

    # Читаем HTML шаблон
    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    return HTMLResponse(content=html_content)

@pages_router.get("/html/allfk/", response_class=HTMLResponse, tags=["HTML"])
async def get_all_sheets_page():
    """Endpoint для получения HTML страницы"""
    html_file = Path(f"api/templates/All_fk.html")

    if not html_file.exists():
        error_content = "<h1>404 - Page not found</h1><p>All_user.html not found in templates directory</p>"
        return HTMLResponse(content=error_content, status_code=404)

    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    return HTMLResponse(content=html_content, status_code=200)

@pages_router.get("/html/current_fk/", response_class=HTMLResponse, tags=["HTML"])
async def get_sheet_page(request: Request, id: int):
    """Endpoint для страницы конкретного пользователя"""
    html_file = Path(f"api/templates/current_fk.html")

    if not html_file.exists():
        return HTMLResponse(
            content="<h1>404 - Страница не найдена</h1>",
            status_code=404
        )

    # Читаем HTML шаблон
    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    return HTMLResponse(content=html_content)

@pages_router.get("/html/sheets/", response_class=HTMLResponse, tags=["HTML"])
async def get_all_sheets_page():
    """Endpoint для получения HTML страницы"""
    html_file = Path(f"api/templates/sheets_to_add.html")

    if not html_file.exists():
        error_content = "<h1>404 - Page not found</h1><p>All_user.html not found in templates directory</p>"
        return HTMLResponse(content=error_content, status_code=404)

    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    return HTMLResponse(content=html_content, status_code=200)



@pages_router.get("/html/index/", response_class=HTMLResponse)
async def get_index_page():
    """Endpoint для получения HTML страницы"""
    html_file = Path("api/templates/index.html")

    if not html_file.exists():
        error_content = "<h1>404 - Page not found</h1><p>index.html not found in templates directory</p>"
        return HTMLResponse(content=error_content, status_code=404)

    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    return HTMLResponse(content=html_content, status_code=200)


@pages_router.get("/html/closed_fk/", response_class=HTMLResponse, tags=["HTML"])
async def get_closed_fk_page():
    """Страница поиска закрытых ФК"""
    html_file = Path("api/templates/closed_fk_search.html")

    if not html_file.exists():
        return HTMLResponse(
            content="<h1>404 - Страница не найдена</h1>",
            status_code=404
        )

    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    return HTMLResponse(content=html_content, status_code=200)


@pages_router.get("/html/closed_fk_view/", response_class=HTMLResponse, tags=["HTML"])
async def get_closed_fk_view_page(request: Request, id: int):
    """Страница просмотра закрытой ФК"""
    html_file = Path("api/templates/closed_fk_view.html")

    if not html_file.exists():
        return HTMLResponse(
            content="<h1>404 - Страница не найдена</h1>",
            status_code=404
        )

    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    return HTMLResponse(content=html_content)