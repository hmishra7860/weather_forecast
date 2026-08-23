# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to utilize Docker caching
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code and images into the container
COPY . .

# Expose the default port Streamlit uses (8501)
EXPOSE 8501

# Run the Streamlit application on startup
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

