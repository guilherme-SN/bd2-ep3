
import mysql.connector
from mysql.connector import Error
from database.connection import get_connection, close_connection 
from database.create_triggers import create_triggers


def create_database_if_not_exists():
    try:
        temp_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"
        )

        if temp_connection.is_connected():
            cursor = temp_connection.cursor()
            cursor.execute("SHOW DATABASES LIKE 'clinica_medica'")
            result = cursor.fetchone()

            if not result:
                cursor.execute("CREATE DATABASE clinica_medica")
                print("Banco de dados 'clinica_medica' criado com sucesso.")

                create_tables()
                create_triggers()
                populate_tables()
                
            cursor.close()
            temp_connection.close()

    except Error as e:
        print(f"Erro ao verificar/criar o banco de dados: {e}")


def create_tables():
    try:
        connection = get_connection()
        if connection.is_connected():
            cursor = connection.cursor()

            create_tables_query = [
                """
                CREATE TABLE IF NOT EXISTS Medico
                (
                	CRM INT NOT NULL,
                	NomeMedico VARCHAR(60) NOT NULL,
                	TelefoneMedico VARCHAR(15),
                	Percentual FLOAT,
                
                	PRIMARY KEY (CRM)
                );
                """,

                """
                CREATE TABLE IF NOT EXISTS Agenda
                (
                 	IdAgenda INT AUTO_INCREMENT PRIMARY KEY,
                DiaSemana VARCHAR(20) NOT NULL,
                HoraInicio TIME NOT NULL,
                HoraFim TIME,
                CRM INT NOT NULL,
                
                	FOREIGN KEY (CRM) REFERENCES Medico(CRM) ON UPDATE CASCADE ON DELETE CASCADE
                );
                """,

                """
                CREATE TABLE IF NOT EXISTS Especialidade
                (
                	IdEspecialidade INT AUTO_INCREMENT PRIMARY KEY,
                	NomeEspecialidade VARCHAR(50) NOT NULL,
                	Indice FLOAT NOT NULL
                );
                """,
                
                """
                CREATE TABLE IF NOT EXISTS ExerceEspecialidade
                (
                	CRM INT NOT NULL,
                	IdEspecialidade INT NOT NULL,
                	
                	PRIMARY KEY (CRM, IdEspecialidade),
                	FOREIGN KEY (CRM) REFERENCES Medico(CRM) ON UPDATE CASCADE ON DELETE CASCADE,
                	FOREIGN KEY (IdEspecialidade) REFERENCES Especialidade(IdEspecialidade) ON UPDATE CASCADE ON DELETE CASCADE
                );
                """,

                """
                CREATE TABLE IF NOT EXISTS Paciente
                (
                    IdPaciente INT AUTO_INCREMENT PRIMARY KEY,
                    CPF BIGINT NOT NULL UNIQUE,
                    NomePaciente VARCHAR(60) NOT NULL,
                    TelefonePaciente VARCHAR(15),
                    Endereco VARCHAR(255) NOT NULL,
                    Idade INT NOT NULL,
                    Sexo VARCHAR(15) NOT NULL
                );
                """,

                """
                CREATE TABLE IF NOT EXISTS Consulta
                (
                	IdConsulta INT AUTO_INCREMENT PRIMARY KEY,
                	CRM INT NOT NULL,
                	IdEspecialidade INT NOT NULL,
                	IdPaciente INT NOT NULL,
                	Data DATE NOT NULL,
                	HoraInicio TIME NOT NULL,
                	HoraFim TIME NOT NULL,
                	Pagou INT NOT NULL,
                	ValorPago FLOAT DEFAULT 0,
                	FormaPagamento VARCHAR(20) NOT NULL,
                
                    FOREIGN KEY (CRM) REFERENCES Medico(CRM) ON UPDATE CASCADE ON DELETE CASCADE,
                    FOREIGN KEY (IdEspecialidade) REFERENCES Especialidade(IdEspecialidade) ON UPDATE CASCADE ON DELETE CASCADE,
                	FOREIGN KEY (IdPaciente) REFERENCES Paciente(IdPaciente) ON UPDATE CASCADE ON DELETE CASCADE,
                
                	CONSTRAINT cPagou CHECK (Pagou = 0 OR Pagou = 1)
                );
                """,
                
                """
                CREATE TABLE IF NOT EXISTS Diagnostico
                (
                	IdDiagnostico INT AUTO_INCREMENT PRIMARY KEY,
                	TratamentoRecomendado VARCHAR(300),
                	RemedioReceitados VARCHAR(300),
                	Observacoes VARCHAR(300),
                	IdConsulta INT NOT NULL,
                
                	FOREIGN KEY (IdConsulta) REFERENCES Consulta(IdConsulta) ON UPDATE CASCADE ON DELETE CASCADE
                );
                """,

                """
                CREATE TABLE IF NOT EXISTS Doenca
                (
                	IdDoenca INT AUTO_INCREMENT PRIMARY KEY,
                	NomeDoenca VARCHAR(255)
                );
                """,

                """
                CREATE TABLE IF NOT EXISTS Diagnostica
                (
                	IdDiagnostico INT NOT NULL,
                	IdDoenca INT NOT NULL,
                
                	PRIMARY KEY (IdDiagnostico, IdDoenca),
                    FOREIGN KEY (IdDiagnostico) REFERENCES Diagnostico(IdDiagnostico) ON UPDATE CASCADE ON DELETE CASCADE,
                    FOREIGN KEY (IdDoenca) REFERENCES Doenca(IdDoenca) ON UPDATE CASCADE ON DELETE CASCADE
                );
                """
            ]

            for query in create_tables_query:
                cursor.execute(query)

            connection.commit()

            print("Tabelas criadas com sucesso")

            close_connection(connection, cursor)

    except Error as e:
        print(f"Erro ao criar as tabelas: {e}")


def populate_tables():
    try:
        connection = get_connection()
        if connection.is_connected():
            cursor = connection.cursor()

            inserts_query = [
                """
                INSERT INTO Medico (CRM, NomeMedico, TelefoneMedico, Percentual) VALUES
                (12345, 'Dr. João Silva', '(11) 9999-8888', 70.5),
                (23456, 'Dra. Maria Oliveira', '(21) 9876-5432', 65.0),
                (34567, 'Dr. Pedro Santos', '(31) 8765-4321', 75.0),
                (45678, 'Dr. Carlos Oliveira', '(41) 1111-2222', 60.0),
                (56789, 'Dra. Fernanda Santos', '(51) 3333-4444', 70.0),
                (67890, 'Dr. Marcos Silva', '(61) 5555-6666', 65.0),
                (00001, 'Dr. House', '(61) 5345-6866', 85.0),
                (99999, 'Dr. Kildare', '(71) 6666-7777', 75.0);
                """,
                
                """
                INSERT INTO Agenda (DiaSemana, HoraInicio, HoraFim, CRM) VALUES
                ('Segunda-feira', '08:00:00', '12:00:00', 12345),
                ('Terça-feira', '09:00:00', '13:00:00', 23456),
                ('Quarta-feira', '10:00:00', '14:00:00', 34567),
                ('Quinta-feira', '08:00:00', '12:00:00', 45678),
                ('Sexta-feira', '09:00:00', '13:00:00', 56789),
                ('Sábado', '10:00:00', '14:00:00', 67890),
                ('Domingo', '10:00:00', '14:00:00', 67890),
                ('Segunda-feira', '10:00:00', '14:00:00', 67890),
                ('Terça-feira', '10:00:00', '14:00:00', 67890),
                ('Quarta-feira', '10:00:00', '14:00:00', 67890),
                ('Quinta-feira', '12:00:00', '16:00:00', 67890),
                ('Sexta-feira', '12:00:00', '16:00:00', 67890);
                """,
                
                """
                INSERT INTO Especialidade (NomeEspecialidade, Indice) VALUES
                ('Cardiologia', 0.8),
                ('Pediatria', 0.9),
                ('Ortopedia', 0.7),
                ('Dermatologia', 0.75),
                ('Ginecologia', 0.85),
                ('Neurologia', 0.8);
                """,
                
                """
                INSERT INTO ExerceEspecialidade (CRM, IdEspecialidade) VALUES
                (12345, 1),
                (23456, 2),
                (34567, 3),
                (45678, 4),
                (56789, 5),
                (67890, 6),
                (99999, 1),
                (99999, 2),
                (99999, 3),
                (99999, 4),
                (99999, 5),
                (00001, 1),
                (00001, 4),
                (99999, 6);
                """,
                
                """
                INSERT INTO Paciente (CPF, NomePaciente, TelefonePaciente, Endereco, Idade, Sexo) VALUES
                (12345678900, 'Ana Souza', '(11) 1234-5678', 'Rua A, 123', 35, 'Feminino'),
                (98765432100, 'José Silva', '(21) 9876-5432', 'Rua B, 456', 45, 'Masculino'),
                (65432198700, 'Maria Santos', '(31) 8765-4321', 'Rua C, 789', 28, 'Feminino'),
                (78901234500, 'Paula Oliveira', '(41) 7777-8888', 'Av. X, 789', 30, 'Feminino'),
                (89012345600, 'Fábio Santos', '(51) 9999-0000', 'Rua Y, 123', 50, 'Masculino'),
                (90123456700, 'Diego Pituca', '(61) 1111-2222', 'Rua Z, 456', 40, 'Masculino');
                """,
                
                """
                INSERT INTO Consulta (CRM, IdEspecialidade, IdPaciente, Data, HoraInicio, HoraFim, Pagou, ValorPago, FormaPagamento) VALUES
                (12345, 1, 1, '2024-05-05', '09:00:00', '10:00:00', 1, 100.00, 'Dinheiro'),
                (23456, 2, 2, '2024-05-06', '10:00:00', '11:00:00', 1, 120.00, 'Cartão'),
                (34567, 3, 3, '2024-05-07', '11:00:00', '12:00:00', 0, 0.00, 'N/A'),
                (45678, 4, 4, '2024-05-08', '09:00:00', '10:00:00', 1, 150.00, 'Cartão'),
                (56789, 5, 5, '2024-05-09', '10:00:00', '11:00:00', 0, 0.00, 'N/A'),
                (67890, 6, 6, '2024-05-10', '11:00:00', '12:00:00', 1, 200.00, 'Dinheiro'),
                (12345, 1, 1, '2024-01-01', '08:00:00', '08:30:00', 1, 100.00, 'Dinheiro'),
                (23456, 2, 2, '2024-01-15', '09:00:00', '09:30:00', 1, 120.00, 'Cartão'),
                (34567, 3, 3, '2024-01-20', '10:00:00', '10:30:00', 0, 0.00, 'N/A'),
                (00001, 1, 6, '2024-03-01', '08:00:00', '09:00:00', 1, 100.00, 'Dinheiro'),
                (00001, 4, 6, '2024-05-10', '14:00:00', '15:00:00', 1, 550.00, 'Dinheiro');
                """,
                
                """
                INSERT INTO Diagnostico (TratamentoRecomendado, RemedioReceitados, Observacoes, IdConsulta) VALUES
                ('Repouso e medicamento X', 'Remédio A, Remédio B', 'Nenhuma observação', 1),
                ('Fisioterapia', 'Remédio C', 'Paciente respondeu bem ao tratamento', 2),
                ('Cirurgia', 'Remédio D', 'Necessário agendar cirurgia com urgência', 3),
                ('Cirurgia plástica', 'N/A', 'Paciente deseja realizar procedimento estético', 4),
                ('Repouso', 'Remédio E', 'Paciente está com gripe', 5),
                ('Fisioterapia intensiva', 'Remédio F', 'Paciente sofreu acidente de carro', 6);
                """,
                
                """
                INSERT INTO Doenca (NomeDoenca) VALUES
                ('Hipertensão'),
                ('Febre'),
                ('Fratura'),
                ('Acne'),
                ('Gripe'),
                ('Traumatismo');
                """,
                
                """
                INSERT INTO Diagnostica (IdDiagnostico, IdDoenca) VALUES
                (1, 1),
                (2, 2),
                (3, 3),
                (4, 4),
                (5, 5),
                (6, 6);
                """
            ]

            for query in inserts_query:
                cursor.execute(query)

            connection.commit()
            
            print("Tabelas populadas com sucesso")

            close_connection(connection, cursor)

    except Error as e:
        print(f"Erro ao criar as tabelas: {e}")

