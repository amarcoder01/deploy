# Ultra-lightweight Dockerfile for Replit deployment
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy minimal requirements first
COPY deploy-requirements.txt ./

# Install only essential dependencies with no cache to reduce size
RUN pip install --no-cache-dir --no-deps -r deploy-requirements.txt

# Copy only essential bot files
COPY Bot_Deployment/minimal_main.py ./Bot_Deployment/main.py
COPY Bot_Deployment/telegram_handler.py ./Bot_Deployment/
COPY Bot_Deployment/market_data_service.py ./Bot_Deployment/
COPY Bot_Deployment/openai_service.py ./Bot_Deployment/
COPY Bot_Deployment/trade_service.py ./Bot_Deployment/
COPY Bot_Deployment/db.py ./Bot_Deployment/
COPY Bot_Deployment/models.py ./Bot_Deployment/
COPY Bot_Deployment/config.py ./Bot_Deployment/
COPY Bot_Deployment/logger.py ./Bot_Deployment/
COPY Bot_Deployment/security_config.py ./Bot_Deployment/
COPY Bot_Deployment/secure_logger.py ./Bot_Deployment/
COPY Bot_Deployment/performance_cache.py ./Bot_Deployment/
COPY Bot_Deployment/monitoring.py ./Bot_Deployment/
COPY Bot_Deployment/rate_limiter.py ./Bot_Deployment/
COPY Bot_Deployment/input_validator.py ./Bot_Deployment/
COPY start.py ./

# Set environment
ENV PYTHONPATH=/app/Bot_Deployment
ENV PYTHONUNBUFFERED=1
ENV SKIP_HEAVY_DEPS=true

# Expose port
EXPOSE 5000

# Start command
CMD ["python", "start.py"]