# Fastspeed
Fastspeed is a toolkit for serving LLM.

## Requirements
- Python >= 3.6

## Installation
```shell
pip install fastspeed
```

## Example
- server
```sh
fastspeed --model model_name_or_path  # default model_hub=modelscope
fastspeed --model model_name_or_path --model_hub hf
```

- client
```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/chat/completions' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "messages": [
    {
      "role": "user",
      "content": "Hello"
    }
  ],
  "model": ""
}'
```
