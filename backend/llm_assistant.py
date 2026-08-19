"""
AI Plant Assistant Chatbot Service (LLM Integration with Gemini & General Crop Expert System)
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fruit_diseases_db import FRUIT_DISEASE_DB


# System Prompt for General Crop Agricultural AI Assistant
SYSTEM_PROMPT = """
You are 'AgriDoctor AI', an expert Agricultural & Plant Pathology Assistant specialized in Crop Disease Detection across a wide range of crops including Wheat, Rice, Corn/Maize, Tomato, Potato, Cotton, Soybean, Apple, Grape, and more.
Your task is to provide concise, accurate, actionable advice to farmers, growers, and Computer Science & Engineering (CSE) students studying agricultural AI.

Guidelines:
1. Explain symptoms, fungal/bacterial pathogens, organic remedies, chemical treatments, and cultural practices clearly.
2. Structure answers using clean Markdown with bullet points or numbered lists.
3. Recommend organic and environmentally friendly IPM (Integrated Pest Management) practices first before chemical sprays.
4. Keep answers friendly, professional, and directly relevant to the user's question.
"""

def generate_chat_response(prompt: str, disease_context: dict = None, conversation_history: list = None) -> str:
    """
    Generate an AI assistant response using Gemini API or fruit crop domain knowledge engine.
    """
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    context_str = ""
    if disease_context and "display_name" in disease_context:
        context_str = f"\nCurrent Active Diagnosis Context: {disease_context.get('display_name')} on {disease_context.get('crop_type')} (Status: {disease_context.get('status')}, Severity: {disease_context.get('severity')})."

    # Attempt Gemini API call if API Key is configured
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            full_prompt = f"{SYSTEM_PROMPT}\n{context_str}\nUser Question: {prompt}"
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt
            )
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"[Gemini LLM] API call notice: {e}. Falling back to fruit expert knowledge engine.")

    # Fallback Fruit Crop Domain Knowledge Engine
    return domain_expert_fallback(prompt, disease_context)


def domain_expert_fallback(prompt: str, context: dict = None) -> str:
    """Intelligent fallback responder covering common fruit crop questions."""
    p_lower = prompt.lower()

    # 1. Wheat Rust Questions
    if "wheat" in p_lower or "rust" in p_lower:
        return """### 🌾 Wheat Rust Management Guide

**Cause**: Fungal pathogens *Puccinia triticina* (Leaf Rust), *P. striiformis* (Yellow Rust), *P. graminis* (Stem Rust).

**Organic & Cultural Control**:
- **Resistant Varieties**: Plant certified rust-resistant wheat varieties as first line of defense.
- **Crop Rotation**: Avoid consecutive wheat seasons; rotate with legumes or non-host crops.
- **Early Planting**: Adjust sowing dates to avoid peak rust-infection periods in your region.
- **Biological Control**: Apply *Bacillus subtilis*-based biocontrol agents at early infection stages.

**Chemical Options**:
- Propiconazole (Tilt 25 EC) or Tebuconazole at visible pustule formation.
- Mancozeb as protective spray before disease onset.

*Tip: Scout fields weekly during grain-fill stage for early pustule detection.*"""

    # 2. Corn Blight / Maize Disease
    if "corn" in p_lower or "maize" in p_lower or "blight" in p_lower:
        return """### 🌽 Corn / Maize Disease Management

**Common Diseases**: Northern Corn Leaf Blight (*Exserohilum turcicum*), Gray Leaf Spot, Smut.

**Key Preventive Steps**:
1. **Hybrid Selection**: Choose blight-tolerant maize hybrids certified for your agro-climatic zone.
2. **Crop Rotation**: Rotate with soybeans or legumes to break the disease cycle.
3. **Residue Management**: Deep-plow infected crop residues after harvest to reduce inoculum.

**Recommended Treatments**:
- **Organic**: Copper-based sprays or *Trichoderma viride* bio-fungicide applications.
- **Conventional**: Azoxystrobin + Propiconazole at VT-R1 growth stage for leaf blight protection."""

    # 3. Treatment / Fungicide / Remedy Questions
    if "treat" in p_lower or "cure" in p_lower or "remedy" in p_lower or "spray" in p_lower:
        if context and "display_name" in context:
            d_name = context.get("display_name")
            org = "\n- ".join(context.get("organic_remedies", ["Apply organic copper spray"]))
            chem = "\n- ".join(context.get("chemical_treatments", ["Consult local agricultural extension service"]))
            return f"""### 🩺 Treatment Plan for **{d_name}**

#### 🌱 Organic Remedies:
- {org}

#### 🧪 Chemical Treatments:
- {chem}

#### 🛡️ Prevention Tip:
- {context.get('prevention', ['Keep foliage dry'])[0]}"""

        return """### 🌿 General Crop Integrated Disease Management (IDM)

1. **Cultural Controls**: Maintain adequate spacing, prune dead wood, and use drip irrigation to keep foliage dry.
2. **Organic Sprays**: Use Copper Hydroxide, Wettable Sulfur, or Neem Oil early in the infection cycle.
3. **Nutritional Balance**: Ensure proper Potassium (K) and Calcium (Ca) levels to strengthen plant cell walls against fungal hyphae penetration."""

    # 4. Tomato Diseases
    if "tomato" in p_lower or "leaf curl" in p_lower or "early blight" in p_lower:
        return """### 🍅 Tomato Disease Management

**Symptoms**: Yellowing leaves, brown lesions (Early Blight), upward leaf curl (Leaf Curl Virus), dark wilting (Late Blight).

**Management Protocol**:
1. **Virus Control**: Use certified virus-free transplants. Control whitefly vectors using yellow sticky traps and neem-based insecticides.
2. **Fungal Blight**: Apply Mancozeb + Metalaxyl (for Late Blight) at 7-day intervals during humid weather.
3. **Soil Health**: Maintain pH 6.0-6.8; avoid excess nitrogen which promotes lush growth susceptible to fungal infection."""

    # 5. Potato Late Blight
    if "potato" in p_lower or "late blight" in p_lower:
        return """### 🥔 Potato Late Blight Management

- **Potato Late Blight** (*Phytophthora infestans*): Apply Cymoxanil + Mancozeb or Fluopicolide + Propamocarb at 7-day intervals in humid conditions.
- **Potato Early Blight**: Apply Chlorothalonil or Azoxystrobin; maintain adequate K nutrition to reduce susceptibility.
- **Storage**: Cure tubers at 10-15°C and 85-90% humidity; inspect regularly for soft rot."""

    # Default Helpful Response
    return """### 🌿 Crop Doctor AI Assistant

I can assist you with crop disease detection, identification, organic remedies, and chemical spray schedules!

**Popular Questions You Can Ask**:
- *How do I treat Wheat Rust organically?*
- *What is the best method to prevent Corn Blight?*
- *How do I control Potato Late Blight?*
- *How to manage Tomato Leaf Curl Virus?*
- *What fertilizer ratio promotes crop disease resistance?*

Upload a crop leaf photo above or ask any question about crop farming!"""
