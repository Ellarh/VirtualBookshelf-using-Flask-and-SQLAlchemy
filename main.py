from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books.database"
database = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Books(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String, nullable=False)
    author = database.Column(database.String(200), unique=True, nullable=False)
    rating = database.Column(database.Float, nullable=False)

    def __repr__(self):
        return '<Books %r>' % self.title

database.create_all()

@app.route('/')
def home():
    all_books = database.session.query(Books).all() # Reading all books
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_book = Books(
                title=request.form['title'],
                author=request.form['author'],
                rating=request.form['rating']
            )
        database.session.add(new_book)
        database.session.commit()
        return redirect(url_for("home"))
    return render_template('add.html')

@app.route("/edit-rating", methods=['GET', 'POST'])
def edit_rating():
    if request.method == 'POST':
        # Update record
        book_id = request.form['id']
        book_to_update = Books.query.get(book_id)
        book_to_update.rating = request.form['rating']
        database.session.commit()
        return redirect(url_for('home'))

    book_id = request.args.get('id')
    book_selected = Books.query.get(book_id)
    return render_template('edit-rating.html',  book=book_selected)

@app.route('/delete')
def delete():
    # Delete record from database
    book_id = request.args.get('id')
    book_to_delete = Books.query.get(book_id)
    database.session.delete(book_to_delete)
    database.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

