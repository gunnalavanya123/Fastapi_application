# Use the official tiangolo/uvicorn-gunicorn-fastapi image as the base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Copy the entire current directory to /app in the Docker image
COPY ./ /backend

# Set the working directory to /app
WORKDIR /backend

# Install the dependencies if you have a requirements.txt
# Uncomment the below line if your project has a requirements.txt file
# RUN pip install -r requirements.txt

# Expose the application on port 8000
EXPOSE 8000

# Command to run the FastAPI app using Uvicorn with auto-reload enabled
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]

# Entry point for the container, this script will be executed when the container starts
# Ensure entrypoint.sh is executable and located in the project root directory
ENTRYPOINT ["/backend/entrypoint.sh"]
