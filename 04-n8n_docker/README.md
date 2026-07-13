# 04 - n8n Docker (Restaurant Chatbot)

```
table for 3 on anni at 8:45 today
Bob tomorrow 17:00 6 customers
make reservation on mina at 22:12 on friday
```

This folder contains a scaffold for the Restaurant chatbot assignment with n8n webhook integration.

Contents
- `restaurant_db.py` — SQLite helpers and `reservations` table
- `restaurant_chatbot.py` — Minimal Gradio chatbot that classifies intents, stores reservations, and fires an n8n webhook
- `docker-compose.yml` — Run n8n locally via Docker
- `.env.example` — Example environment variables

Quick start

1. Create a `.env` file in this folder and edit values (do not commit secrets):

```bash
# Create a file named .env in this folder and set the values below.
# Example (fill in real values; do not commit):
# N8N_WEBHOOK_URL=http://localhost:5678/webhook/restaurant
# OPENAI_API_KEY=your_openai_api_key_here
```

2. Start n8n (in this folder):

```bash
# with docker-compose
docker compose up -d
# or: docker run -p 5678:5678 n8nio/n8n
```

3. Run the chatbot (in a Python environment with dependencies):

```bash
pip install -r requirements.txt
python restaurant_chatbot.py
```

4. Build an n8n workflow:
   - Add a Webhook node with path `restaurant` (POST)
   - Add an IF node checking `{{$json.body.event}} == reservation`
   - Build True/False branches to send notifications (Respond to Webhook, Gmail, Telegram, Twilio)

Testing without n8n

You can test the webhook delivery with curl:

```bash
curl -X POST http://localhost:5678/webhook/restaurant \
  -H "Content-Type: application/json" \
  -d '{"event":"reservation","customer_name":"Alex","date":"2026-06-20","time":"20:00","party_size":3,"id":1}'
```

Notes
- The chatbot uses OpenAI if `OPENAI_API_KEY` is set and `openai` is installed; otherwise it falls back to simple keyword heuristics.
- The n8n webhook URL must match `N8N_WEBHOOK_URL` in `.env`.
