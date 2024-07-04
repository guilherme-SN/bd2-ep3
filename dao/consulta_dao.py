
from mysql.connector import Error
from database.connection import get_connection, close_connection 

class ConsultaDAO:

    def get_all(self):
        data = []

        try:
            connection = get_connection()
            if connection.is_connected():
                cursor = connection.cursor()

                query = f"SELECT * FROM Consulta"
                cursor.execute(query)

                data = cursor.fetchall()

                close_connection(connection, cursor)

                return data

        except (Exception, Error) as error:
            print(f"\nError while fetching data from MySQL: \n {error}")


    def get_by_id(self, id_consulta):
        data = []

        try:
            connection = get_connection()
            if connection.is_connected():
                cursor = connection.cursor()

                query = f"SELECT * FROM Consulta WHERE IdConsulta = %s"
                condition = (id_consulta, )

                cursor.execute(query, condition)

                data = cursor.fetchall()

                close_connection(connection, cursor)

                return data

        except (Exception, Error) as error:
            print(f"\nError while fetching data from MySQL: \n {error}")


    def insert(self, consulta_dto):
        try:
            connection = get_connection()
            if connection.is_connected():
                cursor = connection.cursor()

                query = f"""INSERT INTO Consulta (CRM, IdEspecialidade, IdPaciente, Data, HoraInicio, HoraFim, Pagou, ValorPago, FormaPagamento) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                record = (consulta_dto.crm,
                          consulta_dto.id_especialidade,
                          consulta_dto.id_paciente,
                          consulta_dto.data,
                          consulta_dto.hora_inicio,
                          consulta_dto.hora_fim,
                          consulta_dto.pagou,
                          consulta_dto.valor_pago,
                          consulta_dto.forma_pagamento
                          )

                cursor.execute(query, record)

                connection.commit()

                count = cursor.rowcount
                print(f"\n{count} Record inserted successfully into Consulta table")

                close_connection(connection, cursor)

        except (Exception, Error) as error:
            print(f"\nFailed to insert record into Consulta table: \n {error}")


    def delete(self, id_consulta):
        try:
            connection = get_connection()
            if connection.is_connected():
                cursor = connection.cursor()

                query = f"DELETE FROM Consulta WHERE IdConsulta = %s"
                condition = (id_consulta, )

                cursor.execute(query, condition)

                connection.commit()

                count = cursor.rowcount
                print(f"\n{count} Record deleted successfully from Consulta table")

                close_connection(connection, cursor)

        except (Exception, Error) as error:
            print(f"\nFailed to delete record from Consulta table: \n {error}")


    def update(self, consulta_dto, id_consulta):
        try:
            connection = get_connection()
            if connection.is_connected():
                cursor = connection.cursor()

                query = f"""UPDATE Consulta 
                            SET CRM = %s, IdEspecialidade = %s, IdPaciente = %s, 
                                Data = %s, HoraInicio = %s, HoraFim = %s, Pagou = %s, 
                                ValorPago = %s, FormaPagamento = %s
                            WHERE IdConsulta = %s"""
                record = (consulta_dto.crm,
                          consulta_dto.id_especialidade,
                          consulta_dto.id_paciente,
                          consulta_dto.data,
                          consulta_dto.hora_inicio,
                          consulta_dto.hora_fim,
                          consulta_dto.pagou,
                          consulta_dto.valor_pago,
                          consulta_dto.forma_pagamento,
                          id_consulta
                          )

                cursor.execute(query, record)

                connection.commit()

                print(f"\nRecord updated successfully in Consulta table")
                
                close_connection(connection, cursor)

        except (Exception, Error) as error:
            print(f"\nFailed to update record in Consulta table: \n {error}")

