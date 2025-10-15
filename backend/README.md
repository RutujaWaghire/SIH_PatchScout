# PatchScout Backend - Centralized Vulnerability Detection System

## Overview
PatchScout is a unified AI-driven vulnerability management platform with FastAPI backend that consolidates five security scanning tools (Nmap, OpenVAS, Nessus, Nikto, Nuclei) with intelligent analysis and attack path visualization.

## Architecture

### Technology Stack
- **Backend Framework**: FastAPI (Python 3.9+)
- **Databases**: 
  - PostgreSQL (normalized vulnerability data)
  - ChromaDB (vector embeddings for RAG)
  - Neo4j (attack path graphs)
- **AI/ML**: LangChain, Hugging Face Transformers, sentence-transformers
- **External APIs**: NVD, ExploitDB (mocked), Rapid7

### Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Configuration management
│   ├── database.py                # Database connections
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── scan.py
│   │   ├── vulnerability.py
│   │   └── cve_data.py
│   ├── schemas/                   # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── scan.py
│   │   ├── vulnerability.py
│   │   └── chat.py
│   ├── api/                       # API endpoints
│   │   ├── __init__.py
│   │   ├── scans.py
│   │   ├── vulnerabilities.py
│   │   ├── chat.py
│   │   └── attack_paths.py
│   ├── services/                  # Business logic
│   │   ├── __init__.py
│   │   ├── scanning_engine/
│   │   │   ├── __init__.py
│   │   │   ├── nmap_scanner.py
│   │   │   ├── openvas_scanner.py
│   │   │   ├── nessus_scanner.py
│   │   │   ├── nikto_scanner.py
│   │   │   ├── nuclei_scanner.py
│   │   │   └── orchestrator.py
│   │   ├── data_processing/
│   │   │   ├── __init__.py
│   │   │   ├── normalizer.py
│   │   │   └── deduplicator.py
│   │   ├── threat_intelligence/
│   │   │   ├── __init__.py
│   │   │   ├── nvd_service.py
│   │   │   └── exploitdb_service.py
│   │   ├── attack_path/
│   │   │   ├── __init__.py
│   │   │   └── graph_generator.py
│   │   └── rag_chatbot/
│   │       ├── __init__.py
│   │       ├── embeddings.py
│   │       └── chatbot.py
│   └── utils/
│       ├── __init__.py
│       ├── logging.py
│       └── validators.py
├── tests/
│   ├── __init__.py
│   ├── test_scanners.py
│   ├── test_api.py
│   └── test_integration.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── scripts/
│   ├── init_db.py
│   └── seed_data.py
├── requirements.txt
├── .env.example
└── README.md
```

## Key Features

### 1. Unified Scanning Engine
- **Nmap**: Network discovery, port scanning, service detection
- **OpenVAS**: Comprehensive vulnerability assessment (mocked)
- **Nessus**: Professional compliance scanning (mocked with sample data)
- **Nikto**: Web server vulnerability scanning
- **Nuclei**: Template-based fast scanning

### 2. Data Processing Pipeline
- Normalizes output from all scanners to common CVE/CVSS format
- Deduplicates findings across multiple tools
- Enriches with threat intelligence from NVD and ExploitDB

### 3. Attack Path Analysis
- Neo4j graph database for modeling attack chains
- Identifies lateral movement opportunities
- Prioritizes vulnerabilities by attack path impact

### 4. RAG-Powered AI Assistant
- ChromaDB vector storage for vulnerability knowledge base
- LangChain retrieval for context-aware responses
- Hugging Face transformers for natural language generation
- Plain-language explanations of CVEs and remediation steps

### 5. Real-time Updates
- WebSocket support for live scan progress
- Async processing with Python asyncio
- Background task management

## Installation

### Prerequisites
```bash
- Python 3.9+
- Docker and Docker Compose
- PostgreSQL 14+
- Neo4j 4.4+
```

### Setup
```bash
# Clone repository
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your configuration

# Start Docker services
docker-compose up -d

# Initialize database
python scripts/init_db.py

# Run application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, access:
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Key Endpoints

#### Scanning
- `POST /api/v1/scans/initiate` - Start new vulnerability scan
- `GET /api/v1/scans/{scan_id}` - Get scan status
- `GET /api/v1/scans/{scan_id}/vulnerabilities` - List findings
- `WS /ws/scan-updates/{scan_id}` - Real-time progress

#### Vulnerability Analysis
- `GET /api/v1/vulnerabilities/{vuln_id}/details` - Detailed CVE info
- `GET /api/v1/vulnerabilities/{vuln_id}/exploits` - Exploit availability
- `GET /api/v1/attack-paths/{scan_id}` - Attack path visualization

#### AI Assistant
- `POST /api/v1/chat/query` - RAG chatbot interaction
- `GET /api/v1/chat/history/{session_id}` - Conversation history

#### Reporting
- `GET /api/v1/reports/{scan_id}` - Generate assessment report
- `GET /api/v1/reports/{scan_id}/export` - Export as PDF/JSON

## Configuration

### Environment Variables (.env)
```bash
# Application
APP_NAME=PatchScout
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/patchscout
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# ChromaDB
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_COLLECTION_NAME=vulnerabilities

# External APIs
NVD_API_KEY=your-nvd-api-key
EXPLOITDB_MOCK=True

# Scanning Configuration
MAX_CONCURRENT_SCANS=5
SCAN_TIMEOUT=3600
NMAP_PATH=/usr/bin/nmap
NIKTO_PATH=/usr/bin/nikto
NUCLEI_PATH=/usr/bin/nuclei

# AI/ML
HUGGINGFACE_MODEL=microsoft/DialoGPT-medium
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

## Security Considerations

### Containerization
All scanning operations are containerized for isolation and safety:
- Subprocess execution with strict timeouts
- Network namespace isolation
- Resource limits (CPU, memory)
- Input sanitization and validation

### Authentication
- JWT-based authentication (configurable)
- API key support for external integrations
- Rate limiting on all endpoints

### Data Privacy
- Encrypted database connections
- Secure credential storage
- Audit logging for all operations

## Development

### Running Tests
```bash
# Unit tests
pytest tests/unit -v

# Integration tests
pytest tests/integration -v

# Coverage report
pytest --cov=app tests/
```

### Code Quality
```bash
# Linting
flake8 app/
pylint app/

# Type checking
mypy app/

# Format code
black app/
isort app/
```

## Deployment

### Docker Deployment
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Production Considerations
- Use Gunicorn with Uvicorn workers
- Enable HTTPS with reverse proxy (Nginx/Traefik)
- Configure proper logging (ELK stack)
- Set up monitoring (Prometheus + Grafana)
- Implement backup strategy for databases

## Performance

### Optimization
- Database connection pooling
- Redis caching layer
- Async processing with Celery (optional)
- Vector index optimization in ChromaDB
- Neo4j query optimization

### Scalability
- Horizontal scaling with load balancer
- Microservices architecture for heavy components
- Message queue for scan orchestration

## Troubleshooting

### Common Issues

**Database Connection Errors**
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Reset database
docker-compose down -v
docker-compose up -d postgres
python scripts/init_db.py
```

**Scanner Not Found**
```bash
# Install scanning tools
sudo apt-get install nmap nikto
# Install Nuclei from GitHub releases
```

**ChromaDB Issues**
```bash
# Clear ChromaDB cache
rm -rf ./chroma_db
python scripts/init_embeddings.py
```

## Roadmap

- [ ] Real OpenVAS integration via OMP protocol
- [ ] Paid Nessus API integration
- [ ] CVSS 4.0 support
- [ ] Machine learning for vulnerability prioritization
- [ ] Custom scanning templates
- [ ] Multi-tenancy support
- [ ] SIEM integration (Splunk, ELK)

## Contributing
See CONTRIBUTING.md for development guidelines.

## License
MIT License - See LICENSE file for details.

## Support
- Documentation: https://docs.patchscout.io
- Issues: https://github.com/patchscout/backend/issues
- Discord: https://discord.gg/patchscout
