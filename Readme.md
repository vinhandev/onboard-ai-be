# 🚀 FastAPI OpenAI Proxy – Quick Start Tutorial

This guide helps new users get started running the **FastAPI OpenAI Proxy** project and a local static client.

---

## 🧩 Step 1 – Set up the environment

### 🪟 Windows

```powershell
# 1. Create and activate a virtual environment
py -m venv .venv
.\.venv\Scripts\activate

# 2. Install dependencies
py -m pip install uvicorn
py -m pip install fastapi
py -m pip install httpx
py -m pip install python-dotenv
```

### 🍎 macOS / Linux

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
python3 -m pip install uvicorn
python3 -m pip install fastapi
python3 -m pip install httpx
python3 -m pip install python-dotenv
```

---

## 📂 Step 2 – Navigate to your project folder

### 🪟 Windows

```powershell
cd C:\Projects\python-openai-api\
```

### 🍎 macOS / Linux

```bash
cd ~/Projects/python-openai-api/
```

---

## 🔐 Step 3 – Create your .env file

This file stores your OpenAI API key and CORS origins.

### 🪟 Windows

```powershell
echo OPENAI_API_KEY=sk-your-openai-key > .env
```

### 🍎 macOS / Linux

```bash
echo "OPENAI_API_KEY=sk-your-openai-key" > .env
```

---

## ⚙️ Step 4 – Run the FastAPI server

### 🪟 Windows

```powershell
py -m uvicorn fastapi_openai_proxy:app --reload --port 8000
```

### 🍎 macOS / Linux

```bash
python3 -m uvicorn fastapi_openai_proxy:app --reload --port 8000
```

🩺 Check health endpoint:
Open your browser and visit → [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

Expected output:

```json
{ "status": "ok" }
```

---

## 🌐 Step 5 – Run the static client

Put your `chat.html` (or `index.html`) file inside a folder, for example `client/`.

### 🪟 Windows

```powershell
cd client
py -m http.server 5500
```

### 🍎 macOS / Linux

```bash
cd client
python3 -m http.server 5500
```

🧭 Now open your browser and visit:
👉 [http://127.0.0.1:5500/](http://127.0.0.1:5500/)

---

## ✅ Step 6 – Test the Chat API

In your client JavaScript:

```js
fetch('http://127.0.0.1:8000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ prompt: 'Hello!', model: 'gpt-4o-mini' }),
})
  .then((res) => res.json())
  .then(console.log);
```

You should see a JSON response with the model’s reply.

---

## 🧠 Common issues

| Problem                    | Fix                                                              |
| -------------------------- | ---------------------------------------------------------------- |
| `No module named uvicorn`  | Install inside venv → `pip install uvicorn`                      |
| `CORS policy` error        | Add your client URL to `ALLOWED_ORIGINS` in `.env`               |
| `401 Authentication Error` | Make sure you use your real **OpenAI API key**, not a proxy key  |
| `.env not loaded`          | Ensure `.env` is in the same folder as `fastapi_openai_proxy.py` |
| `Port already in use`      | Try `--port 8001` or `--port 5501`                               |

---

## 🧾 Example .env

```
OPENAI_API_KEY=sk-xxxxxYourKeyxxxxx
ALLOWED_ORIGINS=http://127.0.0.1:5500,http://localhost:5500
```
