from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from xgboost import XGBRegressor
from sklearn.neural_network import MLPRegressor
from catboost import  CatBoostRegressor
from lightgbm import  LGBMRegressor
from sklearn.ensemble import  RandomForestRegressor


def linear_regression(X_train, y_train):
    """
    Обучение модели линейной регрессии

    X_train: датасет признаков для обучения
    y_train: данные целевого признака, используемые для обучения
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def polynomial_regression(X_train, y_train, degree=2):
    """
    Обучение модели полиномиальной регрессии

    X_train: датасет признаков для обучения
    y_train: данные целевого признака, используемые для обучения
    degree: степень полинома
    """
    poly_features = PolynomialFeatures(degree=degree)
    X_poly = poly_features.fit_transform(X_train)
    model = LinearRegression()
    model.fit(X_poly, y_train)
    return model


def xgb_regressor(X_train, y_train, n_estimators=100, learning_rate=0.1, max_depth=3):
    """
    Обучение модели XGBRegressor

    X_train: датасет признаков для обучения
    y_train: данные целевого признака, используемые для обучения
    n_estimators: количество деревьев в ансамбле
    learning_rate: скорость обучения
    max_depth: максимальная глубина деревьев
    """
    model = XGBRegressor(
        objective ='reg:squarederror',
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=max_depth
    )
    model.fit(X_train, y_train)
    return model


def mlp_regressor(X_train, y_train, hidden_layer_sizes=(100,), activation='relu', max_iter=200):
    """
    Обучение модели MLP (Multi-Layer Perceptron) для регрессии

    Параметры:
    X_train: датасет признаков для обучения
    y_train: данные целевого признака, используемые для обучения
    hidden_layer_sizes: количество нейронов в каждом скрытом слое
    activation: функция активации для скрытых слоев
    max_iter: максимальное количество итераций
    """
    model = MLPRegressor(hidden_layer_sizes=hidden_layer_sizes, activation=activation, max_iter=max_iter)
    model.fit(X_train, y_train)

    return model


def catboost_regressor(X_train, y_train, iterations=100, learning_rate=0.1, depth=6):
    """
    Обучение модели CatBoost

    Параметры:
    X_train: датасет признаков для обучения
    y_train: данные целевого признака, используемые для обучения
    iterations : количество деревьев
    learning_rate : скорость обучения
    depth : максимальная глубина дерева
    """
    model = CatBoostRegressor(iterations=iterations, learning_rate=learning_rate, depth=depth)
    model.fit(X_train, y_train)
    return model


def lightgbm_regressor(X_train, y_train, num_leaves=31, learning_rate=0.1, n_estimators=100):
    """
    Обучение модели LightGBM

    Параметры:
    X_train: датасет признаков для обучения
    y_train: данные целевого признака, используемые для обучения
    num_leaves : максимальное количество листьев в одном дереве
    learning_rate : скорость обучения
    n_estimators : количество деревьев
    """
    model = LGBMRegressor(num_leaves=num_leaves, learning_rate=learning_rate, n_estimators=n_estimators)
    model.fit(X_train, y_train)
    return model


def random_forest_regressor(X_train, y_train, n_estimators=100, max_depth=None, min_samples_split=2):
    """
    Обучение модели RandomForest

    Параметры:
    X_train: датасет признаков для обучения
    y_train: данные целевого признака, используемые для обученияshape (n_samples,)
    n_estimators : количество деревьев в лесу
    max_depth : максимальная глубина дерева
    min_samples_split : минимальное количество выборок для разделения внутреннего узла
    """
    model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, min_samples_split=min_samples_split)
    model.fit(X_train, y_train)
    return model
