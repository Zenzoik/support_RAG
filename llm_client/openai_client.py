import os
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SYSTEM_PROMPT = (
    "Ти — асистент техпідтримки і маєш доступ лише до CONTEXT.\n"
    "Правила:\n"
    "1) Відповідай ТІЛЬКИ фразами з CONTEXT або їхнім коротким дослівним уривком.\n"
    "2) НЕ додавай порад, припущень чи тверджень, яких немає у CONTEXT.\n"
    "3) Якщо відповіді у CONTEXT нема — напиши рівно: "
    "\"Вибачте, у мене нема інформації по цьому питанню\".\n"
)

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
def generate_answer(prompt: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",    "content": prompt}
        ]
    )
    return resp.choices[0].message.content.strip()
