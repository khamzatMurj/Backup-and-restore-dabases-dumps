# BACKUP-AND-RESTORE-DATABASES-DUMPS

> **Secure Data, Effortless Recovery, Unmatched Confidence**

![GitHub last commit](https://img.shields.io/github/last-commit/khamzatMury/Backup-and-restore-dabases-dumps?style=flat-square)
![Python](https://img.shields.io/badge/python-100%25-blue?style=flat-square)
![Languages](https://img.shields.io/badge/languages-1-blue?style=flat-square)

Built with:

![Markdown](https://img.shields.io/badge/-Markdown-000?style=flat-square&logo=markdown)
![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=flat-square&logo=fastapi)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker)
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python)

---

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)

---

## Overview

**Backup-and-restore-databases-dumps** is a developer-focused tool that automates PostgreSQL database backup and restore operations within a containerized environment. It leverages **Docker Compose** for orchestration and provides **REST API endpoints** for seamless data management, making data recovery and migration straightforward and reliable.

### Why use this tool?

This project aims to simplify database backup and restore workflows, ensuring consistency and automation. It is ideal for DevOps, database admins, and developers managing PostgreSQL in production or testing environments.

---

## Getting Started

### Prerequisites

Before installing, ensure you have the following:

- **Programming Language**: Python
- **Package Manager**: pip
- **Container Runtime**: Docker

---

### Installation
#### ⚠️ Note: This tool is designed to work properly only on Linux OS.

1. **Clone the repository:**

   ```bash
   git clone https://github.com/khamzatMury/Backup-and-restore-dabases-dumps


**To run the application:**

1. **Install dependencies (including Uvicorn):**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **(Optional) Access the Swagger Docs web UI:**
   ```
   http://localhost:8000/docs
   ```