import time
import os
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
        error,
        sucess,
        prefixo_log,
    ):

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
        print(f"{error};{prefixo_log};Não foi possível criar instancia do mk...")
        return f"{error};{prefixo_log};Não foi possível criar instancia do mk..."

    financeiro = Financeiro()
    conta_pagar: GerenciadorDeContasAPagar = GerenciadorDeContasAPagar()

    # Login mk
    try:
        instance.login()
    except:
        instance.close()
        print(f"{error};{prefixo_log};Login MK.")
        return f"{error};{prefixo_log};Login MK."
    
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
        print(f"{error};{prefixo_log};Moeda Financeiro.")
        return f"{error};{prefixo_log};Moeda Financeiro."

    # Aside Gerenciador de Contas a Pagar
    try:
        instance.iframeAsideCoin(financeiro)
        instance.click(conta_pagar.xpath())
    except:
        instance.close()
        print(f"{error};{prefixo_log};Aside Gerenciador de Contas a Pagar.")
        return f"{error};{prefixo_log};Aside Gerenciador de Contas a Pagar."

    # Botão Faturas pendentes.
    try:
        instance.iframePainel(financeiro, conta_pagar)
        instance.click("//button[@title='Faturas pendentes.']")
    except:
        instance.close()
        print(f"{error};{prefixo_log};Botão Fatura pendentes.")
        return f"{error};{prefixo_log};Botão Fatura pendentes."

    # Botão Adicionar fatura
    try:
        instance.iframePainel(financeiro, conta_pagar)
        instance.click("//button[@title='Adicionar fatura']")
    except:
        instance.close()
        print(f"{error};{prefixo_log};Botão Adicionar fatura.")
        return f"{error};{prefixo_log};Botão Adicionar fatura."

    # Selecionar Credor
    try:
        instance.iframeForm()
        instance.click('//div[@class="HTMLTabContainer"]/div[2]/div[8]/div[2]/div')
        instance.write('//input[@id="lookupSearchQuery"]', f"%{credor}" + Keys.ENTER)
        instance.click('//select[@id="lookupInput"]/option[2]')
    except:
        instance.close()
        print(f"{error};{prefixo_log};Selecionar Credor.")
        return f"{error};{prefixo_log};Selecionar Credor."

    # Escrever Descrição
    try:
        instance.iframeForm()
        instance.write('//div[@class="HTMLTabContainer"]/div[2]/div[9]/div[2]/input', f"{descricao}")
    except:
        instance.close()
        print(f"{error};{prefixo_log};Escrever Descrição.")
        return f"{error};{prefixo_log};Escrever Descrição."

    # Escrever Valor
    try:
        instance.iframeForm()
        instance.write('//div[@class="HTMLTabContainer"]/div[2]/div[11]/div[2]/input', f"-{valor}")
    except:
        instance.close()
        print(f"{error};{prefixo_log};Escrever Valor.")
        return f"{error};{prefixo_log};Escrever Valor."

    # Escrever Vencimento
    try:
        instance.iframeForm()
        instance.write('//div[@class="HTMLTabContainer"]/div[2]/div[16]/div[2]/input', f"{vencimento}" + Keys.TAB)
    except:
        instance.close()
        print(f"{error};{prefixo_log};Escrever Vencimento.")
        return f"{error};{prefixo_log};Escrever Vencimento."
    
    # Error vencimento
    try:
        instance.iframeForm()
        instance.click('//div[@id="intTitleClose"]')
        # Escrever Vencimento
        try:
            instance.iframeForm()
            instance.write('//div[@class="HTMLTabContainer"]/div[2]/div[16]/div[2]/input', f"{vencimento}" + Keys.TAB)
        except:
            instance.close()
            print(f"{error};{prefixo_log};Escrever Vencimento 2.")
            return f"{error};{prefixo_log};Escrever Vencimento 2."
    except:
        pass
    
    # Error desconhecido
    try:
        instance.iframeForm()
        instance.click('//div[@id="intTitleClose"]')
    except:
        pass

    # Botão Próxima etapa
    try:
        instance.iframeForm()
        instance.click('//button[@title="Próxima etapa"]')
    except:
        instance.close()
        print(f"{error};{prefixo_log};Botão Próxima etapa.")
        return f"{error};{prefixo_log};Botão Próxima etapa."

    # Selecionar Plano de contas
    try:
        instance.iframeForm()
        instance.click('//div[@class="HTMLTabContainer"]/div[3]/div[7]/div[2]/div')
        instance.write('//input[@id="lookupSearchQuery"]', f"%{plano_conta}" + Keys.ENTER)
        instance.click(f'//select[@id="lookupInput"]/option[@value="{plano_conta}"]')
    except:
        instance.close()
        print(f"{error};{prefixo_log};Selecionar Plano de contas.")
        return f"{error};{prefixo_log};Selecionar Plano de contas."

    # Selecionar Combinação de centro de custos
    try:
        instance.iframeForm()
        instance.click('//div[@class="HTMLTabContainer"]/div[3]/div[8]/div[2]/div')
        instance.write('//input[@id="lookupSearchQuery"]', f"%{combinacao}" + Keys.ENTER)
        instance.click('//select[@id="lookupInput"]/option[2]')
    except:
        instance.close()
        print(f"{error};{prefixo_log};Selecionar Combinação de centro de custos.")
        return f"{error};{prefixo_log};Selecionar Combinação de centro de custos."

    # Selecionar Negócios
    try:
        instance.iframeForm()
        instance.click('//div[@class="HTMLTabContainer"]/div[3]/div[10]/div[2]/div')
        instance.write('//input[@id="lookupSearchQuery"]', f"%{negocio}" + Keys.ENTER)
        instance.click('//select[@id="lookupInput"]/option[2]')
    except:
        instance.close()
        print(f"{error};{prefixo_log};Selecionar Negócios.")
        return f"{error};{prefixo_log};Selecionar Negócios."

    # Clique para avançar a próxima etapa
    try:
        instance.iframeForm()
        instance.click('//button[@title="Clique para avançar a próxima etapa"]')
    except:
        instance.close()
        print(f"{error};{prefixo_log};Clique para avançar a próxima etapa.")
        return f"{error};{prefixo_log};Clique para avançar a próxima etapa."
    
    # Selecionar Liquidar agora
    try:
        instance.iframeForm()
        instance.click('//div[@title="Informe se deseja liquidar imediatamente esta fatura"]/div')
        instance.write('//input[@id="lookupSearchQuery"]', f"Sim" + Keys.ENTER)
        instance.click('//select[@id="lookupInput"]/option[2]')
    except:
        instance.close()
        print(f"{error};{prefixo_log};Selecionar Liquidar agora.")
        return f"{error};{prefixo_log};Selecionar Liquidar agora."
    
    # Escrever Efetivação
    try:
        instance.iframeForm()
        instance.write('//input[@title="Data de efetivação desta despesa"]', f"{efetiva}")
    except:
        instance.close()
        print(f"{error};{prefixo_log};Escrever Efetivação.")
        return f"{error};{prefixo_log};Escrever Efetivação."
    
    # Selecionar Como pagar
    try:
        instance.iframeForm()
        instance.click('//div[@title="Da onde debitar o pagamento?"]/div')
        instance.write('//input[@id="lookupSearchQuery"]', f"A partir de uma conta banco" + Keys.ENTER)
        instance.click('//select[@id="lookupInput"]/option[2]')
    except:
        instance.close()
        print(f"{error};{prefixo_log};Selecionar Como pagar.")
        return f"{error};{prefixo_log};Selecionar Como pagar."
    
    # Selecionar Conta banco
    try:
        instance.iframeForm()
        instance.click('//div[@title="Conta para registro de pagamento imediato desta conta."]/div')
        instance.write('//input[@id="lookupSearchQuery"]', f"%{conta}" + Keys.ENTER)
        instance.click('//select[@id="lookupInput"]/option[2]')
    except:
        instance.close()
        print(f"{error};{prefixo_log};Selecionar Conta banco.")
        return f"{error};{prefixo_log};Selecionar Conta banco."


    # Clique para efetivar a criação desta fatura.
    try:
        instance.iframeForm()
        instance.click('//button[@title="Clique para efetivar a criação desta fatura."]')
    except:
        instance.close()
        print(f"{error};{prefixo_log};Clique para efetivar a criação desta fatura..")
        return f"{error};{prefixo_log};Clique para efetivar a criação desta fatura.."

    time.sleep(5)
    instance.close()
    print(f'{sucess};{prefixo_log};Lançamento da fatura conluído')
    return f'{sucess};{prefixo_log};Lançamento da fatura conluído'