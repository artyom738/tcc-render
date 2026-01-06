SELECT
    s.ID,
    s.AUTHORS AS 'Автор',
    s.NAME AS 'Название',
    SUM(41 - cp.POSITION) AS 'Очки'
FROM
    songs s
    INNER JOIN chart_positions cp ON s.ID = cp.SONG_ID
    INNER JOIN charts c ON cp.CHART_ID = c.ID
WHERE
    c.CHART_TYPE = 'eht'
    AND c.CHART_DATE >= '2025-01-01'
    AND c.CHART_DATE < '2026-01-01'
GROUP BY
    s.ID, s.AUTHORS, s.NAME
ORDER BY
    Очки DESC;