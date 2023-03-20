from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField
from wtforms.validators import InputRequired
from flask_bootstrap import Bootstrap
from rates import currency_rates
import requests
from currency_history import plot_history


API_KEY = "6cf09567aa8da4798d688041"
API_KEY_2 = "dBta4DkOceoYQFd2h8V2ih1mWWO5Coke"

# Function to convert a currency into another
def convert_currency(amount, from_currency, to_currency):

    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}'

    response = requests.get(url)

    data = response.json()

    rate = data["conversion_rates"][to_currency]

    conversion = amount * rate
    
    return conversion
    

# Form class to input amount to convert and currencies to convert
class ConversionForm(FlaskForm):
    amount = FloatField('Amount', validators=[InputRequired()])
    from_currency = SelectField('From Currency', choices=[currency + ' (' + currency_rates[currency]['name'] + ')' for currency in list(currency_rates.keys())])
    to_currency = SelectField('To Currency', choices=[currency + ' (' + currency_rates[currency]['name'] + ')' for currency in list(currency_rates.keys())])


# Initialise flask app
app = Flask(__name__, template_folder='Templates', static_folder='Static')

# WTForms secret key (not related to any databases; flask just need a key for forms)
app.secret_key = "verysecret"

# import bootstrap
bootstrap = Bootstrap(app)

# Home page
@app.route('/', methods=['POST', 'GET'])
def home():
    
    # Make an instance of ConversionForm to take user input
    conversion_form = ConversionForm()
    
    #print(conversion_form.amount.data, conversion_form.from_currency.data, conversion_form.to_currency.data)
    amount = conversion_form.amount.data
    from_currency = str(conversion_form.from_currency.data).split()[0]
    to_currency = str(conversion_form.to_currency.data).split()[0]
    
    # Calculate the conversion if an amount has been entered
    if amount and from_currency and to_currency:
        conversion = convert_currency(amount, from_currency, to_currency)
    
        # Print the converted currency
        flash(f"{amount:.2f} {currency_rates[from_currency]['name']} is {conversion:.2f} {currency_rates[to_currency]['name']}.")
        
        # Plot and display the historical trend of the selected currencies
        currency_fig = plot_history(from_currency, to_currency)
        currency_fig.savefig("Static/Images/currency_fig.png")
        
        return render_template("home.html", conversion_form=conversion_form, url="Static/Images/currency_fig.png")
    
    
    return render_template("home.html", conversion_form=conversion_form, url=None)

if __name__ == "__main__":
    app.run(debug=True)

