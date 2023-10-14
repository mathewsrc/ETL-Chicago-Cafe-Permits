# Use the official Python 3.8 image as the base image
FROM python:3.8

# Set the working directory to /webapp
WORKDIR /webapp

# Copy the requirements.txt file from the host to the /webapp directory in the container
COPY ./requirements.txt /webapp/requirements.txt

# Install the Python packages listed in requirements.txt
RUN pip install -r requirements.txt

# Copy the contents of the "webapp" directory from the host to the /webapp directory in the container
COPY webapp/* /webapp

# Expose port 8000 for the application
EXPOSE 8000

# Create a non-root user with UID 5678 and no password, then grant permission to access the /webapp folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /webapp

# Set the user to "appuser" for improved security
USER appuser

# Define the entry point for the container as "uvicorn"
ENTRYPOINT [ "uvicorn" ]

# Specify the default command when the container starts
CMD [ "--host", "0.0.0.0", "main:app" ]
