# OOP_Ex4
In this task we asked to implements pokemon game.
In order to implements the graph of the game, we take classes from the previous task: DiGraph and GraphAlgo.
In addition, we implements 2 new classes: Pokemon and Agent.
### Pokemon:<br />
In this class we have the next fields:<br />
value, pos and type that we get from the server and edge: the edge that the pokemon stand on, we get this edge from the function "pok on edge" that we will explain it later.<br />
### Agent:<br />
In this class we have the next fileds:<br />
id, value, pos, src, dest and speed that we get from the server and path, pok. <br />
path= the path that tha agent need to do. pok= the pokemon that we allocate to the agent.<br /><br />
________________________________________________________________________________<br /><br />
The main class is playGame:<br />
In this class we present and activate the game.<br />
We draw the graph and calculate for all the agents to who from the pokemons they need to go.<br />
We have in this class few functions:<br />
### update_agent:<br />
We get from the server json string with all the agents and load them to our dictionary: "dic_agents". if the agent alredy exists we just update the value that could have changed like pos.<br />
### update_pokemons:<br />
We get from the server json string with all the pokemons that we have and loat them to our list : "pokemons".<br />
### distance:<br />
this function 2 id of nodes on the graph and return the distance between them.<br />
### pok_on_edge:<br />
this function find for any pokemone who is the edge that it stand on. we calculate this with the distance function.<br />
### allocate_pok_to_agent:<br />
this function get agent and check to who from all the pokemons he should to go.<br />
if we have just one agent, we pass of all the pokemons and calculate the shortest path to them with the function shortestpath in GraphAlgo class.
<br /><br />
## how to run:
