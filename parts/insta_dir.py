# -*- coding: utf-8 -*-
"""Três direções delicadas para a identidade do @quisutdeusatelie.

Rode depois de insta.py — este script acrescenta a página "Direções"
ao ../instagram/canvas.json.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'instagram')
ART = open(os.path.join(HERE, 'art.svg')).read()
EMBLEM = open(os.path.join(HERE, 'emblem.svg')).read()

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


def write(name, fonts, root, w, h):
    props = json.dumps({"$preview": {"width": w, "height": h}}, ensure_ascii=False)
    open(os.path.join(OUT, name), 'w').write(SHELL % (fonts, CORM, root, props))
    print(name)


def thin(svg, factor, color, op=None):
    """Afina os traços da gravura e troca a cor — é o que deixa o desenho delicado."""
    s = re.sub(r'stroke-width:([\d.]+)',
               lambda m: 'stroke-width:%.2f' % (float(m.group(1)) * factor), svg)
    s = s.replace('var(--gold)', color)
    if op:
        s = s.replace('<svg ', '<svg opacity="%s" ' % op, 1)
    return s


def swatches(items, label_col):
    return ''.join(
        '<div style="display: flex; flex-direction: column; align-items: center; gap: 9px">'
        '<div style="width: 46px; height: 46px; border-radius: 50%%; background: %s; '
        'box-shadow: inset 0 0 0 1px rgba(0,0,0,.12)"></div>'
        '<div style="font-family: %s; font-size: 13px; letter-spacing: .14em; color: %s">%s</div>'
        '</div>' % (hexv, CORM, label_col, hexv.replace('#', '')) for hexv in items)


def band(bg, ink, soft, name, fonts_label, palette, thumbs, avatar):
    """Faixa de baixo: a mesma leitura para as três direções."""
    return (
        '<div style="width: 1080px; height: 320px; background: %s; display: flex; '
        'align-items: center; gap: 48px; padding: 0 64px; box-sizing: border-box; '
        'border-top: 1px solid rgba(0,0,0,.09)">'
        '<div style="display: flex; flex-direction: column; gap: 10px; width: 268px; flex-shrink: 0">'
        '<div style="font-family: %s; font-size: 15px; letter-spacing: .3em; color: %s; '
        'text-indent: .3em">DIRE&#199;&#195;O</div>'
        '<div style="font-family: %s; font-style: italic; font-size: 34px; line-height: 1.15; '
        'color: %s">%s</div>'
        '<div style="font-family: %s; font-size: 17px; line-height: 1.5; color: %s">%s</div></div>'
        '%s'
        '<div style="display: flex; gap: 10px">%s</div>'
        '<div style="display: flex; gap: 18px; margin-left: auto">%s</div>'
        '</div>' % (bg, CORM, soft, CORM, ink, name, CORM, soft, fonts_label,
                    avatar, thumbs, swatches(palette, soft)))


def thumb(bg, inner, border='rgba(0,0,0,.1)'):
    return ('<div style="width: 132px; height: 132px; background: %s; display: flex; '
            'align-items: center; justify-content: center; box-shadow: inset 0 0 0 1px %s; '
            'overflow: hidden">%s</div>' % (bg, border, inner))


def avatar_disc(bg, ring, mark):
    return ('<div style="width: 132px; height: 132px; border-radius: 50%%; background: %s; '
            'box-shadow: inset 0 0 0 1px %s; display: flex; align-items: center; '
            'justify-content: center; flex-shrink: 0">%s</div>' % (bg, ring, mark))


# =========================================================== A · Linho e ouro
A_BG, A_INK, A_GOLD, A_SOFT = '#F6F1E7', '#3A352C', '#A9874B', '#837963'
a_emb = thin(EMBLEM, 0.42, A_GOLD)
a_post = (
    '<div style="position: relative; width: 1080px; height: 1080px; background: %s; '
    'display: flex; flex-direction: column; align-items: center; justify-content: center; '
    'gap: 46px; padding: 120px 120px 150px; box-sizing: border-box; overflow: hidden">'

    '<div style="position: absolute; left: 58px; top: 58px; right: 58px; bottom: 58px; '
    'border: 1px solid %s; opacity: .45; pointer-events: none"></div>'

    '<div style="width: 196px">%s</div>'

    '<div style="display: flex; flex-direction: column; align-items: center; gap: 26px">'
    '<div style="font-family: \'Italiana\', Didot, Georgia, serif; font-size: 112px; '
    'line-height: 1; letter-spacing: .22em; color: %s; text-indent: .22em">QUIS UT DEUS</div>'
    '<div style="display: flex; align-items: center; gap: 20px; width: 560px">'
    '<div style="flex-grow: 1; height: 1px; background: %s; opacity: .5"></div>'
    '<div style="font-family: \'Italiana\', Didot, Georgia, serif; font-size: 26px; '
    'letter-spacing: .5em; color: %s; text-indent: .5em">ATELI&#202;</div>'
    '<div style="flex-grow: 1; height: 1px; background: %s; opacity: .5"></div></div></div>'

    '<div style="font-family: %s; font-style: italic; font-weight: 300; font-size: 42px; '
    'line-height: 1.4; color: %s; text-align: center; max-width: 700px; text-wrap: pretty">'
    'Pe&#231;as de devo&#231;&#227;o, desenhadas e impressas uma a uma.</div>'

    '</div>' % (A_BG, A_GOLD, a_emb, A_INK, A_GOLD, A_GOLD, A_GOLD, CORM, A_SOFT))

a_thumbs = (
    thumb(A_BG, '<div style="width: 72px">%s</div>' % thin(EMBLEM, 0.3, A_GOLD)) +
    thumb('#EFE7D8',
          '<div style="font-family: \'Italiana\', Georgia, serif; font-size: 20px; '
          'letter-spacing: .24em; color: %s; text-align: center; line-height: 1.7; '
          'text-indent: .24em">QUIS<br>UT<br>DEUS?</div>' % A_INK) +
    thumb(A_BG, '<div style="font-family: %s; font-style: italic; font-size: 19px; '
          'color: %s; text-align: center; padding: 0 14px; line-height: 1.4">defendei-nos '
          'no combate</div>' % (CORM, A_SOFT)))

write('Linho.dc.html',
      'https://fonts.googleapis.com/css2?family=Italiana&family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&display=swap',
      a_post + band(A_BG, A_INK, A_SOFT, 'Linho e ouro claro',
                    'Italiana + Cormorant Garamond &#183; papel em vez de noite, '
                    'tra&#231;o fin&#237;ssimo, muito ar',
                    [A_BG, '#EFE7D8', A_GOLD, A_INK], a_thumbs,
                    avatar_disc(A_BG, A_GOLD, '<div style="width: 74px">%s</div>'
                                % thin(EMBLEM, 0.3, A_GOLD))),
      1080, 1400)

# =========================================================== B · Noite de cetim
B_BG, B_BONE, B_CHAMP, B_SOFT = '#0B0C10', '#F0EAE0', '#D9C49A', '#9A8F7E'
b_emb = thin(EMBLEM, 0.4, B_CHAMP)
b_post = (
    '<div style="position: relative; width: 1080px; height: 1080px; '
    'background: radial-gradient(115%% 80%% at 50%% 34%%, #14161C 0%%, #0B0C10 72%%); '
    'display: flex; flex-direction: column; align-items: center; justify-content: center; '
    'gap: 44px; padding: 130px 120px 150px; box-sizing: border-box; overflow: hidden">'

    '<div style="position: absolute; left: 50%%; top: 96px; width: 1px; height: 74px; '
    'background: linear-gradient(180deg, rgba(217,196,154,0) 0%%, rgba(217,196,154,.6) 100%%)">'
    '</div>'

    '<div style="width: 164px">%s</div>'

    '<div style="font-family: %s; font-style: italic; font-weight: 300; font-size: 124px; '
    'line-height: 1.04; letter-spacing: .01em; color: %s">Quis ut Deus</div>'

    '<div style="display: flex; align-items: center; gap: 18px">'
    '<div style="width: 120px; height: 1px; background: %s; opacity: .55"></div>'
    '<div style="font-family: \'Tenor Sans\', \'Optima\', sans-serif; font-size: 22px; '
    'letter-spacing: .52em; color: %s; text-indent: .52em">ATELI&#202;</div>'
    '<div style="width: 120px; height: 1px; background: %s; opacity: .55"></div></div>'

    '<div style="font-family: \'Tenor Sans\', \'Optima\', sans-serif; font-size: 23px; '
    'line-height: 2; letter-spacing: .2em; color: %s; text-align: center; text-indent: .2em">'
    'DESENHADAS AQUI &#183; TIRAGEM CONTADA</div>'

    '</div>' % (b_emb, CORM, B_BONE, B_CHAMP, B_CHAMP, B_CHAMP, B_SOFT))

b_thumbs = (
    thumb('#0E1015', '<div style="width: 62px">%s</div>' % thin(EMBLEM, 0.28, B_CHAMP),
          'rgba(217,196,154,.28)') +
    thumb('#0B0C10', '<div style="font-family: %s; font-style: italic; font-size: 27px; '
          'color: %s">Quis ut<br>Deus</div>' % (CORM, B_BONE), 'rgba(217,196,154,.28)') +
    thumb('#0E1015', '<div style="font-family: \'Tenor Sans\', sans-serif; font-size: 13px; '
          'letter-spacing: .3em; color: %s; text-align: center; line-height: 2; '
          'text-indent: .3em">S&#183;M&#183;A</div>' % B_CHAMP, 'rgba(217,196,154,.28)'))

write('Cetim.dc.html',
      'https://fonts.googleapis.com/css2?family=Tenor+Sans&family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&display=swap',
      b_post + band('#101218', B_BONE, B_SOFT, 'Noite de cetim',
                    'Cormorant Garamond it&#225;lico + Tenor Sans &#183; fica no preto, '
                    'mas champanhe em vez de ouro e nada em vers&#225;is pesadas',
                    [B_BG, '#14161C', B_CHAMP, B_BONE], b_thumbs,
                    avatar_disc('#0E1015', 'rgba(217,196,154,.5)',
                                '<div style="width: 66px">%s</div>'
                                % thin(EMBLEM, 0.28, B_CHAMP))),
      1080, 1400)

# ======================================================== C · Pérola e rosa-antigo
C_BG, C_INK, C_ROSE, C_GOLD, C_SOFT = '#F3E9E6', '#4E383D', '#8E6B6F', '#BFA06B', '#8A7478'
c_emb = thin(EMBLEM, 0.38, C_ROSE)
c_post = (
    '<div style="position: relative; width: 1080px; height: 1080px; background: %s; '
    'display: flex; flex-direction: column; align-items: center; justify-content: center; '
    'gap: 40px; padding: 124px 120px 150px; box-sizing: border-box; overflow: hidden">'

    '<div style="position: absolute; left: 64px; top: 64px; right: 64px; bottom: 64px; '
    'border: 1px solid %s; opacity: .5; pointer-events: none"></div>'
    '<div style="position: absolute; left: 78px; top: 78px; right: 78px; bottom: 78px; '
    'border: 1px solid %s; opacity: .22; pointer-events: none"></div>'

    '<div style="width: 178px">%s</div>'

    '<div style="display: flex; flex-direction: column; align-items: center; gap: 18px">'
    '<div style="font-family: \'Marcellus\', Georgia, serif; font-size: 96px; line-height: 1.04; '
    'letter-spacing: .14em; color: %s; text-indent: .14em">QUIS UT DEUS</div>'
    '<div style="font-family: %s; font-style: italic; font-weight: 300; font-size: 40px; '
    'color: %s">ateli&#234; de arte sacra</div></div>'

    '<div style="display: flex; align-items: center; gap: 16px">'
    '<div style="width: 86px; height: 1px; background: %s"></div>'
    '<svg viewBox="0 0 24 24" width="13" height="13" style="display:block">'
    '<path d="M12 1 L15 12 L12 23 L9 12 Z" fill="%s"/></svg>'
    '<div style="width: 86px; height: 1px; background: %s"></div></div>'

    '<div style="font-family: %s; font-weight: 300; font-size: 38px; line-height: 1.5; '
    'color: %s; text-align: center; max-width: 680px; text-wrap: pretty">'
    'Cada pe&#231;a sai daqui desenhada &#224; m&#227;o, em tiragem contada.</div>'

    '</div>' % (C_BG, C_GOLD, C_ROSE, c_emb, C_INK, CORM, C_ROSE,
                C_GOLD, C_GOLD, C_GOLD, CORM, C_SOFT))

c_thumbs = (
    thumb(C_BG, '<div style="width: 68px">%s</div>' % thin(EMBLEM, 0.28, C_ROSE)) +
    thumb('#EADCD8', '<div style="font-family: \'Marcellus\', Georgia, serif; font-size: 19px; '
          'letter-spacing: .2em; color: %s; text-align: center; line-height: 1.8; '
          'text-indent: .2em">QUIS<br>UT<br>DEUS?</div>' % C_INK) +
    thumb(C_BG, '<div style="font-family: %s; font-style: italic; font-size: 20px; color: %s; '
          'text-align: center; padding: 0 16px; line-height: 1.4">defendei-nos '
          'no combate</div>' % (CORM, C_SOFT)))

write('Perola.dc.html',
      'https://fonts.googleapis.com/css2?family=Marcellus&family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&display=swap',
      c_post + band('#EFE3DF', C_INK, C_SOFT, 'P&#233;rola e rosa-antigo',
                    'Marcellus + Cormorant Garamond &#183; sai do preto-e-ouro: '
                    'p&#233;rola, bord&#244; suave e filete dourado',
                    [C_BG, '#EADCD8', C_ROSE, C_GOLD], c_thumbs,
                    avatar_disc(C_BG, C_GOLD, '<div style="width: 70px">%s</div>'
                                % thin(EMBLEM, 0.28, C_ROSE))),
      1080, 1400)

# ---------------------------------------------------- acrescenta a página ao canvas
cpath = os.path.join(OUT, 'canvas.json')
canvas = json.load(open(cpath))
canvas['pages'] = [p for p in canvas['pages'] if p['id'] != 'page-3'] + \
                  [{"id": "page-3", "name": "Direções"}]
canvas['artboards'] = [a for a in canvas['artboards']
                       if a['file'] not in ('Linho.dc.html', 'Cetim.dc.html', 'Perola.dc.html')]
for i, (f, t) in enumerate([('Linho.dc.html', 'Linho e ouro claro'),
                            ('Cetim.dc.html', 'Noite de cetim'),
                            ('Perola.dc.html', 'Pérola e rosa-antigo')]):
    canvas['artboards'].append({"file": f, "x": i * 1200, "y": 0, "w": 1080, "h": 1400,
                                "page": "page-3", "title": t})
canvas['annotations'] = [n for n in canvas['annotations'] if n['id'] != 'nota-direcoes'] + [
    {"id": "nota-direcoes", "x": 0, "y": -230, "w": 560, "page": "page-3",
     "text": "Três direções delicadas para a identidade — escolha uma e eu refaço "
             "o perfil, o avatar, os destaques e os nove posts nela.\n\n"
             "Linho: claro, de papel, a gravura bem fina em ouro velho.\n"
             "Cetim: continua no preto, mas champanhe e itálico no lugar das versais.\n"
             "Pérola: sai do preto-e-ouro para pérola, bordô suave e filete dourado.\n\n"
             "Cada folha mostra o post de abertura, a foto de perfil, três quadros "
             "do feed e a paleta."}]
canvas['launch'] = {"view": "canvas", "page": "page-3"}
open(cpath, 'w').write(json.dumps(canvas, indent=2, ensure_ascii=False))
print('canvas.json')
