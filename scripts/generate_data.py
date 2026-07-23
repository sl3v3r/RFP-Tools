#!/usr/bin/env python3
"""
Product Data File Generator

Generate sample product data files in different formats:
- CSV
- JSON
- Excel (XLSX)
"""

import sys
import json
import csv
from pathlib import Path
from argparse import ArgumentParser


# ============================================================================
# SAMPLE DATA (Your Company Products)
# ============================================================================

SAMPLE_DATA = [
    {
        "id": "prod_analytics_pro",
        "name": "CloudAnalytics Pro",
        "category": "Analytics",
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
        "category": "AI Training",
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
        "category": "Data Governance",
        "description": "Centralized data governance, lineage tracking, and compliance monitoring",
        "features": "Data lineage, Quality monitoring, PII detection, Access controls, Audit logs, Policy automation",
        "pricing": "$3,000/month + $0.10 per GB cataloged",
        "sla": "99.9% uptime, 2-hour critical incident response",
        "compliance": "SOC 2, HIPAA, GDPR, CCPA, GLBA",
        "case_studies": "Bank data stewardship, Healthcare records management, Retail customer data compliance"
    },
    {
        "id": "prod_security_suite",
        "name": "SecurityGuard Suite",
        "category": "Security",
        "description": "Comprehensive cloud security monitoring and threat detection",
        "features": "Threat detection, Incident response, Vulnerability scanning, Compliance reporting, DLP",
        "pricing": "$2,000/month + $1 per 1000 events",
        "sla": "99.9% uptime, 1-hour response for critical alerts",
        "compliance": "SOC 2, ISO 27001, PCI-DSS, FedRAMP",
        "case_studies": "Enterprise IT security operations, Financial services threat detection, Healthcare incident response"
    },
    {
        "id": "prod_data_pipeline",
        "name": "DataPipeline Flow",
        "category": "Data Integration",
        "description": "Serverless data integration and ETL platform",
        "features": "Visual flow builder, 100+ connectors, Error handling, Scheduling, Monitoring",
        "pricing": "$500/month + $0.05 per 1000 rows processed",
        "sla": "99.9% uptime, 4-hour support response",
        "compliance": "SOC 2, GDPR, HIPAA",
        "case_studies": "Real-time data warehousing, Log aggregation, Customer data synchronization"
    }
]


# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def export_csv(products: list[dict], output_file: str) -> None:
    """Export products to CSV"""
    if not products:
        print("❌ No products to export")
        return
    
    fieldnames = list(products[0].keys())
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)
    
    print(f"✅ Exported {len(products)} products to: {output_file}")


def export_json(products: list[dict], output_file: str, pretty: bool = True) -> None:
    """Export products to JSON"""
    if not products:
        print("❌ No products to export")
        return
    
    with open(output_file, 'w', encoding='utf-8') as f:
        if pretty:
            json.dump(products, f, indent=2, ensure_ascii=False)
        else:
            json.dump(products, f, ensure_ascii=False)
    
    print(f"✅ Exported {len(products)} products to: {output_file}")


def export_xlsx(products: list[dict], output_file: str) -> None:
    """Export products to Excel"""
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment
    except ImportError:
        print("❌ openpyxl not installed. Run: pip install openpyxl")
        return
    
    if not products:
        print("❌ No products to export")
        return
    
    # Create workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Products"
    
    # Get fieldnames
    fieldnames = list(products[0].keys())
    
    # Write headers
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    
    for col, field in enumerate(fieldnames, 1):
        cell = ws.cell(row=1, column=col)
        cell.value = field
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    
    # Write data
    for row, product in enumerate(products, 2):
        for col, field in enumerate(fieldnames, 1):
            cell = ws.cell(row=row, column=col)
            cell.value = product.get(field, "")
            cell.alignment = Alignment(vertical="top", wrap_text=True)
    
    # Adjust column widths
    ws.column_dimensions['A'].width = 20
    for col in range(2, len(fieldnames) + 1):
        ws.column_dimensions[chr(64 + col)].width = 25
    
    # Set row heights
    ws.row_dimensions[1].height = 30
    for row in range(2, len(products) + 2):
        ws.row_dimensions[row].height = 40
    
    # Save
    wb.save(output_file)
    print(f"✅ Exported {len(products)} products to: {output_file}")


def export_markdown(products: list[dict], output_file: str) -> None:
    """Export products as Markdown table"""
    if not products:
        print("❌ No products to export")
        return
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Product Catalog\n\n")
        
        for product in products:
            f.write(f"## {product['name']}\n\n")
            f.write(f"**ID:** {product['id']}\n\n")
            f.write(f"**Category:** {product['category']}\n\n")
            f.write(f"**Description:** {product['description']}\n\n")
            f.write(f"**Features:** {product['features']}\n\n")
            f.write(f"**Pricing:** {product['pricing']}\n\n")
            f.write(f"**SLA:** {product['sla']}\n\n")
            f.write(f"**Compliance:** {product['compliance']}\n\n")
            f.write(f"**Case Studies:** {product['case_studies']}\n\n")
            f.write("---\n\n")
    
    print(f"✅ Exported {len(products)} products to: {output_file}")


def export_template(format_type: str, output_file: str) -> None:
    """Export blank template for data entry"""
    if format_type == 'csv':
        template = "id,name,category,description,features,pricing,sla,compliance,case_studies\nprod_1,My Product,Category,Description,Feature1,Pricing,SLA,Compliance,Use case"
        with open(output_file, 'w') as f:
            f.write(template)
    
    elif format_type == 'json':
        template = [
            {
                "id": "prod_1",
                "name": "My Product",
                "category": "Category",
                "description": "Description",
                "features": "Feature1, Feature2",
                "pricing": "Pricing",
                "sla": "SLA",
                "compliance": "Compliance",
                "case_studies": "Use case"
            }
        ]
        with open(output_file, 'w') as f:
            json.dump(template, f, indent=2)
    
    print(f"✅ Template exported to: {output_file}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point"""
    
    parser = ArgumentParser(description="Generate product data files")
    
    parser.add_argument(
        "--csv",
        type=str,
        help="Export to CSV file"
    )
    parser.add_argument(
        "--json",
        type=str,
        help="Export to JSON file"
    )
    parser.add_argument(
        "--xlsx",
        type=str,
        help="Export to Excel file"
    )
    parser.add_argument(
        "--markdown",
        type=str,
        help="Export to Markdown file"
    )
    parser.add_argument(
        "--template-csv",
        type=str,
        help="Export blank CSV template"
    )
    parser.add_argument(
        "--template-json",
        type=str,
        help="Export blank JSON template"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Export to all formats (in 'output' directory)"
    )
    parser.add_argument(
        "--custom-data",
        type=str,
        help="Load custom products from JSON file"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("📊 PRODUCT DATA FILE GENERATOR")
    print("="*70 + "\n")
    
    # Load data
    products = SAMPLE_DATA
    
    if args.custom_data:
        print(f"Loading custom data from: {args.custom_data}")
        try:
            with open(args.custom_data) as f:
                products = json.load(f)
            print(f"✅ Loaded {len(products)} custom products")
        except Exception as e:
            print(f"❌ Error loading custom data: {e}")
            sys.exit(1)
    else:
        print(f"Using sample data ({len(products)} products)")
    
    # Export
    if args.csv:
        export_csv(products, args.csv)
    
    if args.json:
        export_json(products, args.json)
    
    if args.xlsx:
        export_xlsx(products, args.xlsx)
    
    if args.markdown:
        export_markdown(products, args.markdown)
    
    if args.template_csv:
        export_template('csv', args.template_csv)
    
    if args.template_json:
        export_template('json', args.template_json)
    
    if args.all:
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        export_csv(products, output_dir / "products.csv")
        export_json(products, output_dir / "products.json")
        try:
            export_xlsx(products, output_dir / "products.xlsx")
        except:
            pass
        export_markdown(products, output_dir / "products.md")
        
        print(f"\n✅ All exports saved to: {output_dir}/")
    
    if not any([args.csv, args.json, args.xlsx, args.markdown, 
                args.template_csv, args.template_json, args.all]):
        parser.print_help()
        print("\nEXAMPLES:")
        print("\n1. Export sample data to CSV:")
        print("   python generate_data.py --csv products.csv")
        print("\n2. Export sample data to Excel:")
        print("   python generate_data.py --xlsx products.xlsx")
        print("\n3. Export all formats:")
        print("   python generate_data.py --all")
        print("\n4. Export blank template:")
        print("   python generate_data.py --template-csv my_template.csv")
        print("\n5. Use custom products:")
        print("   python generate_data.py --custom-data my_products.json --csv output.csv")


if __name__ == "__main__":
    main()
