import openai

openai.api_key = "YOUR_API_KEY"


def get_solution(problem_description):
    prompt = f"What is the solution to the following problem:\n{problem_description}"
    completions = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text.strip()
    return message
