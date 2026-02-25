# University Schedule System (Backend)

## 📌 About the Project
This project implements an **alternative schedule system** for a university.  
It is built with a **microservices architecture**, focusing on scalability, security, and extensibility.  

The frontend was developed separately and is not included in this repository.  
This repo contains only the **backend services**.

Key features:
- **Microservices architecture** with API Gateway.
- **JWT-based authentication** with access & refresh tokens.
- **Session management** and blacklisted token storage in Redis.
- **Secure password storage** using hashing with salt.
- **PostgreSQL** for schedule and authentication data.
- **MongoDB** for user profile and preferences.
- **Automatic schedule updates** from official ICS feeds.

---

## 🏗 Architecture Overview

### Components
- **API Gateway** (FastAPI) – single entry point, routing & logging.
- **Auth Service** – login, signup, token verification.
- **Redis** – blacklist of revoked tokens (fast in-memory checks).
- **PostgreSQL**:
  - Schedule database (normalized + recursive group tree).
  - Password storage for users.
- **Schedule Service** – provides schedule data (CRUD operations).
- **Update Service** – fetches and updates schedule from `.ics` files.
- **User Data Service** – stores user profiles and preferences (MongoDB).
- **MongoDB** – flexible document model for favorites, history, UI settings.

### Data Flow
1. User logs in → Auth Service issues **access & refresh tokens**.
2. API Gateway routes requests, validates tokens (checks Redis blacklist).
3. Schedule Service queries Postgres for events.
4. Update Service regularly fetches new `.ics` files, calculates hashes to detect changes, updates DB.
5. User Data Service (Mongo) stores user’s favorites, theme, history.

### Security
- Passwords hashed with `passlib`.
- JWT tokens with expiration.
- Refresh tokens (2 weeks) + Access tokens (2h).
- Session management: up to 5 active devices.
- Token revocation handled by Redis.

A more detailed description of the project is available in this document: [ProjectM.pdf](https://github.com/HobbitTheCat/MarauderMap/blob/main/ProjectM.pdf)

---

## 🚀 Installation & Running

### Requirements
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL, MongoDB, Redis

### Quick Start
It is worth noting that to start, it is necessary to create and fill in .env files.

```bash
git clone https://github.com/HobbitTheCat/MarauderMap
cd university-schedule-backend
docker-compose up --build
```

### This will start:
- API Gateway
- Auth Service
- Schedule Service
- Update Service
- User Service
- Redis, PostgreSQL, MongoDB, PgAdmin
- Cloudflare Tunnel

---

## 📖 Example API Endpoints
- `POST /api/v1/user/auth/signup` — register a new user
- `POST /api/v1/user/auth/signin` — login and receive tokens
- `POST /api/v1/user/auth/refresh` — refresh tokens
- `GET /api/v1/schedule/week?date=2025-02-20&group=MI4-FC` — get weekly schedule for group
- `GET /api/v1/user` — fetch user profile data

---

## ⚠️ Current Limitations
- No frontend included (backend only).
- Performance issues
- Notification service not yet implemented.

---

## 📈 Future Improvements
- Add notification service (Firebase push).
- Integrate SMTP server for 2FA.
- Rewrite critical modules in Rust for performance.
- Optimize API Gateway (migrate to Nginx + caching).
- Possible switch to event-driven architecture for decoupling services.

---
## Model Frontend Figma 
https://www.figma.com/proto/G2IlpxAks7ZCxRYwY0FsBf/Projet?node-id=0-1&t=yeDIh4InE8ceAOK8-1

---
## 👥 Author
- [Semenov Egor](https://github.com/HobbitTheCat) - Architecture, backend implementation, databases, security
- [Piton Leo](https://github.com/Badoux17) - Frontend
