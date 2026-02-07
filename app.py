from flask import Flask, jsonify, render_template, request
render_template, request
import re
from urllib.parse import urlparse

app = Flask(__name__)
def analyze_url(url):
    score = 0
    reason = []

    #Normalize URL
    if not url.startswith('http'):
        url = 'http://' + url 
    parsed = urlparse(url) 

    # check length 
    if len(url) > 75:
        score += 15
        reason.append("URL is too long")

    # check for suspicious keywords
    suspicious_words = ['login', 'verify', 'update', 'free', 'bank', 'secure']
    for word in suspicious_words:
        if word in url.lower():
            score += 20
            reason.append(f'contains suspicious keyword: {word}')
            break 

    # check for IP address usage
    parsed = urlparse(url)
    if re.match(r'\d+\.\d+\.\d+\.\d+', parsed.netloc):
        score += 25
        reason.append('Uses IP address instead of domain ')

    # check for multiple subdomains
    if parsed.netloc.count('.') > 3:
        score += 15 
        reason.append('too many subdomains')
    
    # check @ symbol
    if '@' in url:
        score += 20
        reason.append('contains "@" symbol ')

    #check HTTPS
    if parsed.scheme != 'https':
        score += 10
        reason.append('not using HTTPS')
    
    #classification 
    if score<= 30:
        status = 'Safe 🎉'
    elif score <= 60:
        status = 'Suspicious ⚠️'
    else: 
        status = 'High Risk 🚨'

    return score, reason, status 

@app.route('/', methods =['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        score, status, reasons = analyze_url(url)

        return render_template('index.html',score = score, status = status, reasons = reasons, url = url)
    return render_template('index.html')

@app.route('/api/check')
def api_check():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    score, status, reasons = analyze_url(url)
    return jsonify({'url': url, 'score': score, 'status': status, 'reasons': reasons})


if __name__== '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    
    