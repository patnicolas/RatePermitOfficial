_author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2024. All rights reserved."

from fastapi import FastAPI, Request, Form
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.db.databasemanager import DatabaseManager
from typing import Optional, AnyStr
import logging
from src.web.reviewdata import ReviewData





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
query_permit_officials_id='permitofficials'
post_review_id='postreview'
query_reviews_id = "reviews"
query_users_id="users"


""" ------------------  Default landing page ---------------------- """

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

""" -------------------- POST methods -------------------- """

@app.post(f'/{post_review_id}')
async def post_review(review_data: ReviewData) -> templates.TemplateResponse:
    try:
        logging.info(f'Review\n{str(review_data)}')
        database_manager = DatabaseManager.build()
        database_manager.add_review(review_data)
        return HTMLResponse(content=f'Review\n{str(review_data)}\nhas been added to Review table', status_code=200)

    except Exception as e:
        logging.error(f'Post review failed {str(e)}')
        return HTMLResponse(content='Failed', status_code=500)



""" -------------------  GET methods --------------------------- """

@app.get(f"/{review_input_id}", response_class=HTMLResponse)
async def query_review_input() -> AnyStr:
    with open(f"templates/{review_input_id}.html", 'r') as f:
        html_content = f.read()
    return html_content


@app.get(f"/{query_permit_officials_id}", response_class=HTMLResponse)
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
            f"/{query_permit_officials_id}.html",
            {'request': request, query_permit_officials_id: permit_officials}
        )
    except Exception as e:
        logging.error({str(e)})
        return templates.TemplateResponse("/index")


@app.get(f"/{query_users_id}", response_class=HTMLResponse)
async def query_users(request: Request) -> templates.TemplateResponse:
    """
    Query the current list of users for debugging purpose
    :param request: Web HTTP request
    :type request: Request
    :return: HTML response using Jinja2 template
    :rtype: TemplateResponse
    """
    from src.db.user import User
    import logging

    try:
        db_manager = DatabaseManager.build()
        users = db_manager.query(DatabaseManager.q_users, condition= User.id < 1000)
        return templates.TemplateResponse(
            f"/{query_users_id}.html",
            {'request': request, query_users_id: users}
        )
    except Exception as e:
        logging.error({str(e)})
        return templates.TemplateResponse("/index")


@app.get(f"/{query_reviews_id}", response_class=HTMLResponse)
async def query_reviews(request: Request) -> templates.TemplateResponse:
    """
    Query the current list of reviews for debugging purpose
    :param request: Web HTTP request
    :type request: Request
    :return: HTML response using Jinja2 template
    :rtype: TemplateResponse
    """
    from src.db.review import Review
    import logging

    try:
        db_manager = DatabaseManager.build()
        reviews = db_manager.query(DatabaseManager.q_reviews, condition= Review.id < 1000)
        return templates.TemplateResponse(
            f"/{query_reviews_id}.html",
            {'request': request, query_reviews_id: reviews}
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
