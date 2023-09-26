from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from scraper.auth import login_required
from scraper.db import get_db
from scraper import fetch_data

bp = Blueprint('scraper', __name__)


@bp.route('/')
def index():
    return render_template('scraper/index.html')


@bp.route('/request')
def request():
    # TODO make a json file which you can edit from the webserver which contains all the settings
    site = "https://nl.indeed.com/jobs?q=cyber+security&l=Nederland&fromage=1"
    job_data = fetch_data.WebScraper(f"{site}").main()
    db = get_db()
    for job in job_data:
        try:
            db.execute(
                "INSERT INTO html_job (html) VALUES (?)",
                [job]
            )
            db.commit()
        except db.IntegrityError:
            error = f"Error while adding jobs to the database"
            flash(error)

    return render_template('scraper/request.html')
