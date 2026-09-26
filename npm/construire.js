// Fabrique npm/larkhre.js à partir du moteur du playground (docs/code/index.html),
// pour que le paquet npm et le site utilisent toujours exactement le même moteur.
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'docs', 'code', 'index.html'), 'utf8');
const bloc = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)]
  .map(m => m[1]).find(s => s.includes('const Larkhre = (function'));
if (!bloc) { console.error('moteur introuvable dans docs/code/index.html'); process.exit(1); }
const entete = '// Larkhré — moteur officiel (généré depuis docs/code/index.html par construire.js, ne pas modifier à la main)\n';
fs.writeFileSync(path.join(__dirname, 'larkhre.js'), entete + bloc.trim() + '\n');
console.log('npm/larkhre.js généré');
