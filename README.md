
# Gerenciador de Tarefas - API Back-end (Projeto Veloz)

Este repositório contém a API back-end para o projeto Gerenciador de Tarefas, desenvolvido como parte do desafio técnico "Projeto  Veloz".

A API foi construída seguindo as melhores práticas de arquitetura de software, focando em segurança, performance, escalabilidade e manutenibilidade. O ambiente é 100% containerizado com Docker, garantindo portabilidade e um setup de desenvolvimento rápido e consistente.

---

## ✅ Principais Funcionalidades

* **Gerenciamento Completo (CRUD):** Endpoints para criar, ler, atualizar e deletar Projetos, Tarefas e Usuários.
* **Autenticação Segura:** Sistema de autenticação baseado em `JSON Web Tokens` (JWT), garantindo que apenas usuários autenticados possam acessar os recursos.
* **Sistema de Permissões Robusto:** Lógica de negócio implementada para que um usuário só possa visualizar e interagir com os projetos e tarefas dos quais faz parte (permissões a nível de objeto).
* **Documentação Interativa:** A API é auto-documentada usando o padrão OpenAPI 3 (Swagger), fornecendo uma interface interativa para explorar e testar os endpoints.
* **Ambiente Dockerizado:** Toda a aplicação e seu banco de dados (PostgreSQL) são gerenciados pelo Docker Compose, simplificando a configuração e o deploy.
* **Testes Automatizados:** Suíte de testes com `pytest` para garantir a confiabilidade e a estabilidade da API.
* **Configuração Segura:** Utiliza variáveis de ambiente (`.env`) para gerenciar segredos e configurações sensíveis.

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
| **PostgreSQL** | Banco de dados relacional |
| **Docker & Docker Compose**| Ferramentas para containerização e orquestração do ambiente |
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

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd gerenciador-tarefas-backend
    ```

2.  **Crie o arquivo de ambiente:**
    Nós utilizamos um arquivo `.env.example` como template. Copie-o para criar seu arquivo `.env` local.
    ```bash
    cp .env.example .env
    ```

3.  **Gere uma `SECRET_KEY`:**
    O arquivo `.env` precisa de uma `SECRET_KEY` única. Execute o comando abaixo para gerar uma chave segura e cole-a no seu arquivo `.env`.
    ```bash
    docker-compose run --rm backend python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```
    *Abra o arquivo `.env` e cole a chave gerada na variável `SECRET_KEY`.*

4.  **Construa e suba os contêineres:**
    Este comando irá construir a imagem do Django, baixar a imagem do Postgres e iniciar os serviços.
    ```bash
    docker-compose up --build -d
    ```
    *(A flag `-d` executa os contêineres em segundo plano).*

5.  **Crie um superusuário:**
    Para acessar a área administrativa do Django, você precisa de um usuário.
    ```bash
    docker-compose exec backend python manage.py createsuperuser
    ```
    *Siga as instruções para criar seu usuário e senha.*

✅ **Pronto!** A API estará rodando e acessível em `http://localhost:8000/`.

---

## 🧪 Rodando os Testes

Para garantir que tudo está funcionando como esperado, execute a suíte de testes automatizados:
```bash
docker-compose exec backend pytest
```

## 🏗️ Estrutura do Projeto

* **`core/`**: Contém as configurações globais do projeto Django (`settings.py`, `urls.py` principal).
* **`app/`**: É a nossa aplicação principal, contendo os modelos (`models.py`), as regras da API (`views.py`, `serializers.py`), testes e outras lógicas de negócio do gerenciador de tarefas.
