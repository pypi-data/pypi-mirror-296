import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import ipywidgets as widgets

# Función para el test de Kolmogorov-Smirnov con la opción de visualizar la curva normal y los porcentajes
def kolmogorov_test(
    dataset,
    variable: str,
    transformation: str = None,
    plot_histogram: bool = False,
    bins: int = 30,
    color: str = None,
    language: str = 'English',
    show_normal_curve: bool = False,  # Mostrar la curva normal
    show_percent: bool = False,       # Mostrar los porcentajes en lugar de los conteos
    print_test: bool = True,
    return_test: bool = False,
    plotly_renderer: str = "notebook",
):
    if type(dataset) == dict:
        dataset = pd.DataFrame(dataset)

    dataset = dataset.dropna(subset=[variable]).copy()

    if transformation == "yeo_johnson":
        x = stats.yeojohnson(dataset[variable].to_numpy())[0]
    elif transformation == "log":
        x = np.log1p(dataset[variable].to_numpy())
    else:
        x = dataset[variable].to_numpy()

    # Normalizamos los datos
    x_scale = (x - x.mean()) / x.std()

    # Test de Kolmogorov-Smirnov
    ktest = stats.kstest(x_scale, "norm")

    if print_test:
        if language == 'English':
            print(f"------------------------- Kolmogorov test for the variable {variable} --------------------")
            print(f"statistic={ktest[0]:.3f}, p_value={ktest[1]:.3f}\n")
            if ktest[1] < 0.05:
                print(f"Since {ktest[1]:.3f} < 0.05, you can reject the null hypothesis, so the variable {variable} does not follow a normal distribution.")
                conclusion = "Not normal distribution"
            else:
                print(f"Since {ktest[1]:.3f} > 0.05, you cannot reject the null hypothesis, so the variable {variable} follows a normal distribution.")
                conclusion = "Normal distribution"
            print("-------------------------------------------------------------------------------------------\n")
        elif language == 'Español':
            print(f"------------------------- Prueba de Kolmogorov para la variable {variable} --------------------")
            print(f"estadístico={ktest[0]:.3f}, valor p={ktest[1]:.3f}\n")
            if ktest[1] < 0.05:
                print(f"Como {ktest[1]:.3f} < 0.05, puedes rechazar la hipótesis nula, por lo que la variable {variable} no sigue una distribución normal.")
                conclusion = "Distribución no normal"
            else:
                print(f"Como {ktest[1]:.3f} > 0.05, no puedes rechazar la hipótesis nula, por lo que la variable {variable} sigue una distribución normal.")
                conclusion = "Distribución normal"
            print("-------------------------------------------------------------------------------------------\n")

    if plot_histogram:
        # Cambiamos el histnorm a 'percent' si se selecciona la opción de mostrar porcentajes
        histnorm = 'percent' if show_percent else None

        # Graficar el histograma de los datos con las etiquetas de texto (text_auto=True)
        fig = px.histogram(dataset, x=x, nbins=bins, marginal="box", color=color, barmode="overlay", histnorm=histnorm, text_auto=True)
        fig.update_traces(marker_line_width=1, marker_line_color="white", opacity=0.8)

        # Actualizamos el título del eje Y dependiendo de si mostramos porcentajes o conteos
        yaxis_title = 'Percentage' if show_percent else 'Count'
        fig.update_layout(xaxis_title=variable, yaxis_title=yaxis_title, width=1500, height=500)

        # Solo añadimos la curva de la distribución normal si el checkbox está activado
        if show_normal_curve:
            x_vals = np.linspace(x.min(), x.max(), 100)
            normal_vals = stats.norm.pdf(x_vals, x.mean(), x.std())

            # Ajustar la curva normal al histograma
            normal_vals = normal_vals * len(x) * (x.max() - x.min()) / bins if not show_percent else normal_vals

            # Añadir la curva normal como una línea roja
            fig.add_trace(go.Scatter(x=x_vals, y=normal_vals, mode='lines', name='Normal Distribution', line=dict(color='red', width=2)))

        # Mostrar el gráfico
        fig.show(renderer=plotly_renderer)

# Función principal para llamar al widget interactivo
def kolmogorov_widget(dataset):
    # Filtrar solo las columnas numéricas
    numeric_columns = dataset.select_dtypes(include=[np.number]).columns

    # Crear widgets interactivos
    variable_selector = widgets.Dropdown(
        options=numeric_columns, 
        description='Variable:',
        disabled=False,
    )
    
    transformation_selector = widgets.Dropdown(
        options=[None, 'log', 'yeo_johnson'],
        value=None,
        description='Transform:',
        disabled=False,
    )
    
    plot_hist_selector = widgets.Checkbox(
        value=True,
        description='Plot Histogram',
        disabled=False,
    )
    
    bins_selector = widgets.IntSlider(
        value=30,
        min=5,
        max=100,
        step=1,
        description='Bins:',
        continuous_update=False
    )
    
    color_selector = widgets.Dropdown(
        options=[None] + list(dataset.columns),
        value=None,
        description='Color by:',
        disabled=False,
    )
    
    # Nuevo selector de idioma
    language_selector = widgets.Dropdown(
        options=['English', 'Español'],
        value='English',
        description='Language:',
        disabled=False,
    )

    # Checkbox para mostrar/ocultar la curva normal
    normal_curve_selector = widgets.Checkbox(
        value=False,
        description='Show Normal Curve',
        disabled=False,
    )

    # Checkbox para mostrar los porcentajes en lugar de conteos
    percent_selector = widgets.Checkbox(
        value=False,
        description='Show Percentages',
        disabled=False,
    )

    # Función para actualizar el gráfico y realizar el test
    def update_kstest(variable, transformation, plot_histogram, bins, color, language, show_normal_curve, show_percent):
        kolmogorov_test(
            dataset=dataset,
            variable=variable,
            transformation=transformation,
            plot_histogram=plot_histogram,
            bins=bins,
            color=color,
            language=language,
            show_normal_curve=show_normal_curve,  # Mostrar curva normal
            show_percent=show_percent,            # Mostrar porcentajes
            plotly_renderer="notebook"
        )
    
    # Conectar los widgets a la función
    widgets.interact(update_kstest, 
                     variable=variable_selector, 
                     transformation=transformation_selector, 
                     plot_histogram=plot_hist_selector,
                     bins=bins_selector,
                     color=color_selector,
                     language=language_selector,
                     show_normal_curve=normal_curve_selector,  # Conectar el checkbox para la curva normal
                     show_percent=percent_selector)  # Conectar el checkbox para porcentajes
