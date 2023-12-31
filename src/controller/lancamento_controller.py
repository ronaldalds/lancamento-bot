import os
import concurrent.futures
import pandas as pd
from pyrogram.types import Message
from pyrogram import Client
from datetime import datetime
from dotenv import load_dotenv
from ..service.lancamento_service import lancamento
from ..util.formatador import formatar_data

load_dotenv()
running = False

def handle_start_lancamento(client: Client, message: Message):
    global running
    if not running:
        print(message.document.mime_type)
        # Verifique se a mensagem contém um documento e se o tipo MIME do documento é "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        if message.document and (                  
            message.document.mime_type.startswith("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") or
            message.document.mime_type == "application/vnd.ms-excel" or
            message.document.mime_type == "application/wps-office.xlsx"
        ):
            running = True
            # Quantidade de itens na Pool
            limite_threads = 7

            # Baixe o arquivo XLSX
            file_path = message.download(in_memory=True)
            hora = datetime.now()
            file_name = hora.strftime("%S_%M_%H %Y-%m-%d.log")
            message.reply_text("Preparando arquivo XLSX")
            agente = f"{message.from_user.first_name}.{message.from_user.last_name}"
            
            adm = int(os.getenv("CHAT_ID_ADM"))

            # caminho pasta de logs
            diretorio_logs = os.path.join(os.path.dirname(__file__), 'logs')

            # caminho pasta de docs
            diretorio_docs = os.path.join(os.path.dirname(__file__), 'docs')

            # cria pasta de logs em caso de nao existir
            if not os.path.exists(diretorio_logs):
                os.makedirs(diretorio_logs)

            # cria pasta de docs em caso de nao existir
            if not os.path.exists(diretorio_docs):
                os.makedirs(diretorio_docs)

            resultados = []
            # Processar o arquivo XLSX conforme necessário
            try:
                try:
                    # Ler o arquivo XLSX usando pandas e especificar a codificação UTF-8
                    df = pd.read_excel(file_path)

                    # Converter o dataframe para uma lista de dicionários
                    lista = df.to_dict(orient='records')


                    # Verificar se a chave 'MK' contém valor NaN
                    lista = [dados for dados in lista if not pd.isna(dados.get('MK'))]

                    # Criar aquivo de log com todos os vencimentos enviados para cancelamento
                    with open(os.path.join(diretorio_docs, file_name), "a") as pedido:
                        for c,arg in enumerate(lista):
                            pedido.write(f"{(c + 1):03};Lançamento;ID:{int(arg.get('ID'))};MK:{int(arg.get('MK'))};Negócio:{arg.get('NEGOCIO')};Valor:{arg.get('VALOR')};Descrição:{arg.get('DESCRICAO')};Agente:{agente}\n")
                    
                    # Envia arquivo de docs com todos as solicitações de cancelamento
                    with open(os.path.join(diretorio_docs, file_name), "rb") as enviar_docs:
                        client.send_document(adm, enviar_docs, caption=f"solicitações {file_name}", file_name=f"solicitações {file_name}")

                    
                    message.reply_text(f"Processando arquivo XLSX de lançamento com {len(lista)} fatura...")

                except pd.errors.ParserError:
                    message.reply_text("O arquivo fornecido não é um arquivo XLSX válido.")
                    running = False
                    return
                
                def executar(arg: dict):
                    if running:
                        try:
                            id = arg.get("ID")
                            mk: int = int(arg.get("MK"))
                            credor: str = str(arg.get("CREDOR"))
                            vencimento = formatar_data(arg.get("VENCIMENTO"))
                            efetiva = formatar_data(arg.get("EFETIVA"))
                            descricao: str = str(arg.get("DESCRICAO"))
                            plano_conta: str = str(arg.get("PLANO_CONTA"))
                            combinacao: str = str(arg.get("COMBINACAO"))
                            negocio: str = str(arg.get("NEGOCIO"))
                            valor: str = str(arg.get("VALOR"))
                            conta: str = str(arg.get("CONTA"))

                            warning = f"\033[93mWARNING\033[0m;LANÇAMENTO;{hora.strftime('%d/%m/%Y %H:%M')}"
                            error = f"\033[91mERROR\033[0m;LANÇAMENTO;{hora.strftime('%d/%m/%Y %H:%M')}"
                            sucess = f"\033[92mSUCESS\033[0m;LANÇAMENTO;{hora.strftime('%d/%m/%Y %H:%M')}"
                            prefixo_log = f'ID:{id};Negócio:{negocio};Valor:{valor};Descrição:{descricao}'
                            item = f"ID:{id}-MK:{mk}-Plano:{plano_conta[:14]}-Combinação:{combinacao[:9]}-Vct:{vencimento}-Efetiva:{efetiva}-Negócio:{negocio}-Valor:{valor.replace('.', ',')}-Descrição:{descricao}"
                        
                            print(f'Iniciou {item}')
                            return lancamento(
                                mk = mk,
                                credor = credor,
                                vencimento = vencimento,
                                efetiva = efetiva,
                                descricao = descricao,
                                plano_conta = plano_conta[:14],
                                combinacao = combinacao[:9],
                                negocio = negocio,
                                valor = valor.replace('.', ','),
                                conta = conta,
                                error = error,
                                sucess = sucess,
                                prefixo_log = prefixo_log,
                                )
                        except Exception as e:
                            print(f'Error {item}=={e}')
                            return f"{warning};{prefixo_log};Error na execução"
                    else:
                        message.reply_text(f'Lançamento ID:{id} MK:{mk} Negócio:{negocio} Valor:{valor} Descrição:{descricao} parado.')
                
                # Criando Pool
                with concurrent.futures.ThreadPoolExecutor(max_workers=limite_threads) as executor:
                    resultados = executor.map(executar, lista)

                # Criar aquivo de log com todos os resultados de cancelamento
                with open(os.path.join(diretorio_logs, file_name), "a") as file:
                    if resultados:
                        for resultado in resultados:
                            file.write(f"{resultado}\n")

                # Envia arquivo de log com todos os resultados de cancelamento
                with open(os.path.join(diretorio_logs, file_name), "rb") as enviar_logs:
                    message.reply_document(enviar_logs, caption=file_name, file_name=file_name)
                    client.send_document(adm, enviar_logs, caption=f"resultado {file_name}", file_name=f"resultado {file_name}")

                print("Processo Lançamento concluído.")
                message.reply_text("O arquivo XLSX de lançamento foi processado com sucesso!")
                running = False
                return
            
            except Exception as e:
                print(f"Ocorreu um erro ao processar o arquivo XLSX: {e}")
                message.reply_text("Ocorreu um error ao processar o arquivo XLSX.\nEntre em contato com o Administrador.")
                running = False
                return
        
        else:
            # Responder à mensagem do usuário com uma mensagem de erro
            message.reply_text("Por favor, envie um arquivo XLSX para processar.")
            return
    else:
        message.reply_text("Lançamento em execução.")
        return

def handle_stop_lancamento(client: Client, message: Message):
    global running
    if running:
        running = False
        message.reply_text("Pedido de parada iniciado...")
        return
    else:
        message.reply_text("Lançamento parado")
        return
        
def handle_status_lancamento(client: Client, message: Message):
    global running
    try:
        if running:
            message.reply_text("Lançamento em execução")
            return
        else:
            message.reply_text("Lançamento parado")
            return
    except:
        message.reply_text("Lançamento parado")
        return