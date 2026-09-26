from math import e, pi
from random import choice, randint, uniform

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

OPERATORS = ("+", "-", "*", "/")
DOMAINS = {"naturais", "inteiros", "racionais", "irracionais", "reais"}


def make_problem(domain="naturais"):
    if domain not in DOMAINS:
        domain = "naturais"
    if domain == "reais":
        domain = choice(("naturais", "inteiros", "racionais", "irracionais"))
    if domain == "irracionais":
        constant, value = choice((("π", pi), ("e", e)))
        operator = choice(("+", "-", "*", "/"))
        number = randint(-12, 12)
        while operator == "/" and number == 0:
            number = randint(-12, 12)
        if operator == "+":
            answer = value + number
        elif operator == "-":
            answer = value - number
        elif operator == "*":
            answer = value * number
        else:
            answer = value / number
        return {"question": f"{constant} {operator} {number}", "answer": answer, "tolerance": 0.05}

    operator = choice(OPERATORS)
    if domain == "racionais":
        first, second = round(uniform(-30, 30), 1), round(uniform(-30, 30), 1)
        if operator == "/":
            while abs(second) < 1:
                second = round(uniform(-12, 12), 1)
            answer = round(uniform(-12, 12), 1)
            first = round(second * answer, 2)
        elif operator == "+":
            answer = round(first + second, 2)
        elif operator == "-":
            answer = round(first - second, 2)
        else:
            answer = round(first * second, 2)
        return {"question": f"{first:g} {operator} {second:g}", "answer": answer, "tolerance": 0.05}

    if domain == "inteiros":
        if operator == "+":
            first, second = randint(-50, 50), randint(-50, 50)
            answer = first + second
        elif operator == "-":
            first, second = randint(-50, 50), randint(-50, 50)
            answer = first - second
        elif operator == "*":
            first, second = randint(-12, 12), randint(-12, 12)
            answer = first * second
        else:
            second = randint(-12, 12)
            while second == 0:
                second = randint(-12, 12)
            answer = randint(-12, 12)
            first = second * answer
        return {"question": f"{first} {operator} {second}", "answer": answer, "tolerance": 0}

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

    return {"question": f"{first} {operator} {second}", "answer": answer, "tolerance": 0}


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/problem")
def problem():
    return jsonify(make_problem(request.args.get("domain", "naturais")))


@app.post("/api/check")
def check_answer():
    payload = request.get_json(silent=True) or {}
    answer = payload.get("answer")
    expected = payload.get("expected")

    try:
        tolerance = float(payload.get("tolerance", 0))
        is_correct = abs(float(answer) - float(expected)) <= tolerance + 1e-9
    except (TypeError, ValueError):
        is_correct = False

    return jsonify({"correct": is_correct})


if __name__ == "__main__":
    app.run(debug=True)
