#!/usr/bin/env python3
"""
RFP Agent System - FastAPI Web Server

Provides REST API endpoints for:
- Analyzing RFP documents
- Evaluating response quality
- Managing product knowledge base
- System monitoring
"""

import asyncio
import json
from pathlib import Path
from typing import Optional, List
from datetime import datetime
import logging

from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from rfp_agent_system import (
    ProductKnowledgeBase,
    generate_rfp_response,
    SAMPLE_PRODUCTS
)
from scripts.evaluate_response import ResponseEvaluator

# ============================================================================
# CONFIGURATION
# ============================================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RFP Response Agent API",
    description="AI-powered RFP analysis and response generation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
knowledge_base: Optional[ProductKnowledgeBase] = None
evaluator = ResponseEvaluator()
api_metrics = {
    "total_requests": 0,
    "total_analyses": 0,
    "total_evaluations": 0,
    "avg_response_time": 0,
}


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class ProductInput(BaseModel):
    """Product data model"""
    id: str
    name: str
    category: str
    description: str
    features: str
    pricing: str
    sla: str
    compliance: str
    case_studies: str


class RFPAnalysisRequest(BaseModel):
    """Request model for RFP analysis"""
    rfp_text: str
    use_multi_agent: bool = True


class RFPAnalysisResponse(BaseModel):
    """Response model for RFP analysis"""
    status: str
    timestamp: str
    analysis: dict
    product_context: str
    sections: Optional[dict] = None
    response_text: Optional[str] = None


class EvaluationRequest(BaseModel):
    """Request model for response evaluation"""
    rfp_text: str
    response_text: str


class EvaluationResponse(BaseModel):
    """Response model for evaluation"""
    timestamp: str
    overall_score: float
    recommendation: str
    sections: dict
    analysis: dict


class ProductSearchRequest(BaseModel):
    """Request model for product search"""
    query: str
    n_results: int = 5


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    version: str
    knowledge_base_loaded: bool
    products_count: int


class MetricsResponse(BaseModel):
    """Metrics response"""
    total_requests: int
    total_analyses: int
    total_evaluations: int
    avg_response_time: float
    uptime: str


# ============================================================================
# INITIALIZATION
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    global knowledge_base
    
    logger.info("🚀 Starting RFP Agent API...")
    
    try:
        # Initialize knowledge base
        knowledge_base = ProductKnowledgeBase(db_path="./chroma_db")
        knowledge_base.load_products(SAMPLE_PRODUCTS)
        logger.info(f"✅ Knowledge base loaded with {len(SAMPLE_PRODUCTS)} products")
    except Exception as e:
        logger.error(f"❌ Error initializing knowledge base: {e}")
        raise


# ============================================================================
# HEALTH CHECK ENDPOINTS
# ============================================================================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    api_metrics["total_requests"] += 1
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        knowledge_base_loaded=knowledge_base is not None,
        products_count=len(SAMPLE_PRODUCTS) if knowledge_base else 0
    )


@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get API metrics"""
    return MetricsResponse(**api_metrics)


@app.get("/status")
async def get_status():
    """Get system status"""
    api_metrics["total_requests"] += 1
    
    return {
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "knowledge_base": "loaded" if knowledge_base else "not_loaded",
        "products": len(SAMPLE_PRODUCTS),
        "api_version": "1.0.0"
    }


# ============================================================================
# RFP ANALYSIS ENDPOINTS
# ============================================================================

@app.post("/analyze", response_model=RFPAnalysisResponse)
async def analyze_rfp(request: RFPAnalysisRequest):
    """Analyze RFP and generate response
    
    Args:
        request: RFPAnalysisRequest with rfp_text and use_multi_agent flag
    
    Returns:
        RFPAnalysisResponse with analysis and response sections
    """
    api_metrics["total_requests"] += 1
    api_metrics["total_analyses"] += 1
    
    if not knowledge_base:
        raise HTTPException(status_code=503, detail="Knowledge base not initialized")
    
    if not request.rfp_text or len(request.rfp_text.strip()) < 50:
        raise HTTPException(status_code=400, detail="RFP text too short (minimum 50 characters)")
    
    try:
        logger.info(f"📋 Analyzing RFP ({len(request.rfp_text)} chars)...")
        
        # Generate response
        response = await generate_rfp_response(
            request.rfp_text,
            knowledge_base,
            use_agents=request.use_multi_agent
        )
        
        logger.info(f"✅ Analysis complete")
        
        return RFPAnalysisResponse(
            status="success",
            timestamp=datetime.now().isoformat(),
            analysis=response.get("analysis", {}),
            product_context=response.get("product_context", ""),
            sections=response.get("sections"),
            response_text=response.get("response")
        )
    
    except Exception as e:
        logger.error(f"❌ Error analyzing RFP: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/file")
async def analyze_rfp_file(file: UploadFile = File(...)):
    """Analyze RFP from uploaded file
    
    Args:
        file: Uploaded RFP document (txt or md)
    
    Returns:
        RFPAnalysisResponse
    """
    api_metrics["total_requests"] += 1
    api_metrics["total_analyses"] += 1
    
    if not knowledge_base:
        raise HTTPException(status_code=503, detail="Knowledge base not initialized")
    
    try:
        # Read file
        content = await file.read()
        rfp_text = content.decode('utf-8')
        
        logger.info(f"📄 Analyzing uploaded file: {file.filename}")
        
        # Generate response
        response = await generate_rfp_response(
            rfp_text,
            knowledge_base,
            use_agents=True
        )
        
        return RFPAnalysisResponse(
            status="success",
            timestamp=datetime.now().isoformat(),
            analysis=response.get("analysis", {}),
            product_context=response.get("product_context", ""),
            sections=response.get("sections"),
            response_text=response.get("response")
        )
    
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 text")
    except Exception as e:
        logger.error(f"❌ Error processing file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# EVALUATION ENDPOINTS
# ============================================================================

@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_response(request: EvaluationRequest):
    """Evaluate RFP response quality
    
    Args:
        request: EvaluationRequest with rfp_text and response_text
    
    Returns:
        EvaluationResponse with scores and feedback
    """
    api_metrics["total_requests"] += 1
    api_metrics["total_evaluations"] += 1
    
    try:
        logger.info("🔍 Evaluating response...")
        
        result = evaluator.evaluate(
            request.rfp_text,
            request.response_text
        )
        
        logger.info(f"✅ Evaluation complete: {result.overall_score:.1f}/100")
        
        return EvaluationResponse(
            timestamp=result.timestamp,
            overall_score=result.overall_score,
            recommendation=result.recommendation,
            sections=result.to_dict()["sections"],
            analysis=result.to_dict()["analysis"]
        )
    
    except Exception as e:
        logger.error(f"❌ Error evaluating response: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PRODUCT KNOWLEDGE BASE ENDPOINTS
# ============================================================================

@app.get("/products")
async def list_products():
    """List all products in knowledge base"""
    api_metrics["total_requests"] += 1
    
    if not knowledge_base:
        raise HTTPException(status_code=503, detail="Knowledge base not initialized")
    
    return {
        "total": len(SAMPLE_PRODUCTS),
        "products": SAMPLE_PRODUCTS
    }


@app.post("/products/add")
async def add_product(product: ProductInput):
    """Add a new product to knowledge base
    
    Args:
        product: ProductInput with product details
    
    Returns:
        Success message
    """
    api_metrics["total_requests"] += 1
    
    if not knowledge_base:
        raise HTTPException(status_code=503, detail="Knowledge base not initialized")
    
    try:
        logger.info(f"➕ Adding product: {product.name}")
        
        # Add to knowledge base
        knowledge_base.load_products([product.dict()])
        
        # Also add to sample products for consistency
        SAMPLE_PRODUCTS.append(product.dict())
        
        logger.info(f"✅ Product added: {product.name}")
        
        return {
            "status": "success",
            "message": f"Product '{product.name}' added successfully",
            "product_id": product.id
        }
    
    except Exception as e:
        logger.error(f"❌ Error adding product: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/products/search", response_model=dict)
async def search_products(request: ProductSearchRequest):
    """Search products in knowledge base
    
    Args:
        request: ProductSearchRequest with query and n_results
    
    Returns:
        List of matching products
    """
    api_metrics["total_requests"] += 1
    
    if not knowledge_base:
        raise HTTPException(status_code=503, detail="Knowledge base not initialized")
    
    try:
        logger.info(f"🔍 Searching products: {request.query}")
        
        results = knowledge_base.search(
            request.query,
            n_results=request.n_results
        )
        
        return {
            "query": request.query,
            "total_results": len(results),
            "results": results
        }
    
    except Exception as e:
        logger.error(f"❌ Error searching products: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# BATCH OPERATIONS
# ============================================================================

@app.post("/batch/analyze")
async def batch_analyze(requests: List[RFPAnalysisRequest], background_tasks: BackgroundTasks):
    """Analyze multiple RFPs (batch operation)
    
    Args:
        requests: List of RFPAnalysisRequest objects
    
    Returns:
        Job ID for tracking progress
    """
    api_metrics["total_requests"] += 1
    
    if not knowledge_base:
        raise HTTPException(status_code=503, detail="Knowledge base not initialized")
    
    if len(requests) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 RFPs per batch")
    
    job_id = f"batch_{datetime.now().timestamp()}"
    logger.info(f"📦 Starting batch analysis: {job_id} ({len(requests)} RFPs)")
    
    # Would typically save to database or queue
    return {
        "job_id": job_id,
        "status": "queued",
        "total_items": len(requests),
        "message": "Batch analysis queued. Check /batch/status/{job_id} for progress."
    }


@app.get("/batch/status/{job_id}")
async def batch_status(job_id: str):
    """Get batch operation status
    
    Args:
        job_id: Job ID from batch operation
    
    Returns:
        Job status and progress
    """
    api_metrics["total_requests"] += 1
    
    # Placeholder implementation
    return {
        "job_id": job_id,
        "status": "processing",
        "progress": 0,
        "message": "Batch operation in progress"
    }


# ============================================================================
# EXPORT/DOWNLOAD ENDPOINTS
# ============================================================================

@app.post("/export/response")
async def export_response(request: RFPAnalysisRequest):
    """Export response as downloadable file
    
    Args:
        request: RFPAnalysisRequest
    
    Returns:
        JSON file for download
    """
    api_metrics["total_requests"] += 1
    
    if not knowledge_base:
        raise HTTPException(status_code=503, detail="Knowledge base not initialized")
    
    try:
        response = await generate_rfp_response(
            request.rfp_text,
            knowledge_base,
            use_agents=request.use_multi_agent
        )
        
        # Save to temporary file
        filename = f"rfp_response_{datetime.now().timestamp()}.json"
        with open(filename, 'w') as f:
            json.dump(response, f, indent=2)
        
        return FileResponse(
            filename,
            media_type="application/json",
            filename=filename
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"❌ Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/")
async def root():
    """API documentation and usage"""
    api_metrics["total_requests"] += 1
    
    return {
        "title": "RFP Response Agent API",
        "version": "1.0.0",
        "description": "AI-powered RFP analysis and response generation",
        "endpoints": {
            "health": "/health",
            "status": "/status",
            "metrics": "/metrics",
            "analyze": "POST /analyze",
            "analyze_file": "POST /analyze/file",
            "evaluate": "POST /evaluate",
            "products_list": "GET /products",
            "products_add": "POST /products/add",
            "products_search": "POST /products/search",
            "batch_analyze": "POST /batch/analyze",
            "batch_status": "GET /batch/status/{job_id}",
            "export_response": "POST /export/response"
        },
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    host = "0.0.0.0"
    port = 8000
    reload = False
    
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    if "--reload" in sys.argv:
        reload = True
    
    logger.info(f"🚀 Starting server on {host}:{port}")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
