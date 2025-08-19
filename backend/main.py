from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import csv
import os
import httpx
from fastapi.responses import StreamingResponse
import google.generativeai as genai
from pymongo import MongoClient
from bson import ObjectId
from rapidfuzz import fuzz
# Email imports
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GREETINGS = ["hi", "hello", "hey","Hlo","greetings"]


GOV_KEYWORDS = [
    # Identity & Core Documents
    "passport", "voter id", "ration card", "aadhaar", "e-aadhaar", "election card",
    "voter list", "gazette notification", "identity card", "pan card",
    
    # Certificates
    "birth certificate", "death certificate", "income certificate", "caste certificate",
    "domicile certificate", "nativity certificate", "residence certificate", "community certificate",
    "minority certificate", "character certificate", "marriage certificate", "divorce certificate",
    "disability certificate", "migration certificate", "obc certificate", "creamy layer certificate",
    "medical certificate", "encumbrance certificate", "fair value certificate",
    
    # Property & Land Records
    "land record", "property tax", "land tax", "land registration", "survey number", "mutation",
    "building permit", "occupancy certificate", "house tax",
    
    # Transport & Vehicle
    "license", "licence", "driving licence", "driving license", "vehicle registration", "rc book",
    "motor vehicle tax", "pollution certificate", "fitness certificate", "road tax", "transport permit",
    
    # Utilities & Bills
    "utility", "bill", "water bill", "electricity bill", "kseb", "gas connection", "telephone bill",
    
    # Schemes & Welfare
    "scheme", "pension", "widow pension", "old age pension", "disability pension", "scholarship",
    "student loan subsidy", "agriculture subsidy", "housing scheme", "employment scheme", "welfare fund",
    "kudumbashree", "karunya scheme", "ayushman bharat", "insurance card",
    
    # Municipality / Panchayat Services
    "government service", "public service", "municipality", "panchayat", "trade license",
    "shop license", "birth registration", "death registration", "building approval",
    "sanitation services", "water connection",
    
    # General
    "govt", "government", "permit", "social security",
    
    # Kerala-specific portals & services
    "akshaya", "sevana", "sanchaya", "relis", "edistrict", "ksrtc"
]


# Load CSV into memory at startup
CSV_DATA = []
def load_csv():
    import re
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gov_services.csv')
    if not os.path.exists(csv_path):
        csv_path = os.path.join(os.path.dirname(__file__), 'gov_services.csv')
    if not os.path.exists(csv_path):
        return []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]
CSV_DATA = load_csv()

def find_service_info(user_message):
    import re
    best_score = 0
    best_row = None
    for row in CSV_DATA:
        service = row['service_name'].lower()
        service_main = re.sub(r'\b(application|registration|download|get|apply|for|the|a|an|of)\b', '', service).strip()
        # Fuzzy match: compare service_main to user_message
        score = fuzz.partial_ratio(service_main, user_message)
        if score > best_score:
            best_score = score
            best_row = row
    # Return the best match if score is high enough
    if best_score > 80:
        return best_row
    return None

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["kerala_services"]
complaints_collection = db["complaints"]

@app.post("/register_complaint")
async def register_complaint(request: Request):
    try:
        data = await request.json()
        # Extract fields
        name = data.get("name", "")
        contact = data.get("contact", "")
        service = data.get("service", "")
        complaint_text = data.get("complaint_text", "")
        email = data.get("email", "")  # New field for user's email
        if not complaint_text or not service:
            return {"success": False, "message": "Service and complaint text are required."}
        complaint_doc = {
            "name": name,
            "contact": contact,
            "service": service,
            "complaint_text": complaint_text,
            "email": email  # Store user's email in MongoDB
        }
        result = complaints_collection.insert_one(complaint_doc)
        complaint_id = str(result.inserted_id)

        # Email mapping for departments
        department_emails = {
            "voter id": "hariusha200@gmail.com",
            "birth certificate": "hari.internzenturiotech@gmail.com"
        }
        # Find the email for the service (case-insensitive match)
        service_key = service.strip().lower()
        recipient_email = department_emails.get(service_key)
        if recipient_email:
            # Prepare email using SendGrid API (free tier allows 100 emails/day)
            sender_email = os.getenv("SENDER_EMAIL", "haribro00123@gmail.com")
            subject = f"New Complaint Registered: {service}"
            body = f"""
A new complaint has been registered for the service: {service}

Name: {name}
Contact: {contact}
Email: {email}
Complaint: {complaint_text}
Complaint ID: {complaint_id}
"""
            
            try:
                sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
                
                if not sendgrid_api_key:
                    print("SENDGRID_API_KEY environment variable is not set.")
                    raise ValueError("SENDGRID_API_KEY environment variable is required")
                
                print(f"Attempting to send email to: {recipient_email} from: {sender_email}")
                
                # Create SendGrid message
                from_email = Email(sender_email)
                to_email = To(recipient_email)
                content = Content("text/plain", body)
                mail = Mail(from_email, to_email, subject, content)
                
                # Add reply-to header if user provided email
                if email:
                    mail.reply_to = Email(email)
                
                # Send email via SendGrid
                sg = SendGridAPIClient(sendgrid_api_key)
                response = sg.send(mail)
                
                try:
                    response = sg.send(mail)
                    print(f"Email sent successfully via SendGrid with status code: {response.status_code}")
                    print(f"Email response body: {response.body}")
                    print(f"Email response headers: {response.headers}")
                except Exception as e:
                    print(f"Error sending email to department: {e}")
                # Send a copy to the user if they provided their email
                if email:
                    try:
                        user_subject = f"Copy of Your Complaint Registration: {service}"
                        user_body = f"""
Dear {name},

Thank you for registering your complaint regarding: {service}.

Here are the details you submitted:

Name: {name}
Contact: {contact}
Complaint: {complaint_text}
Complaint ID: {complaint_id}

We have forwarded your complaint to the respective department. You will be contacted if further information is required.

Best regards,
Kerala Services Bot
"""
                        user_mail = Mail(from_email, To(email), user_subject, Content("text/plain", user_body))
                        print(f"Attempting to send copy to user at: {email}")
                        sg.send(user_mail)
                        print(f"Copy sent to user at {email}")
                    except Exception as user_email_err:
                        print(f"Failed to send copy to user: {user_email_err}")
            except Exception as email_err:
                print(f"Failed to send email: {email_err}")
                # Optionally, log this error somewhere

        return {"success": True, "message": "Complaint registered successfully.", "complaint_id": complaint_id}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

@app.post("/track_complaint")
async def track_complaint(request: Request):
    try:
        data = await request.json()
        complaint_id = data.get("complaint_id")
        contact = data.get("contact")
        query = None
        if complaint_id:
            try:
                query = {"_id": ObjectId(complaint_id)}
            except Exception:
                return {"success": False, "message": "Invalid complaint ID format."}
        elif contact:
            query = {"contact": contact}
        else:
            return {"success": False, "message": "Provide complaint ID or contact info."}
        complaint = complaints_collection.find_one(query)
        if complaint:
            complaint["_id"] = str(complaint["_id"])
            return {"success": True, "complaint": complaint}
        else:
            return {"success": False, "message": "Complaint not found."}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

@app.post("/ask")
async def ask_bot(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "").lower()
        is_web = request.headers.get("x-frontend", "").lower() == "web"

        if not message:
            if is_web:
                return {"reply": "Message cannot be empty."}
            def error_stream():
                yield "Message cannot be empty."
            return StreamingResponse(error_stream(), media_type="text/plain")

        if any(greet in message for greet in GREETINGS):
            if is_web:
                return {"reply": "Hello! Please ask about a government service."}
            def greet_stream():
                yield "Hello! Please ask about a government service."
            return StreamingResponse(greet_stream(), media_type="text/plain")

        if not any(keyword in message for keyword in GOV_KEYWORDS):
            if is_web:
                return {"reply": "Sorry, I can only help with government services. Please ask about a government service."}
            def keyword_stream():
                yield "Sorry, I can only help with government services. Please ask about a government service."
            return StreamingResponse(keyword_stream(), media_type="text/plain")

        service_info = find_service_info(message)
        context = ""
        if service_info:
            context = f"Service: {service_info['service_name']}\nDescription: {service_info['description']}\nDepartment: {service_info['department']}\nProcessing Time: {service_info['processing_time']}\nRequired Documents: {service_info['required_documents']}\nFees: {service_info['fees']}\nContact Info: {service_info['contact_info']}\nLinks: {service_info['relevant_links']}\nHow to Apply: {service_info['how_to_apply']}\nOfficial Portal: {service_info['official_portal']}"

        # ollama_url = "http://localhost:11434/api/chat"
        if context:
            system_prompt = (
                "You are a helpful assistant for government services in Kerala, India. "
                "Use the following official service data to answer the user's question. "
                "If the answer is not in the data, you may use your own knowledge. "
                "If you use your own knowledge, mention this clearly in your answer (e.g., 'Based on my general knowledge...'). "
                "Format your answer using Markdown for headings, bold, and bullet points where appropriate. Do not use triple hashes (###) for headings; use single or double # for headings instead.\n"
                + context
            )
        else:
            system_prompt = (
                "You are a helpful assistant for government services in Kerala, India. "
                "If you know the answer about Kerala government services, answer it. "
                "If the user asks about services outside Kerala, politely refuse or redirect them to Kerala-specific information. For any other topic, politely refuse. "
                "If you use your own knowledge, mention this clearly in your answer (e.g., 'Based on my general knowledge...'). "
                "Format your answer using Markdown for headings, bold, and bullet points where appropriate. Do not use triple hashes (###) for headings; use single or double # for headings instead."
            )
        # payload = {
        #     "model": "qwen:1.8b",
        #     "messages": [
        #         {"role": "system", "content": system_prompt},
        #         {"role": "user", "content": message}
        #     ]
        # }

        # Gemini API integration
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('models/gemini-2.5-pro')
        prompt = system_prompt + "\nUser: " + message

        def stream_gemini():
            try:
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    # Handle multi-part responses
                    if hasattr(chunk, 'parts') and chunk.parts:
                        for part in chunk.parts:
                            if hasattr(part, 'text') and part.text:
                                yield part.text
                    elif hasattr(chunk, 'text') and chunk.text:
                        yield chunk.text
            except Exception as e:
                yield f"[ERROR] {e}"

        if is_web:
            # For web, collect full reply as before
            full_reply = ""
            for chunk in stream_gemini():
                full_reply += chunk
            if not full_reply:
                full_reply = "Sorry, I couldn't get a response from Gemini."
            return {"reply": full_reply}
        else:
            # For Telegram, stream the reply
            return StreamingResponse(stream_gemini(), media_type="text/plain")

    except Exception as e:
        print(f"[ERROR] {e}")
        if request.headers.get("x-frontend", "").lower() == "web":
            return {"reply": "Something went wrong while talking to the LLM."}
        def error_stream():
            yield "Something went wrong while talking to the LLM."
        return StreamingResponse(error_stream(), media_type="text/plain")
