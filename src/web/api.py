_author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2024. All rights reserved."

from fastapi import FastAPI, Request
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.web.configparams import configuration_parameters
from src.db.databasemanager import DatabaseManager
from typing import Optional, Any


"""
    Implement the web service to handle HTTP requests
    http://dns_name:{port}/  for landing page defined as index.html
    http://dns_name:{port}/upload for the upload page defined as response.html
"""

app = FastAPI()
base_dir=Path(__file__).parent.parent.absolute()
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "../static"),
    name="static",
)

""" Instantiate JinJa2 template for Request and Response a static variable"""
import os
_dir = os.path.abspath(os.path.expanduser('templates'))
templates = Jinja2Templates(directory=_dir)


@app.get("/", response_class=HTMLResponse)
async def root():
    web_path = configuration_parameters['web_path']
    with open("templates/index.html", 'r') as f:
        html_content = f.read()
    print("loaded index.html")
    return html_content


def get_db() -> Optional[DatabaseManager]:
    import logging
    try:
        return DatabaseManager.build()
    except Exception as e:
        logging.error(f'Cannot access database {str(e)}')
        return None


@app.get("/permitofficials", response_class=HTMLResponse)
async def query_permit_officials(request: Request) -> templates.TemplateResponse:
    """
    Query the current list of permit officials for debugging purpose
    :param request: Web HTTP request
    :type request: Request
    :return: HTML response using Jinja2 template
    :rtype: TemplateResponse
    """
    from src.db.permitofficial import PermitOfficial
    import logging

    try:
        db_manager = DatabaseManager.build()
        permit_officials = db_manager.query(DatabaseManager.q_permit_officials, condition=PermitOfficial.id < 1000)
        return templates.TemplateResponse(
            "/permitofficials.html",
            {'request': request, 'permitofficials': permit_officials}
        )
    except Exception as e:
        logging.error({str(e)})
        return templates.TemplateResponse("/index")

