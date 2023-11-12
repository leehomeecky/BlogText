FROM python:3

WORKDIR /app

# Copy the local code to the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 8200

# Command to run the application
CMD ["sh", "-c", "python main.py"]