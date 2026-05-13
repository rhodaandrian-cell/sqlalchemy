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

# model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

# CRUD

# READ ALL
@app.route("/posts")
def fetch_posts():
    posts = Post.query.all()
    results = []
    for post in posts:
        results.append({
            "id": post.id,
            "title": post.title,
            "content": post.content
        })
    return jsonify(results), 200

# READ ONE
@app.route("/posts/<int:id>", methods=["GET"])
def fetch_post(id):
    post = Post.query.get(id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify({"id": post.id, "title": post.title, "content": post.content}), 200

# ADD
@app.route("/posts", methods=["POST"])
def create_post():
    data = request.json
    new_post = Post(title=data["title"], content=data["content"])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"id": new_post.id, "title": new_post.title, "content": new_post.content}), 201

# UPDATE
@app.route("/posts/<int:id>", methods=["PUT"])
def update_post(id):
    post = Post.query.get(id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    data = request.json
    post.title = data["title"]
    post.content = data["content"]
    db.session.commit()
    return jsonify({"id": post.id, "title": post.title, "content": post.content}), 200

# DELETE
@app.route("/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    post = Post.query.get(id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": f"Post {id} deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)