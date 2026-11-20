# Use a slim base image for smaller size
FROM python:3.14-slim

# Set environment variables for cleaner output and no cached bytecode
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY ./src .

RUN useradd --create-home appuser
USER appuser

EXPOSE 8765

CMD ["python", "main.py"]
