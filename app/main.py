import flask
import json
from flask import Flask, request, render_template_string, render_template

app = Flask(__name__)

# Global books data
books = []

def load_books():
    """Load books from JSON file into global books list"""
    global books
    with open('books.json', 'r') as f:
        books = json.load(f)

# Initialize books data on startup
load_books()

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

@app.route("/api/books/save", methods=['POST'])
def save_book():
    new_book = request.get_json()
    # Convert bookid to int for comparison
    new_book['bookid'] = int(new_book['bookid'])
    
    for i, book in enumerate(books):
        if book['bookid'] == new_book['bookid']:
            books[i] = new_book
            return flask.jsonify({"message": "Book updated successfully"}), 200 
            
    return flask.jsonify({"error": "Book not found"}), 404

@app.route("/api/books/search", methods=['POST'])
def serarch_books():
    criteria = request.get_json()
    title = criteria.get('title', '').lower()
    
    filtered_books = [
        book for book in books
        if (title in book['title'].lower() if title else True)
    ]
    
    return flask.jsonify(filtered_books)

if __name__ == "__main__":
    # Development server — use `flask run` or a production server for deployment
    app.run(debug=True, host="0.0.0.0", port=5500)

