import pandas as pd
import json

# 1. Load your original CSV file
df = pd.read_csv('security_commands_context_command.csv')

def create_mistral_format(row):
    """
    Wraps the prompt and command in Mistral's instruction tokens.
    Format: <s>[INST] Instruction [/INST] Answer </s>
    """
    context = row['context_prompt']  # This is the JSON string (tool, prompt, os)
    command = row['command']         # This is the target shell command
    
    return f"<s>[INST] {context} [/INST] {command} </s>"

# 2. Apply the formatting to every row
df['text'] = df.apply(create_mistral_format, axis=1)

# 3. Save only the 'text' column to a JSONL file
# JSONL (JSON Lines) is the standard format for fine-tuning LLMs
df[['text']].to_json('prepared_mistral_data.jsonl', orient='records', lines=True)

print("Data preparation complete! File saved as: prepared_mistral_data.jsonl")
print(f"Sample row:\n{df['text'].iloc[0]}")