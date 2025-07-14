#!/bin/bash

echo "🚀 Iniciando setup do projeto Django..."

# Verifica se Python está instalado
if ! command -v python &> /dev/null; then
    echo "❌ Python não está instalado. Instale e execute novamente."
    exit 1
fi

# Verifica se manage.py existe
if [ ! -f "manage.py" ]; then
    echo "❌ manage.py não encontrado. Execute o script na raiz do projeto."
    exit 1
fi

# Cria ambiente virtual se não existir
if [ ! -d "pdv_env" ]; then
    echo "📦 Criando ambiente virtual..."
    python -m venv pdv_env
fi

# Ativa o ambiente virtual
source pdv_env/bin/activate

# Atualiza pip
echo "⬆️ Atualizando pip..."
pip install --upgrade pip

# Instala dependências
echo "📥 Instalando dependências..."
pip install django djangorestframework django-filter 

# Aplica migrações
echo "🛠️ Aplicando migrações..."
python manage.py makemigrations
python manage.py migrate

# Cria superusuário (opcional)
read -p "❓ Deseja criar um superusuário agora? (s/n): " criar_super
if [ "$criar_super" == "s" ]; then
    python manage.py createsuperuser
fi

# Inicia servidor
echo "✅ Setup concluído! Acesse: http://127.0.0.1:8000"
python manage.py runserver
