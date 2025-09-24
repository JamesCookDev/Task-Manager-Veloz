# Gerenciador de Tarefas - API Back-end (Projeto Veloz)

Este repositório contém a API back-end para o projeto Gerenciador de Tarefas. Ele serve como o **serviço central (Core API)** em uma arquitetura de microsserviços, sendo a fonte da verdade para todos os dados e lógica de negócios.

A API foi construída seguindo as melhores práticas de arquitetura de software, focando em segurança, performance, escalabilidade e manutenibilidade. O ambiente é 100% containerizado com Docker, garantindo portabilidade e um setup de desenvolvimento rápido e consistente.

---

## 🏗️ Arquitetura do Sistema

Este projeto faz parte de um ecossistema multi-repositório:
1.  **Back-end (Este Repositório):** API robusta em Django/DRF, responsável pela lógica de negócios e persistência de dados.
2.  **BFF (Backend for Frontend):** Serviço intermediário em Go, otimizado para agregar e formatar dados para o cliente.
3.  **Front-end:** Interface de usuário em React.

Este serviço (`backend`) foi projetado para ser consumido exclusivamente pelo BFF, que atua como uma camada de segurança e otimização.

---

## ✅ Principais Funcionalidades

* **Gerenciamento Completo (CRUD):** Endpoints para criar, ler, atualizar e deletar Projetos, Tarefas e Usuários.
* **Autenticação Segura:** Sistema de autenticação baseado em `JSON Web Tokens` (JWT).
* **Sistema de Permissões Robusto:** Lógica de negócio que garante que um usuário só possa interagir com os projetos e tarefas dos quais faz parte.
* **Interface Administrativa Moderna:** Painel de administração customizado com `Django Jazzmin` para uma melhor experiência de usuário, incluindo temas, busca global e layout responsivo.
* **Documentação Interativa:** API auto-documentada com o padrão OpenAPI 3 (Swagger UI e ReDoc).
* **Ambiente Dockerizado:** Aplicação e banco de dados (PostgreSQL) gerenciados pelo Docker Compose.
* **Testes Automatizados:** Suíte de testes com `pytest` para garantir a confiabilidade da API.
* **Configuração Segura:** Utiliza variáveis de ambiente (`.env`) para gerenciar segredos.

---

## 📖 Documentação da API

Com a aplicação rodando, a documentação interativa da API pode ser acessada nos seguintes endpoints:

* **Swagger UI:** [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
* **ReDoc:** [http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Propósito |
| :--- | :--- |
| **Python** | Linguagem de programação principal |
| **Django** | Framework web para a construção da API |
| **Django REST Framework** | Toolkit para construir APIs RESTful robustas |
| **Django Jazzmin** | Tema moderno para a interface de administração |
| **PostgreSQL** | Banco de dados relacional |
| **Docker & Docker Compose**| Ferramentas para containerização e orquestração |
| **JWT (Simple JWT)**| Padrão para autenticação baseada em tokens |
| **drf-spectacular** | Geração automática de documentação OpenAPI/Swagger |
| **pytest-django** | Framework para a execução dos testes automatizados |
| **python-dotenv** | Gerenciamento de variáveis de ambiente |

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e executar o ambiente de desenvolvimento.

### Pré-requisitos

* [Git](https://git-scm.com/)
* [Docker](https://www.docker.com/products/docker-desktop/)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Passos de Instalação

1.  **Clone o repositório principal e navegue até a pasta do back-end:**
    ```bash
    git clone [https://github.com/JamesCookDev/Task-Manager-Veloz.git](https://github.com/JamesCookDev/Task-Manager-Veloz.git)
    cd Task-Manager-Veloz/gerenciador-tarefas-backend
    ```

2.  **Crie o arquivo de ambiente:**
    Copie o template `.env.example` para criar seu arquivo `.env` local.
    ```bash
    cp .env.example .env
    ```

3.  **Gere uma `SECRET_KEY`:**
    O arquivo `.env` precisa de uma `SECRET_KEY` única. Execute o comando abaixo e cole a chave gerada no seu arquivo `.env`.
    ```bash
    docker compose run --rm backend python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```

4.  **Construa e suba os contêineres:**
    Este comando irá construir as imagens e iniciar todos os serviços definidos no `docker-compose.yml` (backend, bff, db).
    ```bash
    docker compose up --build -d
    ```
    *(A flag `-d` executa os contêineres em segundo plano).*

5.  **Crie um superusuário:**
    Para acessar a área administrativa, você precisa de um usuário.
    ```bash
    docker 
    compose exec backend python manage.py createsuperuser
    ```
    *Siga as instruções para criar seu usuário e senha.*
    
6.  **Colete os arquivos estáticos:**
    Este passo é necessário para que o tema do Django Jazzmin seja carregado corretamente.
    ```bash
    docker compose exec backend python manage.py collectstatic --noinput
    ```

✅ **Pronto!** A API estará rodando em `http://localhost:8000/` e a interface administrativa em `http://localhost:8000/admin/`.

---

## 🧪 Rodando os Testes

Para garantir que tudo está funcionando como esperado, execute a suíte de testes automatizados:
```bash
docker compose exec backend pytest
```