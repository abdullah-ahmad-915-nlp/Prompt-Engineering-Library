from pathlib import Path

import boto3
from botocore.exceptions import ClientError

REGION = "us-west-2"
MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"

PROMPTS_DIR = Path("prompts")
INPUT_DIR = Path("inputs")
OUTPUTS_DIR = Path("outputs")

OUTPUTS_DIR.mkdir(exist_ok=True)

client = boto3.client("bedrock-runtime", region_name=REGION)

def generate(prompt: str) -> str:
    response = client.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        inferenceConfig={
            "temperature": 0.2,
            "maxTokens": 1024
        }
    )

    return response["output"]["message"]["content"][0]["text"]

def main():
    prompt_files = sorted(PROMPTS_DIR.glob("*.md"))

    if not prompt_files:
        print("No prompt files found.")
        return

    for prompt_file in prompt_files:
        task_name = prompt_file.stem
        input_file = INPUT_DIR / f"{task_name}_input.md"

        if not input_file.exists():
            print(f"Skipping {task_name}: input file not found.")
            continue

        prompt_template = prompt_file.read_text(encoding="utf-8").strip()
        input_text = input_file.read_text(encoding="utf-8").strip()
        full_prompt = (f"{prompt_template}\n\n{input_text}")

        print(f"Running: {task_name}")

        try:
            output = generate(full_prompt)
            output_file = OUTPUTS_DIR / f"{task_name}_output.md"
            output_file.write_text(output, encoding="utf-8")

            print(f"SAVED: {output_file}")

        except ClientError as e:
            print(f"FAILED: {task_name}")
            print(e)

main()