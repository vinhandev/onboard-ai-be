step 1 : py -m venv .venv

step 2 : cd C:\Projects\python-openai-api\
step 3: echo OPENAI_API_KEY= > .env

py -m uvicorn fastapi_openai_proxy:app --reload --port 8000

py -m http.server 5500 ~ client
