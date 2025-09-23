# ⚡ Sinergia  

> Registro de atendimentos das equipes de campo da **CEEE Equatorial** no processo de recuperação de energia.  

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)  
![Django](https://img.shields.io/badge/Django-5.0-success.svg)  
![Status](https://img.shields.io/badge/Status-Online-brightgreen.svg)  

---

## 🎯 Objetivo  
O **Sinergia** foi desenvolvido para auxiliar o time de atendimento da CEEE Equatorial no gerenciamento e registro dos atendimentos realizados pelas equipes de campo.  

Ele organiza os registros por **regionais (Norte e Sul)** e permite análises rápidas via exportação para Excel.  

---

## 🚀 Funcionalidades  

- 👥 **Gestão de Usuários** – Com separação por regionais **Norte** e **Sul**  
- 👷 **Cadastro de Equipes** – Criação e gerenciamento de equipes de campo  
- 📝 **Registro de Atendimentos** – Salvando informações com tipos e detalhes do atendimento  
- 🏷️ **Tipos de Atendimento** – Configuráveis de acordo com a operação  
- 📊 **Exportação em Excel** – Para facilitar análises de desempenho e relatórios  
- 🎨 **Interface Moderna** com [Jazzmin](https://github.com/farridav/django-jazzmin)  

---

## 🛠️ Tecnologias  

- [Python](https://www.python.org/)  
- [Django](https://www.djangoproject.com/)  
- [SQLite](https://www.sqlite.org/index.html)  
- [Jazzmin](https://github.com/farridav/django-jazzmin) (Admin moderno)  
- Deploy na [PythonAnywhere](https://www.pythonanywhere.com/)  

---

## 🗂️ Estrutura geral do projeto  

```
Sinergia/
├── core/                 # Configurações principais do Django
├── register/             # App responsável por usuários, equipes e registros
├── static/               # Arquivos estáticos da aplicação
├── staticfiles/          # Pasta coletada (collectstatic)
├── manage.py
└── requirements.txt
```

---

## 💻 Como rodar localmente  

1. Clone o repositório  
   ```bash
   git clone https://github.com/romulobarreto/Sinergia.git
   cd Sinergia
   ```

2. Crie e ative um ambiente virtual  
   ```bash
   python -m venv venv
   source venv/bin/activate  # (Linux/Mac)
   venv\Scripts\activate     # (Windows)
   ```

3. Instale as dependências  
   ```bash
   pip install -r requirements.txt
   ```

4. Execute as migrações  
   ```bash
   python manage.py migrate
   ```

5. Crie um superusuário  
   ```bash
   python manage.py createsuperuser
   ```

6. Rode o servidor  
   ```bash
   python manage.py runserver
   ```

Acesse em: http://127.0.0.1:8000/admin/ 🎉  

---

## 🌐 Deploy  

Este projeto está implantado em produção em:  
👉 **[sinergia.pythonanywhere.com](https://sinergia.pythonanywhere.com/)**  

---

## 🤝 Contribuição  

1. Faça um fork 🍴  
2. Crie sua feature branch (`git checkout -b feature/minha-feature`)  
3. Commit suas alterações (`git commit -m 'feat: minha nova feature'`)  
4. Push para a branch (`git push origin feature/minha-feature`)  
5. Abra um Pull Request 🚀  

---

## 👨‍💻 Autor  

Feito por **Rômulo Barreto** ✨  
