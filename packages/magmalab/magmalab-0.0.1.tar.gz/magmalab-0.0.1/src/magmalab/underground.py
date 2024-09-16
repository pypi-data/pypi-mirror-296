import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ipywidgets import HBox, VBox, IntSlider, Dropdown
from IPython.display import display, clear_output

class MiningVisualizer:
    def __init__(self, df, continuous_columns, discrete_columns, width = 1000, height = 600, subset = ['X', 'Y', 'Z'], marker_size = 5, η = 0.15, colab = False):
        self.df = df
        self.continuous_columns = continuous_columns
        self.discrete_columns = discrete_columns
        self.x, self.y, self.z = subset
        self.marker_size = marker_size
        self.η = η
        self.colab = colab
        
        # Apply margin calculation
        x_range = df[self.x].max() - df[self.x].min()
        y_range = df[self.y].max() - df[self.y].min()
        z_range = df[self.z].max() - df[self.z].min()

        # Calculate observed ranges for x, y, z from the dfFrame
        self.xlim = (df[self.x].min() - self.η * x_range, df[self.x].max() + self.η * x_range)
        self.ylim = (df[self.y].min() - self.η * y_range, df[self.y].max() + self.η * y_range)
        self.zlim = (df[self.z].min() - self.η * z_range, df[self.z].max() + self.η * z_range)

        # Create the figure with 3D specs
        self.fig = go.FigureWidget(make_subplots(specs = [[{'is_3d': True}]]))
        self.fig.layout.width = width
        self.fig.layout.height = height

        # Set the axis limits to the observed ranges
        self.fig.update_layout(scene = dict(xaxis = dict(range = self.xlim), yaxis = dict(range = self.ylim), zaxis = dict(range = self.zlim)))

        self.filter_type_dropdown = Dropdown(options = ['None', 'Continuous', 'Discrete'], value = 'None', description = 'Filter Type:')
        self.variable_dropdown = Dropdown(options = [], description = 'Variable:', visible = False)
        self.marker_size_slider = IntSlider(value = marker_size, min = 1, max = 20, step = 1, description = 'Marker Size:')

        self.filter_type_dropdown.observe(self.update_ui, names = 'value')
        self.variable_dropdown.observe(self.update_plot, names = 'value')
        self.marker_size_slider.observe(self.update_marker_size, names = 'value')

    def update_ui(self, change):
        filter_type = self.filter_type_dropdown.value
        if filter_type ==  'Continuous':
            self.variable_dropdown.options = self.continuous_columns
        elif filter_type ==  'Discrete':
            self.variable_dropdown.options = self.discrete_columns
        else:
            self.variable_dropdown.options = []
        self.update_plot(None)

    def update_marker_size(self, change):
        self.marker_size = self.marker_size_slider.value
        self.update_plot(None)
        
    def update_plot(self, change):
        self.fig.data = [] 
        filter_type = self.filter_type_dropdown.value
        selected_var = self.variable_dropdown.value

        df = self.df.dropna(subset = [self.x, self.y, self.z, selected_var] if selected_var != None else [self.x, self.y, self.z])
        trace = dict(x = df[self.x], y = df[self.y], z = df[self.z], mode = 'markers', marker = dict(size = self.marker_size))

        if filter_type ==  'Discrete' and selected_var:
            for category in df[selected_var].unique():
                data = df[df[selected_var] ==  category]
                trace['x'] = data[self.x]
                trace['y'] = data[self.y]
                trace['z'] = data[self.z]
                trace['name'] = f'{selected_var}: {category}'
                self.fig.add_trace(go.Scatter3d(**trace))
        elif filter_type == 'Continuous' and selected_var:
            trace['marker']['color'] = df[selected_var]
            trace['marker']['colorscale'] = 'Turbo'
            trace['marker']['colorbar'] = dict(title=selected_var)
            trace['hovertemplate'] = (f"<b>{self.x}:</b> {{%{{x}}}}<br>"f"<b>{self.y}:</b> {{%{{y}}}}<br>"f"<b>{self.z}:</b> {{%{{z}}}}<br>"f"<b>{selected_var}:</b> {{%{{marker.color}}}}<extra></extra>")
            self.fig.add_trace(go.Scatter3d(**trace))
        else:
            self.fig.add_trace(go.Scatter3d(**trace))

        self.fig.update_layout(scene = dict(xaxis = dict(range = self.xlim), yaxis = dict(range = self.ylim), zaxis = dict(range = self.zlim)))
        
        if self.colab:  
          # Clear only the output for the figure
          clear_output(wait = True)
          display(self.ui)
          self.fig.show()

    def show(self):
        self.ui = VBox([HBox([self.filter_type_dropdown, self.variable_dropdown]), self.marker_size_slider])
        if self.colab:
          from google.colab import output
          output.enable_custom_widget_manager()
          display(self.ui)
        else:
          display(self.ui, self.fig)
        self.update_plot(None)
    
    def save(self, file_name="visualization.html"):
        self.fig.write_html(file_name)
        print(f"Visualization saved to {file_name}")


class Drillhole:
    def __init__(self, collar, survey):
        # Inicializa o Drillhole com os DataFrames de collar e survey copiados
        self.collar = collar.copy()
        self.survey = survey.copy()

    def desurvey(self):
        # Criação do DataFrame
        self.drillhole = self.survey.copy()
        self.drillhole['DIP'] = 90 - self.drillhole['DIP'] if self.drillhole['DIP'].mean() > 45 else self.drillhole['DIP']

        # Inicializa as coordenadas x, y, z como NaN
        self.drillhole[['X', 'Y', 'Z']] = np.nan

        # Ordena os dados por BHID e profundidade (AT)
        self.drillhole.sort_values(by=['BHID', 'AT'], inplace=True)

        # Processa cada grupo de dados por BHID
        for bhid, group in self.drillhole.groupby('BHID'):
            # Seleciona os dados de collar correspondentes ao BHID atual
            collar_row = self.collar[self.collar['BHID'] == bhid]

            # Verifica se os dados necessários estão disponíveis e se não estão nulos
            if collar_row.empty or group[['AT', 'DIP', 'AZ']].isna().any().any():
                print(f"Skipping BHID {bhid}: Missing data.")
                continue

            # Extrai as coordenadas iniciais do collar e dados de inclinação e azimute
            x0, y0, z0 = collar_row[['XCOLLAR', 'YCOLLAR', 'ZCOLLAR']].iloc[0].values
            AT, DIP, AZ = group['AT'].values, group['DIP'].values, group['AZ'].values
            
            # Verifica se os ângulos de inclinação são válidos
            if not ((0 <= DIP).all() and (DIP <= 90).all()):
                print(f"Skipping BHID {bhid}: Invalid dip angles.")
                continue

            # Inicializa as coordenadas para o cálculo
            x, y, z = np.zeros_like(AT, dtype=float), np.zeros_like(AT, dtype=float), np.zeros_like(AT, dtype=float)
            x[0], y[0], z[0] = x0, y0, z0

            # Itera sobre os segmentos para calcular as novas coordenadas
            for i in range(1, len(AT)):
                dx, dy, dz = self.minimum_curvature(AT[i-1], AT[i], DIP[i-1], DIP[i], AZ[i-1], AZ[i])
                x[i] = x[i-1] + dx
                y[i] = y[i-1] + dy
                z[i] = z[i-1] - dz

            # Atualiza o DataFrame survey com as novas coordenadas
            self.drillhole.loc[group.index, 'X'] = x
            self.drillhole.loc[group.index, 'Y'] = y
            self.drillhole.loc[group.index, 'Z'] = z

        self.drillhole = self.drillhole.merge(self.collar, on = 'BHID', how = 'inner')

    def minimum_curvature(self, md1, md2, inc1, inc2, az1, az2):
        # Conversão de graus para radianos
        inc1_rad, inc2_rad = np.radians(inc1), np.radians(inc2)
        az1_rad, az2_rad = np.radians(az1), np.radians(az2)
        
        # Cálculo do ângulo dog-leg
        beta = np.arccos(np.cos(inc2_rad - inc1_rad) - np.sin(inc1_rad) * np.sin(inc2_rad) * (1 - np.cos(az2_rad - az1_rad)))

        # Cálculo do fator de rácio (Ratio Factor, RF)
        if beta == 0:
            rf = 1  # Evita divisão por zero
        else:   
            rf = 2 / beta * np.tan(beta / 2)
        
        # Distância medida entre os pontos
        delta_md = md2 - md1
        
        # Cálculo das mudanças em Norte, Leste e TVD
        north = delta_md / 2 * (np.sin(inc1_rad) * np.cos(az1_rad) + np.sin(inc2_rad) * np.cos(az2_rad)) * rf
        east = delta_md / 2 * (np.sin(inc1_rad) * np.sin(az1_rad) + np.sin(inc2_rad) * np.sin(az2_rad)) * rf
        tvd = delta_md / 2 * (np.cos(inc1_rad) + np.cos(inc2_rad )) * rf

        return east, north, tvd
    
def plot_drillholes_3d(drillhole):
    fig = go.Figure()

    for bhid, group in drillhole.groupby('BHID'):
        fig.add_trace(go.Scatter3d(
            x=group['X'],
            y=group['Y'],
            z=group['Z'],
            mode='lines',
            line=dict(width=8),  # Aumente o valor de 'width' para a espessura desejada
            name=bhid,
            text=bhid,
            hoverinfo='text'
        ))

    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        ),
        title='3D Drillhole Plot'
    )

    return fig

