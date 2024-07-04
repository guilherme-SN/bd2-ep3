
from dao.consulta_dao import ConsultaDAO
from services.consulta_service import ConsultaService
from database.database_init import create_database_if_not_exists


def main():
    create_database_if_not_exists()

    consulta_service = ConsultaService(ConsultaDAO())

    print("\n########## BEM VINDO AO SISTEMA ##########")

    consulta_service.menu()

    print("\n##########  PROGRAMA ENCERRADO  ##########")


if __name__ == '__main__':
    main()

