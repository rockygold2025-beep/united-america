# United Bank of America — Online Banking Platform

Professional US digital banking web application (Flask + SQLAlchemy).

## Brand
- **Name:** United Bank of America
- **Support email:** unitedbankofamericasupport@gmail.com
- **Currency:** USD ($)
- **Deposit insurance messaging:** FDIC up to $250,000
- **HQ (display):** 120 Broadway, New York, NY 10271

## Deploy on Render (free)

1. Push this folder to GitHub.
2. Create a new **Web Service** on [render.com](https://render.com).
3. Build: `pip install -r requirements.txt`
4. Start: `gunicorn backend:app --bind 0.0.0.0:$PORT`
5. Set environment variables:
   - `SECRET_KEY` = long random string
   - `FLASK_ENV` = `production`
   - `DATABASE_URL` = your Postgres URL (Supabase free tier recommended)

### Cold starts on free tier
Render free services sleep after ~15 minutes of no traffic. This project includes:
- A **branded loading overlay** on first visit after idle
- A **soft keep-alive** ping every 12 minutes while a tab is open

For near-always-on on free budget, use a free uptime monitor (e.g. UptimeRobot, cron-job.org) to HIT your URL every 10–14 minutes.

## Domain name suggestions

Best professional options:
1. **unitedbankofamerica.com** (premium; check availability)
2. **ubamerica.bank** (if .bank eligibility)
3. **ubaonline.com**
4. **unitedbankusa.com**
5. **myubabank.com**
6. **ubadigital.com**

### Cheap domains that work well for Nigeria / Africa users
Buy from registrars that support Naira or low USD fees:
- **Namecheap** — frequent promo codes, easy DNS for Render
- **Porkbun** — often cheapest .com / .ng
- **NameSilo** — low renewal prices
- **Whogohost** / **QServers** (Nigeria) — local payment (Naira), good for `.com.ng` / `.ng`
- **HostAfrica** / **Truehost** — regional

Recommended budget path:
1. Buy **ubaonline.com** or **unitedbankusa.com** on Porkbun/Namecheap (~$8–12/yr)
2. Or **uba.com.ng** via Whogohost if you want a Nigerian ccTLD
3. Point DNS A/CNAME to Render (Render provides free SSL)

## Default admin (first boot)
- Username: `bankmanager`
- Password: `Bankmanager@2026`
- PIN: `123456`

Change these immediately after first login.

## Local run
```bash
pip install -r requirements.txt
python run.py
```
