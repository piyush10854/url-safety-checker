from flask import Flask, render_template, request
import re

app = Flask(__name__)

def analyze_url(url):
    score = 0
    reasons = []

    if len(url) > 75:
        score += 20
        reasons.append("URL is very long.")

    if "@" in url:
        score += 20
        reasons.append("URL contains '@' symbol.")

    if "-" in url:
        score += 10
        reasons.append("URL contains '-' which is common in phishing.")

    if not url.startswith("https"):
        score += 25
        reasons.append("Website does not use HTTPS.")

    suspicious_words = ["login", "verify", "update", "bank", "secure"]
    for word in suspicious_words:
        if word in url.lower():
            score += 15
            reasons.append(f"Contains suspicious word: {word}")

    if score > 100:
        score = 100

    return score, reasons


@app.route("/", methods=["GET", "POST"])
def home():
    score = None
    reasons = []

    if request.method == "POST":
        url = request.form["url"]
        score, reasons = analyze_url(url)

    return render_template("index.html", score=score, reasons=reasons)


if __name__ == "__main__":
    app.run(debug=True)
