import os , csv , smtplib
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time


load_dotenv()

email_user = os.getenv("email_user")
email_pass = os.getenv("email_pass")
gemini_api = os.getenv("gemini_api")
gemini_model = os.getenv("gemini_model")

leads = []
with open("lead.csv","r",encoding = "utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        clean_lead = {k.strip() : v.strip() for k,v in row.items()}
        leads.append(clean_lead)


llm = ChatGoogleGenerativeAI(model = gemini_model,google_api_key = gemini_api)

def generate_mail(lead):
    prompt = f"""
    Write a highly personalized cold email.

Details:
Name: {lead["name"]}
Company: {lead["company"]}
Problem: {lead["problem"]}

Rules:
- Output ONLY plain text
- No HTML tags
- No markdown
- No placeholders
- Keep it natural and human
- Max 120 words

Email body only. """

    response = llm.invoke(prompt)
    return response.content 



def html_converter(text):
    html_lines = []
    lines = text.split("\n")

    for line in lines:
        line = line.strip()
        if line:
            html_lines.append(f"<p>{line}</p>")
    html_body = "\n".join(html_lines)

    return f"""
    <html>
    <body>{html_body}</body>
    </html>
    """

def send_mail(to,subject,body):
    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body,"html","UTF-8"))

    try:
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(email_user,email_pass)
        server.sendmail(email_user,to,msg.as_string())
        server.quit()
        print(f"the email is succesfullu sent to : {to}")

    except Exception as e:
        print(f"failed to sent to {to} : {e}")

for lead in leads:
    mail_body = generate_mail(lead)
    html_mail = html_converter(mail_body)
    subject = f"Quick idea for {lead['company']}"
    send_mail(lead["email"],subject,html_mail)
    time.sleep(5)
