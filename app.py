import sqlite3
from flask import Flask, request, jsonify
from database import init_db
from repository import StudentRepository

app = Flask(__name__)
repo = StudentRepository()
init_db()

REQUIRED_FIELDS = ["name", "email", "age", "course"]


def validate_student(data):
    """Return an error message string, or None if the data is valid."""
    if not data:
        return "Request body must be valid JSON"

    for field in REQUIRED_FIELDS:
        if field not in data:
            return f"Missing field: {field}"

    for field in ["name", "email", "course"]:
        if not isinstance(data[field], str) or not data[field].strip():
            return f"{field} must be a non-empty string"

    age = data["age"]
    if not isinstance(age, int) or isinstance(age, bool) or not (0 < age < 120):
        return "age must be a whole number between 1 and 119"

    return None


# 1. ADD a student
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True)
    error = validate_student(data)
    if error:
        return jsonify({"error": error}), 400

    try:
        new_id = repo.add(
            data["name"].strip(),
            data["email"].strip(),
            data["age"],
            data["course"].strip(),
        )
    except sqlite3.IntegrityError:
        return jsonify({"error": "A student with this email already exists"}), 409

    return jsonify(repo.get_by_id(new_id)), 201


# 2. VIEW all students
@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(repo.get_all()), 200


# 3. SEARCH by ID
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = repo.get_by_id(student_id)
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student), 200


# 4. UPDATE a student
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json(silent=True)
    error = validate_student(data)
    if error:
        return jsonify({"error": error}), 400

    try:
        updated = repo.update(
            student_id,
            data["name"].strip(),
            data["email"].strip(),
            data["age"],
            data["course"].strip(),
        )
    except sqlite3.IntegrityError:
        return jsonify({"error": "A student with this email already exists"}), 409

    if not updated:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(repo.get_by_id(student_id)), 200


# 5. DELETE a student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    if not repo.delete(student_id):
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"message": "Student deleted"}), 200


# Global error handlers: always return JSON, never an HTML error page
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found"}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)