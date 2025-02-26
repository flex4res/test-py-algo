# Use a specific Python version
FROM python:3.8-slim

# RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the algorithm script into /app
WORKDIR /app
COPY my_algorithm.py .

# Make the script executable (optional)
RUN chmod +x my_algorithm.py

# Set the entrypoint to run the script
ENTRYPOINT ["python", "/app/my_algorithm.py"]
