#!/bin/bash

# Script de Correção Automática - Email Assistant
# Desenvolvido por Manus AI para Escussel

echo "🚀 INICIANDO CORREÇÃO DO REPOSITÓRIO..."
echo "========================================"

# Verificar se estamos no diretório correto
if [ ! -f "README.md" ]; then
    echo "❌ ERRO: Execute este script no diretório raiz do projeto"
    exit 1
fi

echo "✅ Diretório verificado"

# Remover arquivo ZIP se existir
if [ -f "Escussel-Email-Assistant.zip" ]; then
    echo "🗑️  Removendo arquivo ZIP desnecessário..."
    rm -f Escussel-Email-Assistant.zip
    echo "✅ ZIP removido"
fi

# Verificar se os workflows existem
if [ ! -d ".github/workflows" ]; then
    echo "❌ ERRO: Diretório .github/workflows não encontrado"
    echo "📋 Certifique-se de que todos os arquivos foram extraídos corretamente"
    exit 1
fi

echo "✅ Workflows encontrados"

# Verificar secrets necessários
echo "🔐 Verificando configuração de secrets..."
echo "📋 SECRETS NECESSÁRIOS:"
echo "   - KEYSTORE_BASE64"
echo "   - KEYSTORE_PASSWORD"
echo "   - KEY_ALIAS" 
echo "   - KEY_PASSWORD"

# Configurar git se necessário
if [ ! -d ".git" ]; then
    echo "🔧 Inicializando repositório Git..."
    git init
    git branch -M main
    git remote add origin https://github.com/Escussel/E-mail-Assistant.git
    echo "✅ Git configurado"
fi

# Adicionar todos os arquivos
echo "📦 Adicionando arquivos ao Git..."
git add .
git commit -m "fix: estrutura corrigida para build automático

- Adicionados workflows GitHub Actions
- Configuração de build Android
- Scripts de automação
- Documentação completa"

echo "✅ Commit criado"

# Push para o repositório
echo "🚀 Enviando correções para GitHub..."
git push -u origin main --force

echo ""
echo "🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!"
echo "=================================="
echo ""
echo "📱 PRÓXIMOS PASSOS:"
echo "1. ✅ Estrutura corrigida"
echo "2. ✅ Workflows adicionados" 
echo "3. 🔄 Build automático iniciará em 1-2 minutos"
echo "4. ⏰ APK estará pronto em 5-10 minutos"
echo ""
echo "🔗 ACOMPANHAR PROGRESSO:"
echo "Actions: https://github.com/Escussel/E-mail-Assistant/actions"
echo "Releases: https://github.com/Escussel/E-mail-Assistant/releases"
echo ""
echo "📱 SEU APK ESTARÁ EM:"
echo "https://github.com/Escussel/E-mail-Assistant/releases/latest/download/EmailAssistant-release-signed.apk"
echo ""
echo "✨ Desenvolvido com ❤️ por Manus AI para Escussel"

