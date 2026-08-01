# Task 4 — AI Chatbot Assistant + n8n

Restaurant AI Agent with n8n notifications.  
Book tables, cancel reservations, answer menu/hours questions, and send events to an **n8n** workflow.

Built with **Python**, **Gradio**, **SQLite**, **OpenAI**, **Docker**, and **n8n**.

Based on [Assignment 4 — Restaurant Agent + n8n](https://pythonai200425.github.io/finals/04-n8n-restaurant.html).

---

## Features

- Natural-language reservation booking
- LLM extraction of: `customer_name`, `date`, `time`, `party_size`, `contact`
- Soft-delete cancellation by booking ID (`status = 'cancelled'`)
- SQLite `reservations` table
- Intent classifier: `reservation` | `cancellation` | `menu` | `hours` | `general`
- OpenAI classification with keyword fallback
- Webhook notifications on **booking and cancellation**
- n8n workflow: Webhook → IF (by `event`) → two notification branches
- Telegram notifications (bonus)
- Gradio web chat UI

---

## Project Structure

```text
04-n8n_docker/
├── reservation_chatbot_app.py  # Classifier, handlers, Gradio UI, _notify_n8n
├── chatbot_db.py               # initialize_database, book/cancel/get helpers
├── n8n_workflow.json           # Importable n8n workflow
├── docker-compose.yml          # Local n8n via Docker
├── requirements.txt
├── .env.example                # Environment template (no secrets)
├── .gitignore
├── README.md
└── screenshots/                # Demo screenshots
```

> `.env` and `restaurant.db` are created locally and ignored by Git.

---

## Requirements

- Python 3.10+
- Docker Desktop (for n8n)
- OpenAI API key

---

## Setup

### 1. Install dependencies

```powershell
pip install -r requirements.txt
```

### 2. Configure environment

```powershell
copy .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=sk-your-openai-key-here
OPENAI_MODEL=gpt-4o-mini
N8N_WEBHOOK_URL=http://localhost:5678/webhook/restaurant
RESTAURANT_DB=restaurant.db
```

**Do not commit `.env`.**

---

## Run n8n

```powershell
docker compose up -d
```

1. Open [http://localhost:5678](http://localhost:5678)
2. Import `n8n_workflow.json`
3. Activate / publish the workflow

Webhook used by the chatbot:

```text
POST http://localhost:5678/webhook/restaurant
```

n8n flow:

1. **Webhook** node — method `POST`, path `restaurant`
2. **IF** node — splits on `event == reservation`
3. **Two branches** — different messages for reservation vs cancellation
4. **Respond to Webhook** (+ Telegram as bonus)

---

## Run the Chatbot

```powershell
python reservation_chatbot_app.py
```

Open: [http://127.0.0.1:7860](http://127.0.0.1:7860)

### Example messages

```text
Order table for Lina at 19:55 tonight for 4
Cancel reservation number 42
What do you have for dessert?
What time are you open?
```

---

## How It Works

1. User sends a message in Gradio  
2. `classify_question()` routes to: `reservation` / `cancellation` / `menu` / `hours` / `general`  
3. `_handle_reservation()` extracts details (LLM → JSON) and validates required fields  
4. `book_reservation()` (in `chatbot_db.py`) saves to SQLite and returns the booking ID  
5. `_notify_n8n(data, event="reservation")` POSTs JSON to n8n  
6. For cancellations: extract booking ID → `cancel_reservation()` → `_notify_n8n(..., event="cancellation")`  
7. n8n IF node routes by `event` and sends the matching notification  

### Reservation payload example

```json
{
  "event": "reservation",
  "id": 42,
  "customer_name": "Lina",
  "date": "2026-08-01",
  "time": "19:55",
  "party_size": 4
}
```

Cancellation uses the same webhook with `"event": "cancellation"`.

---

## Test the Webhook (PowerShell)

**Reservation**

```powershell
$body = '{"event":"reservation","customer_name":"Stav","date":"2026-08-01","time":"19:30","party_size":4,"id":102}'
Invoke-WebRequest -Uri "http://localhost:5678/webhook/restaurant" -Method POST -ContentType "application/json" -Body $body
```

**Cancellation**

```powershell
$body = '{"event":"cancellation","id":102}'
Invoke-WebRequest -Uri "http://localhost:5678/webhook/restaurant" -Method POST -ContentType "application/json" -Body $body
```

---

## Grading Criteria (40 pts)

### Part 1 — Python (25)

| Criterion | Points |
|-----------|--------|
| `reservations` table added to DB | 5 |
| `book_reservation()` and `cancel_reservation()` | 5 |
| Classifier routes `reservation` / `cancellation` | 5 |
| LLM extracts name / date / time / party size | 5 |
| Webhook fired on booking **and** cancellation | 5 |

### Part 2 — n8n (15)

| Criterion | Points |
|-----------|--------|
| Webhook node configured and receiving data | 5 |
| IF node splits reservation vs cancellation | 5 |
| Different notification message for each branch | 5 |

### Bonus

| Criterion | Points |
|-----------|--------|
| Gmail / Telegram / Twilio (real notification) | +5 |

---

## Screenshots

### Gradio Chat Interface

![Gradio order_cancel](https://github.com/user-attachments/assets/29f5d156-8658-4291-919d-b2238775243d)

![Terminal](https://github.com/user-attachments/assets/212cc857-8977-4718-ac73-a7c87aff3da0)

### n8n Workflow

![n8n notification workflow](https://github.com/user-attachments/assets/bdc0d55d-e3c2-408a-9301-0cb6baa310ea)

![n8n order](https://github.com/user-attachments/assets/77553e80-2ce6-4ca2-895f-bacad42e581c)

![n8n cancel](https://github.com/user-attachments/assets/afef9c2f-94ba-49a3-80f4-f639d8b7097b)

![DB](https://github.com/user-attachments/assets/a8560451-8292-4458-9832-94a3cd126430)

![Telegram](https://github.com/user-attachments/assets/791a6ea5-9138-41b0-8cad-9a174871a5e1)

---

## Security Notes

- Keep API keys only in `.env`
- `.gitignore` excludes: `.env`, `env`, `*.db`, `__pycache__/`, `.venv/`, logs, n8n runtime data
- Use `.env.example` as a safe template
