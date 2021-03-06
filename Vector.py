#The vector programe that defines vector operation methods.
import math
import numpy as np 

#square magnitude
def sqmag(a):
    """ 
    Return the square magnitude of a vector
    :param a:  3 dimensional numpy array a
    :return: vector a dotted with itself, equivalent to the square of the magnitude of a
    """
    return a*a

# Magnitude of a vector

def mag(a):
    """
    return the magnitude of a vector
    :param a: 3 dimensional numpy array a
    :return: magnitude of a
    """ 
    b = sqmag(a)
    return (b[0] + b[1] + b[2])**0.5

# Scalar Multiple of a vector
def scalar(a, scalar):
    """
    Multiplying a vector by a scalar
    :param a: 3 dimensional numpy array a
    :param scalar: any real integer or fraction that will be inputted by the user
    :return: the product scalar*a
    """
    return a*scalar

#The vector difference between two vectors
def sub(a, b):
    """
    subtract one vector from another 
    :param a: 3 dimensional numpy array a
    :param b: 3 dimensional numpy array b
    :return: difference of vector b from a (subract b from a)
    """ 
    d = a-b
    return d

#The vector sum between two vectors
def add(a,b):
    """ 
    Vector sum
    :param a: 3 dimensional numpy array a
    :param b: 3 dimensional numpy array b
    :return: the sum a+b labelled d
    """
    d = a+b
    return d

#Cross product of three vectors
def cross(a,b):
	"""
    	return the cross product of two vectors
    	:param a: 3 dimensional numpy array a
    	:param b: 3 dimensional numpy array b
    	:return: cross product axb
    	""" 
	x1 = (a[1]*b[2] - a[2]*b[1])
	x2 = (a[2]*b[0] - a[0]*b[2])
	x3 = (a[0]*b[1] - a[1]*b[0])
	d = np.array([x1,x2,x3],float)
	return d
    	
	

#Dot product of two vectors
def dot(a,b):
    """
    Scalar product
    :param a: 3 dimensional numpy array a
    :param b: 3 dimensional numpy array b
    :return: the sum of corresponding elements of a and b
    (a[1]*b[1] + a[2]*b[2] + a[3]*b[3]) labelled d
    """
    d = a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
    return d
