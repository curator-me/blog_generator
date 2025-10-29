# 🧠 AI Blog Generator (Django Backend)

A **Django-based backend** for generating and managing blog posts automatically from **YouTube videos**.  
The system downloads the video’s audio, transcribes it using **AssemblyAI**, and then uses **Groq’s LLaMA model** to generate a fully formatted blog article.

It also supports JWT authentication, profiles, password management, and CRUD operations for blogs.

---

## 🚀 Features

- 🧑‍💻 **User Authentication**
  - Register, Login, Logout with JWT token
  - Change / Reset Password
  - Edit User Profile

- 🧩 **AI Blog Generation**
  - Accepts a YouTube URL
  - Downloads & transcribes audio
  - Generates a well-formatted blog article
  - Saves to the user’s account

- 📝 **Blog Management**
  - View all saved blogs
  - View a specific blog
  - (Delete endpoint placeholder available)

- 🧠 **AI Integration**
  - Uses **AssemblyAI** for speech-to-text transcription
  - Uses **Groq API (LLaMA3)** for blog generation

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-------------|
| Backend | Django 5.x |
| Language | Python 3.x |
| AI API | Groq (LLaMA 3 8B) |
| Transcription | AssemblyAI |
| Video/Audio | yt_dlp |
| Database | SQLite / PostgreSQL |
| Frontend (optional) | HTML Templates (Django) |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/ai-blog-generator.git
cd ai-blog-generator
```

2️⃣ Create a virtual environment
```
python -m venv venv
source venv/bin/activate  # or on Windows: venv\Scripts\activate
```

3️⃣ Install dependencies
```
pip install -r requirements.txt
```

5️⃣ Run the server
```
python manage.py runserver
```
