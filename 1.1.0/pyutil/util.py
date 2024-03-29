"""
util
------------------------------------------------------------------
This module provides several funcions for easier programming
written by using Python3.

usage : 
    import pyutil.util as MODULENAME
    from pyutil.util import FUNCTION

functions :
    .call_error(string_1, string_2)
    .assert_num(number)
    .assert_file(filename, ERR=True)
    .get_line(string, filename, iLine=0)
    .get_lines(string, filename, nLine=1, iBlock=0)
    .get_path(path, n=0)
    .chk_len(list, n, fin=True, bool=False)
    .angle(vector_1, vector_2) 
    .dir_to_cart(lattice_vector, coordinate, inbox=True)
    .cart_to_dir(lattice_vector, coordinate, inbox=True)
    .lvec_rebuild(lattice_vector)

"""

import numpy as np
import os

def assert_num(dat):
    """
assert_num(dat):
------------------------------------------------------------------
check whether given data 'dat' is a number or not.
if a number, return 'True', else, return 'False'.

    """
    dtype = str(np.array([dat]).dtype)
    
    if 'int' in dtype or 'float' in dtype or 'complex' in dtype:
        return True
    else:
        return False

def assert_file(f_name, ERR=True):
    """
assert_file(f_name, callerr=True)
------------------------------------------------------------------
check whether file 'f_name' exists or not. 

if file exists, return True.
if file does not exist, 
    ERR = False : return False.
    ERR = True  : stop

    """
    if os.path.isfile(f_name):
        return True
    else:
        if ERR: 
            raise FileNotFoundError(f_name)
        return False          
        
def get_line(str, f_name, iLine=0):
    """
get_line(str, f_name, iLine=0)
------------------------------------------------------------------
open file 'f_name' and take a line that contains string 'str'
and return. if there is no line contins 'str', return 'None'.

    iLine = 0     : return last one line, default
    iLine > 0     : return 'iLine'-th line.
                    if 'iLine' is larger than number of lines, 
                    return last one line.
    iLine = 'all' : return all lines.

    """
    assert_file(f_name)
    comm = 'grep \'{}\' {}'.format(str, f_name)
    nLine = int(os.popen(comm+' | wc -l').read())
    if (nLine == 0): return None
    if (type(iLine) == int) or (type(iLine) == float):
        if iLine <= 0 or iLine >= nLine:
            option = '| tail -1'
        else:
            option = '| head -{} | tail -1'.format(int(iLine))
        return os.popen(comm+option).read().split()
    elif iLine[0] == 'a':
        buf = os.popen(comm).read().split('\n')
        return [line.split() for line in buf[:-1]]      
    else:
        raise ValueError('wrong input for iLine - {}'.format(iLine))

def get_lines(str, f_name, nLine=1, iBlock=0):
    """
get_lines(str, f_name, nline=1, iBlock=0)
------------------------------------------------------------------
open file 'f_name' and find a line that contains string 'str'.
Then capture the following 'nline' lines and return. if there is 
no line contains 'str', return None
    
    iBlock = 0     : return last one block.
    iBlock > 0     : return 'iBlock'-th block.
                     if 'iBlock' is larger than number of lines, 
                     return last one block.
    iBlock = 'all' : return all blocks.

    """
    assert_file(f_name)
    nBlock = int(os.popen('grep \'{}\' {} | wc -l'.format(str, f_name)).read())
    if nBlock == 0: 
        return None
    if type(iBlock) == int or type(iBlock) == float:
        iBlock = int(iBlock)
        getall = False
        if iBlock == 0 or nBlock < iBlock: 
            iBlock = nBlock
    elif iBlock[0] == 'a':
        blocks = []
        getall = True
    else:
        raise ValueError('wrong input for iBlock - {}'.format(iBlock))
    icount = 0
    with open(f_name) as f:
        for line in f:
            if str in line:
                icount += 1
                if (not getall) and icount == iBlock:
                    lines = [f.readline().split('\n')[0].split() 
                        for i in range(nLine)]
                    return lines
                elif getall:
                    lines = [f.readline().split('\n')[0].split() 
                        for i in range(nLine)]
                    blocks.append(lines)
                    if icount == nBlock: 
                        return blocks

def get_path(path, n=0):
    """
get_path(path, n=0)
------------------------------------------------------------------
if input 'path' include filename at the end, return 'path' without 
filename. if integer n is larger than 0, substract 'n' directories
from the end in 'path' and return.

    """
    isfile = False
    if '~' in path: path = os.path.expanduser(path)
    if type(n) is not int: n=0
    if n < 0: n = 0
    isfile = assert_file(path)
    if isfile:
        path_buf = path.split('/')
        path = ''
        for dir in path_buf[:-1]: path += dir+'/'
    if n == 0: return path
    if (len(path.split('/')) - n - 1 < 0): return path
    path_buf = path.replace('/',' ').split()
    path = ''
    for dir in path_buf[:-n]: path += dir+'/'
    return path

def chk_len(dat, n, ERR=True, BOOL=False):
    """ 
chk_len(dat, n, ERR=True, bool=False)
------------------------------------------------------------------
check whether the first dimension of input array 'dat' (m) 
is larger than input integer 'n'.

    m > n              : return dat[n]
    m < n && ERR = T   : exit
    m < n && ERR = F   : return m 
    BOOL = T && m == n : return True
    BOOL = T && m != n : return False

    """
    if type(n) is not int: 
        raise ValueError('wrong input for n - {}'.format(n))
    if BOOL:
        if np.shape(dat)[0] == n: return True
        if np.shape(dat)[0] != n: return False
    else:
        if np.shape(dat)[0] <= n:
            if ERR: 
                raise ValueError('wrong input length for dat - ({} < {})'.format(np.shape(dat)[0]-1, n)) 
            else: 
                return np.shape(dat)[0]
        else:
            return list[n]

def angle(vec1, vec2):
    """
angle(vec1, vec2)
------------------------------------------------------------------
return angle between two vectors, 'vec1' and 'vec2' using arccos.

    """
    if np.shape(vec1) != (3,):
        raise ValueError('wrong input dimension for vec1 - {}'.format(np.shape(vec1)))
    if np.shape(vec2) != (3,):
        raise ValueError('wrong input dimension for vec2 - {}'.format(np.shape(vec2)))
    len1 = np.sqrt(np.sum(vec1*vec1,dtype=np.float))
    len2 = np.sqrt(np.sum(vec2*vec2,dtype=np.float))
 
    if len1 == 0 or len2 == 0: 
        return np.float(0)
    else:
        return np.arccos(np.sqrt(np.sum(vec1*vec2/(len1*len2),dtype=np.float)))

def dir_to_cart(lvec, coo, inbox=True):
    """
dir_to_cart(lvec, coo, inbox=True
------------------------------------------------------------------
convert fractional coordinate to cartesian and return.

    lvec  : lattice vector (dim: 3*3)
    coo   : fractional coordinate in xyz (dim: n*3)
    inbox : if True, move atoms into the lattice

    """
    if np.shape(lvec) != (3,3):
        raise ValueError('wrong input dimension for lvec - {}'.format(np.shape(lvec)))
    if not ((len(np.shape(coo)) is 1 and np.shape(coo)[0] is 3) or (
            len(np.shape(coo)) is 2 and np.shape(coo)[1] is 3)):
        raise ValueError('wrong input dimension for coo - {}'.format(np.shape(coo)))
     
    latconts = np.sqrt(np.sum(lvec*lvec,axis=1),dtype=np.float)
    
    alp  = angle(lvec[1], lvec[2])
    bet  = angle(lvec[2], lvec[0])
    gam  = angle(lvec[0], lvec[1])
    cosa = np.cos(alp,dtype=np.float)
    cosb = np.cos(bet,dtype=np.float)
    cosg = np.cos(gam,dtype=np.float)
    sing = np.sin(gam,dtype=np.float)

    vol  = np.prod(latconts,dtype=np.float)*np.sqrt(
            np.float(1) - cosa**2 - cosb**2 - 
            cosg**2 + np.float(2)*cosa*cosb*cosg,dtype=np.float)
 
    convm = np.zeros([3,3],dtype=np.float)

    convm[0][0] = latconts[0]
    convm[0][1] = latconts[1]*cosg
    convm[0][2] = latconts[2]*cosb

    convm[1][1] = latconts[1]*sing
    convm[1][1] = latconts[2]*(cosa - cosb*cosg)/sing

    convm[2][2] = vol/(latconts[0]*latconts[1]*sing)

    coo_out = np.array(coo)
    if len(np.shape(coo_out)) == 1:
        coo_out = coo_out.reshape(1,3)

    nAtom = np.shape(coo_out)[0]
     
    for i in range(nAtom):
        if inbox:
            for j in range(3):
                while coo_out[i][j] >= 1: 
                    coo_out[i][j] -= np.float(1.)
                while coo_out[i][j] <  0: 
                    coo_out[i][j] += np.float(1.)
        coo_out[i][:] = np.matmul(convm, coo_out[i])

    if nAtom == 1:
        coo_out = coo_out[0]
    
    return coo_out

def cart_to_dir(lvec, coo, inbox=True):
    """
cart_to_dir(lvec, coo, inbox=True)
------------------------------------------------------------------
convert cartesian coordinate to fractional and return.

    lvec  : lattice vector (dim: 3*3)
    coo   : cartesian coordinate in xyz (dim: n*3)
    inbox : if True, move atoms into the lattice

    """
    if np.shape(lvec) != (3,3):
        raise ValueError('wrong input dimension for lvec - {}'.format(np.shape(lvec)))
    if not ((len(np.shape(coo)) is 1 and np.shape(coo)[0] is 3) or (
            len(np.shape(coo)) is 2 and np.shape(coo)[1] is 3)):
        raise ValueError('wrong input dimension for coo - {}'.format(np.shape(coo)))
     
    latconts = np.sqrt(np.sum(lvec*lvec,axis=1),dtype=np.float)
    alp  = angle(lvec[1], lvec[2])
    bet  = angle(lvec[2], lvec[0])
    gam  = angle(lvec[0], lvec[1])
    cosa = np.cos(alp,dtype=np.float)
    cosb = np.cos(bet,dtype=np.float)
    cosg = np.cos(gam,dtype=np.float)
    sing = np.sin(gam,dtype=np.float)
    vol  = np.prod(latconts,dtype=np.float)*np.sqrt(
            np.float(1) - cosa**2 - cosb**2 - 
            cosg**2 + np.float(2)*cosa*cosb*cosg,dtype=np.float)
 
    convm       = np.zeros([3,3],dtype=np.float)    

    convm[0][0] = np.float(1)/latconts[0]
    convm[0][1] = -cosg/(latconts[0]*sing)
    convm[0][2] = latconts[1]*latconts[2]*(cosg*cosa - cosb)/(sing*vol)
    
    convm[1][1] = np.float(1)/(latconts[1]*sing)
    convm[1][2] = latconts[0]*latconts[2]*(cosb*cosg - cosa)/(sing*vol)

    convm[2][2] = latconts[0]*latconts[1]*sing/vol

    coo_out = np.array(coo)
    if len(np.shape(coo_out)) == 1:
        coo_out = coo_out.reshape(1,3)

    nAtom = np.shape(coo_out)[0]

    for i in range(nAtom):
        coo_out[i] = np.matmul(convm, coo_out[i])
        if inbox:
            for j in range(3):
                while coo_out[i][j] >= 1: 
                    coo_out[i][j] -= np.float(1.)
                while coo_out[i][j] <  0: 
                    coo_out[i][j] += np.float(1.)
    if nAtom == 1:
        coo_out = coo_out[0]
    
    return coo_out

def lvec_rebuild(lvec):
    """
lvec_rebuild(lvec)
------------------------------------------------------------------
rebuild lattice vector 'lvec' and return.

    """
    if np.shape(lvec) != (3,3):
        raise ValueError('wrong input dimension for lvec - {}'.format(np.shape(lvec)))
    latconts = np.sqrt(np.sum(lvec*lvec,axis=1),dtype=np.float)
    alp  = angle(lvec[1], lvec[2])
    bet  = angle(lvec[2], lvec[0])
    gam  = angle(lvec[0], lvec[1])
    cosa = np.cos(alp,dtype=np.float)
    cosb = np.cos(bet,dtype=np.float)
    cosg = np.cos(gam,dtype=np.float)
    
    mat = np.zeros([3,3], dtype=np.float)
 
    mat[0][0] = latconts[0]
    mat[1][0] = latconts[1]*cosg
    mat[1][1] = np.sqrt(latconts[1]**2 - mat[1][0]**2,dtype=np.float)
    mat[2][0] = latconts[2]*cosb
    mat[2][1] = (cosa*latconts[1]*latconts[2] - mat[1][0]*mat[2][0])/mat[1][1]
    mat[2][2] = np.sqrt(latconts[2]**2 - mat[2][0]**2 - mat[2][1]**2,dtype=np.float)
    return mat

