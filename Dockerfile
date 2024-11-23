FROM python:3.9-slim

# Create data directory with proper permissions
RUN mkdir /data && chmod 777 /data

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Command to run the application
CMD ["python", "src/bot.py"]