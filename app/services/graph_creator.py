
from streamlit_agraph import agraph, Node, Edge, Config
from neo4j.exceptions import ClientError
from neo4j import GraphDatabase
import os




def populate_graph_from_neo4j(results):
    nodes = []
    edges = []
    
    # Procesamos los resultados del query (asumiendo que devuelve nodos y relaciones)
    for record in results:
        # Obtenemos información del nodo
        if 'n' in record:  # 'n' sería el alias en el query de Cypher
            node_id = record['n']['id']
            label = record['n']['label']
            size = record['n'].get('size', 25)  # Default a 25 si no existe
            
            # Creamos el nodo
            nodes.append(Node(id=node_id, label=label, size=size))
        
        # Obtenemos información de la relación si existe
        if 'r' in record:  # 'r' sería el alias de la relación en el query
            source = record['r'].start_node['id']
            target = record['r'].end_node['id']
            label = record['r'].type
            
            # Creamos el edge (arista)
            edges.append(Edge(source=source, target=target, label=label))
    
    
    
    # Configuración de visualización
    config = Config(width=750,
                    height=950,
                    directed=True, 
                    physics=True, 
                    hierarchical=False)
    
    # Retornamos el grafo con nodos y edges
    return agraph(nodes=nodes, edges=edges, config=config)

def graph_session():
    URI = "neo4j+s://a575d5a9.databases.neo4j.io:7687"
    AUTH = ("neo4j", "yIjVz15ZVDbIFAyjLdA8tjacG-Re7_Cd8G_rY5YesTo")

    with GraphDatabase.driver(URI, auth=AUTH) as driver:    
        return driver


driver = graph_session()
session = driver.session(database="neo4j")

def query_graph(query, parameters=None):    
    with driver.session() as session:
        result = session.run(query, parameters)
        return [record for record in result]

'''
################

nodes = []
edges = []
nodes.append( Node(id="Spiderman", 
                   label="Peter Parker",
                   size=25)
            ) # includes **kwargs
nodes.append( Node(id="Captain_Marvel", 
                   size=25,) 
            )
edges.append( Edge(source="Captain_Marvel", 
                   label="friend_of", 
                   target="Spiderman", 
                   # **kwargs
                   ) 
            ) 

config = Config(width=750,
                height=950,
                directed=True, 
                physics=True, 
                hierarchical=False,
                # **kwargs
                )

return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)


# Config for physic and stuff of the graph

config_builder = ConfigBuilder(nodes)
config = config_builder.build()
config.save("config.json")
config = Config(from_json="config.json")

################



'''