import csv
running_total = 0 
high_value_client = [ ]
with open("transaction.csv") as f:
    data = csv.DictReader(f)
    for row in data:
        row["amount"] = float(row["amount"])
        if row["status"].strip() == "paid":
            running_total  += row["amount"]
            if row["amount"] >= 1500:
                high_value_client.append(row["client_name"])
print(running_total)
print(high_value_client)     
net_profit =( running_total*0.8)-((running_total*0.8)*0.20)
print(net_profit)
with open("audit_summary.csv","w") as f:
    f.write(f"--- BUSINESS ADUIT ---\n")
    f.write(f"Total Net Profit: {net_profit}\n")
    f.write(f'HIGH VALUE CLIENT: {", ".join(high_value_client)}')
