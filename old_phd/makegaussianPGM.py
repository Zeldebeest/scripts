import numpy as np
image_size = (100, 50)
bit_depth = 256
image_array = np.zeros(image_size) # 40 rows (y size), 60 columns (x size)
pixel_size = 2 # um
sigX = 20/2.3548 # um
sigY = 10/2.3548 # um
offX = 20 # um
offY = 40 # um

[rows, columns] = image_array.shape

for i in range(rows):
	for j in range(columns):
		y_coord = (i-rows/2)*pixel_size - offX
		x_coord = (j-columns/2)*pixel_size - offY
		image_array[i,j] = int(np.exp(-1*( x_coord**2/(2*sigX**2) + 
					y_coord**2/(2*sigY**2) ))*bit_depth
					)
		


filename = "gaussian-" + str(sigX*2.3548) + "x-" + str(sigY*2.3548) + "y.pgm"
with open(filename, 'w') as outFile:
	outFile.write("P2\n#well centered gaussian\n" + str(image_size[0]) + 
			" " + str(image_size[1]) +"\n" + str(bit_depth) + "\n")
with open(filename,'a') as outFile:
	np.savetxt(outFile, image_array, delimiter=" ", fmt="%3i")