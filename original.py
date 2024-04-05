import random
import os
from operator import itemgetter, attrgetter
import copy
prioridadOriginal=[[],[],[],[],[],[],[],[],[],[],[]]
prioridadActual=[]
palabrasReservadas=["numero_procesos","promedio","desv_est","proceso","tiempo_ejec"]
#configuracion
numeroProcesos=0
promedio=0
desviacion=0
tiempoDeEjecucion=0
procesos=[]
#fin configuracion
lista=[]
listaAuxiliar=[]
procesosEnCola=0
tiempodeEjecucionEfectivo=0
def cls():
    if os.name == "posix":
       os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
       os.system ("cls")
def informacion():
    print("Tipo de calendarizador : Interactivo")
    print("Nombre del Calendarizador: Round Robin")
    print("Numero de procesos declarados:     "+str(numeroProcesos))
    print("Promedio configurado:              "+str(promedio))
    print("Desviacion estandar configurada:   "+str(desviacion))
    print("Tiempo de ejecucion configurado:   "+str(tiempoDeEjecucion)+" ms")
    if tiempodeEjecucionEfectivo!=0:
        print("Tiempo de ejecucion del simulador: "+str(tiempodeEjecucionEfectivo)+" ms")
    print("\nProcesos:")
def resumen():
    incompleto=0
    file= open("ResumenResultados.txt","w")
    file.write("Tipo de calendarizador : Interactivo\n")
    file.write("Nombre del Calendarizador: Round Robin\n")
    file.write("Numero de Procesos: "+str(numeroProcesos)+"\n")
    file.write("Promedio configurado: "+str(promedio)+"\n")
    file.write("Desviacion Estandar Configurada: "+str(desviacion)+"\n")
    file.write("Tiempo de Ejecucion: "+str(tiempoDeEjecucion)+" ms"+"\n")
    file.write("Tiempo de Ejecucion del Simulador: "+str(tiempodeEjecucionEfectivo)+" ms"+"\n")
    file.write("\nProcesos:\n")
    file.write("|# Proceso|Tiempo de CPU|Bloqueo E/S|Bloqueo Quanto|Tiempo Efectivo de CPU|Veces Bloqueado|Prioridad|\n")
    for proceso in listaAuxiliar:
        if proceso[0]==proceso[3]:
            file.write("|{:^9}|{:^13}|{:^11}|{:^14}|{:^22}|{:^15}|{:^9}|\n".format(str(proceso[5]),str(proceso[0])+"(ms)",str(proceso[1])+"(ms)",str(proceso[2])+"(ms)",str(proceso[3])+"(ms)",str(proceso[4]),str(proceso[6])))
        else:
            incompleto=1
            file.write("|{:^9}|{:^13}|{:^11}|{:^14}|{:^22}|{:^15}|{:^9}| INCOMPLETO\n".format(str(proceso[5]),str(proceso[0])+"(ms)",str(proceso[1])+"(ms)",str(proceso[2])+"(ms)",str(proceso[3])+"(ms)",str(proceso[4]),str(proceso[6])))    
    if tiempodeEjecucionEfectivo==tiempoDeEjecucion:
        if incompleto==0:
            file.write("\nSE ALCANZO EL LIMITE DE TIEMPO DE LA SIMULACION.\n")
        else:
            file.write("\nSE ALCANZO EL LIMITE DE TIEMPO DE LA SIMULACION Y HAY PROCESOS INCONCLUSOS.\n")
    else:
        file.write("\nSE HAN COMPLETADO TODOS LOS PROCESOS.\n")
    file.close()
def configurar():
    global listaAuxiliar    
    global numeroProcesos
    global promedio
    global desviacion
    global tiempoDeEjecucion
    global procesos
    global procesosEnCola
    global lista
    n=0
    for linea in lista:
        if not linea.startswith("//"):
            listaAuxiliar=linea.split()
            for x in range(0,len(listaAuxiliar)):
                if listaAuxiliar[x] in palabrasReservadas and x+1<len(listaAuxiliar):
                    if listaAuxiliar[x]!=palabrasReservadas[3] and listaAuxiliar[x+1].isnumeric():
                        if listaAuxiliar[x]==palabrasReservadas[0]:
                            numeroProcesos=int(listaAuxiliar[x+1])
                        elif listaAuxiliar[x]==palabrasReservadas[1]:
                            promedio=int(listaAuxiliar[x+1])
                        elif listaAuxiliar[x]==palabrasReservadas[2]:
                            if promedio>int(listaAuxiliar[x+1]):
                                desviacion=int(listaAuxiliar[x+1])
                            else:
                                print ("0x11 hubo un error al guardar "+listaAuxiliar[x])
                                a=input("presione enter para salir...\n")
                                sys.exit()
                        elif listaAuxiliar[x]==palabrasReservadas[4]:
                            tiempoDeEjecucion=int(listaAuxiliar[x+1])
                        else:
                            print ("0x1 hubo un error al guardar "+listaAuxiliar[x])
                            a=input("presione enter para salir...\n")
                            sys.exit()
                    elif listaAuxiliar[x]==palabrasReservadas[3] and x+1<len(listaAuxiliar) and listaAuxiliar[x+1].isnumeric() and x+2<len(listaAuxiliar) and listaAuxiliar[x+2].isnumeric():
                        if x+3<len(listaAuxiliar) and listaAuxiliar[x+3].isnumeric():
                            procesos.append([0,int(listaAuxiliar[x+1]),int(listaAuxiliar[x+2]),0,0,n,int(listaAuxiliar[x+3])])
                        else:
                            procesos.append([0,int(listaAuxiliar[x+1]),int(listaAuxiliar[x+2]),0,0,n,0])
                        n+=1
                        procesosEnCola=procesosEnCola+1
                    else:
                        print ("0x2 hubo un error al guardar "+listaAuxiliar[x])
                        a=input("presione enter para salir...\n")
                        sys.exit()
                elif listaAuxiliar[x] in palabrasReservadas:
                    print ("0x3 hubo un error al guardar "+listaAuxiliar[x])
                    a=input("presione enter para salir...\n")
                    sys.exit()
    for proceso in procesos:
        proceso[0]=random.randint(promedio-desviacion, promedio+desviacion)
    for proceso in procesos:
        for x in range(0,len(prioridadOriginal)):
            if x==proceso[6]:
                prioridadOriginal[x].append(proceso[5])
def simulacion(i):
    global prioridadActual
    global prioridadOriginal
    global procesos
    global lista
    actual=0
    for k in reversed(range(0,len(prioridadActual))):
        for j in range(0,len(prioridadActual[k])):
            if len(prioridadActual[k])>0:
                actual=prioridadActual[k][j]
                if procesos[actual][0]>procesos[actual][3]:
                    file= open("ResumenProcesos.txt","a")
                    file.write("Proceso: "+str(procesos[actual][5])+" Registrado..."+"["+str(procesos[actual][0])+","+str(procesos[actual][1])+","+str(procesos[actual][2])+","+str(procesos[actual][3])+","+str(procesos[actual][4])+","+str(procesos[actual][6])+"]\n")
                    file.close()
                    if k>0:
                        prioridadActual[k-1].append(prioridadActual[k][j])
                while 1==1 and i<tiempoDeEjecucion:
                    if procesos[actual][0]>procesos[actual][3]:
                        procesos[actual][3]+=1
                        i+=1
                    if procesos[actual][0]==procesos[actual][3]:
                        procesos[actual][4]+=1
                        file= open("ResumenProcesos.txt","a")
                        file.write("Proceso: "+str(procesos[actual][5])+" Finalizado..."+"["+str(procesos[actual][0])+","+str(procesos[actual][1])+","+str(procesos[actual][2])+","+str(procesos[actual][3])+","+str(procesos[actual][4])+","+str(procesos[actual][6])+"]\n")
                        file.close()
                        lista.append(procesos[actual])
                        prioridadOriginal[procesos[actual][6]].remove(actual)
                        if k>0:
                            prioridadActual[k-1].pop()
                        break
                    if i%procesos[actual][1]==0 or i%procesos[actual][2]==0:
                        if i%procesos[actual][1]==0 and i%procesos[actual][2]==0:
                            procesos[actual][4]+=1
                            file= open("ResumenProcesos.txt","a")
                            file.write("Proceso: "+str(procesos[actual][5])+" Bloqueo por E/S y Quantum..."+"["+str(procesos[actual][0])+","+str(procesos[actual][1])+","+str(procesos[actual][2])+","+str(procesos[actual][3])+","+str(procesos[actual][4])+","+str(procesos[actual][6])+"]\n")
                            file.close()
                            break
                        elif i%procesos[actual][1]==0:
                            procesos[actual][4]+=1
                            file= open("ResumenProcesos.txt","a")
                            file.write("Proceso: "+str(procesos[actual][5])+" Bloqueo por E/S..."+"["+str(procesos[actual][0])+","+str(procesos[actual][1])+","+str(procesos[actual][2])+","+str(procesos[actual][3])+","+str(procesos[actual][4])+","+str(procesos[actual][6])+"]\n")
                            file.close()
                            break
                        else:
                            procesos[actual][4]+=1
                            file= open("ResumenProcesos.txt","a")
                            file.write("Proceso: "+str(procesos[actual][5])+" Bloqueo por Quantum..."+"["+str(procesos[actual][0])+","+str(procesos[actual][1])+","+str(procesos[actual][2])+","+str(procesos[actual][3])+","+str(procesos[actual][4])+","+str(procesos[actual][6])+"]\n")
                            file.close()
                            break

        prioridadActual[k].clear()
    return i
if __name__ == '__main__':
    file= open("calendarizador.conf",encoding='ansi')
    lista = file.readlines()
    file.close()
    configurar()
    listaAuxiliar.clear()
    lista.clear()
    i=0
    incompleto=0
    if procesosEnCola==numeroProcesos:
        file= open("ResumenProcesos.txt","w")
        file.close()
        informacion()
        print("|# Proceso|Tiempo de CPU|Bloqueo E/S|Bloqueo Quanto|Tiempo Efectivo de CPU|Veces Bloqueado|Prioridad|")
        for proceso in procesos:
            print("|{:^9}|{:^13}|{:^11}|{:^14}|{:^22}|{:^15}|{:^9}|".format(str(proceso[5]),str(proceso[0])+"(ms)",str(proceso[1])+"(ms)",str(proceso[2])+"(ms)",str(proceso[3])+"(ms)",str(proceso[4]),str(proceso[6])))
        a=input("\npresione enter para iniciar simulacion\n")
        prioridadActual=copy.deepcopy(prioridadOriginal)
        print("Trabajando...")
        while i<tiempoDeEjecucion:
            if numeroProcesos!=len(lista):
                i=simulacion(i)
                prioridadActual=copy.deepcopy(prioridadOriginal)
            else:
                break
        tiempodeEjecucionEfectivo=i
        cls()
        informacion()
        print("|# Proceso|Tiempo de CPU|Bloqueo E/S|Bloqueo Quanto|Tiempo Efectivo de CPU|Veces Bloqueado|Prioridad|")
        if numeroProcesos!=len(lista):
            for proceso in procesos:
                if proceso not in lista:
                    lista.append(proceso)
            listaAuxiliar=sorted(lista, key=itemgetter(5))
            for proceso in listaAuxiliar:
                if proceso[0]==proceso[3]:
                    print("|{:^9}|{:^13}|{:^11}|{:^14}|{:^22}|{:^15}|{:^9}|".format(str(proceso[5]),str(proceso[0])+"(ms)",str(proceso[1])+"(ms)",str(proceso[2])+"(ms)",str(proceso[3])+"(ms)",str(proceso[4]),str(proceso[6])))
                else:
                    incompleto=1
                    print("|{:^9}|{:^13}|{:^11}|{:^14}|{:^22}|{:^15}|{:^9}| INCOMPLETO".format(str(proceso[5]),str(proceso[0])+"(ms)",str(proceso[1])+"(ms)",str(proceso[2])+"(ms)",str(proceso[3])+"(ms)",str(proceso[4]),str(proceso[6])))
        else:
            listaAuxiliar=sorted(lista, key=itemgetter(5))
            for proceso in listaAuxiliar:
                print("|{:^9}|{:^13}|{:^11}|{:^14}|{:^22}|{:^15}|{:^9}|".format(str(proceso[5]),str(proceso[0])+"(ms)",str(proceso[1])+"(ms)",str(proceso[2])+"(ms)",str(proceso[3])+"(ms)",str(proceso[4]),str(proceso[6])))
        resumen()
        if tiempodeEjecucionEfectivo==tiempoDeEjecucion:
            if incompleto==0:
                print("\nSE ALCANZO EL LIMITE DE TIEMPO DE LA SIMULACION.\n")
            else:
                print("\nSE ALCANZO EL LIMITE DE TIEMPO DE LA SIMULACION Y HAY PROCESOS INCONCLUSOS.\n")
        else:
            print("\nSE HAN COMPLETADO TODOS LOS PROCESOS.\n")
    else:
        print("diferencia entre procesos declarados y procesos encontrados\nrevise que la cantidad de procesos declarados coincida con la cantidad de procesos configurados")
    a=input("presione enter para salir...\n")
