import pandas as pd 
import smtplib , os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
df = pd.read_csv("sales_data.csv")

load_dotenv()
user_gmail = os.getenv("gmail_user")
gmail = os.getenv("gmail")
gmail_pass = os.getenv("gmail_pass")




#this will clean the columns names 
df.columns = [col.strip() for col in df.columns]
#this will clean the all values by removing the space 
df = df.map(lambda x: x.lower().strip() if isinstance(x,str) else x)

#calculating the total orders 
total_orders = df["product"].count()
#taking only paid 
df = df[df["status"] == "paid"]
#calculating the revenue
revenue = df["amount"].sum()
total_revenue = f"₹{revenue}"
#grouping the product by the frequency
top_list = df.groupby("product").size()
#finding the most selling product
top_product = top_list.idxmax()

#html template
html_body = f"""
<html>
  <body style="font-family: Arial;">

    <h2>📊 Sales Report Summary</h2>

    <p>Here is your daily business report:</p>

    <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
      <tr style="background-color: #f2f2f2;">
        <th>Metric</th>
        <th>Value</th>
      </tr>

      <tr>
        <td>Total Revenue</td>
        <td>{total_revenue}</td>
      </tr>

      <tr>
        <td>Total Orders</td>
        <td>{total_orders}</td>
      </tr>

      <tr>
        <td>Top Product</td>
        <td>{top_product}</td>
      </tr>

    </table>

    <p style="margin-top: 15px;">Regards,<br>Automation System</p>

  </body>
</html>
"""

#formating the mail
msg = MIMEMultipart()
msg["To"] = user_gmail
msg["From"] = gmail
msg["Subject"] = "Daily Sales Report"
msg.attach(MIMEText(html_body,"html","UTF-8"))

#sending the mail
server = smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login(gmail,gmail_pass)
server.sendmail(gmail,user_gmail,msg.as_string())
server.quit()