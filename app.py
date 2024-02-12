from flask import Flask, render_template

app = Flask(__name__)

class Product():
    def __init__(self, id, name, price, description, imageName = "noImage.jpg"):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.imageName = imageName


products = []
products.append(Product(1, "Apple", 11000, "no description for apple", "apple.jpg"))
products.append(Product(2, "Orange", 40000, "Orange orange", "orange.jpg"))

@app.route("/")
def home():
    return render_template("homePage.html", products = products)

@app.route("/product/<int:id>")
def product(id):
    return render_template("product.html", product = products[id - 1])