#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    articles_data = [{
        'id': article.id,
        'title': article.title,
        'author': article.author,
        'content': article.content,
        'preview': article.preview,
        'minutes_to_read': article.minutes_to_read,
        'date': article.date
    } for article in articles]
    return jsonify(articles_data)


@app.route('/articles/<int:id>')
def show_article(id):
    # Increment page_views session variable
    session['page_views'] = session.get('page_views', 0) + 1
    
    # Check if page_views exceeds 3, return 401 if it does
    if session['page_views'] > 3:
        return make_response(jsonify({'message': 'Maximum pageview limit reached'}), 401)
    
    article = Article.query.get_or_404(id)
    return jsonify({
        'id': article.id,
        'title': article.title,
        'author': article.author,
        'content': article.content,
        'preview': article.preview,
        'minutes_to_read': article.minutes_to_read,
        'date': article.date
    })


if __name__ == '__main__':
    app.run(port=5555)
