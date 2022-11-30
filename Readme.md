create virtual env
python3 -m venv mle
source mle/bin/activate

Pregunta 1.
-- Al desconocer el objetivo de las areas de negocios se decidirá arbitrariamente el objetivo de negocio. el cual es será maximizar la precision en las predicciones de atrasos y aceptar algunos errores en la prediccion para casos de atraso como no atrasos. El modelo obtenido con la tecnica xgboost y sus metricas con hiperparametriacion, serían las mejores metricas obtenidas en base a la experimentacion del modelo.
ahora hay que considerar que le modelo tiene un desbalance de clases alto pese al haber utilizado algunas tecnicas de upsampling. en metricas este modelo es el que posee mas "equilibrio" al momento de entregar respuestas a la condicion de atrasos o no atrasos



* aspectos claves
el modelo por si solo toma la informacion desde la salida y no tiene inputs para el momento de llegada, en sí no se manejan dispositivos IOT que ayuden a mejorar las predicciones en medio dle vuelo

* evaluacion de feature engineering

quiza una de las mayores debilidades del modelo al manejar las fechas, es la falta de la utilizacion de UTC el cual podriamos inferir respecto al pais y hacer un cruce de informacion según las fechas, podriamos cuadrar esto con alguna API de confianza, así funciones como "diferencia de tiempo" o tiempos de vuelo será real y no tendremos los falsos tiempos en nuestros features

Otro problema visible en los features es el sesgo de los casos positivos/negativos (55592/12614)
por lo tanto estrategias de upsampling basicas no seán una gran ayuda, solo aumentar margenes de error



pregunta 2.

generado

Pregunta 3.

api + github/workflow

Se generá una API basica para consumo de modelos, considerando el uso de un modelo mas bien primitivo, se enviará mediante variable de ambiente la locacion del modelo



