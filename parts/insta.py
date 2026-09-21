# -*- coding: utf-8 -*-
"""Identidade do @quisutdeusatelie — ateliê de terços.

Desenha o terço (conta, fio, medalha e cruz) e monta com ele três direções
delicadas, a folha de fotos e a prévia do perfil, em ../instagram/.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'instagram')
os.makedirs(OUT, exist_ok=True)

CORM = "'Cormorant Garamond', Georgia, serif"

SHELL = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <link rel="stylesheet" href="%s">
  <style>
    body { margin: 0; font-family: %s; }
    a { color: #A9874B; } a:hover { color: #8C6B34; }
  </style>
</helmet>
%s
</x-dc>
<script data-dc-script data-props='%s'>
class Component extends DCLogic {}
</script>
</body>
</html>
"""

GRAIN = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' "
         "height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' "
         "baseFrequency='.82' numOctaves='3'/%3E%3C/filter%3E%3Crect width='180' "
         "height='180' filter='url(%23n)'/%3E%3C/svg%3E\")")

FONTS_IT = ('https://fonts.googleapis.com/css2?family=Italiana&family=Cormorant+Garamond:'
            'ital,wght@0,300;0,400;1,300;1,400&display=swap')
FONTS_TS = ('https://fonts.googleapis.com/css2?family=Tenor+Sans&family=Cormorant+Garamond:'
            'ital,wght@0,300;0,400;1,300;1,400&display=swap')
FONTS_MA = ('https://fonts.googleapis.com/css2?family=Marcellus&family=Cormorant+Garamond:'
            'ital,wght@0,300;0,400;1,300;1,400&display=swap')


def write(name, fonts, root, w, h):
    props = json.dumps({"$preview": {"width": w, "height": h}}, ensure_ascii=False)
    open(os.path.join(OUT, name), 'w').write(SHELL % (fonts, CORM, root, props))
    print(name)


# ====================================================================== o terço
def bead(cx, cy, r, uid, kind='a'):
    return ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="url(#%s-%s)" stroke="url(#%s-edge)" '
            'stroke-width="%.2f"/>' % (cx, cy, r, uid, kind, uid, r * 0.07))


def gradients(uid, hi, mid, lo, edge):
    """A conta é volume, não contorno: claro no alto à esquerda, escuro na borda."""
    def rg(name, cx, cy, r):
        return ('<radialGradient id="%s-%s" cx="%s" cy="%s" r="%s">'
                '<stop offset="0" stop-color="%s"/>'
                '<stop offset=".46" stop-color="%s"/>'
                '<stop offset="1" stop-color="%s"/></radialGradient>'
                % (uid, name, cx, cy, r, hi, mid, lo))
    return ('<defs>%s%s<linearGradient id="%s-edge" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="%s" stop-opacity=".55"/>'
            '<stop offset="1" stop-color="%s" stop-opacity=".95"/></linearGradient></defs>'
            % (rg('a', '34%', '28%', '78%'), rg('p', '32%', '26%', '80%'), uid, edge, edge))


def rosary(uid, hi, mid, lo, edge, thread, cross_hi, cross_lo, glow=None):
    """Terço inteiro: cinco dezenas, medalha, pendente e cruz."""
    cx, cy, R = 300.0, 322.0, 208.0
    r_a, r_p = 10.2, 15.4
    seq = []                       # (é pater, peso antes)
    for _ in range(5):
        seq.append((True, 1.9))
        seq += [(False, 1.0)] * 10
    total = sum(w for _, w in seq) + 1.9
    span = math.radians(336.0)
    start = math.radians(90.0) + math.radians(12.0)
    beads, acc = [], 0.0
    for is_p, w in seq:
        acc += w
        ang = start + span * (acc / total)
        bx, by = cx + R * math.cos(ang), cy + R * math.sin(ang)
        beads.append(bead(bx, by, r_p if is_p else r_a, uid, 'p' if is_p else 'a'))

    a0, a1 = start, start + span
    p0 = (cx + R * math.cos(a0), cy + R * math.sin(a0))
    p1 = (cx + R * math.cos(a1), cy + R * math.sin(a1))
    thread_ring = ('<path d="M%.1f,%.1f A%.0f,%.0f 0 1 1 %.1f,%.1f" fill="none" stroke="%s" '
                   'stroke-width="1.5" stroke-linecap="round" opacity=".75"/>'
                   % (p0[0], p0[1], R, R, p1[0], p1[1], thread))

    my = cy + R + 26
    medal = ('<path d="M%.1f,%.1f L300,%.1f M300,%.1f L%.1f,%.1f" fill="none" stroke="%s" '
             'stroke-width="1.5" opacity=".75"/>'
             '<ellipse cx="300" cy="%.1f" rx="21" ry="26" fill="url(#%s-p)" '
             'stroke="url(#%s-edge)" stroke-width="1.1"/>'
             '<ellipse cx="300" cy="%.1f" rx="13" ry="17.5" fill="none" stroke="%s" '
             'stroke-width="1" opacity=".55"/>'
             % (p0[0], p0[1], my - 26, my - 26, p1[0], p1[1], thread,
                my, uid, uid, my, thread))

    ys = [my + 52, my + 86, my + 114, my + 142, my + 194]
    pend = ('<path d="M300,%.1f L300,%.1f" fill="none" stroke="%s" stroke-width="1.5" '
            'opacity=".75"/>' % (my + 26, ys[-1] + 6, thread))
    pend += bead(300, ys[0], r_p, uid, 'p')
    for y in ys[1:4]:
        pend += bead(300, y, r_a, uid, 'a')
    pend += bead(300, ys[4], r_p, uid, 'p')

    ct = ys[4] + 24
    cross = ('<defs><linearGradient id="%s-cr" x1="0" y1="0" x2="1" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
             '</linearGradient></defs>'
             '<path d="M291,%.1f L309,%.1f L309,%.1f L344,%.1f L344,%.1f L309,%.1f '
             'L309,%.1f L291,%.1f L291,%.1f L256,%.1f L256,%.1f L291,%.1f Z" '
             'fill="url(#%s-cr)" stroke="%s" stroke-width="1" stroke-linejoin="round"/>'
             '<path d="M300,%.1f L300,%.1f M267,%.1f L333,%.1f" stroke="%s" '
             'stroke-width="1" opacity=".45" fill="none"/>'
             % (uid, cross_hi, cross_lo,
                ct, ct, ct + 46, ct + 46, ct + 64, ct + 64,
                ct + 168, ct + 168, ct + 64, ct + 64, ct + 46, ct + 46,
                uid, lo,
                ct + 12, ct + 156, ct + 55, ct + 55, lo))

    shade = ('filter: drop-shadow(0 10px 22px %s);' % glow) if glow else ''
    return ('<svg viewBox="0 0 600 900" xmlns="http://www.w3.org/2000/svg" '
            'style="width:100%%; height:auto; display:block; %s">%s%s%s%s%s%s</svg>'
            % (shade, gradients(uid, hi, mid, lo, edge), thread_ring,
               ''.join(beads), medal, pend, cross))


def dezena(uid, hi, mid, lo, edge, thread, cross_hi, cross_lo):
    """Dezena de mão — o desenho do avatar: dez contas, medalha e cruz."""
    cx, cy, R, r_a = 150.0, 150.0, 98.0, 11.0
    beads = ''
    for i in range(10):
        ang = math.radians(108.0) + math.radians(324.0) * (i + 1) / 11.0
        beads += bead(cx + R * math.cos(ang), cy + R * math.sin(ang), r_a, uid, 'a')
    a0 = math.radians(108.0)
    a1 = a0 + math.radians(324.0)
    p0 = (cx + R * math.cos(a0), cy + R * math.sin(a0))
    p1 = (cx + R * math.cos(a1), cy + R * math.sin(a1))
    ring = ('<path d="M%.1f,%.1f A%.0f,%.0f 0 1 1 %.1f,%.1f" fill="none" stroke="%s" '
            'stroke-width="1.6" stroke-linecap="round" opacity=".7"/>'
            % (p0[0], p0[1], R, R, p1[0], p1[1], thread))
    my = cy + R + 22
    stem = ('<path d="M%.1f,%.1f L150,%.1f M150,%.1f L%.1f,%.1f M150,%.1f L150,%.1f" '
            'fill="none" stroke="%s" stroke-width="1.6" opacity=".7"/>'
            % (p0[0], p0[1], my - 14, my - 14, p1[0], p1[1], my + 12, my + 30, thread))
    knot = bead(150, my, 13.5, uid, 'p')
    ct = my + 30
    cross = ('<defs><linearGradient id="%s-cr" x1="0" y1="0" x2="1" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
             '</linearGradient></defs>'
             '<path d="M143,%.1f L157,%.1f L157,%.1f L186,%.1f L186,%.1f L157,%.1f '
             'L157,%.1f L143,%.1f L143,%.1f L114,%.1f L114,%.1f L143,%.1f Z" '
             'fill="url(#%s-cr)" stroke="%s" stroke-width=".9" stroke-linejoin="round"/>'
             % (uid, cross_hi, cross_lo,
                ct, ct, ct + 34, ct + 34, ct + 48, ct + 48,
                ct + 122, ct + 122, ct + 48, ct + 48, ct + 34, ct + 34, uid, lo))
    return ('<svg viewBox="0 0 300 460" xmlns="http://www.w3.org/2000/svg" '
            'style="width:100%%; height:auto; display:block">%s%s%s%s%s</svg>'
            % (gradients(uid, hi, mid, lo, edge), ring, beads, stem + knot, cross))


# ================================================================ peças de apoio
def photo_slot(w, h, bg, frame_col, label_col, label, note='', radius='0'):
    return (
        '<div style="position: relative; width: %s; height: %s; border-radius: %s; '
        'background: linear-gradient(150deg, %s 0%%, rgba(0,0,0,.08) 100%%); '
        'display: flex; flex-direction: column; align-items: center; justify-content: center; '
        'gap: 13px; overflow: hidden; box-shadow: inset 0 0 0 1px %s">'
        '<div style="position: absolute; inset: 0; background-image: %s; '
        'background-size: 180px 180px; opacity: .07; pointer-events: none"></div>'
        '<svg viewBox="0 0 48 48" width="32" height="32" style="display:block; fill:none; '
        'stroke:%s; stroke-width:1; stroke-linecap:round">'
        '<path d="M6 13 L42 13 L42 37 L6 37 Z"/><path d="M6 31 L17 21 L27 31"/>'
        '<path d="M24 28 L31 22 L42 32"/><circle cx="33" cy="19" r="3"/></svg>'
        '<div style="font-family: %s; font-size: 18px; letter-spacing: .3em; color: %s; '
        'text-indent: .3em; text-align: center">%s</div>%s</div>'
        % (w, h, radius, bg, frame_col, GRAIN, label_col, CORM, label_col, label,
           ('<div style="font-family: %s; font-style: italic; font-size: 18px; '
            'line-height: 1.4; color: %s; opacity: .85; text-align: center; '
            'max-width: 74%%">%s</div>' % (CORM, label_col, note)) if note else ''))


def swatches(items, label_col):
    return ''.join(
        '<div style="display: flex; flex-direction: column; align-items: center; gap: 9px">'
        '<div style="width: 38px; height: 38px; border-radius: 50%%; background: %s; '
        'box-shadow: inset 0 0 0 1px rgba(0,0,0,.12)"></div>'
        '<div style="font-family: %s; font-size: 13px; letter-spacing: .14em; color: %s">%s</div>'
        '</div>' % (h, CORM, label_col, h.replace('#', '')) for h in items)


def thumb(bg, inner, border='rgba(0,0,0,.1)'):
    return ('<div style="width: 110px; height: 110px; background: %s; display: flex; '
            'align-items: center; justify-content: center; box-shadow: inset 0 0 0 1px %s; '
            'overflow: hidden">%s</div>' % (bg, border, inner))


def mini_photo(bg, col, border='rgba(0,0,0,.1)'):
    return thumb(bg, '<div style="display: flex; flex-direction: column; align-items: center; '
                 'gap: 6px"><svg viewBox="0 0 48 48" width="22" height="22" '
                 'style="display:block; fill:none; stroke:%s; stroke-width:1.1">'
                 '<path d="M6 13 L42 13 L42 37 L6 37 Z"/><path d="M6 31 L17 21 L27 31"/>'
                 '<circle cx="33" cy="19" r="3"/></svg>'
                 '<div style="font-family: %s; font-size: 12px; letter-spacing: .22em; '
                 'color: %s; text-indent: .22em">FOTO</div></div>' % (col, CORM, col), border)


def band(bg, ink, soft, name, note, palette, thumbs):
    return (
        '<div style="width: 1080px; height: 320px; background: %s; display: flex; '
        'align-items: center; gap: 36px; padding: 0 56px; box-sizing: border-box; '
        'border-top: 1px solid rgba(0,0,0,.09)">'
        '<div style="display: flex; flex-direction: column; gap: 9px; width: 244px; flex-shrink: 0">'
        '<div style="font-family: %s; font-size: 15px; letter-spacing: .3em; color: %s; '
        'text-indent: .3em">DIRE&#199;&#195;O</div>'
        '<div style="font-family: %s; font-style: italic; font-size: 33px; line-height: 1.15; '
        'color: %s">%s</div>'
        '<div style="font-family: %s; font-size: 17px; line-height: 1.5; color: %s">%s</div></div>'
        '<div style="display: flex; gap: 10px">%s</div>'
        '<div style="display: flex; gap: 13px; margin-left: auto">%s</div></div>'
        % (bg, CORM, soft, CORM, ink, name, CORM, soft, note, thumbs,
           swatches(palette, soft)))


def avatar_disc(bg, ring, mark):
    return ('<div style="width: 132px; height: 132px; border-radius: 50%%; background: %s; '
            'box-shadow: inset 0 0 0 1px %s; display: flex; align-items: center; '
            'justify-content: center; flex-shrink: 0; overflow: hidden">%s</div>'
            % (bg, ring, mark))


# ==================================================== A · Madeira e linho (clara)
A = dict(bg='#F6F1E7', ink='#3A352C', soft='#837963', gold='#A9874B', tint='#EFE7D8')
a_ros = rosary('ma', '#C9A574', '#9E7647', '#6B4A2A', '#5A3D22', '#8A6B45',
               '#B98F55', '#7A5530', glow='rgba(110,80,40,.18)')
a_dez = dezena('mad', '#C9A574', '#9E7647', '#6B4A2A', '#5A3D22', '#8A6B45',
               '#B98F55', '#7A5530')

a_post = (
    '<div style="position: relative; width: 1080px; height: 1080px; background: %s; '
    'display: flex; align-items: center; justify-content: center; gap: 66px; '
    'padding: 92px 96px; box-sizing: border-box; overflow: hidden">'
    '<div style="position: absolute; inset: 0; background: radial-gradient(70%% 55%% at 40%% 36%%, '
    'rgba(255,253,247,.95) 0%%, rgba(232,223,203,.55) 100%%)"></div>'
    '<div style="position: absolute; inset: 0; background-image: %s; '
    'background-size: 180px 180px; opacity: .06"></div>'
    '<div style="position: absolute; inset: 54px; border: 1px solid %s; opacity: .4"></div>'
    '<div style="width: 380px; position: relative">%s</div>'
    '<div style="display: flex; flex-direction: column; gap: 26px; position: relative; '
    'width: 340px">'
    '<div style="font-family: \'Italiana\', Didot, Georgia, serif; font-size: 74px; '
    'line-height: 1.06; letter-spacing: .16em; color: %s; text-indent: .16em">QUIS<br>UT<br>DEUS</div>'
    '<div style="width: 130px; height: 1px; background: %s; opacity: .6"></div>'
    '<div style="font-family: %s; font-style: italic; font-weight: 300; font-size: 38px; '
    'line-height: 1.35; color: %s">Ter&#231;os montados um a um, conta por conta.</div>'
    '<div style="font-family: \'Italiana\', Georgia, serif; font-size: 20px; '
    'letter-spacing: .46em; color: %s; text-indent: .46em">ATELI&#202;</div></div></div>'
    % (A['bg'], GRAIN, A['gold'], a_ros, A['ink'], A['gold'], CORM, A['soft'], A['gold']))

a_thumbs = (mini_photo(A['tint'], A['soft']) +
            thumb(A['bg'], '<div style="width: 62px">%s</div>' % a_dez) +
            thumb(A['tint'], '<div style="font-family: \'Italiana\', Georgia, serif; '
                  'font-size: 15px; letter-spacing: .2em; color: %s; text-align: center; '
                  'line-height: 1.75; text-indent: .22em">DEZ<br>CONTAS<br>POR DIA</div>' % A['ink']))

write('Linho.dc.html', FONTS_IT,
      a_post + band(A['bg'], A['ink'], A['soft'], 'Madeira e linho',
                    'Italiana + Cormorant Garamond &#183; conta de madeira sobre luz de papel, '
                    'o terço como objeto',
                    [A['bg'], A['tint'], A['gold'], A['ink']], a_thumbs,),
      1080, 1400)

# ======================================================== B · Noite de cetim (escura)
B = dict(bg='#0B0C10', bone='#F0EAE0', champ='#D9C49A', soft='#9A8F7E', tint='#171A21')
b_ros = rosary('ct', '#F6E9C8', '#D9C49A', '#9A8049', '#6E5A2E', '#B9A377',
               '#EBD9AC', '#9C8149', glow='rgba(217,196,154,.22)')
b_dez = dezena('ctd', '#F6E9C8', '#D9C49A', '#9A8049', '#6E5A2E', '#B9A377',
               '#EBD9AC', '#9C8149')

b_post = (
    '<div style="position: relative; width: 1080px; height: 1080px; '
    'background: radial-gradient(116%% 82%% at 50%% 34%%, #171A21 0%%, #0A0B0E 74%%); '
    'display: flex; flex-direction: column; align-items: center; justify-content: center; '
    'gap: 34px; padding: 80px 96px 120px; box-sizing: border-box; overflow: hidden">'
    '<div style="position: absolute; inset: 0; background-image: %s; '
    'background-size: 180px 180px; opacity: .09"></div>'
    '<div style="width: 330px; position: relative">%s</div>'
    '<div style="display: flex; flex-direction: column; align-items: center; gap: 16px; '
    'position: relative">'
    '<div style="font-family: %s; font-style: italic; font-weight: 300; font-size: 92px; '
    'line-height: 1.04; color: %s">Quis ut Deus</div>'
    '<div style="display: flex; align-items: center; gap: 16px">'
    '<div style="width: 96px; height: 1px; background: %s; opacity: .55"></div>'
    '<div style="font-family: \'Tenor Sans\', Optima, sans-serif; font-size: 18px; '
    'letter-spacing: .5em; color: %s; text-indent: .5em">TER&#199;OS</div>'
    '<div style="width: 96px; height: 1px; background: %s; opacity: .55"></div></div></div></div>'
    % (GRAIN, b_ros, CORM, B['bone'], B['champ'], B['champ'], B['champ']))

b_thumbs = (mini_photo(B['tint'], B['soft'], 'rgba(217,196,154,.28)') +
            thumb(B['bg'], '<div style="width: 58px">%s</div>' % b_dez, 'rgba(217,196,154,.28)') +
            thumb(B['tint'], '<div style="font-family: %s; font-style: italic; font-size: 20px; '
                  'color: %s; text-align: center">dez contas<br>por dia</div>'
                  % (CORM, B['bone']), 'rgba(217,196,154,.28)'))

write('Cetim.dc.html', FONTS_TS,
      b_post + band('#101218', B['bone'], B['soft'], 'Noite de cetim',
                    'Cormorant it&#225;lico + Tenor Sans &#183; conta de cristal acesa '
                    'no escuro, brilho de ouro velho',
                    [B['bg'], B['tint'], B['champ'], B['bone']], b_thumbs,),
      1080, 1400)

# ================================================== C · Pérola e rosa-antigo (clara)
C = dict(bg='#F3E9E6', ink='#4E383D', rose='#8E6B6F', gold='#BFA06B', soft='#8A7478',
         tint='#EADCD8')
c_ros = rosary('pe', '#FFFDFB', '#EEDFDC', '#C2A9A6', '#A98F8C', '#C7A9A4',
               '#D8BE86', '#A9874B', glow='rgba(120,90,90,.16)')
c_dez = dezena('ped', '#FFFDFB', '#EEDFDC', '#C2A9A6', '#A98F8C', '#C7A9A4',
               '#D8BE86', '#A9874B')

c_post = (
    '<div style="position: relative; width: 1080px; height: 1080px; background: %s; '
    'display: flex; flex-direction: column; align-items: center; justify-content: center; '
    'gap: 30px; padding: 84px 96px 118px; box-sizing: border-box; overflow: hidden">'
    '<div style="position: absolute; inset: 0; background: radial-gradient(66%% 50%% at 50%% 34%%, '
    'rgba(255,251,250,.95) 0%%, rgba(232,214,210,.6) 100%%)"></div>'
    '<div style="position: absolute; inset: 0; background-image: %s; '
    'background-size: 180px 180px; opacity: .06"></div>'
    '<div style="position: absolute; inset: 58px; border: 1px solid %s; opacity: .5"></div>'
    '<div style="position: absolute; inset: 72px; border: 1px solid %s; opacity: .22"></div>'
    '<div style="width: 320px; position: relative">%s</div>'
    '<div style="display: flex; flex-direction: column; align-items: center; gap: 12px; '
    'position: relative">'
    '<div style="font-family: \'Marcellus\', Georgia, serif; font-size: 66px; line-height: 1.06; '
    'letter-spacing: .14em; color: %s; text-indent: .14em">QUIS UT DEUS</div>'
    '<div style="font-family: %s; font-style: italic; font-weight: 300; font-size: 32px; '
    'color: %s">ateli&#234; de ter&#231;os</div></div></div>'
    % (C['bg'], GRAIN, C['gold'], C['rose'], c_ros, C['ink'], CORM, C['rose']))

c_thumbs = (mini_photo(C['tint'], C['soft']) +
            thumb(C['bg'], '<div style="width: 60px">%s</div>' % c_dez) +
            thumb(C['tint'], '<div style="font-family: \'Marcellus\', Georgia, serif; '
                  'font-size: 15px; letter-spacing: .2em; color: %s; text-align: center; '
                  'line-height: 1.75; text-indent: .2em">DEZ<br>CONTAS<br>POR DIA</div>' % C['ink']))

write('Perola.dc.html', FONTS_MA,
      c_post + band('#EFE3DF', C['ink'], C['soft'], 'P&#233;rola e rosa-antigo',
                    'Marcellus + Cormorant Garamond &#183; conta de p&#233;rola, '
                    'bord&#244; suave e fecho dourado',
                    [C['bg'], C['tint'], C['rose'], C['gold']], c_thumbs,),
      1080, 1400)

# ============================================================ as quatro fotos
SHOTS = [('O TER&#199;O INTEIRO',
          'Aberto sobre linho cru, visto de cima, luz de janela pela esquerda. '
          'A cruz apontando para baixo.'),
         ('A CONTA DE PERTO',
          'A 15 cm, luz rasante: &#233; o brilho e a textura da conta que '
          'seguram a foto.'),
         ('NA M&#195;O',
          'O ter&#231;o enrolado na m&#227;o ou escorrendo entre os dedos, '
          'fundo escuro e liso.'),
         ('A BANCADA',
          'Alicate, fio e contas soltas no meio do trabalho. &#201; a foto que '
          'mostra que &#233; feito &#224; m&#227;o.')]

shot_cards = ''.join(
    '<div style="display: flex; flex-direction: column; gap: 12px">%s'
    '<div style="font-family: \'Italiana\', Georgia, serif; font-size: 20px; '
    'letter-spacing: .22em; color: #3A352C; text-indent: .22em">%s</div>'
    '<div style="font-family: %s; font-style: italic; font-size: 19px; line-height: 1.45; '
    'color: #837963">%s</div></div>'
    % (photo_slot('100%', '236px', '#EFE7D8', 'rgba(169,135,75,.45)', '#9C8E75',
                  '[ FOTO %d ]' % (i + 1)), label, CORM, note)
    for i, (label, note) in enumerate(SHOTS))

write('Fotos.dc.html', FONTS_IT,
      '<div style="position: relative; width: 1080px; height: 1400px; background: #F6F1E7; '
      'display: flex; flex-direction: column; gap: 38px; padding: 68px 78px; '
      'box-sizing: border-box; overflow: hidden">'
      '<div style="position: absolute; inset: 0; background-image: %s; '
      'background-size: 180px 180px; opacity: .06"></div>'
      '<div style="display: flex; flex-direction: column; align-items: center; gap: 12px; '
      'position: relative">'
      '<div style="font-family: \'Italiana\', Didot, Georgia, serif; font-size: 50px; '
      'letter-spacing: .2em; color: #3A352C; text-indent: .2em">AS QUATRO FOTOS</div>'
      '<div style="font-family: %s; font-style: italic; font-size: 23px; color: #837963; '
      'text-align: center; max-width: 640px">o feed de ateli&#234; vive de foto do que '
      'sai da sua m&#227;o &#8212; estas quatro bastam para come&#231;ar</div></div>'
      '<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); '
      'gap: 36px 42px; position: relative">%s</div>'
      '<div style="font-family: %s; font-style: italic; font-size: 20px; line-height: 1.5; '
      'color: #837963; text-align: center; position: relative">Me manda as fotos e eu encaixo '
      'cada uma no recorte e no tom da dire&#231;&#227;o que voc&#234; escolher.</div></div>'
      % (GRAIN, CORM, shot_cards, CORM), 1080, 1400)

# ========================================================= prévia do perfil (Main)
HL = [('terço', 'TERÇOS'), ('dezena', 'DEZENAS'), ('medalha', 'MEDALHAS'),
      ('encomenda', 'ENCOMENDAS'), ('oração', 'ORAÇÃO')]

HL_ICON = {
 'terço': '<circle cx="12" cy="9.4" r="6" stroke-dasharray="1.1 2.7"/>'
          '<path d="M12 16.6 L12 21.6"/><path d="M9.8 18.8 L14.2 18.8"/>',
 'dezena': '<path d="M12 2.8 L12 13.8" stroke-dasharray="1.1 2.5"/>'
           '<path d="M12 15.4 L12 21.4"/><path d="M9.7 17.6 L14.3 17.6"/>',
 'medalha': '<ellipse cx="12" cy="13" rx="5.4" ry="6.4"/><ellipse cx="12" cy="13" rx="2.4" ry="3"/>'
            '<path d="M12 6.6 L12 3.6"/>',
 'encomenda': '<path d="M3 6 L21 6 L21 18 L3 18 Z"/><path d="M3 6.8 L12 13 L21 6.8"/>',
 'oração': '<path d="M12 3.4 L12 20.6"/><path d="M7.4 8.6 L16.6 8.6"/>',
}

GRID = [('foto', 'O terço inteiro'), ('type', 'QUIS<br>UT<br>DEUS'), ('foto', 'A conta de perto'),
        ('dez', ''), ('foto', 'Na mão'), ('type', 'DEZ CONTAS<br>POR DIA'),
        ('foto', 'A bancada'), ('type', 'FEITO<br>À MÃO'), ('foto', 'Encomendas')]

cells = ''
for kind, label in GRID:
    if kind == 'foto':
        cells += ('<div style="aspect-ratio: 1 / 1; background: %s; display: flex; '
                  'flex-direction: column; align-items: center; justify-content: center; gap: 6px">'
                  '<svg viewBox="0 0 48 48" width="18" height="18" style="display:block; '
                  'fill:none; stroke:%s; stroke-width:1.3"><path d="M6 13 L42 13 L42 37 L6 37 Z"/>'
                  '<path d="M6 31 L17 21 L27 31"/><circle cx="33" cy="19" r="3"/></svg>'
                  '<div style="font-family: %s; font-style: italic; font-size: 10px; color: %s; '
                  'text-align: center; padding: 0 6px">%s</div></div>'
                  % (A['tint'], A['soft'], CORM, A['soft'], label))
    elif kind == 'dez':
        cells += ('<div style="aspect-ratio: 1 / 1; background: %s; display: flex; '
                  'align-items: center; justify-content: center"><div style="width: 42px">%s</div>'
                  '</div>' % (A['bg'], a_dez))
    else:
        cells += ('<div style="aspect-ratio: 1 / 1; background: %s; display: flex; '
                  'align-items: center; justify-content: center">'
                  '<div style="font-family: \'Italiana\', Georgia, serif; font-size: 9px; '
                  'letter-spacing: .2em; color: %s; text-align: center; line-height: 1.9; '
                  'text-indent: .2em">%s</div></div>' % (A['bg'], A['ink'], label))

hl_row = ''.join(
    '<div style="display: flex; flex-direction: column; align-items: center; gap: 7px; width: 64px">'
    '<div style="width: 60px; height: 60px; border-radius: 50%%; background: %s; '
    'box-shadow: inset 0 0 0 1px rgba(169,135,75,.55); display: flex; align-items: center; '
    'justify-content: center"><svg viewBox="0 0 24 24" width="26" height="26" '
    'style="display:block; fill:none; stroke:%s; stroke-width:1.1; stroke-linecap:round">%s</svg></div>'
    '<div style="font-family: %s; font-size: 11px; letter-spacing: .04em; color: %s">%s</div></div>'
    % (A['tint'], A['gold'], HL_ICON[k], CORM, A['soft'], lab.capitalize()) for k, lab in HL)

stat = ('<div style="display: flex; flex-direction: column; align-items: center; gap: 1px">'
        '<div style="font-family: %s; font-weight: 600; font-size: 16px; color: %s">%s</div>'
        '<div style="font-family: %s; font-size: 12px; color: %s">%s</div></div>')
sans = 'system-ui, sans-serif'

btn = ('<div style="flex-grow: 1; height: 44px; border: 1px solid rgba(58,53,44,.2); '
       'border-radius: 8px; display: flex; align-items: center; justify-content: center; '
       'font-family: %s; font-size: 13px; font-weight: 500; color: %s">%%s</div>' % (sans, A['ink']))

main = (
    '<div style="width: 390px; height: 1010px; background: %s; display: flex; '
    'flex-direction: column; box-sizing: border-box; overflow: hidden">'
    '<div style="display: flex; align-items: center; gap: 8px; padding: 58px 16px 12px">'
    '<div style="font-family: \'Italiana\', Georgia, serif; font-size: 17px; '
    'letter-spacing: .14em; color: %s">quisutdeusatelie</div></div>'
    '<div style="display: flex; align-items: center; gap: 24px; padding: 4px 16px 14px">'
    '<div style="width: 88px; height: 88px; border-radius: 50%%; background: %s; '
    'box-shadow: inset 0 0 0 1px rgba(169,135,75,.5); display: flex; align-items: center; '
    'justify-content: center; flex-shrink: 0; overflow: hidden">'
    '<div style="width: 46px">%s</div></div>'
    '<div style="display: flex; flex-grow: 1; justify-content: space-around">%s%s%s</div></div>'
    '<div style="display: flex; flex-direction: column; gap: 5px; padding: 0 16px 14px">'
    '<div style="font-family: %s; font-weight: 600; font-size: 13px; color: %s">'
    'Qui Sut Deus &#183; Ateli&#234;</div>'
    '<div style="font-family: %s; font-size: 12px; color: %s">Ter&#231;os feitos &#224; m&#227;o</div>'
    '<div style="font-family: %s; font-size: 13px; line-height: 1.5; color: %s">'
    '&#8220;Quem como Deus?&#8221;<br>Ter&#231;os e dezenas montados um a um, conta por conta.<br>'
    'Encomendas pelo direct &#183; [CIDADE]</div>'
    '<div style="font-family: %s; font-size: 13px; color: %s">[LINK DA LOJA]</div></div>'
    '<div style="display: flex; gap: 8px; padding: 0 16px 18px">%s%s</div>'
    '<div style="display: flex; gap: 14px; padding: 0 16px 18px">%s</div>'
    '<div style="display: flex; border-top: 1px solid rgba(58,53,44,.14)">'
    '<div style="flex-grow: 1; height: 46px; display: flex; align-items: center; '
    'justify-content: center; border-bottom: 1px solid %s">'
    '<svg viewBox="0 0 24 24" width="19" height="19" style="display:block; fill:none; '
    'stroke:%s; stroke-width:1.3"><path d="M3 3 L21 3 L21 21 L3 21 Z"/><path d="M9 3 L9 21"/>'
    '<path d="M15 3 L15 21"/><path d="M3 9 L21 9"/><path d="M3 15 L21 15"/></svg></div>'
    '<div style="flex-grow: 1; height: 46px; display: flex; align-items: center; '
    'justify-content: center"><svg viewBox="0 0 24 24" width="19" height="19" '
    'style="display:block; fill:none; stroke:rgba(131,121,99,.5); stroke-width:1.3">'
    '<path d="M4 4 L20 4 L20 20 L4 20 Z"/><path d="M10 9 L16 12 L10 15 Z"/></svg></div></div>'
    '<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 2px; '
    'padding: 2px">%s</div></div>'
    % (A['bg'], A['ink'], A['tint'], a_dez,
       stat % (sans, A['ink'], '9', sans, A['soft'], 'publica&#231;&#245;es'),
       stat % (sans, A['ink'], '[&#8212;]', sans, A['soft'], 'seguidores'),
       stat % (sans, A['ink'], '[&#8212;]', sans, A['soft'], 'seguindo'),
       sans, A['ink'], sans, A['gold'], sans, A['ink'], sans, A['gold'],
       btn % 'Editar perfil', btn % 'Compartilhar perfil', hl_row,
       A['gold'], A['ink'], cells))
write('Main.dc.html', FONTS_IT, main, 390, 1010)

# ------------------------------------------------------------------------ avatar
write('Avatar.dc.html', FONTS_IT,
      '<div style="position: relative; width: 720px; height: 720px; background: %s; '
      'display: flex; align-items: center; justify-content: center; overflow: hidden">'
      '<div style="position: absolute; inset: 0; background: radial-gradient(60%% 55%% at 50%% 40%%, '
      'rgba(255,253,247,.95) 0%%, rgba(232,223,203,.5) 100%%)"></div>'
      '<div style="position: absolute; inset: 0; background-image: %s; '
      'background-size: 180px 180px; opacity: .06"></div>'
      '<div style="position: absolute; left: 80px; top: 80px; width: 560px; height: 560px; '
      'border-radius: 50%%; border: 1px dashed %s; opacity: .3"></div>'
      '<div style="width: 250px; position: relative">%s</div></div>'
      % (A['bg'], GRAIN, A['gold'], a_dez), 720, 720)

# --------------------------------------------------------------------- destaques
covers = ''.join(
    '<div style="display: flex; flex-direction: column; align-items: center; gap: 20px">'
    '<div style="width: 180px; height: 180px; border-radius: 50%%; background: %s; '
    'box-shadow: inset 0 0 0 1px %s; display: flex; align-items: center; justify-content: center">'
    '<svg viewBox="0 0 24 24" width="74" height="74" style="display:block; fill:none; '
    'stroke:%s; stroke-width:.9; stroke-linecap:round">%s</svg></div>'
    '<div style="font-family: \'Italiana\', Georgia, serif; font-size: 19px; '
    'letter-spacing: .28em; color: %s; text-indent: .28em">%s</div></div>'
    % (A['tint'], A['gold'], A['gold'], HL_ICON[k], A['ink'], lab) for k, lab in HL)

write('Destaques.dc.html', FONTS_IT,
      '<div style="position: relative; width: 1080px; height: 560px; background: %s; '
      'display: flex; flex-direction: column; align-items: center; justify-content: center; '
      'gap: 50px; padding: 52px; box-sizing: border-box; overflow: hidden">'
      '<div style="position: absolute; inset: 0; background-image: %s; '
      'background-size: 180px 180px; opacity: .06"></div>'
      '<div style="font-family: \'Italiana\', Georgia, serif; font-size: 21px; '
      'letter-spacing: .42em; color: %s; text-indent: .42em; position: relative">'
      'CAPAS DE DESTAQUES</div>'
      '<div style="display: flex; gap: 36px; position: relative">%s</div></div>'
      % (A['bg'], GRAIN, A['soft'], covers), 1080, 560)

# ------------------------------------------------------------------- canvas.json
canvas = {
  "pages": [{"id": "page-1", "name": "Direções"}, {"id": "page-2", "name": "Perfil"}],
  "artboards": [
    {"file": "Linho.dc.html", "x": 0, "y": 0, "w": 1080, "h": 1400, "page": "page-1",
     "title": "Madeira e linho"},
    {"file": "Cetim.dc.html", "x": 1200, "y": 0, "w": 1080, "h": 1400, "page": "page-1",
     "title": "Noite de cetim"},
    {"file": "Perola.dc.html", "x": 2400, "y": 0, "w": 1080, "h": 1400, "page": "page-1",
     "title": "Pérola e rosa-antigo"},
    {"file": "Fotos.dc.html", "x": 3600, "y": 0, "w": 1080, "h": 1400, "page": "page-1",
     "title": "As quatro fotos"},
    {"file": "Main.dc.html", "x": 0, "y": 0, "w": 390, "h": 1010, "page": "page-2",
     "title": "Prévia do perfil"},
    {"file": "Avatar.dc.html", "x": 510, "y": 0, "w": 720, "h": 720, "page": "page-2",
     "title": "Foto de perfil"},
    {"file": "Destaques.dc.html", "x": 1350, "y": 0, "w": 1080, "h": 560, "page": "page-2",
     "title": "Capas de destaques"},
  ],
  "annotations": [
    {"id": "nota-direcoes", "x": 0, "y": -250, "w": 560, "page": "page-1",
     "text": "Agora o motivo é o terço — conta, fio, medalha e cruz —, desenhado com "
             "volume e luz, não como contorno.\n\nTrês direções: escolha uma e eu levo "
             "para o perfil inteiro e para os nove primeiros posts.\n\nA quarta folha é "
             "o que só você tem: foto do que sai da sua mão. Marquei os quatro quadros "
             "e o que fotografar em cada um."},
    {"id": "nota-perfil", "x": 0, "y": -210, "w": 480, "page": "page-2",
     "text": "O perfil montado na direção Madeira e linho, para você ver a grade de pé.\n\n"
             "Os quadros marcados FOTO são os que esperam a sua imagem; os outros são "
             "tipográficos e eu já entrego prontos.\n\n[CIDADE] e [LINK DA LOJA] ficaram "
             "entre colchetes para você preencher."},
  ],
  "launch": {"view": "canvas", "page": "page-1"},
}
open(os.path.join(OUT, 'canvas.json'), 'w').write(
    json.dumps(canvas, indent=2, ensure_ascii=False))
print('canvas.json')
