from utils import load_data, parse_elements, make_input_prompt
from prompt import system_prompts, few_shot_examples
from tqdm import tqdm
import json

def gpt_api_request_body(prompt, type, custom_id):
    system_prompt = system_prompts[type]
    few_shot_example = few_shot_examples[type]
    if len(few_shot_example) % 2 != 0:
        raise ValueError(f"few_shot_example's length must be even: {len(few_shot_example)}")

    messages = [{"role": "system", "content": system_prompt}]

    for i in range(len(few_shot_example)):
        role = "user" if i % 2 == 0 else "assistant"
        messages.append({"role": role, "content": few_shot_example[i]})

    messages.append({"role": "user", "content": prompt})

    # Return a request format compatible with Batch API
    return {
        "custom_id": custom_id,
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4o",
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0.2
        }
    }

def prepare_batch_jsonl(error_type, data, jsonl_file):
    """
    Prepare a JSONL file with batch requests based on the input data.
    """
    with open(jsonl_file, 'w') as file:
        for _, item in enumerate(tqdm(data)):
            knowledge_edits, knowledge_chain = parse_elements(item)
            for candidate in item['predicted']['cot']['generated_output']:
                if candidate['is_selected']:
                    instance = candidate
                    break
            
            thoughts = instance['thoughts']
            case_id = item['case_id']

            if error_type != 'distortion':
                prompt = make_input_prompt(knowledge_edits, None, thoughts, error_type)
            elif error_type == 'distortion':
                prompt = make_input_prompt(None, knowledge_chain, thoughts, error_type)
            else:
                raise ValueError(f"error_type is not valid: {error_type}")

            # Create requests for each type of evaluation
            error_request = gpt_api_request_body(prompt, error_type, f"{error_type}-{case_id}")

            # Write requests to file
            file.write(json.dumps(error_request) + '\n')

if __name__ == '__main__':
    # Step 1: Load data and prepare JSONL file
    for model_name in ['llama3', 'mistral', 'qwen2']:
        data = load_data(f'../editing_results/rome_{model_name}_mquake_sample.json')
        
        error_types = ['persistence', 'mismatch', 'distortion']
        for error_type in error_types:
            # Step 2: Prepare the batch JSONL file
            batch_jsonl_file = f'../input/{model_name}/rome_{model_name}_mquake_{error_type}_batch_input_sample.jsonl'
            prepare_batch_jsonl(error_type, data, batch_jsonl_file)
            
        print(f"Batch input file created: {batch_jsonl_file}")
