# larkhre

Le moteur de **Larkhré** (*mosi larkhré* : « la langue de la machine », en soninké),
le langage pour apprendre à coder en français. C'est exactement le moteur du
[playground](https://larkhre.github.io/code/).

```bash
npm install larkhre
```

```js
const Larkhre = require('larkhre');
await Larkhre.run('laz nom = "Awa"\nvox("Bonjour {nom} !")', {
  onPrint: console.log,
  onInput: async (invite) => '',
});
```
