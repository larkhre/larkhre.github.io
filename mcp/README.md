# larkhre-mcp 🤖

**Le serveur MCP du langage [Larkhré](https://larkhre.github.io/code/)** — il donne à n'importe quel agent IA (Claude, et tout client compatible Model Context Protocol) le pouvoir d'**écrire ET d'exécuter** du code Larkhré pour de vrai.

## Ce que l'IA peut faire

- `spec_larkhre` — lire la spécification complète du langage (mots-clés, 48 fonctions, pièges, exemples)
- `executer_larkhre` — lancer un programme et recevoir : la sortie console, les **erreurs pédagogiques en français**, les **dessins SVG**, les fichiers écrits, les paroles `dis()`, les sons, et la mémoire persistante `garde`

Demandez à votre IA : *« Code-moi un jeu en Larkhré et teste-le »* — elle écrit le code, l'exécute, lit les erreurs, corrige, et vous livre un programme **vérifié**.

## Installation (Claude Desktop)

Dans votre fichier `claude_desktop_config.json` :

```json
{
  "mcpServers": {
    "larkhre": {
      "command": "npx",
      "args": ["-y", "larkhre-mcp"]
    }
  }
}
```

Redémarrez Claude Desktop — les outils `executer_larkhre` et `spec_larkhre` apparaissent.

## Tout client MCP

```bash
npx -y larkhre-mcp   # serveur stdio
```

## Le bac à sable

- Exécution limitée à 8 secondes / 240 images de jeu — les boucles infinies s'arrêtent proprement
- Fichiers virtuels (rien n'est écrit sur le disque)
- `demand()` lit le paramètre `entrees` ; `garde` persiste le temps de la session

---
*Larkhré — un langage libre (MIT) créé par Ladji Doucaré ·
[Playground](https://larkhre.github.io/code/) ·
[GitHub](https://github.com/larkhre/larkhre.github.io) ·
`pip install larkhre` · `npm install larkhre`*
