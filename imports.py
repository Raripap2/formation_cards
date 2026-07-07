"""Системные impotrs"""
import json
import signal
import sys

from fastapi import FastAPI, APIRouter, Path, Query, HTTPException
from fastapi.responses import RedirectResponse

from pydantic import BaseModel, Field
from typing import Optional, Dict

"""Импортирование файлов"""
from utils.db_utils import Sheets, Workers, FormationCards, Logs, RollingTask
from api.workers_api import workers_router
from api.formation_cards_api import formation_cards_router
from api.rolling_task_api import rolling_task_router
from api.sheets_api import sheets_router
from api.HTML_API import pages_router
#from api.auth import auth_router
from utils import LocalStorage
import subprocess