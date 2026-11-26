# Kess Quiz — routine quotidienne

## YouTube Shorts (depuis le 26/11/2026) — publication AUTOMATIQUE, jamais de brouillon
Même vidéo que TikTok, publiée en Short via Buffer (Zernio ne gère que TikTok) :
`create_post` channelId "6b07f35d8541f09ecbacbce7" (Kess Quiz | Défi du jour, org 6afa0ec6b734c24f5af94d04 — partagée avec Tamko et Partners in Vice : ne JAMAIS toucher à leurs chaînes), schedulingType "automatic", mode "customScheduled", dueAt ISO avec décalage Paris (ex. 2026-11-27T13:00:00+01:00), text = yt_desc du manifest, assets [{"video": {"url": "<URL raw GitHub>"}}], metadata {"youtube": {"type": "short", "title": "<yt_title>", "categoryId": "24", "madeForKids": false, "privacy": "public", "isAiGenerated": false}}.
- Créneaux visés : vidéo 1 → 13:00, vidéo 2 → 18:00 (pic d'audience).
- Règle des 24 h glissantes (constatée sur les autres chaînes) : 2 Shorts max par 24 h. Avant de programmer, lire dans Buffer (list_posts sur ce channelId) le sentAt (ou dueAt) des 2 derniers Shorts ; le nouveau dueAt doit être ≥ celui du Short 2 rangs avant + 24 h 20. Si le créneau calculé dépasse 22:30, reporter au lendemain.
- Buffer gratuit : 10 posts programmés MAX pour toute l'organisation (3 chaînes) → ne programmer que les 2 Shorts du jour.
- Stats YouTube : Buffer list_posts includeMetrics sur ce channelId (un seul appel/jour).

## ⚠️ MODE BROUILLON TikTok UNIQUEMENT (depuis le 25/11/2026) — FAIT FOI sur la publication TikTok décrite plus bas
TikTok ne publie PAS en direct. Zernio envoie la vidéo en BROUILLON dans la boîte de réception TikTok, Mathieu colle la légende depuis le hub et publie à la main.
- posts_create_post avec `tiktok_settings.draft: true`, `scheduled_for` = 45 min AVANT l'heure de publication (TikTok livre le brouillon 20-35 min après l'envoi) : vidéo 1 → envoi 11:45 (publication 12:30), vidéo 2 → envoi 16:15 (publication 17:00). `content` = titre court (ex. « Spécial animaux »).
- La légende n'est PAS transmise par Zernio : l'écrire dans hub/kess.json → channel.drafts = [{"time": "12:30", "label": "<titre>", "caption": "<légende du manifest>"}, {"time": "17:00", ...}] (heure = heure de PUBLICATION conseillée).
- Étape 0 : les créneaux du jour sont « déjà faits » s'il existe des posts @kessquiz programmés aujourd'hui à 11:45 et 16:15.
- Durée : au moins 7 jours (jusqu'au 02/12 inclus). Ensuite, on ne repasse en publication directe QUE si Mathieu le valide. À partir du 03/12, ajouter dans alerts : « Kess Quiz : 7 jours de brouillons atteints, prêt pour la publication automatique si tu valides ».
- Confirmé par Mathieu le 26/11 : Kess Quiz, nouvelle chaîne, commence en brouillons.
- Étape 0 (suite) : ne jamais envoyer deux fois la même vidéo. Si une heure d'envoi est passée, envoyer dès que possible et indiquer dans le hub l'heure de publication ajustée.
- Avant l'envoi d'une nouvelle vidéo : durée 59-64 s (ffprobe) et une planche d'images (ffmpeg) à regarder (aucun texte qui déborde).

Compte TikTok @kessquiz (Zernio accountId `6b0727f75db4256264895cd7`). Vidéos ~61 s, générées 100 % en code.

1. Cloner : `git clone --depth 1 https://github.com/shinkoco/kessquiz-videos /home/claude/kessquiz-videos`.
2. Outils : `pip install --break-system-packages numpy pillow scipy piper-tts` si besoin, `which ffmpeg`.
   Voix Siwis (CC-BY, crédit en bio uniquement) :
   `mkdir -p /tmp/voices && curl -sL -o /tmp/voices/fr.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx && curl -sL -o /tmp/voices/fr.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json`
   Police Poppins : `/usr/share/fonts/truetype/google-fonts/Poppins-*.ttf` (sinon la télécharger depuis github.com/google/fonts, dossier ofl/poppins).
0. Vérifier d'abord dans Zernio (voir « Mode brouillon ») si les 2 envois du jour sont déjà programmés ou partis pour @kessquiz : si oui, ne rien générer (enrichir quand même la banque) et passer au rapport.
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
   Créneaux (heure de Paris) : vidéo 1 → 12:30, vidéo 2 → 17:00 (pic d'audience vers 18 h). Si un créneau est déjà passé ou à moins de 20 min : maintenant + 30 min (3 h minimum entre les deux).
7. Rapport : fichier, format/thème, nombre de questions, durée, ID du post Zernio.

## Règles éditoriales
- Durée visée 59,5–63,5 s : `fit()` choisit seul le nombre de questions et d'anecdotes. Jamais de remplissage.
- Rotation : pas le même thème que les 4 dernières vidéos, pas le même format deux fois d'affilée.
- Une question n'est republiée qu'une fois toute la banque du thème épuisée.
- Toute nouvelle question ajoutée à `engine/bank.py` doit être vérifiée (source fiable) AVANT ajout. Rien d'approximatif.
- Pas de faux boutons, pas de faux menus, pas d'images récupérées sur internet.

## Enrichissement de la banque (à chaque passage, AVANT de générer)
Lire d'abord `CARNET.md` (thèmes, idées, règles actualité) et y piocher.
Objectif : la banque doit toujours couvrir au moins 2 semaines de vidéos (2/jour, ~6 questions/vidéo).
- Ajouter 8 questions nouvelles (pas plus) dans `engine/bank.py` (QCM thématiques et/ou TROMPE), sur les thèmes existants ou de nouveaux thèmes (sport, corps humain, cuisine, records, espace, langues…). Pour un nouveau thème, l'ajouter aussi dans `THEMES` (libellé + couleur lisible sur fond clair) et dans `caption()` (hashtags) et dans `pick()`.
- Chaque fait est vérifié par une recherche web (source fiable : encyclopédie, site officiel, média reconnu) AVANT ajout. En cas de doute ou de sources contradictoires : ne pas ajouter.
- Pas de sujets sensibles (politique, religion, drames, personnes privées). Réponses courtes (< 22 caractères), 3 options plausibles, une seule bonne réponse indiscutable.
- Les identifiants sont uniques (préfixe du thème). Tester `python3 -c "exec(open('engine/bank.py').read())"` après modification.

## HUB (studiomgi.github.io, onglet KESS)
Après avoir programmé les posts, écrire `hub/kess.json` dans CE dépôt (la page le lit en direct), puis commit + push :
{"updated": ISO+01:00, "date_label": "Jeudi 26 novembre", "alerts": ["Kess Quiz : …"] (vide si rien), "channel": {...}}
`channel` : name "Kess Quiz" ; headline [début, fin en gras] ; summary 1-2 phrases ; kpis [{platform "TikTok", label "Meilleure vidéo", detail, value (vues ou null), unit "vues", bar 0-1}] ;
followers {label "Abonnés TikTok", value (Zernio accounts_get_follower_stats), goal 1000} ; today [{time, platform "TikTok", title (ex. « Spécial animaux »), status programmé|publié|échec}] ;
upcoming [{day, text}] ; trend {labels 7 derniers jours "dd/mm", series {"TikTok": vues/jour via analytics_get_daily_metrics}} ; engagement {likes, comments, shares, followers_gain} ; best_time.
Ne JAMAIS inventer un chiffre : null si inconnu. Un seul appel par source et par jour.
