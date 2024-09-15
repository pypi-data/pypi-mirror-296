import argparse
import time
from typing import Any, Dict, List, Literal, Optional, Union

import torch
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class ChatCompletionRequest(BaseModel):
    model: str
    messages: Union[str, List[Dict[str, Any]]] = Field(examples=[[{"role": "user", "content": "hi"}]])
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    max_tokens: Optional[int] = Field(default=512, examples=[None])


def create_app(args):
    if args.model_hub in ["ms", "modelscope"]:
        from modelscope import AutoModelForCausalLM, AutoTokenizer
    else:
        from transformers import AutoModelForCausalLM, AutoTokenizer

    app = FastAPI()
    model = AutoModelForCausalLM.from_pretrained(args.model, torch_dtype="auto", trust_remote_code=True)
    if args.half == "half":
        model = model.half()
    model = model.to(args.device)
    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)

    @app.post("/chat/completions")
    async def chat(request: ChatCompletionRequest):
        text = tokenizer.apply_chat_template(request.messages, tokenize=False, add_generation_prompt=True)
        model_inputs = tokenizer([text], return_tensors="pt").to(args.device)
        with torch.no_grad():
            generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=request.max_tokens, temperature=request.temperature, top_p=request.top_p)
        generated_ids = [output_ids[len(input_ids) :] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return {"response": response}

    return app


def main():
    parser = argparse.ArgumentParser(description="fastspeed: A fastapi deployment tool based on accelerate.")
    parser.add_argument("--model", type=str, required=True, help="Model id or model path.")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host of API.")
    parser.add_argument("--port", type=int, default=8000, help="Port of API.")
    parser.add_argument("--model_hub", type=str, default="modelscope", choices=["hf", "huggingface", "ms", "modelscope"], help="Model hub.")
    parser.add_argument("--half", type=str, default="half", help="huggingface half")
    parser.add_argument("--device", type=str, default="cuda", help="Device")

    args, unknown = parser.parse_known_args()
    app = create_app(args)
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
