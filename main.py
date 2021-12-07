import base64
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from io import BytesIO
from flask import Flask, request, url_for, redirect, render_template
from matplotlib.ticker import MultipleLocator

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def select():
    if request.method == "POST":
        coin_name = request.form["coin_name"]
        return redirect(url_for('dash', coinname=coin_name))

    else:
        coinSym = set()
        df = pd.read_csv("pythonProject/crypto.csv")
        coins = df["coin"]
        for i in coins:
            coinSym.add(i)

        print(coinSym)
        return render_template("select.html", data=coinSym)


@app.route("/<coinname>")
def dash(coinname):
    coinname = coinname

    plt.rcParams["figure.figsize"] = [10, 7]

    #plt.rcParams["figure.autolayout"] = True
    df = pd.read_csv("pythonProject/crypto.csv")

    #To only select btc
    g1 = df[df.coin == coinname]
    g1 = g1[::-1]


    #Print columns of frame
    #print(df.columns.tolist())
    plt.figure()
    plt.figure()

    #Plotting
    plt.title("Daily Closing Price")

    #plotting btc
    plt.plot(g1.Date, g1.Close)

    plt.xticks(size="small", rotation=60)
    plt.yticks(size="small")
    # Reduce no of ticks
    ax=plt.gca()
    ax.get_xaxis().set_major_locator(MultipleLocator(100))

    # get current axes
    ax = plt.gca()

    # hide x-axis
    #ax.get_xaxis().set_visible(False)

    #output to html

    buf = BytesIO()
    plt.savefig(buf, format="png")
    # Embed the result in the html output.
    Pricegraph = base64.b64encode(buf.getbuffer()).decode("ascii")

    # Market cap GRAPH ----------------------------------------------------------------

    plt.figure()

    plt.axis('off')
    g4 = df[df.coin == coinname]
    g4 = g4[::-1]
    coinlastvol = g4.iloc[-1]["MarketCap"]
    g4btc = df[df.coin == "BTC"]
    g4btc = g4btc[::-1]
    btclastvol = g4btc.iloc[-1]["MarketCap"]

    x = [btclastvol, coinlastvol]
    # x=[1,4]

    myexplode = [0, 0.45]
    plt.pie(x, radius=4, wedgeprops={"linewidth": 3, "edgecolor": "white"}, startangle=180, explode=myexplode,
            shadow=True, frame=True, labels=["BTC", coinname], autopct="%.2f")
    plt.legend(x, loc="lower right", title="Market Cap")

    plt.xticks([])
    plt.yticks([])

    plt.title("Market Cap Comparison with BTC")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    # Embed the result in the html output.
    Mktcapgraph = base64.b64encode(buf.getbuffer()).decode("ascii")


# last100  GRAPH ----------------------------------------------------------------
    plt.figure()

    g3 = df[df.coin == coinname]
    g3 = g3[::-1]
    g3 = g3.iloc[-100:]
    plt.figure()

    plt.step(g3.Date, g3.Close)

    # Reduce no of ticks
    ax = plt.gca()

    plt.xticks(size="small", rotation=60)
    plt.yticks(size="small")
    ax.get_xaxis().set_major_locator(MultipleLocator(7))
   # ax.get_yaxis().set_major_locator(MultipleLocator(20))
    plt.title("Last 100 Days Price Trend")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    # Embed the result in the html output.
    Last100 = base64.b64encode(buf.getbuffer()).decode("ascii")

    # Volatility GRAPH ----------------------------------------------------------------
    plt.figure()

    g2 = df[df.coin == coinname]
    g2 = g2[::-1]
    plt.figure()
    plt.plot(g2.Date, g2.Delta)

    # Reduce no of ticks
    ax = plt.gca()
    ax.get_yaxis().set_major_locator(MultipleLocator(100))

    plt.xticks(size="small", rotation=60)
    plt.yticks(size="small")
    ax.get_xaxis().set_major_locator(MultipleLocator(100))
    ax.get_yaxis().set_major_locator(MultipleLocator(100))
    plt.title("Volitality")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    # Embed the result in the html output.
    Volatility = base64.b64encode(buf.getbuffer()).decode("ascii")

    return f"<H1 align=center>{coinname} Dashboard</h1><img src='data:image/png;base64,{Pricegraph }'/><img src='data:image/png;base64,{Mktcapgraph}'/><br><img src='data:image/png;base64,{Last100}'/><img src='data:image/png;base64,{Volatility}'/>"


if __name__ == '__main__':
    app.run(debug=True)