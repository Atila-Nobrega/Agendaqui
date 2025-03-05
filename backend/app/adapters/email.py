import os
from string import Template

def gerar_email_agendamento(nome_usuario, nome_servico, status_agendamento, data_horario, nome_prestador):
    """
    Preenche o template HTML com os dados do agendamento.
    """
    template_path = os.path.join(os.path.dirname(__file__), "..", "templates", "email_template.html")

    with open(template_path, "r", encoding="utf-8") as file:
        template = Template(file.read())  # ✅ Usa Template do string
    
    return template.safe_substitute(
        nome_usuario=nome_usuario,
        nome_servico=nome_servico,
        status_agendamento=status_agendamento,
        data_horario=data_horario,
        nome_prestador=nome_prestador
    )