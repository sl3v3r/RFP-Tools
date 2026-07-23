#!/usr/bin/env python3
"""
Load Your Product Knowledge Base

This script helps you populate the RFP system with YOUR actual product data.
Supports multiple input formats:
- CSV files
- JSON files
- Manual entry via CLI
- Direct Python dictionaries
"""

import sys
import json
import csv
from pathlib import Path
from typing import list, dict
from argparse import ArgumentParser

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rfp_agent_system import ProductKnowledgeBase


# ============================================================================
# SAMPLE TEMPLATES
# ============================================================================

CSV_TEMPLATE = """id,name,category,description,features,pricing,sla,compliance,case_studies
prod_1,Product Name,category,Brief description,Feature1 Feature2 Feature3,Pricing details,99.9% uptime,SOC2 GDPR,Use case 1 Use case 2
"""

JSON_TEMPLATE = """[
  {
    "id": "prod_1",
    "name": "Your Product Name",
    "category": "category",
    "description": "Brief description",
    "features": "Feature1, Feature2, Feature3",
    "pricing": "Pricing details",
    "sla": "99.9% uptime",
    "compliance": "SOC 2, GDPR",
    "case_studies": "Use case 1, Use case 2"
  }
]
"""


# ============================================================================
# LOADER FUNCTIONS
# ============================================================================

def load_from_csv(csv_file: str) -> list[dict]:
    """Load products from CSV file
    
    Expected columns: id, name, category, description, features, pricing, sla, compliance, case_studies
    """
    products = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            product = {
                "id": row['id'].strip(),
                "name": row['name'].strip(),
                "category": row['category'].strip(),
                "description": row['description'].strip(),
                "features": row['features'].strip(),
                "pricing": row['pricing'].strip(),
                "sla": row['sla'].strip(),
                "compliance": row['compliance'].strip(),
                "case_studies": row['case_studies'].strip(),
            }
            products.append(product)
    
    return products


def load_from_json(json_file: str) -> list[dict]:
    """Load products from JSON file"""
    with open(json_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    # Validate structure
    required_fields = {'id', 'name', 'category', 'description', 'features', 
                       'pricing', 'sla', 'compliance', 'case_studies'}
    
    for product in products:
        missing = required_fields - set(product.keys())
        if missing:
            raise ValueError(f"Product {product.get('id', '?')} missing fields: {missing}")
    
    return products


def load_from_xlsx(xlsx_file: str) -> list[dict]:
    """Load products from Excel file"""
    try:
        import openpyxl
    except ImportError:
        print("❌ openpyxl not installed. Run: pip install openpyxl")
        sys.exit(1)
    
    products = []
    wb = openpyxl.load_workbook(xlsx_file)
    ws = wb.active
    
    # Get headers from first row
    headers = [cell.value for cell in ws[1]]
    
    # Load data rows
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:  # Skip empty rows
            continue
        
        product = dict(zip(headers, row))
        # Clean up None values
        product = {k: v for k, v in product.items() if v is not None}
        products.append(product)
    
    return products


def interactive_product_entry() -> list[dict]:
    """Interactively enter products via CLI"""
    products = []
    
    print("\n📝 Interactive Product Entry Mode")
    print("(Leave field blank to finish)\n")
    
    while True:
        print(f"\n--- Product {len(products) + 1} ---")
        
        product_id = input("Product ID (e.g., prod_analytics): ").strip()
        if not product_id:
            break
        
        name = input("Product Name: ").strip()
        if not name:
            print("❌ Product name is required")
            continue
        
        category = input("Category (e.g., analytics, ai_training): ").strip()
        description = input("Description (1-2 sentences): ").strip()
        features = input("Features (comma-separated): ").strip()
        pricing = input("Pricing Model: ").strip()
        sla = input("SLA Commitments: ").strip()
        compliance = input("Compliance (e.g., SOC2 GDPR): ").strip()
        case_studies = input("Use Cases/Case Studies: ").strip()
        
        product = {
            "id": product_id,
            "name": name,
            "category": category,
            "description": description,
            "features": features,
            "pricing": pricing,
            "sla": sla,
            "compliance": compliance,
            "case_studies": case_studies
        }
        
        products.append(product)
        print(f"✅ Added: {name}")
    
    return products


def validate_products(products: list[dict]) -> bool:
    """Validate product data"""
    required_fields = {'id', 'name', 'category', 'description', 'features', 
                       'pricing', 'sla', 'compliance', 'case_studies'}
    
    for i, product in enumerate(products):
        missing = required_fields - set(product.keys())
        if missing:
            print(f"❌ Product {i+1} ({product.get('name', '?')}) missing fields: {missing}")
            return False
        
        if not product.get('id') or not product.get('name'):
            print(f"❌ Product {i+1} must have id and name")
            return False
    
    return True


def preview_products(products: list[dict], limit: int = 3) -> None:
    """Show preview of products to be loaded"""
    print("\n" + "="*70)
    print("📋 PREVIEW OF PRODUCTS TO LOAD")
    print("="*70)
    
    for i, product in enumerate(products[:limit], 1):
        print(f"\n[{i}] {product['name']}")
        print(f"    Category: {product['category']}")
        print(f"    Description: {product['description'][:60]}...")
        print(f"    Features: {product['features'][:50]}...")
        print(f"    Pricing: {product['pricing']}")
        print(f"    Compliance: {product['compliance']}")
    
    if len(products) > limit:
        print(f"\n... and {len(products) - limit} more products")
    
    print(f"\n📊 Total: {len(products)} products")


def export_template(format_type: str, output_file: str) -> None:
    """Export template file for data entry"""
    if format_type == 'csv':
        template = CSV_TEMPLATE
    elif format_type == 'json':
        template = JSON_TEMPLATE
    else:
        print(f"❌ Unknown format: {format_type}")
        return
    
    with open(output_file, 'w') as f:
        f.write(template)
    
    print(f"✅ Template exported to: {output_file}")
    print(f"   Edit this file and run: python load_products.py --{format_type} {output_file}")


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main entry point"""
    
    parser = ArgumentParser(description="Load your product data into RFP knowledge base")
    
    parser.add_argument(
        "--csv",
        type=str,
        help="Load products from CSV file"
    )
    parser.add_argument(
        "--json",
        type=str,
        help="Load products from JSON file"
    )
    parser.add_argument(
        "--xlsx",
        type=str,
        help="Load products from Excel file"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Enter products interactively"
    )
    parser.add_argument(
        "--export-csv",
        type=str,
        help="Export CSV template"
    )
    parser.add_argument(
        "--export-json",
        type=str,
        help="Export JSON template"
    )
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append to existing knowledge base (don't replace)"
    )
    parser.add_argument(
        "--db-path",
        type=str,
        default="./chroma_db",
        help="Path to Chroma database (default: ./chroma_db)"
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show preview before loading"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("🚀 RFP PRODUCT DATA LOADER")
    print("="*70)
    
    # Export templates
    if args.export_csv:
        export_template('csv', args.export_csv)
        return
    
    if args.export_json:
        export_template('json', args.export_json)
        return
    
    # Load products
    products = None
    
    if args.csv:
        print(f"\n📂 Loading from CSV: {args.csv}")
        try:
            products = load_from_csv(args.csv)
            print(f"✅ Loaded {len(products)} products from CSV")
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            sys.exit(1)
    
    elif args.json:
        print(f"\n📂 Loading from JSON: {args.json}")
        try:
            products = load_from_json(args.json)
            print(f"✅ Loaded {len(products)} products from JSON")
        except Exception as e:
            print(f"❌ Error loading JSON: {e}")
            sys.exit(1)
    
    elif args.xlsx:
        print(f"\n📂 Loading from Excel: {args.xlsx}")
        try:
            products = load_from_xlsx(args.xlsx)
            print(f"✅ Loaded {len(products)} products from Excel")
        except Exception as e:
            print(f"❌ Error loading Excel: {e}")
            sys.exit(1)
    
    elif args.interactive:
        print()
        products = interactive_product_entry()
    
    else:
        parser.print_help()
        print("\n" + "="*70)
        print("QUICK START:")
        print("="*70)
        print("\n1. Export CSV template:")
        print("   python load_products.py --export-csv my_products.csv")
        print("\n2. Edit the CSV file with your products")
        print("\n3. Load products:")
        print("   python load_products.py --csv my_products.csv")
        print("\nOR enter interactively:")
        print("   python load_products.py --interactive")
        return
    
    if not products:
        print("❌ No products loaded")
        sys.exit(1)
    
    # Validate
    if not validate_products(products):
        sys.exit(1)
    
    # Preview
    preview_products(products)
    
    if args.preview:
        print("\n✅ Preview mode - no data loaded")
        return
    
    # Confirm
    confirm = input(f"\n❓ Load {len(products)} products into knowledge base? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled")
        return
    
    # Load into knowledge base
    print(f"\n🔄 Loading into knowledge base at: {args.db_path}")
    
    try:
        kb = ProductKnowledgeBase(db_path=args.db_path)
        kb.load_products(products)
        print(f"\n✅ Successfully loaded {len(products)} products!")
        
        # Test search
        print("\n🧪 Testing search functionality...")
        test_query = products[0]['name']
        results = kb.search(test_query, n_results=1)
        if results:
            print(f"✅ Search working - found: {results[0][:100]}...")
        
        print("\n✅ Your knowledge base is ready!")
        print("\nNext steps:")
        print("   python main.py --rfp examples/sample_rfp.txt")
        print("   python main.py --interactive")
        
    except Exception as e:
        print(f"❌ Error loading into knowledge base: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
