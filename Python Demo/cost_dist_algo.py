#!/usr/bin/env python
"""

DESCRIPTION

    TODO This describes how to use this script. This docstring
    will be printed by the script if there is an error or
    if the user requests help (-h or --help).

EXAMPLES

    TODO: Show some examples of how to use this script.

EXIT STATUS

    TODO: List exit codes

AUTHOR

    TODO: xiao <pku.xiao@gmail.com>

LICENSE

    This script is in the public domain, free from copyrights or restrictions.

VERSION

    $Id$
"""
import numpy
from heapq import *
#from pexpect import run, spawn

SOURCE_VALUE = 1
DIRN_MAT = numpy.array(range(9)).reshape(3,3)

def raster_neighbour_celllist(raster, key):
    """
    summary:
    get the cells which are neighbours of the cell specified by key

    input:
    raster: 2d ndarray
    key: (i,j) index

    return a tuple contains neighbours of cell(i,j), each element is an item as ((i,j),value)
    """
    #TODO
    r_w, r_h = raster.shape
    cell_list = []
    
    index_mat = [
        [(-1, -1), (-1, 0), (-1, 1)],
        [( 0, -1), (0,  0), ( 0, 1)],
        [( 1, -1), (1,  0), ( 1, 1)]] 
    if (key[0] == 0):
        index_mat = index_mat[1:]
    if (key[0] == r_w - 1):
        index_mat = index_mat[:len(index_mat)-1]
    if (key[1] == 0):
        for idx, item in enumerate(index_mat):
            index_mat[idx] = item[1:]
    if (key[1] == r_h - 1):
        for idx, item in enumerate(index_mat):
            index_mat[idx] = item[:len(index_mat) - 1]

    n_list = []
    for i in range(len(index_mat)):
        for j in range(len(index_mat[i])):
            n_list.append(index_mat[i][j])
    for item in n_list:
        if (item[0] == 0 and item[1] == 0):
            continue
        idi = key[0] + item[0]
        idj = key[1] + item[1]
        cell_list.append(((idi, idj), raster[idi, idj]))
    return cell_list

class LookupTable2d:
    def __init__(self):
        self.dict = {}
        #heap item: (dist_value, dirt_value, (i,j)//position)
        self.heap = []

    def __len__(self):
        return len(self.heap)

    def __str__(self):
        return str(self.heap)

    def add_elt(self, key, value):
        self.dict[key] = value
        heappush(self.heap,(value[0], value[1],key))

    def pop_min_elt(self):
        min_elt = heappop(self.heap)
        self.dict.pop(min_elt[2])
        print "pop min elt:\n", min_elt
        return min_elt

    def has_key(self, key):
        return self.dict.has_key(key)

    def update_elt(self, key, value):
        self.dict[key] = value
        #TODO: linear search in heap, oops, it is really slow
        for idx, item in enumerate(self.heap):
            if item[2] == key:
                self.heap[idx] = (value[0], value[1], key)
                break
    def get_value(self, key):
        return self.dict[key]

def lt2_to_darray(lt2, w, h):
    darray = numpy.zeros((w,h))

    for v in lt2.heap:
        print "set {0}, {1}, value {2}".format(v[2][0],v[2][1], v[0])
        darray[v[2][0], v[2][1]] = v[0]
    
    return darray

def calc_direction(st_pt, end_pt):
    """
    input:
    st_pt, tuple(i0,j0) represents the start point position
    end_pt, tuple(i1,j1) represents the end point position

    return:
    interger represents the direction from st_pt to end_pt
    """
    i = end_pt[0] - st_pt[0]
    j = end_pt[1] - st_pt[1]
    return DIRN_MAT[i + 1,j + 1]

def cost_dist(direction, v0,v1):
    """
    direction matrix is as following:
    0 1 2
    3 4 5
    6 7 8
    """
    if direction in [1,3,5,7]:
        return (v0 + v1) * 0.5
    elif direction in [0, 2, 6, 8]:
        return (v0 + v1) * 0.7071
    else:
        return 0

def calc_mct(sr,cmr):
    """
    input:
    sr: 2d ndarray contains the information about source region 
    cmr: 2d ndarray contains information about cost matrix

    return:
    mct: the minimum cost table
    """
    #init lt2: aat and mct
    aat = LookupTable2d()
    mct = LookupTable2d()

    #add source elt to the aat lookuptable_2d
    shape = sr.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
             if sr[i][j] == SOURCE_VALUE:
                 aat.add_elt((i,j),(0,4))

    #main loop
    while len(aat) != 0: #if aat is not empty
        print '-'*20, 'loop start', '-'*20
        print "current aat is:\n", aat
        (min_elt_cost, min_elt_dirt, min_elt_key) = aat.pop_min_elt()
        min_elt_value = (min_elt_cost,min_elt_dirt)
        print "add element to mct:\n pos({0},{1}), dist:{2},direction:{3}".format(min_elt_key[0], min_elt_key[1], min_elt_cost, min_elt_dirt)
        mct.add_elt(min_elt_key, min_elt_value)
        n_cell_list = raster_neighbour_celllist(cmr, min_elt_key)
        print "elt neigbhours are:\n", n_cell_list
        (i0,j0) = min_elt_key
        for n_cell in n_cell_list:
            if n_cell[1] == -1: #NULL Data cell skipped
                continue
            (i1, j1) = n_cell[0]
            #check (i1,j1) is already in mct
            if mct.has_key((i1,j1)) == False:
                v0 = cmr[i0,j0]
                v1 = cmr[i1,j1]
                direction = calc_direction((i0,j0),(i1,j1))
                accu_value = cost_dist(direction,v0,v1)
                if (aat.has_key((i1,j1)) == False):
                    aat.add_elt((i1,j1), (accu_value + min_elt_cost, direction))
                    print "add element to aat\n pos:{0}, cost:{1}, dirt:{2}".format((i1,j1), \
                    accu_value + min_elt_cost, direction)
                elif (accu_value + min_elt_cost < aat.get_value((i1,j1))[0]):
                    print "update element in aat\n pos:{0}, cost:{1}, dirt:{2}".format((i1,j1), \
                    accu_value + min_elt_cost, direction)
                    aat.update_elt((i1,j1), (accu_value + min_elt_cost, direction))
    return mct
