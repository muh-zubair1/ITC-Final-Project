import flask
import json
from flask import Flask, request, render_template_string, render_template

app = Flask(__name__)

# Load books from JSON file
with open('books.json', 'r') as f:
    books = json.load(f)

# ---------------- Root Route ----------------
@app.route("/")
def index():
    return render_template('index.html')

# ---------------- Books Route ----------------
@app.route("/api/books")
def get_books():
    return flask.jsonify(books)

@app.route("/api/books/<int:id>")
def get_book_by_id(id):
    for book in books:
        if book['bookid'] == id:
            return flask.jsonify(book)
    return flask.jsonify({"error": "Book not found"}), 404




if __name__ == "__main__":
    # Development server — use `flask run` or a production server for deployment
    app.run(debug=True, host="0.0.0.0", port=5000)

