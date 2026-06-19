from flask import Flask, render_template, Response, request, jsonify
import cv2
import numpy as np
import threading
import time

app = Flask(__name__)

# Global variables for color detection
current_frame = None
detection_active = False
color_settings = {
    'blue': {'active': True, 'lower': [100, 150, 50], 'upper': [140, 255, 255]},
    'green': {'active': True, 'lower': [40, 70, 50], 'upper': [80, 255, 255]},
    'red': {'active': True, 'lower': [0, 150, 50], 'upper': [10, 255, 255]},
    'yellow': {'active': True, 'lower': [20, 100, 100], 'upper': [30, 255, 255]},
    'purple': {'active': True, 'lower': [130, 50, 50], 'upper': [160, 255, 255]}
}

class ColorDetector:
    def __init__(self):
        self.cap = None
        self.detection_active = False
        
    def start_detection(self):
        global current_frame, detection_active
        
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(1)
            
        detection_active = True
        
        while detection_active and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Flip frame
            frame = cv2.flip(frame, 1)
            
            # Convert to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Process each color
            for color_name, settings in color_settings.items():
                if settings['active']:
                    lower = np.array(settings['lower'])
                    upper = np.array(settings['upper'])
                    
                    mask = cv2.inRange(hsv, lower, upper)
                    
                    # Remove noise
                    kernel = np.ones((5,5), np.uint8)
                    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                    
                    # Find contours
                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    
                    if contours:
                        largest_contour = max(contours, key=cv2.contourArea)
                        area = cv2.contourArea(largest_contour)
                        
                        if area > 500:
                            x, y, w, h = cv2.boundingRect(largest_contour)
                            
                            # Draw bounding box (simplified for web)
                            color_map = {
                                'blue': (255, 0, 0),
                                'green': (0, 255, 0),
                                'red': (0, 0, 255),
                                'yellow': (0, 255, 255),
                                'purple': (255, 0, 255)
                            }
                            
                            cv2.rectangle(frame, (x, y), (x + w, y + h), color_map[color_name], 2)
                            cv2.putText(frame, color_name.upper(), (x, y-10), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_map[color_name], 2)
            
            # Encode frame for web streaming
            ret, buffer = cv2.imencode('.jpg', frame)
            current_frame = buffer.tobytes()
            
        if self.cap:
            self.cap.release()
    
    def stop_detection(self):
        global detection_active
        detection_active = False
        if self.cap:
            self.cap.release()

detector = ColorDetector()

def generate_frames():
    global current_frame
    while True:
        if current_frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + current_frame + b'\r\n')
        time.sleep(0.03)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/detection')
def detection():
    return render_template('detection.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_detection', methods=['POST'])
def start_detection():
    global detection_active
    
    if not detection_active:
        detection_active = True
        thread = threading.Thread(target=detector.start_detection)
        thread.daemon = True
        thread.start()
        
    return jsonify({'status': 'started'})

@app.route('/stop_detection', methods=['POST'])
def stop_detection():
    detector.stop_detection()
    return jsonify({'status': 'stopped'})

@app.route('/update_colors', methods=['POST'])
def update_colors():
    global color_settings
    data = request.json
    
    for color, active in data.items():
        if color in color_settings:
            color_settings[color]['active'] = active
            
    return jsonify({'status': 'updated'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)