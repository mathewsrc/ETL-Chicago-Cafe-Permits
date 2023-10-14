# Base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt /app/requirements.txt

# Upgrade pip
RUN pip install --upgrade pip   

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY app/* /app

# Set the executable and the command to run the application
ENTRYPOINT [ "python" ]
CMD ["app.py"]
