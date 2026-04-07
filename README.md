#  UniEvents — Cloud-Based College Event Registration System

> 🎓 Capstone Project | Google Cloud Digital Leader

🌐 Live Demo: [Open website](https://unievents-app-785490588119.asia-south1.run.app)

Tech: Flask • Firestore • Cloud Run • Pub/Sub • Docker 


##  Overview

**UniEvents** is a cloud-native web application that allows students to register for college events through a simple interface.

This project demonstrates how a traditional local application can be transformed into a **scalable, serverless cloud system** using Google Cloud Platform.

---

## Features

*  Event registration form
*  Admin dashboard (view registrations)
*  Cloud-based database (Firestore)
*  Event-driven messaging (Pub/Sub)
*  Serverless deployment (Cloud Run)
*  Docker-based containerization

---

## 🏗️ Architecture

```
User Browser
     │
     ▼
[Cloud Run] (Flask App)
     │
     ├──► Firestore (NoSQL Database)
     │
     └──► Pub/Sub (Event Messaging)
```

---

## 🧩 Tech Stack

* **Backend:** Python 3.11 + Flask
* **Database (Local):** SQLite
* **Database (Cloud):** Firestore
* **Messaging:** Google Cloud Pub/Sub
* **Containerization:** Docker
* **Hosting:** Google Cloud Run

---

## 📁 Project Structure

```
unievents-cloud/
├── app_cloud.py
├── requirements.txt
├── Dockerfile
├── templates/
├── static/
└── README.md
```

---

## 🖥️ Run Locally

### 1️⃣ Clone Repository

```bash
git clone https://github.com/jeetusinghrajpurohitin/Capstone-Project---UniEvents.git
cd Capstone-Project---UniEvents
```

### 2️⃣ Setup Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements_local.txt
```

### 4️⃣ Run App

```bash
python app_local.py
```

👉 Open: [http://localhost:5000](http://localhost:5000)

---

## ☁️ Cloud Deployment (GCP)

### 🔧 Services Used

| Service           | Purpose             |
| ----------------- | ------------------- |
| Cloud Run         | Serverless hosting  |
| Firestore         | NoSQL database      |
| Pub/Sub           | Event messaging     |
| Artifact Registry | Store Docker images |

---

### Deployment Steps

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable run.googleapis.com firestore.googleapis.com pubsub.googleapis.com artifactregistry.googleapis.com

# Create Firestore
gcloud firestore databases create --location=asia-south1

# Create Pub/Sub topic
gcloud pubsub topics create event-registrations
```

---

### Build & Push Docker Image

```bash
gcloud artifacts repositories create unievents --repository-format=docker --location=asia-south1

gcloud auth configure-docker asia-south1-docker.pkg.dev

docker build -f Dockerfile_cloud -t asia-south1-docker.pkg.dev/YOUR_PROJECT_ID/unievents/app:latest .
docker push asia-south1-docker.pkg.dev/YOUR_PROJECT_ID/unievents/app:latest
```

---

### Deploy to Cloud Run

```bash
gcloud run deploy unievents \
  --image asia-south1-docker.pkg.dev/YOUR_PROJECT_ID/unievents/app:latest \
  --region asia-south1 \
  --platform managed \
  --allow-unauthenticated
```

---

## 🔄 Local → Cloud Migration

| Component | Local        | Cloud     |
| --------- | ------------ | --------- |
| Database  | SQLite       | Firestore |
| Hosting   | Flask server | Cloud Run |
| Messaging | None         | Pub/Sub   |


---

## Author

**Jeetu Singh Rajpurohit**
B.Tech Student

---

## 🧠 Key Learnings

* Serverless architecture using Cloud Run
* NoSQL database design with Firestore
* Event-driven systems using Pub/Sub
* Docker-based deployment workflow

---

