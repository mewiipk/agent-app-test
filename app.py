import base64
import os
from typing import Optional

import streamlit as st
from PIL import Image

try:
    from openai import OpenAI
except Exception:  # import errors handled in UI
    OpenAI = None


def _encode_image(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


def _local_fallback(problem_text: str) -> str:
    """Very small fallback path when no model key is configured."""
    try:
        import sympy as sp

        expr = sp.sympify(problem_text)
        simplified = sp.simplify(expr)
        return (
            "I used a local symbolic math fallback (SymPy) because no API key is configured.\n\n"
            f"- Parsed expression: `{sp.srepr(expr)}`\n"
            f"- Simplified result: **{sp.pretty(simplified)}**\n\n"
            "For full tutoring-style explanations and image-based solving, add `OPENAI_API_KEY`."
        )
    except Exception:
        return (
            "I couldn't confidently solve this locally. Please add `OPENAI_API_KEY` "
            "to enable the AI tutor for richer, step-by-step help."
        )


def solve_math_problem(problem_text: str, image_bytes: Optional[bytes]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or OpenAI is None:
        return _local_fallback(problem_text)

    client = OpenAI(api_key=api_key)

    system_prompt = (
        "You are a patient math tutor agent. Always: "
        "1) restate the problem, 2) show step-by-step reasoning, "
        "3) give final answer clearly, 4) include quick verification. "
        "If the uploaded image has text, read and solve it. "
        "If unclear, state assumptions."
    )

    user_content = []
    if problem_text.strip():
        user_content.append({"type": "text", "text": f"Solve this math problem:\n{problem_text.strip()}"})

    if image_bytes:
        user_content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{_encode_image(image_bytes)}"
                },
            }
        )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
    )
    return response.choices[0].message.content


def main() -> None:
    st.set_page_config(page_title="Math Tutor Agent", page_icon="🧠", layout="centered")

    st.title("🧠 Math Tutor Agent")
    st.caption("Paste a problem or upload a photo. The AI agent explains and solves it step by step.")

    with st.form("math_problem_form"):
        problem_text = st.text_area(
            "Math problem",
            placeholder="e.g., Solve 2x + 5 = 17, or simplify (x^2 - 1)/(x - 1)",
            height=140,
        )
        uploaded_file = st.file_uploader(
            "Upload a photo of the problem (optional)",
            type=["png", "jpg", "jpeg", "webp"],
        )
        submitted = st.form_submit_button("Solve with AI Agent")

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded problem image", use_container_width=True)

    if submitted:
        if not problem_text.strip() and not uploaded_file:
            st.warning("Please paste a problem or upload an image.")
            return

        image_bytes = uploaded_file.getvalue() if uploaded_file else None

        with st.spinner("Thinking through the math problem..."):
            result = solve_math_problem(problem_text, image_bytes)

        st.subheader("Solution")
        st.markdown(result)

    with st.expander("Setup (for full AI features)"):
        st.markdown(
            "- Install dependencies: `pip install -r requirements.txt`\n"
            "- Add your key: `export OPENAI_API_KEY=...`\n"
            "- Run app: `streamlit run app.py`\n"
            "\n"
            "Without an API key, the app uses a limited local SymPy fallback for text expressions."
        )


if __name__ == "__main__":
    main()
