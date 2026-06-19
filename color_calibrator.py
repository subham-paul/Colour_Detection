import cv2
import numpy as np

def nothing(x):
    pass

# Create trackbars for HSV calibration
cv2.namedWindow('HSV Calibrator')

# Create trackbars for lower HSV
cv2.createTrackbar('H Lower', 'HSV Calibrator', 0, 179, nothing)
cv2.createTrackbar('S Lower', 'HSV Calibrator', 0, 255, nothing)
cv2.createTrackbar('V Lower', 'HSV Calibrator', 0, 255, nothing)

# Create trackbars for upper HSV
cv2.createTrackbar('H Upper', 'HSV Calibrator', 179, 179, nothing)
cv2.createTrackbar('S Upper', 'HSV Calibrator', 255, 255, nothing)
cv2.createTrackbar('V Upper', 'HSV Calibrator', 255, 255, nothing)

cap = cv2.VideoCapture(0)

print("HSV Calibration Tool")
print("Adjust trackbars to isolate your colored object")
print("Press 'ESC' to exit and get HSV values")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Get current trackbar positions
    h_low = cv2.getTrackbarPos('H Lower', 'HSV Calibrator')
    s_low = cv2.getTrackbarPos('S Lower', 'HSV Calibrator')
    v_low = cv2.getTrackbarPos('V Lower', 'HSV Calibrator')
    
    h_high = cv2.getTrackbarPos('H Upper', 'HSV Calibrator')
    s_high = cv2.getTrackbarPos('S Upper', 'HSV Calibrator')
    v_high = cv2.getTrackbarPos('V Upper', 'HSV Calibrator')
    
    # Define HSV range
    lower_color = np.array([h_low, s_low, v_low])
    upper_color = np.array([h_high, s_high, v_high])
    
    # Create mask
    mask = cv2.inRange(hsv, lower_color, upper_color)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Display values
    cv2.putText(frame, f'Lower: [{h_low}, {s_low}, {v_low}]', 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, f'Upper: [{h_high}, {s_high}, {v_high}]', 
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Show images
    combined = np.hstack([frame, result])
    cv2.imshow('HSV Calibrator', combined)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

print("\nFinal HSV Values:")
print(f"Lower: [{h_low}, {s_low}, {v_low}]")
print(f"Upper: [{h_high}, {s_high}, {v_high}]")
print("Copy these values to your main.py file")