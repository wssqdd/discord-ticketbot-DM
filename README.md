# 🎫 Discord Ticket Bot

Un bot Discord simple et efficace pour gérer un système de tickets via messages privés (DMs). Les utilisateurs peuvent contacter le support en envoyant des messages privés au bot, et l'équipe de modération peut répondre directement depuis un canal dédié.

## ✨ Fonctionnalités

- **📩 Système de tickets via DMs** - Les utilisateurs envoient des messages privés au bot
- **💬 Réponses directes** - L'équipe peut répondre via une interface modale
- **📋 Transcriptions automatiques** - Historique complet des conversations sauvegardé
- **🔒 Système on/off** - Activation/désactivation du système de tickets
- **🗑️ Suppression de tickets** - Avec génération automatique de transcription
- **👥 Interface staff intuitive** - Boutons répondre/supprimer pour chaque message

## 🚀 Installation

### Prérequis
- Python 3.8 ou plus récent
- Un bot Discord avec les permissions nécessaires

### Étapes d'installation

1. **Cloner le repository**
   ```bash
   git clone https://github.com/votre-username/discord-ticket-bot.git
   cd discord-ticket-bot
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration**
   Créez un fichier `config.json` à la racine du projet :
   ```json
   {
       "token": "VOTRE_TOKEN_BOT",
       "channel_ticket_id": "ID_CANAL_TICKETS",
       "transcript_ticket_id": "ID_CANAL_TRANSCRIPTIONS",
       "color": "0x00ff00",
       "state_ticket": "on"
   }
   ```

4. **Lancer le bot**
   ```bash
   python main.py
   ```

## ⚙️ Configuration

### config.json
- `token` : Token de votre bot Discord
- `channel_ticket_id` : ID du canal où apparaissent les nouveaux messages
- `transcript_ticket_id` : ID du canal où sont envoyées les transcriptions
- `color` : Couleur des embeds (format hexadécimal)
- `state_ticket` : État du système ("on" ou "off")

### Permissions Discord requises
- `Send Messages`
- `Read Messages`
- `Embed Links`
- `Attach Files`
- `Read Message History`

## 🎮 Utilisation

### Pour les utilisateurs
1. Envoyer un message privé au bot
2. Le message apparaît dans le canal des tickets
3. Recevoir les réponses de l'équipe de support

### Pour l'équipe de modération

#### Commandes
- `+unlock_ticket` - Active le système de tickets
- `+lock_ticket` - Désactive le système de tickets

#### Interface
- **Bouton "Répondre"** - Ouvre une fenêtre modale pour répondre à l'utilisateur
- **Bouton "Supprimer"** - Supprime le ticket et génère une transcription

### Transcriptions
Les transcriptions incluent :
- Horodatage de chaque message
- Nom de l'auteur (Bot/Utilisateur)
- Contenu des messages et embeds
- URLs des pièces jointes
- Format `.txt` facilement lisible

## 🔧 Structure du projet

```
discord-ticket-bot/
├── main.py              # Code principal du bot
├── config.json          # Configuration (à créer)
├── requirements.txt     # Dépendances Python
└── README.md           # Documentation
```

## 📝 Exemple de flux de travail

1. **Utilisateur** : Envoie un DM au bot "J'ai un problème avec mon compte"
2. **Système** : Le message apparaît dans le canal des tickets avec des boutons
3. **Staff** : Clique sur "Répondre" et tape sa réponse
4. **Utilisateur** : Reçoit la réponse sous forme d'embed
5. **Staff** : Clique sur "Supprimer" quand le problème est résolu
6. **Système** : Génère une transcription et l'envoie dans le canal dédié

## 🛠️ Personnalisation

Le bot peut être facilement personnalisé :
- Modifier les couleurs des embeds
- Changer les textes des messages
- Ajouter de nouvelles fonctionnalités
- Modifier le format des transcriptions

## 📋 TODO / Améliorations futures

- [ ] Système de catégories de tickets
- [ ] Statistiques d'utilisation
- [ ] Système de ratings/feedback
- [ ] Interface web pour consulter les tickets
- [ ] Support multi-serveurs

## 🐛 Signaler un bug

Si vous trouvez un bug, merci de créer une issue avec :
- Description détaillée du problème
- Étapes pour reproduire
- Logs d'erreur si disponibles
- Informations sur votre environnement

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commit vos changements
4. Push vers la branche
5. Ouvrir une Pull Request

---

**⚡ Fait avec ❤️ pour la communauté Discord**
