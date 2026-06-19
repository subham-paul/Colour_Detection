import cv2
import numpy as np

print("Multi-Color Object Tracker Starting...")

# Initialize webcam with error handling
cap = cv2.VideoCapture(0)

# Check if webcam opened successfully
if not cap.isOpened():
    print("ERROR: Cannot open webcam!")
    print("Trying alternative camera index...")
    cap = cv2.VideoCapture(1)
    
if not cap.isOpened():
    print("ERROR: No webcam found!")
    print("Please check:")
    print("1. Webcam is connected")
    print("2. No other program is using the webcam")
    print("3. Try running as Administrator")
    exit()

print("Webcam opened successfully!")

# Test reading a frame
ret, test_frame = cap.read()
if not ret:
    print("ERROR: Cannot read from webcam!")
    cap.release()
    exit()

print("Webcam test frame captured!")
print("Press 'ESC' to exit")
print("Press 'R' to reset path")
print("Press 'C' for color info")
print("Press '1-5' to toggle colors (1:Blue, 2:Green, 3:Red, 4:Yellow, 5:Purple)")
print("Press 'A' to track ALL colors")

# Define multiple color ranges
color_ranges = {
    'blue': {
        'lower': np.array([100, 150, 50]),
        'upper': np.array([140, 255, 255]),
        'active': True,
        'color': (255, 0, 0)  # BGR - Blue
    },
    'green': {
        'lower': np.array([40, 70, 50]),
        'upper': np.array([80, 255, 255]),
        'active': True,
        'color': (0, 255, 0)  # BGR - Green
    },
    'red': {
        'lower': np.array([0, 150, 50]),
        'upper': np.array([10, 255, 255]),
        'active': True,
        'color': (0, 0, 255)  # BGR - Red
    },
    'yellow': {
        'lower': np.array([20, 100, 100]),
        'upper': np.array([30, 255, 255]),
        'active': True,
        'color': (0, 255, 255)  # BGR - Yellow
    },
    'purple': {
        'lower': np.array([130, 50, 50]),
        'upper': np.array([160, 255, 255]),
        'active': True,
        'color': (255, 0, 255)  # BGR - Purple
    }
}

# Store positions for each color
color_positions = {color: [] for color in color_ranges}
max_positions = 50

try:
    while True:
        # Read frame
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Lost connection to webcam!")
            break
        
        # Flip frame horizontally (mirror effect)
        frame = cv2.flip(frame, 1)
        
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Process each active color
        for color_name, color_info in color_ranges.items():
            if not color_info['active']:
                continue
                
            # Create mask for this color
            mask = cv2.inRange(hsv, color_info['lower'], color_info['upper'])
            
            # Remove noise
            kernel = np.ones((5,5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # If contours found
            if contours:
                # Find largest contour
                largest_contour = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest_contour)
                
                if area > 500:  # Only track substantial objects
                    # Get bounding rectangle
                    x, y, w, h = cv2.boundingRect(largest_contour)
                    
                    # Calculate center
                    center_x = x + w // 2
                    center_y = y + h // 2
                    
                    # Store position
                    color_positions[color_name].append((center_x, center_y))
                    if len(color_positions[color_name]) > max_positions:
                        color_positions[color_name].pop(0)
                    
                    # Draw bounding box
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color_info['color'], 2)
                    
                    # Draw center
                    cv2.circle(frame, (center_x, center_y), 5, color_info['color'], -1)
                    
                    # Draw path
                    positions = color_positions[color_name]
                    for i in range(1, len(positions)):
                        cv2.line(frame, positions[i-1], positions[i], color_info['color'], 2)
                    
                    # Display info
                    cv2.putText(frame, f'{color_name.upper()}', 
                               (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_info['color'], 2)
                    cv2.putText(frame, f'X: {center_x}, Y: {center_y}', 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    cv2.putText(frame, f'Area: {int(area)}', 
                               (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Display color status
        y_offset = 90
        for color_name, color_info in color_ranges.items():
            status = "ON" if color_info['active'] else "OFF"
            color_display = color_info['color']
            cv2.putText(frame, f"{color_name}: {status}", 
                       (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_display, 1)
            y_offset += 25
        
        # Display instructions
        cv2.putText(frame, "ESC: Exit | R: Reset | C: Color Info | 1-5: Toggle Colors | A: All", 
                   (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Show the frame
        cv2.imshow('Multi-Color Object Tracker', frame)
        
        # Keyboard controls
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            print("Exit requested by user")
            break
        elif key == ord('r'):
            color_positions = {color: [] for color in color_ranges}
            print("All tracking paths reset!")
        elif key == ord('c'):
            print("Current color ranges:")
            for color_name, color_info in color_ranges.items():
                print(f"{color_name}: Lower {color_info['lower']}, Upper {color_info['upper']}")
        elif key == ord('a'):
            # Toggle all colors
            all_active = all(color_info['active'] for color_info in color_ranges.values())
            new_state = not all_active
            for color_info in color_ranges.values():
                color_info['active'] = new_state
            state = "ON" if new_state else "OFF"
            print(f"All colors turned {state}")
        elif key in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:
            # Toggle individual colors
            color_keys = ['blue', 'green', 'red', 'yellow', 'purple']
            index = key - ord('1')
            if 0 <= index < len(color_keys):
                color_name = color_keys[index]
                color_ranges[color_name]['active'] = not color_ranges[color_name]['active']
                state = "ON" if color_ranges[color_name]['active'] else "OFF"
                print(f"{color_name} turned {state}")

except Exception as e:
    print(f"ERROR: {e}")

finally:
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("Multi-Color Tracker closed properly!")