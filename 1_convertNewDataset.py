#pip install pandas scikit-image
import pandas as pd
from skimage.color import rgb2lab

# Arquivos
entrada = "DADOS_COLETADO.xlsx"
saida = "DADOS_COLETADO_COM_MEDIAS_LAB.xlsx"

# Ler Excel
df = pd.read_excel(entrada)

# ============================================================
# 1. MÉDIA RGB
# ============================================================

df["R_AVG"] = df[["R1", "R2", "R3"]].mean(axis=1)
df["G_AVG"] = df[["G1", "G2", "G3"]].mean(axis=1)
df["B_AVG"] = df[["B1", "B2", "B3"]].mean(axis=1)


# ============================================================
# 2. MÉDIA LAB MEDIDO
# ============================================================

df["L_LAB_AVG"] = df[["LAB_L1", "LAB_L2", "LAB_L3"]].mean(axis=1)
df["A_LAB_AVG"] = df[["LAB_A1", "LAB_A2", "LAB_A3"]].mean(axis=1)
df["B_LAB_AVG"] = df[["LAB_B1", "LAB_B2", "LAB_B3"]].mean(axis=1)


# ============================================================
# 3. CONVERTER RGB MÉDIO PARA LAB
# ============================================================

# RGB precisa ser normalizado de 0-255 para 0-1
rgb_avg = df[
    ["R_AVG", "G_AVG", "B_AVG"]
].to_numpy() / 255.0

# Conversão RGB → CIELAB
lab = rgb2lab(rgb_avg, illuminant="D65", observer="2")
# Criar novas colunas
df["L_RGB_TO_LAB"] = lab[:, 0]
df["A_RGB_TO_LAB"] = lab[:, 1]
df["B_RGB_TO_LAB"] = lab[:, 2]


# ============================================================
# 4. ARREDONDAR
# ============================================================

new_columns = [
    "R_AVG",
    "G_AVG",
    "B_AVG",
    "L_LAB_AVG",
    "A_LAB_AVG",
    "B_LAB_AVG",
    "L_RGB_TO_LAB",
    "A_RGB_TO_LAB",
    "B_RGB_TO_LAB"
]


new_dataset = [
    "L_LAB_AVG",
    "A_LAB_AVG",
    "B_LAB_AVG",
    "L_RGB_TO_LAB",
    "A_RGB_TO_LAB",
    "B_RGB_TO_LAB"
]

df[new_columns] = df[new_columns].round(4)


df[new_dataset] = df[new_dataset].round(4)

# ============================================================
# 5. SALVAR
# ============================================================

#df.to_csv(saida, index=False)

df[new_dataset].to_csv('dataset.csv', index=False)

print("Processamento concluído!")
print("Arquivo:",'dataset.csv')