# 🚀 TrustScore — MVP

> Your life is your credit score. For 190 million unbanked Indians.

---

## 🌐 Live Demo

👉 https://trustproof1.netlify.app/

---

## Video

👉https://drive.google.com/file/d/1I2EhasrB1vdVxKiMEbh4O_HrCuAlHS3D/view?usp=drive_link


## ⚠️ MVP Note

This project is a **Minimum Viable Product (MVP)** built for demonstration purposes.
The deployed version showcases the **frontend experience**, while the backend (FastAPI), ML scoring logic, and database schema are included in this repository for completeness and future integration.

---

## 📌 Problem Statement

Millions of people lack access to formal credit systems due to the absence of traditional financial history. Despite being financially responsible in daily life, they remain invisible to banks.

---

## 💡 Solution

**TrustScore** provides an alternative credit scoring system using real-life behavioral signals such as:

* Electricity bill payments
* UPI transaction activity
* Mobile recharge consistency
* Community trust (vouching)

---

## 🏗️ Project Structure

```
trustscore/
├── backend/
│   ├── main.py           # FastAPI app — API routes
│   └── requirements.txt
├── ml/
│   ├── __init__.py
│   └── scorer.py         # Scoring engine
├── db/
│   └── schema.sql        # Database schema
├── frontend/
│   └── index.html        # MVP website (deployed)
└── render.yaml           # Backend deployment config
```

---

## ⚙️ How It Works

1. User enters lifestyle-based financial inputs
2. System processes inputs using scoring logic
3. TrustScore is generated instantly
4. Loan eligibility is displayed

---

## 🧠 Scoring Model

The scoring engine (`ml/scorer.py`) uses weighted signals:

| Signal                       | Weight |
| ---------------------------- | ------ |
| Electricity bill consistency | 28%    |
| UPI transaction frequency    | 22%    |
| Mobile recharge consistency  | 18%    |
| SHG membership               | 17%    |
| Community vouches            | 15%    |

Score range: **300 – 900**

---

## 🔗 API Endpoints (Backend)

| Method | Path         | Description          |
| ------ | ------------ | -------------------- |
| GET    | `/health`    | Check service status |
| POST   | `/score`     | Compute TrustScore   |
| GET    | `/user/{id}` | Fetch user profile   |
| POST   | `/vouch`     | Submit vouch         |

---

## 🚀 Future Enhancements

* Deploy backend using cloud platform
* Integrate real-time APIs
* AI/ML model improvements
* Mobile application

---

## 👥 Team Contributions

* Aakshaya V - **Frontend:** UI/UX and user experience
* Amrita S - **Backend:** API and logic handling
* Sre Harshini T - **ML Model:** Scoring algorithm
* Trishna G - **Database:** Schema design and setup

---

## ⚠️ Disclaimer

This is a **hackathon prototype** and not a real financial service.
No sensitive user data is collected or stored.

---

⭐ *Thank you for reviewing our project!*

