import torch
import sys

print(f"Python: {sys.version}")
print(f"PyTorch: {torch.__version__}")
print(f"torch.compile available: {hasattr(torch, 'compile')}")
print(f"CPU threads: {torch.get_num_threads()}")
