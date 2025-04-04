import flet as ft

ARQUIVO_DESPESAS = "despesas.txt"

def adicionar_despesa(nome, valor): 
    with open(ARQUIVO_DESPESAS, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{nome},{valor}\n") 

def listar_despesas(): 
    despesas = [] 
    try:
        with open(ARQUIVO_DESPESAS, "r", encoding="utf-8") as arquivo: 
            for linha in arquivo:
                nome, valor = linha.strip().split(",")
                despesas.append((nome, float(valor)))
    except FileNotFoundError:
        return []
    return despesas

def excluir_despesa(nome, valor):
    despesas = listar_despesas()
    despesas = [d for d in despesas if not (d[0] == nome and d[1] == valor)]
    with open(ARQUIVO_DESPESAS, "w", encoding="utf-8") as arquivo:
        for nome_d, valor_d in despesas:
            arquivo.write(f"{nome_d},{valor_d}\n")

def calcular_total():
    despesas = listar_despesas()
    return sum(valor for _, valor in despesas)

def main(page: ft.Page):
    page.title = "Calculadora de Despesas Pessoais"
    page.window_width = 600
    page.window_height = 400
    page.padding = 20

    nome_input = ft.TextField(label="Nome da Despesa", width=200)
    valor_input = ft.TextField(label="Valor (R$)", width=100, keyboard_type=ft.KeyboardType.NUMBER)

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Valor (R$)")),
            ft.DataColumn(ft.Text("Ação")),  
        ],
        rows=[],
    )

    
    tabela_container = ft.Column(
        controls=[tabela],
        height=250,  
        width=560,   
        scroll=ft.ScrollMode.AUTO,  
    )

    total_label = ft.Text("Total: R$0.00", size=20)

    def atualizar_interface():
        despesas = listar_despesas()
        tabela.rows.clear()
        for nome, valor in despesas:
            tabela.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(nome)),
                    ft.DataCell(ft.Text(f"{valor:.2f}")),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            tooltip="Excluir",
                            on_click=lambda e, n=nome, v=valor: excluir_e_atualizar(n, v)
                        )
                    ),
                ])
            )
        total = calcular_total()
        total_label.value = f"Total: R${total:.2f}"
        page.update()

    def excluir_e_atualizar(nome, valor):
        excluir_despesa(nome, valor)
        atualizar_interface()
        page.snack_bar = ft.SnackBar(ft.Text(f"Despesa '{nome}' excluída!"), open=True)
        page.update()

    def adicionar_clicked(e):
        nome = nome_input.value.strip()
        valor = valor_input.value.strip()
        if nome and valor:
            try:
                valor_float = float(valor)
                adicionar_despesa(nome, valor_float)
                nome_input.value = ""
                valor_input.value = ""
                atualizar_interface()
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("Valor inválido! Use números."), open=True)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos!"), open=True)
        page.update()

    adicionar_btn = ft.ElevatedButton("Adicionar Despesa", on_click=adicionar_clicked)

    page.add(
        ft.Row([nome_input, valor_input, adicionar_btn], alignment=ft.MainAxisAlignment.START),
        tabela_container,  
        total_label,
    )

    atualizar_interface()


