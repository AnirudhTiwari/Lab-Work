'''
For a given list of coordinates of a cluster, this method calculates the density by dividing total number of entries in the cluster by approximate volume
of the cluster 
'''
import common_functions as utils

def calculateDensity(pdb, chain):
	coordinates_list = utils.getCoordinatesListFromPDB(pdb, chain)
	#Calculates the density of the entire pdb,chain assuming it to be a single cluster
	return calculateDensityOfACluster(coordinates_list)

def calculateDensityOfACluster(coordinates):
	
	centroid_x=0
	centroid_y=0
	centroid_z=0

	#Sum of all points along X, Y & Z axis independently
	for x in coordinates:
		centroid_x=x[0]+centroid_x
		centroid_y=x[1]+centroid_y
		centroid_z=x[2]+centroid_z

	#Finding centroid by dividing the sum of all points along each axis by the total number of points.
	try:
		centroid_x = 1.0*centroid_x/len(coordinates)
		centroid_y = 1.0*centroid_y/len(coordinates)
		centroid_z = 1.0*centroid_z/len(coordinates)
	except Exception, e:
		print "behold Null pointer", e,

	centroid = [centroid_x, centroid_y, centroid_z]		

	radius = 0.0

	#Distance of all points from the centroid
	for a in coordinates:
		radius = radius + utils.dist(a, centroid)	



	#Average over the size of cluster, to give an avg. radius of the cluster.
	radius = radius/len(coordinates)

	density = 1.0*len(coordinates)/(radius*radius*radius)
	return density
