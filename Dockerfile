# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set default values for NATS_CHART_NAME and NAMESPACE
ENV NATS_CHART_NAME ""
ENV NAMESPACE ""

# Run app.py when the container launches
CMD ["python", "app.py"]
