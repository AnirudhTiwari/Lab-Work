import numpy as np
import common_functions as utils
import re
import random
# import matplotlib.pyplot as plt

def cluster_points(X, mu):
    clusters  = {}
    for x in X:
        bestmukey = min([(i[0], np.linalg.norm(x-mu[i[0]])) \
                    for i in enumerate(mu)], key=lambda t:t[1])[0]
        try:
            clusters[bestmukey].append(x)
        except KeyError:
            clusters[bestmukey] = [x]
    return clusters
 
def reevaluate_centers(mu, clusters):
    newmu = []
    keys = sorted(clusters.keys())
    for k in keys:
        newmu.append(np.mean(clusters[k], axis = 0))
    return newmu
 
def has_converged(mu, oldmu):
    return (set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu]))
 
def find_centers(X, K):
    # Initialize to K random centers
    oldmu = random.sample(X, K)
    mu = random.sample(X, K)
    while not has_converged(mu, oldmu):
        oldmu = mu
        # Assign all points in X to clusters
        clusters = cluster_points(X, mu)
        # Reevaluate centers
        mu = reevaluate_centers(oldmu, clusters)
    return(mu, clusters)

def Wk(mu, clusters):
    K = len(mu)
    return sum([np.linalg.norm(mu[i]-c)**2/(2*len(c)) \
               for i in range(K) for c in clusters[i]])

def bounding_box(X):
    xmin, xmax = min(X,key=lambda a:a[0])[0], max(X,key=lambda a:a[0])[0]
    ymin, ymax = min(X,key=lambda a:a[1])[1], max(X,key=lambda a:a[1])[1]
    return (xmin,xmax), (ymin,ymax)
 
def gap_statistic(X):
    (xmin,xmax), (ymin,ymax) = bounding_box(X)
    # Dispersion for real distribution
    ks = range(2,7)
    Wks = np.zeros(len(ks))
    Wkbs = np.zeros(len(ks))
    sk = np.zeros(len(ks))
    for indk, k in enumerate(ks):
        mu, clusters = find_centers(X,k)
        Wks[indk] = np.log(Wk(mu, clusters))
        # Create B reference datasets
        B = 10
        BWkbs = np.zeros(B)
        for i in range(B):
            Xb = []
            for n in range(len(X)):
                Xb.append([random.uniform(xmin,xmax),
                          random.uniform(ymin,ymax)])
            Xb = np.array(Xb)
            mu, clusters = find_centers(Xb,k)
            BWkbs[i] = np.log(Wk(mu, clusters))
        Wkbs[indk] = sum(BWkbs)/B
        sk[indk] = np.sqrt(sum((BWkbs-Wkbs[indk])**2)/B)
    sk = sk*np.sqrt(1+1/B)
    return(ks, Wks, Wkbs, sk)

def getCordsList(fileRead, chain):
    cords_list = []
    realId_list = []

    while 1:

        data = fileRead.readline()

        if not data:
            break

        if(data[0]=='E' and data[1]=='N' and data[2]=='D'):
            break

        if(data[0]=='A' and data[1]=='T' and data[2]=='O' and data[21]==chain and data[13]=='C' and data[14]=='A'):

            val = utils.value_finder(22, 26, data)  
                        
            coord_x = float(utils.value_finder(30, 38, data))

            coord_y = float(utils.value_finder(38, 46, data))

            coord_z = float(utils.value_finder(46, 54, data))

        
            if not re.search('[a-zA-Z]+', val):
                real_id = int(val)

                coordinates = [coord_x,coord_y,coord_z]

                cords_list.append(coordinates)
                realId_list.append(real_id)

    return cords_list,realId_list

input_chains = ['1vfaB', '1duyA','1cneA', '2cblA', '1tdjA', '1dgkN']
path_to_pdb_files = 'All PDBs/'

for input_chain in input_chains:
    pdb = input_chain[:4].lower()
    chain = input_chain[4].lower()
    
    open_pdb = open(path_to_pdb_files+pdb+'.pdb','r') #Opening pdb file for k-means
    
    cords_list, realId_list = getCordsList(open_pdb, chain.upper())
    
    X = np.asarray(cords_list)

    ks, Wks, Wkbs, sk = gap_statistic(X)

    gap_statistic_value = []

    for i in range (len(ks)):
        gap_statistic_value.append(Wkbs[i] - Wks[i])

    print "Gap statistic value for ", input_chain
    print gap_statistic_value
    print
    print "sk values"
    print sk
    print
    for i in range (len(ks)-1):
        print gap_statistic_value[i] - gap_statistic_value[i+1] + sk[i+1]
