from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
app.secret_key = "sehtrsdyhndtejdydunuyehbdrvteryhe"


# MODEL
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "username": self.username
        }


# CRUD

# READ ALL
@app.route("/posts")
def fetch_posts():
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts]), 200


# READ ONE
@app.route("/posts/<int:id>", methods=["GET"])
def fetch_post(id):
    post = db.session.get(Post, id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post.to_dict()), 200


# CREATE
@app.route("/posts", methods=["POST"])
def create_post():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    title = data.get("title", "").strip()
    content = data.get("content", "").strip()
    username = data.get("username", "").strip()

    if not title:
        return jsonify({"error": "Title is required"}), 400
    if not content:
        return jsonify({"error": "Content is required"}), 400
    if not username:
        return jsonify({"error": "Username is required"}), 400

    new_post = Post(title=title, content=content, username=username)
    db.session.add(new_post)
    db.session.commit()
    return jsonify(new_post.to_dict()), 201


# UPDATE
@app.route("/posts/<int:id>", methods=["PUT"])
def update_post(id):
    post = db.session.get(Post, id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    title = data.get("title", "").strip()
    content = data.get("content", "").strip()
    username = data.get("username", "").strip()

    if not title:
        return jsonify({"error": "Title is required"}), 400
    if not content:
        return jsonify({"error": "Content is required"}), 400
    if not username:
        return jsonify({"error": "Username is required"}), 400

    post.title = title
    post.content = content
    post.username = username
    db.session.commit()
    return jsonify(post.to_dict()), 200


# DELETE
@app.route("/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    post = db.session.get(Post, id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": f"Post {id} deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)