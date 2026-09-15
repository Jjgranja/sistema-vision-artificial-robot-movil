# Dataset del modelo personalizado

El modelo personalizado utilizado en el trabajo fue entrenado con un conjunto final de **301 imágenes**.

## Distribución

| Partición | Imágenes | Porcentaje |
|---|---:|---:|
| Entrenamiento | 241 | 80.07 % |
| Validación | 40 | 13.29 % |
| Prueba | 20 | 6.64 % |
| **Total** | **301** | **100 %** |

## Clases finales

- `door`
- `wall`
- `window`

La clase `furniture` estuvo presente durante etapas previas del proyecto, pero fue excluida del catálogo final debido a su comportamiento ambiguo y a la superposición con categorías ya reconocidas por el modelo base.

## Preparación

Las imágenes fueron organizadas y anotadas mediante Roboflow usando cajas delimitadoras. Este directorio documenta el conjunto utilizado en el proyecto; las imágenes originales no se incluyen en el repositorio público por tamaño y organización del material de trabajo.
