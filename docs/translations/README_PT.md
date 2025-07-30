# Babel - Tradução de Áudio em Tempo Real com Sobreposição de Legendas

**[English](../../README.md) | [Español](README_ES.md) | [Français](README_FR.md) | [Deutsch](README_DE.md) | Português | [日本語](README_JA.md) | [한국어](README_KO.md) | [中文](README_ZH.md)**

Uma aplicação Python que captura o áudio interno do seu PC, traduz em tempo real usando Faster-Whisper e Google Translate, e exibe legendas traduzidas como sobreposição na sua tela.

## 🌟 Recursos

### 🎵 **Captura de Áudio**
- **Detecção automática**: Encontra automaticamente o melhor dispositivo de loopback (Stereo Mix, Virtual Audio Cable)
- **Seleção manual**: Escolha entre dispositivos de entrada disponíveis com detalhes do dispositivo
- **Captura específica de app**: Suporte para Virtual Audio Cable para capturar aplicações individuais
- **Áudio do sistema**: Capture todo o áudio do PC ou áudio de aplicação específica

### 🧠 **Tradução Baseada em IA**
- **Reconhecimento de voz**: Usa modelos Faster-Whisper (tiny, turbo, large-v3, distil-large-v3)
- **Detecção automática de idioma**: Deixe o Whisper detectar automaticamente o idioma de origem
- **90+ idiomas de origem**: Suporte para todos os principais idiomas que o Whisper pode transcrever
- **100+ idiomas de destino**: Traduz para qualquer idioma suportado pelo Google Translate
- **Processamento em tempo real**: Otimizado para baixa latência e uso de memória

### 📺 **Legendas Profissionais**
- **Exibição sobreposta**: Sobreposição de legendas transparente, sempre no topo
- **Fontes personalizáveis**: Escolha entre 10 fontes populares e múltiplos tamanhos (10px-48px)
- **Reposicionável**: Arraste legendas para qualquer posição na tela
- **Limpeza automática**: Legendas desaparecem automaticamente durante silêncio
- **Design moderno**: Fundo semi-transparente com contornos de texto para legibilidade

### 🌍 **Interface Multilíngue**
- **6 Idiomas de UI**: Inglês, Espanhol, Francês, Alemão, Português, Coreano
- **Localização completa**: Todos os menus, botões, descrições e nomes de idiomas traduzidos
- **Mudança dinâmica**: Altere o idioma da interface e veja atualizações imediatas
- **Dropdowns específicos de idioma**: Nomes de idiomas exibidos no idioma atual da interface

### ⚙️ **Configurações Inteligentes**
- **Configuração persistente**: Todas as configurações salvas automaticamente em `babel_settings.json`
- **Modo de performance**: Alterne entre velocidade e precisão
- **Sensibilidade de áudio**: Limiar ajustável para filtrar ruído de fundo
- **Navegação alfabética**: Digite letras nos dropdowns para encontrar opções rapidamente

## 📋 Requisitos

- **Python**: 3.9 ou superior
- **Sistema Operacional**: Windows (para captura de áudio loopback WASAPI)
- **Memória**: Pelo menos 4GB RAM (8GB recomendado para modelos grandes)
- **Armazenamento**: 1-5GB para modelos Whisper (baixados automaticamente)
- **Internet**: Necessária para API do Google Translate

## 🚀 Instalação

1. **Clone ou baixe** este repositório
2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Execute a aplicação**:
   ```bash
   python main.py
   ```
   Ou use o arquivo batch fornecido:
   ```bash
   run.bat
   ```

## 📖 Guia de Início Rápido

### Configuração Básica
1. **Inicie** a aplicação: `python main.py`
2. **Entrada de Áudio**: Selecione "Auto (Recomendado)" ou escolha um dispositivo específico
3. **Idiomas**: 
   - **De**: Escolha idioma de origem ou "Detectar automaticamente"
   - **Para**: Escolha idioma de destino (padrão: Inglês)
4. **Clique** "▶️ Iniciar Tradução"

### Dicas de Configuração Inicial
- **Teste áudio**: Fale ou reproduza áudio para verificar se o microfone/áudio do sistema está funcionando
- **Ajuste sensibilidade**: Valores menores = mais sensível a áudio baixo
- **Posicione legendas**: Use "⚙ Reposicionar Legendas" para colocá-las onde desejar
- **Escolha modelo**: "turbo" é recomendado para velocidade/precisão equilibrada
- **Seleção rápida de idioma**: Digite letras nos dropdowns de idioma para ir para opções (ex: digite "I" para Inglês)
- **Todas as configurações salvas**: Suas preferências são automaticamente lembradas entre sessões

## 🌍 Idiomas da Interface do Usuário

Babel suporta os seguintes idiomas para a interface do usuário:
- **Inglês** (padrão)
- **Espanhol** (Español)
- **Francês** (Français) 
- **Alemão** (Deutsch)
- **Português** (padrão)
- **Coreano** (한국어)

Altere o idioma da UI na página "⚙ Configurações" usando o dropdown "Idioma da UI". Todos os menus, botões, descrições, tooltips e nomes de idiomas serão exibidos no seu idioma selecionado.

## 🗣️ Idiomas Suportados

### Idiomas de Origem (Reconhecimento Whisper)
**Detectar automaticamente**, Africâner, Albanês, Amárico, Árabe, Armênio, Assamês, Azerbaijano, Bashkir, Basco, Bielorrusso, Bengali, Bósnio, Bretão, Búlgaro, Birmanês, Catalão, Chinês, Croata, Tcheco, Dinamarquês, Holandês, Inglês, Estoniano, Feroês, Finlandês, Francês, Galego, Georgiano, Alemão, Grego, Gujarati, Haitiano, Hauçá, Havaiano, Hebraico, Hindi, Húngaro, Islandês, Indonésio, Italiano, Japonês, Javanês, Canarim, Cazaque, Khmer, Coreano, Laociano, Latim, Letão, Lituano, Luxemburguês, Macedônio, Malgaxe, Malaio, Malaiala, Maltês, Maori, Marata, Mongol, Nepalês, Norueguês, Occitano, Pashto, Persa, Polonês, Português, Punjabi, Romeno, Russo, Sânscrito, Sérvio, Shona, Sindi, Cingalês, Eslovaco, Esloveno, Somali, Espanhol, Sundanês, Suaíli, Sueco, Tagalo, Tajique, Tâmil, Tártaro, Telugu, Tailandês, Tibetano, Turco, Turcomano, Ucraniano, Urdu, Uzbeque, Vietnamita, Galês, Iídiche, Iorubá

### Idiomas de Destino (Google Translate)
**Inglês** (padrão), Africâner, Albanês, Amárico, Árabe, Armênio, Azerbaijano, Basco, Bielorrusso, Bengali, Bósnio, Búlgaro, Catalão, Cebuano, Chinês (Simplificado), Chinês (Tradicional), Corso, Croata, Tcheco, Dinamarquês, Holandês, Esperanto, Estoniano, Finlandês, Francês, Frísio, Galego, Georgiano, Alemão, Grego, Gujarati, Crioulo Haitiano, Hauçá, Havaiano, Hebraico, Hindi, Hmong, Húngaro, Islandês, Igbo, Indonésio, Irlandês, Italiano, Japonês, Javanês, Canarim, Cazaque, Khmer, Coreano, Curdo, Quirguiz, Laociano, Latim, Letão, Lituano, Luxemburguês, Macedônio, Malgaxe, Malaio, Malaiala, Maltês, Maori, Marata, Mongol, Birmanês (Birmano), Nepalês, Norueguês, Odia (Oriya), Pashto, Persa, Polonês, Português, Punjabi, Romeno, Russo, Samoano, Gaélico Escocês, Sérvio, Sesoto, Shona, Sindi, Cingalês, Eslovaco, Esloveno, Somali, Espanhol, Sundanês, Suaíli, Sueco, Tagalo, Tajique, Tâmil, Tártaro, Telugu, Tailandês, Turco, Turcomano, Ucraniano, Urdu, Uigur, Uzbeque, Vietnamita, Galês, Xosa, Iídiche, Iorubá, Zulu

## ⚙️ Opções de Configuração

### Configurações de Áudio
- **Seleção de Dispositivo**: Detecção automática ou seleção manual de dispositivo
- **Sensibilidade de Áudio**: Limiar 0.001-0.100 para filtragem de ruído
- **Modo de Performance**: Alterne para velocidade vs. precisão otimizada

### Modelos de IA
- **tiny**: Mais rápido, precisão básica (~40MB)
- **turbo**: Velocidade/precisão equilibrada (~810MB) - **Recomendado**
- **large-v3**: Maior precisão, mais lento (~3GB)
- **distil-large-v3**: Modelo grande otimizado (~1.5GB)

### Aparência das Legendas
- **Família da Fonte**: Segoe UI, Arial, Helvetica, Times New Roman, Calibri, Trebuchet MS, Verdana, Georgia, Comic Sans MS, Impact
- **Tamanho da Fonte**: 10px a 48px
- **Posição**: Arraste para reposicionar em qualquer lugar da tela
- **Limpeza automática**: Legendas desaparecem após 2 segundos de silêncio

## 🎯 Guia de Captura de Áudio Específica de App

### Para Aplicações Individuais
1. **Instale Virtual Audio Cable** (VB-Cable ou similar)
2. **Configure saída de áudio da aplicação** para Virtual Cable
3. **No Babel**: Selecione o dispositivo Virtual Cable (marcado com 🎯)
4. **Inicie tradução** - agora apenas o áudio desse app será traduzido

### Para Áudio do Sistema
1. **Ative Stereo Mix** nas configurações de Som do Windows:
   - Clique direito no ícone do alto-falante → Sons → aba Gravação
   - Clique direito no espaço vazio → Mostrar Dispositivos Desabilitados
   - Ative "Stereo Mix"
2. **No Babel**: Selecione dispositivo Stereo Mix (marcado com 🔊) ou use detecção automática

### Configuração do Virtual Audio Cable
1. **Baixe** VB-Audio Virtual Cable (gratuito)
2. **Instale e reinicie** seu computador
3. **Configure aplicação alvo** para saída em "CABLE Input"
4. **No Babel**: Selecione dispositivo "🎯 CABLE Output"
5. **Opcional**: Configure "CABLE Input" como seu dispositivo de reprodução padrão para ouvir áudio

## 🛠️ Solução de Problemas

### Nenhum Áudio Detectado
- **Verifique seleção de dispositivo**: Tente "Auto (Recomendado)" primeiro
- **Verifique fonte de áudio**: Certifique-se de que áudio está realmente tocando
- **Ajuste sensibilidade**: Diminua o limiar de sensibilidade de áudio
- **Ative Stereo Mix**: Siga o guia de configuração de áudio do sistema acima

### Captura de Áudio Não Funciona Durante Chamadas (Zoom, Teams, Discord, etc.)
**Este é um problema comum ao usar aplicações de conferência. Aqui estão as soluções:**

#### **Problema: Conflito de Modo Exclusivo**
- **Problema**: Apps de conferência frequentemente tomam controle exclusivo de dispositivos de áudio
- **Solução**: 
  1. Vá para Configurações de Som do Windows → Propriedades do Dispositivo → Avançado
  2. Desmarque "Permitir que aplicações tomem controle exclusivo deste dispositivo"
  3. Aplique isso tanto ao seu microfone quanto aos alto-falantes
  4. Reinicie ambas as aplicações

#### **Problema: Roteamento de Dispositivo de Áudio**
- **Problema**: Áudio de chamada pode usar dispositivos virtuais ou cancelamento de eco que contornam áudio do sistema
- **Solução**: 
  1. **Instale um Virtual Audio Cable** (VB-Cable, VoiceMeeter)
  2. **No seu app de conferência**: Configure saída de áudio para Virtual Cable
  3. **No Babel**: Selecione o Virtual Cable como dispositivo de entrada
  4. **Opcional**: Configure Virtual Cable como dispositivo de reprodução padrão para ouvir áudio

#### **Problema: Isolamento de Áudio Específico de App**
- **Problema**: Alguns apps de conferência criptografam ou isolam seus streams de áudio
- **Soluções**:
  1. **Use Windows 11**: Tente o recurso "Application Audio Capture" do OBS
  2. **Altere configurações do app de conferência**: Procure por opções "Áudio do sistema" ou "Compartilhar som do computador"
  3. **Use versão do navegador**: Apps de conferência baseados na web são frequentemente mais fáceis de capturar
  4. **Tente VoiceMeeter**: Solução de roteamento de áudio virtual mais avançada

#### **Correções Rápidas para Captura de Áudio de Chamada**
1. **Antes de entrar numa chamada**: Inicie Babel e verifique se captura áudio do sistema
2. **Use "Compartilhar Áudio do Computador"**: Ative esta opção no seu app de conferência
3. **Mude para versão do navegador**: Frequentemente tem menos restrições de áudio
4. **Use fones de ouvido**: Previne loops de feedback que podem interferir com captura
5. **Verifique Configurações de Privacidade do Windows**: Certifique-se de que permissões de microfone estão habilitadas para todos os apps

### Tradução Não Funciona
- **Verifique conexão com internet**: Google Translate requer internet
- **Verifique idiomas**: Certifique-se de que idioma de origem coincide com o áudio real
- **Tente detecção automática**: Deixe Whisper detectar automaticamente o idioma de origem
- **Mude modelos**: Tente modelo "turbo" para melhor precisão

### Problemas de Performance
- **Ative Modo de Performance**: Reduz uso de memória e melhora velocidade
- **Use modelo menor**: Mude de "large-v3" para "turbo" ou "tiny"
- **Feche outras aplicações**: Libere RAM para melhor performance
- **Verifique velocidade da internet**: Conexão lenta afeta velocidade de tradução

### Problemas de Legenda
- **Legendas não visíveis**: Verifique se sobreposição está atrás de outras janelas
- **Posição errada**: Use "⚙ Reposicionar Legendas" para movê-las
- **Fonte muito pequena/grande**: Ajuste tamanho da fonte nas configurações
- **Não limpando**: Verifique sensibilidade de áudio - pode estar detectando ruído de fundo

## 🔧 Como Funciona

### Pipeline de Áudio
1. **Captura**: Grava áudio do dispositivo selecionado (áudio do sistema ou específico de app)
2. **Processamento**: Converte estéreo para mono, aplica filtragem de ruído
3. **Transcrição**: Usa Faster-Whisper para converter fala em texto
4. **Tradução**: API do Google Translate traduz para idioma de destino
5. **Exibição**: Mostra legendas como sobreposição com limpeza automática

### Detalhes Técnicos
- **Formato de Áudio**: 48kHz estéreo, convertido para 16kHz mono para Whisper
- **Tamanho do Chunk**: Segmentos de áudio de 3 segundos para processamento em tempo real
- **Gerenciamento de Memória**: Limites de tamanho de fila (máx 3 chunks) e coleta de lixo para eficiência
- **Otimização de Latência**: Beam size 1, filtragem VAD, reamostragem otimizada
- **Framework UI**: PyQt5 com widgets AlphabetComboBox personalizados para navegação aprimorada
- **Armazenamento de Configurações**: Configuração persistente baseada em JSON com salvamento automático

### Arquitetura do Sistema de Tradução
- **Arquivos JSON Externos**: Todas as traduções armazenadas no diretório `translations/`
- **Carregamento Dinâmico**: Traduções carregadas automaticamente na inicialização
- **Detecção de Idioma**: Traduções hardcoded previnem problemas de recursão
- **Localização Completa**: Texto da UI, nomes de idiomas, descrições todos traduzidos
- **Mapeamento Reverso**: Nomes de idiomas traduzidos convertidos de volta para inglês para armazenamento de configurações

### Persistência de Configurações
Todas as configurações são automaticamente salvas em `babel_settings.json`:
```json
{
  "subtitle_y_offset": 184,
  "subtitle_x_offset": -5,
  "font_family": "Segoe UI",
  "font_size": 16,
  "source_language": "Korean",
  "target_language": "English",
  "audio_device": "Auto (Recommended)",
  "audio_device_data": -1,
  "whisper_model": "turbo",
  "audio_threshold": 0.001,
  "performance_mode": false,
  "ui_language": "Portuguese"
}
```

## 📁 Estrutura de Arquivos

```
babel/
├── main.py                    # Arquivo principal da aplicação
├── requirements.txt           # Dependências Python
├── babel_settings.json        # Configurações do usuário auto-salvas
├── run.bat                   # Arquivo batch do Windows para executar o app
├── logo.png                  # Logo da aplicação
├── translations/             # Arquivos de tradução da UI
│   ├── en.json              # Traduções em inglês
│   ├── es.json              # Traduções em espanhol
│   ├── fr.json              # Traduções em francês
│   ├── de.json              # Traduções em alemão
│   ├── pt.json              # Traduções em português
│   └── ko.json              # Traduções em coreano
└── README.md                 # Esta documentação
```

## 🎮 Uso Avançado

### Dispositivos de Áudio Personalizados
A aplicação detecta automaticamente:
- **🎯 Virtual Audio Cables**: Para captura específica de app
- **🔊 Dispositivos de Áudio do Sistema**: Para captura de áudio completo do sistema  
- **🎤 Entradas de Microfone**: Para fontes de áudio externas

### Ajuste de Performance
- **Para Velocidade**: Use modelo "tiny" + Modo de Performance habilitado
- **Para Precisão**: Use modelo "large-v3" + Modo de Performance desabilitado
- **Equilibrado**: Use modelo "turbo" (padrão recomendado)

### Uso de Memória
- **modelo tiny**: ~200MB RAM
- **modelo turbo**: ~1GB RAM  
- **modelo large-v3**: ~4GB RAM
- **distil-large-v3**: ~2GB RAM

## 📚 Suporte e Contribuição

### Obtendo Ajuda
1. **Verifique este README** para soluções comuns
2. **Verifique requisitos**: Python 3.9+, SO Windows
3. **Teste com áudio simples**: Tente com fala clara primeiro
4. **Verifique o console**: Execute da linha de comando para ver mensagens de erro

### Limitações Conhecidas
- **Apenas Windows**: Captura de áudio loopback WASAPI requer Windows
- **Internet necessária**: API do Google Translate precisa de conexão com internet
- **Downloads de modelo**: Primeira execução baixa modelos Whisper (podem ser grandes)
- **Processamento em tempo real**: Algum atraso é normal (1-3 segundos)

### Melhorias Futuras
- Suporte Linux/macOS
- Opções de tradução offline
- Temas de legenda personalizados
- Processamento de arquivo em lote
- API para integrações externas

## 🆕 Recursos e Atualizações Mais Recentes

### **Experiência do Usuário Aprimorada** 
- **Todas as configurações auto-salvas**: Toda configuração automaticamente salva em `babel_settings.json`
- **Navegação alfabética**: Digite letras nos dropdowns para ir rapidamente para idiomas
- **UI melhorada**: Tema escuro moderno com melhor espaçamento e feedback visual
- **Padrões inteligentes**: Idioma de destino inglês, modelo turbo pré-selecionado

### **Localização Completa da Interface**
- **6 Idiomas de UI**: Suporte completo para Inglês, Espanhol, Francês, Alemão, Português, Coreano
- **Mudança dinâmica de idioma**: Altere idioma da interface e veja atualizações imediatas
- **Traduções hardcoded**: Todos os nomes de idiomas traduzidos para prevenir recursão
- **Cobertura abrangente**: 70+ idiomas traduzidos em cada idioma da interface

### **Personalização Avançada de Legendas**
- **10 opções de fonte**: Segoe UI, Arial, Helvetica, Times New Roman e mais
- **13 tamanhos de fonte**: De 10px a 48px para visibilidade perfeita
- **Posicionamento por arrastar**: Clique "⚙ Reposicionar Legendas" e arraste para qualquer posição da tela
- **Limpeza automática**: Legendas desaparecem após 2 segundos de silêncio
- **Design moderno**: Fundos semi-transparentes com contornos de texto

### **Detecção Inteligente de Dispositivo de Áudio**
- **Auto-categorização**: Dispositivos marcados com 🎯 (Virtual Cable), 🔊 (Áudio do Sistema), 🎤 (Microfone)
- **Prioridade inteligente**: Seleciona automaticamente o melhor dispositivo loopback disponível
- **Detalhes do dispositivo**: Mostra canais e taxa de amostragem para cada dispositivo
- **Capacidade de atualização**: Atualiza lista de dispositivos sem reiniciar

### **Otimizações de Performance**
- **Modo de Performance**: Alterne para otimização velocidade vs precisão
- **Gerenciamento de memória**: Coleta de lixo automática e limites de tamanho de fila
- **Modelos otimizados**: Suporte para distil-large-v3 (modelo grande otimizado)
- **Filtragem VAD**: Detecção de Atividade de Voz para reduzir processamento de silêncio

---

**Babel** - Tornando tradução em tempo real acessível para todos. Perfeito para jogos internacionais, assistir conteúdo estrangeiro ou aprender novos idiomas!
