### Foi coletado os dados do censo 2022 do IBGE.
### Foi ordenado em ordem decrescente
### Foi excluir o primeiro que era "Rural", mesmo contendo sozinho 58.772
### Com os bairros, foram coletados as coordenadas centrais a partir da API do google mapas
### Notado que no IBGE não constam bairros como Chapadinha, Pedra miuda, angelica e alguns outros que ficaram como zona rural
### Verificado visualmente os bairros comparado com o zoneamento da semplan
### Usado um método de Cluster do Scipy para agrupar os pontos próximos e o ponto resultante foi definido por centro de gravidade ponderado pela população
### Esse agrupamento fez com que ficassem 20 pontos para serem usados no calculo
### A partir disso foi plotado um novo mapa com pontos
### Mais outro mapa, que o tamanho do ponto é proporcional à quantidade da população do local
### Coleta dos endereços de coleta atuais fixos e o moveis
### Plotagem e conferencia visual dos pontos de coleta
# TODO: Otimizar os pontos itinerantes