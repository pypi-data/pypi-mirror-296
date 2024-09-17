from .archon import Archon
from dotenv import load_dotenv
load_dotenv()
# Initialize Archon

archon_config = {
    "name": "archon-quickstart",
    "layers": [
        [
            {
                "type": "generator",
                "model": "claude-3-haiku-20240307",
                "model_type": "Anthropic_API",
                "top_k": 1,
                "temperature": 0.7,
                "max_tokens": 2048,
                "samples": 1
            }
        ]
    ],
}

#################################################

archon = Archon(archon_config, query_saves=False)

testing_instruction = [{"role": "user", "content": "How do I make a cake?"}]

response = archon.generate(testing_instruction)

print(response)
