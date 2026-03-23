import pandas as pd 
import smtplib
from email.meme.multipart import MEMEMultipart
from email.meme.text import MEMEText
df = pd.read_csv("sales_data.csv")

#this will clean the columns names 
df.columns = [col.strip() for col in df.columns]
#this will clean the all values by removing the space 
df = df.map(lambda x: x.lower().strip() if isinstance(x,str) else x)
print(df)
total_orders = df["product"].count()

df = df[df["status"] == "paid"]

revenue = df["amount"].sum()

total_revenue = f"₹{revenue}"

top = df.groupby("product").size()

top_product = top.idxmax()
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

print(html_body)