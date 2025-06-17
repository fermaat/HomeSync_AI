# HomeSyncAI/src/Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY src/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire 'src' directory from the build context to /app/src
COPY src/ /app/src/

# Copy the entire 'cfg' directory from the build context to /app/cfg
COPY cfg/ /app/cfg/

# Expose the port your FastAPI app runs on
EXPOSE 8000

# Command to run the application
# Use 0.0.0.0 to listen on all interfaces inside the container
# Use --host 0.0.0.0 with uvicorn in Docker
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]