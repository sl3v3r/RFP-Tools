"""
RFP Agent System Core Module
Provides knowledge base management and multi-agent RFP response generation.
"""

import asyncio
import json
from typing import Optional
import chromadb

try:
    from agent_framework import Agent
    from agent_framework.foundry import FoundryChatClient
except ImportError:
    # Fallback if Agent Framework not available
    Agent = None
    FoundryChatClient = None


# ============================================================================
# SAMPLE PRODUCT DATA
# ============================================================================

SAMPLE_PRODUCTS = [
    {
        "id": "prod_analytics_pro",
        "name": "CloudAnalytics Pro",
        "category": "analytics",
        "description": "Enterprise-grade real-time analytics platform with 99.99% uptime SLA",
        "features": "Real-time dashboards, Custom reports, API access, ML integrations, Data warehousing, Custom connectors",
        "pricing": "$5,000/month base + $0.50 per GB ingested, minimum 12-month contract",
        "sla": "99.99% uptime, 15-minute response time for support",
        "compliance": "SOC 2 Type II, HIPAA, GDPR, FedRAMP (in progress)",
        "case_studies": "Fortune 500 financial services, healthcare analytics, retail chain optimization"
    },
    {
        "id": "prod_ai_suite",
        "name": "AI Training Suite Enterprise",
        "category": "ai_training",
        "description": "Managed machine learning platform for building, training, and deploying models at scale",
        "features": "AutoML, Distributed training, Model registry, GPU clusters, A/B testing, Experiment tracking",
        "pricing": "$10,000/month + compute costs ($2-5 per GPU hour)",
        "sla": "99.95% uptime, 24-hour support response",
        "compliance": "SOC 2 Type II, GDPR, CCPA, ISO 27001",
        "case_studies": "Computer vision for autonomous vehicles, NLP for customer service, Recommendation engines"
    },
    {
        "id": "prod_data_gov",
        "name": "DataGovernance Platform",
        "category": "governance",
        "description": "Centralized data governance, lineage tracking, and compliance monitoring",
        "features": "Data lineage, Quality monitoring, PII detection, Access controls, Audit logs, Policy automation",
        "pricing": "$3,000/month + $0.10 per GB cataloged",
        "sla": "99.9% uptime, 2-hour critical incident response",
        "compliance": "SOC 2, HIPAA, GDPR, CCPA, GLBA",
        "case_studies": "Bank data stewardship, Healthcare records management, Retail customer data compliance"
    }
]


# ============================================================================
# KNOWLEDGE BASE CLASS
# ============================================================================

class ProductKnowledgeBase:
    """Manages product information in Chroma vector database"""
    
    def __init__(self, db_path: str = "./chroma_db"):
        """Initialize knowledge base with Chroma
        
        Args:
            db_path: Path to persist Chroma database
        """
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name="product_knowledge",
            metadata={"hnsw:space": "cosine"}
        )
    
    def load_products(self, products_data: list[dict]) -> None:
        """Load product information into knowledge base
        
        Args:
            products_data: List of product dicts with keys:
                - id: unique identifier
                - name: product name
                - description: brief description
                - features: comma-separated features
                - pricing: pricing model
                - sla: SLA guarantees
                - compliance: compliance certifications
                - case_studies: relevant use cases
        """
        documents = []
        metadatas = []
        ids = []
        
        for product in products_data:
            # Create searchable document
            doc = f"""
            Product: {product['name']}
            Description: {product['description']}
            Features: {product['features']}
            Pricing: {product['pricing']}
            SLA: {product['sla']}
            Compliance: {product['compliance']}
            Use Cases: {product['case_studies']}
            """
            
            documents.append(doc)
            metadatas.append({
                "product_id": product['id'],
                "product_name": product['name'],
                "category": product.get('category', 'general')
            })
            ids.append(product['id'])
        
        # Upsert into Chroma
        self.collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"✅ Loaded {len(documents)} products into knowledge base")
    
    def search(self, query: str, n_results: int = 5) -> list[str]:
        """Search knowledge base for relevant products
        
        Args:
            query: Search query
            n_results: Number of results to return
        
        Returns:
            List of relevant product information
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return results['documents'][0] if results['documents'] else []


# ============================================================================
# AGENT CREATION FUNCTIONS
# ============================================================================

async def create_rfp_analyzer_agent(kb: ProductKnowledgeBase) -> Agent:
    """Create agent that analyzes RFP requirements"""
    
    if Agent is None or FoundryChatClient is None:
        raise ImportError("Agent Framework not installed. Run: pip install agent-framework")
    
    try:
        from azure.identity import AzureCliCredential
        client = FoundryChatClient(credential=AzureCliCredential())
    except:
        # Fallback to OpenAI
        from agent_framework.openai import OpenAIChatCompletionClient
        client = OpenAIChatCompletionClient(model="gpt-4.1")
    
    agent = Agent(
        client=client,
        name="RFPAnalyzer",
        instructions="""
You are an expert RFP (Request for Proposal) analyst. Your job is to:
1. Analyze the RFP document provided
2. Extract key requirements (technical, compliance, pricing, SLA)
3. Identify critical evaluation criteria
4. Suggest which products are the best fit

Format your analysis as JSON with sections:
- requirements: key technical/business requirements
- evaluation_criteria: what the customer will judge us on
- compliance_needs: regulatory requirements mentioned
- budget_range: estimated budget if mentioned
- recommended_products: which products fit best
- gaps: areas where we might need customization
"""
    )
    
    return agent


async def create_technical_agent() -> Agent:
    """Create agent for technical response sections"""
    
    if Agent is None or FoundryChatClient is None:
        raise ImportError("Agent Framework not installed")
    
    try:
        from azure.identity import AzureCliCredential
        client = FoundryChatClient(credential=AzureCliCredential())
    except:
        from agent_framework.openai import OpenAIChatCompletionClient
        client = OpenAIChatCompletionClient(model="gpt-4.1")
    
    agent = Agent(
        client=client,
        name="TechnicalLead",
        instructions="""
You are a technical architect. Write the TECHNICAL APPROACH section of an RFP response.
Include:
- System architecture diagram (as text)
- Technology stack and integration approach
- Implementation timeline
- Risk mitigation
- Performance and scalability guarantees
- Support and SLA commitments

Be specific, concrete, and reference the customer's requirements.
"""
    )
    
    return agent


async def create_pricing_agent() -> Agent:
    """Create agent for pricing section"""
    
    if Agent is None or FoundryChatClient is None:
        raise ImportError("Agent Framework not installed")
    
    try:
        from azure.identity import AzureCliCredential
        client = FoundryChatClient(credential=AzureCliCredential())
    except:
        from agent_framework.openai import OpenAIChatCompletionClient
        client = OpenAIChatCompletionClient(model="gpt-4.1")
    
    agent = Agent(
        client=client,
        name="PricingLead",
        instructions="""
You are a pricing specialist. Write the PRICING & COMMERCIAL TERMS section.
Include:
- Detailed pricing breakdown
- Volume discounts if applicable
- Implementation costs
- Support/maintenance costs
- Payment terms
- Cost comparison to industry benchmarks
- Value proposition (ROI)

Base pricing on the customer's stated budget and requirements.
"""
    )
    
    return agent


async def create_compliance_agent() -> Agent:
    """Create agent for compliance section"""
    
    if Agent is None or FoundryChatClient is None:
        raise ImportError("Agent Framework not installed")
    
    try:
        from azure.identity import AzureCliCredential
        client = FoundryChatClient(credential=AzureCliCredential())
    except:
        from agent_framework.openai import OpenAIChatCompletionClient
        client = OpenAIChatCompletionClient(model="gpt-4.1")
    
    agent = Agent(
        client=client,
        name="ComplianceLead",
        instructions="""
You are a compliance officer. Write the SECURITY & COMPLIANCE section.
Include:
- Certifications and attestations (SOC 2, ISO, HIPAA, GDPR, etc.)
- Data security measures
- Access controls and authentication
- Audit and logging capabilities
- Disaster recovery and business continuity
- Incident response procedures
- Sub-processor information if applicable

Address each compliance requirement mentioned in the RFP specifically.
"""
    )
    
    return agent


# ============================================================================
# RFP RESPONSE GENERATION
# ============================================================================

async def generate_rfp_response(
    rfp_text: str,
    kb: ProductKnowledgeBase,
    use_agents: bool = True
) -> dict:
    """Generate complete RFP response
    
    Args:
        rfp_text: Full RFP document text
        kb: ProductKnowledgeBase instance
        use_agents: If True, use multi-agent; else use single analyzer
    
    Returns:
        Dictionary with response sections
    """
    
    print("\n" + "="*70)
    print("🔍 ANALYZING RFP")
    print("="*70)
    
    # Step 1: Analyze RFP
    analyzer = await create_rfp_analyzer_agent(kb)
    analysis = await analyzer.run(f"Analyze this RFP:\n\n{rfp_text}")
    
    print(f"\n📋 Analysis:\n{analysis}\n")
    
    # Parse analysis
    try:
        analysis_json = json.loads(analysis)
    except:
        analysis_json = {"raw_analysis": analysis}
    
    # Step 2: Search knowledge base
    print("\n" + "="*70)
    print("🔍 SEARCHING PRODUCT KNOWLEDGE BASE")
    print("="*70)
    
    search_query = str(analysis_json.get("requirements", ""))[:200]
    relevant_products = kb.search(search_query, n_results=3)
    
    product_context = "\n\n".join(relevant_products)
    print(f"\n📚 Found relevant products:\n{product_context}\n")
    
    # Step 3: Generate response sections
    if use_agents:
        print("\n" + "="*70)
        print("✍️  GENERATING RESPONSE SECTIONS")
        print("="*70)
        
        tech_agent = await create_technical_agent()
        pricing_agent = await create_pricing_agent()
        compliance_agent = await create_compliance_agent()
        
        context = f"""
RFP Requirements: {analysis_json.get('requirements', '')}
Our Relevant Products: {product_context}
Customer Budget: {analysis_json.get('budget_range', 'Not specified')}
Compliance Needs: {analysis_json.get('compliance_needs', '')}
"""
        
        print("\n📝 Technical approach...")
        tech_response = await tech_agent.run(f"Write the technical section based on:\n{context}")
        
        print("💰 Pricing section...")
        pricing_response = await pricing_agent.run(f"Write the pricing section based on:\n{context}")
        
        print("🔒 Compliance section...")
        compliance_response = await compliance_agent.run(f"Write the compliance section based on:\n{context}")
        
        return {
            "status": "success",
            "analysis": analysis,
            "product_context": product_context,
            "sections": {
                "technical_approach": tech_response,
                "pricing": pricing_response,
                "compliance": compliance_response
            }
        }
    
    else:
        # Single analyzer generates all sections
        response_prompt = f"""
Based on the RFP analysis and our product knowledge, generate a complete RFP response with these sections:

1. EXECUTIVE SUMMARY
2. TECHNICAL APPROACH
3. PRICING & COMMERCIAL TERMS
4. SECURITY & COMPLIANCE
5. PROJECT TIMELINE
6. TEAM & EXPERIENCE

RFP: {rfp_text[:2000]}

Our Products: {product_context}

Analysis: {analysis}
"""
        
        analyzer = await create_rfp_analyzer_agent(kb)
        full_response = await analyzer.run(response_prompt)
        
        return {
            "status": "success",
            "response": full_response,
            "analysis": analysis,
            "product_context": product_context
        }
