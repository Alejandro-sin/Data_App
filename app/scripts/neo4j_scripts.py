



persons_count = """

MATCH (p:Person)-[:WORKS_AT]->(d:Department)
RETURN d.name AS Departamento, COUNT(p) AS NumeroDePersonas
ORDER BY NumeroDePersonas DESC

"""


most_frequent_job = """

MATCH (p:Person)-[:HOLDS]->(j:Job)
RETURN j.name AS Trabajo, COUNT(p) AS NumeroDePersonas
ORDER BY NumeroDePersonas DESC

"""

most_important_department = """

MATCH (p:Person)-[:WORKS_AT]->(d:Department)
RETURN d.name AS Departamento, COUNT(p) AS NumeroDePersonas
ORDER BY NumeroDePersonas DESC
LIMIT 1


"""

