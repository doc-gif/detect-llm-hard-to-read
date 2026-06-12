i = str(input())
f = str(input())
ti = int(f"{i[0]}{i[1]}")*60 + int(f"{i[3]}{i[4]}")
tf = int(f"{f[0]}{f[1]}")*60 + int(f"{f[3]}{f[4]}")
m = (ti+tf)/2
tm = ti+(tf-m)
if (int(tm//60)>=10 and int(tm%60)>=10):
  print(f"{int(tm//60)}:{int(tm%60)}")
elif int(tm//60)>=10 and int(tm%60)<10:
  print(f"{int(tm//60)}:0{int(tm%60)}")
elif int(tm//60)<10 and int(tm%60)>=10:
  print(f"0{int(tm//60)}:{int(tm%60)}")
else:
  print(f"0{int(tm//60)}:0{int(tm%60)}")