from random import randint
import threading
# Variavel global
n_populacao = []
# funcoes
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
def gerar_pop(tam_pop, peso, valor, cap_max, qtd_itens):
    for i in range(tam_pop):
        cromossomo = []
        cap = val = n = 0
        stop = False
        while(cap_max > cap and stop == False):
            x = randint(0,1)
            if (x==1):
                aux = cap + peso[n]
                if (aux > cap_max):
                    stop = True
                else:
                    cap = cap + peso[n]
                    val = val + valor[n]
                    cromossomo.append(x)
            else:
                cromossomo.append(0)
            n += 1
            if (n==qtd_itens):
                stop = True
        while(not (len(cromossomo)==qtd_itens)):
            cromossomo.append(0)
        cromossomo.insert(0,cap)
        cromossomo.insert(0,val)
        populacao.append(cromossomo)
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
def crossover(populacao, tx_mutacao, peso, valor, cap_max, ini, fim): # retorna uma nova geração crossover + mutação
    tam_pop = fim
    qtd_itens = len(peso)
    corte = randint(2,qtd_itens)
    i=ini
    while(i < (tam_pop - 1)):
    	filho1 = populacao[i][2:corte] + populacao[i+1][corte:]
    	filho2 = populacao[i+1][2:corte] + populacao[i][corte:] 

    	#filho1 = mutacao(filho1, tx_mutacao)
    	filho2 = mutacao(filho2, tx_mutacao)

    	cap = peso_cromo(filho1, peso)
    	cap2 = peso_cromo(filho2, peso)
    	if (cap <= cap_max):
    		val = valor_cromo(filho1, valor)
    		if (val > populacao[i][0]):
	    		populacao.pop(i)
	    		populacao.insert(i, filho1)
	    		populacao[i].insert(0, cap)
	    		populacao[i].insert(0, val)	
    	i +=1
    	if (cap2 <= cap_max):
    		val = valor_cromo(filho2, valor)
    		if (val > populacao[i][0]):
	    		populacao.pop(i)
	    		populacao.insert(i, filho2)
	    		populacao[i].insert(0, cap2)
	    		populacao[i].insert(0, val)
    	i+=1
    # populacao.sort(reverse=True)
    n_populacao = populacao

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
	# Variaveis
	tam_pop = 2000 # pode ser alterada pelo usuário
	max_geracao = 10
	processos = 2
	tx_mutacao = 5  # pode ser alterada pelo usuario (qtd de itens a sofrer mutação)
	cap_max = int(instancias[1])
	qtd_itens = int(instancias[0])
	geracao_atual = 1
	populacao = []

	# Inicio do algoritmo
	# 1 - Gerar a população inicial
	populacao = gerar_pop(tam_pop, peso, valor, cap_max, qtd_itens)
	# 2 - Avaliar a população
	while (geracao_atual != max_geracao+1):
		print("Geracao: ", geracao_atual)
		#definir 6 processos
		if (processos == 1):
				itens = tam_pop/processos
				i0=i1=0
				x1=0
				i1=int(i0+itens)
				while(i1<=(tam_pop-1)):
					i1=i1+1
				# Processo 1
				t1 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i0,i1))
				t1.start()
				t1.join()
				if (t1.is_alive()==False):
					del populacao
					populacao = n_populacao
		elif (processos == 2):
				itens = tam_pop/processos
				i0=i1=i2=0
				i1=int(i0+itens)
				i2=int(i1+itens)
				while(i2<=(tam_pop-1)):
					i2=i2+1
				# Processo 1
				t1 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i0,i1))
				t1.start()
				t1.join()
				# Processo 2
				t2 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i1,i2))
				t2.start()
				t2.join()
				if (t1.is_alive()==t2.is_alive()==False):
					del populacao
					populacao = n_populacao

		elif (processos==3):
				itens = tam_pop/processos
				i0=i1=i2=i3=0
				i1=int(i0+itens)
				i2=int(i1+itens)
				i3=int(i2+itens)
				while(i3<=(tam_pop-1)):
					i3=i3+1
				# Processo 1
				t1 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i0,i1))
				t1.start()
				t1.join()
				# Processo 2
				t2 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i1,i2))
				t2.start()
				# Processo 3
				t3 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i2,i3))
				t3.start()
				t2.join()
				t3.join()
				if (t1.is_alive()==t2.is_alive()==t3.is_alive()==False):
					del populacao
					populacao = n_populacao
		elif (processos==4):
				itens = tam_pop/processos
				i0=i1=i2=i3=i4=0
				i1=int(i0+itens)
				i2=int(i1+itens)
				i3=int(i2+itens)
				i4=int(i3+itens)
				while(i4<=(tam_pop-1)):
					i4=i4+1
				# Processo 1
				t1 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i0,i1))
				t1.start()
				t1.join()
				# Processo 2
				t2 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i1,i2))
				t2.start()
				# Processo 3
				t3 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i2,i3))
				t3.start()
				# Processo 4
				t4 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i3,i4))
				t4.start()
				t2.join()
				t3.join()
				t4.join()
				if (t1.is_alive()==t2.is_alive()==t3.is_alive()==t4.is_alive()==False):
					del populacao
					populacao = n_populacao

		elif (processos==5):
				itens = tam_pop/processos
				i0=i1=i2=i3=i4=i5=0
				i1=int(i0+itens)
				i2=int(i1+itens)
				i3=int(i2+itens)
				i4=int(i3+itens)
				i5=int(i4+itens)
				while(i5<=(tam_pop-1)):
					i5=i5+1
				# Processo 1
				t1 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i0,i1))
				t1.start()
				t1.join()
				# Processo 2
				t2 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i1,i2))
				t2.start()
				# Processo 3
				t3 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i2,i3))
				t3.start()
				# Processo 4
				t4 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i3,i4))
				t4.start()
				# Processo 5
				t5 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i4,i5))
				t5.start()

				t2.join()
				t3.join()
				t4.join()
				t5.join()
				if (t1.is_alive()==t2.is_alive()==t3.is_alive()==t4.is_alive()==t5.is_alive()==False):
					del populacao
					populacao = n_populacao
		elif (processos==6):
				itens = tam_pop/processos
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
				t1 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i0,i1))
				t1.start()
				t1.join()
				# Processo 2
				t2 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i1,i2))
				t2.start()
				# Processo 3
				t3 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i2,i3))
				t3.start()
				# Processo 4
				t4 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i3,i4))
				t4.start()
				# Processo 5
				t5 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i4,i5))
				t5.start()
				# Processo 6
				t6 = threading.Thread(target=crossover, args=(populacao, tx_mutacao, peso, valor, cap_max, i5,i6))
				t6.start()

				t2.join()
				t3.join()
				t4.join()
				t5.join()
				t6.join()
				if (t1.is_alive()==t2.is_alive()==t3.is_alive()==t4.is_alive()==t5.is_alive()==t6.is_alive()==False):
					del populacao
					populacao = n_populacao

		geracao_atual += 1
		if geracao_atual == max_geracao:
			populacao.sort(reverse=True)
	print("Processos:", processos)
	print("Melhor solucao da geracao ", geracao_atual-1)
	print("Valor: ",populacao[0][0]," Peso: ",populacao[0][1])
	print("Cromossomo", populacao[0][2:])

"""
import threading
from multiprocessing import Queue
def dobro(x, que):
	x = x*x
	que.put(x)
	print(x)

queue1 = Queue()
t1 = threading.Thread(target=dobro, args=(2,queue1))
t1.start()
print(t1)
#t1.join()
x = queue1.get()
print(x)
print(t1)

"""