k , a , b , v = map( int , input( ).split( ) )
s = 0
while  a > 0 :
    a -= min( k , b + 1 ) * v
    b -= min( k - 1 , b )
    s += 1
print( s )