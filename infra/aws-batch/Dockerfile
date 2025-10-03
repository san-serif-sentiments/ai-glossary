FROM public.ecr.aws/docker/library/python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTORCH_CPU_INDEX_URL=https://download.pytorch.org/whl/cpu

WORKDIR /app

COPY infra/aws-batch/requirements.txt requirements.txt
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential git \
    && pip install --upgrade pip \
    && pip install "torch==2.2.2" --index-url "$PYTORCH_CPU_INDEX_URL" \
    && pip install -r requirements.txt \
    && apt-get purge -y build-essential git \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY scripts/enrich_related_terms.py ./enrich_related_terms.py

CMD ["python", "enrich_related_terms.py"]
