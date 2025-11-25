import json

def load_data(path):
    # load JSON file
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def save_data(path, data):
    # save json file
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def parse_elements(item):
    knowledge_chain = '\n'.join([f'{idx+1}. ('+', '.join(hop)+')' for idx, hop in enumerate(item["orig"]["new_triples_labeled"])])
    
    new_premise = []
    # create a dictionary to map relation ID to natural language
    relation_dict = {}

    # extract relation from new_triples_labeled
    for i, triple in enumerate(item["orig"]["edit_triples"]):
        relation_id = triple[1]  # the second element of edit_triples is relation ID
        relation_label = None
        for j, triple_ in enumerate(item["orig"]["new_triples"]):
            if triple_[1] == relation_id:
                relation_label = item["orig"]["new_triples_labeled"][j][1]  # the second element of new_triples_labeled is natural language relation
        if not relation_label:
            raise Exception
        relation_dict[relation_id] = relation_label  # map relation ID to natural language
    
    for idx, rewrite in enumerate(item["requested_rewrite"]):
        subject = rewrite['subject']
        relation = relation_dict[rewrite['relation_id']]
        
        if (relation is None):
            raise ValueError("Relation label not found")
        
        target_true = rewrite['target_true']['str']
        target_new = rewrite['target_new']['str']
        
        # save in tuple format (include relation)
        new_premise.append(f"{idx+1}. ({subject}, {relation}, {target_true} → {target_new})")
    
    knowledge_edits = '\n'.join(new_premise)

    return knowledge_edits, knowledge_chain

def make_input_prompt(knowledge_edits, knowledge_chain, thoughts, type=None):
    if type is 'distortion':
        prompt = f"# Knowledge Chain:\n{knowledge_chain}\n\n# Post-Edit Reasoning Path\n{thoughts}"
    else:
        prompt = (
            f"# Knowledge Edits:\n{knowledge_edits}\n\n"
            f"# Post-Edit Reasoning Path\n{thoughts}"
        )
    return prompt
