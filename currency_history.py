import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt

def plot_history(from_currency, to_currency):

    # Calculate the interval
    interval = 52
    start_date = (datetime.datetime.today() - datetime.timedelta(weeks=interval)).strftime('%Y-%m-%d')
    end_date = datetime.datetime.today().strftime('%Y-%m-%d')

    # Get data from API
    url = f"https://api.exchangerate.host/timeseries?base={from_currency}&start_date={start_date}&end_date={end_date}&symbols={to_currency}"
    response = requests.get(url)
    data = response.json()

    # pprint.pprint(data["rates"])

    
    # extract dates and rates from each item of dictionary or json in the above created list
    rates=[]
    for date, rate in data["rates"].items():
        rates.append([date , rate[to_currency]])
        
    # pprint(rates)

    # Create DataFrame
    df = pd.DataFrame(rates)
    df.columns=["date", "rate"]

    # pprint(df)
    
    # Plot the graph
    x = df["date"]
    y = df["rate"]
    plt.figure(figsize=(15,6))
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Exchange Rates", fontsize=12)
    plt.title(f"{from_currency} to {to_currency} Exchange Rates Over {interval} Weeks")
    plt.plot(x,y)
    plt.xticks([0, interval * 7 // 4, interval * 7 // 2, interval * 7 * 3 // 4, interval * 7])
    plt.grid()
    # plt.show()
    
    return plt
    
    
# plot_history("AUD", "JPY")