# -*- coding: utf-8 -*-
"""Gera os artboards do kit de Instagram (@quisutdeusatelie) em ../instagram/."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'instagram')
os.makedirs(OUT, exist_ok=True)

ART = open(os.path.join(HERE, 'art.svg')).read()
EMBLEM = open(os.path.join(HERE, 'emblem.svg')).read()
SHIRT = open(os.path.join(HERE, 'shirt.svg')).read()
BACK = open(os.path.join(HERE, 'back.html')).read()

GOLD, BONE, INK, CREAM = '#C6A15B', '#EDE6D6', '#1B1A17', '#E9E2D6'

CINZEL = "'Cinzel', 'Trajan Pro', Georgia, serif"
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
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600&family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&display=swap">
  <style>
    body {{ margin: 0; font-family: {corm}; }}
    a {{ color: #C6A15B; }} a:hover {{ color: #E0C289; }}
  </style>
</helmet>
{root}
</x-dc>
<script data-dc-script data-props='{props}'>
class Component extends DCLogic {{{logic}}}
</script>
</body>
</html>
"""


def write(name, root, w, h, gold_tweak=True):
    if gold_tweak:
        props = {"gold": {"editor": "color", "default": GOLD,
                          "options": [GOLD, "#D8B77A", "#8C6B34", BONE], "section": "Cor"},
                 "$preview": {"width": w, "height": h}}
        logic = "\n  renderVals() {\n    return { gold: this.props.gold ?? '%s' };\n  }\n" % GOLD
    else:
        props = {"$preview": {"width": w, "height": h}}
        logic = ""
    doc = SHELL.format(corm=CORM, root=root,
                       props=json.dumps(props, ensure_ascii=False).replace("'", '&#39;'),
                       logic=logic)
    path = os.path.join(OUT, name)
    open(path, 'w').write(doc)
    print(name, len(doc))


# ---------------------------------------------------------------- peças soltas

def frame(color=GOLD, op='.32', inset='46px'):
    return ('<div style="position: absolute; left: %s; top: %s; right: %s; bottom: %s; '
            'border: 1px solid %s; opacity: %s; pointer-events: none"></div>'
            % (inset, inset, inset, inset, color, op))


def wordmark(color=GOLD, op='.62'):
    return ('<div style="position: absolute; left: 0; right: 0; bottom: 74px; text-align: center; '
            'font-family: %s; font-weight: 400; font-size: 22px; letter-spacing: .46em; '
            'color: %s; opacity: %s; text-indent: .46em">QUIS UT DEUS &#183; ATELI&#202;</div>'
            % (CINZEL, color, op))


def eyebrow(text, color=GOLD, size=24, op='.8'):
    return ('<div style="font-family: %s; font-weight: 400; font-size: %dpx; letter-spacing: .44em; '
            'color: %s; opacity: %s; text-indent: .44em">%s</div>' % (CINZEL, size, color, op, text))


def rule(width=520, color=GOLD, op='.5'):
    return ('<div style="width: %dpx; height: 1px; background: %s; opacity: %s"></div>'
            % (width, color, op))


def diamond(size=14, color='var(--gold)', op='.8'):
    return ('<svg viewBox="0 0 24 24" width="%d" height="%d" style="display:block">'
            '<path d="M12 1 L15 12 L12 23 L9 12 Z" fill="%s" opacity="%s"/></svg>'
            % (size, size, color, op))


def post(inner, bg='#0E0F13', gold='var(--gold)', frame_col=GOLD, mark_col=GOLD, mark_op='.62'):
    return ('<div style="--gold: {{gold}}; --bone: %s; position: relative; width: 1080px; height: 1080px; '
            'background: %s; display: flex; flex-direction: column; align-items: center; '
            'justify-content: center; padding: 104px 96px 150px; box-sizing: border-box; overflow: hidden">\n'
            '%s\n%s\n%s\n</div>' % (BONE, bg, frame(frame_col), inner, wordmark(mark_col, mark_op)))


# ------------------------------------------------------------------- 1 · abertura
p1 = post(
    '<div style="display: flex; flex-direction: column; align-items: center; gap: 34px">'
    '<div style="width: 286px">%s</div>'
    '<div style="font-family: %s; font-weight: 500; font-size: 96px; line-height: 1; '
    'letter-spacing: .12em; color: var(--bone); text-indent: .12em">QUIS UT DEUS</div>'
    '<div style="display: flex; align-items: center; gap: 26px; width: 700px">'
    '%s<div style="font-family: %s; font-size: 34px; letter-spacing: .46em; color: var(--gold); '
    'text-indent: .46em">ATELI&#202;</div>%s</div>'
    '<div style="font-family: %s; font-style: italic; font-weight: 300; font-size: 44px; '
    'letter-spacing: .04em; color: var(--bone); opacity: .84; margin-top: 6px">'
    'Pe&#231;as de devo&#231;&#227;o, desenhadas e impressas uma a uma.</div>'
    '</div>' % (EMBLEM, CINZEL,
                '<div style="flex-grow: 1; height: 1px; background: var(--gold); opacity: .55"></div>',
                CINZEL,
                '<div style="flex-grow: 1; height: 1px; background: var(--gold); opacity: .55"></div>',
                CORM))
write('Post1.dc.html', p1, 1080, 1080)

# --------------------------------------------------------------------- 2 · a arte
p2 = post(
    '<div style="display: flex; flex-direction: column; align-items: center; gap: 30px">'
    '%s<div style="width: 520px">%s</div>'
    '<div style="display: flex; flex-direction: column; align-items: center; gap: 14px">'
    '<div style="font-family: %s; font-weight: 500; font-size: 62px; letter-spacing: .16em; '
    'color: var(--bone); text-indent: .16em">S&#195;O MIGUEL</div>'
    '<div style="font-family: %s; font-style: italic; font-size: 36px; color: var(--gold); '
    'opacity: .9">arte de costas &#183; 25 &#215; 33 cm</div>'
    '</div></div>' % (eyebrow('A ARTE'), ART, CINZEL, CORM))
write('Post2.dc.html', p2, 1080, 1080)

# ------------------------------------------------------------------- 3 · a peça
front_emblem = ('<div style="--gold: %s; width: 360px; height: 420px; background: #0E0F13; '
                'display: flex; flex-direction: column; align-items: center; justify-content: center; '
                'gap: 20px; padding: 28px; box-sizing: border-box; overflow: hidden">'
                '<div style="width: 176px">%s</div></div>' % (GOLD, EMBLEM))
shirt_front = SHIRT.replace('__COLLAR__', 'M155,46 C163,68 179,80 200,80 C221,80 237,68 245,46')
shirt_back = SHIRT.replace('__COLLAR__', 'M154,45 C164,60 180,66 200,66 C220,66 236,60 246,45')
back_design = BACK.replace('__GOLD__', GOLD).replace('<!--ART-->', ART)

p3 = ('<div style="position: relative; width: 1080px; height: 1080px; background: %s; '
      'display: flex; flex-direction: column; align-items: center; justify-content: center; '
      'gap: 30px; padding: 96px 72px 150px; box-sizing: border-box; overflow: hidden">\n'
      '%s\n'
      '<div style="font-family: %s; font-size: 24px; letter-spacing: .44em; color: #8C6B34; '
      'text-indent: .44em">A PE&#199;A</div>'
      '<div style="display: flex; align-items: flex-end; justify-content: center; gap: 56px">'
      '<div style="display: flex; flex-direction: column; align-items: center; gap: 18px">'
      '<div style="position: relative; width: 380px; height: 456px">%s'
      '<div style="position: absolute; left: 56.5%%; top: 25.5%%; width: 45px; height: 53px; overflow: hidden">'
      '<div style="width: 360px; height: 420px; transform: scale(.1259); transform-origin: top left">%s</div>'
      '</div></div>'
      '<div style="font-family: %s; font-size: 20px; letter-spacing: .4em; color: #6B6154; '
      'text-indent: .4em">FRENTE</div></div>'
      '<div style="display: flex; flex-direction: column; align-items: center; gap: 18px">'
      '<div style="position: relative; width: 380px; height: 456px">%s'
      '<div style="position: absolute; left: 27%%; top: 21%%; width: 175px; height: 237px; overflow: hidden">'
      '<div style="width: 960px; height: 1300px; transform: scale(.182); transform-origin: top left">%s</div>'
      '</div></div>'
      '<div style="font-family: %s; font-size: 20px; letter-spacing: .4em; color: #6B6154; '
      'text-indent: .4em">COSTAS</div></div>'
      '</div>'
      '<div style="font-family: %s; font-style: italic; font-size: 36px; color: #6B6154; '
      'text-align: center; max-width: 740px">Malha preta, gravura dourada. Emblema de 8 cm no peito, '
      'arcanjo inteiro nas costas.</div>'
      '<div style="position: absolute; left: 0; right: 0; bottom: 68px; text-align: center; '
      'font-family: %s; font-size: 22px; letter-spacing: .46em; color: #8C6B34; opacity: .8; '
      'text-indent: .46em">QUIS UT DEUS &#183; ATELI&#202;</div>'
      '</div>' % (CREAM, frame('#8C6B34', '.3'), CINZEL,
                  shirt_front, front_emblem, CINZEL,
                  shirt_back, back_design, CINZEL, CORM, CINZEL))
write('Post3.dc.html', p3, 1080, 1080, gold_tweak=False)

# -------------------------------------------------------------------- 4 · oração
p4 = post(
    '<div style="display: flex; flex-direction: column; align-items: center; gap: 46px">'
    '<div style="width: 118px">%s</div>'
    '<div style="font-family: %s; font-style: italic; font-weight: 300; font-size: 78px; '
    'line-height: 1.3; letter-spacing: .01em; color: var(--bone); text-align: center; '
    'max-width: 820px; text-wrap: pretty">S&#227;o Miguel Arcanjo, defendei-nos no combate.</div>'
    '<div style="display: flex; align-items: center; gap: 22px">%s%s%s</div>'
    '</div>' % (EMBLEM, CORM, rule(180), diamond(16), rule(180)))
write('Post4.dc.html', p4, 1080, 1080)

# ---------------------------------------------------------- 5 · o nome da casa
p5 = post(
    '<div style="display: flex; flex-direction: column; align-items: center; gap: 40px">'
    '%s'
    '<div style="display: flex; flex-direction: column; align-items: center; gap: 2px">'
    '<div style="font-family: %s; font-weight: 500; font-size: 132px; line-height: 1.04; '
    'letter-spacing: .08em; color: var(--bone); text-indent: .08em">QUIS</div>'
    '<div style="font-family: %s; font-weight: 400; font-size: 72px; line-height: 1.1; '
    'letter-spacing: .3em; color: var(--gold); text-indent: .3em">UT</div>'
    '<div style="font-family: %s; font-weight: 500; font-size: 132px; line-height: 1.04; '
    'letter-spacing: .08em; color: var(--bone); text-indent: .08em">DEUS?</div>'
    '</div>'
    '%s'
    '<div style="font-family: %s; font-weight: 300; font-size: 40px; line-height: 1.55; '
    'color: var(--bone); opacity: .9; text-align: center; max-width: 780px; text-wrap: pretty">'
    '&#8220;Quem como Deus?&#8221; &#8212; o grito do arcanjo diante do orgulho. '
    '&#201; o nome da casa e o que cada pe&#231;a carrega.</div>'
    '</div>' % (eyebrow('O NOME DA CASA'), CINZEL, CINZEL, CINZEL, rule(420), CORM))
write('Post5.dc.html', p5, 1080, 1080)

# -------------------------------------------------------------------- 6 · detalhe
p6 = post(
    '<div style="display: flex; flex-direction: column; align-items: center; gap: 34px">'
    '%s'
    '<div style="width: 620px; height: 500px; overflow: hidden; position: relative">'
    '<div style="position: absolute; left: -330px; top: -60px; width: 1480px">%s</div>'
    '</div>'
    '<div style="font-family: %s; font-style: italic; font-size: 38px; color: var(--bone); '
    'opacity: .88; text-align: center; max-width: 720px">Asa por asa, tra&#231;o vetorial: '
    'sai limpo na serigrafia e no DTF.</div>'
    '</div>' % (eyebrow('O DETALHE'), ART, CORM))
write('Post6.dc.html', p6, 1080, 1080)

# -------------------------------------------------------- 7 · direção crua (clara)
art_ink = ART.replace('var(--gold)', INK)
p7 = ('<div style="position: relative; width: 1080px; height: 1080px; background: %s; '
      'display: flex; flex-direction: column; align-items: center; justify-content: center; '
      'gap: 28px; padding: 104px 96px 150px; box-sizing: border-box; overflow: hidden">\n'
      '%s\n'
      '<div style="font-family: %s; font-size: 24px; letter-spacing: .44em; color: #8C6B34; '
      'text-indent: .44em">DIRE&#199;&#195;O CRUA</div>'
      '<div style="width: 470px">%s</div>'
      '<div style="font-family: %s; font-style: italic; font-size: 38px; color: #4A4337; '
      'text-align: center; max-width: 720px">A mesma gravura em tinta sobre malha crua &#8212; '
      'para o dia da festa, sob o sol.</div>'
      '<div style="position: absolute; left: 0; right: 0; bottom: 68px; text-align: center; '
      'font-family: %s; font-size: 22px; letter-spacing: .46em; color: #8C6B34; opacity: .85; '
      'text-indent: .46em">QUIS UT DEUS &#183; ATELI&#202;</div>'
      '</div>' % (CREAM, frame('#8C6B34', '.3'), CINZEL, art_ink, CORM, CINZEL))
write('Post7.dc.html', p7, 1080, 1080, gold_tweak=False)

# ------------------------------------------------------------- 8 · ficha técnica
rows = [('MALHA', 'Algod&#227;o penteado &#183; [GRAMATURA] g/m&#178;'),
        ('IMPRESS&#195;O', 'Serigrafia dourada &#183; ou DTF'),
        ('TAMANHOS', 'P ao GG &#183; modelagem [MODELAGEM]'),
        ('ARTE', 'Desenho pr&#243;prio, vetorial'),
        ('PRE&#199;O', 'R$ [PRE&#199;O]')]
row_html = ''.join(
    '<div style="display: flex; align-items: baseline; gap: 28px; width: 100%%">'
    '<div style="font-family: %s; font-size: 26px; letter-spacing: .3em; color: var(--gold); '
    'width: 300px; flex-shrink: 0; text-indent: .3em">%s</div>'
    '<div style="flex-grow: 1; height: 1px; background: var(--gold); opacity: .28"></div>'
    '<div style="font-family: %s; font-size: 36px; color: var(--bone); opacity: .92; '
    'text-align: right">%s</div></div>' % (CINZEL, k, CORM, v) for k, v in rows)
p8 = post(
    '<div style="display: flex; flex-direction: column; align-items: center; gap: 48px; width: 100%%">'
    '%s'
    '<div style="display: flex; flex-direction: column; gap: 30px; width: 780px">%s</div>'
    '%s</div>' % (eyebrow('FICHA'), row_html, diamond(18)))
write('Post8.dc.html', p8, 1080, 1080)

# ----------------------------------------------------------------- 9 · lançamento
p9 = post(
    '<div style="display: flex; flex-direction: column; align-items: center; gap: 36px">'
    '%s'
    '<div style="font-family: %s; font-weight: 500; font-size: 104px; line-height: 1.06; '
    'letter-spacing: .1em; color: var(--bone); text-indent: .1em; text-align: center">'
    '[DIA] DE [M&#202;S]</div>'
    '%s'
    '<div style="font-family: %s; font-style: italic; font-weight: 300; font-size: 46px; '
    'line-height: 1.4; color: var(--gold); text-align: center; max-width: 760px">'
    'Primeira tiragem, quantidade contada.</div>'
    '<div style="font-family: %s; font-size: 26px; letter-spacing: .36em; color: var(--bone); '
    'opacity: .86; text-indent: .36em; text-align: center; line-height: 1.9">'
    'ENCOMENDAS PELO DIRECT<br>[LINK DA LOJA]</div>'
    '</div>' % (eyebrow('LAN&#199;AMENTO'), CINZEL, rule(360), CORM, CINZEL))
write('Post9.dc.html', p9, 1080, 1080)

# --------------------------------------------------------------------- avatar
avatar = (
    '<div style="--gold: {{gold}}; position: relative; width: 720px; height: 720px; '
    'background: #0E0F13; display: flex; align-items: center; justify-content: center; '
    'box-sizing: border-box; overflow: hidden">'
    '<div style="position: absolute; left: 80px; top: 80px; width: 560px; height: 560px; '
    'border-radius: 50%%; border: 1px dashed var(--gold); opacity: .28"></div>'
    '<div style="width: 320px">%s</div>'
    '</div>' % EMBLEM)
write('Avatar.dc.html', avatar, 720, 720)

# ------------------------------------------------------------------- destaques
ICONS = {
 'shirt': '<path d="M8.5 3 L5 5 L3.5 9 L6 10 L6 21 L18 21 L18 10 L20.5 9 L19 5 L15.5 3 '
          'C15 4.8 13.6 5.8 12 5.8 C10.4 5.8 9 4.8 8.5 3 Z"/>',
 'halo': '<circle cx="12" cy="13" r="5.2"/><path d="M12 2.4 L12 5"/><path d="M5.2 5.2 L7 7"/>'
         '<path d="M18.8 5.2 L17 7"/><path d="M3 12 L5.4 12"/><path d="M21 12 L18.6 12"/>',
 'needle': '<path d="M20.5 3.5 L10 14"/><path d="M8.2 15.8 L6 21 L11.2 18.8 Z"/>'
           '<path d="M17.6 4.4 C14 2.6 10.6 4.4 11.4 7.6"/>',
 'mail': '<path d="M3 6 L21 6 L21 18 L3 18 Z"/><path d="M3 6.8 L12 13 L21 6.8"/>',
 'cross': '<path d="M12 3 L12 21"/><path d="M6.5 8.6 L17.5 8.6"/>'
          '<circle cx="12" cy="23" r="0"/>',
}
HL = [('shirt', 'PE&#199;AS'), ('halo', 'SANTOS'), ('needle', 'PROCESSO'),
      ('mail', 'PEDIDOS'), ('cross', 'ORA&#199;&#195;O')]
covers = ''.join(
    '<div style="display: flex; flex-direction: column; align-items: center; gap: 22px">'
    '<div style="width: 180px; height: 180px; border-radius: 50%%; background: #0E0F13; '
    'border: 1px solid var(--gold); display: flex; align-items: center; justify-content: center">'
    '<svg viewBox="0 0 24 24" width="76" height="76" style="display:block; fill:none; '
    'stroke:var(--gold); stroke-width:1.1; stroke-linecap:round; stroke-linejoin:round">%s</svg>'
    '</div>'
    '<div style="font-family: %s; font-size: 20px; letter-spacing: .3em; color: var(--bone); '
    'opacity: .86; text-indent: .3em">%s</div></div>' % (ICONS[k], CINZEL, label)
    for k, label in HL)
destaques = (
    '<div style="--gold: {{gold}}; --bone: %s; position: relative; width: 1080px; height: 560px; '
    'background: #0E0F13; display: flex; flex-direction: column; align-items: center; '
    'justify-content: center; gap: 56px; padding: 56px; box-sizing: border-box; overflow: hidden">'
    '%s'
    '<div style="display: flex; gap: 38px; justify-content: center">%s</div>'
    '</div>' % (BONE, eyebrow('CAPAS DE DESTAQUES', size=22), covers))
write('Destaques.dc.html', destaques, 1080, 560)

# ------------------------------------------------------- prévia do perfil (Main)
THUMBS = [('QUIS UT DEUS', 'dark', 'emblem'), ('S&#195;O MIGUEL', 'dark', 'art'),
          ('A PE&#199;A', 'light', 'none'), ('DEFENDEI-NOS', 'dark', 'emblem'),
          ('QUIS UT DEUS?', 'dark', 'none'), ('O DETALHE', 'dark', 'art'),
          ('DIRE&#199;&#195;O CRUA', 'light', 'none'), ('FICHA', 'dark', 'none'),
          ('[DIA] DE [M&#202;S]', 'dark', 'emblem')]

MINI = ('<svg viewBox="0 0 204 300" width="26" height="38" style="display:block; fill:none; '
        'stroke:%s; stroke-width:5; stroke-linecap:round; stroke-linejoin:round">'
        '<circle cx="102" cy="46" r="8"/>'
        '<path d="M66,82 C78,77 126,77 138,82 C126,87 78,87 66,82 Z"/>'
        '<path d="M102,86 L102,256"/>'
        '<path d="M84,240 C92,252 96,258 102,258 C108,258 112,252 120,240"/></svg>')

cells = ''
for label, tone, mark in THUMBS:
    bg = CREAM if tone == 'light' else '#12141A'
    fg = '#8C6B34' if tone == 'light' else GOLD
    txt = '#4A4337' if tone == 'light' else BONE
    inner = MINI % fg if mark == 'emblem' else (
        '<svg viewBox="0 0 24 24" width="22" height="22" style="display:block"><path d="M12 1 L15 12 '
        'L12 23 L9 12 Z" fill="%s" opacity=".75"/></svg>' % fg if mark == 'art' else '')
    cells += ('<div style="aspect-ratio: 1 / 1; background: %s; display: flex; flex-direction: column; '
              'align-items: center; justify-content: center; gap: 8px; overflow: hidden">%s'
              '<div style="font-family: %s; font-size: 8px; letter-spacing: .2em; color: %s; '
              'opacity: .9; text-indent: .2em; text-align: center; padding: 0 6px">%s</div></div>'
              % (bg, inner, CINZEL, txt, label))

hl_row = ''.join(
    '<div style="display: flex; flex-direction: column; align-items: center; gap: 7px; width: 64px">'
    '<div style="width: 60px; height: 60px; border-radius: 50%%; background: #0E0F13; '
    'border: 1px solid rgba(198,161,91,.75); display: flex; align-items: center; justify-content: center">'
    '<svg viewBox="0 0 24 24" width="26" height="26" style="display:block; fill:none; '
    'stroke:%s; stroke-width:1.2; stroke-linecap:round; stroke-linejoin:round">%s</svg></div>'
    '<div style="font-family: system-ui, sans-serif; font-size: 10px; letter-spacing: .04em; '
    'color: rgba(237,230,214,.72)">%s</div></div>' % (GOLD, ICONS[k], label.replace('&#199;', 'Ç')
                                                      .replace('&#195;', 'Ã'))
    for k, label in HL)

stat = ('<div style="display: flex; flex-direction: column; align-items: center; gap: 1px">'
        '<div style="font-family: system-ui, sans-serif; font-weight: 600; font-size: 16px; '
        'color: %s">%s</div><div style="font-family: system-ui, sans-serif; font-size: 12px; '
        'color: rgba(237,230,214,.6)">%s</div></div>')

btn = ('<div style="flex-grow: 1; height: 44px; border: 1px solid rgba(237,230,214,.22); '
       'border-radius: 8px; display: flex; align-items: center; justify-content: center; '
       'font-family: system-ui, sans-serif; font-size: 13px; font-weight: 500; '
       'color: rgba(237,230,214,.9)">%s</div>')

main = (
    '<div style="--gold: {{gold}}; --bone: %s; width: 390px; height: 844px; background: #0B0C0F; '
    'display: flex; flex-direction: column; box-sizing: border-box; overflow: hidden">'

    '<div style="display: flex; align-items: center; gap: 8px; padding: 58px 16px 12px">'
    '<div style="font-family: %s; font-size: 17px; letter-spacing: .12em; color: var(--bone)">'
    'quisutdeusatelie</div>%s</div>'

    '<div style="display: flex; align-items: center; gap: 24px; padding: 4px 16px 14px">'
    '<div style="width: 88px; height: 88px; border-radius: 50%%; background: #0E0F13; '
    'border: 1px solid rgba(198,161,91,.55); display: flex; align-items: center; '
    'justify-content: center; flex-shrink: 0"><div style="width: 44px">%s</div></div>'
    '<div style="display: flex; flex-grow: 1; justify-content: space-around">%s%s%s</div></div>'

    '<div style="display: flex; flex-direction: column; gap: 5px; padding: 0 16px 14px">'
    '<div style="font-family: system-ui, sans-serif; font-weight: 600; font-size: 13px; '
    'color: var(--bone)">Qui Sut Deus &#183; Ateli&#234;</div>'
    '<div style="font-family: system-ui, sans-serif; font-size: 12px; color: rgba(198,161,91,.9)">'
    'Roupa e arte sacra</div>'
    '<div style="font-family: system-ui, sans-serif; font-size: 13px; line-height: 1.5; '
    'color: rgba(237,230,214,.88)">&#8220;Quem como Deus?&#8221;<br>'
    'Camisetas de devoção desenhadas aqui, tiragem contada.<br>'
    'Encomendas pelo direct &#183; [CIDADE]</div>'
    '<div style="font-family: system-ui, sans-serif; font-size: 13px; color: #C6A15B">'
    '[LINK DA LOJA]</div></div>'

    '<div style="display: flex; gap: 8px; padding: 0 16px 18px">%s%s</div>'

    '<div style="display: flex; gap: 14px; padding: 0 16px 18px">%s</div>'

    '<div style="display: flex; border-top: 1px solid rgba(237,230,214,.12)">'
    '<div style="flex-grow: 1; height: 46px; display: flex; align-items: center; '
    'justify-content: center; border-bottom: 1px solid var(--gold)">'
    '<svg viewBox="0 0 24 24" width="19" height="19" style="display:block; fill:none; '
    'stroke:var(--bone); stroke-width:1.4"><path d="M3 3 L21 3 L21 21 L3 21 Z"/>'
    '<path d="M9 3 L9 21"/><path d="M15 3 L15 21"/><path d="M3 9 L21 9"/><path d="M3 15 L21 15"/></svg></div>'
    '<div style="flex-grow: 1; height: 46px; display: flex; align-items: center; '
    'justify-content: center">'
    '<svg viewBox="0 0 24 24" width="19" height="19" style="display:block; fill:none; '
    'stroke:rgba(237,230,214,.45); stroke-width:1.4"><path d="M4 4 L20 4 L20 20 L4 20 Z"/>'
    '<path d="M10 9 L16 12 L10 15 Z"/></svg></div></div>'

    '<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 2px; '
    'padding: 2px">%s</div>'

    '</div>' % (BONE, CINZEL,
                '<svg viewBox="0 0 24 24" width="18" height="18" style="display:block; fill:none; '
                'stroke:rgba(237,230,214,.7); stroke-width:1.5; stroke-linecap:round">'
                '<path d="M6 10 L12 16 L18 10"/></svg>',
                EMBLEM,
                stat % (BONE, '9', 'publica&#231;&#245;es'),
                stat % (BONE, '[&#8212;]', 'seguidores'),
                stat % (BONE, '[&#8212;]', 'seguindo'),
                btn % 'Editar perfil', btn % 'Compartilhar perfil',
                hl_row, cells))
write('Main.dc.html', main, 390, 844)

# -------------------------------------------------------------------- legendas
CAPS = [
 ('01 &#183; Abertura',
  'Quis ut Deus. &#8220;Quem como Deus?&#8221; &#8212; foi o que o arcanjo disse quando tudo '
  'se decidia.\n\nAbrimos este ateli&#234; para vestir essa pergunta. Desenho pr&#243;prio, '
  'tiragem contada, nada feito &#224;s pressas.\n\nFica por aqui: o primeiro lan&#231;amento '
  '&#233; dia [DIA] de [M&#202;S].',
  '#quisutdeus #saomiguelarcanjo #artesacra #modacatolica'),
 ('02 &#183; A arte',
  'S&#227;o Miguel Arcanjo, de corpo inteiro, para as costas da camiseta: 25 &#215; 33 cm de '
  'gravura.\n\nTudo tra&#231;o &#8212; asa por asa, an&#233;is da serpente, a espada no eixo. '
  'Nada de efeito, s&#243; linha.',
  '#saomiguelarcanjo #ilustracaosacra #artesacra #serigrafia'),
 ('03 &#183; A pe&#231;a',
  'Frente e costas. Emblema de 8 cm no peito &#8212; espada, nimbo e asas, sem detalhe fino que '
  'suma no tamanho pequeno. Arcanjo inteiro atr&#225;s.\n\nMalha preta, dourado por cima.',
  '#modacatolica #camisetacatolica #quisutdeus #ateliê'),
 ('04 &#183; Ora&#231;&#227;o',
  'S&#227;o Miguel Arcanjo, defendei-nos no combate.\n\nReze com a gente hoje. Se quiser, deixe '
  'nos coment&#225;rios por quem est&#225; pedindo &#8212; a gente reza junto.',
  '#saomiguelarcanjo #oracao #fecatolica #defendeinos'),
 ('05 &#183; O nome da casa',
  'Quis ut Deus? &#8212; &#8220;Quem como Deus?&#8221;\n\n&#201; o grito do arcanjo diante do '
  'orgulho, e o nome que escolhemos para a casa. Cada pe&#231;a sai daqui carregando essa '
  'pergunta.',
  '#quisutdeus #latim #saomiguelarcanjo #artesacra'),
 ('06 &#183; O detalhe',
  'De perto: a asa. Desenho vetorial, o que significa que sai limpo em serigrafia ou DTF, no '
  'tamanho que for.\n\nEsse &#233; o tipo de coisa que ningu&#233;m v&#234; de longe &#8212; e '
  'que muda a pe&#231;a toda.',
  '#vetor #serigrafia #detalhe #artesacra'),
 ('07 &#183; Dire&#231;&#227;o crua',
  'A mesma gravura em tinta sobre malha crua. Mais discreta, mais leve &#8212; pensada para o dia '
  'da festa, debaixo do sol.\n\nPreta ou crua? Diz aqui embaixo qual voc&#234; levaria.',
  '#modacatolica #malhacrua #camisetacatolica #quisutdeus'),
 ('08 &#183; Ficha',
  'O que voc&#234; leva: algod&#227;o penteado [GRAMATURA] g/m&#178;, impress&#227;o dourada, '
  'P ao GG, modelagem [MODELAGEM]. R$ [PRE&#199;O].\n\nD&#250;vida de tamanho? Manda no direct '
  'que a gente mede com voc&#234;.',
  '#fichatecnica #modacatolica #feitoamao #camisetacatolica'),
 ('09 &#183; Lan&#231;amento',
  '[DIA] de [M&#202;S]. Primeira tiragem, quantidade contada.\n\nEncomendas pelo direct ou em '
  '[LINK DA LOJA]. Quem avisar que veio por aqui entra primeiro na fila.',
  '#lancamento #quisutdeus #saomiguelarcanjo #modacatolica'),
]

cap_html = ''.join(
    '<div style="display: flex; flex-direction: column; gap: 12px">'
    '<div style="font-family: %s; font-size: 17px; letter-spacing: .26em; color: %s; '
    'text-indent: .26em">%s</div>'
    '<div style="height: 1px; background: %s; opacity: .3"></div>'
    '<div style="font-family: %s; font-size: 21px; line-height: 1.6; color: #2A2823; '
    'white-space: pre-line">%s</div>'
    '<div style="font-family: %s; font-size: 19px; color: #8C6B34">%s</div></div>'
    % (CINZEL, '#8C6B34', title, '#8C6B34', CORM, body, CORM, tags)
    for title, body, tags in CAPS)

bio_block = (
    '<div style="display: flex; flex-direction: column; gap: 12px">'
    '<div style="font-family: %s; font-size: 17px; letter-spacing: .26em; color: #8C6B34; '
    'text-indent: .26em">PERFIL</div>'
    '<div style="height: 1px; background: #8C6B34; opacity: .3"></div>'
    '<div style="font-family: %s; font-size: 21px; line-height: 1.7; color: #2A2823; '
    'white-space: pre-line">Usu&#225;rio: @quisutdeusatelie\n'
    'Nome: Qui Sut Deus &#183; Ateli&#234;\n'
    'Categoria: Roupa e arte sacra\n\n'
    'Bio (150 caracteres):\n&#8220;Quem como Deus?&#8221;\n'
    'Camisetas de devo&#231;&#227;o desenhadas aqui, tiragem contada.\n'
    'Encomendas pelo direct &#183; [CIDADE]\n[LINK DA LOJA]</div></div>' % (CINZEL, CORM))

legendas = (
    '<div style="width: 820px; background: #F4EFE4; padding: 70px 72px; box-sizing: border-box; '
    'display: flex; flex-direction: column; gap: 44px">'
    '<div style="display: flex; flex-direction: column; align-items: center; gap: 16px">'
    '<div style="font-family: %s; font-weight: 500; font-size: 40px; letter-spacing: .14em; '
    'color: #2A2823; text-indent: .14em">LEGENDAS</div>'
    '<div style="font-family: %s; font-style: italic; font-size: 22px; color: #8C6B34">'
    'o que vai escrito em cada um dos nove posts</div></div>'
    '%s%s'
    '<div style="font-family: %s; font-style: italic; font-size: 19px; line-height: 1.6; '
    'color: #6B6154">O que est&#225; entre [colchetes] &#233; para voc&#234; preencher: data, '
    'pre&#231;o, gramatura, modelagem, cidade e link.</div>'
    '</div>' % (CINZEL, CORM, bio_block, cap_html, CORM))
write('Legendas.dc.html', legendas, 820, 2840, gold_tweak=False)

# -------------------------------------------------------------------- canvas.json
canvas = {
  "pages": [{"id": "page-1", "name": "Perfil"}, {"id": "page-2", "name": "Feed"}],
  "artboards": [
    {"file": "Main.dc.html", "x": 0, "y": 0, "w": 390, "h": 844, "page": "page-1",
     "title": "Prévia do perfil"},
    {"file": "Avatar.dc.html", "x": 510, "y": 0, "w": 720, "h": 720, "page": "page-1",
     "title": "Foto de perfil"},
    {"file": "Destaques.dc.html", "x": 1350, "y": 0, "w": 1080, "h": 560, "page": "page-1",
     "title": "Capas de destaques"},
    {"file": "Legendas.dc.html", "x": 2550, "y": 0, "w": 820, "h": 2840, "page": "page-1",
     "title": "Legendas e bio", "print": "flow"},
  ] + [
    {"file": "Post%d.dc.html" % i, "x": ((i - 1) % 3) * 1200, "y": ((i - 1) // 3) * 1200,
     "w": 1080, "h": 1080, "page": "page-2", "title": t}
    for i, t in enumerate(["1 · Abertura", "2 · A arte", "3 · A peça",
                           "4 · Oração", "5 · O nome da casa",
                           "6 · O detalhe", "7 · Direção crua",
                           "8 · Ficha", "9 · Lançamento"], start=1)
  ],
  "annotations": [
    {"id": "nota-perfil", "x": 0, "y": -190, "w": 460, "page": "page-1",
     "text": "Perfil @quisutdeusatelie.\nA foto de perfil é o emblema sozinho — "
             "o círculo tracejado marca o corte redondo do Instagram.\nBio, link, cidade e "
             "preço estão entre [colchetes] para você preencher."},
    {"id": "nota-feed", "x": 0, "y": -190, "w": 520, "page": "page-2",
     "text": "Nove posts 1080 × 1080, na ordem de publicação (1 em cima à "
             "esquerda).\nOs dois claros — 3 e 7 — existem para abrir a grade; se trocar "
             "a ordem, mantenha-os em diagonal.\nAs legendas de cada um estão no artboard "
             "Legendas, na página Perfil."},
  ],
  "launch": {"view": "canvas", "page": "page-2"},
}
open(os.path.join(OUT, 'canvas.json'), 'w').write(json.dumps(canvas, indent=2, ensure_ascii=False))
print('canvas.json')
