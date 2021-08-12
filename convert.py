from flask import Flask, request, render_template

import requests

app = Flask(__name__)


@app.route('/')
def home():
	return render_template('home.html')


@app.route('/cryptocalc')
def cryptocalc():
	return render_template('theform.html')


@app.route('/result', methods=["POST"])
def result():
	currency_1 = request.form['currency_1']
	amount = float(request.form['amount'])
	currency_2 = request.form['currency_2']
	rates = get_rates()
	formula = conversion_formula(rates, currency_1, amount, currency_2)
	return render_template('process.html', amount=amount, currency_1=currency_1, 
			currency_2=currency_2, formula=formula)

def get_rates():
	response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")

	result = response.json()

	btc_usd = result["bpi"]["USD"]["rate_float"]
	usd_btc = 1 / btc_usd
	btc_gbp = result["bpi"]["GBP"]["rate_float"]
	gbp_btc = 1 / btc_gbp
	btc_eur = result["bpi"]["EUR"]["rate_float"]
	eur_btc = 1 / btc_eur
	usd_eur = btc_usd / btc_eur
	eur_usd = 1 / usd_eur
	gbp_eur = btc_gbp / btc_eur
	eur_gbp = 1 / gbp_eur
	gbp_usd = btc_usd / btc_gbp
	usd_gbp = 1 / gbp_usd

	rates = {
        "btc": {"usd": btc_usd, "eur": btc_eur, "gbp": btc_gbp},
        "eur": {"usd": eur_usd, "btc": eur_btc, "gbp": eur_gbp},
        "usd": {"eur": usd_eur, "btc": usd_btc, "gbp": usd_gbp},
        "gbp": {"eur": gbp_eur, "usd": gbp_usd, "btc": gbp_btc},
    }
	return rates

def conversion_formula(rates, currency_1, amount, currency_2):

	if currency_2 in ["usd", "eur", "gbp"]:

		formula = rates[currency_1][currency_2] * amount

		return "%.3f" % round(formula, 3)

	formula = rates[currency_1][currency_2] * amount
	return formula



if __name__ == "__main__":
	app.run(debug=True)
