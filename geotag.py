import cv2                       
import numpy as np  
import math

# font = cv2.FONT_HERSHEY_SIMPLEX
video_capture = cv2.VideoCapture("C:/Users/GuestAdmin/Desktop/DOOAF/stable_video_2.avi")
frame_counter = 0

target = [100, 100]
drone_coord = [100, 100]
fov = 10
alti = 40
input_res = [640, 480]
cam_angle = 45
drone_heading = 179
tank = [10, 10]

def target_delta(target, pixel, drone_coord, fov, alti, input_res, cam_angle, drone_heading):

	hor_dist_center = alti * math.tan(cam_angle * (math.pi/180))
	dist_center = alti/math.cos(cam_angle * (math.pi/180))
	frame_length = 2 * (math.tan((fov/2)*(math.pi/180)) * dist_center)
	length_per_pixel = frame_length / input_res[0]
	
	center_cord = [0, 0]
	center_pixel = [input_res[0]/2, input_res[1]/2]
	det_cord = [0, 0]

	center_cord[0] = (hor_dist_center * math.cos(drone_heading*(math.pi/180))) + drone_coord[0]
	center_cord[1] = (hor_dist_center * math.sin(drone_heading*(math.pi/180))) + drone_coord[1]
	
	print("center coord", center_cord)

	#defining quadrant of click
	if pixel[0] > center_pixel[0] and pixel[1] > center_pixel[1]:
		phi = math.degrees(math.atan((pixel[1] - center_pixel[1])/(pixel[0] - center_pixel[0])))
		alpha = phi + drone_heading + 270
		quad = 1
	
	elif pixel[0] < center_pixel[0] and pixel[1] > center_pixel[1]:
		phi = math.degrees(math.atan((center_pixel[0] - pixel[0])/(pixel[1] - center_pixel[1])))
		alpha = phi + drone_heading 
		quad = 2

	elif pixel[0] < center_pixel[0] and pixel[1] < center_pixel[1]:
		phi = math.degrees(math.atan((center_pixel[1] - pixel[1])/(center_pixel[0] - pixel[0])))
		alpha = phi + drone_heading + 90
		quad = 3

	else:
		phi = math.degrees(math.atan((pixel[0] - center_pixel[0])/(center_pixel[1] - pixel[1])))
		alpha = phi + drone_heading + 	180
		quad = 4

	# print("click quad", quad, "alpha", alpha, "phi", phi)
	dist_center_click = (math.sqrt(((pixel[0] - center_pixel[0])**2) + ((pixel[1] - center_pixel[1])**2))) * length_per_pixel

	det_cord[0] = dist_center_click * math.cos(math.radians(alpha)) + center_cord[0]
	det_cord[1] = dist_center_click * math.sin(math.radians(alpha)) + center_cord[1]

	print("blast coord", det_cord)


	dist_tank_blast = math.sqrt(((det_cord[0] - tank[0])**2) + ((det_cord[1] - tank[1])**2))
	dist_tank_target = math.sqrt(((target[0] - tank[0])**2) + ((target[1] - tank[1])**2))

	# print("tank blast", dist_tank_blast, "tank target", dist_tank_target)

	long_delta = dist_tank_target - dist_tank_blast

	# print("target", target, "tank", tank, 'blast', det_cord, math.degrees(math.acos((target[0] - tank[0])/dist_tank_target)))

	target_degree = math.degrees(math.acos((target[0] - tank[0])/dist_tank_target))
	if (target[0] - tank[0]) < 0 and (target[1] - tank[1]) < 0:
		target_degree += 90
	elif (target[0] - tank[0]) > 0 and (target[1] - tank[1]) < 0:
		target_degree += 270

	blast_degree = math.degrees(math.acos((det_cord[0] - tank[0])/dist_tank_blast))
	# print ("calc blast", blast_degree)
	if (det_cord[0] - tank[0]) < 0 and (det_cord[1] - tank[1]) < 0:
		blast_degree += 90
	elif (det_cord[0] - tank[0]) > 0 and (det_cord[1] - tank[1]) < 0:
		blast_degree += 270

	barrel_yaw = target_degree - blast_degree #positive left rotate, negative right rotate

	# barrel_yaw = math.degrees(math.asin((target[0] - tank[0])/(dist_tank_target)) - math.asin((det_cord[0] - tank[0])/(dist_tank_blast)))

	return "barrel rotation:", barrel_yaw, "y delta:", long_delta

def mouseHandler(event, x, y, flags, params):
   
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, input_res[1] - y)
        cv2.circle(frame, (x, y), 3, (255, 0, 0), -1)

        pixel = [0, 0]
        pixel[0] = x
        pixel[1] = input_res[1] - y
        print(target_delta(target, pixel, drone_coord, fov, alti, input_res, cam_angle, drone_heading))

while(True):

    # Capture frame-by-frame
    _, frame = video_capture.read()
    frame_counter += 1
    #If the last frame is reached, reset the capture and the frame_counter
    if frame_counter == video_capture.get(cv2.CAP_PROP_FRAME_COUNT):
        frame_counter = 0 #Or whatever as long as it is the same as next line
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow('Video', frame)
    cv2.setMouseCallback('Video', mouseHandler)

video_capture.release()
cv2.destroyAllWindows() 


