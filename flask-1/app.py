from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    from_currency = request.form['from_currency']
    to_currency = request.form['to_currency']
    amount = request.form['amount']

    
    api_url = f'
    # YOUR_API_ENDPOINT?from={from_currency}&to={to_currency}'
    # I am not sure which API to use?
    response = requests.get(api_url)
    data = response.json()

    if 'error' in data:
        return jsonify({'error': 'Invalid currency code or API error'})

    conversion_rate = data['rate']
    converted_amount = float(amount) * conversion_rate
    result = f"{to_currency} {converted_amount:.2f}"

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
