import sqlite3
import datetime
import csv

#Declaração de funções
#Calcula a quantidade de visualizações, compartilhamentos e clicks
def calculadoraVisualizacoes(visualizacoes):
    
    clicks = visualizacoes * 12 / 100
    compartilhamentos = clicks * 3 / 20
    novopublico = compartilhamentos * 40

    return(clicks, compartilhamentos, novopublico)

#Valida se a data inserida é válida
def validar_data(data):
        try:
            data_entrada = datetime.datetime.strptime(data, '%d/%m/%Y')
            return(data_entrada)
        except:
            print("Formato da data está incorreto! Digite: dd/mm/aaaa")

#Função padrão para inserir valores na tabela SQL
def inserirVariavelNaTabela(cliente, nome_Anuncio, data_inicio, datafim, invest_dia, invest_total, qnt_visu, qnt_cliq, qnt_comp):
    try:
        #Abre a conexão com o BD
        conexao_sqlite = sqlite3.connect('BD_SQLite_Anuncios.db')
        cursor = conexao_sqlite.cursor()
        print("Conectado ao SQLite")

        #Busca a ultima chave da tabela
        try:        
            cursor.execute("SELECT * FROM Anuncios_Cadastrados ORDER BY id DESC LIMIT 1")
            result = cursor.fetchone()
            if result ==None:
                result = [0]
        except:
            result = [0]

        #Query para inserir os valores
        sqlite_inserir_param = """INSERT INTO Anuncios_Cadastrados
                          (id, cliente, nome_Anuncio, data_inicio, data_fim, invest_dia, invest_total, qnt_visu, qnt_comp, qnt_cliq) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        data_tuple = (result[0]+1, cliente, nome_Anuncio, data_inicio, datafim, invest_dia, invest_total, qnt_visu, qnt_cliq, qnt_comp)
        cursor.execute(sqlite_inserir_param, data_tuple)
        conexao_sqlite.commit()
        print("Variaveis salvas com sucesso no banco de dados!")

        cursor.close()
    #Resolução de erros
    except sqlite3.Error as error:
        print("Falha ao salvar as variaveis no banco de dados!", error)
    finally:
        if conexao_sqlite:
            conexao_sqlite.close()
            print("Conexao com SQLite encerrada")

#Função para realizar todo o cadastro de um novo anuncio
def cadastrar():
    #Declaração de váraiveis
    dadosBrutosVisualizacao = None
    totalVisualizacoes = None
    totalCompartilhamentos = 0.0
    totalClicks = 0.0
    visuaFuncao = None

    #Verifica se a planilha e tabela de SQL já existem no diretório atual
    try:
        conexao_sqlite = sqlite3.connect('BD_SQLite_Anuncios.db')
        sqlite_query_criar_tab = '''CREATE TABLE Anuncios_Cadastrados (
                                    id INTEGER PRIMARY KEY,
                                    cliente TEXT NOT NULL,
                                    nome_Anuncio text NOT NULL,
                                    data_inicio datetime,
                                    data_fim datetime,
                                    invest_dia REAL NOT NULL, invest_total REAL NOT NULL,
                                    qnt_visu INTEGER NOT NULL, qnt_comp INTEGER NOT NULL, qnt_cliq INTEGER NOT NULL);'''

        cursor = conexao_sqlite.cursor()
        print("\nConexão com SQLite estabelecida com sucesso")
        cursor.execute(sqlite_query_criar_tab)
        conexao_sqlite.commit()
        print("Tabela do SQLite criada com sucesso")

        cursor.close()
    except:
        print("Banco de dados já existe! Itens serão anexados ao BD")
    finally:
        if conexao_sqlite:
            conexao_sqlite.close()

    #Input e validação de dados
    nomeCliente = input(" \nPor favor, digite o nome do cliente:\n")

    nomeCampanha = input(" \nPor favor, digite o nome da campanha:\n")

    while True:
        dataInicio = input("\nPor favor, digite a data de inicio da campanha:\n")
        dataInicioIte = validar_data(dataInicio)
        if dataInicioIte != None:
            break

    while True:
        dataFim = input("\nPor favor, digite a data de fim da campanha:\n")
        dataFimIte = validar_data(dataFim)
        if dataFimIte != None and dataFimIte>dataInicioIte:
            break
        elif dataFimIte != None and dataFimIte<=dataInicioIte:
            print("A data de término deve ser posterior a data de ínicio")

    diasCampanha = dataFimIte-dataInicioIte
    totalDiasCampanha = diasCampanha.days + 1

    while True:
        try:
            valorInvestido = float(input(" \nPor favor, digite o investimento diário da campanha publicitária:\nR$ "))
            if valorInvestido <= 0: 
                raise Exception("Digite um número positivo!\n")
            else:
                valorCentavos = str(valorInvestido).split(".", 1)
                if len(valorCentavos[1])>2:
                    raise Exception("Digite um valor com até duas casas decimais!\n")
                else:
                    break
        except:
            print(" \nDigite um número válido! (Ex: 50; 15,25; ...)\n ")

    totalInvestido = totalDiasCampanha * valorInvestido

    #Calcula a quantidade de visualizações originais
    visualizacoesOriginais = totalInvestido * 30

    totalVisualizacoes = visualizacoesOriginais
    visuaFuncao = visualizacoesOriginais

    #Chama a função de cálculo e executa 4 cilos de compartilhamento
    for i in range(4):
        dadosBrutosVisualizacao = calculadoraVisualizacoes(visuaFuncao)
        totalVisualizacoes = dadosBrutosVisualizacao[2] + totalVisualizacoes
        totalCompartilhamentos = dadosBrutosVisualizacao[1] + totalCompartilhamentos
        totalClicks = dadosBrutosVisualizacao[0] + totalClicks
        visuaFuncao = dadosBrutosVisualizacao[2]
    
    inserirVariavelNaTabela(nomeCliente, nomeCampanha, dataInicio, dataFim, valorInvestido, round(totalInvestido,2), round(totalVisualizacoes), round(totalCompartilhamentos), round(totalClicks))

    print("\n-------DADOS CADASTRADOS--------\nCliente: ",nomeCliente,"\nCampanha cadastrada: ",nomeCampanha,"\nData de ínicio: ",dataInicio,"\nData final: ",dataFim,"\nValor total investido: ",totalInvestido,"\nTotal de visualizações previstas:",round(totalVisualizacoes),"\nTotal de compartilhamentos previstos:",round(totalCompartilhamentos),"\nTotal de clicks previstos:",round(totalClicks))

#Programa principal que chama as funções a serem excecutadas
print(" \n-------------------- Início do programa --------------------")
while True:
    acao = input("\nVocê deseja consultar o banco de dados ou cadastrar um novo anúncio? (Digite cadastrar, exportar, visualizar ou sair)\n")

    if acao == "cadastrar":
        cadastrar()
    elif acao =="exportar":
        try:
            conexao_sqlite = sqlite3.connect('BD_SQLite_Anuncios.db')
        
            #Exporta os dados para CSV
            print ("Exportando dados para um CSV...")
            cursor = conexao_sqlite.cursor()
            cursor.execute("SELECT * FROM Anuncios_Cadastrados")
            with open("BD_Anuncios_Cadastrados.csv", "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=";", lineterminator='\n')
                csv_writer.writerow([i[0] for i in cursor.description])
                csv_writer.writerows(cursor)
            print ("Exportado!!")
        except:
            print(" \nNenhum lançamento encontrado!\n ")
    elif acao == "visualizar":
        try:
            #Mostra os dados cadastrados no banco de dados
            print ("Dados cadastrados:\n")
            conexao_sqlite = sqlite3.connect("BD_SQLite_Anuncios.db")
            cursor = conexao_sqlite.cursor()
            cursor.execute("SELECT * FROM Anuncios_Cadastrados")
            linhas = cursor.fetchall()
            print("\n-------DADOS CADASTRADOS--------")
            for linha in linhas:
                print("\nCliente: ",linha[1],"\nCampanha cadastrada: ",linha[2],"\nData de ínicio: ",linha[3],"\nData final: ",linha[4],"\nValor total investido: ",linha[6],"\nTotal de visualizações previstas:",round(linha[7]),"\nTotal de compartilhamentos previstos:",round(linha[8]),"\nTotal de clicks previstos:",round(linha[9]))    
            print("\n-------FIM--------")
        except:
            print(" \nNenhum lançamento encontrado!\n ")

    elif acao == "sair":
        break