SELECT
    a,
    b,
    c,
FROM `test.some_dataset.some_table` AS A
LEFT JOIN `test.other_dataset.other_table` AS B
ON A.a = B.A
WHERE
    A = 1
    AND B = "test"