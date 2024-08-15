_author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2024. All rights reserved."

from fastapi import FastAPI, Request, Form
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.db.databasemanager import DatabaseManager
from typing import Optional, AnyStr, NoReturn
import logging
from pydantic import BaseModel
from db.kpi import KPI
from db.review import Review
from db.permitofficial import PermitOfficial


class ReviewData(BaseModel):
    permitofficial: str
    permit: str
    helpfulness: int
    consistency: int
    responsiveness: int
    cost: int
    comment: str

    def __str__(self) -> AnyStr:
        return f'\nOfficial: {self.permitofficial}' \
               f'\nHelpfulness: {self.helpfulness}' \
               f'\nConsistency: {self.consistency}' \
               f'\nResponsiveness:  {self.responsiveness}' \
               f'\nConst:  {self.cost}' \
               f'\nComments:\n {self.comment[0: 64]}... '



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
post_review_id='postreview'


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
    import datetime
    try:
        logging.info(f'Review\n{str(review_data)}')

        """
        content: typing.Any = None,
        status_code: int = 200,
        headers: typing.Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None
        """
        database_manager = DatabaseManager.create_database_manager()
        logging.info(f'Initialize database: {str(database_manager)}')
        kpi_entry = KPI(
            helpfulness=review_data.helpfulness,
            consistency=review_data.consistency,
            responsiveness=review_data.responsiveness,
            cost=review_data.cost)
        kpi_entry_resp = database_manager.add(kpi_entry)
        kpi_id = kpi_entry_resp.id

        official_id = database_manager.query(
            DatabaseManager.q_permit_official_id,
            PermitOfficial.last_name == review_data.permitofficial
        )

        official_id = database_manager.query
        review_entry = Review(
            date=datetime.datetime.now(),
            user_name='Patrick',
            permit=review_data.permit,
            comment=review_data.comment,
            kpi_id=kpi_id,
            permit_official_id=official_id
        )
        database_manager.add(review_entry)
        return HTMLResponse(content='New review has been added to Review table', status_code=200)

    except Exception as e:
        logging.error(f'Post review failed {str(e)}')
        return HTMLResponse(content='Failed', status_code=500)



""" -------------------  GET methods --------------------------- """

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
