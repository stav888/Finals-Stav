import os
import re
import json
import requests
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# FIXED IMPORT: Added get_reservation_by_id
from restaurant_db import (
    initialize_database,
    book_reservation,
    cancel_reservation,
    get_reservation_by_id,
    get_reservations,
)

load_dotenv()


class RestaurantChatbot:
    def __init__(self):
        self.db_path = "restaurant.db"
        initialize_database(self.db_path)

        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your-api-key-here":
            try:
                self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)
                print("✅ OpenAI API key loaded successfully")
            except Exception as e:
                print(f"❌ Error initializing OpenAI: {e}")
                self.llm = None
        else:
            print("⚠️  No valid OPENAI_API_KEY found. Using keyword-based classification.")
            self.llm = None

    # ──────────────────── Classifier ───────────────────
    def classify_question(self, question: str) -> str:
        """Classify intent using LLM if available, otherwise use keywords."""
        question_lower = question.lower()
        
        reservation_keywords = ["book", "reserve", "reservation", "table for", "table", "booking"]
        cancellation_keywords = ["cancel", "cancellation", "remove reservation"]
        menu_keywords = ["menu", "food", "eat", "dish", "drink", "dessert", "price", "have"]
        hours_keywords = ["open", "close", "hours", "time", "when", "schedule"]
        
        if any(kw in question_lower for kw in reservation_keywords):
            return "reservation"
        elif any(kw in question_lower for kw in cancellation_keywords):
            return "cancellation"
        elif any(kw in question_lower for kw in menu_keywords):
            return "menu"
        elif any(kw in question_lower for kw in hours_keywords):
            return "hours"
        
        if self.llm:
            try:
                classify_prompt = ChatPromptTemplate.from_messages([
                    ("system", "Classify the user message into one category: reservation, cancellation, menu, hours, or general. Return ONLY the category word."),
                    ("human", "{question}")
                ])
                chain = classify_prompt | self.llm | StrOutputParser()
                result = chain.invoke({"question": question}).strip().lower()
                valid = {"reservation", "cancellation", "menu", "hours", "general"}
                return result if result in valid else "general"
            except Exception as e:
                print(f"❌ LLM classification error: {e}")
        
        return "general"

    # ─────────────────── Main router ──────────────────
    def answer(self, question: str) -> str:
        category = self.classify_question(question)
        print(f"📋 Classified as: {category}")

        if category == "reservation":
            return self._handle_reservation(question)
        elif category == "cancellation":
            return self._handle_cancellation(question)
        elif category == "menu":
            return self._handle_menu(question)
        elif category == "hours":
            return self._handle_hours(question)
        else:
            return self._handle_general(question)

    # ──────────────────── Reservation Handler ────────────────────
    def _handle_reservation(self, question: str) -> str:
        if self.llm:
            return self._extract_with_llm(question)
        return self._extract_reservation_keywords(question)

    def _extract_with_llm(self, question: str) -> str:
        extract_prompt = ChatPromptTemplate.from_messages([
            ("system", "Extract reservation details. Return ONLY valid JSON with keys: customer_name, date, time, party_size, contact. Use null for missing fields."),
            ("human", "{question}")
        ])
        try:
            chain = extract_prompt | self.llm | StrOutputParser()
            raw = chain.invoke({"question": question})
            details = json.loads(raw)
            return self._process_reservation(details)
        except Exception as e:
            print(f"❌ LLM extraction error: {e}")
            return self._extract_reservation_keywords(question)

    def _extract_reservation_keywords(self, question: str) -> str:
        """Extract reservation details using regex (no LLM needed)."""
        # 1. Extract party size
        party_match = re.search(r'for\s+(\d+)\s*(people|person|guests|ppl)?', question, re.IGNORECASE)
        if not party_match:
            party_match = re.search(r'(\d+)\s*(people|person|guests|ppl)', question, re.IGNORECASE)
        party_size = int(party_match.group(1)) if party_match else 2
        
        # 2. Extract time
        time_match = re.search(r'at\s+(\d{1,2}(?:[:.]\d{0,2})?\s*(?:am|pm)?)', question, re.IGNORECASE)
        if not time_match:
            time_match = re.search(r'(\d{1,2}(?:[:.]\d{1,2})?\s*(?:am|pm))', question, re.IGNORECASE)
        time_str = time_match.group(1).strip() if time_match else None
        
        # 3. Extract date
        date_str = None
        question_lower = question.lower()
        if "today" in question_lower:
            date_str = "today"
        elif "tomorrow" in question_lower:
            date_str = "tomorrow"
        else:
            date_match = re.search(r'(monday|tuesday|wednesday|thursday|friday|saturday|sunday)', question_lower)
            if date_match:
                date_str = date_match.group(1)
            else:
                date_match = re.search(r'(\d{1,2}[./-]\d{1,2}(?:[./-]\d{2,4})?)', question)
                if date_match:
                    date_str = date_match.group(1)
        
        # 4. Extract name (Improved)
        customer_name = "Guest"
        # Try explicit indicators first
        name_match = re.search(r'(?:my name is|name is|name:)\s*([A-Za-z]+)', question, re.IGNORECASE)
        if name_match:
            customer_name = name_match.group(1).capitalize()
        else:
            # Remove "for X people" to avoid confusing numbers with names
            cleaned_q = re.sub(r'for\s+\d+\s*(people|person|guests|ppl)?', '', question, flags=re.IGNORECASE)
            # Look for "for [Name]"
            name_match = re.search(r'\bfor\s+([a-zA-Z]+)\b', cleaned_q)
            if name_match:
                customer_name = name_match.group(1).capitalize()
        
        if not time_str:
            return "Please provide the time for your reservation (e.g., '7 PM' or '19:00')."
        if not date_str:
            return "Please provide the date for your reservation (e.g., 'today', 'tomorrow', or day of week)."
        
        details = {
            "customer_name": customer_name,
            "date": date_str,
            "time": time_str,
            "party_size": party_size,
            "contact": None
        }
        
        return self._process_reservation(details)

    def _process_reservation(self, details: dict) -> str:
        required = ["customer_name", "date", "time", "party_size"]
        if not all(details.get(k) for k in required):
            return "I need your name, date, time, and party size. Example: 'Table for 2 on Friday at 7pm, name is Sara'"

        try:
            res_id = book_reservation(
                self.db_path, details["customer_name"], details["date"],
                str(details["time"]), int(details["party_size"]), details.get("contact")
            )
            self._notify_n8n({**details, "id": res_id}, event="reservation")
            return (
                f"✅ Reservation confirmed!\n"
                f"Name: {details['customer_name']}\n"
                f"Date: {details['date']} at {details['time']}\n"
                f"Party of {details['party_size']} · Booking #{res_id}"
            )
        except Exception as e:
            print(f"❌ Database error: {e}")
            return "Sorry, there was an error processing your reservation."

    # ─────────────────── Cancellation Handler (FIXED) ────────────────────
    def _handle_cancellation(self, question: str) -> str:
        """Extract booking ID and cancel the reservation efficiently."""
        match = re.search(r'\b(\d+)\b', question)
        if match:
            res_id = int(match.group(1))
            
            # Efficiently fetch ONLY this specific reservation
            reservation = get_reservation_by_id(self.db_path, res_id)
            
            if not reservation:
                return f"❌ Reservation #{res_id} not found in our database."
            
            if reservation['status'] == 'cancelled':
                return f"⚠️ Reservation #{res_id} is already cancelled."
            
            # Actually update the database
            success = cancel_reservation(self.db_path, res_id)
            
            if success:
                self._notify_n8n({"id": res_id, "customer_name": reservation['customer_name']}, event="cancellation")
                return f"✅ Reservation #{res_id} has been successfully cancelled."
            else:
                return f"❌ Failed to cancel reservation #{res_id}."
        
        return "Please provide your booking ID number to cancel (e.g., 'Cancel reservation 5')."

    # ──────────────────── Menu / Hours / General ───────────────────
    def _handle_menu(self, question: str) -> str:
        if not self.llm:
            return "Our menu includes pasta, pizza, salads, and desserts. Prices range from $10-$30."
        prompt = ChatPromptTemplate.from_messages([("system", "You are a helpful restaurant assistant. Answer menu questions briefly."), ("human", "{question}")])
        return (prompt | self.llm | StrOutputParser()).invoke({"question": question})

    def _handle_hours(self, question: str) -> str:
        if not self.llm:
            return "We are open Sunday–Thursday 12:00–23:00, Friday–Saturday 12:00–01:00."
        prompt = ChatPromptTemplate.from_messages([("system", "You are a helpful restaurant assistant. Answer hours/location questions briefly."), ("human", "{question}")])
        return (prompt | self.llm | StrOutputParser()).invoke({"question": question})

    def _handle_general(self, question: str) -> str:
        if not self.llm:
            return "Welcome to our restaurant! How can I help you today? You can book a table, cancel a reservation, or ask about our menu and hours."
        prompt = ChatPromptTemplate.from_messages([("system", "You are a helpful restaurant assistant."), ("human", "{question}")])
        return (prompt | self.llm | StrOutputParser()).invoke({"question": question})

    # ──────────────────── n8n Webhook ───────────────────
    def _notify_n8n(self, data: dict, event: str) -> None:
        webhook_url = os.getenv("N8N_WEBHOOK_URL")
        if not webhook_url:
            print("⚠️  No N8N_WEBHOOK_URL configured")
            return
        try:
            response = requests.post(webhook_url, json={**data, "event": event}, timeout=5)
            print(f"✅ n8n notification sent: {response.status_code}")
        except Exception as e:
            print(f"❌ n8n notification failed: {e}")


# ──────────────────── Gradio UI ───────────────────
if __name__ == "__main__":
    import gradio as gr

    bot = RestaurantChatbot()

    def respond(message, history):
        return bot.answer(message)

    demo = gr.ChatInterface(
        fn=respond,
        title="🍽️ Restaurant Reservation Assistant",
        description="Book tables, cancel reservations, or ask about our menu and hours",
        examples=[
            "I want to book a table for 4 people tomorrow at 7 PM, name is John",
            "Cancel reservation number 5",
            "What do you have for dessert?",
            "What time do you close on Friday?",
        ],
    )

    demo.launch()