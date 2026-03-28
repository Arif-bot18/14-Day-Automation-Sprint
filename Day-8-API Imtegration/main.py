from openai import OpenAI
import os , re , csv , json
from dotenv import load_dotenv
from fastapi import FastAPI , Request
from pydantic import BaseModel
app = FastAPI()

load_dotenv()

client = OpenAI(api_key = os.getenv("GROQ_API_KEY"),base_url="https://api.groq.com/openai/v1")

def rule_based_classifier(message):
    message = message.lower()

    # --- Budget-based ---
    if "$" in message or "budget" in message or "₹" in message:
        match = re.search(r"\d+", message)
        
        if match:
            amount = int(match.group())

            if amount > 3000:
                return {
                    "priority": "High Value",
                    "reason": f"Budget is {amount}, which is greater than 3000"
                }

            elif 1000 <= amount <= 3000:
                return {
                    "priority": "Medium Value",
                    "reason": f"Budget is {amount}, which is between 1000 and 3000"
                }

            else:
                return {
                    "priority": "Low Value",
                    "reason": f"Budget is {amount}, which is less than 1000"
                }

    # --- Intent-based ---
    if "urgent" in message or "asap" in message:
        return {
            "priority": "High Value",
            "reason": "Urgent intent detected (urgent/asap)"
        }

    if "just exploring" in message or "checking" in message:
        return {
            "priority": "Low Value",
            "reason": "Low intent detected (just exploring/checking)"
        }

    # --- Fallback ---
    return None

def llm_based_classifier(message):
    response = client.responses.create(input=f"""You are a sales assistant categorize lead into : High Value, Medium Value, Low Value, Based on budget urgency the lead is {message} give the output like this 
    Return output ONLY in this format: {{"priority": "High Value / Medium Value / Low Value", "reason": "short explanation"}} follow the output format strictly """,
    model = os.getenv("model"))

    return response.output_text


def parser_llm_model(description):
    priority = None
    reason =None
    try:
        data = json.loads(description)
        data = {key.lower() : value for key ,value in data.items()}
        priority = data.get("priority")
        reason = data.get("reason")

    except Exception:
        priority_match = re.search(r"(category|priority)\s*:\s*(.+)",description,re.IGNORECASE)
        if priority_match:
            priority = priority_match.group(2).strip()
        reason_match = re.search(r"(reason)\s*:\s*(.+)",description,re.IGNORECASE)
        if reason_match:
            reason = reason_match.group(2).strip()

    if priority:
        priority = priority.lower().strip()
        if "high" in priority:
            priority = "High Value"
        elif "medium" in priority:
            priority = "Medium Value"
        elif "low" in priority:
            priority = "Low Value"
        else :
            priority = "Medium Value"
    else:
        priority = "Medium Value"

    if not reason:
        reason = "No reason provided"
    return priority,reason

class Format_schema(BaseModel):
    name:str
    email:str 
    message: str 


@app.post("/analyze-lead")
def analyze_lead(package:Format_schema):
    name = package.name
    email = package.email
    message = package.message
    description = rule_based_classifier(message)
    if description:
        priority = description["priority"]
        reason = description["reason"]
    else:
        try:
            llm_output = llm_based_classifier(message)
            priority,reason = parser_llm_model(llm_output)
        except:
            priority = "Medium Value"
            reason = "LLM Failed"


    with open("priority_leads.csv","a",newline = "") as f:
        writer = csv.writer(f)
        writer.writerow([name,email,message,priority,reason])

    return {"message":"thank you"}
