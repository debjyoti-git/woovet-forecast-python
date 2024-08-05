FROM public.ecr.aws/lambda/python:3.12

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Copy forecastFunctions packages
COPY forecastFunctions ${LAMBDA_TASK_ROOT}/forecastFunctions

# If you need to modify a package, copy your modified files
# Example: Suppose you want to modify a file in the package 'some_package'
COPY forecaster.py /var/lang/lib/python3.12/site-packages/prophet/forecaster.py

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]