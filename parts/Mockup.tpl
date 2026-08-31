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
    a { color: #8C6B34; } a:hover { color: #6E5326; }
  </style>
</helmet>
<div style="width: 1440px; height: 900px; background: #E9E2D6; display: flex; align-items: center; justify-content: center; gap: 120px; box-sizing: border-box; overflow: hidden">

  <div style="display: flex; flex-direction: column; align-items: center; gap: 26px">
    <div style="position: relative; width: 520px; height: 624px">
      <!--SHIRT_FRONT-->
      <div style="position: absolute; left: 56.5%; top: 25.5%; width: 62px; height: 72px; overflow: hidden">
        <div style="width: 360px; height: 420px; transform: scale(.1722); transform-origin: top left"><!--FRONTDESIGN--></div>
      </div>
    </div>
    <div style="font-family: 'Cinzel', Georgia, serif; font-size: 17px; letter-spacing: .4em; color: #6B6154; text-indent: .4em">FRENTE</div>
  </div>

  <div style="display: flex; flex-direction: column; align-items: center; gap: 26px">
    <div style="position: relative; width: 520px; height: 624px">
      <!--SHIRT_BACK-->
      <div style="position: absolute; left: 27%; top: 21%; width: 239px; height: 324px; overflow: hidden">
        <div style="width: 960px; height: 1300px; transform: scale(.249); transform-origin: top left"><!--BACKDESIGN--></div>
      </div>
    </div>
    <div style="font-family: 'Cinzel', Georgia, serif; font-size: 17px; letter-spacing: .4em; color: #6B6154; text-indent: .4em">COSTAS</div>
  </div>

</div>
</x-dc>
<script data-dc-script data-props='{"$preview":{"width":1440,"height":900}}'>
class Component extends DCLogic {}
</script>
</body>
</html>
