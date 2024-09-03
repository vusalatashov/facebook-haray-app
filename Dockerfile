FROM python:3.9-slim

# Install required packages and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg2 \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*


# Set the environment variable for the ChromeDriver binary
ENV PATH="/usr/local/bin:${PATH}"

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copy the requirements file
COPY resources/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app

# Set the working directory
WORKDIR /app

# Set the entry point for the container
CMD ["python", "main.py"]