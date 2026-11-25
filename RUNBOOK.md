# Kess Quiz — routine quotidienne

Compte TikTok @kessquiz (Zernio accountId `6b0727f75db4256264895cd7`). Vidéos ~61 s, générées 100 % en code.

1. Cloner : `git clone --depth 1 https://github.com/shinkoco/kessquiz-videos /home/claude/kessquiz-videos`.
2. Outils : `pip install --break-system-packages numpy pillow scipy piper-tts` si besoin, `which ffmpeg`.
   Voix Siwis (CC-BY, crédit en bio uniquement) :
   `mkdir -p /tmp/voices && curl -sL -o /tmp/voices/fr.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx && curl -sL -o /tmp/voices/fr.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json`
   Police Poppins : `/usr/share/fonts/truetype/google-fonts/Poppins-*.ttf` (sinon la télécharger depuis github.com/google/fonts, dossier ofl/poppins).
0. Vérifier d'abord dans Zernio (`posts_list` status scheduled) si les 2 créneaux du jour sont déjà programmés pour @kessquiz : si oui, ne rien générer et passer au rapport.
3. Générer : `cd engine && python3 daily.py ../videos 2` → vidéo + `../videos/manifest.json` (file, kind, theme, n, duration, caption) ; `engine/history.json` mis à jour (questions déjà publiées).
   Forcer un format : `KQ_FORMAT=qcm:animaux` / `drapeaux:drapeaux` / `trompe:trompe`.
4. Nettoyer : supprimer les `videos/kq_*.mp4` de plus de 3 jours.
5. Commit + push sur `main` (vidéo, manifest, history.json).
6. Publier sur TikTok via Zernio (`call_tool` → `posts_create_post`) :
```json
{"content":"<caption>","media_items":[{"type":"video","url":"https://raw.githubusercontent.com/shinkoco/kessquiz-videos/main/videos/<file>"}],
 "scheduled_for":"<YYYY-MM-DDTHH:MM:00>","timezone":"Europe/Paris",
 "platforms":[{"platform":"tiktok","accountId":"6b0727f75db4256264895cd7","scheduledFor":"<YYYY-MM-DDTHH:MM:00>"}],
 "tiktok_settings":{"privacyLevel":"PUBLIC_TO_EVERYONE","allowComment":true,"allowDuet":true,"allowStitch":true,
   "contentPreviewConfirmed":true,"expressConsentGiven":true,"videoCoverTimestampMs":1500}}
```
   Créneaux (heure de Paris) : vidéo 1 → 12:30, vidéo 2 → 17:00 (pic d'audience vers 18 h). Si un créneau est déjà passé ou à moins de 20 min, le lendemain même heure.
7. Rapport : fichier, format/thème, nombre de questions, durée, ID du post Zernio.

## Règles éditoriales
- Durée visée 59,5–63,5 s : `fit()` choisit seul le nombre de questions et d'anecdotes. Jamais de remplissage.
- Rotation : pas le même thème que les 4 dernières vidéos, pas le même format deux fois d'affilée.
- Une question n'est republiée qu'une fois toute la banque du thème épuisée.
- Toute nouvelle question ajoutée à `engine/bank.py` doit être vérifiée (source fiable) AVANT ajout. Rien d'approximatif.
- Pas de faux boutons, pas de faux menus, pas d'images récupérées sur internet.

## Enrichissement de la banque (à chaque passage, AVANT de générer)
Objectif : la banque doit toujours couvrir au moins 2 semaines de vidéos (2/jour, ~6 questions/vidéo).
- Ajouter 10 à 15 questions nouvelles dans `engine/bank.py` (QCM thématiques et/ou TROMPE), sur les thèmes existants ou de nouveaux thèmes (sport, corps humain, cuisine, records, espace, langues…). Pour un nouveau thème, l'ajouter aussi dans `THEMES` (libellé + couleur lisible sur fond clair) et dans `caption()` (hashtags) et dans `pick()`.
- Chaque fait est vérifié par une recherche web (source fiable : encyclopédie, site officiel, média reconnu) AVANT ajout. En cas de doute ou de sources contradictoires : ne pas ajouter.
- Pas de sujets sensibles (politique, religion, drames, personnes privées). Réponses courtes (< 22 caractères), 3 options plausibles, une seule bonne réponse indiscutable.
- Les identifiants sont uniques (préfixe du thème). Tester `python3 -c "exec(open('engine/bank.py').read())"` après modification.
