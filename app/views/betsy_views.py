from flask import Blueprint, render_template, request, redirect, g, url_for
from .public_views import login_required

bp = Blueprint("betsy", __name__, url_prefix="/betsy")


@bp.route("/")
@login_required
def betsy():
    return render_template("user/betsy.html")


@bp.route("/search_product", methods=("GET", "POST"))
@login_required
def search_product():
    res = []
    if request.method == "POST":
        term = request.form["term"].lower()

        from ..database.models.functions.betsy_functions import search_product
        res = search_product(term)

    return render_template("user/betsy/search_product.html", res=res)


@bp.route("/list_user_products", methods=("GET", "POST"))
@login_required
def list_user_products():
    res = []
    if request.method == "POST":
        user_id = request.form["user_id"]

        from ..database.models.functions.betsy_functions import list_user_products
        res = list_user_products(user_id)

    return render_template("user/betsy/search_user_products.html", res=res)


@bp.route("/list_product_by_tag", methods=("GET", "POST"))
@login_required
def list_product_by_tag():
    res = []
    if request.method == "POST":
        tag_id = request.form["tag_id"]

        from ..database.models.functions.betsy_functions import list_products_per_tag
        res = list_products_per_tag(tag_id)

    return render_template("user/betsy/list_products_by_tag.html", res=res)


@bp.route("/add_product", methods=("GET", "POST"))
@login_required
def add_product():
    res = []
    checked_tags = []
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        quantity = request.form["quantity"]

        from ..database.models.functions.betsy_functions import read_tags
        tags = read_tags()
        for item in tags:
            if request.form.get(item.tag):
                checked_tags.append(item.taid)

        from ..database.models.functions.betsy_functions import add_product
        res = add_product(g.user.id, name, description,
                          price, quantity, checked_tags)

        return redirect(url_for("betsy.update_product"))

    from ..database.models.functions.betsy_functions import read_tags
    tags = read_tags()

    return render_template("user/betsy/add_product.html", res=res, tags=tags)


@bp.route("/show_product", methods=("GET", "POST"))
@login_required
def show_product():
    res = []

    from ..database.models.functions.betsy_functions import get_all_products_by_user
    res = get_all_products_by_user(g.user.id)

    return render_template("user/betsy/remove_product.html", res=res)


@bp.route("/update_product", methods=("GET", "POST"))
@login_required
def update_product():
    res = []

    from ..database.models.functions.betsy_functions import get_all_products_by_user
    res = get_all_products_by_user(g.user.id)

    return render_template("user/betsy/update_stock_quantity.html", res=res)


@bp.route("/<name>/remove_product/", methods=("POST",))
@login_required
def remove_product(name):

    from ..database.models.functions.betsy_functions import delete_product
    delete_product(name)

    return redirect(url_for("betsy.show_product"))


@bp.route("/<id>/update_quantity", methods=("POST",))
@login_required
def update_quantity(id):

    if request.method == "POST":
        quantity = request.form["quantity"]

    from ..database.models.functions.betsy_functions import update_stock
    update_stock(id, quantity)

    return redirect(url_for("betsy.update_product"))


@bp.route("/handle_purchase", methods=("GET", "POST"))
@login_required
def handle_purchase():
    res = []
    if request.method == "POST":
        term = request.form["term"].lower()

        from ..database.models.functions.betsy_functions import search_product
        res = search_product(term)

    return render_template("user/betsy/handle_purchase.html", res=res)


@bp.route("/<product_id>/buy_product", methods=("GET", "POST"))
@login_required
def buy_product(product_id):

    if request.method == "POST":
        quantity = request.form["quantity"]

        from ..database.models.functions.betsy_functions import purchase_product
        purchase_product(product_id, g.user.id,  quantity)

        return redirect(url_for("betsy.handle_purchase"))
