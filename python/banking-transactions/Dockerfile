# Python runtime as parent image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Run tests
CMD ["pytest", "-q"]