import json
from classic_heuristics.gillet_miller_sweep import gillet_miller_init
from util import sol2routes
import numpy
from loader import Loader
from flask import jsonify
from kafkaService import kafkaService

__author__ = "Ashar Fatmi"
__maintainer__ = "Ashar Fatmi"
__email__ = "asharfatmi.fatmi@gmail.com"
__status__ = "Development"


class testFunction:
    def __init__(self):
        self.KAFKA = kafkaService()
        pass

    def gilletMiller(self, runFromJson, input=None):
        runFromJson = True

        with open('request.json')as jsonFile:
            data = jsonFile.read()
        options = json.loads(data)

        if runFromJson == False:
            pass

        print("capacity_of_the_bus = ", options["capacity_of_the_bus"])
        points = input["points"] if runFromJson != True else options["points"]

        full_distance_matrix = input["full_distance_matrix"] if runFromJson != True else options["full_distance_matrix"]

        full_distance_matrix = numpy.array(full_distance_matrix)

        for i in range(full_distance_matrix.shape[0]):
            for j in range(i, full_distance_matrix.shape[1]):
                full_distance_matrix[i, j] = full_distance_matrix[j, i]

        pupils_on_each_bus_stop = input["pupils_on_each_bus_stop"] if runFromJson != True else options["pupils_on_each_bus_stop"]

        capacity_of_the_bus = input["capacity_of_the_bus"] if runFromJson != True else options["capacity_of_the_bus"]

        constraint = input["CONSTRAINT"]
        minimize_number_of_buses = False

        loader = Loader("Running Heuristics...",
                        "Heuristics Done!", 0.1).start()
        solution = gillet_miller_init(
            points=points,
            D=full_distance_matrix,
            d=pupils_on_each_bus_stop,
            C=capacity_of_the_bus,
            L=constraint,
            minimize_K=minimize_number_of_buses)
        loader.stop()

        ROUTES = []

        loader.__init__("Preparing Response", "Response ready!!", timeout=0.1)
        loader.start()

        for route_idx, route in enumerate(sol2routes(solution)):
            print("Route #%d : %s" % (route_idx+1, route))
            ROUTES.append({"routeId": route_idx+1, "stops": route})

        loader.stop()

        with open("response.json", "w") as outfile:
            json.dump(
                {"success": True, "data": {"routes": ROUTES}}, outfile)

        return ROUTES


if __name__ == "__main__":
    testObj = testFunction()
    ROUTES = testObj.gilletMiller(runFromJson=True, input=None)
