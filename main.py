#import os
#os.environ['HF_HOME'] = './.cache'

from fastapi import FastAPI, Query
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from transformers import AutoModelForCausalLM, AutoTokenizer


model_path = "theoracle/resume2"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="auto",
        torch_dtype='auto',
       # offload_dir=offload_dir
    ).eval()

tokenizer.pad_token = tokenizer.eos_token

app = FastAPI()


@app.get("/greet/{name}")
def greet_name(name: str):
    return {"message": f"Hello, {name}!"}


@app.get("/testpage")
def just_a_page():
    return {"message": "Just a test page"}


@app.get("/gemmac64")

def gemma_64(input):#: str = Query(default="")
    #device = "cuda" if torch.cuda.is_available() else "cpu"
    
    prompt = f'''###resume: {input}
    ###json: '''

    # Tokenize the prompt to get input IDs and attention mask
    encoding = tokenizer(prompt, return_tensors='pt', padding=True, truncation=True, max_length=500, add_special_tokens=True)
    input_ids = encoding['input_ids']
    attention_mask = encoding['attention_mask']

    # Generate output, ensuring to pass the attention mask and set pad_token_id
    output_ids = model.generate(
        input_ids.to('cuda'),
        attention_mask=attention_mask.to('cuda'),
        max_new_tokens=300,  # Specify the number of new tokens to generate
        pad_token_id=tokenizer.eos_token_id,
        #temperature=0.7,
        #do_sample=True,
        #top_k=1,
        #repetition_penalty=1.5

       )

    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return JSONResponse(content={"output": response})

    #return response

app.mount("/", StaticFiles(directory="static", html=True), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(path="/app/static/index.html", media_type="text/html")




