import time
import os
from datetime import datetime
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
from ..api.mk.mk_driver import Mk
from ..api.mk.coin.coin import Financeiro
from ..api.mk.aside.aside_financeiro import GerenciadorDeContasAPagar

load_dotenv()

def lancamento(
        mk,
        credor,
        vencimento,
        efetiva,
        descricao,
        plano_conta,
        combinacao,
        negocio,
        valor,
        conta,
    ):
    hora = datetime.now()
    print(f'Iniciou lançamento {hora.strftime("%d/%m/%Y %H:%M")} Negócio:{negocio} Valor:{valor} Descrição:{descricao}')
    error = f"\033[91mERROR\033[0m;LANÇAMENTO;{hora.strftime('%d/%m/%Y %H:%M')}"
    sucess = f"\033[92mSUCESS\033[0m;LANÇAMENTO;{hora.strftime('%d/%m/%Y %H:%M')}"

    prefixo_log_lancamento = f'Negócio:{negocio};Valor:{valor};Descrição:{descricao}'

    if mk == 1:
        instance = Mk(
            username=os.getenv("USERNAME_MK1"),
            password=os.getenv("PASSWORD_MK1"),
            url=os.getenv("URL_MK1"),
        )
    elif mk == 3:
        instance = Mk(
            username=os.getenv("USERNAME_MK3"),
            password=os.getenv("PASSWORD_MK3"),
            url=os.getenv("URL_MK3"),
        )
    else:
        print(f"{error};{prefixo_log_lancamento};Não foi possível criar instancia do mk...")
        return f"{error};{prefixo_log_lancamento};Não foi possível criar instancia do mk..."

    financeiro = Financeiro()
    conta_pagar: GerenciadorDeContasAPagar = GerenciadorDeContasAPagar()

    # Login mk
    try:
        instance.login()
    except:
        instance.close()
        print(f"{error};{prefixo_log_lancamento};Login MK.")
        return f"{error};{prefixo_log_lancamento};Login MK."
    
    # Fecha cadastro
    try:
        instance.iframeMain()
        instance.click('//div[@class="OptionClose"]')
    except:
        pass

    # Moeda Finaceiro
    try:
        instance.iframeCoin()
        instance.click(financeiro.xpath())
    except:
        instance.close()
        print(f"{error};{prefixo_log_lancamento};Moeda Financeiro.")
        return f"{error};{prefixo_log_lancamento};Moeda Financeiro."

    # Aside Gerenciador de Contas a Pagar
    try:
        instance.iframeAsideCoin(financeiro)
        instance.click(conta_pagar.xpath())
    except:
        instance.close()
        print(f"{error};{prefixo_log_lancamento};Aside Gerenciador de Contas a Pagar.")
        return f"{error};{prefixo_log_lancamento};Aside Gerenciador de Contas a Pagar."

    # Botão Faturas pendentes.
    try:
        instance.iframePainel(financeiro, conta_pagar)
        instance.click("//button[@title='Faturas pendentes.']")
    except:
        instance.close()
        print(f"{error};{prefixo_log_lancamento};Botão Fatura pendentes.")
        return f"{error};{prefixo_log_lancamento};Botão Fatura pendentes."

    # Botão Adicionar fatura
    try:
        instance.iframePainel(financeiro, conta_pagar)
        instance.click("//button[@title='Adicionar fatura']")
    except:
        instance.close()
        print(f"{error};{prefixo_log_lancamento};Botão Adicionar fatura.")
        return f"{error};{prefixo_log_lancamento};Botão Adicionar fatura."

    # Selecionar Credor
    try:
        instance.iframeForm()
        instance.click('//div[@class="HTMLTabContainer"]/div[2]/div[8]/div[2]/div')
        instance.write('//input[@id="lookupSearchQuery"]', f"%{credor}" + Keys.ENTER)
        instance.click('//select[@id="lookupInput"]/option[2]')
    except:
        instance.close()
        print(f"{error};{prefixo_log_lancamento};Selecionar Credor.")
        return f"{error};{prefixo_log_lancamento};Selecionar Credor."

    # Escrever Descrição
    try:
        instance.iframeForm()
        instance.write('//div[@class="HTMLTabContainer"]/div[2]/div[9]/div[2]/input', f"{descricao}")
    except:
        instance.close()
        print(f"{error};{prefixo_log_lancamento};Escrever Descrição.")
        return f"{error};{prefixo_log_lancamento};Escrever Descrição."

    # Escrever Valor
    try:
        instance.iframeForm()
        instance.write('//div[@class="HTMLTabContainer"]/div[2]/div[11]/div[2]/input', f"{valor}")
    except:
        instance.close()
        print(f"{error};{prefixo_log_lancamento};Escrever Valor.")
        return f"{error};{prefixo_log_lancamento};Escrever Valor."

    # Escrever Vencimento
    try:
        instance.iframeForm()
        instance.write('//div[@class="HTMLTabContainer"]/div[2]/div[16]/div[2]/input', f"{vencimento}")
    except:
        instance.close()
        print(f"{error};{prefixo_log_lancamento};Escrever Vencimento.")
        return f"{error};{prefixo_log_lancamento};Escrever Vencimento."

    # Botão Próxima etapa
    try:
        instance.iframeForm()
        instance.click('//div[@class="HTMLTabContainer"]/div[2]//button[@title="Próxima etapa"]')
    except:
        instance.close()
        print(f"{error};{prefixo_log_lancamento};Botão Próxima etapa.")
        return f"{error};{prefixo_log_lancamento};Botão Próxima etapa."

    # Selecionar Plano de contas
    try:
        instance.iframeForm()
        instance.click('//div[@class="HTMLTabContainer"]/div[3]/div[7]/div[2]/div')
        instance.write('//input[@id="lookupSearchQuery"]', f"%{plano_conta}" + Keys.ENTER)
        instance.click('//select[@id="lookupInput"]/option[2]')
    except:
        instance.close()
        print(f"{error};{prefixo_log_lancamento};Selecionar Plano de contas.")
        return f"{error};{prefixo_log_lancamento};Selecionar Plano de contas."

    # Selecionar Combinação de centro de custos
    try:
        instance.iframeForm()
        instance.click('//div[@class="HTMLTabContainer"]/div[3]/div[8]/div[2]/div')
        instance.write('//input[@id="lookupSearchQuery"]', f"%{combinacao}" + Keys.ENTER)
        instance.click('//select[@id="lookupInput"]/option[2]')
    except:
        instance.close()
        print(f"{error};{prefixo_log_lancamento};Selecionar Combinação de centro de custos.")
        return f"{error};{prefixo_log_lancamento};Selecionar Combinação de centro de custos."

    # Selecionar Negócios
    try:
        instance.iframeForm()
        instance.click('//div[@class="HTMLTabContainer"]/div[3]/div[10]/div[2]/div')
        instance.write('//input[@id="lookupSearchQuery"]', f"%{negocio}" + Keys.ENTER)
        instance.click('//select[@id="lookupInput"]/option[2]')
    except:
        instance.close()
        print(f"{error};{prefixo_log_lancamento};Selecionar Negócios.")
        return f"{error};{prefixo_log_lancamento};Selecionar Negócios."

    # Clique para avançar a próxima etapa
    try:
        instance.iframeForm()
        instance.click('//button[@title="Clique para avançar a próxima etapa"]')
    except:
        instance.close()
        print(f"{error};{prefixo_log_lancamento};Clique para avançar a próxima etapa.")
        return f"{error};{prefixo_log_lancamento};Clique para avançar a próxima etapa."
    
    # Selecionar Liquidar agora
    try:
        instance.iframeForm()
        instance.click('//div[@title="Informe se deseja liquidar imediatamente esta fatura"]/div')
        instance.write('//input[@id="lookupSearchQuery"]', f"Sim" + Keys.ENTER)
        instance.click('//select[@id="lookupInput"]/option[2]')
    except:
        instance.close()
        print(f"{error};{prefixo_log_lancamento};Selecionar Liquidar agora.")
        return f"{error};{prefixo_log_lancamento};Selecionar Liquidar agora."
    
    # Escrever Efetivação
    try:
        instance.iframeForm()
        instance.write('//input[@title="Data de efetivação desta despesa"]', f"{efetiva}")
    except:
        instance.close()
        print(f"{error};{prefixo_log_lancamento};Escrever Efetivação.")
        return f"{error};{prefixo_log_lancamento};Escrever Efetivação."
    
    # Selecionar Como pagar
    try:
        instance.iframeForm()
        instance.click('//div[@title="Da onde debitar o pagamento?"]/div')
        instance.write('//input[@id="lookupSearchQuery"]', f"A partir de uma conta banco" + Keys.ENTER)
        instance.click('//select[@id="lookupInput"]/option[2]')
    except:
        instance.close()
        print(f"{error};{prefixo_log_lancamento};Selecionar Como pagar.")
        return f"{error};{prefixo_log_lancamento};Selecionar Como pagar."
    
    # Selecionar Conta banco
    try:
        instance.iframeForm()
        instance.click('//div[@title="Conta para registro de pagamento imediato desta conta."]/div')
        instance.write('//input[@id="lookupSearchQuery"]', f"%{conta}" + Keys.ENTER)
        instance.click('//select[@id="lookupInput"]/option[2]')
    except:
        instance.close()
        print(f"{error};{prefixo_log_lancamento};Selecionar Conta banco.")
        return f"{error};{prefixo_log_lancamento};Selecionar Conta banco."


    # Clique para efetivar a criação desta fatura.
    try:
        instance.iframeForm()
        instance.click('//button[@title="Clique para efetivar a criação desta fatura."]')
    except:
        instance.close()
        print(f"{error};{prefixo_log_lancamento};Clique para efetivar a criação desta fatura..")
        return f"{error};{prefixo_log_lancamento};Clique para efetivar a criação desta fatura.."

    time.sleep(5)
    instance.close()
    print(f'{sucess};{prefixo_log_lancamento};Lançamento da fatura conluído')
    return f'{sucess};{prefixo_log_lancamento};Lançamento da fatura conluído'