from flask import redirect, url_for, request, flash, render_template, session, current_app
from shop import db, app, photos
from .models import Brand, Category, Product
from .forms import AddProducts
import secrets, os

def get_all_brands():
    brands = Brand.query.join(Product, (Brand.id==Product.brand_id)).all()
    return brands

def get_all_categories():
    return Category.query.join(Product, (Category.id==Product.category_id)).all()

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(Product.stock > 0).paginate(page=page, per_page=4)
    return render_template('products/index.html', title="Store Home", products=products, brands=get_all_brands(), categories=get_all_categories())

@app.route('/product/<int:id>')
def product_details(id):
    product = Product.query.get_or_404(id)
    brands = Brand.query.join(Product, (Brand.id==Product.brand_id)).all()
    categories = Category.query.join(Product, (Category.id==Product.category_id)).all()
    return render_template('products/product_details.html', product=product, title=product.name, brands=brands, 
                    categories=get_all_categories())

@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type=int)
    get_b = Brand.query.filter_by(id=id).first_or_404()
    brand = Product.query.filter_by(brand = get_b).paginate(page=page, per_page=4)
    return render_template('products/index.html', brand=brand, title=Brand.query.get(id).name, brands=get_all_brands(), 
    categories=get_all_categories(), get_b=get_b)

@app.route('/category/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    category = Product.query.filter_by(category = get_cat).paginate(page=page, per_page=4)
    return render_template('products/index.html', category=category, title=Category.query.get(id).name, 
                            categories=get_all_categories(), brands=get_all_brands(), get_cat=get_cat)


@app.route('/addbrand', methods=["GET", "POST"])
def addbrand():
    if request.method == "POST":
        getBrand = request.form.get('brand')
        brand = Brand(name=getBrand)
        db.session.add(brand)
        flash(f'The Brand {getBrand} was added to DataBase.', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', title='Add Brand', brands='brands')

@app.route('/addcategory', methods=["GET", "POST"])
def addcategory():
    if request.method == "POST":
        getCategory = request.form.get('category')
        category = Category(name=getCategory)
        db.session.add(category)
        flash(f'The Category {getCategory} was added to DataBase.', 'success')
        db.session.commit()
        return redirect(url_for('addcategory'))
    return render_template('products/addbrand.html', title='Add Category')

@app.route('/addproduct', methods=["GET", "POST"])
def addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddProducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        stock = form.stock.data
        desc = form.desc.data
        brand_id = request.form.get('brand')
        category_id = request.form.get('category')
        print(f"Brand ID:{brand_id}, Category Id:{category_id}")
        # category = Category.query.get(id=category_id).first()
        # brand = Brand.query.get(id=brand_id).first()
        # print(f"Brand:{brand}, Category:{category}")
        image_1 = photos.save(request.files['image_1'] , name=secrets.token_hex(10) + '.')
        print(f"Image 1 name:{image_1}, its type:{type(image_1)}")
        product = Product(name=name, price=price, stock=stock, desc=desc, brand_id=brand_id, 
        category_id=category_id, image_1=image_1)
        db.session.add(product)
        flash(f"{name} has been added to database.", 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', title='Add Product', form=form, brands=brands, 
                            categories=categories)

@app.route('/updatebrand/<int:id>', methods=["GET", "POST"])
def updatebrand(id):
    if 'email' not in session:
        flash('Please Log In first', 'danger')
    
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == "POST":
        updatebrand.name = brand
        flash(f'Your brand has been updated', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title="Update Brand Info", 
                            updatebrand=updatebrand)

@app.route('/updatecategory/<int:id>', methods=["GET", "POST"])
def updatecategory(id):
    if 'email' not in session:
        flash('Please Log In first', 'danger')
    
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        updatecategory.name = category
        flash(f'Your category has been updated', 'success')
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('products/updatebrand.html', title="Update category Info", 
                            updatecategory=updatecategory)    

@app.route('/updateproduct/<int:id>', methods=["GET", "POST"])
def updateproduct(id):
    if 'email' not in session:
        flash('Please Log In first', 'danger')
    brands = Brand.query.all()
    categories = Category.query.all()
    brand = request.form.get('brand')
    category = request.form.get('category')
    product = Product.query.get_or_404(id)
    form = AddProducts(request.form)
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.desc = form.desc.data
        product.brand_id = brand
        product.category_id = category
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
                product.image_1 = photos.save(request.files['image_1'] , name=secrets.token_hex(10) + '.')
            except:
                product.image_1 = photos.save(request.files['image_1'] , name=secrets.token_hex(10) + '.')
        db.session.commit()
        flash('Product Updated', 'success')
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.stock.data = product.stock
    form.desc.data = product.desc
    return render_template('products/updateproduct.html', title="Update Product", form=form, brands=brands,
                        categories=categories, product=product) #, updatebrand=updatebrand)

@app.route('/deletebrand/<int:id>', methods=["POST"])
def deletebrand(id):
    if 'email' not in session:
        flash('Please Log In first', 'danger')
    
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(brand)
        db.session.commit()
        flash(f'Brand: {brand.name} Deleted', 'success')
        return redirect(url_for('admin'))
    flash(f'Brand: {brand.name} cant be Deleted', 'warning')
    return redirect(url_for('admin'))

@app.route('/deletecategory/<int:id>', methods=["POST"])
def deletecategory(id):
    if 'email' not in session:
        flash('Please Log In first', 'danger')
    
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(category)
        db.session.commit()
        flash(f'Category: {category.name} Deleted', 'success')
        return redirect(url_for('admin'))
    flash(f'Category: {category.name} cant be Deleted', 'warning')
    return redirect(url_for('admin'))

@app.route('/deleteproduct/<int:id>', methods=["POST"])
def deleteproduct(id):
    if 'email' not in session:
        flash('Please Log In first', 'danger')
    product = Product.query.get_or_404(id)
    if request.method == "POST":
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
            except Exception as e:
                print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'{product.name} Deleted', 'success')
        return redirect(url_for('admin'))
    flash(f'Cant delete {product.name}', 'warning')
    return redirect(url_for('admin'))