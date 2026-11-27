# Requisitos

## Requisitos funcionais

| ID | Requisito |
| --- | --- |
| RF01 | O sistema deve permitir consultar produtos disponíveis no catálogo com preço, estoque e identificação do vendedor. |
| RF02 | O sistema deve orquestrar a criação de pedidos reservando o estoque do produto antes da cobrança. |
| RF03 | O sistema deve processar pagamentos (PIX ou Cartão) calculando automaticamente o split entre a comissão do marketplace (10%) e o repasse líquido ao vendedor (90%). |
| RF04 | O sistema deve garantir idempotência no processamento de pagamentos por meio de `idempotency_key`, evitando cobranças duplicadas. |
| RF05 | O sistema deve executar compensação automática (liberação de estoque e cancelamento do pedido) e notificar o cliente caso o pagamento seja recusado ou falhe. |

## Requisitos não funcionais

| ID | Requisito |
| --- | --- |
| RNF01 | **Arquitetura Orientada a Serviços (SOA):** Cada domínio de negócio deve rodar como um serviço independente com contrato REST/JSON explícito e endpoint `/health`. |
| RNF02 | **Observabilidade e Rastreabilidade:** Todas as requisições entre serviços devem propagar um `X-Correlation-ID` e gerar logs estruturados para auditoria do fluxo completo. |
| RNF03 | **Portabilidade e Execução Única:** Todo o ecossistema de serviços deve subir com um único comando (`docker compose up --build`) com healthchecks ordenados e harness automatizado de verificação. |
