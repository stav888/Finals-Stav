# Task 4: AI Chatbot Assistant

An AI-powered restaurant reservation chatbot built with Python, Gradio, SQLite, OpenAI, Docker, and n8n. The assistant can answer restaurant questions, create reservations, cancel bookings, and send reservation events to an n8n workflow.

## Features

- Natural-language reservation requests
- Reservation details extraction: name, date, time, party size, and contact
- Opening-hours validation before saving a booking
- SQLite storage for reservations
- Reservation cancellation by booking ID
- Menu and opening-hours responses
- OpenAI classification with a keyword-based fallback
- n8n webhook notifications for reservations and cancellations
- Gradio web chat interface

## Project Structure

```text
04-n8n_docker/
├── restaurant_chatbot.py   # Chatbot logic and Gradio interface
├── restaurant_db.py        # SQLite database functions
├── restaurant.db           # Local reservation database
├── n8n_workflow.json       # Importable n8n workflow
├── docker-compose.yml      # n8n Docker configuration
├── requirements.txt        # Python dependencies
├── env                     # Local environment variables
└── README.md
```

## Requirements

- Python 3.10 or newer
- Docker Desktop, for running n8n
- An OpenAI API key

## Installation

Install the Python dependencies:

```powershell
pip install -r requirements.txt
```

Create or edit the local `env` file:

```env
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini
N8N_WEBHOOK_URL=http://localhost:5678/webhook/restaurant
RESTAURANT_DB=restaurant.db
```

The `env` file contains secrets and should not be committed.

## Run n8n

Start the n8n container:

```powershell
docker compose up -d
```

Open n8n at [http://localhost:5678](http://localhost:5678), import `n8n_workflow.json`, and publish or activate the workflow.

The webhook endpoint used by the chatbot is:

```text
POST http://localhost:5678/webhook/restaurant
```

## Run the Chatbot

From the task directory, run:

```powershell
python restaurant_chatbot.py
```

Open the Gradio interface at [http://127.0.0.1:7860](http://127.0.0.1:7860).

Example messages:

```text
Order table for Lina at 19:55 tonight for 4
Cancel reservation number 42
What do you have for dessert?
What time are you open?
```

Clicking an example fills the message box. Press **Enter** or click **Submit** to send it.

## How It Works

1. The user sends a message through the Gradio chat interface.
2. The chatbot classifies the request as a reservation, cancellation, menu, hours, or general question.
3. Reservation details are extracted and validated.
4. Valid reservations are saved to SQLite and assigned a booking ID.
5. The chatbot sends a JSON event to the n8n webhook.
6. n8n routes the event and sends the configured notification.

Reservation event example:

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

Cancellation events use the same webhook with `"event": "cancellation"`.

## Testing the Webhook

Reservation test:

```powershell
$body = '{"event":"reservation","customer_name":"Stav","date":"2026-08-01","time":"19:30","party_size":4,"contact":"050-1234567","id":102}'
Invoke-WebRequest -Uri "http://localhost:5678/webhook/restaurant" -Method POST -ContentType "application/json" -Body $body
```

Cancellation test:

```powershell
$body = '{"event":"cancellation","id":102}'
Invoke-WebRequest -Uri "http://localhost:5678/webhook/restaurant" -Method POST -ContentType "application/json" -Body $body
```

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

## Security and Local Files

The task `.gitignore` excludes the local environment file, SQLite databases, Gradio logs, Python caches, and n8n runtime data. Keep API keys and webhook credentials in `env` only.
