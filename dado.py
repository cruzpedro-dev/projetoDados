import sqlite3

conexao = sqlite3.connect('estudio_tatuagem.db')
cursor = conexao.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Estilos_Arte (
    ID_Estilo INTEGER PRIMARY KEY,
    Nome_Estilo TEXT NOT NULL,
    Preco_Base REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Agendamentos (
    ID_Agendamento INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome_Cliente TEXT NOT NULL,
    Data_Sessao TEXT,
    ID_Estilo INTEGER,
    FOREIGN KEY (ID_Estilo) REFERENCES Estilos_Arte(ID_Estilo)
)
''')

cursor.execute("INSERT OR IGNORE INTO Estilos_Arte (ID_Estilo, Nome_Estilo, Preco_Base) VALUES (1, 'Old School', 350.00)")
cursor.execute("INSERT OR IGNORE INTO Estilos_Arte (ID_Estilo, Nome_Estilo, Preco_Base) VALUES (2, 'Blackwork', 450.00)")
cursor.execute("INSERT OR IGNORE INTO Estilos_Arte (ID_Estilo, Nome_Estilo, Preco_Base) VALUES (3, 'Realismo', 900.00)")
cursor.execute("INSERT OR IGNORE INTO Estilos_Arte (ID_Estilo, Nome_Estilo, Preco_Base) VALUES (4, 'Fineline', 250.00)")
conexao.commit()

while True:
    print("\n--- ESTÚDIO DE TATUAGEM ---")
    print("1. Novo Agendamento")
    print("2. Ver Agenda")
    print("3. Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        nome = input("Digite o nome do cliente: ")
        data = input("Digite a data (ex: 2026-04-10): ")
        
        print("\nEstilos Disponíveis:")
        cursor.execute("SELECT * FROM Estilos_Arte")
        estilos = cursor.fetchall()
        for estilo in estilos:
            print(f"[{estilo[0]}] {estilo[1]} - R$ {estilo[2]:.2f}")
            
        id_estilo = input("Digite o número do estilo desejado: ")
        
        cursor.execute("INSERT INTO Agendamentos (Nome_Cliente, Data_Sessao, ID_Estilo) VALUES (?, ?, ?)", (nome, data, id_estilo))
        conexao.commit()
        
        cursor.execute("SELECT Nome_Estilo, Preco_Base FROM Estilos_Arte WHERE ID_Estilo = ?", (id_estilo,))
        info_estilo = cursor.fetchone()
        
        if info_estilo:
            print(f"\nSucesso! Agendamento de {info_estilo[0]} marcado para {nome} no dia {data}.")
            print(f"Valor estimado: R$ {info_estilo[1]:.2f}")
            
    elif opcao == '2':
        cursor.execute('''
        SELECT Agendamentos.Data_Sessao, Agendamentos.Nome_Cliente, Estilos_Arte.Nome_Estilo, Estilos_Arte.Preco_Base
        FROM Agendamentos
        INNER JOIN Estilos_Arte ON Agendamentos.ID_Estilo = Estilos_Arte.ID_Estilo
        ORDER BY Agendamentos.Data_Sessao
        ''')
        resultados = cursor.fetcha
        print("\n--- AGENDA ATUAL ---")
        if not resultados:
            print("Nenhum agendamento encontrado.")
        else:
            for linha in resultados:
                print(f"Data: {linha[0]} | Cliente: {linha[1]} | Estilo: {linha[2]} | Valor: R$ {linha[3]:.2f}")
                
    elif opcao == '3':
        print("Saindo do sistema...")
        break
    else:
        print("Opção inválida.")

conexao.close()