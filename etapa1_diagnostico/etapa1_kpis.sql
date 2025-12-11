--------------------------------------------
-- KPI 1 — TOP 5 PRODUTOS MAIS VENDIDOS
--------------------------------------------
SELECT
    Description AS Produto,
    SUM(Quantity) AS QuantidadeVendida
FROM vendas
GROUP BY Description
ORDER BY QuantidadeVendida DESC
LIMIT 5;


--------------------------------------------
-- KPI 2 — RECEITA TOTAL POR MÊS
--------------------------------------------
SELECT
    AnoMes,
    SUM(Receita) AS ReceitaTotal
FROM vendas
GROUP BY AnoMes
ORDER BY AnoMes;


--------------------------------------------
-- KPI 3 — TAXA DE RETORNO DE CLIENTES
--------------------------------------------

WITH compras_por_cliente AS (
      SELECT
          CustomerID,
          COUNT(DISTINCT InvoiceNo) AS qtd_compras
      FROM vendas
      WHERE CustomerID IS NOT NULL
      GROUP BY CustomerID
)
SELECT
    (SELECT COUNT(*) FROM compras_por_cliente) AS TotalClientes,
    (SELECT COUNT(*) FROM compras_por_cliente WHERE qtd_compras > 1) AS ClientesComRetorno,
    ROUND(
        100.0 * (SELECT COUNT(*) FROM compras_por_cliente WHERE qtd_compras > 1)
        / (SELECT COUNT(*) FROM compras_por_cliente), 2
    ) || '%' AS TaxaRetorno
;


--------------------------------------------
-- KPI 4 — MÉDIA DE TEMPO ENTRE COMPRAS
--------------------------------------------

WITH cte_datas AS (
     SELECT
        CustomerID,
        InvoiceDate,
        LAG(InvoiceDate) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS DataAnterior
     FROM vendas
     WHERE CustomerID IS NOT NULL
),
cte_diff AS (
    SELECT
        CustomerID,
        JULIANDAY(InvoiceDate) - JULIANDAY(DataAnterior) AS DiffDias
    FROM cte_datas
    WHERE DataAnterior IS NOT NULL
)
SELECT
    ROUND(AVG(DiffDias), 2) AS MediaDiasEntreCompras
FROM cte_diff;
