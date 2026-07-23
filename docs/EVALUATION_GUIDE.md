# Response Quality Evaluation Guide

## Overview

The RFP system includes comprehensive evaluation tools to measure the quality of generated responses. Use these to:

✅ Score response quality (0-100)
✅ Identify strengths and weaknesses
✅ Get improvement suggestions
✅ Compare multiple responses
✅ Track performance over time

---

## Quick Start

### Evaluate Single Response

```bash
python scripts/evaluate_response.py \
  --rfp examples/sample_rfp.txt \
  --response rfp_response.json
```

**Output:**
```
🎯 OVERALL SCORE
Score: 78.5/100
Recommendation: Good

📈 SCORE BREAKDOWN
Completeness ████████░░ 80/100 (weight: 15%)
Relevance   █████████░ 85/100 (weight: 25%)
Compliance  ███████░░░ 70/100 (weight: 20%)
Clarity     █████████░ 82/100 (weight: 15%)
Pricing     ██████████ 75/100 (weight: 25%)
```

### Batch Evaluate Multiple Responses

```bash
python scripts/batch_evaluate.py \
  --rfp-dir ./rfps \
  --response-dir ./responses \
  --output-dir ./evaluation_results
```

---

## Evaluation Metrics

### 1. Completeness (15% weight)

**What it measures:** Are all required sections present in the response?

**Checks for:**
- Executive summary
- Technical approach
- Pricing
- Compliance
- Implementation timeline
- Team/Experience
- Support/SLA
- And more

**Score interpretation:**
- ≥80: Covers all major sections
- 60-79: Missing some sections
- <60: Significant gaps

### 2. Relevance (25% weight - Most Important)

**What it measures:** How well does the response address customer requirements?

**Checks for:**
- Key requirements from RFP
- Technical specifications
- Business requirements
- Timeline requirements
- Specific needs mentioned

**Score interpretation:**
- ≥80: Highly relevant, addresses all major needs
- 60-79: Addresses most needs
- <60: Limited relevance to RFP

### 3. Compliance (20% weight)

**What it measures:** Does response address compliance/security requirements?

**Checks for:**
- SOC 2, HIPAA, GDPR, etc.
- Security measures
- Audit capabilities
- Compliance certifications
- Data protection details

**Score interpretation:**
- ≥80: Comprehensive compliance coverage
- 60-79: Adequate compliance discussion
- <60: Insufficient compliance detail

### 4. Clarity (15% weight)

**What it measures:** Is the response well-structured and easy to understand?

**Checks for:**
- Headings and structure
- Use of lists and bullet points
- Paragraph formatting
- Reasonable length (200-5000 words)
- Professional presentation

**Score interpretation:**
- ≥80: Well-organized, easy to follow
- 60-79: Adequate structure
- <60: Poor organization or too brief/verbose

### 5. Pricing (25% weight - Also Important)

**What it measures:** Does response include appropriate pricing information?

**Checks for:**
- Pricing section
- Specific dollar amounts
- Payment terms
- Volume discounts
- Implementation costs
- Support costs

**Score interpretation:**
- ≥80: Detailed pricing with all components
- 60-79: Basic pricing information
- <60: Missing or vague pricing

---

## Overall Score Interpretation

| Score | Recommendation | Action |
|-------|---|---|
| 85-100 | **Excellent** | Ready to submit (minor polish) |
| 70-84 | **Good** | Review suggested improvements |
| 60-69 | **Acceptable** | Significant improvements needed |
| <60 | **Needs Improvement** | Major revisions required |

---

## Usage Examples

### Example 1: Quick Evaluation

```bash
python scripts/evaluate_response.py \
  --rfp rfps/customer_rfp.txt \
  --response responses/our_response.txt
```

### Example 2: Save JSON Report

```bash
python scripts/evaluate_response.py \
  --rfp rfps/customer_rfp.txt \
  --response responses/our_response.txt \
  --output evaluation_report.json
```

### Example 3: JSON Format Only

```bash
python scripts/evaluate_response.py \
  --rfp rfps/customer_rfp.txt \
  --response responses/our_response.txt \
  --format json \
  --output report.json
```

### Example 4: Batch Evaluation

```bash
# Setup directories
mkdir -p rfps responses evaluation_results

# Put RFP files in rfps/
# Put response files in responses/

# Run batch evaluation
python scripts/batch_evaluate.py \
  --rfp-dir ./rfps \
  --response-dir ./responses \
  --output-dir ./evaluation_results
```

### Example 5: Evaluate JSON Response

When response is in JSON format (from `main.py`):

```bash
python scripts/evaluate_response.py \
  --rfp examples/sample_rfp.txt \
  --response rfp_response.json
```

---

## Improving Your Scores

### If Completeness is Low

✓ Add missing sections:
- Executive Summary - brief overview
- Timeline - implementation schedule
- Team - key personnel bios
- Support - support model details

### If Relevance is Low

✓ Explicitly address RFP requirements:
- Reference specific requirements from RFP
- Map your features to their needs
- Use their terminology
- Show you understand their business

### If Compliance is Low

✓ Highlight security and compliance:
- List all certifications (SOC 2, HIPAA, etc.)
- Describe security measures
- Discuss audit/compliance capabilities
- Address specific compliance needs from RFP

### If Clarity is Low

✓ Improve organization:
- Use clear headings
- Break into logical sections
- Use bullet points for lists
- Keep paragraphs focused and concise
- Maintain 200-3000 word range

### If Pricing is Low

✓ Add pricing details:
- Include pricing section
- Specify costs ($X/month, etc.)
- Describe payment terms
- Mention implementation costs
- Note any discounts or volume pricing

---

## Output Files

### Single Evaluation

**Console Output:**
```
📊 RFP RESPONSE EVALUATION REPORT
Score: 78.5/100
Recommendation: Good
[Detailed breakdown by section]
[Strengths, weaknesses, improvements]
```

**JSON Report (`--output report.json`):**
```json
{
  "timestamp": "2024-07-23T17:30:00",
  "overall": {
    "score": 78.5,
    "recommendation": "Good"
  },
  "sections": {
    "completeness": {"score": 80, "feedback": [...]},
    "relevance": {"score": 85, "feedback": [...]},
    ...
  },
  "analysis": {
    "strengths": [...],
    "weaknesses": [...],
    "improvements": [...]
  }
}
```

### Batch Evaluation

**Summary Report:**
```
Total Evaluated: 5
Average Score: 72.3/100
Score Range: 58.0 - 85.5

Excellent (≥85): 1 (20%)
Good (70-84):    3 (60%)
Acceptable:      1 (20%)
Needs Improve:   0 (0%)
```

**Detailed Results:**
- `evaluation_results/evaluation_response1.json`
- `evaluation_results/evaluation_response2.json`
- `evaluation_results/batch_evaluation_report.json`

---

## Workflow Integration

### Step 1: Generate Response

```bash
python main.py --rfp customer_rfp.txt
```

Output: `rfp_response.json`

### Step 2: Evaluate

```bash
python scripts/evaluate_response.py \
  --rfp customer_rfp.txt \
  --response rfp_response.json
```

### Step 3: Review Results

If score ≥70:
- Minor refinements only
- Ready to submit

If score 60-69:
- Address weaknesses
- Regenerate response
- Re-evaluate

If score <60:
- Major revision needed
- Check product knowledge base
- Update RFP input
- Regenerate and re-evaluate

---

## Best Practices

### 1. Regular Evaluation

- Evaluate every generated response
- Track scores over time
- Identify patterns
- Improve system prompts based on trends

### 2. Threshold Setting

- Set minimum score (e.g., 70) before submission
- Escalate low scores for human review
- Celebrate high scores (≥85)

### 3. Improvement Loop

```
Generate → Evaluate → Review → Improve → Regenerate
```

### 4. Batch Testing

- Test with multiple RFPs
- Compare scores
- Identify weak areas
- Focus improvements on consistency

---

## Troubleshooting

### "Files not found"

Ensure paths are correct:
```bash
ls examples/sample_rfp.txt  # Check RFP exists
ls rfp_response.json         # Check response exists
```

### "Low scores across board"

- Check product knowledge base is loaded
- Review RFP quality
- Test with sample RFP first
- Check system prompts in rfp_agent_system.py

### "JSON response parsing failed"

If response is JSON, script auto-extracts text. If not working:
```bash
# Convert JSON to text first
python -c "import json; data=json.load(open('response.json')); print(data['response'] if 'response' in data else data['sections'])"
```

---

## Advanced: Custom Scoring

To modify weights or add custom metrics, edit `ResponseEvaluator` in `scripts/evaluate_response.py`:

```python
# Adjust weights (must sum to 1.0)
completeness.weight = 0.20  # Increase from 0.15
relevance.weight = 0.30     # Increase from 0.25
pricing.weight = 0.20       # Decrease from 0.25

# Add custom criteria
def _score_customer_focus(self, response_text: str) -> SectionScore:
    # Your custom scoring logic
    ...
```

Then integrate into overall score calculation.

---

## Support

For evaluation questions:
1. Check example outputs in `evaluation_results/`
2. Review metric definitions above
3. Test with `examples/sample_rfp.txt`
4. Check GitHub issues for similar problems
