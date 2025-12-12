# JobBot — Universal Job Finder CLI Tool

JobBot is a universal job-search CLI tool that fetches jobs from Naukri & Indeed.
It supports ANY job role, ANY location, salary filtering, experience filtering,
and sends alerts via Email & WhatsApp.

---

## Installation

git clone https://github.com/YOURNAME/jobbot
cd jobbot
pip install .

yaml
Copy code

---

## Environment setup

Copy `.env.example`:

cp .env.example .env

yaml
Copy code

Fill the fields:

- EMAIL_FROM  
- EMAIL_PASSWORD  
- WHATSAPP API keys (optional)

---

## Usage

jobbot run

yaml
Copy code

You'll be asked:

- Job Role  
- Location  
- Salary Range  
- Experience  
- Remote / Hybrid / Onsite  
- Email / WhatsApp alerts  

---

## Example

jobbot run
Job role: python developer
Location: bangalore
Salary: 4-8
Experience: 0-2
Remote / Hybrid / Onsite / All: remote
Alert method: email

yaml
Copy code

JobBot will scrape data and send alerts.

---

## License
MIT
