# RFP Response Agent System

An AI-powered system that automatically analyzes RFP documents and generates response drafts using your product knowledge base.

## Architecture

```
┌─────────────────────────────┐
│  Product Knowledge Base     │  (Chroma Vector DB)
│  - Datasheets              │  - Pricing
│  - Case studies            │  - Feature matrix
│  - Specifications          │  - Compliance docs
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  RFP Analyzer Agent         │  (Agent Framework)
│  - Parse RFP requirements  │
│  - Extract key sections    │
│  - Retrieve relevant docs  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Response Generator         │  (Multi-Agent Workflow)
│  - Technical lead           │
│  - Pricing lead             │
│  - Compliance lead          │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  RFP Response Draft         │
│  (Ready for review)         │
└─────────────────────────────┘
```

## Features

✅ Free vector database (Chroma)
✅ Multi-agent orchestration (Agent Framework)
✅ RAG (Retrieval-Augmented Generation)
✅ Interactive CLI
✅ Batch processing
✅ Parallel agent execution
✅ Structured JSON output

## Tech Stack

- **Vector DB**: Chroma (free, persistent)
- **Agent Framework**: Microsoft Agent Framework
- **LLM**: OpenAI or Azure Foundry
- **Language**: Python 3.10+

## Installation

### 1. Clone & Setup

```bash
git clone https://github.com/sl3v3r/RFP-Tools.git
cd RFP-Tools
git checkout RFP-Tools
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

**Option A: Azure Foundry**
```bash
export FOUNDRY_PROJECT_ENDPOINT="https://your-project.region.api.azureml.ms"
export FOUNDRY_MODEL_DEPLOYMENT_NAME="gpt-4.1"
# Use: az login
```

**Option B: OpenAI**
```bash
export OPENAI_API_KEY="sk-..."
```

### 4. Initialize Knowledge Base

```bash
python scripts/load_knowledge_base.py
```

## Quick Start

### Analyze a Single RFP

```bash
python main.py --rfp examples/sample_rfp.txt
```

Output saved to: `rfp_response.json`

### Interactive Mode

```bash
python main.py --interactive
# Paste RFP document, press Ctrl+D (Mac/Linux) or Ctrl+Z (Windows)
```

### Use Single Agent (Simpler)

```bash
python main.py --rfp examples/sample_rfp.txt --single-agent
```

## Usage Examples

### Example 1: Batch Process Multiple RFPs

```python
import asyncio
from rfp_agent_system import ProductKnowledgeBase, generate_rfp_response

async def process_rfps():
    kb = ProductKnowledgeBase()
    kb.load_products(SAMPLE_PRODUCTS)
    
    for rfp_file in Path("rfps/").glob("*.txt"):
        with open(rfp_file) as f:
            rfp_text = f.read()
        
        response = await generate_rfp_response(rfp_text, kb)
        print(f"Processed: {rfp_file.name}")

asyncio.run(process_rfps())
```

### Example 2: Add Your Own Products

```python
from rfp_agent_system import ProductKnowledgeBase

kb = ProductKnowledgeBase()

my_products = [
    {
        "id": "prod_custom_1",
        "name": "My Product",
        "category": "analytics",
        "description": "...",
        "features": "...",
        "pricing": "...",
        "sla": "...",
        "compliance": "...",
        "case_studies": "..."
    }
]

kb.load_products(my_products)
```

### Example 3: Custom Agent Instructions

```python
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient

agent = Agent(
    client=FoundryChatClient(),
    name="CustomRFPAgent",
    instructions="Your custom instructions here..."
)
```

## Project Structure

```
RFP-Tools/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── main.py                        # Entry point
├── rfp_agent_system.py           # Core system
├── scripts/
│   └── load_knowledge_base.py    # Initialize KB with products
├── examples/
│   ├── sample_rfp.txt            # Sample RFP for testing
│   └── sample_response.json      # Example output
├── products/
│   ├── datasheets/               # Product documentation
│   └── pricing.json              # Pricing info
├── chroma_db/                    # Vector database (auto-created)
└── rfp_response.json             # Generated response output
```

## API Reference

### ProductKnowledgeBase

```python
from rfp_agent_system import ProductKnowledgeBase

kb = ProductKnowledgeBase(db_path="./chroma_db")

# Load products
kb.load_products(products_data)

# Search knowledge base
results = kb.search(query="analytics solutions", n_results=5)
```

### generate_rfp_response()

```python
response = await generate_rfp_response(
    rfp_text="...",
    kb=knowledge_base,
    use_agents=True  # Multi-agent or single analyzer
)

# Returns:
# {
#   "status": "success",
#   "analysis": "...",
#   "product_context": "...",
#   "sections": {
#     "technical_approach": "...",
#     "pricing": "...",
#     "compliance": "..."
#   }
# }
```

## Customization

### Adding Your Products

Edit `scripts/load_knowledge_base.py` and add your products to the list:

```python
MY_PRODUCTS = [
    {
        "id": "prod_1",
        "name": "My Product",
        "description": "...",
        # ... other fields
    }
]
```

### Modifying Agent Instructions

Edit agent creation functions in `rfp_agent_system.py`:

```python
async def create_technical_agent():
    agent = Agent(
        client=...,
        name="TechnicalLead",
        instructions="Your custom instructions..."  # Edit here
    )
    return agent
```

### Changing Response Format

Modify the response parsing in `generate_rfp_response()`:

```python
return {
    "status": "success",
    # Add/remove fields as needed
    "your_field": "your_value"
}
```

## Cost Analysis

| Component | Cost |
|-----------|------|
| Chroma (Vector DB) | **FREE** |
| Agent Framework | **FREE** |
| OpenAI API calls | Pay per token (~$0.01-0.10 per RFP) |
| Azure Foundry | Pay per token (~$0.01-0.10 per RFP) |
| **Total to start** | **$0** |

## Performance

- **RFP Analysis**: 5-15 seconds
- **Multi-agent response generation**: 30-60 seconds
- **Single-agent response**: 20-40 seconds
- **Knowledge base search**: <100ms

## Troubleshooting

### Issue: "Chroma database not found"
**Solution**: Run `python scripts/load_knowledge_base.py` to initialize

### Issue: "Authentication failed"
**Solution**: Verify environment variables are set:
```bash
echo $OPENAI_API_KEY  # or check Foundry credentials
```

### Issue: "No products found in knowledge base"
**Solution**: Run `python scripts/load_knowledge_base.py` again

## Advanced Features

### Batch Processing

See `examples/batch_process.py` for processing multiple RFPs in parallel.

### Evaluation Metrics

See `scripts/evaluate_response.py` to score response quality.

### Custom Vector Store

To use a different vector DB (Pinecone, Weaviate, etc.), implement the `ProductKnowledgeBase` interface.

## Contributing

Contributions welcome! Please:
1. Create a feature branch
2. Add tests
3. Submit a pull request

## License

MIT License - see LICENSE file

## Support

- 📖 [Agent Framework Docs](https://learn.microsoft.com/agent-framework/)
- 📚 [Chroma Docs](https://docs.trychroma.com/)
- 💬 [Microsoft Agent Framework Discord](https://discord.gg/b5zjErwbQM)

## Roadmap

- [ ] Support for PDF/DOCX RFP parsing
- [ ] Scoring rubric automation
- [ ] Response quality evaluation
- [ ] Team collaboration features
- [ ] Integration with Salesforce/HubSpot
- [ ] Multi-language support
