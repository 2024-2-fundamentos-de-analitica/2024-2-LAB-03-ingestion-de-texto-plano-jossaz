"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
import re

def load_data(input):
  datos = []
  with open(input, 'rt', encoding='utf-8') as f:
    file = f.read()
    line = []

    # Se toma cada caracter en raw de cada fila del archivo y se mete en datos[]
    for char in file:
      # Si es algo diferente a un salto de linea, se mete a line[]
      if char != '\n':
        line.append(char)

      # Si es un salto de linea, se mete line a datos, esto correcponde a una fila.
      else:
        datos.append(line)
        line = []
  return datos



def clean_data(text):
  cleaned_text = []
  for line in text:
    # Se convierte de caracteres a una cadena entera:
    datos = ''.join(line)
    # Reemplaza saltos de linea con un espacio:
    datos = re.sub(r"\n", " ", datos)
    # Elimina % y puntos
    datos =  re.sub(r"[.%]", "", datos)
    # Reemplaza tabs y espacios multiples, por 1 unico espacio
    datos = re.sub(r"\s+", " ", datos)
    # Elimina cualquier otro espacio fuera de lugar(al comienzo y final)
    datos = datos.strip()
    # Lo llevamos todo a minusculas
    datos = datos.lower()


    cleaned_text.append(datos)
  # Se eliminan las filas del encabezado y separador, que no nos interesan
  del(cleaned_text[0:4])
  return cleaned_text


# Aqui convertiremos el texto a un diccionario, la clave será el número del cluster
# Los valores de cada clave serán las palabras separadas en una lista.
def text_to_dic(text):
  # Patron que separa los primeros 3 números(si los hay) y el texto
  patron = r'\d+(?:,\d+)?'
  dic = {}

  clave = 0
  for line in text:
    numeros = re.findall(patron, line)

    # Implica que es una cadena con números(una inicial)
    if numeros:
      clave = int(numeros[0])
      dic[clave] = []
      dic[clave].append(int(numeros[1]))
      # Aqui se cambia la coma del numero, por un punto flotante
      dic[clave].append(float(numeros[2].replace(',','.')))

      # Le retiramos el texto de los números al texto de letras
      texto = ' '.join(numeros) + ' '
      line = line.replace(texto, '')
      # Se añade el texto al diccionario
      dic[clave].append(line)

    # Si la linea esta vacia
    elif line == '':
      continue
    # Si solo es texto
    else:
      # Se concatena la el texto, para que quede solo una larga linea de texto
      dic[clave][2] = dic[clave][2] + ' ' + line

  return dic





  


data = load_data('files/input/clusters_report.txt')
data = clean_data(data)
data = text_to_dic(data)





def pregunta_01():
    data = load_data('files/input/clusters_report.txt')
    data = clean_data(data)
    data = text_to_dic(data)

    # Procesar los datos
    processed_data = []

    for cluster, values in data.items():
        cantidad_de_palabras_clave = values[0]
        porcentaje_de_palabras_clave = values[1]
        principales_palabras_clave = values[2]

        # palabras_clave = values[2].split(', ')  # Separar las palabras clave por coma
        # principales_palabras_clave = ', '.join(palabras_clave)
        
        processed_data.append({
            'cluster': cluster,
            'cantidad_de_palabras_clave': cantidad_de_palabras_clave,
            'porcentaje_de_palabras_clave': porcentaje_de_palabras_clave,
            'principales_palabras_clave': principales_palabras_clave
        })

    # Crear el DataFrame
    df = pd.DataFrame(processed_data, columns=['cluster', 'cantidad_de_palabras_clave', 'porcentaje_de_palabras_clave', 'principales_palabras_clave'])
    return df


"""
Construya y retorne un dataframe de Pandas a partir del archivo
'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

- El dataframe tiene la misma estructura que el archivo original.
- Los nombres de las columnas deben ser en minusculas, reemplazando los
  espacios por guiones bajos.
- Las palabras clave deben estar separadas por coma y con un solo
  espacio entre palabra y palabra.


"""
