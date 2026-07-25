# Assignment 4 - Restaurant Agent + n8n

Restaurant chatbot that supports table reservations and cancellations.  
Data is stored in SQLite and real-time notifications are sent to Telegram through an n8n workflow.

## Project Structure

```text
04-n8n_docker/
├─ restaurant_chatbot.py      # Chatbot logic, intent classification, LLM extraction
├─ restaurant_db.py           # SQLite functions (book / cancel / get reservations)
├─ restaurant.db              # SQLite database
├─ n8n_workflow.json          # n8n workflow (Webhook + IF + Telegram)
├─ docker-compose.yml         # n8n Docker setup
├─ requirements.txt
├─ env                        # Environment variables
└── README.md
```

## Setup

### 1. Python environment

```bash
pip install -r requirements.txt
```

### 2. Environment variables

Create / edit the `env` file:

```env
OPENAI_API_KEY=your_openai_key
N8N_WEBHOOK_URL=http://localhost:5678/webhook/restaurant
```

### 3. Start n8n (Docker)

```bash
docker-compose up -d
```

Then open http://localhost:5678 and import `n8n_workflow.json`.  
Make sure the workflow is **Published**.

### 4. Run the chatbot

```bash
python restaurant_chatbot.py
```

## How it works

1. User sends a natural language message (reservation or cancellation)
2. Chatbot classifies the intent using LLM
3. Relevant data is extracted and saved to SQLite
4. A webhook is sent to n8n
5. n8n sends a formatted Telegram notification

## n8n Workflow

- **Webhook** - `POST /restaurant`
- **IF** node - splits by `event` (`reservation` / `cancellation`)
- **Telegram** - different messages for each case
- **Respond to Webhook** - returns confirmation

## Testing the Webhook

**New Reservation:**
```powershell
$body = '{"event":"reservation","customer_name":"Stav","date":"2026-07-26","time":"19:30","party_size":4,"contact":"050-1234567","id":102}'
Invoke-WebRequest -Uri "http://localhost:5678/webhook/restaurant" -Method POST -ContentType "application/json" -Body $body
```

**Cancellation:**
```powershell
$body = '{"event":"cancellation","id":102}'
Invoke-WebRequest -Uri "http://localhost:5678/webhook/restaurant" -Method POST -ContentType "application/json" -Body $body
```

## Notes

- Telegram Bot Token and Chat ID are configured inside the n8n workflow.
- The chatbot uses fire-and-forget for the webhook (does not crash if n8n is down).
- Database file: `restaurant.db`
