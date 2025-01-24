from flask import Flask, jsonify
from routes import app_routes  # Import the routes from another file
import utils.mongo_client as mongo_client
import os
from dotenv import load_dotenv

load_dotenv()
# import logging

# Configure logging
# logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(message)s")
app = Flask(__name__)
# Register the routes from routes.py using a blueprint


# @app.errorhandler(Exception)
# def handle_exception(e):
#     # Log the exception
#     app.logger.error(f"An error occurred: {e}", exc_info=True)
#     print("app: =====ss===> ")
#     # Return a generic JSON response
#     response = {
#         "error": "An unexpected error occurred.",
#         "message": str(e),  # You can customize this message for production
#     }


# return jsonify(response), 500


app.register_blueprint(app_routes)
mongo_client.connect_to_mongo()

# Run the app

if __name__ == "__main__":
    app.run(debug=True, port=5005)
