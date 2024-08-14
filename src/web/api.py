_author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2024. All rights reserved."

from fastapi import FastAPI, Request
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.db.databasemanager import DatabaseManager
from typing import Optional, AnyStr


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

root_id='index'
review_input_id='reviewinput'
permit_officials_id='permitofficials'

@app.get("/", response_class=HTMLResponse)
async def root() -> AnyStr:
    """
    Load the default landing page 'index.html'
    @return: HTML content of the landing page
    @rtype: str
    """
    with open(f"templates/{root_id}.html", 'r') as f:
        html_content = f.read()
    print("loaded index.html")
    return html_content

@app.get(f"/{review_input_id}", response_class=HTMLResponse)
async def query_review_input() -> AnyStr:
    with open(f"templates/{review_input_id}.html", 'r') as f:
        html_content = f.read()
    return html_content

@app.get(f"/{permit_officials_id}", response_class=HTMLResponse)
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
            f"/{permit_officials_id}.html",
            {'request': request, permit_officials_id: permit_officials}
        )
    except Exception as e:
        logging.error({str(e)})
        return templates.TemplateResponse("/index")

""" ----------------------   Supporting helper methods ----------------------- """


def __get_db() -> Optional[DatabaseManager]:
    import logging
    try:
        return DatabaseManager.build()
    except Exception as e:
        logging.error(f'Cannot access database {str(e)}')
        return None
