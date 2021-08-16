from . models import *
import datetime
import heapq
import operator

def get_post_dict(post, key):
    result = {}
    if post:
        import re
        patt = re.compile('^([a-zA-Z_]\w+)\[([a-zA-Z_\-][\w\-]*)\]$')
        for post_name, value in post.items():
            value = post[post_name]
            match = patt.match(post_name)
            if not match or not value:  
                continue
            name = match.group(1)

            if name == key:
                k = match.group(2)
                result.update({k: value})
    return result



def postFormCopy(data, objeto):
    for item in objeto:
        data[item] = get_post_dict(data, item)
    return data


def clearData(dataInicial, dataFinal, model):
    data = {}
    if dataInicial != '' and dataFinal != '':
        dataInicial = str(dataInicial)
        dataFinal = str(dataFinal)
        
        dataInicial = dataInicial.split('-', 2)
        dataInicial[2] = dataInicial[2].split('T', 1)[0]
        dataFinal = dataFinal.split('-', 2)
        dataFinal[2] = dataFinal[2].split('T', 1)[0]
        
        dataInicial = list(map(int, dataInicial))
        dataFinal = list(map(int, dataFinal))
    
        return model.objects.filter(inicio__gte=datetime.date(dataInicial[0], dataInicial[1], dataInicial[2]),
                                    fim__lte=datetime.date(dataFinal[0], dataFinal[1], dataFinal[2]))
    
    else:
        return model.objects.all()
    

def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l


def filterReason(dataInicial = '', dataFinal = ''):
    #Principais chamados
    motivos = list(Motivo.objects.all())
    controle = list(clearData(dataInicial, dataFinal, Controle))
    chamadosMotivo = []
    dictChamados = {}
    
    cont=0    
    for motivo in motivos:
        for atendimento in controle:
            if motivo.nome == atendimento.motivoChamado.nome:
                cont += 1
        chamadosMotivo.append({motivo.nome : cont})
        cont = 0

    for obj in chamadosMotivo:
       key = list(obj.keys())
       value = list(obj.values())
       dictChamados[key[0]] = value[0]
    
    
    max_motivos = {}
    for i in range(5):
        if len(dictChamados) > 0:
            maxi = max(dictChamados, key=lambda key: dictChamados[key])
            max_motivos[maxi] = dictChamados[maxi]
            del dictChamados[maxi]

    return list(max_motivos.keys()), list(max_motivos.values())
            
            

    
        
        
def filterCalls(dataInicial = '', dataFinal = ''):
    #Atendimentos
    names = ["Lucas","Hilana","Mariana"]
    data = []
    
    model = clearData(dataInicial, dataFinal, Controle)
    
    lucasAtendimento = model.filter(atendente='Lucas')
    hilanaAtendimento = model.filter(atendente='Hilana')
    marianaAtendimentos = model.filter(atendente='Mariana')
    data.append(len(lucasAtendimento))
    data.append(len(hilanaAtendimento))
    data.append(len(marianaAtendimentos))
    
    return names, data
     
     
def filterPendence(dataInicial = '', dataFinal = ''):   
    #Pendencias
    model = clearData(dataInicial, dataFinal, Controle) 
    data = model.all()
    pendentes = model.filter(status='pendente')
    pendentes = (len(pendentes) / len(data)) * 100
    return round(pendentes, 1)




def filterCompanies(dataInicial = '', dataFinal = ''):
    #Filtrar empresas com mais chamados
    chamados = clearData(dataInicial, dataFinal, Controle) 
    
    chamados = list(chamados)
    empresasList = []
    contador = 0
    
    for i in chamados:
        empresasList.append(i.empresa.nomeFantasia)
    
    empresasSemRepeticao = remove_repetidos(empresasList)
    empresasDict = {}
    
    for empresa in empresasSemRepeticao:
        contador = empresasList.count(empresa)
        empresasDict[empresa] = contador
        contador = 0
     
    max_chamados = {}
    for i in range(5):
        if len(empresasDict) > 0:
            maxi = max(empresasDict, key=lambda key: empresasDict[key])
            max_chamados[maxi] = empresasDict[maxi]
            del empresasDict[maxi]
       
    return list(max_chamados.keys()), list(max_chamados.values())
   