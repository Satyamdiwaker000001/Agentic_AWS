import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_PATH = "models/qwen-0.5b"

# ─── Maximize CPU performance ─────────────────────────────────────────
torch.set_num_threads(4)          # Use all CPU threads
torch.set_grad_enabled(False)     # Globally disable gradients (inference only)

# ─── Load tokenizer ───────────────────────────────────────────────────
print("[*] Loading Qwen model...")
_start = time.time()

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)

# ─── Load model directly to CPU ───────────────────────────────────────
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)
model.eval()

# Disabled torch.compile() because it requires MSVC compiler (cl.exe)
# on Windows, which is causing server crashes when not present.
print("[OK] torch.compile skipped (requires MSVC on Windows)")

_elapsed = round(time.time() - _start, 2)
print(f"[OK] Qwen model loaded in {_elapsed}s")


# ─── Warmup ───────────────────────────────────────────────────────────
def warmup_model():
    """Run dummy generations to warm caches."""
    print("[*] Warming up model...")
    _ws = time.time()
    try:
        dummy_input = tokenizer("Hello", return_tensors="pt")
        with torch.inference_mode():
            model.generate(**dummy_input, max_new_tokens=5,
                          pad_token_id=tokenizer.eos_token_id)
        _we = round(time.time() - _ws, 2)
        print(f"[OK] Warmup done in {_we}s - model ready!")
    except Exception as e:
        print(f"[WARN] Warmup skipped: {e}")


warmup_model()