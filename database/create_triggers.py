
from database.connection import get_connection


def create_triggers():
    triggers = [
        """
        CREATE TRIGGER verifica_horario_medico BEFORE INSERT ON Consulta
        FOR EACH ROW
        BEGIN
            DECLARE conflito INT;
            SELECT COUNT(*)
            INTO conflito
            FROM Consulta
            WHERE CRM = NEW.CRM
            AND Data = NEW.Data
            AND ((NEW.HoraFim >= HoraInicio AND NEW.HoraInicio <= HoraFim)
                OR (NEW.HoraInicio <= HoraInicio AND NEW.HoraFim > HoraInicio)
            );                
            IF conflito > 0 THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'O médico já possui uma consulta marcada neste horário.';
            END IF;
        END;
        """,
        """
        CREATE TRIGGER verifica_horario_paciente BEFORE INSERT ON Consulta
        FOR EACH ROW
        BEGIN
            DECLARE conflito INT;    
            SELECT COUNT(*)
            INTO conflito
            FROM Consulta
            WHERE IdPaciente = NEW.IdPaciente
            AND Data = NEW.Data
            AND (
                (NEW.HoraFim >= HoraInicio AND NEW.HoraInicio <= HoraFim)  -- overlapping 
                OR (NEW.HoraInicio <= HoraInicio AND NEW.HoraFim > HoraInicio)  -- overlapping parcial
            );
            
            IF conflito > 0 THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'O paciente já possui uma consulta marcada neste horário.';
            END IF;
        END;
        """
    ]

    connection = get_connection()
    cursor = connection.cursor()

    for trigger in triggers:
        try:
            cursor.execute(trigger)
            print("Trigger criado com sucesso.")
        except Exception as e:
            print(f"Erro ao criar o trigger: {e}")

    cursor.close()
    connection.close()

