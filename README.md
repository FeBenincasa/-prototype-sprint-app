# 📋 Task Reminder Desktop App (Eel + Python)

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Eel](https://img.shields.io/badge/eel-v3.1.4+-green.svg)
![SQLite](https://img.shields.io/badge/database-SQLite-lightblue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

> **Demo de aplicativo desktop para gerenciamento de tarefas com lembretes por email.**

Um mini-app desktop elegante que demonstra a integração entre Python backend e frontend web usando Eel, com funcionalidades completas de CRUD e envio de emails.

![App Screenshot](https://via.placeholder.com/800x500/667eea/ffffff?text=Task+Reminder+App+Screenshot)

## ✨ Funcionalidades

- ✅ **CRUD Completo de Tarefas** - Criar, visualizar, completar e excluir tarefas
- 📧 **Lembretes por Email** - Envio automático de tarefas do dia (SMTP real ou simulado)
- 🗄️ **Banco SQLite Local** - Armazenamento persistente e confiável
- 🎨 **Interface Responsiva** - Design moderno com HTML/CSS/JavaScript
- 🖥️ **App Desktop Nativo** - Experiência desktop com tecnologia web
- 🔄 **Atualização em Tempo Real** - Interface dinâmica e reativa
- ⚡ **Performance Otimizada** - Carregamento rápido e operações fluidas

## 🛠️ Tech Stack

| Tecnologia | Uso | Versão |
|------------|-----|--------|
| **Python** | Backend logic | 3.8+ |
| **Eel** | Desktop GUI framework | 3.1.4+ |
| **SQLAlchemy** | ORM para database | 2.0.0+ |
| **SQLite** | Banco de dados local | Built-in |
| **HTML/CSS/JS** | Frontend interface | ES6+ |
| **SMTP** | Envio de emails | Built-in |

## 🚀 Como rodar

### Pré-requisitos

- Python 3.8 ou superior
- Chrome ou Chromium instalado (recomendado)
- Git (para clonar o repositório)

### Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/eel-task-app.git
cd eel-task-app
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure email (opcional)**
```bash
# Copie o arquivo de exemplo
copy .env.example .env

# Edite o .env com suas credenciais SMTP
# (Se não configurar, o app simulará o envio)
```

5. **Execute a aplicação**
```bash
python main.py
```

### Modo Desenvolvimento

Para executar com dados de exemplo:
```bash
python main.py --dev
```

## 📱 Como usar

### Gerenciar Tarefas
1. **Adicionar**: Preencha o título e data (opcional) e clique em "Add Task"
2. **Completar**: Marque o checkbox ao lado da tarefa
3. **Excluir**: Clique no ícone de lixeira 🗑️
4. **Atualizar**: Use o botão "Refresh" ou aguarde a atualização automática

### Enviar Lembretes
1. Insira seu email no campo correspondente
2. Clique em "Send Daily Reminder"
3. Receberá um email com todas as tarefas do dia

## 📂 Estrutura do Projeto

```
eel-task-app/
├── main.py               # 🚀 Aplicação principal com Eel
├── database.py           # 🗄️ Modelos e operações SQLite
├── email_sender.py       # 📧 Lógica de envio de emails
├── requirements.txt      # 📦 Dependências Python
├── .env.example         # ⚙️ Configurações de exemplo
├── .gitignore           # 📋 Arquivos ignorados pelo Git
├── README.md            # 📖 Documentação
└── web/                 # 🌐 Frontend
    ├── index.html       # 📄 Interface principal
    ├── style.css        # 🎨 Estilos responsivos
    └── script.js        # ⚡ Lógica JavaScript
```

## 🔧 Configuração Avançada

### Email SMTP

Para usar envio real de emails, configure o arquivo `.env`:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=seu_email@gmail.com
SENDER_PASSWORD=sua_senha_de_app
```

**⚠️ Importante para Gmail:**
- Use uma "Senha de App" em vez da senha normal
- Gere em: [Google App Passwords](https://myaccount.google.com/apppasswords)
- Ative a verificação em 2 etapas

### Banco de Dados

O app usa SQLite por padrão (`tasks.db`). Para usar PostgreSQL:

1. Instale: `pip install psycopg2-binary`
2. Modifique `DATABASE_URL` em `database.py`
3. Configure variáveis de ambiente para conexão

## 🔍 API Python

### Funções Expostas ao JavaScript

```python
@eel.expose
def py_add_task(title, due_date=None)    # Adicionar tarefa
def py_get_tasks()                       # Listar tarefas
def py_toggle_task(task_id)              # Alternar status
def py_delete_task(task_id)              # Excluir tarefa
def py_send_reminder(email)              # Enviar lembrete
```

### Uso no JavaScript

```javascript
// Adicionar nova tarefa
const task = await eel.py_add_task("Minha tarefa", "2025-11-03")();

// Obter todas as tarefas
const tasks = await eel.py_get_tasks()();

// Enviar lembrete
const result = await eel.py_send_reminder("email@exemplo.com")();
```

## 🎯 Funcionalidades Futuras

- [ ] 🌙 Modo escuro
- [ ] 📊 Dashboard com estatísticas
- [ ] 🔔 Notificações desktop
- [ ] 📱 Export para mobile (Cordova/Electron)
- [ ] 🔄 Sincronização com cloud
- [ ] 👥 Colaboração em equipe
- [ ] 📈 Relatórios de produtividade

## 🐛 Solução de Problemas

### Chrome não encontrado
```bash
# Erro: "Chrome not found"
# Solução: Instale Chrome ou use modo padrão
python main.py  # Tentará usar o navegador padrão
```

### Erro de permissão SQLite
```bash
# Erro: "database is locked"
# Solução: Feche outras instâncias da app
pkill python  # Linux/Mac
taskkill /f /im python.exe  # Windows
```

### SMTP não funciona
```bash
# Verifique as credenciais no .env
# Use senha de app para Gmail
# Teste com: python email_sender.py
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Adicionar nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📜 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Seu Nome**
- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [Seu Perfil](https://linkedin.com/in/seu-perfil)
- Email: seu.email@exemplo.com

---

### 💡 Sobre o Projeto

Este é um **projeto pessoal** desenvolvido para demonstrar:
- ✅ **Clean Code** e arquitetura limpa
- ✅ **Integração Full-Stack** (Python + Web)
- ✅ **Boas práticas** de desenvolvimento
- ✅ **Documentação profissional**
- ✅ **Interface moderna** e responsiva

Ideal para **portfólio**, **estudos** ou como **base** para projetos maiores.

### ⭐ Se este projeto te ajudou, considere dar uma estrela!

```bash
# Clone e teste você mesmo!
git clone https://github.com/seu-usuario/eel-task-app.git
cd eel-task-app
pip install -r requirements.txt
python main.py
```

---

**Feito com ❤️ e muito ☕ por [Seu Nome]**