# RFP Agent REST API Documentation

## Overview

The RFP Agent API provides RESTful endpoints for:
- Analyzing RFP documents
- Evaluating response quality
- Managing product knowledge base
- Batch processing
- System monitoring

**Base URL:** `http://localhost:8000`

**API Version:** 1.0.0

**Interactive Docs:** `http://localhost:8000/docs` (Swagger UI)

---

## Quick Start

### 1. Start the API

```bash
# Development
python app.py

# Production with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Docker
docker-compose up
```

### 2. Test Health Check

```bash
curl http://localhost:8000/health
```

### 3. Analyze an RFP

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "rfp_text": "REQUEST FOR PROPOSAL...",
    "use_multi_agent": true
  }'
```

---

## Endpoints

### Health & Status

#### GET `/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-07-23T17:45:00.000Z",
  "version": "1.0.0",
  "knowledge_base_loaded": true,
  "products_count": 3
}
```

#### GET `/status`
System status

**Response:**
```json
{
  "status": "operational",
  "timestamp": "2024-07-23T17:45:00.000Z",
  "knowledge_base": "loaded",
  "products": 3,
  "api_version": "1.0.0"
}
```

#### GET `/metrics`
API metrics and statistics

**Response:**
```json
{
  "total_requests": 42,
  "total_analyses": 15,
  "total_evaluations": 10,
  "avg_response_time": 2.5
}
```

---

### RFP Analysis

#### POST `/analyze`
Analyze RFP and generate response

**Request:**
```json
{
  "rfp_text": "REQUEST FOR PROPOSAL - Analytics Platform...\n\nWe need...",
  "use_multi_agent": true
}
```

**Parameters:**
- `rfp_text` (string, required): Full RFP document text (minimum 50 chars)
- `use_multi_agent` (boolean, optional): Use multi-agent orchestration (default: true)

**Response:**
```json
{
  "status": "success",
  "timestamp": "2024-07-23T17:45:00.000Z",
  "analysis": {
    "requirements": "Real-time dashboards, API access...",
    "evaluation_criteria": "Technical fit 40%, Cost 30%...",
    "recommended_products": ["CloudAnalytics Pro"]
  },
  "product_context": "Product: CloudAnalytics Pro...",
  "sections": {
    "technical_approach": "System architecture overview...",
    "pricing": "$5,000/month base...",
    "compliance": "SOC 2 Type II certification..."
  }
}
```

**Status Codes:**
- 200: Success
- 400: Invalid request (RFP too short)
- 500: Server error
- 503: Knowledge base not initialized

#### POST `/analyze/file`
Analyze RFP from uploaded file

**Request:**
```bash
curl -X POST http://localhost:8000/analyze/file \
  -F "file=@customer_rfp.txt"
```

**Response:** Same as `/analyze`

---

### Response Evaluation

#### POST `/evaluate`
Evaluate RFP response quality

**Request:**
```json
{
  "rfp_text": "REQUEST FOR PROPOSAL...",
  "response_text": "RESPONSE TO RFP...\n\nExecutive Summary..."
}
```

**Response:**
```json
{
  "timestamp": "2024-07-23T17:45:00.000Z",
  "overall_score": 78.5,
  "recommendation": "Good",
  "sections": {
    "completeness": {
      "score": 80,
      "max": 100,
      "weight": 0.15,
      "feedback": ["Found 7/9 expected sections"]
    },
    "relevance": {
      "score": 85,
      "max": 100,
      "weight": 0.25,
      "feedback": ["Addresses key requirements"]
    },
    "compliance": {
      "score": 70,
      "max": 100,
      "weight": 0.20,
      "feedback": ["Partial compliance coverage"]
    },
    "clarity": {
      "score": 82,
      "max": 100,
      "weight": 0.15,
      "feedback": ["Well-structured"]
    },
    "pricing": {
      "score": 75,
      "max": 100,
      "weight": 0.25,
      "feedback": ["Pricing included"]
    }
  },
  "analysis": {
    "strengths": ["Strong relevance: 85/100"],
    "weaknesses": ["Weak compliance: 70/100"],
    "improvements": ["Highlight relevant certifications"]
  }
}
```

---

### Product Management

#### GET `/products`
List all products in knowledge base

**Response:**
```json
{
  "total": 3,
  "products": [
    {
      "id": "prod_analytics_pro",
      "name": "CloudAnalytics Pro",
      "category": "analytics",
      "description": "Enterprise-grade real-time analytics platform",
      "features": "Real-time dashboards, API access...",
      "pricing": "$5,000/month base...",
      "sla": "99.99% uptime...",
      "compliance": "SOC 2, HIPAA, GDPR...",
      "case_studies": "Fortune 500 financial services..."
    }
  ]
}
```

#### POST `/products/add`
Add new product to knowledge base

**Request:**
```json
{
  "id": "prod_new",
  "name": "New Product",
  "category": "analytics",
  "description": "Product description",
  "features": "Feature1, Feature2, Feature3",
  "pricing": "$X/month",
  "sla": "99.9% uptime",
  "compliance": "SOC 2, GDPR",
  "case_studies": "Use case 1, Use case 2"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Product 'New Product' added successfully",
  "product_id": "prod_new"
}
```

#### POST `/products/search`
Search products by query

**Request:**
```json
{
  "query": "analytics solutions",
  "n_results": 5
}
```

**Response:**
```json
{
  "query": "analytics solutions",
  "total_results": 2,
  "results": [
    "Product: CloudAnalytics Pro...\nFeatures: Real-time dashboards...",
    "Product: DataAnalytics Suite...\nFeatures: Advanced analytics..."
  ]
}
```

---

### Batch Operations

#### POST `/batch/analyze`
Analyze multiple RFPs (batch operation)

**Request:**
```json
[
  {
    "rfp_text": "RFP Document 1...",
    "use_multi_agent": true
  },
  {
    "rfp_text": "RFP Document 2...",
    "use_multi_agent": true
  }
]
```

**Response:**
```json
{
  "job_id": "batch_1690138000.000",
  "status": "queued",
  "total_items": 2,
  "message": "Batch analysis queued. Check /batch/status/{job_id} for progress."
}
```

#### GET `/batch/status/{job_id}`
Check batch operation status

**Response:**
```json
{
  "job_id": "batch_1690138000.000",
  "status": "processing",
  "progress": 0,
  "message": "Batch operation in progress"
}
```

---

### Export

#### POST `/export/response`
Export response as downloadable JSON file

**Request:**
```json
{
  "rfp_text": "REQUEST FOR PROPOSAL...",
  "use_multi_agent": true
}
```

**Response:** JSON file download

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Error message",
  "error": "Additional error details"
}
```

### Common Status Codes

| Code | Meaning |
|------|----------|
| 200 | Success |
| 400 | Bad Request (invalid input) |
| 403 | Forbidden (auth required) |
| 404 | Not Found |
| 500 | Server Error |
| 503 | Service Unavailable (KB not loaded) |

### Example Error

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"rfp_text": "short"}'

# Response:
{
  "detail": "RFP text too short (minimum 50 characters)"
}
```

---

## Rate Limiting (Optional)

### Implementation

Add to `app.py`:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/analyze")
@limiter.limit("10/minute")
async def analyze_rfp(request: RFPAnalysisRequest):
    ...
```

---

## Authentication (Optional)

### API Key Authentication

Add to `app.py`:
```python
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.post("/analyze")
async def analyze_rfp(
    request: RFPAnalysisRequest,
    api_key: str = Depends(api_key_header)
):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")
    ...
```

### Bearer Token Authentication

```python
from fastapi.security import HTTPBearer, HTTPAuthenticationCredentials

security = HTTPBearer()

@app.post("/analyze")
async def analyze_rfp(
    request: RFPAnalysisRequest,
    credentials: HTTPAuthenticationCredentials = Depends(security)
):
    # Validate token
    ...
```

---

## Deployment

### Docker Compose (Recommended)

```bash
# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Start
docker-compose up -d

# Logs
docker-compose logs -f rfp-agent

# Stop
docker-compose down
```

### Kubernetes

**k8s/deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rfp-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rfp-agent
  template:
    metadata:
      labels:
        app: rfp-agent
    spec:
      containers:
      - name: rfp-agent
        image: rfp-agent:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: openai
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

### AWS Lambda + API Gateway

Use Mangum adapter:

```python
from mangum import Mangum
from app import app

handler = Mangum(app)
```

### Heroku

**Procfile:**
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

---

## Client Examples

### Python

```python
import requests

API_URL = "http://localhost:8000"

# Analyze RFP
response = requests.post(
    f"{API_URL}/analyze",
    json={
        "rfp_text": "REQUEST FOR PROPOSAL...",
        "use_multi_agent": True
    }
)
print(response.json())

# Evaluate response
response = requests.post(
    f"{API_URL}/evaluate",
    json={
        "rfp_text": "RFP...",
        "response_text": "Response..."
    }
)
print(response.json())
```

### JavaScript/Node.js

```javascript
const API_URL = "http://localhost:8000";

// Analyze RFP
const response = await fetch(`${API_URL}/analyze`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    rfp_text: "REQUEST FOR PROPOSAL...",
    use_multi_agent: true
  })
});

const data = await response.json();
console.log(data);
```

### cURL

```bash
# Analyze
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "rfp_text": "REQUEST FOR PROPOSAL...",
    "use_multi_agent": true
  }' | jq

# Evaluate
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "rfp_text": "RFP...",
    "response_text": "Response..."
  }' | jq

# Products
curl http://localhost:8000/products | jq
```

---

## Monitoring

### Prometheus Metrics

Add to `app.py`:
```python
from prometheus_client import Counter, Histogram

request_count = Counter('rfp_requests_total', 'Total requests')
request_duration = Histogram('rfp_request_duration_seconds', 'Request duration')

@app.middleware("http")
async def add_metrics(request, call_next):
    request_count.inc()
    # ... timing logic
    return response
```

### Logging

Logs are written to console and can be collected by:
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Splunk
- New Relic
- DataDog

---

## Performance Tips

1. **Caching**: Cache product searches with Redis
2. **Async**: All endpoints are async for better throughput
3. **Load Balancing**: Run multiple instances with nginx/HAProxy
4. **Database**: Use PostgreSQL for persistence
5. **Background Tasks**: Use Celery for long-running operations

---

## Support

For API issues:
1. Check `/health` endpoint
2. Review logs: `docker-compose logs rfp-agent`
3. Check `/metrics` for usage statistics
4. See `/docs` for interactive API documentation
