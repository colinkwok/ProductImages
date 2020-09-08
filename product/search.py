from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from product.db import get_db

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/keyword', methods=['POST'])
def search_by_keyword():
    if request.method == 'POST':
        search_field = request.form['search']

    db = get_db()
    error = None

    if search_field is None:
        error = 'Search keyword is required'
    else:
        keywords = search_field.split()

        results = []
        for keyword in keywords:
            keyword = f'%{keyword}%'
            result = db.execute(
                'SELECT * FROM PRODUCT P WHERE id LIKE ? OR gender LIKE ? OR masterCategory LIKE ? OR subCategory LIKE ? OR articleType LIKE ? OR baseColour LIKE ? OR season LIKE ? OR year LIKE ? OR usage LIKE ? OR productDisplayName LIKE ?',
                (keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword,)
            ).fetchall()
            results = results + result

        # remove duplicate products
        results = list(dict.fromkeys(results))

        return render_template('search/index.html', query=search_field, products=results)


def get_product(product_id):
    product = get_db().execute(
        'SELECT * FROM PRODUCT P WHERE P.id = ?',
        (product_id,)
    ).fetchone()

    if product is None:
        abort(404, f'Product id {id} does not exist.')
    return product


@bp.route('/<int:id>/similar', methods=['POST'])
def search_by_similarity(id):

    product = get_product(id)
    query_id = product[0]
    query_product_name = product[9]

    if request.method == 'POST':
        if product is None:
            error = 'Product Info is required'
        else:
            db = get_db()
            error = None

            product_id = product[0]
            product_gender = product[1]
            product_article_type = product[4]

            results = db.execute(
                'SELECT * FROM PRODUCT P WHERE id <> ? AND gender = ? AND articleType LIKE ?',
                (product_id, product_gender, product_article_type)
            ).fetchall()

            # remove duplicate products
            results = list(dict.fromkeys(results))

            return render_template('search/index.html', query_id=query_id, query_product_name=query_product_name, products=results)