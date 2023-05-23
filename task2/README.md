# Task2: Implementação de Um Sistema de Recuperação Em Memória Segundo o Modelo Vetorial

### Algumas observações sobre o código

1. O código foi implementado em python e pode ser encontrado na pasta "task2\src".

2. O Notebook execute_flow.ipynb coordena a execução das classes implementadas e o Notebook avalia.ipynb implementa os algoritmos de avaliação do mecanismo.

2. Os arquivos de entrada utilizados para a execução do código estão na pasta "task2\inputs".

3. Os arquivos retornados pela execução dos métodos estão na pasta "task2\results"

4. O modelo foi implementado em formato matricial e salvo como um arquivo csv, em que as colunas são as palavras e as linhas (índices) são os documentos.

5. O Código foi deselvolvido em cima de um ambiente virtual python, as bibliotecas utilizadas podem ser encontradas no arquivo "../requirements.txt"

6. A avaliação dos resultados está na pasta "task2\avalia", as informações estão organizadas no arquivo RELATÓRIO.MD

### Implementações

- Processador de Consultas: "src/processador.py"
- Gerador Lista Invertida: "src/gerador.py"
- Indexador: "src/indexador.py"
- Buscador: "src/buscador.py"
- Coordenação: "src/execute_flow.py"
- Avaliação: "src/avalia.py"