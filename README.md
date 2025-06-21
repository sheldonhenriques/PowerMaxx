# Flask Chat App

A simple Flask application with a modern chat interface that includes a dummy backend endpoint.

## Features

- 🎨 Modern, responsive chat interface
- 💬 Real-time message display
- ⏰ Timestamp for each message
- 📱 Mobile-friendly design
- 🔄 Typing indicators
- 🎯 Dummy backend endpoint for testing

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

## How it works

- The frontend sends POST requests to `/api/chat` with JSON data containing the user's message
- The backend processes the message and returns a response with:
  - `response`: The bot's reply
  - `timestamp`: When the response was generated
  - `status`: Success/error status

## API Endpoint

**POST** `/api/chat`

**Request Body:**
```json
{
  "message": "Hello, how are you?"
}
```

**Response:**
```json
{
  "response": "Hello! How can I help you today?",
  "timestamp": "14:30:25",
  "status": "success"
}
```

## Customization

To integrate with a real AI service, modify the `chat()` function in `app.py` to call your preferred AI API instead of the dummy responses.

## Project Structure

```
Mara/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── templates/
    └── index.html     # Chat interface template
``` 