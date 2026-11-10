
Automação de Extração e Organização de XMLs (TOTVS)

Este repositório contém um script em Python desenvolvido com o auxílio de Inteligência Artificial para automatizar o processo de extração, download e organização de arquivos XML gerados através do sistema TOTVS.

📌 O Problema

A tarefa consistia em acessar o portal do TOTVS para extrair arquivos XML de diversas filiais da empresa, englobando todo o ano de 2025 (janeiro a dezembro). O processo manual exigia:
• Seleção da loja e período.
• Espera de 1 a 4 minutos pelo processamento do sistema.
• Download manual de cada lote.
• Organização manual dos arquivos em uma estrutura de pastas específica (Ex: Lojas/Loja_01/2025/01_Janeiro/).
Devido ao volume de lojas e meses, o processo manual era altamente ineficiente e propenso a falhas operacionais.

💡 A Solução

O script automatiza a maior parte do fluxo de RPA (Robotic Process Automation):
1. Navegação Automatizada: Realiza os cliques de geração, aguarda o tempo de processamento do sistema de forma inteligente e efetua o download.
2. Organização de Arquivos: O script lê o arquivo baixado e o move automaticamente para a pasta correta correspondente à loja, ao ano e ao mês correto.
3. Controle Humano (Semi-automatizado): O script solicita a seleção da loja no início, permitindo que o operador tenha total controle sobre o progresso da tarefa e auditoria dos dados.

## 🛠️ Tecnologias Utilizadas
* **Python 3**
* `Selenium`: Para automação web, preenchimento de formulários e cliques dinâmicos.
* `Webdriver Manager`: Para gerenciamento automático da versão do driver do Chrome.
* `os` e `shutil`: Para mapeamento do sistema de arquivos e movimentação dos XMLs.

⚠️ Nota de Segurança

Este código foi sanitizado para exibição pública. Todas as credenciais de acesso, URLs internas da empresa, nomes reais de servidores ou dados sensíveis de clientes foram removidos ou substituídos por variáveis de ambiente / dados fictícios.
