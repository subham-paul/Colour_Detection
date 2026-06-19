# 🎨 Colour Detection

A real-time **Colour Detection Web Application** built with **Python**, **Flask**, and **OpenCV**. This project captures live video from a webcam, detects colors in real time, and identifies them based on their RGB values. It provides an interactive way to explore computer vision concepts and color recognition.

> Detect, identify, and analyze colors instantly using your webcam.

---

## ✨ Features

- 🎥 Real-time webcam color detection
- 🎨 Detect colors using OpenCV image processing
- 📍 Identify RGB color values
- ⚡ Fast and responsive processing
- 🌐 Flask-powered web interface
- 🖥️ User-friendly interface
- 📷 Live video streaming
- 💻 Lightweight and easy to use

---

# 🛠️ Tech Stack

### Backend
- Python 3.10+
- Flask 2.3.3

### Computer Vision
- OpenCV
- NumPy

### Frontend
- HTML
- CSS
- JavaScript
- Jinja2 Templates

---

# 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 2.3.3 | Web Framework |
| OpenCV | 4.8.1.78 | Image Processing & Webcam |
| NumPy | 1.24.3 | Numerical Operations |
| Jinja2 | 3.1.6 | HTML Templating |
| Werkzeug | 3.1.8 | WSGI Utility Library |
| click | 8.4.1 | Flask CLI Support |
| blinker | 1.9.0 | Signal Support |
| colorama | 0.4.6 | Colored Terminal Output |
| itsdangerous | 2.2.0 | Secure Data Handling |
| MarkupSafe | 3.0.3 | Safe HTML Rendering |

---

# 📂 Project Structure

```
Colour-Detection/
│
├── app.py
├── requirements.txt
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── index.html
│   └── ...
│
├── README.md
│
└── ...
```

---

# 🚀 How It Works

1. The webcam captures live video frames.
2. OpenCV processes each frame.
3. The selected color region is analyzed.
4. RGB values are extracted from the detected area.
5. The application displays the detected color information in real time through the Flask web interface.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/subham-paul/Colour-Detection.git
```

```bash
cd Colour-Detection
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Application

```bash
python app.py
```

or

```bash
flask run
```

---

# 🌐 Access the Application

Open your browser:

```
http://127.0.0.1:5000
```

---

# 📋 Requirements

```text
blinker==1.9.0
click==8.4.1
colorama==0.4.6
Flask==2.3.3
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
numpy==1.24.3
opencv-python==4.8.1.78
Werkzeug==3.1.8
```

---

# 💡 Applications

- Color Recognition
- Computer Vision Learning
- Image Processing Projects
- Educational Demonstrations
- Object Color Identification
- Quality Inspection
- Robotics
- Industrial Automation

---

# 🚀 Future Enhancements

- HSV Color Detection
- Multiple Color Tracking
- Object Tracking
- Color Histogram Analysis
- Custom Color Selection
- Screenshot Capture
- Mobile-Friendly UI
- AI-Based Object Recognition
- Export Detection Results
- Dark Mode Support

---

# 🤝 Contributing

Contributions are welcome!

1. Fork this repository.
2. Create a feature branch.

```bash
git checkout -b feature/NewFeature
```

3. Commit your changes.

```bash
git commit -m "Add New Feature"
```

4. Push to your branch.

```bash
git push origin feature/NewFeature
```

5. Open a Pull Request.

---

# 🐞 Issues

If you discover a bug or have suggestions for improvement, feel free to open an issue.

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

## **Subham Paul**

Passionate about **Python, Computer Vision, Artificial Intelligence, Automation, and Web Development.**

- GitHub: https://github.com/subham-paul
- LinkedIn: https://www.linkedin.com/in/subham-paul-india/

---

# ⭐ Support

If you found this project useful:

- ⭐ Star this repository
- 🍴 Fork the project
- 🤝 Contribute
- 💬 Share your feedback


---

## 🙏 Acknowledgements

Thanks to the amazing open-source communities behind:

- Flask
- OpenCV
- NumPy

for providing the tools that made this project possible.

---

> **"Bringing colors to life through the power of Computer Vision."** 🎨
