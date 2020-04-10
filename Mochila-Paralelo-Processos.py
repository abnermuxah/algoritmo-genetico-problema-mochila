#Bibliotecas 
from random import randint
from multiprocessing import Process, Queue
# ----- Funções --------
# 1 - Gerar a população Inicial - (Serão eliminados os cromossomos que excedam a capacidade máxima)
def peso_cromo(cromossomo, peso): # retorna o peso toal que que o cromossomo pode levar
	sum_peso = 0
	qtd_itens = len(peso)
	for i in range(qtd_itens):
	    if cromossomo[i]==1:
	        sum_peso += peso[i]   		
	return sum_peso
def valor_cromo(cromossomo, valor): # retorna o valor total que o cromossomo pode levar
	sum_valor = 0
	qtd_itens = len(peso)
	sum_valor = 0
	for i in range(qtd_itens):
	    if cromossomo[i]==1:
	        sum_valor += valor[i]   		
	return sum_valor
def gerar_pop2(tam_pop, qtd_itens): # gerar pop_inicial apenas com numeros aleatorios
    populacao = [[randint(0,1) for n in range(qtd_itens)] for m in range(tam_pop)]
    return populacao
def gerar_pop(tam_pop, peso, cap_max): # retorna uma lsita da população inicial
	populacao = []
	cromossomo = []
	qtd_itens = len(peso)
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
			populacao.append(cromossomo)
		else:
			cromossomo = [randint(0,1) for n in range(qtd_itens)]
			cap = peso_cromo(cromossomo, peso)
			n = 0 # variavel que salva o indice da primeira posicao da lista
			while (cap > cap_max):
				cromossomo.pop(n)
				cromossomo.insert(n, 0)
				cap = peso_cromo(cromossomo, peso)
				n += 1
			populacao.append(cromossomo)
	return populacao
# 2 - Avaliar a população gerada
def aval_pop(populacao, peso, valor): # retorna uma lista de listas com [peso, valor, indice] que cada individuo consegue carregar
	analise = []
	tam_pop = len(populacao)
	qtd_itens = len(peso)
	sum_valor = sum_peso = 0
	for i in range(tam_pop):
	   	for j in range(qtd_itens):
	           if populacao[i][j]==1:
	           	sum_peso += peso[j]
	           	sum_valor += valor[j]   		
	   	analise.append([])
	   	analise[i].append(sum_peso)
	   	analise[i].append(sum_valor)
	   	analise[i].append(i)
	   	sum_valor = sum_peso = 0
	analise.sort(reverse=True)
	return analise
def melhor_individuo(populacao, peso, valor, id1): 
	analise = []
	qtd_itens = len(peso)
	sum_valor = sum_peso = 0
	#for id1 in range(1):
	for j in range(qtd_itens):
	           if populacao[id1][j]==1:
	           	sum_peso += peso[j]
	           	sum_valor += valor[j]   		
	analise.append(sum_peso)
	analise.append(sum_valor)
	return analise
def selec_melhor(analise, populacao, cap_max): # retorna a lista do melhor cromossomo [peso, valor, indice, cromossomo], eu so analizaria 50% da populacao
	tam_pop = len(analise)
	maior = id1 = -1
	lista = []
	for i in range(int(tam_pop)):
		if (analise[i][0] <= cap_max): # analisa o peso dos indices que estao no intervalo definido max
			if (analise[i][1]>=maior):   # seleciona o item que tiver maior valor entre os itens avaliados anteriormente
				maior = analise[i][1]
				id1 = i
	if maior > -1:
		lista.append(analise[id1][0])
		lista.append(analise[id1][1])
		lista.append(id1)
		lista.append(populacao[id1])
		return lista
	else:
		return lista.append(None)
# 3 ------ Crossover + Mutação ------
def mutacao(cromossomo, tx_mut): # valor da tx_mutação em % com relação ao tamanho do cromossomo 
	qtd_itens = (len(cromossomo)-1)
	corte_ini = randint(0,qtd_itens)
	tx_mut = round(float((tx_mut/100)*len(cromossomo)))
	corte_fim = corte_ini + tx_mut
	while (corte_ini < corte_fim):
		# se o corte_final passar do intervalo a mutação é truncada ate a qtd_itens  
		if corte_fim > qtd_itens:
			corte_fim = qtd_itens 
		if cromossomo[corte_ini] == 1:
			cromossomo.pop(corte_ini)
			cromossomo.insert(corte_ini, 0)
		elif cromossomo[corte_ini] == 0:
			cromossomo.pop(corte_ini)
			cromossomo.insert(corte_ini, 1)
		corte_ini += 1
	return cromossomo
def crossover(populacao, analise, tx_mutacao, cap_max, ini, fim, que): # retorna uma nova geração crossover simples + mutação
    nova_geracao = []
    tam_pop = fim
    qtd_itens = len(populacao[0])
    corte = randint(2,qtd_itens-2)
    while(ini < (tam_pop - 1)):
    	if analise[ini][0] <= cap_max:
    		filho1 = populacao[ini]
    		nova_geracao.append(filho1)
    	else:
    		filho1 = populacao[analise[ini][2]][:corte] + populacao[analise[ini+1][2]][corte:]
    		filho1 = mutacao(filho1, tx_mutacao)
    		nova_geracao.append(filho1)

    	if analise[ini+1][0] <= cap_max:
    		filho2 = populacao[ini+1]
    		nova_geracao.append(filho2)
    	else:
    		filho2 = populacao[analise[ini+1][2]][:corte] + populacao[analise[ini][2]][corte:]
    		filho2 = mutacao(filho2, tx_mutacao)
    		nova_geracao.append(filho2)
    	ini=ini+2
    	if ((ini+1)==(tam_pop)):
        	filho1 = populacao[analise[ini][2]]
        	filho1 = mutacao(filho1, tx_mutacao)
        	nova_geracao.append(filho1)
		
    del populacao
    populacao = nova_geracao
    que.put(populacao)
    #return populacao

# ---- FUNÇÃO PRINCIPAL --------
if __name__ == '__main__':
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
	# ENTRADAS:
	tam_pop = 2000 # pode ser alterada pelo usuário
	tx_mutacao = 5  # pode ser alterada pelo usuario
	max_geracao = 50 # Pode ser alterada pelo usuario
	processos = 6 # MAXIMO 6
	qtd_itens = len(peso)
	cap_max = int(instancias[1])
	geracao_atual = 1
	populacao = []
	melhor_atual = []
	melhor_individuo = [0,0,0,0] # melhor individuo
	analise = []
	peso_atual = 0
	## codigo principal
	# Gerar a populacao Inicial
	populacao = gerar_pop(tam_pop, peso, cap_max)
	# enqunato criterio parada = False
	#print(populacao)
	while (geracao_atual != max_geracao+1):
		analise = aval_pop(populacao, peso, valor)
		#print(analise)
		#print(populacao)
		melhor_atual.clear()
		melhor_atual = selec_melhor(analise, populacao, cap_max)
		if (melhor_atual==None):
			print("\n Nesta geracao nao foi encontrado algum individuo apto \n")
			break
		print("Melhor individuo da geracao:", geracao_atual )
		print("PESO:", melhor_atual[0],"\nVALOR:",melhor_atual[1])
		print("indice:", melhor_atual[2])
		print("Cromossomo:",melhor_atual[3],"\n")
		geracao_atual = geracao_atual + 1
		if (geracao_atual != max_geracao): ## eh aqui que tem que paralelizar
		# defini 4 processos
			if (processos == 1):
				itens = tam_pop/processos
				i0=i1=0
				x1=0
				i1=int(i0+itens)
				while(i1<=(tam_pop-1)):
					i1=i1+1
				# Processo 1
				queue1 = Queue()
				p1 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i0,i1, queue1))
				p1.start()
				x1 = queue1.get()
				p1.join()
				nova_geracao = x1
			elif (processos == 2):
				itens = tam_pop/processos
				x1=x2=0
				i0=i1=i2=0
				i1=int(i0+itens)
				i2=int(i1+itens)
				while(i2<=(tam_pop-1)):
					i2=i2+1
				# Processo 1
				queue1 = Queue()
				p1 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i0,i1, queue1))
				p1.start()
				x1 = queue1.get()
				p1.join()
				# Processo 2
				p2 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i1,i2, queue1))
				p2.start()
				x2 = queue1.get()
				p2.join()
				nova_geracao = (x1 + x2)
			elif (processos==3):
				itens = tam_pop/processos
				x1=x2=x3=0
				i0=i1=i2=i3=0
				i1=int(i0+itens)
				i2=int(i1+itens)
				i3=int(i2+itens)
				while(i3<=(tam_pop-1)):
					i3=i3+1
				# Processo 1
				queue1 = Queue()
				p1 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i0,i1, queue1))
				p1.start()
				x1 = queue1.get()
				p1.join()
				# Processo 2
				p2 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i1,i2, queue1))
				p2.start()
				x2 = queue1.get()
				p2.join()
				# Processo 3
				p3 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i2,i3, queue1))
				p3.start()
				x3 = queue1.get()
				p3.join()
				nova_geracao = (x1 + x2 + x3)
			elif (processos==4):
				itens = tam_pop/processos
				x1=x2=x3=x4=0
				i0=i1=i2=i3=i4=0
				i1=int(i0+itens)
				i2=int(i1+itens)
				i3=int(i2+itens)
				i4=int(i3+itens)
				while(i4<=(tam_pop-1)):
					i4=i4+1
				# Processo 1
				queue1 = Queue()
				p1 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i0,i1, queue1))
				p1.start()
				x1 = queue1.get()
				p1.join()
				# Processo 2
				p2 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i1,i2, queue1))
				p2.start()
				x2 = queue1.get()
				p2.join()
				# Processo 3
				p3 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i2,i3, queue1))
				p3.start()
				x3 = queue1.get()
				p3.join()
				# Processo 4
				p4 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i3,i4, queue1))
				p4.start()
				x4 = queue1.get()
				p4.join()
				nova_geracao = (x1 + x2 + x3 + x4)
			elif (processos==5):
				itens = tam_pop/processos
				x1=x2=x3=x4=x5=0
				i0=i1=i2=i3=i4=i5=0
				i1=int(i0+itens)
				i2=int(i1+itens)
				i3=int(i2+itens)
				i4=int(i3+itens)
				i5=int(i4+itens)
				while(i5<=(tam_pop-1)):
					i5=i5+1
				# Processo 1
				queue1 = Queue()
				p1 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i0,i1, queue1))
				p1.start()
				x1 = queue1.get()
				p1.join()
				# Processo 2
				p2 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i1,i2, queue1))
				p2.start()
				x2 = queue1.get()
				p2.join()
				# Processo 3
				p3 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i2,i3, queue1))
				p3.start()
				x3 = queue1.get()
				p3.join()
				# Processo 4
				p4 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i3,i4, queue1))
				p4.start()
				x4 = queue1.get()
				p4.join()
				# Processo 5
				p5 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i4,i5, queue1))
				p5.start()
				x5 = queue1.get()
				p5.join()
				nova_geracao = (x1 + x2 + x3 + x4 + x5)
			elif (processos == 6):
				itens = tam_pop/processos
				x1=x2=x3=x4=x5=x6=0
				i0=i1=i2=i3=i4=i5=i6=0
				i1=int(i0+itens)
				i2=int(i1+itens)
				i3=int(i2+itens)
				i4=int(i3+itens)
				i5=int(i4+itens)
				i6=int(i5+itens)
				while(i6<=(tam_pop-1)):
					i6=i6+1
				# Processo 1
				queue1 = Queue()
				p1 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i0,i1, queue1))
				p1.start()
				x1 = queue1.get()
				p1.join()
				# Processo 2
				p2 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i1,i2, queue1))
				p2.start()
				x2 = queue1.get()
				p2.join()
				# Processo 3
				p3 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i2,i3, queue1))
				p3.start()
				x3 = queue1.get()
				p3.join()
				# Processo 4
				p4 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i3,i4, queue1))
				p4.start()
				x4 = queue1.get()
				p4.join()
				# Processo 5
				p5 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i4,i5, queue1))
				p5.start()
				x5 = queue1.get()
				p5.join()
				nova_geracao = (x1 + x2 + x3 + x4 + x5)
				# Processo 6
				p6 = Process(target=crossover, args=(populacao, analise, tx_mutacao, cap_max, i5,i6, queue1))
				p6.start()
				x6 = queue1.get()
				p6.join()
				nova_geracao = (x1 + x2 + x3 + x4 + x5 + x6)
			else:
				print("Quantidade de processos invalidos, tente valores de 1 a 6")
				break
			del populacao
			populacao = nova_geracao