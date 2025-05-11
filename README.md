# 🎬 YTube Trans

**YTube Trans** is a Python + Streamlit web app that allows users to:
- Download YouTube videos
- Extract audio
- Translate spoken audio into another language using a Speech-to-Speech Translation (S2ST) model
- Combine the translated audio back with the original video

---

## 🚀 Features

- 🎥 Download videos directly from YouTube
- 🎧 Extract and process audio with `moviepy` and `torchaudio`
- 🧠 Translate speech using a PyTorch-based S2ST model (`unity_on_device.ptl`)
- 🔄 Combine translated audio and original video into a new file
- 🌐 Simple web interface built using `Streamlit`

---

## 🧰 Tech Stack

| Layer        | Technology           |
|--------------|----------------------|
| UI           | Streamlit            |
| Video        | Pytube, MoviePy      |
| Audio        | Torchaudio, PyTorch  |
| Translation  | Custom S2ST model    |

---

## 📦 Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/TharunNo1/ytube-trans.git
   cd ytube-trans
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Make sure the S2ST model exists:**
   - Path: `models/unity_on_device.ptl`
   - If you don't have it, please contact the maintainer or update the model loading code.

---

## 🛠️ Usage

Run the app with Streamlit:

```bash
streamlit run app.py
```

1. Enter the YouTube video URL
2. Select a target language (e.g., Hindi, Spanish)
3. Click the **Translate** button
4. Wait for the processing to finish
5. Watch the translated video directly in your browser!

---

## 📝 Requirements

- Python 3.8+
- ffmpeg installed and available in PATH (required by MoviePy)

Install it via:

- **Windows**: [Download FFmpeg](https://ffmpeg.org/download.html)
- **Mac/Linux**:
  ```bash
  brew install ffmpeg   # macOS
  sudo apt install ffmpeg  # Ubuntu
  ```

---

## 📁 Folder Structure

```
ytube-trans/
├── main.py
├── models/
│   └── unity_on_device.ptl
└── README.md
```

---

## ❓ FAQ

**Q: Why do I get `HTTP Error 400`?**  
A: Update PyTube with `pip install --upgrade pytube` and sanitize the video URL to remove extra parameters.

**Q: How do I get a valid translation model?**  
A: You need a `.ptl` TorchScript model trained for S2ST (like English → Hindi). Currently, a sample path is assumed: `models/unity_on_device.ptl`.

---

## 📜 License

MIT License © 2025 Tharun G

---

## 👨‍💻 Author

**Tharun G**  
