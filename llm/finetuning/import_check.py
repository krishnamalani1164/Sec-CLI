import os
import sys

# Force bypass triton and specific torch patches that cause the 'int1' error
os.environ["UNSLOTH_RETURN_LOGITS"] = "1"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

try:
    from unsloth import FastLanguageModel
    import torch
except Exception as e:
    print(f"Still failing? Error: {e}")

# The rest of your code...