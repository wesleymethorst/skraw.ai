from together import Together

client = Together()

user_question = input("Stel je vraag aan de AI: ")

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    messages=[
        {
            "role": "system",
            "content": (
                "Je bent een AI die zeer goed is in topografie. Je kent alle hoofdsteden van de wereld. "
                "Wanneer je een vraag krijgt, geef je enkel 'ja' of 'nee' als antwoord, op basis van of de bewering feitelijk klopt."
            )
        },
        {
            "role": "user",
            "content": user_question
        }
    ]
)

print(response.choices[0].message.content)