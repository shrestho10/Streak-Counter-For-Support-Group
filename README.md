# Streak-Counter-For-Support-Group


This project tracks **daily posting streaks** in the NewMe support group and sends **Twilio SMS reminders** to members who post on **2+ consecutive days**.  

Members are encouraged to keep their streak alive — if they skip a day, their streak resets, and they can start again anytime.

---

## ✨ Features
- Tracks posting activity from `log.csv` (chat history).
- Uses `users.csv` for user → phone number mapping.
- Detects **streaks of consecutive days** based on chat logs.
- Sends personalized SMS via [Twilio](https://www.twilio.com/) every day at **12:01 AM**:
  ```
  Congratulations! You have a X-day streak with your NewMe support group. 
  Post again today to continue your streak!
  ```
- Runs continuously using the [`schedule`](https://pypi.org/project/schedule/) library (no cron required).
- Automatically resets streaks if a day is skipped.

---

## 📂 File Structure
```
├── log.csv        # Chat log file (timestamp, user, message, intent, response)
├── users.csv      # User → phone number mapping (user, phonenumber)
├── streaks.py     # Main script (streak detection + Twilio messaging)
└── README.md      # Project description
```

### Example `log.csv`
| timestamp           | user   | message                 | intent | response |
|---------------------|--------|-------------------------|--------|----------|
| 2025-09-29 08:12:00 | alice  | I’m feeling motivated!  | share  | ...      |
| 2025-09-30 09:45:00 | alice  | Another good day!       | share  | ...      |
| 2025-10-01 14:02:00 | bob    | Struggling a little...  | share  | ...      |

### Example `users.csv`
| user   | phonenumber |
|--------|-------------|
| alice  | number  |
| bob    | number  |

---

## ⚙️ Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/shrestho10/Streak-Counter-For-Support-Group.git
   cd Streak-Counter-For-Support-Group
   ```

2. Install dependencies:
   ```bash
   pip install pandas twilio schedule
   ```

3. Configure Twilio credentials in `streaks.py`:
   ```python
   ACCOUNT_SID = "your_twilio_sid"
   AUTH_TOKEN  = "your_twilio_auth"
   FROM_PHONE  = "+1XXXXXXXXXX"  # your Twilio number
   ```


4. Run the script:
   ```bash
   python streaks.py
   ```

The script will keep running and automatically check at **00:01 AM daily**.  

---

## 🕒 Scheduling & Timezones
- By default, the script runs based on **server local time**.  
- If users are in different timezones, add a `timezone` column in `users.csv` and adjust timestamps accordingly.

---

## 📬 Example SMS
```
Congratulations! You have a 3-day streak with your NewMe support group. 
Post again today to continue your streak!
```

---

## 🚀 Future Improvements
- Add per-user timezone support.
- Persist streaks in a database instead of recalculating from CSV each day.


