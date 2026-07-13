import os
import re
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from restaurant_db import (
    initialize_database,
    book_reservation,
    cancel_reservation,
    get_reservation_by_id,
    get_reservations,
)


env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(env_path)


class RestaurantChatbot:
    def __init__(self):
        db_name = os.getenv("RESTAURANT_DB", "restaurant.db")
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_name)
        initialize_database(self.db_path)

        api_key = os.getenv("OPENAI_API_KEY")
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        if api_key and api_key != "your-api-key-here" and api_key.startswith("sk-"):
            try:
                self.llm = ChatOpenAI(model=model_name, temperature=0, api_key=api_key)
                print(f"✅ OpenAI API key loaded successfully (Model: {model_name})")
            except Exception as e:
                print(f"❌ Error initializing OpenAI: {e}")
                self.llm = None
        else:
            print("⚠️  No valid OPENAI_API_KEY found. Using keyword-based fallback.")
            self.llm = None

    def classify_question(self, question: str) -> str:
        question_lower = question.lower()
        if any(kw in question_lower for kw in ["book", "reserve", "reservation", "table for", "table", "order table", "booking"]):
            return "reservation"
        elif any(kw in question_lower for kw in ["cancel", "cancellation", "remove reservation"]):
            return "cancellation"
        elif any(kw in question_lower for kw in ["menu", "food", "eat", "dish", "drink", "dessert", "price", "have"]):
            return "menu"
        elif any(kw in question_lower for kw in ["open", "close", "hours", "time", "when", "schedule"]):
            return "hours"
        
        if self.llm:
            try:
                classify_prompt = ChatPromptTemplate.from_messages([
                    ("system", "Classify into: reservation, cancellation, menu, hours, general. Return ONLY the word."),
                    ("human", "{question}")
                ])
                result = (classify_prompt | self.llm | StrOutputParser()).invoke({"question": question}).strip().lower()
                return result if result in {"reservation", "cancellation", "menu", "hours", "general"} else "general"
            except Exception:
                pass
        return "general"

    def answer(self, question: str) -> str:
        category = self.classify_question(question)
        print(f" Classified as: {category}")

        if category == "reservation": return self._handle_reservation(question)
        elif category == "cancellation": return self._handle_cancellation(question)
        elif category == "menu": return self._handle_menu(question)
        elif category == "hours": return self._handle_hours(question)
        else: return self._handle_general(question)

    def _handle_reservation(self, question: str) -> str:
        if self.llm:
            try:
                return self._extract_with_llm(question)
            except Exception as e:
                print(f"❌ LLM extraction failed: {e}")
        return self._extract_reservation_keywords(question)

    def _extract_with_llm(self, question: str) -> str:
        
        current_real_date = datetime.now().strftime("%Y-%m-%d")
        
        extract_prompt = ChatPromptTemplate.from_messages([
            ("system", f"Today's actual date is {current_real_date}. Extract reservation details. Return ONLY valid JSON with keys: customer_name, date, time, party_size, contact. Use null for missing fields. For date, resolve 'today', 'tonight', or 'tomorrow' to YYYY-MM-DD format relative to today."),
            ("human", "{question}")
        ])
        raw = (extract_prompt | self.llm | StrOutputParser()).invoke({"question": question})
        details = json.loads(raw)
        return self._process_reservation(details)

    def _extract_reservation_keywords(self, question: str) -> str:
        """Extract reservation details using regex (no LLM needed)."""
        print(f" Extracting from: '{question}'")
        
        # 1. Extract party size
        party_match = re.search(r'for\s+(\d+)\s*(people|person|guests|ppl)?', question, re.IGNORECASE)
        if not party_match:
            party_match = re.search(r'(\d+)\s*(people|person|guests|ppl)', question, re.IGNORECASE)
        party_size = int(party_match.group(1)) if party_match else 2
        print(f"  👥 Party size: {party_size}")
        
        # 2. Extract time
        time_match = re.search(r'\bat\s+(\d{1,2}[:.]\d{2}(?:\s*(?:am|pm))?)\b', question, re.IGNORECASE)
        if not time_match:
            time_match = re.search(r'\bat\s+(\d{1,2}(?:\s*(?:am|pm)))\b', question, re.IGNORECASE)
        time_str = time_match.group(1).strip() if time_match else None
        print(f"  🕐 Time: {time_str}")
        
        date_str = None
        question_lower = question.lower()
        
        if "today" in question_lower or "tonight" in question_lower:
            date_str = datetime.now().strftime("%Y-%m-%d")
        elif "tomorrow" in question_lower:
            date_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        else:
            date_match = re.search(r'(monday|tuesday|wednesday|thursday|friday|saturday|sunday)', question_lower)
            if date_match:
                date_str = date_match.group(1).capitalize()
            else:
                date_match = re.search(r'(\d{1,2}[./-]\d{1,2}(?:[./-]\d{2,4})?)', question)
                if date_match:
                    date_str = date_match.group(1)
        print(f"  📅 Date: {date_str}")
        
        # 4. Extract name
        customer_name = "Guest"
        name_match = re.search(r'(?:my name is|name is|name:|i am|i\'m)\s*([A-Za-z]+)', question, re.IGNORECASE)
        if name_match:
            customer_name = name_match.group(1).capitalize()
            print(f"  👤 Name (explicit): {customer_name}")
        else:
            cleaned_q = re.sub(r'for\s+\d+\s*(people|person|guests|ppl)?', '', question, flags=re.IGNORECASE)
            name_match = re.search(r'\bfor\s+([a-zA-Z]+)\b', cleaned_q)
            if name_match:
                customer_name = name_match.group(1).capitalize()
                print(f"  👤 Name (from 'for'): {customer_name}")
            else:
                name_match = re.search(r'\b([A-Z][a-z]+)\'s\b', question)
                if name_match:
                    customer_name = name_match.group(1)
                    print(f"  👤 Name (possessive): {customer_name}")
        
        if not time_str:
            return "Please provide the time for your reservation (e.g., '19:55' or '7 PM')."
        if not date_str:
            return "Please provide the date for your reservation (e.g., 'today', 'tonight', 'tomorrow')."
        
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
            return "I need your name, date, time, and party size. Example: 'Table for 2 tonight at 19:55, name is Sara'"

        try:
            res_id = book_reservation(
                self.db_path, details["customer_name"], details["date"],
                str(details["time"]), int(details["party_size"]), details.get("contact")
            )
            print(f"✅ Reservation saved to DB with ID: {res_id}")
            
            self._notify_n8n({
                "id": res_id,
                "customer_name": details["customer_name"],
                "date": details["date"],
                "time": details["time"],
                "party_size": details["party_size"],
                "contact": details.get("contact"),
                "message": f"🎉 NEW RESERVATION: {details['customer_name']} booked a table for {details['party_size']} on {details['date']} at {details['time']}"
            }, event="reservation")
            
            return (
                f"✅ Reservation confirmed!\n"
                f"Name: {details['customer_name']}\n"
                f"Date: {details['date']} at {details['time']}\n"
                f"Party of {details['party_size']} · Booking #{res_id}"
            )
        except Exception as e:
            print(f"❌ Database error: {e}")
            return "Sorry, there was an error processing your reservation."

    def _handle_cancellation(self, question: str) -> str:
        print(f" Processing cancellation: '{question}'")
        match = re.search(r'\b(\d+)\b', question)
        if match:
            res_id = int(match.group(1))
            print(f"  🆔 Found reservation ID: {res_id}")
            
            reservation = get_reservation_by_id(self.db_path, res_id)
            if not reservation:
                print(f"  ❌ Reservation #{res_id} not found in DB")
                return f"❌ Reservation #{res_id} not found in our database."
            
            print(f"  ✅ Found reservation: {reservation['customer_name']} on {reservation['date']}")
            
            if reservation['status'] == 'cancelled':
                print(f"  ⚠️ Reservation #{res_id} already cancelled")
                return f"⚠️ Reservation #{res_id} is already cancelled."
            
            print(f"  🔄 Attempting to cancel reservation #{res_id}...")
            success = cancel_reservation(self.db_path, res_id)
            print(f"  📝 Cancel DB result: {success}")
            
            if success:
                print(f"  ✅ Reservation #{res_id} successfully cancelled in DB")
                self._notify_n8n({
                    "id": res_id,
                    "customer_name": reservation['customer_name'],
                    "date": reservation['date'],
                    "time": reservation['time'],
                    "party_size": reservation['party_size'],
                    "message": f"❌ CANCELLATION: {reservation['customer_name']}'s reservation for {reservation['date']} at {reservation['time']} has been CANCELLED"
                }, event="cancellation")
                return f"✅ Reservation #{res_id} has been successfully cancelled."
            else:
                print(f"  ❌ Failed to cancel reservation #{res_id}")
                return f"❌ Failed to cancel reservation #{res_id}."
        
        print("  ⚠️ No reservation ID found in message")
        return "Please provide your booking ID number to cancel (e.g., 'Cancel reservation 5')."

    def _handle_menu(self, question: str) -> str:
        if not self.llm: return "Our menu includes pasta, pizza, salads, and desserts. Prices range from $10-$30."
        prompt = ChatPromptTemplate.from_messages([("system", "You are a helpful restaurant assistant. Answer menu questions briefly."), ("human", "{question}")])
        return (prompt | self.llm | StrOutputParser()).invoke({"question": question})

    def _handle_hours(self, question: str) -> str:
        if not self.llm: return "We are open Sunday–Thursday 12:00–23:00, Friday–Saturday 12:00–01:00."
        prompt = ChatPromptTemplate.from_messages([("system", "You are a helpful restaurant assistant. Answer hours/location questions briefly."), ("human", "{question}")])
        return (prompt | self.llm | StrOutputParser()).invoke({"question": question})

    def _handle_general(self, question: str) -> str:
        if not self.llm: return "Welcome to our restaurant! How can I help you today?"
        prompt = ChatPromptTemplate.from_messages([("system", "You are a helpful restaurant assistant."), ("human", "{question}")])
        return (prompt | self.llm | StrOutputParser()).invoke({"question": question})

    def _notify_n8n(self, data: dict, event: str) -> None:
        webhook_url = os.getenv("N8N_WEBHOOK_URL")
        if not webhook_url:
            print("⚠️  No N8N_WEBHOOK_URL configured in .env")
            return
        try:
            print(f"📤 Sending webhook to n8n: {webhook_url}")
            print(f"   Event: {event}, Data: {data}")
            response = requests.post(webhook_url, json=data, timeout=5)
            print(f"✅ n8n notification sent: {response.status_code}")
        except Exception as e:
            print(f"❌ n8n notification failed: {e}")


if __name__ == "__main__":
    import gradio as gr
    bot = RestaurantChatbot()
    def respond(message, history): return bot.answer(message)
    demo = gr.ChatInterface(
        fn=respond,
        title="🍽️ Restaurant Reservation Assistant",
        description="Book tables, cancel reservations, or ask about our menu and hours",
        examples=[
            "Order table for Lina at 19:55 tonight for 4",
            "Cancel reservation number 5",
            "What do you have for dessert?",
        ],
    )
    demo.launch()
