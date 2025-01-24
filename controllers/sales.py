import json
from prophet import Prophet
import pandas as pd
from utils.mongo_client import get_db_instance

# Function for clients forecasting monthly or weekly


def handle_sales_forecast(request):
    try:
        _db = get_db_instance()
        duration = request.args.get("duration")
        interval = request.args.get("type")
        if duration is None or interval is None:
            raise Exception("Required fields are missing !!!")

        duration = int(duration)
        collection = _db["forecast_sales"]
        items = list(collection.find({}, {"_id": 0}))
        # Convert list of dictionaries to DataFrame
        df = pd.DataFrame(items)
        # Rename the columns
        df.columns = ["ds", "y"]

        # Convert 'ds' column to datetime format
        df["ds"] = pd.to_datetime(df["ds"], format="%m/%d/%Y")

        # Train your Prophet model
        model = Prophet()
        model.fit(df)

        # Get the current date
        current_date = pd.Timestamp.now()

        # Calculate the start of the current month
        start_date = current_date.replace(day=1)

        # Calculate the end of the next three months
        end_date = (start_date + pd.DateOffset(months=duration)) - pd.DateOffset(days=1)

        # Create a date range from the start of the current month to the end of the next three months
        future_dates = pd.date_range(start=start_date, end=end_date, freq="D")

        # Create a DataFrame for the future dates
        future = pd.DataFrame(future_dates, columns=["ds"])

        # Make predictions
        forecast = model.predict(future)

        response = (
            forecast[["ds", "yhat"]]
            .rename(columns={"ds": "date", "yhat": "count"})
            .to_dict(orient="records")
        )

        # Convert the response to a DataFrame
        df_response = pd.DataFrame(response)

        # Convert 'date' column to datetime format and set as index
        df_response["date"] = pd.to_datetime(df_response["date"])
        df_response.set_index("date", inplace=True)

        if interval == "weekly":
            # Resample by week and sum
            weekly_resampled = df_response.resample("W").sum().reset_index()
            weekly_resampled["date"] = weekly_resampled["date"].dt.strftime("%Y-%m-%d")
            weekly_resampled["count"] = weekly_resampled["count"].apply(
                lambda x: max(0, int(round(x)))
            )
            weekly_response = weekly_resampled.to_dict(orient="records")
            return {
                "body": json.dumps(weekly_response),
            }
        else:
            # Resample by month and sum
            monthly_resampled = df_response.resample("MS").sum().reset_index()
            monthly_resampled["date"] = monthly_resampled["date"].dt.strftime(
                "%Y-%m-%d"
            )
            monthly_resampled["count"] = monthly_resampled["count"].apply(
                lambda x: max(0, int(round(x)))
            )
            monthly_response = monthly_resampled.to_dict(orient="records")
            return {
                "body": json.dumps(monthly_response),
            }
    except Exception as e:
        return e


def handle_sales_services_forecast(request):
    try:
        _db = get_db_instance()
        duration = request.args.get("duration")
        if duration is None:
            raise Exception("Required fields are missing !!!")

        duration = int(duration)
        collection = _db["forecast_sales_services"]
        items = list(
            collection.aggregate(
                [
                    {
                        "$group": {
                            "_id": "$planCat",
                            "data": {"$push": {"date": "$date", "count": "$count"}},
                        }
                    },
                    {
                        "$lookup": {
                            "from": "plan_cats",
                            "localField": "_id",
                            "foreignField": "_id",
                            "as": "planCat",
                        }
                    },
                    {
                        "$project": {
                            "service": {"$arrayElemAt": ["$planCat.name", 0]},
                            "data": 1,
                        }
                    },
                    {"$sort": {"_id": 1}},
                ]
            )
        )

        # Get the current date
        current_date = pd.Timestamp.now()

        # Calculate the start of the current month
        start_date = current_date.replace(day=1)

        # Calculate the end of the next three months
        end_date = (start_date + pd.DateOffset(months=duration)) - pd.DateOffset(days=1)

        # Create a date range from the start of the current month to the end of the next three months
        future_dates = pd.date_range(start=start_date, end=end_date, freq="D")

        # Create a DataFrame for the future dates
        future = pd.DataFrame(future_dates, columns=["ds"])

        sales_services_forecast = []

        for item in items:
            # Convert list of dictionaries to DataFrame
            df = pd.DataFrame(item["data"])
            # Rename the columns
            df.columns = ["ds", "y"]

            # Convert 'ds' column to datetime format
            df["ds"] = pd.to_datetime(df["ds"], format="%m/%d/%Y")

            # Train your Prophet model
            model = Prophet()
            model.fit(df)

            # Make predictions
            forecast = model.predict(future)

            yhat_sum = forecast["yhat"].sum()

            sales_services_forecast.append(
                {"service": item["service"], "amount": max(0, round(yhat_sum, 2))}
            )

        return {
            "body": json.dumps(sales_services_forecast),
        }

    except Exception as e:
        return e
