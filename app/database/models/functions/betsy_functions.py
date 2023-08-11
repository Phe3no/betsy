from peewee import IntegrityError, DatabaseError, DoesNotExist, PeeweeException
from flask import flash


def read_tags():
    res = []
    message = ""
    try:
        from ..tag import Tag
        query = Tag.select()
        for item in query:
            res.append(item)

    except DatabaseError:
        message = "A problem occured while reading tags from the database."

    flash(message)
    return res


def get_product(product_name):
    message = None
    try:
        from ..product import Product
        product = Product.get(Product.name == product_name)
        message = ""
    except DoesNotExist:
        message = "Product can't be found in the database."
    flash(message)
    return product


def get_all_products_by_user(user_id):
    res = []
    message = None
    try:
        from ..product import Product
        query = Product.select().where(Product.user_id == user_id)
        for item in query:
            res.append(item)
        if len(res) == 0:
            message = "There are no products found."
        else:
            message = ""
    except DatabaseError:
        message = "Some error occured while getting all products by user."

    flash(message)
    return res


def search_product(term):
    res = []
    message = ''
    try:
        from ..product import Product
        query = Product.select().where((Product.name.contains(term) |
                                        (Product.description.contains(term))))

        for item in query:
            res.append(item)
            if len(res) == 0:
                message = "Nothing found what matches your request."

    except DatabaseError:
        message = "Something went wrong searching product"

    flash(message)
    return res


def list_user_products(user_id):
    res = []
    message = ""
    try:
        from ..product import Product
        query = Product.select(Product).where(Product.user_id == int(user_id))

        for item in query:
            res.append(item)
            if len(res) == 0:
                message = "Nothing found what matches your request."

    except DatabaseError:
        message = "Something went wrong listing user product"

    flash(message)
    return res


def list_products_per_tag(tag_id):
    res = []
    message = ""
    try:
        from ..product_tag import ProductTag
        from ..product import Product
        query = Product.select(Product, ProductTag.tag_id).join(
            ProductTag).where(ProductTag.tag_id == tag_id)

        for item in query:
            res.append(item)
            if len(res) == 0:
                message("No products found matching the tag you specified")

    except DatabaseError:
        message = "Something went wrong listing products per tag"

    flash(message)
    return res


def add_product(user_id, name, description, price, quantity, checked_tags):
    message = None
    res = []
    try:
        from ..product import Product
        query = Product.create(
            user_id=user_id,
            name=name,
            description=description,
            price_per_unit=price,
            amount_in_stock=quantity)
        query.save()
        message = ""

    except IntegrityError:
        message = "This product name is already in use, please change the name!"

    # get the just inserted product from the database (need id)
    product = get_product(name)

    try:
        from ..product_tag import ProductTag
        for item in checked_tags:
            query = ProductTag.create(product_id=product, tag_id=item)

    except DatabaseError:
        if len(message) == 0:
            message = "Some problem updating the tags."

    flash(message)
    return res


def delete_product(name):
    message = None
    try:
        from ..product import Product
        product = Product.get(Product.name == name)
        number = product.delete_instance()
        message = f"{number} product deleted!"
    except DoesNotExist:
        message = "The product selected can't be deleted. It appears not to be in the database."

    flash(message)


def update_stock(product_id, new_quantity):
    message = None
    print(type(product_id), product_id)

    try:
        from ..product import Product
        query = Product.update(amount_in_stock=new_quantity).where(
            Product.id == product_id)
        number = query.execute()
        message = f"{number} product updated!"
    except DoesNotExist:
        message = "The product selected can't be updated. It appears not to be in the database."

    flash(message)


def purchase_product(product_id, buyer_id, quantity):
    message = ""
    try:
        from ..product import Product
        product = Product.get(Product.id == product_id)
        if product.amount_in_stock - int(quantity) >= 0:
            res = product.amount_in_stock - int(quantity)
            query = Product.update(amount_in_stock=res).where(
                Product.id == product_id)
            query.execute()
            message = "The seller has enough of this product in stock, the stock of the sellers product is updated.\n"

            try:
                from ..transaction import Transaction
                query = Transaction.create(
                    product_id=product_id,
                    user_id=buyer_id,
                    quantity=quantity
                )
                query.save()
                if quantity == "1":
                    message = message + \
                        f"You have just bought an awesome product. The account for this will follow ASAP."
                else:
                    print(type(quantity))
                    message = message + \
                        f"You have just bought {quantity} awesome products. The account for this will follow ASAP."

            except DatabaseError as e:
                message = f"Something went wrong with your purchase, please try again. {e}"
        else:
            message = "Transaction stopped. The owner of this product has not enough of this product in stock!"

    except PeeweeException as e:
        message = "There was an error when trying to update the amount of stock.. Maybe, if you can find the time, you can send us the next message! Thank you in advance. Message: {e}"

    flash(message)
