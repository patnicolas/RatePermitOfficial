_author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2024. All rights reserved."

from fastapi import FastAPI, Request, Form
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.db.databasemanager import DatabaseManager
from typing import Optional, AnyStr, List
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
    :type request: class Request
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
    :type request: class Request
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
    :type request: class Request
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


@app.get("/plotsX", response_class=HTMLResponse)
async def query_plots_x(request: Request):
    from matplotlib.figure import Figure

    from io import BytesIO
    try:
        fig = Figure()
        ax = fig.subplots()
        ax.plot([1, 2, 3, 4], [10, 20, 25, 30])
        ax.set_title("Sample Plot")
        ax.set_xlabel("X Axis")
        ax.set_ylabel("Y Axis")

        # Save the plot to a BytesIO object
        buf = BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        buf_value = buf.getvalue()
        # data = buf.getvalue().decode("latin1")
        data = buf.getvalue().decode("UTF-8")

        # Create a matplotlib figure
        """
        plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
        plt.title("Sample Plot")
        plt.xlabel("X Axis")
        plt.ylabel("Y Axis")
        plot_filename = "plots/plots.png"
        plt.savefig(fname=plot_filename)
        """




        # Render the HTML template and embed the image
        rendered_images = templates.TemplateResponse("plots.html", {"request": request, "plots": data})
        return rendered_images
    except Exception as e:
        logging.error(f'Query plots failed: {str(e)}')
        return templates.TemplateResponse("/index")


@app.get("/plots", response_class=HTMLResponse)
async def query_plots(request: Request):
    import matplotlib.pyplot as plt
    import numpy as np

    try:
        db_manager = DatabaseManager.build()

        plt.rcParams['font.family'] = 'serif'  # Set the font family
        plt.rcParams['font.serif'] = ['Times New Roman']  # Set the specific font
        plt.rcParams['font.size'] = 8  # Set the font size

        dates, frequencies = get_reviews_profile(db_manager)

        fig, (ax1, ax2) = plt.subplots(2, 1)

        ax1.bar(dates, frequencies, color='magenta', edgecolor='black')
        ax1.set_title("Reviews profile")
        ax1.set_xlabel("Dates")
        ax1.set_ylabel("Number of reviews")

        permit_officials, kips = get_permit_official_metrics(db_manager)
        x = np.arange(len(permit_officials))
        width = 0.2
        bars1 = ax2.bar(x - 1.5*width, kips[0], width, label='Helpfulness')
        bars2 = ax2.bar(x - 0.5 * width, kips[1], width, label='Consistency')
        bars3 = ax2.bar(x + 0.5 * width, kips[2], width, label='Responsiveness')
        bars4 = ax2.bar(x + 1.5 * width,kips[3], width, label='Cost')
        ax2.set_title("Average KPIs")
        ax2.set_xlabel("Permit officials")
        ax2.set_ylabel("KIPs")

        ax2.set_xticks(x)
        ax2.set_xticklabels(permit_officials)
        ax2.legend()


        plot_filename = "static/plots/plots1.png"
        plt.tight_layout()
        plt.savefig(fname=plot_filename)


        # Render the HTML template and embed the image
        rendered_images = templates.TemplateResponse("plots.html", {"request": request})
        return rendered_images
    except Exception as e:
        logging.error(f'Query plots failed: {str(e)}')
        return templates.TemplateResponse("/index")


@staticmethod
def get_reviews_profile(db_manager: DatabaseManager) -> (List[AnyStr], List[int]):
    from src.db.review import Review
    results = db_manager.query(DatabaseManager.q_reviews_profile, Review.id < 1000)
    dates = []
    frequencies = []
    for date, frequency in results:
        dates.append(str(date))
        frequencies.append(int(frequency))
    return dates, frequencies


@staticmethod
def get_permit_official_metrics(db_manager: DatabaseManager) -> (List[AnyStr], List[List[float]]):
    from src.db.review import Review
    from src.db.permitofficial import PermitOfficial

    permit_officials_list = []
    helpfulness_list = []
    consistency_list = []
    responsiveness_list = []
    cost_list = []
    results = db_manager.query(DatabaseManager.q_permit_official_metrics, Review.id < 1000)
    for permit_official_id, avg_helpfulness, avg_consistency, avg_responsiveness, avg_cost in results:
        permit_officials = db_manager.query(
            DatabaseManager.q_permit_officials,
            PermitOfficial.id == permit_official_id)
        permit_officials_list.append(f'{permit_officials[0].last_name}: {permit_officials[0].city}')
        helpfulness_list.append(avg_helpfulness)
        consistency_list.append(avg_consistency)
        responsiveness_list.append(avg_responsiveness)
        cost_list.append(avg_cost)
    return permit_officials_list, [helpfulness_list, consistency_list, responsiveness_list, cost_list]




""" ----------------------   Supporting helper methods ----------------------- """

def __get_db() -> Optional[DatabaseManager]:
    import logging
    try:
        return DatabaseManager.build()
    except Exception as e:
        logging.error(f'Cannot access database {str(e)}')
        return None
