from twilio.rest import Client
import pandas as pd
from datetime import datetime, timedelta
import schedule
import time

# -----------------------------
# Twilio credentials
# -----------------------------
ACCOUNT_SID =  ""
AUTH_TOKEN =  ""
FROM_PHONE =  '' 



client = Client(ACCOUNT_SID, AUTH_TOKEN)


# Function to calculate streaks & send texts

def send_streak_texts():
    print("Running streak check at", datetime.now())

    # Load CSVs
    logs = pd.read_csv("log.csv", parse_dates=["timestamp"])
    users = pd.read_csv("users.csv")

    # Filter out chatbot messages
    logs = logs[logs["user"] != "newme"]
    logs["date"] = logs["timestamp"].dt.date

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    streaks = {}

    # Calculate streaks for each user
    for user, df in logs.groupby("user"):
        dates = sorted(set(df["date"]))
        streak = 0
        last_date = None

        for d in dates:
            if last_date is None:
                streak = 1
            elif (d - last_date).days == 1:  # consecutive day
                streak += 1
            elif (d - last_date).days > 1:  # streak broken
                streak = 1
            last_date = d

        # If user posted yesterday, and streak >= 2 → send message
        if yesterday in dates and streak >= 2:
            streaks[user] = streak

    # Send Twilio messages
    for user, streak in streaks.items():
        try:
            phone = str(users.loc[users["user"] == user, "phonenumber"].values[0])
            if not phone.startswith("+1"):
                phone = "+1" + phone

            message = (
                f"Congratulations! You have a {streak}-day streak with your NewMe support group. "
                f"Post again today to continue your streak!"
            )

            client.messages.create(to=phone, from_=FROM_PHONE, body=message)
            print(f"✅ Sent to {user} ({phone}): {message}")

        except Exception as e:
            print(f"⚠️ Failed to send to {user}: {e}")

# -----------------------------
# Schedule job daily at 00:01
# -----------------------------
schedule.every().day.at("00:01").do(send_streak_texts)

print("Scheduler started. Waiting for 00:01 daily job...")

while True:
    schedule.run_pending()
    time.sleep(30)  # avoid high CPU usage


#This scheduling can be easily done with cron job scheduling, for making this straight forward in the code we have just made the code run all the time.