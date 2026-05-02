FROM python:3.11-slim

WORKDIR /app

# Copy Consumer code
COPY Consumer/consumer_runner.py Consumer/model_integration.py Consumer/s3_writer.py Consumer/utils/logger.py ./Consumer/


# Copy requirements
COPY Consumer/requirements.txt ./Consumer/

# Copy Model files
COPY Model/ ./Model/

# Install dependencies
RUN pip install --no-cache-dir -r Consumer/requirements.txt

CMD ["python", "Consumer/consumer_runner.py"]
