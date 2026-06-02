import os
import json
import re
import requests
from dotenv import load_dotenv

load_dotenv()

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class RestaurantChatbot:
    """Restaurant chatbot with reservation and cancellation handling (LangChain version)."""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or os.getenv("RESTAURANT_DB", "restaurant.db")
        self.n8n_webhook = os.getenv("N8N_WEBHOOK_URL")
        
        # LangChain LLM setup
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        self.llm = None
        if self.openai_key:
            try:
                self.llm = ChatOpenAI(
                    model=self.openai_model,
                    temperature=0,
                    api_key=self.openai_key
                )
            except Exception:
                self.llm = None

        # Initialize database
        from restaurant_db import initialize_database
        initialize_database(self.db_path)

    def classify_question(self, question: str) -> str:
        """Use LLM to classify user intent (LangChain style)."""
        if not self.llm:
            # Fallback keyword classification
            q = (question or "").lower()
            if any(w in q for w in ["book", "reserve", "reservation", "table"]):
                return "reservation"
            if any(w in q for w in ["cancel", "cancellation"]):
                return "cancellation"
            if any(w in q for w in ["menu", "price", "dish"]):
                return "menu"
            if any(w in q for w in ["open", "hours", "location"]):
                return "hours"
            return "general"

        classify_prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a router for a restaurant chatbot. "
                "Classify the user message into exactly one of these categories:\n"
                "reservation — user wants to book a table\n"
                "cancellation — user wants to cancel an existing booking\n"
                "menu — questions about food, drinks, or prices\n"
                "hours — questions about opening hours or location\n"
                "general — anything else\n"
                "Return ONLY the single category word. No punctuation, no explanation."
            ),
            ("human", "{question}")
        ])

        chain = classify_prompt | self.llm | StrOutputParser()
        result = chain.invoke({"question": question}).strip().lower()
        
        valid = {"reservation", "cancellation", "menu", "hours", "general"}
        return result if result in valid else "general"

    def _notify_n8n(self, data: dict, event: str) -> None:
        """Fire-and-forget webhook to n8n. Never crashes the chatbot."""
        webhook_url = os.getenv("N8N_WEBHOOK_URL")
        if not webhook_url:
            return
        try:
            requests.post(
                webhook_url,
                json={**data, "event": event},
                timeout=5
            )
        except Exception:
            pass  # n8n being down should not crash the chatbot

    def _handle_reservation(self, question: str) -> str:
        # Ask the LLM to extract structured data from the user's message
        extract_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "Extract reservation details from the message. "
             "Return ONLY valid JSON with keys: "
             "customer_name, date, time, party_size, contact. "
             "Use null for missing fields. No explanation."),
            ("human", "{question}")
        ])

        if not self.llm:
            return "Please call us directly to make a reservation!"

        chain = extract_prompt | self.llm | StrOutputParser()
        raw = chain.invoke({"question": question})

        try:
            details = json.loads(raw)
            required = ["customer_name", "date", "time", "party_size"]
            if not all(details.get(k) for k in required):
                return ("I need your name, date, time, and party size. "
                        "Example: 'Table for 2 on Friday at 7pm, name is Sara'")

            from restaurant_db import book_reservation
            res_id = book_reservation(
                self.db_path,
                details["customer_name"], details["date"],
                str(details["time"]), int(details["party_size"]),
                details.get("contact")
            )
            self._notify_n8n({**details, "id": res_id}, event="reservation")

            return (f"✅ Reservation confirmed!\n"
                    f"Name: {details['customer_name']}\n"
                    f"Date: {details['date']} at {details['time']}\n"
                    f"Party of {details['party_size']} · Booking #{res_id}")
        except (json.JSONDecodeError, ValueError):
            return "Sorry, I couldn't process that. Please try again."

    def _handle_cancellation(self, question: str) -> str:
        # Simple: ask the user for their booking ID
        # (For the bonus: use LLM to extract booking ID from the message)
        import re
        match = re.search(r'\b(\d+)\b', question)
        if match:
            res_id = int(match.group(1))
            from restaurant_db import cancel_reservation
            cancel_reservation(self.db_path, res_id)
            self._notify_n8n({"id": res_id}, event="cancellation")
            return f"Reservation #{res_id} has been cancelled."
        return "Please provide your booking ID number to cancel."

    def answer(self, message: str) -> str:
        intent = self.classify_question(message)
        if intent == 'reservation':
            return self._handle_reservation(message)
        if intent == 'cancellation':
            return self._handle_cancellation(message)
        if intent == 'menu':
            return "We serve seasonal dishes. Ask about a specific dish or price."
        if intent == 'hours':
            return "We're open Tue-Sun 11:00-22:00. Closed Mon."
        return "Sorry, I can help with reservations, cancellations, menu and hours."


if __name__ == '__main__':
    import gradio as gr

    bot = RestaurantChatbot()

    def answer_fn(message, history):
        return bot.answer(message)

    demo = gr.ChatInterface(
        fn=answer_fn,
        chatbot=gr.Chatbot(),
        textbox=gr.Textbox(placeholder="Ask about reservations or menu..."),
        title="Restaurant Chatbot with n8n webhook",
    )

    demo.launch()