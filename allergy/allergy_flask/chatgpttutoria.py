import openai

API_KEY = open("API_KEY.txt", "r").read()
openai.api_key = API_KEY

response = openai.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = [{"role": "user", "content": "What is the difference between Celsius and Fahrenheit?"},]
)

print(response)