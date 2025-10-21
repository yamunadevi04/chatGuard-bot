# 🧠 ChatGuard Bot

An intelligent chatbot that responds to queries while filtering out offensive, harmful, or irrelevant content.

## 🎯 Features

- **Content Moderation**: Detects harmful/offensive content using Hugging Face AI
- **Dual Response Modes**: Toggle between Formal and Funny personalities
- **Clean Interface**: Pure HTML/CSS/JavaScript frontend
- **Python Backend**: Flask API with Hugging Face transformers

## 🏗️ Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python 3.9+, Flask, Hugging Face Transformers
- **AI Models**: Hugging Face (toxicity detection + text generation)

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Free Hugging Face account

### Get Your Free Hugging Face API Key

1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Give it a name and select "read" access
4. Copy your token

### Installation

1. **Clone/Navigate to project:**
   ```bash
   cd project-chatbot
   ```

2. **Set up Python backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your Hugging Face token
   ```

4. **Run the backend:**
   ```bash
   python app.py
   ```

5. **Open the frontend:**
   - Open `frontend/index.html` in your browser
   - Or use a local server:
   ```bash
   cd ../frontend
   python -m http.server 3000
   ```
   Then visit http://localhost:3000

## 🔧 Configuration

Edit `backend/.env`:
```env
FLASK_PORT=5000
FLASK_ENV=development
HUGGINGFACE_API_KEY=hf_your_token_here
```

## 📡 API Endpoints

### POST `/api/chat`
**Request:**
```json
{
  "message": "User input text",
  "mode": "formal"
}
```

**Response:**
```json
{
  "reply": "Bot response",
  "classification": "safe",
  "mode": "formal"
}
```

### GET `/api/health`
Check server status

## 🎭 Response Modes

**Formal**: Professional and respectful
**Funny**: Witty and playful

## 🛡️ Moderation

Uses Hugging Face models:
- **Toxicity**: `unitary/toxic-bert`
- **Text Generation**: `microsoft/DialoGPT-medium`

## 📁 Project Structure

```
project-chatbot/
├── backend/
│   ├── app.py                 # Flask server
│   ├── services/
│   │   ├── moderation.py      # Content moderation
│   │   └── response.py        # Response generation
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Configuration
├── frontend/
│   ├── index.html            # Main page
│   ├── styles.css            # Styling
│   └── script.js             # Chat logic
└── README.md
```

## 📄 License

MIT License
