from MultiAgentAlg.AntColonyOptimization.utils import instance_reader

C, G = instance_reader("./Instances/problem2.ant")


C.collect_food(1000, G, 60)

print(C.food)
