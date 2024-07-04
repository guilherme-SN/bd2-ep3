
## Estrutura do EP
- `dao/`: Scripts para acesso e manipulação dos dados das consultas no banco de dados.
- `dto/`: Define os objetos de transferência de dados (DTO) para representar as consultas.
- `services/`: Lógica de negócio e serviços oferecidos pela aplicação.
- `database/`: Scripts para relacionados à conexão com o banco de dados e inicialização do mesmo.
- `main.py`: Script principal.

## Instalação

1. Clone o repositório.
    ```bash
    git clone https://github.com/guilherme-SN/bd2-ep3.git
    ```

2. Instale as dependências:
    ```bash
    pip3 install -r requirements.txt
    ```
3. É necessário configurar o banco de dados MySQL e os parâmetros específicos no arquivo database/connection.py

## Uso

Execute o script principal:
```bash
python3 main.py
```
