import GTC

def Solve(A,B):
    """
    https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/pseudinv.htm
    If A is a square matrix of full rank, then the inverse of A exists (A is referred to as an invertible matrix) and
    
    Ax = b has the solution x = pinv(A)b 
    pinv(A) = inv(AtxA)xA' 
    
    :param A: 
    :param B: 
    :return: 
    """
    At=GTC.la.transpose(A)
    AtxA=GTC.la.dot(At,A)
    inv_AtxA=GTC.la.inv(AtxA)
    pinvA=GTC.la.dot(inv_AtxA,GTC.la.transpose(A))
    X=GTC.la.dot(pinvA,B)
    return X
#AX=B

a=[[-2,3],[-4,1],[1,1]]
b=[-4,2,-2.95]

A=GTC.la.uarray(a)
B=GTC.la.uarray(b)

X=Solve(A,B)
print('X=',X)

z=[(1,2),(3,4),(1,-3)]

for x,y in z:
    print('x=',x,'y=',y)