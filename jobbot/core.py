import os
import re
import json
import logging
from datetime import datetime
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_TO = os.getenv("WHATSAPP_TO")

SEEN_FILE = "seen_jobs.json"

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

# ----------- User selections (global vars) -----------
USER_ROLE = None
USER_LOCATION = None
USER_SALARY = None
USER_EXP = None
USER_JOBTYPE = None
USER_ALERT = None


# -----------------------------------------------------
def load_seen():
    try:
        return set(json.load(open(SEEN_FILE)))
    except:
        return set()


def save_seen(data):
    json.dump(list(data), open(SEEN_FILE, "w"))


def fetch(url):
    try:
        r = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9",
        })
        r.raise_for_status()
        return r.text
    except:
        return ""


def parse_salary_to_lpa(text):
    if not text:
        return None
    text = text.replace("₹", "")
    nums = re.findall(r"[\d,]+", text)
    if not nums:
        return None
    vals = [float(n.replace(",", "")) for n in nums]
    avg = sum(vals) / len(vals)
    if avg > 100000:
        return avg / 100000
    if avg > 1000:
        return avg * 12 / 100000
    return avg


def matches_salary(lpa):
    try:
        mn, mx = map(float, USER_SALARY.split("-"))
        return lpa and mn <= lpa <= mx
    except:
        return False


def matches_exp(text):
    try:
        mn, mx = map(int, USER_EXP.split("-"))
        for y in range(mn, mx + 1):
            if str(y) in text:
                return True
        if "fresher" in text.lower():
            return True
        return False
    except:
        return False


def matches_remote(text):
    t = text.lower()
    jt = USER_JOBTYPE.lower()
    if jt == "all":
        return True
    if jt == "remote" and "remote" in t:
        return True
    if jt == "hybrid" and "hybrid" in t:
        return True
    if jt == "onsite" and ("remote" not in t and "hybrid" not in t):
        return True
    return False


# -----------------------------------------------------
# Naukri Scraper
# -----------------------------------------------------
def scrape_naukri():
    url = f"https://www.naukri.com/{quote_plus(USER_ROLE)}-jobs"
    html = fetch(url)
    soup = BeautifulSoup(html, "lxml")

    jobs = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "job-listings" not in href:
            continue

        title = a.text.strip()
        parent = a.find_parent()
        body = parent.get_text(" ") if parent else title

        if not matches_exp(body): continue
        if not matches_remote(body): continue

        salary_match = re.search(r"₹[\d,]+.*", body)
        salary = salary_match.group(0) if salary_match else ""
        lpa = parse_salary_to_lpa(salary)
        if not matches_salary(lpa): continue

        jobs.append({
            "id": "naukri_" + href[-12:],
            "title": title,
            "company": "Unknown",
            "salary": salary,
            "salary_lpa": lpa,
            "location": USER_LOCATION,
            "type": USER_JOBTYPE,
            "url": href,
            "source": "Naukri"
        })
    return jobs


# -----------------------------------------------------
# Indeed Scraper
# -----------------------------------------------------
def scrape_indeed():
    url = f"https://www.indeed.co.in/jobs?q={quote_plus(USER_ROLE)}"
    html = fetch(url)
    soup = BeautifulSoup(html, "lxml")

    jobs = []
    for card in soup.find_all("a", href=True):
        href = card["href"]
        if not href.startswith("/"):
            continue

        title = card.text.strip()
        parent = card.find_parent()
        body = parent.get_text(" ") if parent else title

        if not matches_exp(body): continue
        if not matches_remote(body): continue

        salary_match = re.search(r"₹[\d,]+.*", body)
        salary = salary_match.group(0) if salary_match else ""
        lpa = parse_salary_to_lpa(salary)
        if not matches_salary(lpa): continue

        jobs.append({
            "id": "indeed_" + href[-20:].replace("/", ""),
            "title": title,
            "company": "Unknown",
            "salary": salary,
            "salary_lpa": lpa,
            "location": USER_LOCATION,
            "type": USER_JOBTYPE,
            "url": "https://www.indeed.co.in" + href,
            "source": "Indeed"
        })
    return jobs


# -----------------------------------------------------
# Email Sender
# -----------------------------------------------------
def send_email(subject, html):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg.attach(MIMEText(html, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        server.quit()
        logging.info("Email sent!")
    except Exception as e:
        logging.error("Email failed: %s", e)


# -----------------------------------------------------
# WhatsApp API Sender
# -----------------------------------------------------
def send_whatsapp(text):
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_NUMBER_ID:
        return

    url = f"https://graph.facebook.com/v19.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": WHATSAPP_TO,
        "type": "text",
        "text": { "body": text }
    }
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10)
        logging.info("WhatsApp alert sent!")
    except Exception as e:
        logging.error("WhatsApp failed: %s", e)


# -----------------------------------------------------
# Main Controller
# -----------------------------------------------------
def main():
    seen = load_seen()

    jobs = scrape_naukri() + scrape_indeed()

    new_jobs = [j for j in jobs if j["id"] not in seen]

    for j in new_jobs:
        seen.add(j["id"])
    save_seen(seen)

    if USER_ALERT in ["email", "both"]:
        html = "<h2>Your Job Results</h2>"
        for j in new_jobs:
            html += f"<p>{j['title']} - {j['company']} - {j['salary']}<br>{j['url']}</p>"
        send_email(f"{len(new_jobs)} new {USER_ROLE} jobs found", html)

    if USER_ALERT in ["whatsapp", "both"]:
        send_whatsapp(f"{len(new_jobs)} new {USER_ROLE} jobs found!")



# -----------------------------------------------------
# Entry point from CLI
# -----------------------------------------------------
def run_bot(job_role, location, salary_range, exp_range, job_type, alert_method):
    global USER_ROLE, USER_LOCATION, USER_SALARY, USER_EXP, USER_JOBTYPE, USER_ALERT

    USER_ROLE = job_role
    USER_LOCATION = location
    USER_SALARY = salary_range
    USER_EXP = exp_range
    USER_JOBTYPE = job_type
    USER_ALERT = alert_method

    main()
