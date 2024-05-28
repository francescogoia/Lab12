from model.model import Model

myModel = Model()
myModel.build_graph("Germany", "2016")
print(myModel.info_grafo())

myModel.calcola_volumi()
print(myModel.ordina_retailer_per_volume())

print("*/*/*/*/")
myModel.calcola_percorso(5)
