from sklearn.cluster import DBSCAN, HDBSCAN, OPTICS, KMeans
import numpy as np


def dbscan(X, eps=0.5, min_samples=5, metric='euclidean'):
    """
    Выполняет кластеризацию DBSCAN на входных данных.
    
    Параметры:
    X : array-like, shape (n_samples, n_features)
        Входные данные для кластеризации.
    eps : float, optional (default=0.5)
        Максимальное расстояние между двумя образцами для их рассмотрения как соседей.
    min_samples : int, optional (default=5)
        Минимальное количество образцов в окрестности для основных точек.
    metric : string, or callable, optional (default='euclidean')
        Метрика для вычисления расстояния между экземплярами в наборе данных.
    
    Возвращает:
    labels : array, shape (n_samples,)
        Метки кластеров для каждой точки в наборе данных.
    n_clusters : int
        Количество кластеров, найденных алгоритмом.
    """
    # Создаем и применяем модель DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric=metric)
    labels = dbscan.fit_predict(X)
    
    # Определяем количество кластеров
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    print("Кол-во кластеров:", n_clusters,"\n")
    
    return labels


def hdbscan_clustering(X, min_cluster_size=5, min_samples=None):
    """
    Выполняет кластеризацию с помощью алгоритма HDBSCAN.

    Параметры:
    X: входные данные для кластеризации
    min_cluster_size:  минимальный размер кластера
    min_samples:  минимальное количество образцов в окрестности точки

    Возвращает:
    return:  метки кластеров для каждой точки данных
    """
    clusterer = HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples)
    cluster_labels = clusterer.fit_predict(X)

    return cluster_labels


def optics_clustering(X, min_samples=5, max_eps=np.inf):
    """
    Выполняет кластеризацию с помощью алгоритма OPTICS.

    Параметры:
    X: входные данные для кластеризации
    min_samples: минимальное количество образцов в окрестности точки
    max_eps: максимальное расстояние между двумя образцами для формирования кластера

    Возвращает:
    cluster_labels: метки кластеров для каждой точки данных
    """
    clusterer = OPTICS(min_samples=min_samples, max_eps=max_eps)
    cluster_labels = clusterer.fit_predict(X)

    return cluster_labels


def kmeans_clustering(X, n_clusters=8, random_state=None):
    """
    Выполняет кластеризацию с помощью алгоритма K-Means.

    Параметры:
    X: входные данные для кластеризации
    n_clusters: количество кластеров
    random_state: начальное значение для генератора случайных чисел

    Возвращает:
    cluster_labels: метки кластеров для каждой точки данных
    """
    clusterer = KMeans(n_clusters=n_clusters, random_state=random_state)
    cluster_labels = clusterer.fit_predict(X)

    return cluster_labels
