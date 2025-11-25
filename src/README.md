# Source Code Overview

This directory contains the core scripts for running the evaluation pipeline of **Watch Your Step**, a framework for assessing multi-hop knowledge editing performance in large language models.

## Files

| File | Description |
|------|-------------|
| create_batch_jsonl.py | Generates batch input files for GPT-4o evaluation. |
| scoring.py | Computes scores and statistics from GPT-4o evaluation outputs. |
| prompt.py | Includes system prompts and few-shot examples used for evaluation requests. |
| utils.py *(if applicable)* | Helper functions for data loading and processing. |

## Usage

### 1. Generate batch jsonl files

    cd src
    python create_batch_jsonl.py

Batch files will be saved under `input/`.

### 2. Run scoring

    python scoring.py

This script prints evaluation metrics for each model and error type.

## Notes

- The provided sample dataset contains 100 examples.
- File naming conventions for editing results and outputs should match those used in the pipeline.
- Personally identifiable metadata (e.g., API request IDs) is removed.

---

For more information, please refer to the main project README.
