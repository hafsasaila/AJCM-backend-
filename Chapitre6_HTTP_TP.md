# Chapitre 6 — Le Protocole HTTP (Travaux Pratiques)

# Sommaire
- TP1 — Exploration avec DevTools
- TP2 — Maîtrise de cURL
- TP3 — API REST avec JavaScript
- TP4 — Analyse des Headers de Sécurité
- TP5 — Cache HTTP
- Exercices récapitulatifs

---

# TP 1 : Exploration avec les DevTools

## Objectifs
- Analyser les requêtes/réponses HTTP
- Comprendre les headers
- Observer les codes de statut

---

## 1.1 Ouvrir les DevTools

- Ouvrir Chrome ou Firefox
- F12 ou Ctrl+Shift+I
- Onglet Network

---

## 1.2 Observer une requête simple

URL :

```text
https://httpbin.org/get
```

### Résultats

Code de statut :

```http
200 OK
```

Headers observés :

```http
Host: httpbin.org
User-Agent: Mozilla/Chrome
Accept: */*
Accept-Language: fr-FR
Accept-Encoding: gzip
Connection: keep-alive
```

Content-Type :

```http
application/json
```

---

## 1.3 Tester différentes méthodes

### GET

```javascript
fetch('https://httpbin.org/get')
.then(r=>r.json())
.then(console.log);
```

---

### POST

```javascript
fetch('https://httpbin.org/post',{
 method:'POST',
 headers:{
   'Content-Type':'application/json'
 },
 body:JSON.stringify({
   name:'John',
   age:30
 })
});
```

---

## 1.4 Codes de statut

| URL | Code | Signification |
|---|---|---|
| status/200 | 200 | Succès |
| status/404 | 404 | Introuvable |
| status/500 | 500 | Erreur serveur |
| redirect/3 | 302 puis 200 | Redirection |

---

## Tableau récapitulatif

| URL | Méthode | Code | Content-Type |
|---|---|---|---|
| httpbin.org/get | GET | 200 | application/json |
| httpbin.org/post | POST | 200 | application/json |
| httpbin.org/status/201 | GET | 201 | text/html |

---

# TP 2 : Maîtrise de cURL

## GET simple

```bash
curl https://httpbin.org/get
curl -i https://httpbin.org/get
curl -v https://httpbin.org/get
```

## Différence entre -i et -v

### -i

Affiche :

- headers réponse
- body

---

### -v

Mode debug :

- détails connexion
- headers envoyés
- TLS
- diagnostic réseau

---

## POST Form

```bash
curl -X POST \
-d "name=John&email=john@example.com" \
https://httpbin.org/post
```

---

## POST JSON

```bash
curl -X POST \
-H "Content-Type: application/json" \
-d '{"name":"John","email":"john@example.com"}' \
https://httpbin.org/post
```

---

## Headers personnalisés

```bash
curl \
-H "Authorization: Bearer mon-token-secret" \
-H "Accept: application/json" \
https://httpbin.org/headers
```

---

## Redirections

```bash
curl https://httpbin.org/redirect/3
curl -L https://httpbin.org/redirect/3
```

---

## Télécharger un fichier

```bash
curl -o image.png https://httpbin.org/image/png
```

```bash
curl -O https://example.com/fichier.pdf
```

---

## Exercice avancé

```bash
curl -i -X POST \
-H "Content-Type: application/json" \
-H "X-Custom-Header: MonHeader" \
-d '{"action":"test","value":42}' \
https://httpbin.org/post
```

---

# TP 3 : API REST avec JavaScript

## GET

```javascript
fetch('https://jsonplaceholder.typicode.com/users')
.then(r=>r.json())
.then(console.log)
.catch(console.error);
```

---

## POST

```javascript
createPost({
 title:'Mon article',
 body:'Contenu',
 userId:1
});
```

---

## PUT

```javascript
updatePost(1,{
 title:'Article modifié'
});
```

---

## DELETE

```javascript
deletePost(1);
```

---

## fetchWithRetry

```javascript
async function fetchWithRetry(
 url,
 options={},
 maxRetries=3
){

 for(let i=0;i<=maxRetries;i++){

  try{

   let response=
      await fetch(url,options);

   if(
     response.status>=500 &&
     response.status<600
   ){
      throw new Error();
   }

   return response;

  }

  catch(error){

   if(i===maxRetries){
      throw error;
   }

   await new Promise(
      r=>setTimeout(r,1000)
   );

  }

 }

}
```

---

# TP 4 : Headers de Sécurité

## Vérification

```bash
curl -I https://google.com
```

```bash
curl -s -D - https://github.com \
-o /dev/null \
| grep -i "strict\|x-frame\|x-content\|content-security"
```

---

## Analyse

| Site | HSTS | X-Frame | CSP | Note |
|---|---|---|---|---|
| github.com | Oui | Oui | Oui | A+ |
| google.com | Oui | Oui | Oui | A |
| example.com | Non | Non | Non | Faible |

---

## Headers importants

| Header | But |
|---|---|
| Strict-Transport-Security | Forcer HTTPS |
| X-Frame-Options | Anti-clickjacking |
| X-Content-Type-Options | Anti-sniffing |
| CSP | Contrôle scripts |
| Referrer-Policy | Contrôle referrer |

---

# TP 5 : Cache HTTP

## Observer le cache

```bash
curl -i https://httpbin.org/cache/60
```

Chercher :

```http
Cache-Control
ETag
Expires
```

---

## Requête conditionnelle

```bash
curl -i https://httpbin.org/etag/test123
```

---

```bash
curl -i \
-H "If-None-Match: test123" \
https://httpbin.org/etag/test123
```

Réponse :

```http
304 Not Modified
```

---

## Cache recommandé

Images :

```http
Cache-Control: public,max-age=31536000
```

CSS/JS :

```http
Cache-Control: public,max-age=86400
```

---

# Exercices Récapitulatifs

---

## Exercice 1 — Client HTTP minimaliste

Le script doit :

- saisir URL
- choisir méthode
- envoyer requête
- afficher :
  - statut
  - headers
  - body

---

## Exercice 2 — Questions théoriques

### no-cache vs no-store

## no-cache

- stockable
- revalidation obligatoire

## no-store

- jamais stocké

---

## Pourquoi POST n'est pas idempotent

Deux POST peuvent créer :

- deux commandes
- deux paiements
- deux utilisateurs

---

## Code 301

```http
301 Moved Permanently
```

- redirection permanente
- nouvelle URL utilisée

---

## Header Origin

Exemple :

```http
Origin: https://monsite.com
```

Utilisé pour :

- CORS
- sécurité cross-origin

---

## HttpOnly

```http
Set-Cookie: session=abc; HttpOnly; Secure
```

Protège contre :

- vol de session
- XSS

---

# Conclusion

Ce chapitre a permis de pratiquer :

- HTTP et DevTools
- cURL
- APIs REST
- sécurité des headers
- cache HTTP