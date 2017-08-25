Installation
============

## Prérequis et installation minimale

Nous recommendons l'installation d'un environnement virtuel avec `virtualenv`.
```
$ virtualenv -p python3.5 ../venv
$ . ../venv/bin/activate
```

puis 

```
$ python setup.py install
```

L'installation de toutes ces librairies reposent parfois sur des paquets "systèmes". Pour une distribution linux basée sur Debian, assurez-vous que les paquets suivants sont installés:

- libxml2-dev
- libxslt-dev
- python-libxml2
- python-libxslt1
- python-dev
- zlib1g-dev


## Exécution du script en local

```
$ cnparser --help
```
