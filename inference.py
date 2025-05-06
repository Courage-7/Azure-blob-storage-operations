from transformers import AutoModelForCausalLM, AutoTokenizer

# Path to the model files
model_path = r"c:\Users\V\Desktop\azure-blob\container_contents\blobs\DeepSeek-R1-Distill-Qwen-1.5B-1742394704\model-files"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map="auto",  # Use available GPU or CPU
    trust_remote_code=True  # May be needed for some models
)

# Example prompt for inference
prompt = "Write a short story about a robot learning to paint:"

# Tokenize input
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

# Generate text with parameters from generation_config.json
outputs = model.generate(
    inputs.input_ids,
    max_length=500,  # Adjust as needed
    do_sample=True,
    temperature=0.6,
    top_p=0.95,
    bos_token_id=151646,
    eos_token_id=151643,
)

# Decode and print the generated text
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(generated_text)