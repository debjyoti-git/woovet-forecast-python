import json
from prophet import Prophet
import pandas as pd
from utils.mongo_client import get_db_instance

# Function for clients forecasting monthly or weekly


def handle_appointment_forecast(request):
    try:
        _db = get_db_instance()
        duration = request.args.get("duration")
        interval = request.args.get("type")
        if duration is None or interval is None:
            raise Exception("Required fields are missing !!!")

        duration = int(duration)
        collection = _db["forecast_app"]
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


def handle_noshows_forecast(request):
    try:
        _db = get_db_instance()
        duration = request.args.get("duration")
        interval = request.args.get("type")
        if duration is None or interval is None:
            raise Exception("Required fields are missing !!!")

        duration = int(duration)
        collection = _db["forecast_noshows"]
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


def handle_appointment_doctor_forecast(request):
    try:
        _db = get_db_instance()
        duration = request.args.get("duration")
        if duration is None:
            raise Exception("Required fields are missing !!!")

        duration = int(duration)
        collection = _db["forecast_app_doctors"]
        items = list(
            collection.aggregate(
                [
                    {
                        "$group": {
                            "_id": "$staff",
                            "data": {"$push": {"date": "$date", "count": "$count"}},
                        }
                    },
                    {
                        "$lookup": {
                            "from": "staffs",
                            "localField": "_id",
                            "foreignField": "_id",
                            "as": "staff",
                        }
                    },
                    {
                        "$project": {
                            "staff": {"$arrayElemAt": ["$staff.name", 0]},
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

        app_doctor_forecast = []

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

            app_doctor_forecast.append(
                {"staff": item["staff"], "count": max(0, int(round(yhat_sum)))}
            )

        return {
            "body": json.dumps(app_doctor_forecast),
        }

    except Exception as e:
        return e
