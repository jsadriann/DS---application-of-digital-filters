# Filtro Rejeita-Banda com Butterworth

## Descrição do Projeto

Este projeto tem como objetivo aplicar um **filtro rejeita-banda Butterworth** em um sinal de áudio com ruído. O filtro rejeita uma faixa de frequências específica para remover ruídos indesejados, preservando o restante do sinal. O projeto calcula a **Relação Sinal-Ruído (SNR)** antes e depois da aplicação do filtro, e exibe os resultados com gráficos que mostram o espectro de frequências e as formas de onda do áudio.

## Estrutura do Projeto

- `final.py`: Script principal que realiza o carregamento do sinal, aplica o filtro e gera os gráficos.
- `audio_ruido.wav`: Arquivo de áudio com ruído que será processado pelo filtro.
- `audio_bandstop_filtered.wav`: Arquivo de áudio filtrado gerado após o processamento.
- `requeriments.txt`: Lista de dependências para o projeto.

## Funcionalidades

1. **Carregamento de áudio**: O sinal de áudio com ruído é carregado a partir de um arquivo `.wav`.
2. **Aplicação de Filtro Rejeita-Banda**: Um filtro Butterworth rejeita uma faixa de frequências definida (2200 Hz a 10000 Hz), removendo o ruído do áudio.
3. **Cálculo da Relação Sinal-Ruído (SNR)**: O SNR é calculado antes e depois da filtragem para avaliar a melhoria na qualidade do sinal.
4. **Gráficos**: São gerados gráficos do espectro de frequências e da forma de onda para comparar o áudio com ruído e o áudio filtrado.

## Como Executar o Projeto

### Pré-requisitos

Este projeto utiliza Python e algumas bibliotecas adicionais. Para rodar o código, é necessário instalar as dependências listadas no arquivo `requeriments.txt`. Use o comando abaixo para instalar:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requeriments.txt

