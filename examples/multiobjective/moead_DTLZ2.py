from jmetal.algorithm.multiobjective.moead import MOEAD
from jmetal.operator import PolynomialMutation, DifferentialEvolutionCrossover
from jmetal.problem import LZ09_F2, DTLZ1, DTLZ2
from jmetal.problem.multiobjective.lz09 import LZ09_F9, LZ09_F5, LZ09_F6
from jmetal.util.aggregative_function import Tschebycheff
from jmetal.util.neighborhood import WeightVectorNeighborhood
from jmetal.util.observer import ProgressBarObserver, VisualizerObserver, PlotFrontToFileObserver
from jmetal.util.solution_list import read_solutions, print_function_values_to_file, print_variables_to_file
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.visualization import Plot, InteractivePlot

if __name__ == '__main__':
    problem = DTLZ2()
    problem.reference_front = read_solutions(filename='../../resources/reference_front/DTLZ2.3D.pf'.format(problem.get_name()))

    population_size = 300
    max_evaluations = 150000

    algorithm = MOEAD(
        problem=problem,
        population_size=population_size,
        crossover=DifferentialEvolutionCrossover(CR=1.0, F=0.5, K=0.5),
        mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
        aggregative_function=Tschebycheff(dimension=problem.number_of_objectives),
        neighbor_size=20,
        neighbourhood_selection_probability=0.9,
        max_number_of_replaced_solutions=2,
        termination_criterion=StoppingByEvaluations(max=max_evaluations),
        weight_files_path = "../../resources/MOEAD_weights"
    )

    progress_bar = ProgressBarObserver(max=max_evaluations)
    algorithm.observable.register(observer=progress_bar)
    algorithm.observable.register(observer=VisualizerObserver(reference_front=problem.reference_front, display_frequency=1000))

    algorithm.run()
    front = algorithm.get_result()

    label = algorithm.get_name() + "." + problem.get_name()
    algorithm_name = label

    # Plot front
    plot_front = Plot(plot_title='Pareto front approximation', axis_labels=problem.obj_labels)
    plot_front.plot(front, label=label, filename=algorithm_name)

    # Plot interactive front
    plot_front = InteractivePlot(plot_title='Pareto front approximation', axis_labels=problem.obj_labels)
    plot_front.plot(front, label=label, filename=algorithm_name)

    # Save results to file
    print_function_values_to_file(front, 'FUN.' + label)
    print_variables_to_file(front, 'VAR.'+ label)

    print('Algorithm (continuous problem): ' + algorithm.get_name())
    print('Problem: ' + problem.get_name())
    print('Computing time: ' + str(algorithm.total_computing_time))