# =====================================================================
# USE CASE 1: EXTRACTION (Few-Shot Pattern)
# =====================================================================
extraction_prompt = [
    {
        "role": "system",
        "content": (
            "You are a financial data harvesting bot. Your only job is to extract the "
            "Product Name and Price from the text. Output format must be strictly a clean list.\n\n"
            "Examples:\n"
            "Input: 'I bought a brand new iPhone for 999 dollars yesterday.'\n"
            "Output: - Product: iPhone | Price: $999\n\n"
            "Input: 'The mechanical keyboard was on sale for 120 USD.'\n"
            "Output: - Product: mechanical keyboard | Price: $120"
        )
    },
    {
        "role": "user",
        "content": "Input: 'My office ordered 3 units of Dell Monitors and paid around 450 USD total.'"
    }
]

# =====================================================================
# USE CASE 2: CLASSIFICATION (Zero-Shot + Constraint Pattern)
# =====================================================================
classification_prompt = [
    {
        "role": "system",
        "content": (
            "You are an automated email routing system. Classify the incoming text into exactly "
            "ONE of the following categories:\n"
            "1. BILLING (payment issues, invoices, refunds)\n"
            "2. TECHNICAL (bugs, crashes, login failure)\n"
            "3. GENERAL (partnerships, feedback, hiring)\n\n"
            "CRITICAL RULES:\n"
            "- Reply with the category name in ALL CAPS only.\n"
            "- Do not provide explanation.\n"
            "- If uncertain, output 'UNCLASSIFIED'."
        )
    },
    {
        "role": "user",
        "content": "Hey, I was charged twice for my subscription this month. Can you check please?"
    }
]

# =====================================================================
# USE CASE 3: GENERATION (Chain-of-Thought Pattern)
# =====================================================================
generation_prompt = [
    {
        "role": "system",
        "content": (
            "You are a senior executive assistant. Your task is to draft follow-up emails "
            "for clients based on rough meeting notes.\n\n"
            "To write a great email, execute your thinking process in these steps:\n"
            "Step 1: Identify all action points discussed in the notes.\n"
            "Step 2: Note down any deadlines or timelines mentioned.\n"
            "Step 3: Draft the final email using a warm, professional corporate tone.\n\n"
            "Show your thinking process for Step 1 and Step 2 before writing the final email."
        )
    },
    {
        "role": "user",
        "content": (
            "Notes:\n"
            "- Met with Alex from Acme Corp.\n"
            "- They liked the logo design but wanted the color blue to be darker.\n"
            "- Promised to send the updated design by this Friday.\n"
            "- Next call scheduled for Monday morning."
        )
    }
]

# --- Testing Print to see our Python Object Structure ---
if __name__ == "__main__":
    import json
    print("--- Structure Ready for Classification API Call ---")
    print(json.dumps(classification_prompt, indent=2))