from django import forms
from django.db.models import fields
from .models import Empresa, Controle, Tipo, Motivo, atentende

class EmpresaForm(forms.Form):
    nome = forms.CharField(required=False)
    nomeFantasia = forms.CharField(required=True)
    cnpjCpf = forms.CharField(required=True)
    email = forms.CharField(required=False)
    endereco = forms.JSONField(required=False)
    
    def clean(self):
        data = self.cleaned_data
        try:
            nomeFantasia = data['nomeFantasia']
        except:
            raise forms.ValidationError("O nome fantasia não pode estar em branco!!!")
        
        cnpjCpf = self.cleaned_data['cnpjCpf']
        if Empresa.objects.filter(cnpjCpf=cnpjCpf).exists():
            raise forms.ValidationError("Empresa já cadastrada!!!")
        

    def create(self, validated_data):
        data = validated_data
        Empresa.objects.create(**data)
        
        
        
        
class MotivoForm(forms.Form):
    nome = forms.CharField(required=True)
    
    def clean(self):
        data = self.cleaned_data  
        
        try:
            motivo = self.cleaned_data['nome']
        except:
            return forms.ValidationError("O campo motivo não pode estar em branco")
        
        nomeMotivo = data['nome']
        if Motivo.objects.filter(nome = nomeMotivo).exists():
            raise forms.ValidationError("Motivo já cadastrado")
        
    
    def create(self, validated_data):
        data = validated_data.copy()
        Motivo.objects.create(**data) 

        
class ControleForm(forms.Form):
    empresa = forms.CharField(required=True)
    motivoChamado = forms.CharField(required=False)
    sistema = forms.CharField(required=False)
    atendente = forms.CharField(required=True)
    
    status = forms.CharField(required=False)
    solucao = forms.CharField(required=False)
    tipo = forms.CharField(required=False)
    
    inicio = forms.CharField()
    fim = forms.CharField()
        
    def clean(self):
        data = self.cleaned_data
        
        try:
            empresa = data['empresa']
            
        except:
            raise forms.ValidationError("Selecione uma empresa!!!")
        
        try:
            atendente = data['atendente']
    
        except:
            raise forms.ValidationError("Selecione o atendente!!!")
    
        class Meta: 
            model = Controle
            fields = '__all__'
        
        
    def create(self, validated_data):
        data = validated_data.copy()
        
        data['empresa'] = Empresa.objects.get(id=data['empresa'])
        data['motivoChamado'] = Motivo.objects.get(id=data['motivoChamado'])
        Controle.objects.create(**data)
        
    