# AWS Batch Enrichment Assets

This folder keeps everything you need to run `scripts/enrich_related_terms.py` on AWS Batch/Fargate.

## Files
- `Dockerfile` – builds a minimal image with Python 3.11, dependencies, and the enrichment script.
- `requirements.txt` – pinned Python dependencies installed into the image.
- `job-definition.json` – sample Batch job definition wired for the `us-east-1` region. Update the account ID, IAM role, and S3 URIs to match your environment before registering it.

## Workflow Overview
1. **Upload inputs** – place `build/glossary.json` in S3 (for example `s3://ai-glossary-shailesh/input/glossary.json`).
2. **Build and push the image**
   ```bash
   docker build -t glossary-enrich -f infra/aws-batch/Dockerfile .
   aws --profile glossary ecr create-repository --repository-name glossary-enrich
   aws --profile glossary ecr get-login-password | docker login --username AWS --password-stdin 881254692732.dkr.ecr.us-east-1.amazonaws.com
   docker tag glossary-enrich 881254692732.dkr.ecr.us-east-1.amazonaws.com/glossary-enrich:latest
   docker push 881254692732.dkr.ecr.us-east-1.amazonaws.com/glossary-enrich:latest
   ```
3. **Register the job definition**
   ```bash
   aws --profile glossary batch register-job-definition \
     --cli-input-json file://infra/aws-batch/job-definition.json
   ```
4. **Create a Fargate compute environment and queue** – use the AWS console or CLI; point the queue at the compute environment.
5. **Submit the job**
   ```bash
   aws --profile glossary batch submit-job \
     --job-name enrich-500 \
     --job-queue glossary-queue \
     --job-definition glossary-enrich:1
   ```
6. **Download results** – when the job succeeds, sync the outputs from S3
   ```bash
   aws --profile glossary s3 sync s3://ai-glossary-shailesh/output ./build/related
   ```
7. **Clean up** – delete the Batch job, queue, compute environment, and empty the S3 output prefix to avoid lingering costs.

## What the container does
At runtime the script looks for three environment variables:
- `INPUT_S3_URI` – when set, the script downloads the glossary JSON into `build/glossary.json`.
- `OUTPUT_S3_PREFIX` – when set, the generated `related.json` and Markdown snippets are uploaded to that S3 prefix.
- `AWS_REGION` – optional hint so the boto3 client talks to the correct region.

If those variables are missing, the script falls back to the local file system so you can still run it on your laptop.
