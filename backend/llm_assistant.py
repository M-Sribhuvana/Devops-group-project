
"""
AI Plant Assistant Chatbot Service
Gemini-powered agricultural assistant with a local fallback.
"""

import os
from dotenv import load_dotenv
from google import genai

from fruit_diseases_db import FRUIT_DISEASE_DB

# Load variables from backend/.env when running locally.
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """
You are AgriDoctor AI, a helpful agricultural and plant health assistant.

Your primary purpose is to help farmers and students with:
- Crop diseases, symptoms, causes, and diagnosis limitations
- Organic remedies and integrated pest management (IPM)
- Fertilizers, soil health, irrigation, and crop nutrition
- Prevention, cultivation, and general agricultural questions
- Follow-up questions about earlier answers

Instructions:
1. Answer the user's actual question, including custom questions not in a preset list.
2. Do not restrict your answers to a fixed list of crops or keywords.
3. Use the supplied crop diagnosis as context when relevant, but do not assume
   every question is about that diagnosis.
4. If the user asks a general question, answer it directly.
5. Use clear Markdown and practical, easy-to-follow steps.
6. Prefer environmentally responsible methods when appropriate.
7. Do not invent diagnoses, research findings, product labels, or treatment doses.
8. For chemical treatments, advise following the local product label and
   local agricultural guidance.
9. If information is insufficient, explain what additional details are needed.
10. If the question is unrelated to agriculture, answer briefly and helpfully,
    then guide the conversation back to the assistant's agricultural purpose.
"""


def generate_chat_response(
    prompt: str,
    disease_context: dict = None,
    conversation_history: list = None
) -> str:
    """Generate a response to preset or custom user questions."""

    if not isinstance(prompt, str) or not prompt.strip():
        return "Please type a question so I can help you."

    api_key = (
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
    )

    # Build diagnosis context only when useful.
    context_str = ""
    if disease_context:
        context_str = (
            "\nCurrent crop diagnosis (use only if relevant):\n"
            f"{disease_context}\n"
        )

    # Keep recent conversation turns for follow-up questions.
    history_str = ""
    if conversation_history:
        history_lines = []
        for item in conversation_history[-10:]:
            if not isinstance(item, dict):
                continue

            role = item.get("role", "user")
            message = item.get("content", item.get("text", ""))

            if role not in ("user", "assistant", "model"):
                continue
            if isinstance(message, str) and message.strip():
                history_lines.append(f"{role}: {message.strip()}")

        if history_lines:
            history_str = (
                "\nRecent conversation:\n"
                + "\n".join(history_lines)
                + "\n"
            )

    # Gemini can answer questions beyond predefined keywords.
    if api_key:
        try:
            client = genai.Client(api_key=api_key)

            full_prompt = f"""
{SYSTEM_PROMPT}

{context_str}
{history_str}

Current user question:
{prompt.strip()}

Answer the current question directly. Do not simply repeat a list of
suggested questions. If it is a follow-up, use the conversation context.
"""

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=full_prompt
            )

            answer = getattr(response, "text", None)
            if answer and answer.strip():
                return answer.strip()

            print("[Gemini LLM] The model returned an empty response.")

        except Exception as exc:
            # Log details in the backend terminal, not in the user's response.
            print(f"[Gemini LLM] Request failed: {exc}")

    # Use the existing keyword-based fallback if Gemini is unavailable.
    fallback = domain_expert_fallback(prompt, disease_context)

    return fallback



def domain_expert_fallback(prompt: str, context: dict = None) -> str:
    """Provide useful guidance when Gemini is unavailable."""

    p_lower = prompt.lower()
    name = "the diagnosed plant disease"

    if context and context.get("display_name"):
        name = context["display_name"]

    if any(word in p_lower for word in ("hello", "hi", "hey")):
        return (
            "Hello! I'm AgriDoctor AI. I can help with plant diseases, "
            "symptoms, treatment, irrigation, soil health, and fertilizers."
        )

    if any(word in p_lower for word in ("symptom", "sign", "identify")):
        return (
            f"### Symptoms of {name}\n\n"
            "Check for leaf spots, yellowing, wilting, unusual growth, "
            "or lesions. Symptoms vary by disease, so compare them with "
            "the diagnosis shown and monitor whether they spread."
        )

    if any(word in p_lower for word in ("treat", "treatment", "cure", "remedy", "manage")):
        return (
            f"### Treatment guidance for {name}\n\n"
            "Remove severely affected plant material when appropriate, "
            "clean tools, improve airflow, and avoid overhead watering "
            "if the disease spreads in wet conditions. Use only treatments "
            "approved for the crop and disease, following the product label "
            "and local agricultural advice."
        )

    if any(word in p_lower for word in ("prevent", "prevention", "avoid", "spread")):
        return (
            f"### Prevention for {name}\n\n"
            "Use clean tools and healthy planting material, remove infected "
            "debris, provide good spacing and airflow, and avoid excess "
            "moisture on leaves. Follow crop-specific local advice."
        )

    if any(word in p_lower for word in ("water", "irrigation", "irrigate")):
        return (
            "### Irrigation guidance\n\n"
            "Water near the base of the plant, preferably in the morning. "
            "Avoid waterlogging and adjust watering to the crop, soil, "
            "weather, and disease."
        )

    if any(word in p_lower for word in ("npk", "fertilizer", "fertiliser", "nutrient")):
        return (
            "### Fertilizer guidance\n\n"
            "Choose an NPK ratio based on the crop's growth stage and, "
            "ideally, a soil test. Avoid excess fertilizer, especially "
            "nitrogen. There is no single NPK ratio suitable for every crop."
        )

    return (
        f"### Plant care guidance for {name}\n\n"
        "The live AI service is temporarily unavailable. Check the "
        "diagnosis and confidence score, monitor symptoms, keep tools clean, "
        "maintain suitable watering and airflow, and consult a local "
        "agricultural expert for disease-specific treatment."
        "\n\n*Offline guidance mode: Gemini is temporarily unavailable.*"
    )
