from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.db import connection
from .help import *
from .forms import *
from .models import * 
import json

def cadAtendimento(request):
    empresas = Empresa.objects.all()
    motivos = Motivo.objects.all()
    atendentes = atentende.objects.all()
    sistemas = sistema.objects.all()
    controles = Controle.objects.prefetch_related().all()
    form = {}
    if request.method == 'POST':
        form = ControleForm(request.POST.copy())
        if form.is_valid():
            form.create(validated_data=form.cleaned_data)
            return redirect('cadAtendimento')
        print(form.errors)
    return render(request,  'cadAtendimento.html', {'empresas' : empresas, 'motivos': motivos, 'atendentes': atendentes, 'sistemas' : sistemas, 'controles': controles, 'form': form})




def motivoChamado(request):
    form = {}
    if request.method == 'POST':
        form = MotivoForm(request.POST.copy())
        if form.is_valid():
            form.create(validated_data=form.cleaned_data)
            return redirect('motivoChamado')
    return render(request, 'motivoChamado.html', {'form': form})


def createEmpresa(request):
    empresas = Empresa.objects.all()
    form = {}
    if request.method == 'POST':
        dataPost = postFormCopy(request.POST.copy(), ['endereco'])
        form = EmpresaForm(dataPost)
        if form.is_valid():
            form.create(validated_data=form.cleaned_data)
            return redirect('createEmpresa')
        
    return render(request, 'cadEmpresa.html', {'form': form, 'empresas' : empresas})



def redUpdate(request, id):
    obj = get_object_or_404(Controle,pk=id)
    return render(request, 'updateAtendimento.html', {'data': obj})


def updateAtendimento(request):
    form = dict(request.POST)
    obj = get_object_or_404(Controle, id = form['id'][0])
    obj.status = form['status'][0]
    obj.save()
    return render(request,  'updateAtendimento.html', {'data' : obj})


def redUpdateEmpresa(request, id):
    form = dict(request.POST)
    obj = get_object_or_404(Empresa, pk = id)
    empresas = Empresa.objects.all()
    
    if request.method == 'POST':
        obj.nome = form['nome'][0]
        obj.nomeFantasia = form['nomeFantasia'][0]
        obj.cnpjCpf = form['cnpjCpf'][0]
        obj.email = form['email'][0]
        obj.save()
    
    return render(request, 'updateEmpresa.html', {'obj' : obj, 'empresas': empresas})


def graficosRegistro(request):
    #Atendimentos
    names, data = filterCalls()
    
    #Pendencias
    pendentes = filterPendence()
    
    #Problemas mais ocorridos
    motivo, motivoVal = filterReason()
    
    #Principais chhamdos
    empresas, dataEmpresas = filterCompanies()
    
    
    context = {
        'names': json.dumps(names),
        'data': json.dumps(data),
        'contMotivo': json.dumps(motivoVal),
        'chamadosMotivo': json.dumps(motivo),
        'pendentes': json.dumps(round(pendentes, 1)),
        'empresas' :json.dumps(empresas),
        'dataEmpresas' :json.dumps(dataEmpresas),
    }
        
    return render(request, 'graficosRegistro.html', context)





def filtrarRelatorio(request, dataInicial = '', dataFinal = ''):
    context = {}
    formFiltro = dict(request.POST)
    
     #Atendimentos
    names, data = filterCalls(formFiltro['dataInicial'][0], formFiltro['dataFinal'][0])
    
    #Pendencias
    pendentes = filterPendence(formFiltro['dataInicial'][0], formFiltro['dataFinal'][0])
    
    #Problemas mais ocorridos
    motivo, motivoVal = filterReason(formFiltro['dataInicial'][0], formFiltro['dataFinal'][0])
    
    
    #Principais chhamdos
    empresas, dataEmpresas = filterCompanies(formFiltro['dataInicial'][0], formFiltro['dataFinal'][0])
    
    context = {
        'names': json.dumps(names),
        'data': json.dumps(data),
        'contMotivo': json.dumps(motivoVal),
        'chamadosMotivo': json.dumps(motivo),
        'pendentes': json.dumps(round(pendentes, 1)),
        'empresas' :json.dumps(empresas),
        'dataEmpresas' :json.dumps(dataEmpresas),
    }
    return render(request, 'graficosRegistro.html', context)