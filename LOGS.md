# Logs do fluxo principal

Descrevam em uma frase o fluxo executado e colem abaixo os logs copiados do terminal.

**Fluxo:** O Orquestrador SOA executou o checkout de compra aprovada via PIX com split (10% marketplace / 90% vendedor), validou a idempotência com a mesma `idempotency_key` sem cobrança duplicada e executou a compensação automática (liberação de estoque e cancelamento do pedido) após recusa simulada no cartão.

```text
[HARNESS] 1. Verificando healthchecks dos 5 serviços SOA...
  [OK] orquestrador saudável (http://orquestrador:8000/health)
  [OK] catalogo saudável (http://catalogo:8001/health)
  [OK] pedidos saudável (http://pedidos:8002/health)
  [OK] pagamentos saudável (http://pagamentos:8003/health)
  [OK] notificacoes saudável (http://notificacoes:8004/health)

[HARNESS] Estoque inicial prod-1: 10

[HARNESS] 2. Executando Cenário 1: Compra Aprovada (cid=harness-ok-9143cd, key=idem-fa9f9aee)
  [OK] Pedido ped-33a3ce10 PAGO | Split: {'marketplace_comissao_10pct': 50.0, 'vendedor_repasse_90pct': 450.0}
  [OK] Estoque atualizado: 8

[HARNESS] 3. Executando Cenário 2: Teste de Idempotência (cid=harness-idem-34c5f3, key=idem-fa9f9aee)
  [OK] Idempotência confirmada (tx=tx-33fcf9c0, estoque mantido=8)

[HARNESS] 4. Executando Cenário 3: Pagamento Recusado + Compensação (cid=harness-fail-3b5390)
  [OK] Compensação executada: pedido ped-ddff6d37 CANCELADO, estoque restaurado=8

[HARNESS] 5. Notificações registradas: 2 eventos
[HARNESS] TODOS OS TESTES PASSARAM COM SUCESSO!

=== LOGS DOS SERVIÇOS (docker compose logs) ===
pagamentos-1    | 2026-11-11 00:30:59,448 | pagamentos | INFO | cid=harness-ok-9143cd | Pagamento APROVADO | tx=tx-33fcf9c0 pedido=ped-33a3ce10 total=500.00 split(mkt=50.00, vend=450.00)
catalogo-1      | 2026-11-11 00:30:59,477 | catalogo | INFO | cid=harness-idem-34c5f3 | Estoque reservado | produto=prod-1 qtd=2 restante=6
pedidos-1       | 2026-11-11 00:30:59,480 | pedidos | INFO | cid=harness-idem-34c5f3 | Pedido criado | pedido_id=ped-0a7d56a2 status=PENDENTE valor=500.0
pagamentos-1    | 2026-11-11 00:30:59,485 | pagamentos | INFO | cid=harness-idem-34c5f3 | IDEMPOTÊNCIA ATIVADA | key=idem-fa9f9aee transacao=tx-33fcf9c0 (sem cobrança duplicada)
catalogo-1      | 2026-11-11 00:30:59,487 | catalogo | INFO | cid=harness-idem-34c5f3 | COMPENSAÇÃO: Estoque liberado | produto=prod-1 qtd=2 estoque_atual=8
pedidos-1       | 2026-11-11 00:30:59,490 | pedidos | INFO | cid=harness-idem-34c5f3 | Status atualizado | pedido_id=ped-0a7d56a2 PENDENTE -> CANCELADO
catalogo-1      | 2026-11-11 00:30:59,523 | catalogo | INFO | cid=harness-fail-3b5390 | Estoque reservado | produto=prod-1 qtd=1 restante=7
pedidos-1       | 2026-11-11 00:30:59,526 | pedidos | INFO | cid=harness-fail-3b5390 | Pedido criado | pedido_id=ped-ddff6d37 status=PENDENTE valor=250.0
pagamentos-1    | 2026-11-11 00:30:59,529 | pagamentos | WARNING | cid=harness-fail-3b5390 | Pagamento RECUSADO | pedido_id=ped-ddff6d37 metodo=CARTAO valor=250.00
orquestrador-1  | 2026-11-11 00:30:59,531 | orquestrador | WARNING | cid=harness-fail-3b5390 | Pagamento recusado para ped-ddff6d37. Executando compensação SOA...
catalogo-1      | 2026-11-11 00:30:59,532 | catalogo | INFO | cid=harness-fail-3b5390 | COMPENSAÇÃO: Estoque liberado | produto=prod-1 qtd=1 estoque_atual=8
pedidos-1       | 2026-11-11 00:30:59,534 | pedidos | INFO | cid=harness-fail-3b5390 | Status atualizado | pedido_id=ped-ddff6d37 PENDENTE -> CANCELADO
orquestrador-1  | 2026-11-11 00:30:59,537 | orquestrador | INFO | HTTP Request: POST http://notificacoes:8004/notificacoes "HTTP/1.1 201 Created"
```
