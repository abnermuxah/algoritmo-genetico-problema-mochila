from random import randint
# funcoes
# obs: vc pode acrescentar o tam_pop na funcao crossover p diminuir esforço computacional (mais tarde não esqueça)
def peso_cromo(cromossomo, peso): # retorna o peso toal que que o cromossomo pode levar
	sum_peso = 0
	qtd_itens = len(peso)
	n = 0
	if (len(cromossomo)!=qtd_itens):
		n = 2
	else:
		n = 0
	for i in range(qtd_itens):
	    if cromossomo[n]==1:
	        sum_peso += peso[i]
	    n = n+1
	return sum_peso
def valor_cromo(cromossomo, valor): # retorna o valor total que o cromossomo pode levar
	sum_valor = 0
	qtd_itens = len(valor)
	if (len(cromossomo)!=qtd_itens):
		n = 2
	else:
		n = 0
	for i in range(qtd_itens):
	    if cromossomo[n]==1:
	        sum_valor += valor[i]
	    n = n+1
	return sum_valor
def gerar_pop(tam_pop, peso, valor, cap_max, qtd_itens): # retorna uma lsita da população inicial
	populacao = []
	cromossomo = []
	for i in range(tam_pop):
		if i%2==0:
			cromossomo = [randint(0,1) for n in range(qtd_itens)]
			cap = peso_cromo(cromossomo, peso)
			n = (qtd_itens-1) # variavel que salva o indice da ultima posicao da lista 
			while (cap > cap_max):
				cromossomo.pop(n)
				cromossomo.insert(n, 0)
				cap = peso_cromo(cromossomo, peso)
				n -= 1
			cap = peso_cromo(cromossomo, peso)
			val = valor_cromo(cromossomo, valor)
			populacao.append(cromossomo)
			populacao[i].insert(0, val)
			populacao[i].insert(1, cap)
		else:
			cromossomo = [randint(0,1) for n in range(qtd_itens)]
			cap = peso_cromo(cromossomo, peso)
			n = 0 # variavel que salva o indice da primeira posicao da lista
			while (cap > cap_max):
				cromossomo.pop(n)
				cromossomo.insert(n, 0)
				cap = peso_cromo(cromossomo, peso)
				n += 1
			val = valor_cromo(cromossomo, valor)
			populacao.append(cromossomo)
			populacao[i].insert(0, val)
			populacao[i].insert(1, cap)
	populacao.sort(reverse=True)
	return populacao
def mutacao(cromossomo, tx_mut): # faz a mutacao do cromossomo com uma porcentagem de tx_mutação 
	qtd_itens = (len(cromossomo)+(-1-2)) # -1 pq começar em zero - 2 pra nao contar valor, peso 
	corte_ini = randint(2,qtd_itens) # senore vai começar 0-valor, 1-peso, 2- em diante (Cromossomo)
	corte_fim = corte_ini + tx_mut  # define quantos indices sofrerao mutacao
	while (corte_ini < corte_fim):
		if corte_fim > qtd_itens:  # se o corte_final passar do intervalo a mutação é truncada ate a qtd_itens  
			corte_fim = qtd_itens 
		if cromossomo[corte_ini] == 1:
			cromossomo.pop(corte_ini)
			cromossomo.insert(corte_ini, 0)
		elif cromossomo[corte_ini] == 0:
			cromossomo.pop(corte_ini)
			cromossomo.insert(corte_ini, 1)
		corte_ini += 1
	corte_ini = 0
	return cromossomo
def crossover(populacao, tx_mutacao, peso, valor, qtd_itens, cap_max): # retorna uma nova geração crossover + mutação
    tam_pop = len(populacao)
    corte = randint(2,tam_pop)
    i=0
    while(i < (tam_pop - 1)):
    	filho1 = populacao[i][2:corte] + populacao[i+1][corte:]
    	filho2 = populacao[i+1][2:corte] + populacao[i][corte:] 

    	filho1 = mutacao(filho1, tx_mutacao)
    	filho2 = mutacao(filho2, tx_mutacao)

    	cap = peso_cromo(filho1, peso)
    	val = valor_cromo(filho1, valor)

    	cap2 = peso_cromo(filho2, peso)
    	val2 = valor_cromo(filho2, valor)
    	if (cap <= cap_max and val > populacao[i][0]):
    		populacao.pop(i)
    		populacao.insert(i, filho1)
    		populacao[i].insert(0, val)
    		populacao[i].insert(0, cap)
    	i +=1
    	if (cap2 <= cap_max and val2 > populacao[i][0]):
    		populacao.pop(i)
    		populacao.insert(i, filho2)
    		populacao[i].insert(0, val2)
    		populacao[i].insert(0, cap2)
    	i+=1
    populacao.sort(reverse=True)
    return populacao


# ---- FUNÇÃO PRINCIPAL --------
# Leitura do arquivo externo (instancias) 
file = open("100.txt")
arquivo = file.read() # ler a cadeia de caracteres do arquivo .txt
instancias = arquivo.split() # separar e agrupar os caracteres
# manipulando a entrada dos dados
qtd_instancias = (len(instancias))
valor = []
peso = []
# salvar as infos do valor na lista valor 
for i in range(2, qtd_instancias, 2):
    valor.append(int(instancias[i]))
# salvar as infors do peso na lista peso
for i in range(3,qtd_instancias,2):
    peso.append(int(instancias[i]))
# Variaveis
tam_pop = 4 # pode ser alterada pelo usuário
tx_mutacao = 2  # pode ser alterada pelo usuario (qtd de itens a sofrer mutação)
cap_max = int(instancias[1])
qtd_itens = int(instancias[0])
max_geracao = 4
geracao_atual = 1
max_geracao = 10
populacao = []

# Inicio do algoritmo
# 1 - Gerar a população inicial
populacao = gerar_pop(tam_pop, peso, valor, cap_max, qtd_itens)
# 2 - Avaliar a população
while (geracao_atual != max_geracao+1):
	print("Geracao: ", geracao_atual)
	populacao = crossover(populacao, tx_mutacao, peso, valor, qtd_itens, cap_max)
	geracao_atual += 1

print("Melhor solucao da geracao ", geracao_atual-1)
print("Valor: ",populacao[0][0]," Peso: ",populacao[0][1])
print("Cromossomo", populacao[0][2:])
