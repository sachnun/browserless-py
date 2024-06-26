# Python image
FROM python:latest

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port available to the world outside this container
EXPOSE 7860

# Run app.py when the container launches
CMD ["uvicorn", "web:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "4"]