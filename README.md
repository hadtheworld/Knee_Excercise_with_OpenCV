# Knee_Excercise_with_OpenCV
This is my attempt with OpenCv where I am analysis an knee excercize video and providing instructions at the real time when to do what step and record all successful reps for the user. It provides the performance of the user and also generates an output video of the analysis.

Google Drive link:- https://drive.google.com/drive/folders/1KkkGtzciz1Z0uJX2SqS8J2EN7yJL-3z9?usp=share_link
In the above G-drive link I have uploaded the complete project as it was getting difficult to upload here, Please visit it also for knowing more. 

Main goal:
  - To analyse video "KneeBendVideo.mp4" using OpenCV module in python i.e :- "cv2" and "mediapipe" module of pthon
  - breaking the video into frames and checker for Body Posture using mediapipe.solutions.pose mehods
  - Here the frames are read as static image files using "mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)".
  - mp_pose=mp.solutions.pose
  - In each frame check for the knee movements and give instructions to "Keep your knee bent" and "Stretch your leg" as per the time of 8sec for each bending and relaxing
  - count of successful reps is taken to give the final result of how many reps did the user made.
  
  
**Detaile explainatio on Code**:
The code has following parts:
     - is_knee_bend(keypoints,w,h):- This function takes in the processed image frame of mediapipe posture analysis as "keypoints" and width of human as "w" and height as "h" and checks if the person has bend their knees or not and returns "True" or "False" Accordingly.
     
     - is_leg_strech(keypoints,w,h):-This function takes in the processed image frame of mediapipe posture analysis as "keypoints" and width of human as "w" and height as "h" and checks if the person has streched their legs or not and returns "True" or "False" Accordingly.
     
     - Create_video(recorded_video):- This function creates the output video using the list if image frames in "recorded_video". It uses the cv2.VideoWriter() function
     
     - Calculate_performance(rep_count):- this function checks the performance of the program by checking for the amount of correct reps detected and gice the percentage of effeciency as the performance.
     
     - infinite while loop:- It is used for creating frames out of the video and calling above functions to analyse them according to a knee bend and strech reps of >=8 sec each. this loop will run till no frame is generated or the video ends.
     
     
**Comments are also provided inside the code for easy understanding and flow of the program

LEARNING IN THIS PROJECT:-
As this was my first expoerience with OpenCv and mediapipe I enjoyed the functionalities provided by them and ease of image analysis using them.
      I this project I learned:-
      - human pose analysis using mediapipe which converts the image frames into coordinates of various human body parts and propotions whic can be used to create neede logics like in my case to analyse knee bends.
      
      - cv2.VideoCapture() in opencv:- this function helps in goin through the video frame by frames and seperates frames from them to anayles it.
      
      - .set() in OpenCv:- This function allows us to jump to a specific time in the video which we can use to generate limited amount of frames as per our need of the video.
      
      - .read() in OpenCv:- This function allows us to get frame from a capured video instance which we have got using cv2.VideoCapture
      
      - cv2.imread(),cv2.imwrite() :- to create image out of frames obtained above and read them to generate videos
      
      - cv2.VideoWriter():- This creates the video by combining the image files accoding to specefied frame rate and frame size.
