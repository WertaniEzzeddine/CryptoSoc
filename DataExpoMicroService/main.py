from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import matplotlib.pyplot as plt

from fastapi import FastAPI, HTTPException, Query
app = FastAPI()

DatacollectorUrl = "http://127.0.0.1:8000/"

class DateRange(BaseModel):
    start_date: str
    end_date: str

@app.post("/trending_range/")
def get_distinct_coins(date_range: DateRange):
    """
    Get distinct coins from the data collector service for a specific date range.
    """
    # Extract start and end dates from the request body
    start_date = date_range.start_date
    end_date = date_range.end_date

    # Construct the full URL with the query parameters
    url = f"{DatacollectorUrl}/distinct_coins/?start_date={start_date}&end_date={end_date}"

    # Send the GET request to the external data collector service
    response = requests.get(url)

    # Check if the response is successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return {"distinct_coins": data["distinct_coins"]}
    else:
        # Handle errors by raising an HTTPException
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
@app.get("/coin_price_curve/")
def get_coin_price_curve(coin_id: str, start_date: str, end_date: str):
    """
    Get a curve showing the taux of average prices from the daily stats.
    """
    # Construct the URL for the `/aboutcoinDaily/` endpoint
    url = f"{DatacollectorUrl}/aboutcoinDaily/?coin_id={coin_id}&startDate={start_date}&endDate={end_date}"
    
    # Send the request to the other service
    response = requests.get(url)

    # Check for success
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()
    
    # Ensure data exists
    if not data:
        raise HTTPException(status_code=404, detail="No data found for the given range.")
    
    # Extract daily statistics
    daily_stats = data
    
    # If there are no statistics
    if not daily_stats:
        raise HTTPException(status_code=400, detail="No daily statistics available for the given range.")

    # Get the average price of the first day
    first_day_avg_price = daily_stats[0]["avg_price"]
    
    # Calculate taux for each day (avg_price / first_day_avg_price)
    taux_data = []
    for day_data in daily_stats:
        taux = day_data["avg_price"] / first_day_avg_price
        taux_data.append({
            "date": day_data["date"],
            "taux": taux
        })
    
    # Prepare the data for plotting
    dates = [entry["date"] for entry in taux_data]
    taux_values = [entry["taux"] for entry in taux_data]

    # Plot the curve
    plt.figure(figsize=(10, 6))
    plt.plot(dates, taux_values, marker="o", linestyle="-")
    plt.xlabel("Date")
    plt.ylabel("Taux (Avg Price / First Day Avg Price)")
    plt.title(f"Taux of Average Prices for {coin_id}")
    plt.xticks(rotation=45)
    plt.grid(True)

    # Save the plot or return it as an image
    plt.tight_layout()
    plot_path = "/tmp/coin_price_curve.png"
    plt.savefig(plot_path)

    # You can also return the path to the image if you prefer to serve the image file
    return {"message": "Plot generated successfully", "plot_path": plot_path}

