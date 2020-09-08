from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from product.db import get_db

bp = Blueprint('product', __name__)

@bp.route('/')
def index():
    db = get_db()
    products = db.execute(
        'SELECT *'
        ' FROM PRODUCT P'
        ' ORDER BY P.id DESC'
    ).fetchall()
    return render_template('product/index.html', products=products)


@bp.route('/add_product', methods=['POST'])
def add_entity_to_db():
    product_id = request.get_json()['id']
    product_gender = request.get_json()['gender']
    product_master_category = request.get_json()['masterCategory']
    product_sub_category = request.get_json()['subCategory']
    product_article_type = request.get_json()['articleType']
    product_base_colour = request.get_json()['baseColour']
    product_season = request.get_json()['season']
    product_year = request.get_json()['year']
    product_usage = request.get_json()['usage']
    product_display_name = request.get_json()['productDisplayName']

    db = get_db()
    error = None

    if not product_id:
        error = 'Product ID is required.'
    elif not product_display_name:
        error = 'Product Display Name is required.'
    else:
        db.execute(
            'INSERT INTO PRODUCT (id, gender, masterCategory, subCategory, articleType, baseColour, season, year, usage, productDisplayName) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (product_id, product_gender, product_master_category, product_sub_category, product_article_type, product_base_colour, product_season, product_year, product_usage, product_display_name)
        )
        db.commit()
        return 'Success!'

    return error