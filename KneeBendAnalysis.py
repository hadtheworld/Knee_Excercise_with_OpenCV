import mediapipe as mp
import math
import cv2
mp_pose = mp.solutions.pose

# Setup the Pose function for images - independently for the images standalone processing.
pose_image = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
# initialize the holding timer limit and rep count
holding_timer_limit = 8
rep_count = 0

def Create_vide(recorded_video):
    # set the frame size and codec
    frame_size = (854, 640)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # create a VideoWriter object
    out = cv2.VideoWriter("output.mp4", fourcc, 2, frame_size)
    # loop through the image filenames and add each frame to the video
    for image_filename in recorded_video:
        # image_path = os.path.join(folder_path, image_filename)
        # frame = cv2.imread(image_path)
        out.write(image_filename)
    #  release the VideoWriter object
    out.release()
    cv2.destroyAllWindows()

def calculate_performance(rep_count):
    # set a target rep count
    target_rep_count = 30

    # calculate the percentage of target rep count achieved
    performance = rep_count / target_rep_count * 100

    return performance

# start the video capture
video_capture = cv2.VideoCapture("KneeBendVideo.mp4")
recorded_video = []

def is_knee_bend(keypoints,w,h):
    
    try:
        lm=mp_pose.PoseLandmark
        lm2=keypoints.pose_landmarks
        # get the keypoints for the left and right knee
        left_knee_keypoints = [int(lm2.landmark[lm.LEFT_KNEE].x*w),int(lm2.landmark[lm.LEFT_KNEE].y*h)]
        right_knee_keypoints = [int(lm2.landmark[lm.RIGHT_KNEE].x*w),int(lm2.landmark[lm.RIGHT_KNEE].y*h)]
        # get the keypoints for the left and right hip
        left_hip_keypoints = [int(lm2.landmark[lm.LEFT_HIP].x*w),int(lm2.landmark[lm.LEFT_HIP].y*h)]
        right_hip_keypoints = [int(lm2.landmark[lm.RIGHT_HIP].x*w),int(lm2.landmark[lm.RIGHT_HIP].y*h)]
        # calculate the angle between the hip and knee for both leg
        left_knee_angle = math.degrees(math.atan2(left_knee_keypoints[1] - left_hip_keypoints[1], left_knee_keypoints[0] - left_hip_keypoints[0]))
        right_knee_angle = math.degrees(math.atan2(right_knee_keypoints[1] - right_hip_keypoints[1], right_knee_keypoints[0] - right_hip_keypoints[0]))
    except:
        return False
    # check if either angle is less than 140 degrees (indicating a knee bend)
    if left_knee_angle < 140 or right_knee_angle < 140:
        return True
    else:
        return False

def is_leg_stretch(keypoints,w,h):
    
    try:
        lm=mp_pose.PoseLandmark
        lm2=keypoints.pose_landmarks
        # get the keypoints for the left and right ankle
        left_ankle_keypoints = [int(lm2.landmark[lm.LEFT_ANKLE].x*w),int(lm2.landmark[lm.LEFT_ANKLE].y*h)]
        right_ankle_keypoints = [int(lm2.landmark[lm.RIGHT_ANKLE].x*w),int(lm2.landmark[lm.RIGHT_ANKLE].y*h)]
        # get the keypoints for the left and right knee
        left_knee_keypoints = [int(lm2.landmark[lm.LEFT_KNEE].x*w),int(lm2.landmark[lm.LEFT_KNEE].y*h)]
        right_knee_keypoints = [int(lm2.landmark[lm.RIGHT_KNEE].x*w),int(lm2.landmark[lm.RIGHT_KNEE].y*h)]
        # calculate the angle between the knee and ankle for both legs
        left_ankle_angle = math.degrees(math.atan2(left_ankle_keypoints[1] - left_knee_keypoints[1], left_ankle_keypoints[0] - left_knee_keypoints[0]))
        right_ankle_angle = math.degrees(math.atan2(right_ankle_keypoints[1] - right_knee_keypoints[1], right_ankle_keypoints[0] - right_knee_keypoints[0]))
    except:
        return False
    # check if both angles are close to 180 degrees (indicating a leg stretch)
    if abs(left_ankle_angle - 180) < 20 and abs(right_ankle_angle - 180) < 20:
        return True
    else:
        return False

frame_rate=0.5
# loop through the video frames
sec=0
while True:
    # get the next frame from the video
    video_capture.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    success,frame = video_capture.read()
    if not success:
        break
    sec+=frame_rate
    sec=round(sec,2)
    # run the frame through the pose model to get the pose keypoints
    cv2.imshow("output",frame)
    h, w = frame.shape[:2]
    # Convert the BGR image to RGB.
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    keypoints = pose_image.process(frame)
    print(keypoints)
    
    # check if the keypoints indicate a knee bend
    if is_knee_bend(keypoints,w,h):
        # start the holding timer
        holding_timer = 0
        fl_nm=0
        if not success:
            break
        fl=True
        fl2=True
        # loop until the holding timer reaches the limit or the keypoints no longer indicate a knee bend
        while True:
            # increment the holding timer
            # fps = video_capture.get(cv2.CAP_PROP_FPS)
            if is_knee_bend(keypoints,w,h):
                holding_timer += frame_rate
            # get the next frame from the video
            video_capture.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
            resu, frame = video_capture.read()
            # print(resu)
            if not resu: 
                if frame==None:
                    break
            # print(resu)
            sec+=frame_rate
            sec=round(sec,2)
            cv2.imshow("output",frame)
            h, w = frame.shape[:2]
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # run the frame through the pose model to get the updated keypoints
            keypoints = pose_image.process(frame)
            if holding_timer>=holding_timer_limit and is_leg_stretch(keypoints,w,h):
                print("good")
                rep_count+=1
                cv2.imwrite("D:/DSA/images/frame"+str(fl_nm)+".jpg",frame)
                frame=cv2.imread('D:/DSA/images/frame'+str(fl_nm)+".jpg")
                recorded_video.append(frame)
                holding_timer=0
                fl=True
                fl2=True
                fl_nm+=1
            else:
                cv2.imwrite("D:/DSA/images/frame"+str(fl_nm)+".jpg",frame)
                frame=cv2.imread('D:/DSA/images/frame'+str(fl_nm)+".jpg")
                recorded_video.append(frame)
                fl_nm+=1
            if holding_timer<holding_timer_limit and is_leg_stretch(keypoints,w,h) and fl:
                print("Keep your knee bent")
                fl=False
            if holding_timer<holding_timer and is_knee_bend(keypoints,w,h):
                continue
            if holding_timer>=holding_timer_limit and is_knee_bend(keypoints,w,h) and fl2:
                print("Stretch your leg")
                fl2=False
            
            if cv2.waitKey(1) & 0xFF== ord('q'):
                break
    else:
        # add the logic to handle fluctuations
        pass
    if cv2.waitKey(1) & 0xFF== ord('q'):
                break

# upload the recorded video to drive
Create_vide(recorded_video)

# # print the rep count and the performance of the user
print("Rep count:", rep_count)
print("Performance:", calculate_performance(rep_count))