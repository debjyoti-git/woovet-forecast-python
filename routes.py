from flask import request, Blueprint
from controllers import client, patient, sales, appointment, referrals

app_routes = Blueprint("app_routes", __name__)


# Define routes using the blueprint
@app_routes.route("/api/v1/forecast-clients")
def forecast_clients():
    return client.handle_client_forecast(request)


@app_routes.route("/api/v1/forecast-patients")
def forecast_patients():
    return patient.handle_patient_forecast(request)


@app_routes.route("/api/v1/forecast-sales")
def forecast_sales():
    return sales.handle_sales_forecast(request)


@app_routes.route("/api/v1/forecast-appointments")
def forecast_appointment():
    return appointment.handle_appointment_forecast(request)


@app_routes.route("/api/v1/forecast-referrals")
def forecast_referrals():
    return referrals.handle_referral_forecast(request)


@app_routes.route("/api/v1/forecast-noshows")
def forecast_noshows():
    return appointment.handle_noshows_forecast(request)


@app_routes.route("/api/v1/forecast-app-doctors")
def forecast_app_doctors():
    return appointment.handle_appointment_doctor_forecast(request)


@app_routes.route("/api/v1/forecast-app-types")
def forecast_app_types():
    return appointment.handle_appointment_type_forecast(request)


@app_routes.route("/api/v1/forecast-sales-services")
def forecast_sales_service():
    return sales.handle_sales_services_forecast(request)


# return "hello"


@app_routes.route("/about")
def about():
    return "About Page"


@app_routes.route("/greet/<name>")
def greet(name):
    return f"Hello, {name}!"
