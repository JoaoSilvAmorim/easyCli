from django.db import models
import uuid
from django.db.models.fields import PositiveIntegerField
from django.db.models.fields.json import JSONField
from django.contrib.auth.models import User

# Create your models here.

def endereco():
    return {
        "cep": "",
        "complemento": "",
        "bairro": "",
        "localidade": "",
        "uf": "",
    }
     
class Empresa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    codigo = models.UUIDField(default=uuid.uuid4, editable=False)
    
    nome = models.CharField(max_length=32)
    nomeFantasia = models.CharField(max_length=32, null=True)
    cnpjCpf = models.CharField(max_length=17, unique=True, null=True)
    email = models.CharField(max_length=22, null=True)
    
    endereco = JSONField(null=True, blank=True)
      
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Tipo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=24)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
class Motivo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=36, null=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class atentende(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=21)
    
class sistema(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=21)
    
 
class Controle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    sistema = models.CharField(max_length=21)
    atendente = models.CharField(max_length=21)

    tipo = models.CharField(max_length=12)
    status = models.CharField(max_length=12)
    inicio = models.DateTimeField()
    fim = models.DateTimeField()
    
    solucao = models.CharField(max_length=32)
    
    motivoChamado = models.ForeignKey(
        Motivo,
        on_delete=models.CASCADE,
    )
    
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    



























#usuario = models.ForeignKey(User, on_delete=models.CASCADE)