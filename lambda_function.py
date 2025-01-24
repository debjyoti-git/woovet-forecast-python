from prophet import Prophet
import pandas as pd
import json
import os
from pymongo import MongoClient
from forecastFunctions import appointment, client, patient, sales, referrals


def get_client():
    # Replace the following with your MongoDB connection string
    mongo_uri = os.getenv("MONGO_URI")
    return MongoClient(mongo_uri)


def handler(event, context):
    db_client = get_client()
    database = os.getenv("DATABASE")
    db = db_client[database]

    resource = event["resource"]

    if resource == "/api/v1/forecast-clients":
        collection = db["forecast_clients"]
        return client.handle_client_forecast(event, collection)
    elif resource == "/api/v1/forecast-patients":
        collection = db["forecast_patients"]
        return patient.handle_patient_forecast(event, collection)
    elif resource == "/api/v1/forecast-sales":
        collection = db["forecast_sales"]
        return sales.handle_sales_forecast(event, collection)
    elif resource == "/api/v1/forecast-appointments":
        collection = db["forecast_app"]
        return appointment.handle_appointment_forecast(event, collection)
    elif resource == "/api/v1/forecast-referrals":
        collection = db["forecast_referrals"]
        return referrals.handle_referral_forecast(event, collection)
    elif resource == "/api/v1/forecast-noshows":
        collection = db["forecast_noshows"]
        return appointment.handle_noshows_forecast(event, collection)
    elif resource == "/api/v1/forecast-app-doctors":
        collection = db["forecast_app_doctors"]
        return appointment.handle_appointment_doctor_forecast(event, collection)
    elif resource == "/api/v1/forecast-app-types":
        collection = db["forecast_app_types"]
        return appointment.handle_appointment_type_forecast(event, collection)
    elif resource == "/api/v1/forecast-sales-services":
        collection = db["forecast_sales_services"]
        return sales.handle_sales_services_forecast(event, collection)
    else:
        return {
            "statusCode": 400,
            "body": json.dumps(f"Unsupported resource: {resource}"),
        }
