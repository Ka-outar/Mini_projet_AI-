# Planification Robuste sur Grille : A* + Chaînes de Markov 🤖🗺️

Ce dépôt contient le code source et les résultats du mini-projet réalisé dans le cadre du module **Bases de l'Intelligence Artificielle** (Master SDIA1 - ENSET Mohammedia).

## 📖 À propos du projet

L'objectif de ce projet est de concevoir une solution hybride pour la planification de trajectoire d'un agent sur une grille 2D contenant des obstacles. L'agent doit atteindre une cible (GOAL) en minimisant son coût de déplacement. 

Le projet se divise en deux phases majeures :
1. **Planification Déterministe :** Recherche du chemin optimal dans un environnement idéalisé à l'aide d'algorithmes de recherche heuristique.
2. **Modélisation Stochastique (Markov) :** Évaluation de la robustesse de ce plan lorsque l'agent est soumis à des incertitudes de déplacement (glissements, erreurs d'action) via des chaînes de Markov à temps discret.

## ✨ Fonctionnalités implémentées

* **Algorithmes de Recherche (Pathfinding) :**
  * **UCS** (Uniform Cost Search) - Recherche non informée.
  * **Greedy Best-First Search** - Recherche dirigée par l'heuristique.
  * **A*** - Recherche optimale combinant coût réel et heuristique ($f = g + h$).
  * **Weighted A*** - Variante sacrifiant la garantie d'optimalité pour la vitesse.
* **Heuristique :** Implémentation de la distance de Manhattan.
* **Modélisation Markovienne :** * Création d'une matrice de transition stochastique $P$ intégrant un taux d'erreur $\epsilon$.
  * Calcul de l'évolution de la probabilité d'atteindre le but via les équations de Chapman-Kolmogorov ($\pi^{(n)} = \pi^{(0)}P^n$).
* **Simulation Monte-Carlo :** Exécution de 1000 trajectoires aléatoires pour valider empiriquement le modèle théorique sous différents niveaux de perturbation stochastique.

## 📊 Résultats clés

* **Efficacité des heuristiques :** L'algorithme A* réduit considérablement l'espace d'exploration par rapport à UCS, tout en garantissant l'optimalité sur des grilles complexes.
* **Impact de l'incertitude :** Les simulations démontrent qu'un plan purement déterministe est fragile. Par exemple, pour un taux d'erreur de 15% ($\epsilon = 0.15$), l'agent a moins de 50% de chances d'atteindre la cible dans le temps optimal prévu par A*.
* **Monte-Carlo :** La probabilité de succès s'effondre drastiquement (tombant à 26.9%) lorsque le taux d'erreur $\epsilon$ atteint 0.3.

## 🛠️ Technologies utilisées

* **Langage :** Python 3.x
* **Bibliothèques (selon votre code) :** `numpy` (calcul matriciel), `matplotlib` / `seaborn` (génération des graphiques et de la heatmap).

## 🚀 Comment exécuter le projet

1. Clonez ce dépôt ou extrayez le dossier du projet.
2. Assurez-vous d'avoir Python installé ainsi que les dépendances requises :
   ```bash
   pip install numpy matplotlib seaborn
