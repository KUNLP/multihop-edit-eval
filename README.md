# Watch Your Step: A Fine-Grained Evaluation Framework for Multi-hop Knowledge Editing in Large Language Models

Official code for the CIKM 2025 paper:  
**Watch Your Step: A Fine-Grained Evaluation Framework for Multi-hop Knowledge Editing in Large Language Models**

## Paper

📄 [Watch Your Step: A Fine-Grained Evaluation Framework for Multi-hop Knowledge Editing in Large Language Models (CIKM 2025)](https://dl.acm.org/doi/10.1145/3746252.3760840)

## Directory Structure

- `src/`  
  Main pipeline code for evaluation, data preprocessing, and scoring.
- `editing_results/`  
  Stores the results of knowledge editing (e.g., responses from edited LLMs). Currently, only 100 samples are included.
- `input/`  
  Input data for evaluation (e.g., queries, gold answers). Currently, only 100 samples are included.
- `output/`  
  Stores evaluation results (e.g., GPT-4o outputs, scores). Currently, only 100 samples are included. Note that any identifiable information (e.g., OpenAI request IDs) has been removed from the results.
- `src/prompt.py`  
  Contains system prompts and few-shot examples used for generating evaluation requests.

## Evaluation Pipeline

1. **Perform Knowledge Editing and Save Results**
   - Run your knowledge editing method and save the edited LLM responses in the `editing_results/` directory.
   - File format and naming may vary by experiment.

2. **Create GPT-4o Evaluation Batch**
   - Change directory to `src/`:
     ```bash
     cd src
     ```
   - Run the batch creation script:
     ```bash
     python create_batch_jsonl.py
     ```
   - This will generate batch input files in the `input/` directory for each model and error type.

3. **Call OpenAI Batch API**
   - Upload the generated batch jsonl files to the OpenAI Platform Batch API and request evaluation with GPT-4o.
   - Refer to the OpenAI Batch documentation.

4. **Save API Results**
   - Download the evaluation results from OpenAI and save them in the `output/` directory.
   - Example filename:  
     `output/{model_name}/rome_{model_name}_mquake_{error_type}_batch_output_sample.jsonl`
   - Each line should include the evaluation query, model response, and GPT-4o's evaluation (score, reasoning, etc).

5. **Scoring**
   - Run the scoring script to compute final scores and statistics:
     ```bash
     python scoring.py
     ```
   - The script will print the scores for each model and error type.

---

## Citation

If you use this framework in your research, please cite the following paper:

```bibtex
@inproceedings{jeong2025watch,
  author       = {Geunyeong Jeong and Juoh Sun and Harksoo Kim},
  title        = {Watch Your Step: A Fine-Grained Evaluation Framework for Multi-hop Knowledge Editing in Large Language Models},
  booktitle    = {Proceedings of the 34th ACM International Conference on Information and Knowledge Management (CIKM)},
  year         = {2025},
  doi          = {10.1145/3746252.3760840}
}
