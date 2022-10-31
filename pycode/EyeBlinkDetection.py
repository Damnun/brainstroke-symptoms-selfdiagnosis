import cv2
import dlib
import imutils
from scipy.spatial import distance as dist
from imutils import face_utils


def calculate_EAR(eye):
    # calculate the vertical distances
    y1 = dist.euclidean(eye[1], eye[5])
    y2 = dist.euclidean(eye[2], eye[4])

    # calculate the horizontal distance
    x1 = dist.euclidean(eye[0], eye[3])

    # calculate the EAR
    EAR = (y1 + y2) / x1
    return EAR


# Variables
blink_thresh = 0.45
succ_frame = 2
count_frame = 0


(L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

detector = dlib.get_frontal_face_detector()
landmark_predict = dlib.shape_predictor('../model/shape_predictor_68_face_landmarks.dat')

cam = cv2.VideoCapture(0)
while 1:
	_, frame = cam.read()
	frame = imutils.resize(frame, width=640)
	img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	faces = detector(img_gray)
	for face in faces:
		shape = landmark_predict(img_gray, face)
		shape = face_utils.shape_to_np(shape)

		lefteye = shape[L_start: L_end]
		righteye = shape[R_start:R_end]

		# Calculate the EAR
		left_EAR = calculate_EAR(lefteye)
		right_EAR = calculate_EAR(righteye)

		# Avg of left and right eye EAR
		avg = (left_EAR + right_EAR) / 2
		if avg < blink_thresh:
			count_frame += 1  # incrementing the frame count
		else:
			if count_frame >= succ_frame:
				cv2.putText(frame, 'Blink Detected', (30, 30),
							cv2.FONT_HERSHEY_DUPLEX, 1, (0, 200, 0), 1)
			else:
				count_frame = 0

	cv2.imshow("Video", frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cam.release()
cv2.destroyAllWindows()