"""Pre-built: the model call, keyless, with a strict output schema and a cost.

Signs in with your Azure identity (`az login` on your machine, OIDC in GitHub
Actions): no API key anywhere. Every call returns the parsed JSON, the tokens
used, and what they cost.
"""

import json
import os
from dataclasses import dataclass
from functools import lru_cache

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

# Prices per 1K tokens for gpt-5.4-mini, GlobalStandard, as of October 2026.
# Estimates for the cost line, not billing truth: your Azure bill always wins.
PRICE_IN_PER_1K = 0.00025
PRICE_OUT_PER_1K = 0.001


@dataclass
class Reply:
    data: dict  # the model's answer, parsed: it always matches the schema
    input_tokens: int
    output_tokens: int

    @property
    def cost_usd(self) -> float:
        return (self.input_tokens * PRICE_IN_PER_1K + self.output_tokens * PRICE_OUT_PER_1K) / 1000


@lru_cache
def client() -> OpenAI:
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    if not endpoint:
        raise SystemExit("AZURE_OPENAI_ENDPOINT isn't set: paste the export lines from scripts/bring-up.sh")
    token = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")
    return OpenAI(base_url=endpoint, api_key=token, max_retries=4, timeout=60)


def ask(instructions: str, prompt: str, schema: dict, name: str = "review") -> Reply:
    """One call. The service only lets the model produce JSON that fits `schema`."""
    response = client().responses.create(
        model=os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT", "chat"),
        instructions=instructions,
        input=prompt,
        text={"format": {"type": "json_schema", "name": name, "schema": schema, "strict": True}},
    )
    usage = response.usage
    return Reply(json.loads(response.output_text), usage.input_tokens, usage.output_tokens)
