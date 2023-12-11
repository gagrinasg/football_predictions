# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the entire project to the container
COPY . /app

# Install Poetry
RUN pip install poetry==1.6.1 \
    && poetry --version

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Create a virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install uvicorn within the virtual environment
RUN /venv/bin/pip install uvicorn

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run uvicorn when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
