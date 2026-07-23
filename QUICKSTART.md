# Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set API Key

**Option A: OpenAI**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

**Option B: Azure Foundry**
```bash
az login
export FOUNDRY_PROJECT_ENDPOINT="https://your-project.region.api.azureml.ms"
export FOUNDRY_MODEL_DEPLOYMENT_NAME="gpt-4.1"
```

### 3. Initialize Knowledge Base

```bash
python scripts/load_knowledge_base.py
```

### 4. Run Test

```bash
python main.py --test
```

You should see output like:
```
✅ Knowledge base ready (3 products)
📊 RFP size: 1234 characters
📝 Technical approach...
💰 Pricing section...
🔒 Compliance section...
✅ Response saved to rfp_response.json
```

## Usage Examples

### Analyze Your RFP

```bash
python main.py --rfp path/to/your_rfp.txt
cat rfp_response.json
```

### Interactive Mode

```bash
python main.py --interactive
# Paste your RFP, press Ctrl+D
```

### Use Single Agent (Faster)

```bash
python main.py --rfp path/to/rfp.txt --single-agent
```

## Adding Your Products

Edit `rfp_agent_system.py` and add your products to `SAMPLE_PRODUCTS`:

```python
SAMPLE_PRODUCTS = [
    {
        "id": "prod_1",
        "name": "Your Product",
        "category": "analytics",
        "description": "...",
        "features": "...",
        "pricing": "...",
        "sla": "...",
        "compliance": "...",
        "case_studies": "..."
    }
]
```

Then reload:
```bash
python scripts/load_knowledge_base.py
```

## Troubleshooting

**Q: "Chroma database not found"**
A: Run `python scripts/load_knowledge_base.py`

**Q: "Authentication failed"**
A: Check your API key: `echo $OPENAI_API_KEY`

**Q: Want to use a different vector DB?**
A: See `ADVANCED.md` for Pinecone, Weaviate, etc.

## Next Steps

- Read `README.md` for full documentation
- Check `examples/sample_rfp.txt` for RFP format
- Customize agent instructions in `rfp_agent_system.py`
- Add your product knowledge base
