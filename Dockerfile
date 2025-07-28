# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of your application code to the container
COPY . .

# --- NEW LINES TO FIX PERMISSION ERROR ---
# Copy the pre-build script and make it executable
COPY pre_build_script.sh .
RUN chmod +x pre_build_script.sh

# Run the pre-build script
RUN ./pre_build_script.sh
# --- END OF NEW LINES ---

# Make port 7860 available to the world outside this container
EXPOSE 7860

# Command to run the application
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "7860"]