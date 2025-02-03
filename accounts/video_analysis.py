import cv2
import numpy as np
import os
from django.conf import settings

def analyze_football_video(video_path, output_path):
    # Reading the video
    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Create output video writer with H.264 codec
    try:
        # Try XVID codec first
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(
            output_path.replace('.mp4', '.avi'),  # Save as AVI first
            fourcc,
            fps,
            (frame_width, frame_height)
        )
    except:
        # Fallback to MP4V codec
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        out = cv2.VideoWriter(
            output_path,
            fourcc,
            fps,
            (frame_width, frame_height)
        )

    # Initialize variables
    player_positions = {}
    player_speeds = {}
    ball_position = None
    ball_speed = 0
    frame_idx = 0
    font = cv2.FONT_HERSHEY_SIMPLEX

    success, image = vidcap.read()
    while success:
        # Convert frame to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define color ranges
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([70, 255, 255])
        lower_blue = np.array([110, 50, 50])
        upper_blue = np.array([130, 255, 255])
        lower_red = np.array([0, 31, 255])
        upper_red = np.array([176, 255, 255])
        lower_ball = np.array([20, 100, 100])
        upper_ball = np.array([30, 255, 255])

        # Process frame
        mask = cv2.inRange(hsv, lower_green, upper_green)
        res = cv2.bitwise_and(image, image, mask=mask)
        res_gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((13, 13), np.uint8)
        thresh = cv2.threshold(res_gray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        current_frame_positions = {}

        for c in contours:
            x, y, w, h = cv2.boundingRect(c)

            # Player detection
            if h >= 1.5 * w and w > 15 and h >= 15:
                player_img = image[y:y + h, x:x + w]
                player_hsv = cv2.cvtColor(player_img, cv2.COLOR_BGR2HSV)

                mask_blue = cv2.inRange(player_hsv, lower_blue, upper_blue)
                mask_red = cv2.inRange(player_hsv, lower_red, upper_red)
                
                nz_blue = cv2.countNonZero(mask_blue)
                nz_red = cv2.countNonZero(mask_red)

                label = None
                color = None

                if nz_blue >= 20:
                    label = 'France'
                    color = (255, 0, 0)
                elif nz_red >= 20:
                    label = 'Belgium'
                    color = (0, 0, 255)

                if label:
                    player_id = f"{label}_{x}_{y}"
                    current_frame_positions[player_id] = (x + w // 2, y + h // 2)

                    cv2.putText(image, label, (x - 2, y - 2), font, 0.8, color, 2, cv2.LINE_AA)
                    cv2.rectangle(image, (x, y), (x + w, y + h), color, 3)

                    if player_id in player_positions:
                        prev_x, prev_y = player_positions[player_id]
                        cur_x, cur_y = current_frame_positions[player_id]
                        distance = np.sqrt((cur_x - prev_x)**2 + (cur_y - prev_y)**2)
                        speed = (distance * fps) / 100
                        player_speeds[player_id] = speed
                        cv2.putText(image, f"Speed: {speed:.2f} m/s", (x, y + h + 20), font, 0.6, (0, 255, 0), 2)

        # Update player positions and write frame
        player_positions = current_frame_positions
        out.write(image)
        
        success, image = vidcap.read()
        frame_idx += 1

    # Release resources
    vidcap.release()
    out.release()
    
    # Convert AVI to MP4 if needed
    if fourcc == cv2.VideoWriter_fourcc(*'XVID'):
        import subprocess
        mp4_output = output_path
        avi_output = output_path.replace('.mp4', '.avi')
        try:
            subprocess.run([
                'ffmpeg', '-i', avi_output,
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '23',
                '-c:a', 'aac',
                '-b:a', '128k',
                mp4_output
            ], check=True)
            os.remove(avi_output)  # Remove the temporary AVI file
        except:
            # If ffmpeg fails, just rename the AVI file to MP4
            os.rename(avi_output, mp4_output)
    
    return True 