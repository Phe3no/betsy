from flask import Blueprint, render_template, request, flash
from ..database.models.dish import Dish
from ..database.models.ingredient import Ingredient
from ..database.models.rating import Rating
from ..database.models.rating import Restaurant
from peewee import IntegrityError, DoesNotExist
from .public_views import login_required
from datetime import time

bp = Blueprint("exercise", __name__, url_prefix="/exercise")


@bp.route("/")
@login_required
def exercise():
    return render_template("user/exercise.html")


@bp.route("/ingredients")
@login_required
def ingredients():
    res = []
    error = None
    try:
        ingredients = Ingredient.select().order_by(Ingredient.name.asc())
        for ingredient in ingredients:
            res.append(ingredient)
        error = ""

    except DoesNotExist:
        error = "Can not find any ingredients."

    flash(error)

    return render_template("user/exercise/ingredients.html", res=res)


@bp.route("/cheapest_dish")
@login_required
def cheapest_dish():
    error = None
    res = None
    try:
        query = Dish.select(Dish.name).order_by(
            Dish.price_in_cents.asc()).get()
        res = query.name
        error = ""
    except DoesNotExist:
        error = "Can not find any dishes."

    flash(error)

    return render_template("user/exercise/cheapest_dish.html", res=res)


@bp.route("/add_ingredient", methods=("GET", "POST"))
@login_required
def add_ingredient():

    if request.method == "POST":
        name = request.form["name"]
        vegatarian = True if request.form.get("vegatarian") else False
        vegan = True if request.form.get("vegan") else False
        glutenfree = True if request.form.get("glutenfree") else False
        error = None

        try:
            item = Ingredient(name=name, is_vegetarian=vegatarian,
                              is_vegan=vegan, is_glutenfree=glutenfree)
            item.save()
            error = f"{name} added to the list."
        except IntegrityError:
            error = f"Ingredient {name} already exists."

        flash(error)

    return render_template("user/exercise/add_ingredient.html")


@bp.route("/vegetarian_dishes")
@login_required
def vegetarian_dishes():
    dishes = []
    try:
        for dish in Dish.select():
            for ingredient in dish.ingredients:
                if dish.ingredients.where(Ingredient.is_vegetarian == False):
                    break
                else:
                    if dish not in dishes:
                        dishes.append(dish)

    except DoesNotExist:
        error = "Can not find any vegetarian dishes."

    return render_template("user/exercise/vegetarian_dishes.html", dishes=dishes)


@bp.route("/best_average_rating")
@login_required
def best_average_rating():
    best_restaurant = ""
    best_average = 0
    try:
        restaurant = []
        # join is not nessary, could have taken Rating.restaurant
        query = Rating.select(Restaurant.name).join(
            Restaurant, on=(Restaurant.name == Rating.restaurant))
        for item in query:
            if item.restaurant.name not in restaurant:
                restaurant.append(item.restaurant.name)

        for item in restaurant:
            count = 0
            total = 0
            for elem in Rating.select().where(Rating.restaurant == item):
                count += 1
                total += elem.rating
            if total/count > best_average:
                best_average = total/count
                best_restaurant = item

        best_average = round(best_average, 2)

    except DoesNotExist:
        error = "Can not find any rating."

    return render_template("user/exercise/best_average_rating.html", best_restaurant=best_restaurant, best_average=best_average)


@bp.route("/add_rating", methods=("GET", "POST"))
@login_required
def add_rating():
    error = None
    try:
        restaurants = Restaurant.select(Restaurant.name)
    except DoesNotExist:
        error = "Not one restaurant found."

    if request.method == "POST":
        restaurant = request.form["restaurant"]
        rating = request.form["rating"]
        comment = request.form["comment"]

        try:
            item = Rating(restaurant=restaurant,
                          rating=rating, comment=comment)
            item.save()
        except DoesNotExist:
            error = "Restaurant does not exist"

    return render_template("user/exercise/add_rating.html", restaurants=restaurants)


@bp.route("/dinner_date_possible")
@login_required
def dinner_date_possible():
    dinner_time = time(19, 0, 0)
    res = []

    try:
        query = (Restaurant
                 .select(Restaurant, Dish)
                 .join(Dish, on=(Dish.served_at == Restaurant.name))
                 .where(
                     (Restaurant.opening_time < dinner_time) &
                     (Restaurant.closing_time > dinner_time)
                 )
                 )

        for item in query:
            count = 0
            for ingredient in item.dish.ingredients:
                if ingredient.is_vegan == False:
                    count += 1

            if count == 0 and item not in res:
                res.append(item)

        for item in res:
            item.closing_time = item.closing_time.strftime("%H:%M")

    except DoesNotExist:
        pass

    return render_template("user/exercise/dinner_date_possible.html", res=res)


@bp.route("/add_dish", methods=("GET", "POST"))
@login_required
def add_dish():
    name = "club sandwich"
    dish = None
    message = None
    restaurant = None
    try:
        new_dish = Dish.create(name=name, served_at=1, price_in_cents=975)
        new_dish.save()

        dish = Dish.get(Dish.name == name)
        dish.ingredients.add(Ingredient.get(Ingredient.name == "white bread"))
        dish.ingredients.add(Ingredient.get(Ingredient.name == "lettuce"))
        dish.ingredients.add(Ingredient.get(Ingredient.name == "butter"))
        dish.ingredients.add(Ingredient.get(Ingredient.name == "bacon"))
        dish.ingredients.add(Ingredient.get(
            Ingredient.name == "chicken breast"))

        try:
            restaurant = Restaurant.get(Restaurant.id == dish.served_at)
            message = ""
        except DoesNotExist:
            message = f"There is no restaurant with id {dish.served_at} in the database."

    except IntegrityError:
        message = "Dish already exists, it is not possible yet to eat the same dish in different restaurants, unless you give it a different name."

    flash(message)

    return render_template("user/exercise/add_dish.html", dish=dish, restaurant=restaurant)
