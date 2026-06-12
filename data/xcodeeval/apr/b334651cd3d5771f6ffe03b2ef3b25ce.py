l, r = list( map( int, input().split() ) )

def cnt( x ) :
    ret = 0
    for i in range( 1, x+1 ):
        s = str(i)
        if s[0] == s[-1]:
            ret += 1
            #print(s)
    return ( ret )

def cnt2( x ):

    ret = 0
    s = str(x)
    L = len(s)

    if L >= 2 and x == 10**(L-1):
        return ( cnt2( 10**(L-1)-1 ) )

    if L <= 1:
        return ( x )
    elif L <= 2:
        while x//10 != x%10:
            x -= 1
        return ( 9 + x//10 )
    else:
        ret = int( "1" + "0"*(L-3) + "8" )
        num = list( str(x) )
        #print( num )
        if num[0] != num[-1]:
            if int(num[0]) > int( num[-1] ):
                how = int(num[-1]) + 10-int(num[0])
            else:
                how = int(num[-1]) - int(num[0])
            x -= how
        num = str(x)
        d = x % 10
        #print( 'num',num )
        #print( 'd', d )
        #print( 'num', num, 'ret before', ret )
        ret += ( int(d-1) ) * int( "9" * (L-2) ) + int( num[1:-1] ) + int(d)

    return ( ret )

#print( cnt(1024), cnt2(1024) )
#print( cnt(47), cnt2(47) )
#print( cnt(9), cnt2(9) )
#print( cnt(58), cnt2(58) )
#print( cnt(999), cnt2(999) )
#print( cnt(8987), cnt2(8987) )
#print()
#print( cnt(99999), cnt2(99999) )
#print( cnt(99899), cnt2(99899) )
#print( cnt(1000), cnt2(1000) )
#print( cnt2(1) )
#exit(0)
    
print( cnt2(r) - cnt(l-1) )