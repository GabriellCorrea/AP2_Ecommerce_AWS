# Diferenciais Implementados — AP2

---

## 1. Organização de ambientes (dev e prod)

**Como foi feito:**

O `settings.py` detecta automaticamente em qual ambiente está rodando pela presença da variável `RDS_HOSTNAME`, que é injetada automaticamente pelo Elastic Beanstalk quando há um RDS vinculado.

```python
# settings.py
if os.environ.get('RDS_HOSTNAME'):
    # produção: MySQL no RDS
    DATABASES = { 'default': { 'ENGINE': 'django.db.backends.mysql', ... } }
else:
    # desenvolvimento local: SQLite
    DATABASES = { 'default': { 'ENGINE': 'django.db.backends.sqlite3', ... } }

if os.environ.get('AWS_STORAGE_BUCKET_NAME'):
    # produção: imagens no S3
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    # desenvolvimento local: imagens em /media/
    MEDIA_ROOT = BASE_DIR / 'media'
```

Em desenvolvimento, nenhuma variável de ambiente é necessária — o projeto roda com SQLite e mídia local. Em produção (EB), as variáveis do RDS e do S3 ativam automaticamente os serviços AWS.

---

## 2. Tratamento de erros de upload e validações adicionais

**Como foi feito:**

Validação implementada no serializer (`api/serializers.py`) antes do arquivo ser enviado ao S3:

```python
IMAGEM_TIPOS_PERMITIDOS = ['image/jpeg', 'image/png', 'image/webp']
IMAGEM_TAMANHO_MAXIMO_MB = 5

def validate_imagem(self, arquivo):
    if arquivo.content_type not in IMAGEM_TIPOS_PERMITIDOS:
        raise serializers.ValidationError(
            f"Tipo de arquivo não permitido: {arquivo.content_type}. Use JPEG, PNG ou WebP."
        )
    if arquivo.size > IMAGEM_TAMANHO_MAXIMO_MB * 1024 * 1024:
        raise serializers.ValidationError(
            f"Arquivo muito grande ({arquivo.size / 1024 / 1024:.1f} MB). O limite é 5 MB."
        )
    return arquivo
```

Se o arquivo for inválido, a API retorna HTTP 400 com mensagem descritiva antes de qualquer tentativa de upload.

---

## 3. Checklist de troubleshooting no README

**Como foi feito:**

Seção adicionada no `README.md` com os problemas reais encontrados durante o desenvolvimento e as soluções aplicadas:

| Problema | Verificação |
|---|---|
| `migrate` falha no deploy | Verificar Security Group do RDS — liberar porta 3306 para o SG do EB |
| Imagem não aparece na API | Confirmar `AWS_STORAGE_BUCKET_NAME` e política pública do bucket S3 |
| Erro 500 após deploy | Verificar logs: `eb logs` ou console EB → Logs |
| Django Admin sem CSS | Verificar configuração do WhiteNoise e rodar `collectstatic` |
| Variáveis não reconhecidas | Console EB → Configuração → Software → conferir todas as variáveis |

Os itens do checklist foram baseados em erros reais que ocorreram durante o deploy do projeto.

---

## 4. Script de bootstrap para setup local

**Como foi feito:**

Script `setup.sh` na raiz do projeto que automatiza todo o setup local em um único comando:

```bash
bash setup.sh
```

O script executa automaticamente:
1. Cria o ambiente virtual Python (`venv`)
2. Instala todas as dependências (`pip install -r requirements.txt`)
3. Sobe o MySQL local via Docker
4. Aguarda o banco ficar disponível
5. Aplica as migrations (`manage.py migrate`)
6. Roda o `collectstatic`
7. Orienta a criação do superusuário

Qualquer integrante do grupo consegue rodar o projeto localmente com um único comando, sem configuração manual.

---

## 5. Uso de JSONField com consultas JSON

**Como foi feito:**

Campo `atributos` adicionado ao modelo `Produto` (`api/models.py`):

```python
atributos = models.JSONField(blank=True, null=True)
```

Permite armazenar atributos variáveis por categoria de produto sem criar colunas fixas para cada especificação.

Filtros implementados na view (`api/views.py`) usando a sintaxe de lookup do Django para campos JSON:

```python
ATRIBUTOS_FILTRO = ['marca', 'cor', 'ram_gb', 'tamanho', 'voltagem']

def get_queryset(self):
    qs = Produto.objects.all()
    for atributo in self.ATRIBUTOS_FILTRO:
        valor = self.request.query_params.get(atributo)
        if valor:
            qs = qs.filter(**{f'atributos__{atributo}': valor})
    return qs
```

Exemplos de uso:
```
GET /api/produtos/?marca=Dell
GET /api/produtos/?cor=preto
GET /api/produtos/?loja=1&ram_gb=16
```

**Observação sobre o banco:** O projeto usa MySQL (em vez de PostgreSQL), então o campo é `JSONField` com consultas JSON nativas do MySQL 8+, não `JSONField` com consultas JSONB do PostgreSQL. A funcionalidade é equivalente — filtragem dentro do JSON funciona — mas sem o índice GIN do PostgreSQL. O diferencial foi implementado conforme solicitado.
