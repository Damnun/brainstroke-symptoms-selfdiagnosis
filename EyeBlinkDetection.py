import cv2
import dlib
from scipy.spatial import distance as dist
from imutils import face_utils


cam = cv2.VideoCapture(0)
blink_count = 0

def calculate_EAR(eye):
	y1 = dist.euclidean(eye[1], eye[5])
	y2 = dist.euclidean(eye[2], eye[4])
	x1 = dist.euclidean(eye[0], eye[3])
	EAR = (y1 + y2) / x1

# Variables
blink_thresh = 0.45
succ_frame = 1
count_frame = 0

# Eye landmarks
(L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

# Initializing the Models for Landmark and
# face Detection
detector = dlib.get_frontal_face_detector()
landmark_predict = dlib.shape_predictor('model/shape_predictor_68_face_landmarks.dat')

while cam.isOpened():
	if cam.get(cv2.CAP_PROP_POS_FRAMES) == cam.get(
			cv2.CAP_PROP_FRAME_COUNT):
		cam.set(cv2.CAP_PROP_POS_FRAMES, 0)

	else:
		_, frame = cam.read()
		# frame = imutils.resize(frame, width=640)

		# converting frame to gray scale to
		# pass to detector
		try:
			img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		except:
			cam.release()
			cv2.destroyAllWindows()
			print("blink count :", blink_count)

		# detecting the faces
		faces = detector(img_gray)
		for face in faces:
			# landmark detection
			shape = landmark_predict(img_gray, face)
			shape = face_utils.shape_to_np(shape)
			lefteye = shape[L_start: L_end]
			righteye = shape[R_start:R_end]

			# Calculate the EAR
			left_EAR = calculate_EAR(lefteye)
			right_EAR = calculate_EAR(righteye)

			# Avg of left and right eye EAR
			avg = (left_EAR + right_EAR)/2
			if avg < blink_thresh:
				count_frame += 1  # incrementing the frame count
			else:
				if count_frame >= succ_frame:
					cv2.putText(frame, 'Blink Detected', (240, 30),
								cv2.FONT_HERSHEY_DUPLEX, 1, (0, 200, 0), 1)
				else:
					blink_count += 1
					print(blink_count)
					count_frame = 0
		cv2.imshow("Video", frame)

	if cv2.waitKey(1) & 0xff == ord('q'):
		cam.release()
		cv2.destroyAllWindows()
		print("blink_count = ", blink_count)
