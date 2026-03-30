import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os
from matplotlib.ticker import FuncFormatter


CACHE_DIR = "dados_cache"
results_path = os.path.join(CACHE_DIR, "resultados.pkl")

if not os.path.exists(results_path):
    raise FileNotFoundError(f"Arquivo {results_path} não encontrado!")


# Carregar resultados
print("Carregando resultados...")
with open(results_path, "rb") as f:
    data = pickle.load(f)

ks = sorted(data["simulations"].keys())
deterministic_labels = ["Degree", "Closeness", "Betweenness"]
random_label = ["Random10","Random20","Random100"]


# extrair dados para boxplot
def extract_boxplot_data(metric):
    rows = []

    for k in ks:

        # determinísticos — 1 valor por k
        for label in deterministic_labels:
            rows.append({
                "strategy": label,
                "value": data["simulations"][k][label.lower()][metric]
            })

        # random10
        for res in data["simulations"][k]["random_10"]:
            rows.append({"strategy": "Random10", "value": res[metric]})

        # random20
        for res in data["simulations"][k]["random_20"]:
            rows.append({"strategy": "Random20", "value": res[metric]})

        # random100
        for res in data["simulations"][k]["random_100"]:
            rows.append({"strategy": "Random100", "value": res[metric]})

    return pd.DataFrame(rows)



df_components = extract_boxplot_data("n_components")
df_disconnected = extract_boxplot_data("disconnected_pairs")
df_largest_cc = extract_boxplot_data("largest_cc_size")


# Plot

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("Resilience Metrics Distribution Under Diferent Removal Strategies", fontsize=14)




# 1. Número de Componentes
df_components.boxplot(by="strategy", column="value",ax=axes[0,0])
axes[0,0].set_title("Strongly Connected Components(SCCs)")
axes[0,0].set_ylabel("Number of SCCs")         
axes[0,0].set_xlabel("")
axes[0,0].grid(True)

# 2. Pares Desconectados
df_disconnected.boxplot(by="strategy", column="value",ax=axes[0,1])
axes[0,1].set_title("Disconnected Pairs")
axes[0,1].set_ylabel("Number of Disconnected Pairs")         
axes[0,1].set_xlabel("")
axes[0,1].grid(True)

axes[0,1].yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))

# 3. Maior Componente Fortemente Conectada
df_largest_cc.boxplot(by="strategy", column="value",ax=axes[1,0])
axes[1,0].set_title("Size of Largest Strongly Connected Component(LSCC)")
axes[1,0].set_ylabel("Number of vertices in the LSCC")            
axes[1,0].set_xlabel("")
axes[1,0].grid(True)

# Limpar o quarto subplot
axes[1,1].axis("off")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
