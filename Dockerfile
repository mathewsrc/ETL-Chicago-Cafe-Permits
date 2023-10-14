FROM python:3.8

COPY ./requirements.txt /webapp/requirements.txt

# Set the working directory to /webapp
WORKDIR /webapp

# Copy the requirements file and install the dependencies
COPY ./requirements.txt /webapp/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip &&\
        pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

COPY webapp/* /webapp

EXPOSE 8000

# Creates a non-root user with an explicit UID and adds permission to access the /webapp folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /webapp
USER appuser

ENTRYPOINT [ "uvicorn" ]

CMD [ "--host", "0.0.0.0", "main:app" ]