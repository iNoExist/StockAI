import openai
import requests
import yfinance as yf
from flask import Flask, render_template, request

app = Flask(__name__)

# Set your OpenAI API Key for ChatGPT (hardcoded)
openai.api_key = ""  # Replace with your actual OpenAI API key

# List of stocks to consider
stock_symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "NVDA", "META"]

# Function to get stock data for the last 6 months (but only return the most recent close price)
def get_stock_data(stock_symbol):
    try:
        stock = yf.Ticker(stock_symbol)
        history = stock.history(period="6mo")
        if history.empty:
            print(f"No data available for {stock_symbol}")
            return None  # If no data is found
        latest_price = history['Close'].iloc[-1]  # Get the most recent closing price
        return latest_price
    except Exception as e:
        print(f"Error fetching stock data for {stock_symbol}: {e}")
        return None

# Function to get investment advice from ChatGPT based on stock data
def get_investment_advice(stock_symbols, risk_level, length_months, initial_capital, image_index):
    stocks_data = {}

    # Collect stock data for each stock
    for stock_symbol in stock_symbols:
        stock_data = get_stock_data(stock_symbol)
        if stock_data is None:
            print(f"Skipping {stock_symbol} due to missing stock data.")
            continue  # Skip stocks with no valid data

        stocks_data[stock_symbol] = stock_data

    # Check if we have any valid data to pass to OpenAI
    if not stocks_data:
        print("No valid stock data available to analyze.")
        return "No valid stock data available to analyze."

    # Determine the image category based on the image index
    image_category = ""
    if image_index == 0:
        image_category = "Tech"
    elif image_index == 1:
        image_category = "Energy"
    elif image_index == 2:
        image_category = "Automotive"

    # Construct the messages for the OpenAI API call
    messages = [
        {"role": "system", "content": "You are a helpful finance assistant who is always choosing the ideal stocks."},
        {"role": "user", "content": f"Risk level: {risk_level}, Preferred length: {length_months} months, Initial Capital: £{initial_capital}, Image Category: {image_category}"}
    ]

    for stock_symbol in stocks_data:
        price = stocks_data[stock_symbol]
        messages.append(
            {"role": "user", "content": f"Stock: {stock_symbol}\nLatest Price: {price}"}
        )

    messages.append(
        {"role": "user", "content": "Based on this data, provide a recommendation on which singular stock is a good investment."}
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Ensure you're using the correct GPT-4 model as specified
            messages=messages,    # Use the constructed messages list
            max_tokens=150,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error getting response from OpenAI: {e}")
        return "Error getting investment advice."

@app.route("/", methods=["GET", "POST"])
def index():
    investment_advice = None
    if request.method == "POST":
        # Get the values from the sliders, textbox, and hidden image index
        investment_amount = request.form.get("investment_amount")
        length_amount = request.form.get("length_amount")
        quantity = request.form.get("quantity")
        image_index = int(request.form.get("image_index"))  # Convert to integer
        
        # Print the captured values in the terminal, including image index and category
        print(f"VALUES: investment_amount = {investment_amount}, length_amount = {length_amount}, quantity = {quantity}, image_index = {image_index}")

        # Get the image category based on the image index
        if image_index == 0:
            image_category = "Tech"
        elif image_index == 1:
            image_category = "Energy"
        elif image_index == 2:
            image_category = "Automotive"
        else:
            image_category = "Unknown"

        # Call the investment advice function with the captured values
        investment_advice = get_investment_advice(
            stock_symbols, 
            investment_amount, 
            length_amount, 
            quantity,
            image_index
        )

    return render_template("index.html", investment_advice=investment_advice)

if __name__ == "__main__":
    app.run(debug=True)
