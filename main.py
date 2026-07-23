#!/usr/bin/env python3
"""
RFP Response Agent System - Main Entry Point
Analyzes RFP documents and generates response drafts using product knowledge base.
"""

import asyncio
import json
from pathlib import Path
from argparse import ArgumentParser
import sys

try:
    from rfp_agent_system import (
        ProductKnowledgeBase,
        generate_rfp_response,
        SAMPLE_PRODUCTS
    )
except ImportError as e:
    print(f"❌ Error importing rfp_agent_system: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)


async def main():
    """Main entry point for RFP Agent System"""
    
    parser = ArgumentParser(
        description="RFP Response Agent System - AI-powered RFP analysis and response generation"
    )
    parser.add_argument(
        "--rfp",
        type=str,
        help="Path to RFP document file"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive mode - paste RFP directly"
    )
    parser.add_argument(
        "--single-agent",
        action="store_true",
        help="Use single analyzer instead of multi-agent orchestration"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="rfp_response.json",
        help="Output file path (default: rfp_response.json)"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test with sample RFP"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("🚀 RFP RESPONSE AGENT SYSTEM")
    print("="*70)
    print()
    
    # Initialize knowledge base
    print("📚 Initializing knowledge base...")
    kb = ProductKnowledgeBase(db_path="./chroma_db")
    kb.load_products(SAMPLE_PRODUCTS)
    print(f"✅ Knowledge base ready ({len(SAMPLE_PRODUCTS)} products)\n")
    
    # Process RFP
    if args.test or (not args.rfp and not args.interactive):
        # Test mode with sample RFP
        print("🧪 Running test with sample RFP...\n")
        
        sample_rfp = Path("examples/sample_rfp.txt")
        if sample_rfp.exists():
            with open(sample_rfp) as f:
                rfp_text = f.read()
        else:
            # Use inline sample
            rfp_text = """# REQUEST FOR PROPOSAL - Analytics Platform

## Organization Overview
TechCorp Inc. is a mid-sized financial services company with 500 employees.
We need a cloud-based analytics platform to handle customer transaction data.

## Requirements

### Technical Requirements
- Real-time data ingestion (10GB/day)
- Dashboard refresh every 5 minutes
- Support for 100+ concurrent users
- REST API for integration with legacy systems

### Compliance Requirements
- SOC 2 Type II certification
- GDPR compliance
- Encryption at rest and in transit

### Budget
- $150,000-200,000 per year
"""
        
        response = await generate_rfp_response(
            rfp_text,
            kb,
            use_agents=not args.single_agent
        )
        
        # Save response
        with open(args.output, "w") as f:
            json.dump(response, f, indent=2)
        
        print(f"\n✅ Response saved to {args.output}")
        print("\n" + "="*70)
        print("📄 SAMPLE RESPONSE")
        print("="*70)
        print(json.dumps(response, indent=2)[:1500] + "...\n")
        
    elif args.rfp:
        # Load RFP from file
        rfp_path = Path(args.rfp)
        
        if not rfp_path.exists():
            print(f"❌ Error: RFP file not found: {args.rfp}")
            sys.exit(1)
        
        print(f"📄 Loading RFP from: {args.rfp}")
        with open(rfp_path) as f:
            rfp_text = f.read()
        
        print(f"📊 RFP size: {len(rfp_text)} characters\n")
        
        response = await generate_rfp_response(
            rfp_text,
            kb,
            use_agents=not args.single_agent
        )
        
        # Save response
        with open(args.output, "w") as f:
            json.dump(response, f, indent=2)
        
        print(f"\n✅ Response saved to {args.output}")
        print(json.dumps(response, indent=2)[:1500] + "...\n")
        
    elif args.interactive:
        # Interactive mode
        print("🎯 INTERACTIVE MODE")
        print("Paste your RFP document (Ctrl+D on Mac/Linux, Ctrl+Z on Windows to finish):\n")
        
        rfp_lines = []
        try:
            while True:
                line = input()
                rfp_lines.append(line)
        except EOFError:
            pass
        
        rfp_text = "\n".join(rfp_lines)
        
        if not rfp_text.strip():
            print("\n❌ No RFP provided")
            sys.exit(1)
        
        print(f"\n📊 RFP size: {len(rfp_text)} characters\n")
        
        response = await generate_rfp_response(
            rfp_text,
            kb,
            use_agents=not args.single_agent
        )
        
        # Save response
        with open(args.output, "w") as f:
            json.dump(response, f, indent=2)
        
        print(f"\n✅ Response saved to {args.output}")
        print("\n" + "="*70)
        print("📄 GENERATED RESPONSE")
        print("="*70)
        print(json.dumps(response, indent=2))
    
    else:
        parser.print_help()
        print("\n" + "="*70)
        print("EXAMPLES:")
        print("="*70)
        print("# Analyze RFP from file")
        print("python main.py --rfp path/to/rfp.txt")
        print()
        print("# Interactive mode")
        print("python main.py --interactive")
        print()
        print("# Test with sample RFP")
        print("python main.py --test")
        print()
        print("# Use single analyzer instead of multi-agent")
        print("python main.py --rfp path/to/rfp.txt --single-agent")
        print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
