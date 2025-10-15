"""
Pydantic schemas for AI chat operations.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ChatMessageSchema(BaseModel):
    """Schema for chat message."""
    role: str = Field(..., description="Role: user or assistant")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatSource(BaseModel):
    """Schema for RAG source citation."""
    type: str = Field(..., description="Source type: CVE, MITRE, NVD, etc.")
    title: str
    url: str
    relevance: float = Field(..., ge=0.0, le=1.0)


class ChatRequestSchema(BaseModel):
    """Schema for chat request."""
    message: str = Field(..., description="User message")
    rag_mode: bool = Field(default=True, description="Enable RAG context")
    scan_id: Optional[int] = None
    context_window: int = Field(default=5, ge=1, le=20)


class ChatResponseSchema(BaseModel):
    """Schema for chat response."""
    message: str
    sources: List[ChatSource] = Field(default_factory=list)
    rag_context_used: bool
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatHistorySchema(BaseModel):
    """Schema for chat history."""
    messages: List[ChatMessageSchema]
    scan_id: Optional[int]
