FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY calculator.py /app/calculator.py

# A named Docker volume mounted at /results can be written by this non-root user.
RUN groupadd --gid 10001 researcher \
    && useradd --uid 10001 --gid 10001 --create-home researcher \
    && mkdir -p /results \
    && chown researcher:researcher /results

USER researcher

# Used if someone runs the image outside the Portainer tutorial.
CMD ["python", "/app/calculator.py", "add", "2", "3"]
