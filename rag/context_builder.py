def build_context(retrieved_items,user_prompt):
    """
    Build a structure prompt for the LLM using retrieved.
    """
    context = "You are an expert command-line assisstant.\n"
    context += "Use the following examples to generate a safe CLI coomand.\n\n"

    for i,item in enumerate(retrieved_items, start = 1):
        context += f"Example {i}:\n"
        context += f"User Prompt: {item['nl_prompt']}\n"
        context += f"Command: {item['cli_command_demo']}\n"
        context += f"Safety Note: {item['safety_note']}\n\n"
    
    context += "Now generate a single CLI command for the following request.\n"
    context += f"User Request: {user_prompt}\n"
    context += "Only output the command. Do not explain.\n"

    return context