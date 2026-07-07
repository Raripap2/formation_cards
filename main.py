import os

from fastapi.staticfiles import StaticFiles

from imports import *

app = FastAPI(title="Formation Cards", version="1.0.0")
app.include_router(workers_router)
app.include_router(rolling_task_router)
app.include_router(sheets_router)
app.include_router(formation_cards_router)
app.include_router(pages_router)
#app.include_router(auth_router)

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "api", "templates", "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

subprocess.run(['python', 'utils/subprocesss.py'])




def main():
    """Значение None или NULL запрещены к передаче в формате строки, т.е. Пользователь не может передавать такие значения при авторизации и т.п."""
    import uvicorn
    # uvicorn main:app --reload
    print('http://127.0.0.1:5000/docs')
    print('http://127.0.0.1:5000/html/allfk')

    uvicorn.run(app, port=5000)


if __name__ == '__main__':
    main()
