import random


def generate_prompt(ai_model, inputs):
    if isinstance(inputs, str):
        inputs = [inputs]
    formatted_inputs = [input.capitalize() for input in inputs]
    return ai_model.value.format(*formatted_inputs)


def weighted_random(lowest, highest, std_dev):
    mean = (lowest + highest) / 2
    iteration = 0
    while iteration < 1500:
        num = random.normalvariate(mean, std_dev)
        if lowest <= num <= highest:
            return num
        iteration += 1
    return mean


def get_random_theme():
    with open('resources/list_of_themes.txt') as f:
        themes = f.read().splitlines()
        theme = random.choice(themes).strip()
    return theme
