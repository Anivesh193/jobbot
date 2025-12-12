# JobBot — Universal Job Finder CLI Tool

**JobBot** is a universal job-search CLI tool that fetches jobs from **Naukri** and **Indeed**.
It supports **any job role**, **any location**, **salary filtering**, **experience filtering**, and sends alerts via **Email** & **WhatsApp**.

---

## Features

* Search jobs by **role** and **location**
* Filter jobs by **salary range** and **experience**
* Filter by **Remote / Hybrid / Onsite** jobs
* Get **alerts via Email and WhatsApp**
* Works with **Naukri** and **Indeed**

---

## Installation

```bash
git clone https://github.com/Anivesh193/jobbot
cd jobbot
pip install .
```

---

## Environment Setup

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Fill in the required fields in `.env`:

* `EMAIL_FROM`
* `EMAIL_PASSWORD`
* WhatsApp API keys (optional)

---

## Usage

Run the JobBot CLI:

```bash
jobbot run
```

You will be prompted to enter the following:

| Prompt                             | Description                   |
| ---------------------------------- | ----------------------------- |
| **Job Role**                       | Example: `python developer`   |
| **Location**                       | Example: `bangalore` or `all` |
| **Salary Range**                   | Example: `3-6` LPA            |
| **Experience**                     | Example: `0-2` years          |
| **Remote / Hybrid / Onsite / All** | Choose work preference        |
| **Alert method**                   | Choose `email` or `whatsapp`  |

---

## Commands

| Command         | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| `jobbot run`    | Starts the interactive job search CLI and prompts for inputs |
| `pip install .` | Installs the JobBot package locally                          |
| `.env`          | Configure your Email and WhatsApp API keys for alerts        |

---

## Example

```bash
jobbot run
```

**Inputs:**

* Job role: python developer
* Location: bangalore
* Salary: 4-8 LPA
* Experience: 0-2 years
* Remote / Hybrid / Onsite: remote
* Alert method: email

JobBot will scrape relevant jobs and send alerts accordingly.

---

## License

MIT





