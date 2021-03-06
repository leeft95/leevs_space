"""Importing necessary packages and classes"""
import sys
import matplotlib.pyplot as pyplot
import numpy as np
import math as math
from Particle3D import Particle3D
import MDUtilities as MDUtilities
from copy import copy

""" Ensure user inputs correct number of arguments"""
if len(sys.argv)!=3:
    print "Wrong number of arguments."
    print "Usage: " + sys.argv[0] + "<input file>" + "<output file>"
    quit()
else:
    filename = sys.argv[1]    
    outfileName = sys.argv[2]
"""Open files to write on and read from"""
outfile = open(outfileName, "w")
infile = open(filename,"r")

"""Numerically defining values for variables:
Where 	rho= number density of particles
	temp= temperature
	n= number of particles in box
	rcutoff= Cut off radius beyond which force between particles is not calculated (negligible)
	nAt= number of particles converted into float form
	boxsize= length of each side of the box"""
rho = 0.8446
temp = 0.0768
n = 108
rcutoff = 2.5
nAt= float(n)
boxSize = (nAt/rho)**(1.0/3.0)
"""set 3D arrays for position and velocity of particles
where 	pos= numpy array for position
	vel= numpy array for velocity
	mass= mass of particle
	particles"""

pos = np.array([0.0,0.0,0.0],float)
vel = np.array([0.0,0.0,0.0],float)
mass = float(1)
particles = [Particle3D.base(pos,vel,mass) for i in range(n)]

"""Use MDUtilities class to set initial positions and velocities for particles"""
MDUtilities.setInitialPositions(rho, particles)
MDUtilities.setInitialVelocities(temp, particles)
"""Use a for loop to display the resulting mass, positions, and velocities of the particles"""
for i in range(n):
	print particles[i]
print len(particles)
"""Define the timescale for the plot
	numstep= number of steps in the program
	time= time (initial value set to zero)
	dt= increment by which time is increased for each step
	tlog= number of time steps before position vector is updated
	pe= potential energy (initial value set to zero)
	e= total energy (initial value set to zero)"""
numstep = 10000
time = 0.0
dt = 0.0001
tlog = 100
pe = 0.0
e = 0.0
""" Creating lists for each numstep
	tvalue= list of time values of each step
	
	kE= list of kinetic energy values for each step
	force= force between particles before positional update
	force_new= between particles after positional update"""
tValue = []	
posValue_x = [particles[0].position[0]]
posValue_y = [particles[0].position[1]]
kE = []
force = 0.0
force_new = 0.0

"""This loop ensures the Minimum Image Convention is to be obeyed. 
It is also ensured that no particles are used more than once in the calculation.
The closest particles are determined and their interaction calculated."""
for i in range(numstep):
	point = i+1
	if i%100 == 0:
		outfile.write(str(n) + "\nPoint = " + str(point) + "\n")
	for j in range(len(particles)):
		for k in range(len(particles)):
			if j!=k:
				vecsep_x = particles[j].position[0]-particles[k].position[0]	
				vecsep_y = particles[j].position[1]-particles[k].position[1]	
				vecsep_z = particles[j].position[2]-particles[k].position[2]	
				if (vecsep_x>=0.5*boxSize): 
					xpos_im = particles[k].position[0]-boxSize
				else:
					xpos_im = particles[k].position[0]
				if (vecsep_y>=0.5*boxSize): 
					ypos_im = particles[k].position[1]-boxSize
				else:
					ypos_im = particles[k].position[1]
				if (vecsep_z>=0.5*boxSize):
					zpos_im = particles[k].position[2]-boxSize
				else:
					zpos_im = particles[k].position[2]
				pos_img = np.array((xpos_im,ypos_im,zpos_im),dtype = float)
				img = Particle3D(pos_img, particles[k].velocity, particles[k].mass)
			
				img_sep = Particle3D.vec_sep(particles[j],img)
				img_sqmag = math.sqrt(sum(img_sep*img_sep))  
				if img_sqmag<=rcutoff:
					pe_mod = Particle3D.Lj_pot(particles[j], img)
		            		f_mod = Particle3D.Lj_force(particles[j], img)	
					force = force + f_mod
					pe = pe + pe_mod
""""Here, the periodic boundary conditions are set. 
This ensures a finite number of particles are modeled and that when one particle leaves the box, it re-enters from the other side"""
		p1 = j+1
	    	particles[j].leapPos2nd(dt,force)
		if particles[j].position[0]>=boxSize:
           		x_pos = particles[j].position[0]-boxSize
            		particles[j].position[0] = x_pos
        	if particles[j].position[0]<=str(0):
           		x_pos = particles[j].position[0]+boxSize
            		particles[j].position[0] = x_pos
		if particles[j].position[1]>=boxSize:
           		y_pos = particles[j].position[1]-boxSize
            		particles[j].position[1] = y_pos
        	if particles[j].position[1]<=str(0):
           		y_pos = particles[j].position[1]+boxSize
            		particles[j].position[1] = y_pos
		if particles[j].position[2]>=boxSize:
           		z_pos = particles[j].position[2]-boxSize
            		particles[j].position[2] = z_pos
        	if particles[j].position[2]<=str(0):
           		z_pos = particles[j].position[2]+boxSize
            		particles[j].position[2] = z_pos

		if i%100 == 0:
            		outfile.write(str(p1) + " " + str(particles[j].position[0]) + " " + str(particles[j].position[1]) + " " + str(particles[j].position[2]) + "\n")
""" Again, the minimum image convention is laid out. 
The forces are computed for the initial position and for after the position is updated."""
	for l in range(len(particles)): 
        	for m in range(len(particles)): 
		    	if l!=m: 
				x_sep= particles[l].position[0]-particles[m].position[0]
				y_sep= particles[l].position[1]-particles[m].position[1]
				z_sep= particles[l].position[2]-particles[m].position[2] 
				if x_sep>=0.5*boxSize: 
				    	xposi=particles[m].position[0]-boxSize
				else:
				    	xposi=particles[m].position[0]
			       	if y_sep>=0.5*boxSize:
				    	yposi=particles[m].position[1]-boxSize
				else:
				   	yposi=particles[m].position[1]
				if z_sep>=0.5*boxSize:
				    	zposi=particles[m].position[2]-boxSize
				else:
				    	zposi=particles[m].position[2]
				img_pos= np.array((xposi, yposi, zposi), float) 
				img = Particle3D(img_pos, particles[m].velocity, particles[m].mass)
				img_sep = Particle3D.vec_sep(particles[l], img)
				img_sqmag = math.sqrt(sum(img_sep*img_sep))
				if img_sqmag<=rcutoff:         
				    pot_mod1 = Particle3D.Lj_pot(particles[l], img)
				    f_mod1 = Particle3D.Lj_force(particles[l], img)
				    force_new = force_new + f_mod1
				    potential_new = pe + pot_mod1   
        
		particles[l].leapVelocity(dt, 0.5*(force+force_new))
		force_new = 0
		force = 0
		potential = 0


outfile.close()
infile.close()
"""
pyplot.figure()
pyplot.subplot(111)
pyplot.plot(posValue_y,posValue_x)
pyplot.title('Trajectory using Velocity Verlet')
pyplot.xlabel('x position')
pyplot.ylabel('y position')
pyplot.savefig('TrajectoryVV.png')
pyplot.figure()
pyplot.subplot(111)
pyplot.plot(tValue,kE)
pyplot.title('Total Energy of the particle against time')
pyplot.xlabel('Time(s)')
pyplot.ylabel('Energy(J)')
pyplot.savefig('EnergyVV.png')
"""
