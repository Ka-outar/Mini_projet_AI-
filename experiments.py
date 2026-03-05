from grid import Grid
from search_algorithms import search
from markov_chain import *
from simulation import *
from visualization import plot_grid

import numpy as np
import matplotlib.pyplot as plt
import time  # pour mesurer le temps

# =============================================================================
#   DÉFINITION DES TROIS GRILLES POUR LA COMPARAISON (E.1 du sujet)
# =============================================================================

# Facile : presque aucun obstacle
grid_easy = [
    ["S", ".", ".", "."],
    [".", ".", ".", "."],
    [".", ".", ".", "."],
    [".", ".", ".", "G"]
]

# Moyenne : ta grille de référence
grid_medium = [
    ["S", ".", ".", "."],
    [".", "#", "#", "."],
    [".", ".", ".", "."],
    [".", "#", ".", "G"]
]

# Difficile : Un vrai labyrinthe (10x10) pour voir la puissance de A*
grid_hard = [
    ["S", ".", ".", ".", "#", ".", ".", ".", ".", "."],
    [".", "#", "#", ".", "#", ".", "#", "#", "#", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "#", "."],
    ["#", "#", "#", "#", "#", "#", "#", ".", "#", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", "#", "#", "#", "#", "#", "#", "#", "#", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "#", "."],
    [".", "#", "#", "#", "#", "#", "#", ".", "#", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "#", "."],
    [".", "#", "#", "#", "#", "#", "#", ".", ".", "G"]
]

# Dictionnaire pour boucler facilement
grids = {
    "Facile":   (grid_easy,   (0,0), (3,3)),
    "Moyenne":  (grid_medium, (0,0), (3,3)),
    "Difficile":(grid_hard,   (0,0), (9,9)) 
}


# =============================================================================
#   E.1 — COMPARAISON UCS / GREEDY / A* SUR 3 NIVEAUX DE DIFFICULTÉ
# =============================================================================

algorithms_comparison = ["ucs", "greedy", "astar"]
results_difficulty = {diff: {} for diff in grids}

print("\n" + "="*80)
print("COMPARAISON UCS / GREEDY / A* SUR 3 NIVEAUX DE DIFFICULTÉ")
print("="*80)

for diff_name, (gmap, st, gl) in grids.items():
    print(f"\n--- {diff_name.upper()} ---")
    grid_temp = Grid(gmap, st, gl)
    
    for algo in algorithms_comparison:
        # On moyenne sur 100 exécutions pour éviter le temps de "chauffe" de Python
        nb_runs = 100
        t_start = time.perf_counter()
        
        for _ in range(nb_runs):
            path, explored = search(grid_temp, st, gl, mode=algo)
            
        t_end = time.perf_counter()
        
        length = len(path) - 1 if path else "—"
        duration = ((t_end - t_start) * 1000) / nb_runs # Temps moyen en ms
        
        results_difficulty[diff_name][algo] = {
            "explored": explored,
            "length": length,
            "time": duration
        }
        
        print(f"  {algo:8} → nœuds: {explored:5d}   | longueur: {length:>3}   | temps: {duration:.4f}ms")
    
    print("-"*80)


# Graphique groupé 1 : VITESSE (Temps d'exécution par difficulté)
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(algorithms_comparison))
width = 0.25

for i, diff in enumerate(grids.keys()):
    values = [results_difficulty[diff][algo]["time"] for algo in algorithms_comparison]
    ax.bar(x + i*width, values, width, label=diff)

ax.set_xlabel('Algorithme')
ax.set_ylabel("Temps d'exécution (millisecondes)")
ax.set_title("Vitesse d'exécution — UCS vs Greedy vs A* sur 3 difficultés")
ax.set_xticks(x + width)
ax.set_xticklabels(algorithms_comparison)
ax.legend(title="Difficulté")
plt.tight_layout()
plt.show()


# =============================================================================
#   PHASE 2 : COMPARAISON UCS / GREEDY / A* / WEIGHTED SUR LA GRILLE MOYENNE
# =============================================================================

print("\n" + "="*80)
print("COMPARAISON UCS / GREEDY / A* / WEIGHTED A* SUR LA GRILLE MOYENNE")
print("="*80)

grid = Grid(grid_medium, (0,0), (3,3))
algorithms = ["ucs", "greedy", "astar", "weighted"]
explored_counts = []
path_lengths = []
last_path = None

for algo in algorithms:
    if algo == "weighted":
        path, explored = search(grid, (0,0), (3,3), mode="weighted", weight=2)
    else:
        path, explored = search(grid, (0,0), (3,3), mode=algo)
    
    explored_counts.append(explored)
    path_lengths.append(len(path) - 1 if path else 0)
    last_path = path
    
    print(f"\n{algo.upper():8}")
    print("  path:   ", path)
    print("  nodes:  ", explored)


# Tableau récapitulatif
print("\n" + "-"*70)
print("RÉCAPITULATIF GRILLE MOYENNE")
print("-"*70)
print(f"{'Algorithme':12} | {'Nœuds développés':>16} | {'Longueur chemin':>14}")
print("-"*70)
for algo, exp, lng in zip(algorithms, explored_counts, path_lengths):
    lng_str = str(lng) if lng > 0 else "—"
    print(f"{algo:12} | {exp:>16} | {lng_str:>14}")
print("="*70)


# Graphique 2 : EFFICACITÉ (Longueur du chemin sur la grille moyenne)
fig, ax = plt.subplots(figsize=(9, 5.5))
x = np.arange(len(algorithms))

bars = ax.bar(x, path_lengths, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])

ax.set_xlabel('Algorithme')
ax.set_ylabel('Longueur du chemin')
ax.set_title("Efficacité sur la grille moyenne\n(Plus le chemin est court, plus l'algorithme est optimal)")
ax.set_xticks(x)
ax.set_xticklabels(algorithms)

for bar in bars:
    height = bar.get_height()
    if height > 0:
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.1,
                f'L={int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.show()


# Affichage du chemin trouvé (dernier algo)
plot_grid(grid_medium, last_path)


# =============================================================================
#   CONSTRUCTION POLITIQUE et LISTE DES ÉTATS (sur la grille moyenne)
# =============================================================================

policy = {}
for i in range(len(last_path)-1):
    policy[last_path[i]] = last_path[i+1]

states = []
for i in range(grid.rows):
    for j in range(grid.cols):
        if grid_medium[i][j] != "#":
            states.append((i, j))


# =============================================================================
#   PHASE 3-4 : ANALYSE MARKOV
# =============================================================================

print("\n=== ANALYSE MARKOV (politique déterministe + incertitude ε) ===")

epsilon_analysis = 0.15
P = build_transition_matrix(states, policy, epsilon_analysis)

row_sums = P.sum(axis=1)
print(f"Matrice P construite  ({P.shape[0]} × {P.shape[1]})")
print(f"Somme des lignes → min = {row_sums.min():.4f}   max = {row_sums.max():.4f}")
print(f"Est stochastique ?   → {np.allclose(row_sums, 1.0, atol=1e-10)}")


pi0 = np.zeros(len(states))
start_idx = states.index((0,0))
pi0[start_idx] = 1.0
goal_idx = states.index((3,3))

print(f"\nÉvolution P(être dans GOAL) pour ε = {epsilon_analysis}")
print(" n     |   Probabilité    |  commentaire")
for n in range(0, 16):
    pi_n = compute_pi_n(pi0, P, n)
    p_goal = pi_n[goal_idx]
    comment = "← longueur chemin optimal" if n == 6 else "← convergence notable" if n == 10 else ""
    print(f"{n:2d}    |     {p_goal:>6.3%}      |  {comment}")


print("\nProbabilité cumulée d'avoir atteint GOAL au plus tard à t = n :")
cumul = 0.0
for n in range(1, 21):
    pi_n = compute_pi_n(pi0, P, n)
    p_new = pi_n[goal_idx] - cumul
    cumul += p_new
    print(f"  ≤ {n:2d}    →   {cumul:>6.2%}")


# =============================================================================
#   VISUALISATION DE LA MATRICE DE TRANSITION (HEATMAP)
# =============================================================================

print("\nAffichage de la matrice de transition P...")

plt.figure(figsize=(10, 8))
# cmap='viridis' donne de belles couleurs modernes (violet au jaune)
im = plt.imshow(P, cmap='viridis', interpolation='nearest') 

plt.colorbar(im, label='Probabilité de transition')
plt.title(f"Visualisation de la Matrice de Transition P (ε = {epsilon_analysis})")
plt.xlabel("État d'arrivée (Index)")
plt.ylabel("État de départ (Index)")

plt.tight_layout()
plt.show()


# =============================================================================
#   PHASE 5 : SIMULATION MONTE-CARLO
# =============================================================================

print("\n" + "="*70)
print("SIMULATION MONTE-CARLO (1000 trajectoires par valeur de ε)")
print("="*70)

epsilons = [0.0, 0.1, 0.2, 0.3]
results = []
avg_times = []

for eps in epsilons:
    prob, avg_time = monte_carlo((0,0), (3,3), policy, eps, N=1000)
    results.append(prob)
    avg_times.append(avg_time)
    
    print(f"\nε = {eps}")
    print(f"  Probabilité de succès : {prob:.4f}  ({prob*100:5.1f} %)")
    if avg_time:
        print(f"  Temps moyen (si succès) : {avg_time:.2f} étapes")
    else:
        print("  Temps moyen : —")


# Graphique Monte-Carlo
plt.figure(figsize=(8, 5))
plt.plot(epsilons, results, marker='o', linestyle='-', color='darkblue')
plt.xlabel("ε (niveau d'incertitude)")
plt.ylabel("Probabilité de succès")
plt.title("Impact de l'incertitude sur la réussite (Monte-Carlo)")
plt.grid(True, alpha=0.3)
plt.ylim(0, 1.05)
plt.show()