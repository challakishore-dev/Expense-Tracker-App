
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
sns.set(style="whitegrid")

np.random.seed(42)
rows = 500
categories = ['Food','Travel','Rent','Shopping','Bills','Entertainment','Health','Education']
payments = ['Cash','UPI','Card','NetBanking']
start = datetime(2025,1,1)

records=[]
for _ in range(rows):
    date = start + timedelta(days=int(np.random.randint(0,365)))
    cat = np.random.choice(categories, p=[0.18,0.12,0.2,0.12,0.14,0.1,0.08,0.06])
    amt = int(np.random.randint(100,12000) if cat=='Rent' else np.random.randint(50,4000))
    pay = np.random.choice(payments)
    records.append([date,cat,amt,pay])

df=pd.DataFrame(records,columns=['Date','Category','Amount','Payment'])
df['Date']=pd.to_datetime(df['Date'])
df['Month']=df['Date'].dt.strftime('%b')
df.to_csv('data/expenses.csv',index=False)

summary = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
print("Top categories:\n", summary)

plt.figure(figsize=(11,6))
sns.barplot(x=summary.index,y=summary.values)
plt.xticks(rotation=30, ha='right')
plt.title("Category Wise Spending")
plt.tight_layout()
plt.savefig("outputs/category_spending.png")
plt.close()

monthly=df.groupby(df['Date'].dt.month)['Amount'].sum()
plt.figure(figsize=(11,6))
monthly.plot(marker='o')
plt.title("Monthly Spending Trend")
plt.xlabel("Month")
plt.ylabel("Amount")
plt.tight_layout()
plt.savefig("outputs/monthly_trend.png")
plt.close()

pie=df.groupby('Category')['Amount'].sum()
plt.figure(figsize=(8,8))
plt.pie(pie.values, labels=pie.index, autopct='%1.1f%%', startangle=140)
plt.title("Expense Distribution")
plt.tight_layout()
plt.savefig("outputs/distribution.png")
plt.close()

budget=50000
month_totals=df.groupby(df['Date'].dt.month)['Amount'].sum()
alerts = month_totals[month_totals>budget]
with open("outputs/insights.txt","w") as f:
    f.write("Highest spending category: %s\n" % summary.idxmax())
    f.write("Months over budget:\n")
    for m,v in alerts.items():
        f.write(f"Month {m}: {v}\n")
print("Done. Check outputs folder.")
