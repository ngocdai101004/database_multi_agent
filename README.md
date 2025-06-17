# Agentic AI-Based Database Multi-Agent System for SAP/ERP Workflow Automation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-orange.svg)](https://langchain.com/)

## 📖 Overview

A multi-agent system designed to automate database interaction workflows in SAP/ERP environments using Agentic AI. This project focuses on creating intelligent query strategies and converting natural language to SQL for smart database querying through coordinated agent collaboration.

## 🎯 Key Features

- **🤖 Multi-Agent Architecture**: System designed with 3 specialized agents operating in a pipeline
- **🌍 Multilingual Support**: Supports both Vietnamese and English
- **🔄 Feedback Loop**: Automatic feedback mechanism to improve SQL query quality
- **⚡ Smart Resource Management**: Automatically selects appropriate LLM models based on complexity
- **🔌 Easy Integration**: Seamless integration with existing SAP/ERP systems
- **📊 Real-time Validation**: SQL verification and validation through dry-run execution

## 🏗️ System Architecture

![System Architecture Pipeline](docs/pipeline.png)

The system consists of 3 main phases:

### 1. Intent Understanding (Agent: Planner)
- Language detection (Vietnamese/English)
- Query intent classification
- Entity and relationship extraction
- Complexity estimation
- Query restructuring based on conversation history

### 2. Context Preparation (Agent: Context Preparator)
- Retrieve appropriate schema
- Identify tables and relationships
- Map entities across multiple tables
- Enhance queries with actual metadata
- Prepare sample data for validation

### 3. Text-to-SQL Generation (Agent: SQL Generator)
- Select optimal LLM model
- Generate multiple SQL candidates
- Feedback loop with validator
- Validation through dry-run execution

## 📱 Demo

🎥 **[Live Demo](https://youtu.be/u28sVD9uv2M)**

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI
- **AI/ML**: LangChain, LangGraph
- **Database for dry run**: Sqlite3
- **Architecture**: Clean Architecture

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Styling**: Bootstrap 5
- **State Management**: React Hooks

### AI/LLM
- **Models**: OpenAI GPT-4,
- **Techniques**: ReAct, RAG, Tool Calling
- **Routing**: Dynamic LLM selection based on complexity

## 🎯 Real-world Applications

### 1. Intelligent Report Automation
- Generate reports from natural language requests
- Automated report templates (revenue, inventory, performance)
- Scheduled periodic reporting

### 2. Advanced Data Filtering System
- Complex condition queries
- Multi-dimensional filtering through natural language
- Efficient data mining
- 
### 3. Democratized Data Access
- Bridge for non-SQL users
- User-friendly natural language interface
- Enterprise data access democratization

## 📝 License

This project is distributed under the MIT License. See `LICENSE` for more information.

## 📞 Contact

**Tran Ngoc Dai**
- 📧 Email: ngocdai101004@gmail.com
- 🔗 LinkedIn: [Ngoc Dai Tran ](https://www.linkedin.com/in/tndai/)
- 🐙 GitHub: [@ngocdai101004](https://github.com/ngocdai101004)

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for AI/LLM framework
- [FastAPI](https://fastapi.tiangolo.com/) for web framework
- [React](https://reactjs.org/) for frontend framework
- Open source community for amazing tools and libraries

---

⭐ **If this project is helpful, please give us a star!** ⭐
