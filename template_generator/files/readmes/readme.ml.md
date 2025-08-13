# Projeto de Análise de Dados

Este projeto utiliza o JupyterLab para análise de dados e visualização com a biblioteca Seaborn.

## Como Iniciar

### Ativando o Ambiente Virtual

Antes de iniciar o JupyterLab, é necessário ativar o ambiente virtual onde as dependências do projeto estão instaladas. Siga as instruções abaixo para ativar o ambiente:

1. **Windows:**

Abra o Prompt de Comando e execute:
```bash
.\venv\Scripts\activate
```

2. **macOS/Linux:**

Abra o Terminal e execute:
```bash
source venv/bin/activate
```

### Iniciando o JupyterLab

Após ativar o ambiente virtual, inicie o JupyterLab com o seguinte comando:

```bash
jupyter lab
```

O JupyterLab será aberto no seu navegador padrão.

## Criando um Gráfico Simples com Seaborn

Abaixo estão as instruções para gerar um gráfico simples utilizando a biblioteca Seaborn:

1. **Crie um novo notebook** no JupyterLab.

2. **Importe as bibliotecas necessárias** no seu notebook:

```Python
import seaborn as sns
import matplotlib.pyplot as plt
```

3. **Carregue um conjunto de dados de exemplo** (por exemplo, o conjunto de dados `tips`):

```Python
tips = sns.load_dataset("tips")
```

4. **Gere um gráfico de dispersão** (scatter plot) simples:

```Python
sns.scatterplot(data=tips, x="total_bill", y="tip")
plt.show()
```

Este código irá criar e exibir um gráfico de dispersão que mostra a relação entre o valor total da conta (`total_bill`) e a gorjeta (`tip`).
