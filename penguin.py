"""
Пингвин — ваш собственный ИИ-ассистент.

Запуск:
    pip install anthropic
    export ANTHROPIC_API_KEY="ваш_ключ"     # Windows: set ANTHROPIC_API_KEY=ваш_ключ
    python penguin.py

Ключ можно получить на https://console.anthropic.com
Чтобы выйти из чата, напишите: выход
"""

import anthropic

# Модель, на которой работает Пингвин. Можно заменить на другую.
MODEL = "claude-sonnet-5-5"

# Здесь задаётся личность Пингвина. Меняйте как хотите!
SYSTEM_PROMPT = """Ты — Пингвин, дружелюбный и умный ИИ-ассистент.

Характер:
- Спокойный, доброжелательный, с лёгким чувством юмора.
- Иногда уместно шутишь про лёд, рыбу и Антарктиду, но не злоупотребляешь этим.
- Объясняешь просто и понятно, без лишней воды.

Правила:
- Всегда называй себя Пингвин.
- Отвечай на том языке, на котором пишет пользователь.
- Если чего-то не знаешь — честно скажи об этом, не выдумывай.
- Помогай с учёбой, текстами, кодом, идеями и повседневными вопросами.
"""


def main():
    client = anthropic.Anthropic()  # берёт ключ из ANTHROPIC_API_KEY
    history = []

    print("🐧 Пингвин на связи! (для выхода напишите: выход)\n")

    while True:
        try:
            user_text = input("Вы: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n🐧 Пока!")
            break

        if not user_text:
            continue
        if user_text.lower() in ("выход", "exit", "quit"):
            print("🐧 Пока! Заходите ещё.")
            break

        history.append({"role": "user", "content": user_text})

        print("Пингвин: ", end="", flush=True)
        reply = ""
        try:
            with client.messages.stream(
                model=MODEL,
                max_tokens=1500,
                system=SYSTEM_PROMPT,
                messages=history,
            ) as stream:
                for chunk in stream.text_stream:
                    print(chunk, end="", flush=True)
                    reply += chunk
        except anthropic.APIError as e:
            print(f"\n[Ошибка API: {e}]")
            history.pop()  # убираем сообщение, на которое не получили ответ
            continue

        print("\n")
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
