
class ConsultaDTO:

    def __init__(self, crm, id_especialidade, id_paciente, data, hora_inicio,
                 hora_fim, pagou, valor_pago, forma_pagamento):

        self.crm = crm
        self.id_especialidade = id_especialidade
        self.id_paciente = id_paciente
        self.data = data
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.pagou = pagou
        self.valor_pago = valor_pago
        self.forma_pagamento = forma_pagamento

