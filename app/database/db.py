from peewee import SqliteDatabase
from flask import current_app, g
import click


def get_db():
    if "db" not in g:
        g.db = SqliteDatabase(
            current_app.config["DATABASE"]
        )

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    # from ..database.models.Model import Model
    from ..database.models.dish import Dish
    from ..database.models.ingredient import Ingredient
    from ..database.models.rating import Rating
    from ..database.models.restaurant import Restaurant
    from ..database.models.user import User
    from ..database.models.product import Product
    from ..database.models.product_tag import ProductTag
    from ..database.models.tag import Tag
    from ..database.models.transaction import Transaction
    DishIngredient = Dish.ingredients.get_through_model()
    db.connect()
    db.create_tables([
        Dish, 
        Ingredient, 
        Rating, 
        Restaurant, 
        User,
        Product,
        ProductTag,
        Transaction,
        Tag,
        DishIngredient
        ])
    
    # populate the ingredients table
    from .data.populate_data import ingredients
    for item in ingredients:
        ingredient = Ingredient(
            name=item.get("name"),
            is_vegetarian=item.get("is_vegetarian"),
            is_vegan=item.get("is_vegan"), 
            is_glutenfree=item.get("is_glutenfree")
        )
        ingredient.save()

    # populate the restaurants table
    from .data.populate_data import restaurants
    for item in restaurants:
        restaurant = Restaurant(
            name=item.get("name"),
            open_since=item.get("open_since"),
            opening_time=item.get("opening_time"),
            closing_time=item.get("closing_time"),
        )
        restaurant.save()

    # populate the dish table
    from .data.populate_data import dishes
    for item in dishes:
        dish = Dish(
            name=item.get("name"),
            served_at=item.get("served_at"),
            price_in_cents=item.get("price_in_cents"),
        )
        dish.save()
        for x in item.get("ingredients"):
            ingredient = Ingredient.get(Ingredient.name == x)
            dish.ingredients.add(ingredient)
        
    # populate the rating table
    from .data.populate_data import ratings
    for item in ratings:
        rating = Rating(
            restaurant=item.get("restaurant"),
            rating=item.get("rating"),
            comment=item.get("comment"),
        )    
        rating.save()

    # populate the user table
    from .data.populate_user import users
    User.insert_many(users).execute()

    # populate the product table
    from .data.populate_product import products
    Product.insert_many(products).execute()

    # populate the tag table
    from .data.populate_tag import tags
    Tag.insert_many(tags).execute()

    # populate the product-tag table
    from .data.populate_product_tags import product_tags
    ProductTag.insert_many(product_tags).execute()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized and populated the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
