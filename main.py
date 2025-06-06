from together import Together

client = Together()

target_word = "ijsbeer"
user_question = input("Wat is jouw gokwoord? ")

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    messages=[
        {
            "role": "system",
            "content": (
                "Je bent een spelmaster. De speler moet een woord raden. "
                "Beoordeel het gokwoord van de speler ten opzichte van het doelwoord. "
                "Antwoord uitsluitend met één van deze woorden, en niets anders:\n"
                "- juist\n"
                "- bijna goed\n"
                "- zelfde thema\n"
                "- totaal fout"
            )
        },
        {
            "role": "user",
            "content": f"Het doelwoord is '{target_word}'. De speler gokt: '{user_question}'."
        }
    ]
)

print(response.choices[0].message.content)