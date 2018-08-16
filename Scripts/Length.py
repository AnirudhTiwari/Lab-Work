'''
Module to calculate the Length of a given chain. This does so by processing the PDB file and counting
only the alpha carbons which are present ad data from CATHDomall is unreliable in terms of length 
as a lot of residues can be missing in the actual PDB.
'''

import common_functions as utils

path_to_pdb_files = 'All PDBs/'

def calculateLength(pdb, chain):
	pdb_file = open(path_to_pdb_files+pdb+'.pdb','r')
	coordinates_list = utils.getCoordinatesListFromPDB(pdb, chain)
	return len(coordinates_list)

