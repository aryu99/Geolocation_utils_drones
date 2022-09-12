import math

def transform(drone_coord, pixel, fov, alti, input_res, cam_angle, drone_heading):

	hor_dist_center = alti * math.tan(cam_angle * (math.pi/180))
	dist_center = alti/math.cos(cam_angle * (math.pi/180))
	frame_length = 2 * (math.tan((fov/2)*(math.pi/180)) * dist_center)
	length_per_pixel = frame_length / input_res[0]
	
	center_cord = [0, 0]
	det_cord = [0, 0]
	theta = 0
	quad = 0

	# determining the angle w.r.t the x-axis
	if drone_heading < 90:
		theta = 90 - drone_heading
		center_cord[0] = (hor_dist_center * math.cos(theta*(math.pi/180))) + drone_coord[0]
		center_cord[1] = (hor_dist_center * math.sin(theta*(math.pi/180))) + drone_coord[1]
		quad = 1

	elif drone_heading > 90 and drone_heading < 180:
		theta = drone_heading - 90
		center_cord[0] = (hor_dist_center * math.cos(theta*(math.pi/180))) + drone_coord[0]
		center_cord[1] = drone_coord[1] - (hor_dist_center * math.sin(theta*(math.pi/180))) 
		quad = 2

	elif drone_heading > 180 and drone_heading < 270:
		theta = 90 - (drone_heading - 180)
		center_cord[0] = drone_coord[0] - (hor_dist_center * math.cos(theta*(math.pi/180))) 
		center_cord[1] = drone_coord[1] - (hor_dist_center * math.sin(theta*(math.pi/180))) 
		quad = 3

	else: 
		theta = drone_heading - 270
		center_cord[0] = drone_coord[0] - (hor_dist_center * math.cos(theta*(math.pi/180)))  
		center_cord[1] = (hor_dist_center * math.sin(theta*(math.pi/180))) + drone_coord[1]
		quad = 4

	det_x_pixel = [pixel[0], input_res[1]/2]
	dist_center_detx = math.sqrt(((input_res[0]/2 - det_x_pixel[0])**2) + ((input_res[1]/2 - det_x_pixel[1])**2)) * length_per_pixel #distance of centre of the frame to the detection's x-axis location in meters

	if pixel[0] > input_res[0]/2 :
		det_x = 0 # detection in either 1st or 2nd quad of the input frame
	else:
		det_x = 1 # detection in either 3rd or 4th quad of input frame
	
	#Combining the the heading of the drone and the detection quadrant to determine the coords of detection
	if (quad == 1 and det_x == 1) or (quad == 3 and det_x == 0):
		det_cord[0] = center_cord[0] - (dist_center_detx * math.cos(theta*(math.pi/180))) 
		det_cord[1] = (dist_center_detx * math.sin(theta*(math.pi/180))) + center_cord[1]

	elif (quad == 1 and det_x == 0) or (quad == 3 and det_x == 1):
		det_cord[0] = (dist_center_detx * math.cos(theta*(math.pi/180))) + center_cord[0]
		det_cord[1] = center_cord[1] - (dist_center_detx * math.sin(theta*(math.pi/180)))

	elif (quad == 2 and det_x == 1) or (quad == 4 and det_x == 0):
		det_cord[0] = (dist_center_detx * math.cos(theta*(math.pi/180))) + center_cord[0]
		det_cord[1] = (dist_center_detx * math.sin(theta*(math.pi/180))) + center_cord[1]

	elif (quad == 2 and det_x == 0) or (quad == 4 and det_x == 1):
		det_cord[0] = center_cord[0] - (dist_center_detx * math.cos(theta*(math.pi/180))) 
		det_cord[1] = center_cord[1] - (dist_center_detx * math.sin(theta*(math.pi/180))) 

	return det_cord

print (transform([0,0], [640, 480], 10, 14.14, [640, 480], 45, 315))









