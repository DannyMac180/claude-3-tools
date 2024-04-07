import anthropic
import os
from dotenv import load_dotenv
from tools import get_weather

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)

# Send the initial message asking for the weather in a city
response = client.beta.tools.messages.create(
    model="claude-3-opus-20240229",
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
                },
                "required": ["location"]
            }
        }
    ],
    messages=[{"role": "user", "content": "What is the weather like in Atlanta?"}]
)

# Extract the tool_use data from the response
tool_use_data = response.content[-1]

# Call the get_weather function with the provided input
weather_result = get_weather(tool_use_data.input['location'])

# Send the tool result back to the assistant
response = client.beta.tools.messages.create(
    model="claude-3-opus-20240229",
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
                },
                "required": ["location"]
            }
        }
    ],
    messages=[
        {"role": "user", "content": "What is the weather like in New York City?"},
        {"role": "assistant", "content": response.content[0].text},
        {"role": "user", "content": [
            {
                "type": "tool_result",
                "tool_use_id": tool_use_data.id,
                "content": weather_result
            }
        ]}
    ]
)

print(response['content'][0]['text'])