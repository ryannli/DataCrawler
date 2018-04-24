import operator
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.optimize import curve_fit

IMAGE_DIR = "../img/"


def hub_actors(graph, number=10, save_fig=True):
    """
    Create data analysis with image for hub actors in graph
    :param graph: the input graph
    :param number: the maximum number of actors for analysis image
    :param save_fig: if we expect to save the image or not
    :return: a list of actor names with connection numbers
    """
    actor_vertices = graph.get_actor_vertices()
    for actor_name in actor_vertices:
        actor_vertices[actor_name].set_compare_value(len(actor_vertices[actor_name].get_siblings()))

    sorted_actors = sorted(actor_vertices.items(), key=operator.itemgetter(1))
    # Selects the "number" of tail
    sorted_actors = sorted_actors[:-(number + 1):-1]

    actor_names, conn_numbers = [], []
    for actor in sorted_actors:
        actor_name = actor[0]
        conn_number = actor_vertices[actor_name].get_compare_value()
        actor_names.append(actor_name)
        conn_numbers.append(conn_number)

    # Create chart and save image
    create_bar_chart(actor_names, conn_numbers, xlabel="Actor Names", ylabel='Actor Connection Number',
                     title="Hub Actor Analysis", save_fig=save_fig)

    return list(zip(actor_names, conn_numbers))


def grossing_vs_age(graph, save_fig=True):
    """
    Create the data analysis about relationship between grossing value and actor age. Generates a scatter plot with
    fitted polynomial curve on result.
    :param graph: the input graph
    :param save_fig: if we expect to save the image or not
    """
    actor_vertices = graph.get_actor_vertices()
    relation = defaultdict(float)
    count = defaultdict(int)
    for actor_name in actor_vertices:
        content = actor_vertices[actor_name].get_content()
        if content['age'] > 0 and content['total_gross'] > 0:
            relation[content['age']] += content['total_gross']
            count[content['age']] += 1
    for age in relation:
        relation[age] /= count[age]

    ages, grossings = get_sorted_lists_from_dict(relation)

    create_scatter_fit_curve(ages, grossings, xlabel="Age Range", ylabel="Average Grossing"
                             , title="Correlation between Age and Grossing Value", save_fig=save_fig)


def movie_year_percentage(graph, save_fig=True):
    """
    Create the data analysis about movie yearly production and build pie chart for presentation
    :param graph: the input graph
    :param save_fig: if we expect to save the image or not
    """
    relation = defaultdict(int)
    movie_vertices = graph.get_movie_vertices()
    for movie_name in movie_vertices:
        content = movie_vertices[movie_name].get_content()
        if content['year'] > 1800:
            relation[content['year'] // 10 * 10] += 1

    years, movie_numbers = get_sorted_lists_from_dict(relation)
    years = [str(year) + "s" for year in years]
    create_pie_chart(years, movie_numbers, "Movie Production and Year", save_fig=save_fig)


def create_bar_chart(X, Y, xlabel, ylabel, title, save_fig):
    """
    Create and save a bar chart by X values and Y values
    :param X: the list of X coordinate values
    :param Y: the list of Y coordinate values
    :param xlabel: the name of x label
    :param ylabel: the name of y label
    :param title: the title of image
    :param save_fig: if we expect to save the image or not
    """
    assert len(X) == len(Y)
    y_pos = np.arange(len(X))

    cm = plt.cm.get_cmap('RdYlBu_r')

    C = [cm((pos / len(y_pos))) for pos in y_pos]
    rects = plt.bar(y_pos, Y, align='center', alpha=0.5, color=C)
    plt.xticks(y_pos, X)
    plt.xticks(rotation=75)
    autolabel(rects)

    plt.ylabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    if save_fig:
        plt.savefig("../img/" + title)


def create_scatter_fit_curve(X, Y, xlabel, ylabel, title, save_fig):
    """
    Create and save scatter plot of X and Y along with the fitted curve
    Tutorial: http://blog.csdn.net/vola9527/article/details/40402189;
    https://matplotlib.org/gallery/shapes_and_collections/scatter.html#sphx-glr-gallery-shapes-and-collections-scatter-py

    :param X: the list of X coordinate values
    :param Y: the list of Y coordinate values
    :param xlabel: the name of x label
    :param ylabel: the name of y label
    :param title: the title of image
    :param save_fig: if we expect to save the image or not
    """
    plt.clf()
    z2 = np.polyfit(np.array(X), np.array(Y), 6)
    # generate polynomial
    p2 = np.poly1d(z2)
    colors = np.random.rand(len(X))
    area = np.pi * (np.random.randint(3, 5, size=len(X))) ** 2  # 3 to 5 point random integer
    plt.scatter(X, Y, s=area, c=colors, alpha=0.5)
    plt.plot(X, p2(X), 'r*')
    plt.ylabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if save_fig:
        plt.savefig("../img/" + title)


def create_pie_chart(names, sizes, title, save_fig):
    """
    Create and save pie chart
    :param names: the name of each group
    :param sizes: the list of sizes
    :param title: the title of the image
    :param save_fig: if we expect to save the image or not
    """
    plt.clf()
    cm = plt.cm.get_cmap('RdYlBu_r')
    C = [cm((i / len(sizes))) for i, pos in enumerate(sizes)]
    max_size = max(sizes)
    explode = [0.1 if size == max_size else 0.0 for size in sizes]  # explode 1st slice
    patches, texts, _ = plt.pie(sizes, labels=names, colors=C, explode=explode,
                                autopct='%1.1f%%', shadow=True, startangle=140)
    plt.legend(patches, names, loc=4)
    plt.axis("equal")
    plt.title(title)
    if save_fig:
        plt.savefig("../img/" + title)


def autolabel(rects):
    """
    Set auto labels for plt bar graphs
    Tutorial: https://matplotlib.org/xkcd/examples/pylab_examples/barchart_demo.html
    :param rects: the object returned by plt.bar
    """
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2., height, '%d' % int(height),
                 ha='center', va='bottom')


def get_sorted_lists_from_dict(input_dict):
    """
    Get keys and values sorted by keys from a dict
    :param input_dict: the input dictionary
    :return: the list of sorted keys and values
    """
    X = []
    Y = []
    for x, y in sorted(input_dict.items(), key=operator.itemgetter(0)):
        X.append(x)
        Y.append(y)
    return X, Y
