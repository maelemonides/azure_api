# Use the official Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir "pymongo[srv]" fastapi pydantic uvicorn

# Copy the current directory contents into the container at /app
COPY . .

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# If needed, you can also expose the port
EXPOSE 8000
