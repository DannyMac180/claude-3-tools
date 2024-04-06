import anthropic
import os

client = anthropic.Anthropic()

response = client.beta.tools.messages.create(
    model="claude-3-opus-20240229",
    api_key=os.environ["ANTHROPIC_API_KEY"],
    max_tokens=1024,
    tools=[
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The unit of temperature, either \"celsius\" or \"fahrenheit\""
                    }
                },
                "required": ["location"]
            }
        }
    ],
    messages=[{"role": "user", "content": "What is the weather like in San Francisco?"}]
)

print(response)