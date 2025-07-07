# Use a base Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /D:/MRSIC/MRSIC

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV STREAMLIT_API_KEY=$STREAMLIT_API_KEY
# Copy your application code
COPY . .

# Expose the port your application listens on (if it's a web app)
EXPOSE 8051
# Command to run your application when the container starts
CMD ["streamlit","run","main.py","--server.port=8501"] 
