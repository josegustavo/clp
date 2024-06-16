**Diapositiva 1**

- Buenas días a todos. Mi nombre es Gustavo Quilca, mi tutor Javier Alcaraz. Hoy voy a presentar el trabajo titulado "Optimización del Llenado Manual de Contenedores con Paquetes Heterogéneos".

**Diapositiva 2**

- La presentación se dividirá en las siguientes secciones: una Introducción, el contexto de problema, propuesta de solución con un Algoritmo Genético, validación de la solución con un Estudio Computacional, finalmente las Conclusiones.

**Diapositiva 3**

- Veamos la introducción

**Diapositiva 4**

- El problema de llenado de contenedores (CLP) es un problema clásico de optimización combinatoria que se enfoca en encontrar la mejor manera de llenar un contenedor con paquetes de distintos tamaños, optimizando el uso del espacio. Este problema tiene importantes aplicaciones en logística, transporte y almacenamiento.

**Diapositiva 5**

En el CLP, las restricciones básicas incluyen evitar la superposición de paquetes, no superar el peso máximo del contenedor y asegurar que todos los paquetes estén dentro de los límites del contenedor. Además, hay restricciones prácticas que consideran la estabilidad de los paquetes, el centro de gravedad del contenedor, la prioridad de carga y la contigüidad de tipos, entre otros.

**Diapositiva 6**

En la literatura, se han propuesto distintos métodos para resolver el CLP. Los métodos exactos garantizan la solución óptima pero son computacionalmente costosos. Los métodos heurísticos proporcionan soluciones de buena calidad en un tiempo razonable. Los métodos metaheurísticos son estrategias flexibles de alto nivel diseñadas para desarrollar algoritmos que resuelven problemas específicos.

**Diapositiva 7**

-- Pasemos a ver ¿Cuál es el contexto del problema?

**Diapositiva 8**

- Se trata de una empresa que se dedica a enviar paquetes en contenedores marítimos, sin control sobre las medidas de los paquetes y con una cantidad máxima disponible para cada tipo. Además, la empresa envía un solo contenedor a la vez y utiliza procedimientos manuales para su llenado.

**Diapositiva 9**

- El objetivo es maximizar el beneficio de la carga de un contenedor con los paquetes disponibles.
- Para facilitar la carga manual, se debe asegurar la estabilidad de los paquetes apilados y que todos los paquetes del mismo tipo estén agrupados. Además, los paquetes del mismo tipo son rotados en una misma dirección.

**Diapositiva 10**

- Formalmente, se puede decir que, se busca optimizar la carga de un contenedor, determinando el orden, la cantidad y la rotación de los tipos de paquetes, cumpliendo con las restricciones prácticas del llenado manual.
- Por ejemplo en la imagen se puede observar al operario que recibe los paquetes en serie y los coloca en el contenedor, siguiendo un procedimiento específico.

**Diapositiva 11**

- Ahora la propuesta de solución ¿Qué es un algoritmo genético?

**Diapositiva 12**

- Un Algoritmo Genético es una técnica de optimización inspirada en la evolución natural.
- Los pasos incluyen la generación y evaluación de una población inicial
- luego selección, cruce, mutación y volver a evaluar hasta cumplir un criterio de parada.

**Diapositiva 13**

- Se utiliza una codificación específica con 3 listas para representar el orden de llenado.
- Por ejemplo, en la imagen, se muestra que primero ingresan 27 paquetes de tipo 2 al contenedor sin aplicar rotación (rotación 0). Luego, ingresan 10 paquetes de tipo 1 aplicando rotación, y así sucesivamente.
- Esto ayuda a garantizar la factibilidad y especifica la forma en la que los paquetes llegarían al operario.

**Diapositiva 14**

- La función de evaluación calcula el beneficio total de la carga y verifica la factibilidad de las soluciones.
- Se necesita un algoritmo que imita el procedimiento de llenado manual.

**Diapositiva 15**

- Se basa en el algoritmo conocido como DBLF.
- El primer paso es introducir un paquete en el contenedor.
- Luego, se generan tres nuevos subespacios. uno frontal, uno lateral y uno superior.
- Cada subespacio es considerado como un nuevo contenedor vacío y se repite el proceso recursivo de llenar un paquete hasta que se acaben los espacios.

**Diapositiva 16**

- Este algoritmo se adapta al problema, para que se pueda unir subespacios vacíos, también para eliminar subespacios inaccesibles y subespacios profundos para mejorar el proceso de llenado.

**Diapositiva 17**

- Los procedimientos internos para hacer estas mejoras son complejas ya que se trabaja todo el tiempo con subespacios en tres dimensiones, estructuras de datos complejas y restricciones reales, por lo que los algoritmos no son triviales ni sencillos de implementar.

**Diapositiva 18**

- Veamos un ejemplo, tenemos un conjunto de 20 paquetes distintos, cada uno representado por un color.
- Viendo desde el primer elemento de la solución, se interpreta como, primero se cargan 24 paquetes plomos aplicando rotación, luego 18 paquetes naranjas sin rotación, continuando por 42 paquetes celestes sin rotación y así sucesivamente.
- Ahora veamos una animación de cómo se realiza el llenado manual.
- Como se puede ver los paquetes entran de uno en uno y son colocados en una posición correspondiente, este procedimiento es el mismo que realizan los operadores, la complejidad aumenta cuando paquetes de distintos tamaños son apilados o colocados completando espacios laterales, pero el algoritmo es determinista lo que quiere decir que cada solución tendrá una única forma de ser llenado.

**Diapositiva 19**

- Continuamos con el algoritmo genético.
- Comienza con la generación aleatoria de la población inicial y la selección mediante torneo binario.

**Diapositiva 20**

- Luego, se realiza el cruce adaptado para permutaciones lo que evita generar soluciones inválidas.

**Diapositiva 21**

- La mutación se aplica de tres formas distintas, intercambiando dos elementos, aplicando rotación a un paquete o cambiando la cantidad de paquetes de un tipo.

**Diapositiva 22**

- El procedimiento de mejora de soluciones es una técnica que ayuda a llenar los espacios vacíos con paquetes adicionales disponibles, como se muestra en la primera imagen, en el contenedor solo se ha llenado un tipo y hay una una posibilidad agregar un paquete extra en un espacio vacío.
- Esto podría mejorar o empeorar la solución, pero en la segunda imagen el paquete extra podría ser colocado luego de terminar de llenar el contenedor, lo que garantiza que la solución no se deteriore. Aunque esta técnica puede optimizar la carga, implica un tiempo adicional de cómputo.

**Diapositiva 23**

- Ahora veamos cómo se aplicó estos algoritmos.

**Diapositiva 24**

- Para evaluar el algoritmo, se generaron datos de prueba con dimensiones fijas del contenedor y distintos tipos de paquetes.

**Diapositiva 25**

- Se programaron los algoritmos con Python y los parámetros usados fueron: población de 100 individuos, probabilidad de cruce del 80% y probabilidad de mutación del 5%.

**Diapositiva 26**

- Se consideraron 5 variantes del algoritmo, la primera variante M0, es el algoritmo genético básico, la variante M1 incluye el procedimiento de mejora durante el llenado, la variante M2 incluye el procedimiento de mejora al final, la variante M3 es lo mismo que M2 pero aplicado al 50% de la población y la variante M4 es lo mismo que M2 pero aplicado solo al mejor individuo de la población.

**Diapositiva 27**

- Los experimentos se configuraron con 25 problemas por cada instancia, con un tiempo máximo de 5 minutos por problema, lo que resultó en un total de 150 problemas y una duración de ejecución de 62 horas y media.
- Ademas, para hacer una comparación justa, se ha usado la misma población inicial para todas las variantes.

**Diapositiva 28**

- En la figura se tiene en el eje X las instancias con las distintas cantidades de tipos de cajas, y en el eje Y el porcentaje de mejora en el beneficio de la carga. Cada linea de color representa una variante del algoritmo.
- Se puede observar que la variante M1, que aplica las mejoras durante el llenado, es la que obtiene los mejores resultados en la mayoría de los casos y la variante M0 que es la versión básica del algoritmo genético es la que obtiene los peores resultados.
- También se puede observar que a medida que aumenta la cantidad de tipos de cajas, las mejoras son más notorias entre las distintas variantes.

**Diapositiva 29**

- Tambien se ha calculado cuánto tiempo se tarda cada variante en encontrar la su mejor solución.
- Se encontró que la variante M0 es la que tarda más tiempo en encontrar su mejor solución y el resto de variantes tardan menos tiempo, siendo la M1 que en algunos casos tarda menos.

**Diapositiva 30**

- En este caso se ha medido cuánto tiempo demora cada variante en evaluar una generación, es decir 100 individuos.
- Se puede observar que la variante M2 es la que más tiempo tarda en evaluar una generación seguido por la M1, y la M0 es la que menos tiempo tarda según lo esperado ya que las variantes M1 y M2 incluyen procedimientos de mejora.
- Cabe resaltar que el tiempo de evaluación de una generación no necesariamente indica que tardará más en encontrar la mejor solución.

**Diapositiva 31**

- Para consolidar una comparación de beneficio y tiempo, se ha calculado el rendimiento de cada variante. que sería cuánto beneficio se obtiene por cada segundo de ejecución.
- Se puede observar que la variante M1 es la que obtiene el mejor rendimiento en la mayoría de los casos, y la variante M0 es la que obtiene el peor rendimiento.

**Diapositiva 32**

- Por último, se visto que M1 es la que obtiene los mejores resultados en la mayoría de los casos, por lo que se ha realizado un análisis de progreso de la mejor solución en el tiempo.
- Se puede observar que la variante M1, las líneas de colores sólidos para distintas instancias, requiere menos tiempo para encontrar soluciones mejores en comparación con M0, que son las líneas punteadas.

**Diapositiva 33**

- En conclusión

**Diapositiva 34**

- El algoritmo genético ha demostrado ser eficiente para determinar la disposición de los paquetes en el contenedor.
- Se ha observado que las variantes de mejora reducen el tiempo necesario y mejoran la calidad de las soluciones, en especial la variante llamada M1.
- También se pudo ver que mientras más tipos de paquetes se tengan, se necesita más tiempo para converger.

**Diapositiva 35**

- Como trabajo futuro, se propone mejorar la eficiencia del algoritmo, considerar otras variantes de mejora, probar el algoritmo con datos reales y finalmente incluirlo en un sistema de soporte de decisiones.

**Diapositiva 36**

- Muchas gracias por su atención.
