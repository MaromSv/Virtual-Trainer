import defines
import cv2
import mediapipe as mp
import numpy as np
import pygame
import time
import threading

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

def distance_two_points(a,b):
    a = np.array(a)
    b = np.array(b)
    return np.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

#a =  shoulder, b = left shoulder, c = right_hip, d =left_hip
def straight_Back(leftShoulder, rightShoulder, rightHip, leftHip):
    rightShoulder = np.array(rightShoulder)
    leftShoulder = np.array(leftShoulder)
    rightHip = np.array(rightHip)
    leftHip = np.array(leftHip)

    distRight = distance_two_points(rightShoulder, rightHip)

    distLeft = distance_two_points(leftShoulder, leftHip)

    if (distLeft + distRight < 0.4):
        return True
    else:
        return False

def on_the_ground(rightThumb, leftThumb, rightHip, leftHip):
    rightThumbY = rightThumb[1]
    leftThumbY = leftThumb[1]
    rightHipY = rightHip[1] 
    leftHipY = leftHip[1]

    distance = abs((rightThumbY + leftThumbY) - (rightHipY + leftHipY))
    print(distance)
    if (distance < 0.05):
        return True
    else:
        return False
    
def heelsontheground(leftHeel, rightHeel):
    print(leftHeel, current_heel_left, rightHeel, current_heel_right)
    if abs(leftHeel - current_heel_left) > 0.2:
        return False
    if abs(rightHeel - current_heel_right) > 0.2:
        return False
    else:
        return True

def play_sound(file_path):
    sound_effect = pygame.mixer.Sound(file_path)
    sound_effect.play()

def play_background_music(volume=0.05):
    pygame.mixer.init()
    # pygame.mixer.music.load('Application\\Assets\\Audio\\li-jali-cucu-8466.mp3')
    pygame.mixer.music.load('Application\\Assets\\Audio\\backgroundMusic.mp3')
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play() 

'''def pushUpLogic(leftAngle, rightAngle, stage, straightBack, counter):
    if leftAngle > 155 and rightAngle > 155:
        if stage == "middle":
            print("go lower")
            play_sound("Application\Assets\Audio\goLower.mp3")
        stage = "up"

    if leftAngle < 100 and rightAngle < 100 and stage =='up': 
        stage = "middle"

    if leftAngle < 65 and rightAngle < 65 and stage =='middle': 
        stage="down"
        if straightBack:
            counter +=1
            print(counter)
            audioPath = f"Application\\Assets\\Audio\\numbers\\{str(counter)}.mp3"
            try:
                play_sound(audioPath)
            except:
                print("")
        else:
            print("Keep Your Back Straight")
            play_sound("Application\Assets\Audio\keepBackStraightAudio.mp3")
    return stage, counter'''

def squaTLogic(leftAngle, rightAngle, stage, heels_on_the_ground, counter, leftHeel, rightHeel):
    if leftAngle > 160 and rightAngle > 160:
        if stage == 'middle':
            print('go lower')
            play_sound("Application\Assets\Audio\goLower.mp3")
        stage = 'up'
        global current_heel_left
        global current_heel_right
        current_heel_left = leftHeel[1]
        current_heel_right = rightHeel[1]
    if leftAngle < 140 and rightAngle < 140 and stage =='up': 
        stage = "middle"

    if leftAngle < 110 and rightAngle < 110 and stage =='middle': 
        stage="down"
        if heels_on_the_ground:
            counter +=1
            print(counter)
            audioPath = f"Application\\Assets\\Audio\\numbers\\{str(counter)}.mp3"
            try:
                play_sound(audioPath)
            except:
                print("")
        else:
            print("Keep Your Heels of the Ground")
            play_sound("Application\Assets\Audio\keepBackStraightAudio.mp3")
    return stage, counter

def squaTCounter():
    my_thread = threading.Thread(target=play_background_music, name="MyThread")
    print("test")

    cap = cv2.VideoCapture(defines.CAPTURE_CAMERA_ID, cv2.CAP_DSHOW)

    

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, defines.CAPTURE_FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, defines.CAPTURE_FRAME_HEIGHT)

    # Squat counter variables
    global current_heel_left
    global current_heel_right
    current_heel_left = 0
    current_heel_right = 0
    counter = 0 
    stage = None
    heels_on_the_ground = None
    heels_difference = 0
    start_time = time.time()
    my_thread.start()
    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            #frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

            timeSpent = time.time() - start_time
            timeLeft = (defines.TIMER - timeSpent + 2 )#Time left for attempt, 2 s for startup

            # frame = frame[0:820, 0:600]
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            


            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                leftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                leftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                leftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                leftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                leftThumb = [landmarks[mp_pose.PoseLandmark.LEFT_THUMB.value].x, landmarks[mp_pose.PoseLandmark.LEFT_THUMB.value].y]
                leftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                leftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                leftHeel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
                
                rightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                rightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                rightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                rightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                rightThumb = [landmarks[mp_pose.PoseLandmark.LEFT_THUMB.value].x, landmarks[mp_pose.PoseLandmark.LEFT_THUMB.value].y]
                rightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                rightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                rightHeel = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
                
                # Calculate angle
                leftAngle = calculate_angle(leftAnkle, leftKnee, leftHip)
                rightAngle = calculate_angle(rightAnkle, rightKnee, rightHip)
                #straightBack = straight_Back(leftShoulder, rightShoulder, rightHip, leftHip)

                #heels_on_the_ground = heelsontheground(leftHeel, rightHeel)
                heels_on_the_ground = True
                print(heels_on_the_ground)
                
                # Curl counter logic
                stage, counter = squaTLogic(leftAngle, rightAngle, stage, heels_on_the_ground, counter, leftHeel, rightHeel)
                        
            except:
                pass
            
            
            # Render curl counter
            # Setup status box
            cv2.rectangle(image, (0,0), (450,70), (245,117,16), -1)


            # Time left
            cv2.putText(image, 'Time', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(int(timeLeft)), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 2, cv2.LINE_AA)
            
            # Rep data
            cv2.putText(image, 'REPS', (100,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (100,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            # Stage data
            cv2.putText(image, 'STAGE', (300,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (300,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
        
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )
            cv2.imshow('Squat Counter', image)


            if (timeLeft < 0):
                cap.release()
                cv2.destroyAllWindows()
                my_thread.join()
                return counter

            if cv2.waitKey(10) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                my_thread.join()
                break

