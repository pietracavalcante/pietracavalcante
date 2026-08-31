<!doctype html>
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
    body { margin: 0; font-family: 'Cormorant Garamond', Georgia, serif; }
    a { color: #C6A15B; } a:hover { color: #E0C289; }
  </style>
</helmet>
<div style="--gold: {{gold}}; --bone: #EDE6D6; width: 960px; height: 1300px; background: #0E0F13; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; padding: 44px 0 0; box-sizing: border-box; overflow: hidden">

  <div style="width: 700px">
    <!--ART-->
  </div>

  <div style="display: flex; flex-direction: column; align-items: center; gap: 16px; margin-top: 30px">

    <div style="font-family: 'Cinzel', 'Trajan Pro', Georgia, serif; font-weight: 500; font-size: 86px; line-height: .96; letter-spacing: .1em; color: var(--bone); text-indent: .1em">SÃO MIGUEL</div>

    <div style="display: flex; align-items: center; gap: 22px; width: 640px">
      <div style="flex-grow: 1; height: 1px; background: var(--gold); opacity: .55"></div>
      <div style="font-family: 'Cinzel', 'Trajan Pro', Georgia, serif; font-weight: 400; font-size: 38px; letter-spacing: .42em; color: var(--gold); text-indent: .42em">ARCANJO</div>
      <div style="flex-grow: 1; height: 1px; background: var(--gold); opacity: .55"></div>
    </div>

    <div style="font-family: 'Cinzel', 'Trajan Pro', Georgia, serif; font-weight: 400; font-size: 21px; letter-spacing: .3em; color: var(--bone); opacity: .82; text-indent: .3em; margin-top: 6px">DEFENDEI-NOS NO COMBATE</div>

    <div style="display: flex; align-items: center; gap: 14px; margin-top: 4px">
      <svg viewBox="0 0 24 24" width="13" height="13" style="display:block"><path d="M12 1 L15 12 L12 23 L9 12 Z" fill="var(--gold)" opacity=".8"/></svg>
      <div style="font-family: 'Cormorant Garamond', Georgia, serif; font-style: italic; font-weight: 400; font-size: 25px; letter-spacing: .16em; color: var(--gold); opacity: .8">Quis ut Deus</div>
      <svg viewBox="0 0 24 24" width="13" height="13" style="display:block"><path d="M12 1 L15 12 L12 23 L9 12 Z" fill="var(--gold)" opacity=".8"/></svg>
    </div>

  </div>
</div>
</x-dc>
<script data-dc-script data-props='{"gold":{"editor":"color","default":"#C6A15B","options":["#C6A15B","#D8B77A","#8C6B34","#EDE6D6"],"section":"Cor"},"$preview":{"width":960,"height":1300}}'>
class Component extends DCLogic {
  renderVals() {
    return { gold: this.props.gold ?? '#C6A15B' };
  }
}
</script>
</body>
</html>
