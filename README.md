# Back-End for CARBON ©

## Présentation du projet:

La pollution générée par l’industrie du net et son impact sur le climat sont équivalents à ceux du secteur de l’aviation.

L'empreinte écologique du numérique est loin d'être négligeable même si elle paraît anodine comparée à d'autres secteurs et qu'il est difficile de croire que l'on puisse "polluer" en surfant sur Internet et pourtant c'est ce qui se passe !

Nous avons décidé de traiter cette problématique en se focalisant sur l'impact des réseaux sociaux sur l'environnement et de là, notre choix s'est porté sur le réseau social Twitter.

A fin de garantir la meilleure expérience utilisateur (qu'elle soit interactive, immersive mais aussi impactante), nous avons conçu et développé une datavisualisation adaptée à notre thématique. 

Quel est donc l'impact environnemental de votre activité sur Twitter ? 

On vous donne rendez-vous sur notre site [Carbon](https://carbonproject.netlify.app/) pour découvrir la réponse !

## Organisation du projet: 

En ce qui concerne l'organisation, nous avons opté d'utiliser l'application [Notion](https://www.notion.so/carbonproject/Compte-rendu-data-Ecologique-60d2de0b9e514b54a05626d54f7154ba), nous avons mis en place plusieurs workspaces (calendrier, data ...), et delà une mise à jour quotidienne été établie, ce qui nous permettait de suivre l'avancement de notre projet.
Nous avons bien séparé la partie Front et Back.
[@Youness](https://github.com/younessidbakkasse) a choisi les technos coté back et front.
[@Nassim](https://github.com/Nassim-dev) s'est principalement occupé seul de la partie back et de la recherche de la data-écologique avec l'aide de [@Tania](https://github.com/TaniaMAHOUCHE).
Nous avons séparé en deux branches une dev et une prod, tous les test se sont fait en local.

## Technologies côté back-end:
- [Docker](https://docs.docker.com/) est un logiciel libre permettant de créer des contenuers logiciels. Dans une équipe, chaque personne a différent système d'exploitation, et des versions différentes, cela peut créer des problèmes en productions. L'avantage de Docker est de permettre de créer et travailler dans un environnement qui tourne dans tout type d'ordinateur et serveur, ce dernier nous a beaucoup facilité l'hébergement de notre API avec un seul ligne de commande, on a pu héberger notre API sur [DigitalOcean](https://www.digitalocean.com/products/droplets/) sur un Droplet(serveur Linux Ubunto aui vient avec Docker et Git installés.), pour transfer les fichier de notre machine en local au serveur en 138.68.103.215, on a utilisé git avec un ```git pull origin prod```en suite on a lancé la container de l'application basé sur Python v3.9 avec la commande ```docker compose up```.

- [FastAPI](https://fastapi.tiangolo.com/) est un framework web pour construire des API sur Python. Il est très rapide et simple d'utilisation, avec une documentation bien construite. (c'est comme Flask pour les connaisseurs)

- [Tweepy](https://www.tweepy.org/) est une librairie Python et un client (SDK community) pour intéragir avec l'API de Twitter en utilisant Python, ceci nous a permet de scrapper les données sur Twitter.

- [API Twitter](https://developer.twitter.com/en) nous a permis d'avoir l'accès aux données avec des clefs secrètes et uniques qu'on a caché dans un fichier .env, une documentation très instructive et détaillée. Nous avons principalement décidé de travailler sur Twitter grâce à l'accès aux données moins restreints que d'autre social media, mais aussi notamment grâce à leur documentation.
 
- [Python](https://docs.python.org/fr/3/) est un langage de programmation interprété, multi-paradigme. Nous avons choisi de travailler sur Python car j'y suis plus à l'aise, et il est notamment très utilisé en data-science et machine learning. Parfait alors pour un projet de datavisualisation.

- [JSON](https://www.json.org/json-en.html) JavaScript Object Notation est un format de données textuelles dérivé de la notation des objets du langage JavaScript. Nous envoyons toutes les données collectés et mes calculs sous le format JSON pour qu'il puisse être traité par la suite par l'équie Front.


## Récolte de la data-écologique
[lien d'accès au notion](https://www.notion.so/carbonproject/Compte-rendu-data-Ecologique-60d2de0b9e514b54a05626d54f7154ba)
 Vous y retrouverez tous les détails des calculs et la liste des associations concernées.
 
 Tania et moi même avons cherché partout, contacté une dizaine d'association pour récolter des infos et des data concernant la pollution numérique des réseaux sociaux et de Twitter. Malheureusement, il y a beaucoup de recherche en cours et peu de résultat concrêt.
 
Je suis parti dans l'idée de créer une forme de pondération et d'approximation pour mes calculs.
0.02g EqCO2 for 140 charact. per minute on server
1 charact = 0.001g

image = 0.2g EqCO2 max 1mb. per minute on server

estimate of 400g EqCO2 per hour (durée de la video) max 512 MB. per minute on server
durée max video = 2mn20
video = 13.5g EqCO2 max per minute on server
 
 ## Lien d'accès à l'API:
http://138.68.103.215/
  
### points d'accées:
On a plusuiers points d'accées mais le principale pour récuperer la data sous format .json traités est: http://138.68.103.215/user/<username> exemple pour tester http://138.68.103.215/user/cristiano avec username est pseudo twitter de l'utilisateur, notre API est sécurisé avec CORS, donc personne ne peut l'utiliser que notre site hébergé sur netlify.
  
 L'équipe Back-End CARBON :)

### Contributeurs:

- Nassim Yazi (Calculs/API)
- Youness Ib Bakkasse (Choix de techno/Sécurité/Hébergement)
