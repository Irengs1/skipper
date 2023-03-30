FROM python:3.10

RUN apt-get update && apt-get install -y nano

# Set the working directory to /app
WORKDIR /

# Copy the current directory contents into the container at /app
COPY . /

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run the app when the container launches
CMD ["python", "-u", "main.py"]
