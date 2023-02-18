import os
import openai


beer_number = os.getenv("BEER_NUMBER")
admin_user = os.getenv("ADMIN_USER")
dev_channel = os.getenv("DEV_CHANNEL")

openai.api_key = os.getenv("OPENAI_API_KEY")


def do_openai_question(prompt, temperature=0.5, max_tokens=150, top_p=0.3, frequency_penalty=0.5,
                       presence_penalty=0.0):

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )

    except openai.APIError as error:
        if error.status_code == 429:
            return f"The billing limit has been reached. Please try again later. Else you can :beer: me @{admin_user} at {beer_number}"
        return f"There was a server issue. Please try again later. @{admin_user}"

    return f"{response.choices[0].text.lstrip()}"


def do_openai_image_create(question):
    # TODO: handle exceptions
    return openai.Image.create(
        prompt=question,
        n=1,
        size="1024x1024"
    )
