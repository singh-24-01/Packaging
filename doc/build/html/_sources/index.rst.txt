.. ng20-lda documentation master file

Documentation ng20-lda
======================

.. image:: https://img.shields.io/badge/python-3.11+-blue.svg
   :target: https://www.python.org/downloads/

Ce projet est réalisé dans le cadre du TP de *Packaging Python*. 
Il implémente une chaîne de traitement complète pour l'analyse de thématiques (LDA) sur le dataset 20 Newsgroups.

.. toctree::
   :maxdepth: 2
   :caption: Guide Utilisateur
   :hidden:

   Installation <self>
   usage

Fonctionnalités principales
---------------------------

Le package fournit quatre outils en ligne de commande :

* **Export** : Téléchargement et organisation des documents par catégorie.
* **Entraînement** : Création d'un modèle LDA (Latent Dirichlet Allocation) sauvegardé via Pickle.
* **Description** : Analyse d'un document pour afficher les 3 thèmes majeurs.
* **Utilitaires** : Comptage performant de lignes dans des fichiers texte.

Référence Technique
-------------------

Si vous cherchez des détails sur l'implémentation des modules, consultez la documentation générée automatiquement :

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
