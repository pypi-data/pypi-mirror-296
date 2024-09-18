import numpy as np



def submatrix(M, i, j):
    """
    submatrix(M, i, j)
    
    Returns a copy of M with the i-th row(s) and j-th column(s) removed.
    
    Parameters
    ----------
    M : 2-D array_like
        Matrix, from which the row and column should be removed.
    i : slice, int or array of ints
        Index/Indices of the row(s) that should be removed.
    j : slice, int or array of ints
        Index/Indices of the column(s) that should be removed.
    
    Returns
    -------
    out : ndarray
        A copy of M with the i-th row(s) and j-th column(s) removed.
    """
    return np.delete(np.delete(M, i, 0), j, 1)



def minor(M, i, j):
    """
    minor(M, i, j)
    
    Returns the (i, j) minor of M.
    
    Parameters
    ----------
    M : 2-D array_like
        Matrix, from which the minor should be calculated.
    i : slice, int or array of ints
        Index/Indices of the row(s) that should be removed.
    j : slice, int or array of ints
        Index/Indices of the column(s) that should be removed.
    
    Returns
    -------
    out : ndarray
        The the (i, j) minor of M.
    """
    return np.linalg.det(submatrix(M, i, j))



def adj(M):
    """
    adj(M)
    
    Returns the adjugate of M.
    
    Parameters
    ----------
    M : 2-D array_like
        Matrix, from which the adjugate should be calculated.
    
    Returns
    -------
    out : ndarray
        The adjugate of M.
    """
    adjM = np.zeros_like(M)
    for i in range(adjM.shape[0]):
        for j in range(adjM.shape[1]):
            adjM[i, j] = (-1)**(i+j) * minor(M, j, i)
    return adjM



def cof(M):
    """
    cof(M)
    
    Returns the cofactor matrix of M.
    
    Parameters
    ----------
    M : 2-D array_like
        Matrix, from which the cofactor matrix should be calculated.
    
    Returns
    -------
    out : ndarray
        The cofactor matrix of M.
    """
    return adj(M).T
