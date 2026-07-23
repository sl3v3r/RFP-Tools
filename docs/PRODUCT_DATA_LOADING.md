# Product Data Loading Guide

## Overview

This guide helps you load your actual product information into the RFP system's knowledge base.

## Quick Start (2 minutes)

### Option 1: Generate Sample Data

```bash
python scripts/generate_data.py --all
ls output/
```

You'll get:
- `products.csv` - Spreadsheet format
- `products.json` - JSON format
- `products.xlsx` - Excel format
- `products.md` - Documentation

### Option 2: Edit and Load

```bash
# Generate CSV template
python scripts/generate_data.py --template-csv my_products.csv

# Edit in Excel/Google Sheets
# (Then load it)
python scripts/load_products.py --csv my_products.csv
```

### Option 3: Interactive Entry

```bash
python scripts/load_products.py --interactive
```

You'll be prompted to enter each product field one at a time.

---

## Data Format

### Required Fields

Every product needs these fields:

| Field | Example | Notes |
|-------|---------|-------|
| `id` | `prod_analytics_pro` | Unique identifier, no spaces |
| `name` | `CloudAnalytics Pro` | Display name (appears in RFP responses) |
| `category` | `analytics` | Product category |
| `description` | `Enterprise-grade real-time analytics` | 1-2 sentence overview |
| `features` | `Real-time dashboards, API access, ML integrations` | Comma-separated list |
| `pricing` | `$5,000/month + usage` | Pricing model |
| `sla` | `99.99% uptime, 15-min response` | Service level commitments |
| `compliance` | `SOC 2, HIPAA, GDPR` | Certifications and standards |
| `case_studies` | `Fortune 500 financial services, Healthcare` | Use cases and customer types |

---

## Input Methods

### Method 1: CSV File

**Advantages:**
- Edit in Excel/Google Sheets
- Easy to maintain
- Share with team

**Steps:**

```bash
# 1. Generate template
python scripts/generate_data.py --template-csv products.csv

# 2. Open and edit
open products.csv  # Mac
# or: start products.csv  # Windows
# or: xdg-open products.csv  # Linux

# 3. Load into knowledge base
python scripts/load_products.py --csv products.csv
```

**CSV Example:**
```csv
id,name,category,description,features,pricing,sla,compliance,case_studies
prod_analytics,CloudAnalytics,analytics,Enterprise analytics platform,Real-time dashboards,"$5,000/month",99.99% uptime,SOC2,Financial services
prod_ai,AI Suite,ai_training,ML platform,AutoML,"$10,000/month",99.95% uptime,ISO27001,Healthcare
```

### Method 2: JSON File

**Advantages:**
- Programmatically generate
- Version control friendly
- API integration ready

**Steps:**

```bash
# 1. Generate template
python scripts/generate_data.py --template-json products.json

# 2. Edit JSON
# (Edit in your code editor)

# 3. Load
python scripts/load_products.py --json products.json
```

**JSON Example:**
```json
[
  {
    "id": "prod_analytics",
    "name": "CloudAnalytics",
    "category": "analytics",
    "description": "Enterprise analytics platform",
    "features": "Real-time dashboards, API access",
    "pricing": "$5,000/month",
    "sla": "99.99% uptime",
    "compliance": "SOC 2, HIPAA",
    "case_studies": "Financial services, Healthcare"
  }
]
```

### Method 3: Excel File

**Advantages:**
- Most user-friendly
- Visual data entry
- Easy to share

**Steps:**

```bash
# 1. Generate sample Excel
python scripts/generate_data.py --xlsx products.xlsx

# 2. Open and edit
open products.xlsx

# 3. Load
python scripts/load_products.py --xlsx products.xlsx
```

### Method 4: Interactive CLI

**Advantages:**
- No files needed
- Interactive validation
- Quick entry

**Steps:**

```bash
python scripts/load_products.py --interactive
```

You'll see prompts like:
```
Product ID (e.g., prod_analytics): prod_1
Product Name: My Product
Category (e.g., analytics, ai_training): analytics
Description (1-2 sentences): My awesome product
...
```

---

## Workflow Examples

### Example 1: Starting Fresh

```bash
# Create CSV template
python scripts/generate_data.py --template-csv my_products.csv

# Edit in Excel
# (Add your products)

# Load
python scripts/load_products.py --csv my_products.csv

# Test
python main.py --test
```

### Example 2: Using Existing Spreadsheet

If you already have product data in Excel:

1. Export as CSV from Excel
2. Rename columns to match (id, name, category, etc.)
3. Load:
   ```bash
   python scripts/load_products.py --csv your_spreadsheet.csv
   ```

### Example 3: Generate from Existing Data

If you have products in JSON format:

```bash
# Convert to other formats
python scripts/generate_data.py --custom-data my_products.json --csv output.csv
python scripts/generate_data.py --custom-data my_products.json --xlsx output.xlsx
```

### Example 4: Team Workflow

```bash
# Team lead generates template
python scripts/generate_data.py --template-csv products_template.csv

# Team fills in data
# (Edit in Excel/Google Sheets)

# Tech lead loads into system
python scripts/load_products.py --csv products_filled.csv

# Test with sample RFP
python main.py --test
```

---

## Best Practices

### 1. Product IDs
- Use lowercase with underscores: `prod_analytics_pro`
- Make them meaningful
- Keep them unique

### 2. Descriptions
- 1-2 sentences max
- Include key value proposition
- Avoid marketing fluff

### 3. Features
- Comma-separated list
- 5-10 features per product
- Technical + business features

### 4. Pricing
- Include units ($/month, per GB, etc.)
- Note minimums/contracts if applicable
- Be specific

### 5. Compliance
- List all certifications
- Include relevant standards
- Update when new certs achieved

### 6. Case Studies
- Include industry verticals
- Mention customer types
- Note specific use cases

---

## Troubleshooting

### "Product missing fields"
**Fix:** Ensure all required fields are present. Run:
```bash
python scripts/load_products.py --csv products.csv --preview
```

### "CSV not loading"
**Fix:** Check that:
- File exists and is readable
- Columns match required fields
- No special characters in product IDs

### "Excel file won't export"
**Fix:** Install openpyxl:
```bash
pip install openpyxl
```

### "Search not finding products"
**Fix:** Verify products loaded:
```bash
python scripts/load_products.py --csv products.csv --preview
```

---

## Maintenance

### Updating Products

To update product information:

```bash
# 1. Export current data
python scripts/load_products.py --csv current_products.csv

# 2. Edit the CSV
# (Update in Excel)

# 3. Reload
python scripts/load_products.py --csv updated_products.csv
```

### Backup

Always keep backups of your product data:

```bash
# Backup to multiple formats
python scripts/generate_data.py --custom-data products.json --all
cp -r output backups/backup_$(date +%Y%m%d)/
```

### Versioning

Keep product data in version control:

```bash
git add products.json
git commit -m "Update product data"
git push
```

---

## Integration with CI/CD

Automate product data loading:

```bash
#!/bin/bash
# Load products automatically during deployment
python scripts/load_products.py --json products.json
python main.py --test
```

---

## API Integration

Generate product data from your APIs:

```python
import requests
import json

# Fetch from your API
response = requests.get("https://api.example.com/products")
products = response.json()

# Save to JSON
with open("products.json", "w") as f:
    json.dump(products, f, indent=2)

# Load into RFP system
# python scripts/load_products.py --json products.json
```

---

## Support

For issues or questions:
1. Check the examples in `examples/` directory
2. Review sample files in `output/` (after running generate_data.py)
3. Run with `--preview` flag to validate before loading
