import transformers

from timer import Timer

timer = Timer()

model = transformers.AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = transformers.AutoTokenizer.from_pretrained("gpt2")
timer.lap("load model")

dataset = [
    "Hello, my name is",
    "I am a student",
    "I am a programmer",
    "I am a data scientist",
    "I am a software engineer",
    "I am a machine learning engineer",
]

timer.lap("load dataset")

optimizer = transformers.AdamW(model.parameters(), lr=1e-4)
model = model.to("cuda")

timer.lap("preprocess")
timer.split("preprocess")


for data in dataset:
    inputs = tokenizer(data, return_tensors="pt")
    inputs = inputs.to("cuda")
    outputs = model(**inputs, labels=inputs["input_ids"])
    loss = outputs.loss
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    timer.lap("train_step")

timer.split("training")

example = "I am"
input_ids = tokenizer(example, return_tensors="pt")["input_ids"].to("cuda")
output = model.generate(input_ids, max_length=50)
output_text = tokenizer.decode(output[0], skip_special_tokens=True)

timer.lap("generate")

timer.split("end")

print(timer.report(sort_key=False))
