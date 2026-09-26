from random import choice, randint

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

OPERATORS = ("+", "-", "*", "/")


def make_problem():
    operator = choice(OPERATORS)
    if operator == "+":
        first, second = randint(1, 99), randint(1, 99)
        answer = first + second
    elif operator == "-":
        first, second = randint(1, 99), randint(1, 99)
        first, second = max(first, second), min(first, second)
        answer = first - second
    elif operator == "*":
        first, second = randint(2, 12), randint(2, 12)
        answer = first * second
    else:
        second = randint(2, 12)
        answer = randint(2, 12)
        first = second * answer

    return {"question": f"{first} {operator} {second}", "answer": answer}


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/problem")
def problem():
    return jsonify(make_problem())


@app.post("/api/check")
def check_answer():
    payload = request.get_json(silent=True) or {}
    answer = payload.get("answer")
    expected = payload.get("expected")

    try:
        is_correct = float(answer) == float(expected)
    except (TypeError, ValueError):
        is_correct = False

    return jsonify({"correct": is_correct})


if __name__ == "__main__":
    app.run(debug=True)
