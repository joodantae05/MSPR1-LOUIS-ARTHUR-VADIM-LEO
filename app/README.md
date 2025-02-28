# MSPR_TPRE511
 MSPR 1 python

dashboard_page.py : Affichage du nombre d'hôtes connectés, leur ip, les ports ouverts, les services et les vulnérabilités associés, la date du dernier scan, les infos de la machine hotes (os, ip, nom) et versioning de l'application à partir des dernières mises à jours dans le dépôt.

home_page.py : Page par défaut avec la navbar

main.py : page principale avec l'affichage de la page avec le bouton de scan et la barre de progression

scan.py : effectue un scan réseau à partir de la plage ip de l'adresse ip locale de la machine hôte avec la librairie nmap-python (nmap -sV -T4)

stats_page.py : nb de scan total, temps moyen de scan du réseau, l'hôte le plus vulnérable

scan_results.json : stocke le résultat du dernier scan effectué

scanned_ips.txt : stocke uniquement les adresses IP pour effectuer un ping

stats.json : stocke les statistiques des scans (date du scan, nombre de scans réalisés, temps moyen des scan, hôte le plus vulnérable)