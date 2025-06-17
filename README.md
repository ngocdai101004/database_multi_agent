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

## 🚀 Installation

### System Requirements
- Python 3.8+
- Node.js 16+ (for demo UI)
- PostgreSQL/MySQL/SQLite

### Install Dependencies

```bash
# Clone repository
git clone https://github.com/your-username/agentic-db-multi-agent.git
cd agentic-db-multi-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
```

### Configuration

1. Create `.env` file from template:
```bash
cp .env.example .env
```

2. Update environment variables:
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# LLM Configuration
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Notification Services (Optional)
SLACK_WEBHOOK_URL=your_slack_webhook
WHATSAPP_API_KEY=your_whatsapp_api
```

## 🎮 Usage

### Start Backend
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend
```bash
cd frontend
npm start
```

### API Endpoints

```bash
# Text-to-SQL conversion
POST /api/v1/query
{
    "query": "Find all customers with revenue over 100 million in the last quarter",
    "language": "en",
    "schema": "sales_db"
}

# Schema information
GET /api/v1/schemas

# Query history
GET /api/v1/history
```

## 📱 Demo

🎥 **[Live Demo](https://youtu.be/u28sVD9uv2M)**

Experience the system directly with a user-friendly web interface, supporting:
- Input queries in Vietnamese/English
- View auto-generated SQL
- Check dry-run results
- Monitor agent processing workflow

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI
- **AI/ML**: LangChain, LangGraph
- **Database**: SQLAlchemy, PostgreSQL
- **Architecture**: Clean Architecture

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Styling**: Bootstrap 5
- **State Management**: React Hooks

### AI/LLM
- **Models**: OpenAI GPT-4, Anthropic Claude
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

### 3. Business Process Optimization
- Automate repetitive query tasks
- Real-time performance monitoring
- Automated trend analysis

### 4. Democratized Data Access
- Bridge for non-SQL users
- User-friendly natural language interface
- Enterprise data access democratization

## 📊 Achievements

- ✅ Optimized pipeline for SQL generation
- ✅ High-quality SQL queries through validation
- ✅ High-accuracy user template processing
- ✅ Scalable and easily integrable architecture

## 🛣️ Roadmap

### Phase 2: Enterprise Integration
- [ ] SAP system adapters
- [ ] ERP workflow automation
- [ ] Intelligent dashboards
- [ ] Real-time data integration

### Phase 3: Enhanced User Experience
- [ ] Advanced filtering mechanisms
- [ ] Semantic search capabilities
- [ ] Performance optimization for large-scale datasets
- [ ] Guided query builder

## 🤝 Contributing

We welcome all contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is distributed under the MIT License. See `LICENSE` for more information.

## 📞 Contact

**Tran Ngoc Dai**
- 📧 Email: ngocdai101004@gmail.com
- 🔗 LinkedIn: [your-linkedin-profile](https://linkedin.com/in/your-profile)
- 🐙 GitHub: [@your-username](https://github.com/your-username)

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for AI/LLM framework
- [FastAPI](https://fastapi.tiangolo.com/) for web framework
- [React](https://reactjs.org/) for frontend framework
- Open source community for amazing tools and libraries

---

⭐ **If this project is helpful, please give us a star!** ⭐
