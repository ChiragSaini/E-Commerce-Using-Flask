from flask import redirect, render_template, session, url_for, flash, request, current_app
from shop import db, app
from shop.products.models import Product
from shop.products.routes import get_all_brands, get_all_categories

def merge_dict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@app.route('/addcart', methods=["POST"])
def add_cart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        product = Product.query.filter_by(id=product_id).first()
        if request.method == "POST" and product_id and quantity:
            DictItems = {product_id:{"name":product.name, 'price':int(product.price), 'quantity':int(quantity), 
                        'image':product.image_1}}
            if 'shopcart' in session:
                print(session['shopcart'])
                if product_id in session['shopcart']:
                    for key, item in session['shopcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                    print("This product is already in your Cart")
                else:
                    session['shopcart'] = merge_dict(session['shopcart'], DictItems)
            else:
                session['shopcart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/cart')
def get_cart():
    if 'shopcart' not in session:
        return redirect(request.referrer)
    total_without_tax = 0
    for key, product in session['shopcart'].items():
        # subtotal = 0
        # subtotal += product['price']*product['quantity']
        # # tax += round(0.06 * subtotal, 0)
        total_without_tax += product['price']*int(product['quantity'])
        # total += round((subtotal + tax), 2)  
    return render_template('products/cart.html', title="Your Cart", total_without_tax=total_without_tax, brands=get_all_brands(),
                            categories=get_all_categories())

@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)

@app.route('/updatecart/<int:code>', methods=["POST"])
def updatecart(code):
    if 'shopcart' not in session and len(session['shopcart']) <= 0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, item in session['shopcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    flash('Item Updated', 'success')
                    return redirect(url_for('get_cart'))
        except Exception as e:
            print(e)
            return redirect(url_for('get_cart'))

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'shopcart' not in session or len(session['shopcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['shopcart'].items():
            if int(key) == id:
                session['shopcart'].pop(key, None)
                return redirect(url_for('get_cart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getcart'))

@app.route('/clearcart')
def clearcart():
    try:
        session.pop('shopcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)