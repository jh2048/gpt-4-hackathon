import openai
import os
import pandas as pd

openai.api_key = os.getenv("OPENAI_API_KEY")


def prompt_gpt_4(input_message: str = "Let's Go!"):

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{input_message}"},
        ],
    )
    generated_text = response["choices"][0]["message"]["content"].strip()
    print(f"Generated response: {generated_text}")
    return generated_text


df = pd.read_json("food-enforcement.json")
