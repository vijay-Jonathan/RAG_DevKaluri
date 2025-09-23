"""
FastAPI server for RAG-based chatbot API endpoints.

This module provides REST API endpoints for external applications to interact
with the RAG chatbot system that answers questions about Dev using PDF documents.
"""

import os
# Disable ChromaDB telemetry to prevent telemetry errors
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY_IMPL"] = "none"

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uvicorn
from datetime import datetime
import logging

# Import the RAG functionality
from langchain_helper import execute_user_query

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG DevKaluri API",
    description="API for RAG-based chatbot that answers questions about Dev using PDF documents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class QueryRequest(BaseModel):
    """Request model for chat queries."""
    question: str = Field(..., min_length=1, max_length=1000, description="The question to ask about Dev")
    session_id: Optional[str] = Field(None, description="Optional session ID for conversation tracking")
    
    class Config:
        schema_extra = {
            "example": {
                "question": "Tell me about Dev's experience",
                "session_id": "user123_session1"
            }
        }

class QueryResponse(BaseModel):
    """Response model for chat queries."""
    answer: str = Field(..., description="The generated answer to the question")
    question: str = Field(..., description="The original question asked")
    session_id: Optional[str] = Field(None, description="Session ID if provided")
    timestamp: str = Field(..., description="Timestamp of the response")
    status: str = Field(default="success", description="Status of the request")
    
    class Config:
        schema_extra = {
            "example": {
                "answer": "Dev is a software engineer with experience in...",
                "question": "Tell me about Dev's experience",
                "session_id": "user123_session1",
                "timestamp": "2024-01-15T10:30:00Z",
                "status": "success"
            }
        }

class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Health status")
    timestamp: str = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")

class ErrorResponse(BaseModel):
    """Response model for errors."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: str = Field(..., description="Error timestamp")
    status: str = Field(default="error", description="Status of the request")

# API Endpoints

@app.get("/", response_model=Dict[str, Any])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "RAG DevKaluri API",
        "description": "API for RAG-based chatbot that answers questions about Dev",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "POST /chat": "Ask questions about Dev",
            "GET /health": "Health check endpoint"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        # You could add more sophisticated health checks here
        # like checking database connectivity, model availability, etc.
        return HealthResponse(
            status="healthy",
            timestamp=datetime.utcnow().isoformat() + "Z",
            version="1.0.0"
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unhealthy"
        )

@app.post("/chat", response_model=QueryResponse)
async def chat_with_dev(request: QueryRequest):
    """
    Ask questions about Dev and get AI-generated responses.
    
    This endpoint processes natural language questions about Dev using the RAG system
    and returns contextual answers based on the PDF documents in the knowledge base.
    """
    try:
        logger.info(f"Received query: {request.question[:100]}...")
        
        # Validate input
        if not request.question.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question cannot be empty"
            )
        
        # Execute the RAG query
        answer = execute_user_query(request.question)
        
        if not answer:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate response"
            )
        
        # Create response
        response = QueryResponse(
            answer=answer,
            question=request.question,
            session_id=request.session_id,
            timestamp=datetime.utcnow().isoformat() + "Z",
            status="success"
        )
        
        logger.info(f"Successfully processed query for session: {request.session_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.api_route("/chatbot", methods=["GET", "POST"])
async def chatbot_endpoint(
    question: Optional[str] = None,
    session_id: Optional[str] = None,
    request_body: Optional[QueryRequest] = None
):
    """
    Universal chatbot endpoint for frontend integration.
    
    Supports both GET and POST methods:
    - GET: http://localhost:8057/chatbot?question=Your question here
    - POST: Send JSON with {"question": "Your question", "session_id": "optional"}
    
    Perfect for frontend chatbot integration with clean responses.
    """
    try:
        # Handle POST request with JSON body
        if request_body:
            question = request_body.question
            session_id = request_body.session_id
        
        # Validate question
        if not question or not question.strip():
            return {
                "success": False,
                "error": "Question is required",
                "message": "Please provide a question to ask about Dev"
            }
        
        # Execute the RAG query
        logger.info(f"Chatbot query: {question[:100]}...")
        answer = execute_user_query(question)
        
        if not answer:
            return {
                "success": False,
                "error": "No response generated",
                "message": "Unable to generate a response. Please try again."
            }
        
        # Return clean response for frontend
        return {
            "success": True,
            "question": question,
            "answer": answer,
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        logger.error(f"Chatbot endpoint error: {str(e)}")
        return {
            "success": False,
            "error": "Internal server error",
            "message": "Something went wrong. Please try again later.",
            "details": str(e) if os.getenv("DEBUG") else None
        }

@app.get("/ask")
async def ask_question_get(question: str, session_id: Optional[str] = None):
    """
    Simple GET endpoint to ask questions via URL parameters.
    
    Usage: http://localhost:8000/ask?question=Tell me about Dev
    """
    try:
        if not question.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question parameter cannot be empty"
            )
        
        # Execute the RAG query
        answer = execute_user_query(question)
        
        return {
            "question": question,
            "answer": answer,
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in GET endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}"
        )

@app.post("/chat/batch", response_model=List[QueryResponse])
async def batch_chat(requests: List[QueryRequest]):
    """
    Process multiple questions in a single request.
    
    This endpoint allows you to send multiple questions at once and get responses
    for all of them. Useful for batch processing or when you have multiple related questions.
    """
    if len(requests) > 10:  # Limit batch size
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Batch size cannot exceed 10 questions"
        )
    
    responses = []
    for req in requests:
        try:
            answer = execute_user_query(req.question)
            response = QueryResponse(
                answer=answer,
                question=req.question,
                session_id=req.session_id,
                timestamp=datetime.utcnow().isoformat() + "Z",
                status="success"
            )
            responses.append(response)
        except Exception as e:
            logger.error(f"Error in batch processing: {str(e)}")
            error_response = QueryResponse(
                answer=f"Error processing question: {str(e)}",
                question=req.question,
                session_id=req.session_id,
                timestamp=datetime.utcnow().isoformat() + "Z",
                status="error"
            )
            responses.append(error_response)
    
    return responses

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "error"
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return {
        "error": "Internal server error",
        "detail": str(exc),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "error"
    }

if __name__ == "__main__":
    # Get port from environment variable (for deployment platforms) or default to 8057
    port = int(os.environ.get("PORT", 8057))
    
    # Run the server
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload in production
        log_level="info"
    )
