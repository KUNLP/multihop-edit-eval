import json
import re

model_names = ['mistral', 'llama3', 'qwen2']
error_types = ['persistence', 'mismatch', 'distortion']


# Function to extract "True" and "False" results from the assistant's output
def extract_true_false(content):
    # Regex to capture lines with Result: True or Result: False
    pattern = r"Result:\s*(True|False)"
    matches = re.findall(pattern, content)
    return matches

# Function to evaluate alignment based on the rules provided
def check_alignment(result_list, target_length):
    return len(result_list) == target_length

scores = {model_name: {error_type: {}} for model_name in model_names for error_type in error_types}

for model_name in model_names:
    # Step 2: Read the JSON file (containing case_id and rewrites)
    data_path = f'../editing_results/rome_{model_name}_mquake_sample.json'  # Path to the JSON file
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    case_id_to_edit_count = {}
    for instance in data:
        case_id = instance['case_id']
        case_id_to_edit_count[case_id] = len(instance['requested_rewrite'])
    
    # Step 1: Read and Parse the JSONL file
    for error_type in error_types:
        file_path = f'../output/{model_name}/rome_{model_name}_mquake_{error_type}_batch_output_sample.jsonl'

        # Read the JSONL file
        outputs = []
        with open(file_path, 'r') as file:
            for line in file:
                outputs.append(json.loads(line))
        
        score = 0
        for item in outputs:
            content = item['response']['body']['choices'][0]['message']['content']
            parsed_results = extract_true_false(content)
            parsed_results = [True if item=='True' else False for item in parsed_results]
            
            case_id = int(item['custom_id'].split('-')[1])
            # Calculate and store average scores for this case
            if error_type=='distortion':
                avg_score = sum(parsed_results) / len(parsed_results)
                score += avg_score
            else:
                edit_count = case_id_to_edit_count[case_id]  # Get the length of requested_rewrite
                is_alignment = check_alignment(parsed_results, edit_count)

                if is_alignment:
                    is_error = True if (sum(parsed_results) / len(parsed_results)) > 0 else False
                    score += is_error
                else:
                    print(f"Model: {model_name}, Error Type: {error_type}, Case ID: {case_id}, Alignment: {is_alignment}")
        scores[model_name][error_type] = score/len(outputs)

for model_name in model_names:
    print(f"Model: {model_name}")
    for error_type in error_types:
        print(f"Error Type: {error_type}, Score: {scores[model_name][error_type]*100:.2f}")


