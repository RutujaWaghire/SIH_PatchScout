🧠 PatchScout AI Assistant

An AI-driven Centralized Vulnerability Detection and Intelligent Query Interface
Developed by Team PatchScout for Smart India Hackathon 2025 (Problem ID: SIH25234) under the Smart Automation theme.

🚀 Overview

PatchScout is an AI-powered vulnerability detection and management platform that unifies multiple security tools into one intelligent dashboard.
It enables automated scanning, risk mapping, and natural language assistance through a Retrieval-Augmented Generation (RAG) chatbot — making security analysis faster, simpler, and smarter.

🔍 Key Features

All-in-One Scanner:
Integrates five top security tools (Nmap, OpenVAS, Nessus, Nikto, Nuclei) for comprehensive coverage.

Easy-to-Use Interface:
Simple web app where users can scan any website for vulnerabilities in one click.

AI Chatbot Assistant:
Uses LangChain + HuggingFace models to explain findings and recommend fixes in plain English.

Attack Path Visualization:
Neo4j-based graphs to visualize chained exploits and attack flow.

Smart Reports:
Generates summarized, prioritized vulnerability reports with actionable remediation guidance.

Threat Intelligence Integration:
Connects to NVD, ExploitDB, and Rapid7 for real-time vulnerability updates.

⚙️ Tech Stack

Frontend: React.js, TypeScript, Tailwind CSS
Backend: Python, FastAPI
AI Chatbot: LangChain RAG, HuggingFace Transformers, Neo4j Graphs
Databases: PostgreSQL, ChromaDB (vector DB), Neo4j
Scanning Tools: Nmap, OpenVAS, Nessus, Nikto, Nuclei
Threat Intelligence APIs: NVD, ExploitDB, Rapid7

🧩 System Architecture

Scan: Perform multi-tool vulnerability scans on targets.

Normalize: Aggregate and normalize vulnerability data.

Analyze: Correlate findings using AI and threat intelligence sources.

Assist: Use the RAG chatbot for natural-language explanations and fixes.

Output: Visual attack path graphs, reports, and remediation steps.

💡 Innovation & Uniqueness

First unified platform combining multiple scanners with AI-driven contextual reasoning.

RAG-based chatbot for real-time, human-friendly vulnerability explanations.

Attack path modeling powered by Neo4j for deep risk visualization.

Automated risk normalization for faster triage and response.

🔄 Feasibility

Technically Viable: Built using proven frameworks (FastAPI, React, LangChain).

Market Demand: High need among SOC teams for unified vulnerability management.

Financially Scalable: SaaS-ready design reducing licensing overhead.

Legally Compliant: Adheres to cybersecurity and privacy standards with full audit control.

🧱 Risk Mitigation
Risk	Mitigation
Integration complexity	Standardized APIs and unified data schemas
AI model inaccuracies	Regular retraining with curated threat datasets
Performance bottlenecks	Auto-scaling with container orchestration
Data privacy issues	Encryption, RBAC, MFA, and audit logs
📊 Impact & Benefits

🔹 Reduces manual effort by automating scanning and reporting

🔹 Increases accuracy via AI-driven analysis

🔹 Lowers costs by consolidating multiple tools

🔹 Improves collaboration through chatbot-based guidance

🔹 Accelerates incident response time

📎 Resources

GitHub Repository: https://github.com/RutujaWaghire/SIH_PatchScout

Prototype Demo Video: YouTube Demo
Link :https://youtu.be/DSgYR-I0SKg

NVD - National Vulnerability Database

ExploitDB

Rapid7 Threat Intelligence

LangChain Documentation

Research on AI-based Attack Graphs

👥 Team PatchScout

Mentors:

Prof. A. P. Bangar – Assistant Professor, Computer Networks

Mr. Dharmesh Vala – Software Engineer, Industry Mentor
