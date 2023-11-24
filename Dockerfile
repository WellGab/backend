# Use an official Python runtime as a parent image
FROM python:3.9.18-alpine3.18

# Install build dependencies
RUN apk add --no-cache build-base libffi-dev

# Install cffi and netifaces
RUN pip install cffi netifaces

# Set the working directory to /wellgab
WORKDIR /wellgab

# Copy the current directory contents into the container at /wellgab
COPY . /wellgab

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the app when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
