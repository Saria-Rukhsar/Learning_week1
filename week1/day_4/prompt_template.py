from jinja2 import Template

# 1. Advance Template (Jis mai Loop aur If-Else dono hain)
# Note: {% ... %} logic ke liye hota hai, aur {{ ... }} variable print karne ke liye.
advance_prompt_template = """
You are an expert financial auditor. Your task is to clean this messy transaction data.

CRITICAL RULES:
- Format each transaction line properly.
- If an item costs more than $100, add a [⚠️ HIGH SPEND ALERT] tag next to it!

Here are the transactions to process:
{% for item in transactions %}
- Item: {{ item.name }} | Cost: ${{ item.price }} {% if item.price > 100 %}<- ⚠️ HIGH SPEND ALERT{% endif %}
{% endfor %}

Please return the cleaned data summary.
"""

# 2. Dynamic Data (Jo real-world mai database ya API se aata hai)
data_from_database = [
    {"name": "Pizza Delivery", "price": 20},
    {"name": "Office Desk Chairs", "price": 350},  # 100 se bara hai
    {"name": "GitHub Copilot Sub", "price": 10},
    {"name": "MacBook Pro Monitor", "price": 450}  # 100 se bara hai
]

# 3. Jinja2 Compile aur Render
template = Template(advance_prompt_template)
final_prompt = template.render(transactions=data_from_database)

print(final_prompt)