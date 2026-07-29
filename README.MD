# Prompt Engineering Library

A structured library of reusable prompt templates for common AI tasks, paired
with a runnable Python script that executes each prompt against an Amazon
Bedrock model (Anthropic Claude) and saves the generated output. This
demonstrates not just prompt design, but how prompts integrate into a real,
end-to-end AI application.

## Overview

| Category | Prompt | Sample Input | Sample Output |
|---|---|---|---|
| Summarization | [`prompts/summarization.md`](prompts/summarization.md) | [`inputs/summarization_input.md`](inputs/summarization_input.md) | [`outputs/summarization_output.md`](outputs/summarization_output.md) |
| Translation | [`prompts/translation.md`](prompts/translation.md) | [`inputs/translation_input.md`](inputs/translation_input.md) | [`outputs/translation_output.md`](outputs/translation_output.md) |
| JSON Extraction | [`prompts/json_extraction.md`](prompts/json_extraction.md) | [`inputs/json_extraction_input.md`](inputs/json_extraction_input.md) | [`outputs/json_extraction_output.md`](outputs/json_extraction_output.md) |
| Email Generation | [`prompts/email_generation.md`](prompts/email_generation.md) | [`inputs/email_generation_input.md`](inputs/email_generation_input.md) | [`outputs/email_generation_output.md`](outputs/email_generation_output.md) |
| Data Validation | [`prompts/data_validation.md`](prompts/data_validation.md) | [`inputs/data_validation_input.md`](inputs/data_validation_input.md) | [`outputs/data_validation_output.md`](outputs/data_validation_output.md) |
| SQL Generation | [`prompts/sql_generation.md`](prompts/sql_generation.md) | [`inputs/sql_generation_input.md`](inputs/sql_generation_input.md) | [`outputs/sql_generation_output.md`](outputs/sql_generation_output.md) |

## Project Structure

```
prompt-engineering-library/
├── prompts/           # Prompt templates (one per task, .md)
├── inputs/            # Example input data for each prompt (.md)
├── outputs/           # Generated model outputs, saved after each run (.md)
├── run_prompts.py      # Runs every prompt+input pair through Bedrock
├── requirements.txt    # Python dependencies
└── README.md
```

Each prompt in `prompts/` is paired with an input file of the same name in
`inputs/` (e.g. `prompts/sql_generation.md` ↔ `inputs/sql_generation_input.md`).
`run_prompts.py` combines each pair, sends it to the model, and writes the
response to `outputs/<name>_output.md`.

## Prerequisites

- Python 3.9+
- An AWS account with access to **Amazon Bedrock**
- Model access enabled for the Claude model used in `run_prompts.py`
  (Bedrock console → **Model access**)
- AWS credentials configured locally (e.g. via `aws configure`, environment
  variables, or an IAM role) with `bedrock:InvokeModel` / Converse permissions

## Setup

```bash
# Clone the repo
git clone <your-repo-url>
cd prompt-engineering-library

# Install dependencies
pip install -r requirements.txt
```

## Usage

Run every prompt in the library against the configured Bedrock model:

```bash
python run_prompts.py
```

For each `prompts/<name>.md` file with a matching `inputs/<name>_input.md`
file, the script will:

1. Combine the prompt template and input text into a single message.
2. Send it to the model via the Bedrock `Converse` API.
3. Save the raw response to `outputs/<name>_output.md`.
4. Print a `SAVED` or `FAILED` line to the console per task.

To change the model or region, edit the constants at the top of
`run_prompts.py`:

```python
REGION = "us-west-2"
MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
```

## Prompt Design Notes & Observations

- **Summarization** — constrains output to one paragraph, ≤150 words, no
  bullet points. Reliably stays on-topic and within the word limit; works
  well for condensing explanatory/informational text.
- **Translation** — explicitly instructs idiom-aware translation rather than
  literal word-for-word conversion, and preserves names/numbers/formatting.
  Produces natural, fluent translations rather than stiff literal ones.
- **JSON Extraction** — enforces "no markdown/code fences, null for missing
  fields, no invented data" to keep output machine-parseable. Consistently
  returns clean, valid JSON matching the requested schema.
- **Email Generation** — structured with explicit sections (greeting, body,
  closing) and a "don't invent information" constraint. Produces
  well-organized, professional emails that stick closely to the facts
  supplied in the input.
- **Data Validation** — encodes explicit business rules (field formats,
  ranges, allowed values) and asks for a structured JSON validation report.
  Correctly flags invalid records with specific field-level error messages
  without altering the input data.
- **SQL Generation** — restricts output to a single, unexplained SQL query
  and instructs the model not to assume undocumented columns. Reliably infers
  correct joins and filters from the supplied schema and relationship
  description.

**General observation:** prompts that pair a narrow, single-purpose task with
explicit output-format constraints (e.g. "valid JSON only," "one paragraph,"
"no explanations") produce far more consistent, directly usable output than
open-ended instructions — this made it easier to plug these prompts directly
into a script and treat the output as structured data rather than free text.

## Notes on Amazon Bedrock

- This project uses Bedrock's **Converse API**, which provides a unified
  interface across Bedrock-hosted models.
- `ThrottlingException` errors (e.g. "too many tokens per day") can occur
  if Bedrock on-demand quotas haven't been raised.
  Quotas can be viewed and requested per-model under **Service Quotas** in the
  AWS Console.
- Model IDs occasionally reach end-of-life and are retired; if a
  `ResourceNotFoundException` mentions a model has "reached the end of its
  life," swap in a current model ID from the Bedrock **Model catalog**.