from flask import request, Blueprint
from controllers import client, patient

app_routes = Blueprint("app_routes", __name__)


# Define routes using the blueprint
@app_routes.route("/api/v1/forecast-clients")
def forecast_clients():
    return client.handle_client_forecast(request)


@app_routes.route("/api/v1/forecast-patients")
def forecast_patients():
    return patient.handle_patient_forecast(request)


# return "hello"


@app_routes.route("/about")
def about():
    return "About Page"


@app_routes.route("/greet/<name>")
def greet(name):
    return f"Hello, {name}!"
