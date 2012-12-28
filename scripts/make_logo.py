import Image, ImageDraw

im = Image.new("RGB", (800,600), (255,255,255))
import math
draw = ImageDraw.Draw(im)
coseno = lambda angle: math.cos(math.radians(angle))
seno = lambda angle: math.sin(math.radians(angle))
aseno = lambda x: math.asin(x)

omega1 = 360.0/3

c1fr1 = lambda r1: 2*r1*seno(omega1)
c2fr2 = lambda r2: 2*r2*seno(omega2)
c1fd1 = lambda r1,d1: 2*math.sqrt(r1**2-d1**2)
c2fd2 = lambda r2,d2: 2*math.sqrt(r2**2-d2**2)
r2fr1 = lambda r1: (r1*seno(omega1/2.0))/seno(omega2/2.0)
omeg2fr1 = lambda c, r1:  math.degrees(2*aseno(float(c)/(2*r1)))

center = lambda x,y,r: (x-r, y-r, x+r, y+r)

r1 = 100
r2 = r1*3
c1 = c1fr1(r1)
c2 = c1
omega2 = omeg2fr1(c1, r2)

#d2 ? e d1 ?
d2fc2 = lambda c2, r2: math.sqrt((r2**2)-((c2**2)/4.0))
d1fc1 = lambda c1, r1: math.sqrt((r1**2)-((c1**2)/4.0))
d2 = d2fc2(c2, r2)
d1 = d1fc1(c1, r1)

#alfa1 ?
alfa1fomega1 = lambda omega1: 90-(omega1/2.0)
deltaxfalfa = lambda alfa1, d1, d2: coseno(alfa1)*(d1 + d2)
deltayfalfa = lambda alfa1, d1, d2: seno(alfa1)*(d1 + d2)

alfa1 = alfa1fomega1(omega1)
deltax = deltaxfalfa(alfa1, d1, d2)
deltay = deltayfalfa(alfa1, d1, d2)

print c1, omega2, omega1, d2, d1, alfa1, deltax, deltay



draw.line((400, 300, 400+c1, 300), fill='#ff0000')#red
draw.line((400, 310, 400+d2, 310), fill='#00ff00')#green
draw.line((400, 320, 400+d1, 320), fill='#0000ff')#blue

draw.arc(center(400, 300, r1), 0, 360, fill='#cccccc')
draw.arc(center(int(400-deltax), int(300+deltay), int(r2)), 0, 360, fill='#00ffff')
draw.arc(center(int(400+deltax), int(300+deltay), int(r2)), 0, 360, fill='#00ffff')
draw.arc(center(int(400), int(300-d2-d1), int(r2)), 0, 360, fill='#00ffff')

#px1 = r1*coseno(30)
#py1 = r1*seno(30)
#for i in range(16):
#    draw.line((400-px1, 300+py1, 400, 300-(float(r1)/15)*i), fill=128)
#    draw.line((400+px1, 300+py1, 400, 300-(float(r1)/15)*i), fill=128)
#
#del draw 

im.save(open('logo.png', 'wb'), "PNG")