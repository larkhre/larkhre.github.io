// Exécute un programme avec le moteur JavaScript du playground (docs/index.html)
// et écrit sur la sortie exactement ce que le moteur Python afficherait.
// Utilisation : node tests/run_js.js programme.laz [entrees.in]
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '..', 'docs', 'code', 'index.html'), 'utf8');
const bloc = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)]
  .map(m => m[1]).find(s => s.includes('const Larkhre = (function'));
if (!bloc) { console.error('moteur introuvable dans docs/index.html'); process.exit(2); }
const mod = { exports: {} };
new Function('module', 'exports', 'require', bloc)(mod, mod.exports, require);
const Moteur = mod.exports;

const [fichier, fichierEntrees] = process.argv.slice(2);
const source = fs.readFileSync(fichier, 'utf8');
const entrees = fichierEntrees && fs.existsSync(fichierEntrees)
  ? fs.readFileSync(fichierEntrees, 'utf8').split('\n') : [];

let sortie = '';
(async () => {
  const r = await Moteur.run(source, {
    onPrint: (t) => { sortie += t + '\n'; },
    onInput: async (invite) => { sortie += invite; return entrees.length ? entrees.shift() : ''; },
    shouldStop: () => false,
  });
  if (!r.ok && r.error) {
    sortie += r.error + '\n';
    if (r.histoire && r.histoire.length) {
      sortie += "\n— Le film juste avant l'erreur :\n";
      for (const [l, n, v] of r.histoire) sortie += '   ligne ' + l + ' : ' + n + ' = ' + v + '\n';
    }
  }
  process.stdout.write(sortie);
})();
