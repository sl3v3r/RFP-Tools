#!/usr/bin/env python3
"""
Initialize and load product knowledge base
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rfp_agent_system import ProductKnowledgeBase, SAMPLE_PRODUCTS


def main():
    """Load sample products into knowledge base"""
    
    print("🚀 Initializing Product Knowledge Base...\n")
    
    # Create knowledge base
    kb = ProductKnowledgeBase(db_path="./chroma_db")
    
    # Load sample products
    print(f"📦 Loading {len(SAMPLE_PRODUCTS)} products...")
    kb.load_products(SAMPLE_PRODUCTS)
    
    # Test search
    print("\n🔍 Testing knowledge base search...")
    results = kb.search("analytics solutions", n_results=2)
    
    print(f"\nFound {len(results)} results for 'analytics solutions':")
    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(result[:200] + "...")
    
    print("\n✅ Knowledge base initialized successfully!")
    print("\nYou can now run: python main.py --rfp examples/sample_rfp.txt")


if __name__ == "__main__":
    main()
