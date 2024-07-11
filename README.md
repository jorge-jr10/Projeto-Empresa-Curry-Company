# Problema de negócio

A Cury Company é uma empresa de tecnologia que criou um aplicativo que conecta restaurantes, entregadores e pessoas. Através desse aplicativo, é possível realizar o pedido de uma refeição em qualquer restaurante cadastrado e recebê-lo no conforto da sua casa por um entregador também cadastrado no aplicativo da Cury Company. 

A empresa gera muitos dados sobre entregas, tipos de pedidos, condições climáticas e avaliação dos entregadores. Apesar do crescimento da empresa, o CEO não tem visibilidade completa sobre os KPIs de crescimento da companhia.

A necessidade da empresa é ter os principais KPIs estratégicos organizados em uma única ferramenta, para que o CEO possa consultar e conseguir tomar decisões simples, porém importantes.

A Cury Company possui um modelo de negócio Marketplace, que faz o intermédio do negócio entre três clientes principais: Restaurantes, entregadores e pessoas compradoras. Nesse caso, o CEO gostaria de ver o crescimento e evolução da companhia. O objetivo desse projeto é criar um conjunto de gráficos e tabelas que exibam essas métricas.

# Premissas assumidas para a análise
   
  1. A análise foi realizada com dados entre 11/02/2022 e 06/04/2022.
  2. Marketplace foi o modelo de negócio assumido.
  3. As 3 principais visões do negócio foram: Visão transação de pedidos, visão restaurante e visão entregadores.

# Estratégia da solução
   
O painel estratégico foi desenvolvido utilizando as métricas que refletem as 3 principais visões do modelo de negócio da empresa:
  1. Visão do crescimento da empresa
  2. Visão do crescimento dos restaurantes
  3. Visão do crescimento dos entregadores
   
Cada visão é representada pelo seguinte conjunto de métricas:

## Visão do crescimento da empresa
   1. Quantidade de pedidos por dia.
   2. Quantidade de pedidos por condições de tráfego
   3. Quantidade de pedidos por cidade e condições de tráfego
   4. Pedidos por semana.
   5. Pedidos por entregador (Semana)
   6. Demonstração geográfica das localidades de entrega

## Visão do crescimento dos restaurantes
   1. Distância média percorrida
   2. Tempo médio entrega com e sem Festival
   3. Desvio padrão das entregas com e sem Festival
   4. Tempo médio de entrega por cidade com variabilidade
   5. Tempo médio de entrega e desvio padrão por cidade e tipo de pedido
   6. Variação de distância Restaurante x Entrega entre as cidades
   7. Média e STD do tempo de entrega por cidade e densidade de trânsito

## Visão do crescimento dos entregadores
   1. Maior e menor idade dos entregadores
   2. Melhor e pior condição do veículo
   3. Quantidade de entregadores únicos
   4. Média de avaliações por entregador
   5. Avaliação média e desvio padrão por densidade de trânsito
   6. Avaliação média e desvio padrão por clima
   7. Entregadores mais rápidos e mais lentos por cidade

# Top 3 Insights de dados
  1. A sazonalidade da quantidade de pedidos é diária. Há uma variação de aproximadamente 10% do número de pedidos em dia sequenciais.
  2. As cidades do tipo Semi-Urban não possuem condições baixas de trânsito.
  3. As maiores variações no tempo de entrega, acontecem durante o clima ensolarado.

# O produto final do projeto
Painel online, hospedado em cloud e disponível para acesso em qualquer dispositivo conectado à internet.
O painel pode ser acessado através desse link: https://jorge-jr-projeto-curry-company.streamlit.app/

# Conclusão
O objetivo desse projeto fora criar uma visualização clara que exiba as métricas da melhor forma possível para o CEO.
Da visão Empresa, podemos concluir que o número de pedidos cresceu entre a semana 06 e a semana 13 do ano de 2022.

# Próximo passos
  1. Reduzir o número de métricas.
  2. Criar novos filtros.
  3. Adicionar novas visões de negócio.
