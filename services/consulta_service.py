
from dao.consulta_dao import ConsultaDAO
from dto.consulta_dto import ConsultaDTO


class ConsultaService:

    def __init__(self, consulta_dao: ConsultaDAO):
        self.consulta_dao = consulta_dao


    def menu(self):
        while True:
            print("\nQual ação você quer executar?")
            print("0 - Sair")
            print("1 - Cadastrar nova consulta")
            print("2 - Atualizar uma consulta")
            print("3 - Deletar uma consulta")
            print("4 - Visualizar todas consultas")
            print("5 - Visualizar uma consulta\n")

            try:
                opcao = int(input("> "))
                print("")
            except ValueError:
                print("Por favor, digite um número válido.\n")
                continue

            if opcao == 0:
                break
            elif opcao == 1:
                self.cadastrar()
            elif opcao == 2:
                self.atualizar()
            elif opcao == 3:
                self.deletar()
            elif opcao == 4:
                self.visualizar()
            elif opcao == 5:
                self.visualizar_consulta()
            else:
                print("Opção inválida!\n")


    def cadastrar(self):
        crm = input("CRM: ")
        id_especialidade = int(input("ID da Especialidade: "))
        id_paciente = int(input("ID do Paciente: "))
        data = input("Data (AAAA-MM-DD): ")
        hora_inicio = input("Horário de inicio da consulta: ")
        hora_fim = input("Horário do fim da consulta: ")
        pagou = int(input("Pagou? (0 - Não | 1 - Sim): "))
        valor_pago = float(input("Valor pago: R$"))
        forma_pagamento = input("Forma de pagamento: ")

        consulta_dto = ConsultaDTO(crm, id_especialidade, id_paciente, data,
                                   hora_inicio, hora_fim, pagou, valor_pago,
                                   forma_pagamento)

        self.consulta_dao.insert(consulta_dto)


    def atualizar(self):
        id_consulta = int(input("ID da consulta a ser atualizada: "))

        consulta = self.consulta_dao.get_by_id(id_consulta)

        if not consulta:
            print(f"Não há consultas com ID = {id_consulta}")

        else:
            crm = input("Novo CRM: ")
            id_especialidade = int(input("Novo ID da Especialidade: "))
            id_paciente = int(input("Novo ID do Paciente: "))
            data = input("Nova Data (AAAA-MM-DD): ")
            hora_inicio = input("Novo Horário de inicio da consulta: ")
            hora_fim = input("Novo Horário do fim da consulta: ")
            pagou = int(input("Pagou? (0 - Não | 1 - Sim): "))
            valor_pago = float(input("Novo Valor pago: R$"))
            forma_pagamento = input("Nova Forma de pagamento: ")
            
            consulta_dto = ConsultaDTO(crm, id_especialidade, id_paciente, data,
                                       hora_inicio, hora_fim, pagou, valor_pago,
                                       forma_pagamento)

            self.consulta_dao.update(consulta_dto, id_consulta)


    def deletar(self):
        id_consulta = int(input("ID da consulta a ser deletada: "))

        consulta = self.consulta_dao.get_by_id(id_consulta)

        if not consulta:
            print(f"Não há consultas com ID = {id_consulta}")

        else:
            self.consulta_dao.delete(id_consulta)


    def visualizar(self):
        
        consultas = self.consulta_dao.get_all()

        if not consultas:
            print("Não há consultas no banco de dados\n")

        else:
            for consulta in consultas:
                print(f"ID: {consulta[0]}")
                print(f"\tCRM: {consulta[1]}")
                print(f"\tIdEspecialidade: {consulta[2]}")
                print(f"\tIdPaciente: {consulta[3]}")
                print(f"\tData: {consulta[4]}")
                print(f"\tInício da consulta: {consulta[5]}")
                print(f"\tFim da consulta: {consulta[6]}")
                print(f"\tPagou? (0 - Não | 1 - Sim): {consulta[7]}")
                print(f"\tValor pago: R${consulta[8]}")
                print(f"\tForma de pagamento: {consulta[9]}")
                print("")


    def visualizar_consulta(self):

        id_consulta = int(input("ID da consulta a ser visualizada: "))

        consulta = self.consulta_dao.get_by_id(id_consulta)

        if not consulta:
            print(f"Não há consultas com ID = {id_consulta}")

        else:
            consulta = consulta[0]

            print(f"ID: {consulta[0]}")
            print(f"\tCRM: {consulta[1]}")
            print(f"\tIdEspecialidade: {consulta[2]}")
            print(f"\tIdPaciente: {consulta[3]}")
            print(f"\tData: {consulta[4]}")
            print(f"\tInício da consulta: {consulta[5]}")
            print(f"\tFim da consulta: {consulta[6]}")
            print(f"\tPagou? (0 - Não | 1 - Sim): {consulta[7]}")
            print(f"\tValor pago: R${consulta[8]}")
            print(f"\tForma de pagamento: {consulta[9]}")
            print("")

