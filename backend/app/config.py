"""
Application Configuration
Loads settings from environment variables
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "PatchScout"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-this"
    API_V1_STR: str = "/api/v1"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    RELOAD: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://patchscout:patchscout123@localhost:5432/patchscout_db"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Neo4j
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "neo4j_password"
    NEO4J_DATABASE: str = "neo4j"
    
    # ChromaDB
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "vulnerabilities"
    CHROMA_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600
    
    # External APIs
    NVD_API_KEY: str = ""
    NVD_API_URL: str = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    NVD_RATE_LIMIT: int = 5
    EXPLOITDB_MOCK: bool = True
    RAPID7_API_KEY: str = ""
    
    # Scanning
    MAX_CONCURRENT_SCANS: int = 5
    SCAN_TIMEOUT: int = 3600
    DEFAULT_SCAN_TYPE: str = "comprehensive"
    
    # Scanner Paths
    NMAP_PATH: str = "/usr/bin/nmap"
    NIKTO_PATH: str = "/usr/bin/nikto"
    NUCLEI_PATH: str = "/usr/local/bin/nuclei"
    OPENVAS_HOST: str = "localhost"
    OPENVAS_PORT: int = 9390
    
    # AI/ML
    HUGGINGFACE_MODEL: str = "microsoft/DialoGPT-medium"
    HUGGINGFACE_CACHE_DIR: str = "./model_cache"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    MAX_CHAT_HISTORY: int = 10
    RAG_TOP_K: int = 5
    RAG_SIMILARITY_THRESHOLD: float = 0.7
    
    # Security
    JWT_SECRET_KEY: str = "your-jwt-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://localhost:5000"
    ]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    LOG_FILE: str = "logs/patchscout.log"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 10
    
    # WebSocket
    WS_HEARTBEAT_INTERVAL: int = 30
    WS_MAX_CONNECTIONS: int = 100
    
    # Feature Flags
    ENABLE_REAL_NMAP: bool = True
    ENABLE_MOCK_OPENVAS: bool = True
    ENABLE_MOCK_NESSUS: bool = True
    ENABLE_REAL_NIKTO: bool = False
    ENABLE_REAL_NUCLEI: bool = False
    ENABLE_THREAT_INTEL: bool = True
    ENABLE_RAG_CHATBOT: bool = True
    ENABLE_ATTACK_PATHS: bool = True
    
    # Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    HEALTH_CHECK_INTERVAL: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        

# Create settings instance
settings = Settings()
