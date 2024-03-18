from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'
app.config['SECRET_KEY'] = '3435c9fecc7c117d96e6c4e0b497957404d63f9cf25516d0'
app.app_context().push()
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float)
    description = db.Column(db.String)
    imageName = db.Column(db.String)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False)
    hashedPassword = db.Column(db.String, nullable=False)

    def get(self, user_id):
        user = self.query.filter_by(id = user_id).first()
        return user
    
    def is_autenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    return User().get(user_id)

@app.route("/")
def home():
    products = Product.query.all()
    return render_template("homePage.html", products = products)

@app.route("/product/<int:id>")
def product(id):
    product = Product.query.get(id)
    return render_template("product.html", product = product)

@app.route("/addproduct", methods=['GET', 'POST'])
def addproduct():
    if request.method == 'GET':
        return render_template("addproduct.html")
    else:
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        imageName = request.form['imageName']
        product = Product(name = name, price = price, description = description, imageName = imageName)
        db.session.add(product)
        db.session.commit()
        return redirect("/")

@app.route("/product/<int:id>/delete")
def deleteproduct(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return redirect("/")
    return 'Не удалось найти продукт'

@app.route("/product/<int:id>/update", methods=['GET', 'POST'])
def updateproduct(id):
    product = Product.query.get(id)
    if product:
        if request.method == 'GET':
            return render_template('updateproduct.html', product = product)
        product.name = request.form['name']
        product.price = request.form['price']
        product.description = request.form['description']
        product.imageName = request.form['imageName']
        db.session.commit()
        return redirect(f"/product/{id}")

@app.route("/about")
def about():
    return "О нас"

@app.route("/registration", methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        hash = generate_password_hash(request.form["password"])
        email = request.form["email"]
        user = User(email = email, hashedPassword = hash)
        db.session.add(user)
        db.session.commit()
        return "User added"
    return render_template("registration.html")