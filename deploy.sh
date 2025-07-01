#!/bin/bash

# Build and deploy to Google Cloud Run
PROJECT_ID="agents-460202"
SERVICE_NAME="mcp-server"
REGION="us-central1"
REPOSITORY="cloud-run-source-deploy"

# Create Artifact Registry repository if it doesn't exist
gcloud artifacts repositories create ${REPOSITORY} \
    --repository-format=docker \
    --location=${REGION} \
    --description="Cloud Run source deployments" || echo "Repository already exists"

# Build and push the Docker image
gcloud builds submit --tag ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${SERVICE_NAME}

# Deploy to Cloud Run
gcloud run deploy ${SERVICE_NAME} \
    --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${SERVICE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --port 8000 \
    --project ${PROJECT_ID}