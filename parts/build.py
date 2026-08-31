import re, os
art = open('art.svg').read()
emblem = open('emblem.svg').read()
shirt = open('shirt.svg').read()
back = open('back.html').read()
front = open('front.html').read()
out = '..'

def w(name, s):
    open(os.path.join(out, name), 'w').write(s)
    print(name, len(s))

# Main
m = open('Main.tpl').read().replace('<!--ART-->', art)
w('Main.dc.html', m)

# Peito
p = open('Peito.tpl').read().replace('<!--EMBLEM-->', emblem)
w('Peito.dc.html', p)

# Direcoes
for n in ('DirecaoB', 'DirecaoC'):
    w(n + '.dc.html', open(n + '.tpl').read().replace('<!--ART-->', art))

# Mockup
frente = shirt.replace('__COLLAR__', 'M155,46 C163,68 179,80 200,80 C221,80 237,68 245,46')
costas = shirt.replace('__COLLAR__', 'M154,45 C164,60 180,66 200,66 C220,66 236,60 246,45')
mk = open('Mockup.tpl').read()
mk = mk.replace('<!--SHIRT_FRONT-->', frente).replace('<!--SHIRT_BACK-->', costas)
mk = mk.replace('<!--FRONTDESIGN-->', front.replace('__GOLD__', '#C6A15B').replace('<!--EMBLEM-->', emblem))
mk = mk.replace('<!--BACKDESIGN-->', back.replace('__GOLD__', '#C6A15B').replace('<!--ART-->', art))
w('Mockup.dc.html', mk)
