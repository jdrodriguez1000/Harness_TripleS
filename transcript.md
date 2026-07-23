Video: Construyo mi propio arnés de IA… y te enseño como hacer el tuyo
URL: https://youtu.be/2B9QTg_-nyc

0:00 Hoy vamos a construir un arnés desde cero. Y cuando digo arnés, me
0:04 refiero a un arnés completo, a toda la estructura que permite que un modelo de
0:09 inteligencia artificial deje de ser un chatbot y empiece a ser realmente
0:13 un agente. Un sistema capaz de razonar en un bucle, capaz de utilizar
0:18 herramientas, capaz de delegar tareas a otros agentes y también trabajar con un
0:23 contexto razonable. Y no solo eso, sino que te voy a dar un repositorio
0:27 extensible a modo de tutorial para que tú puedas experimentar, jugar y hasta
0:32 construirte tu propio de inteligencia artificial. Vamos a ello. Pero
0:36 antes de entrar en los detalles específicos de código, te quiero contar
0:39 algunos conceptos que tienes que entender para realmente poder construir
0:43 un arnés con sentido. Y es que este vídeo es la tercera parte de una serie
0:47 en la que hablamos de Harness Engineering. Habíamos hecho un vídeo
0:50 introductorio explicando qué es esta disciplina. Habíamos hecho un vídeo
0:54 modificando un arnés ya existente y ahora vamos a hacer un arnés desde cero.
0:59 Y es que a nivel conceptual es un poco difuso dónde empieza y dónde termina un
1:04 arnés. A mí me gusta verlo como si fueran unas capas de una cebolla en las
1:08 que nosotros podríamos tener aquí abajo la primera capa, el núcleo de nuestro
1:13 arnés, que sería directamente el código que ejecuta las llamadas a la LLM,
1:20 ¿vale? Es decir, aquí dentro tendríamos pues yo que sé el SDK de Claude, ¿no? El
1:27 SDK de OpenAI o en general pues la conectividad, las llamadas que hacemos
1:33 al modelo, esto es la parte del cerebro y digamos la el control, ¿no?, de este
1:39 cerebro. Y luego tendríamos otras capas que podrían ser, pues por ejemplo,
1:43 aquí tendríamos la creación de tools, la creación de subagentes o incluso la
1:50 creación de skills que también pueden afectar al comportamiento
1:57 de esta capa interna. Es decir, aquí lo que tendríamos es que hay como una serie
2:01 de conexiones en las que nosotros podemos actuar. Lo que hicimos en los
2:06 vídeos anteriores fue agarrar un arnés que ya existía. En este caso estábamos
2:11 utilizando Claude, Claude Code en específico, y modificábamos esta capa de
2:16 aquí, pues gestionando, por ejemplo, un flujo de TDD. ¿Cómo? pues generando
2:22 subagentes, generando tools que controlaran, pues por ejemplo cómo
2:26 nosotros o cómo este cerebro, esta parte más core del arnés gestiona todo esto.
2:33 En este vídeo lo que vamos a ver es a crear esta parte de aquí dentro, a crear
2:38 este core, este binario y podríamos incluso verlo como crear nuestro propio
2:42 Claude Code. Entonces, ¿qué forma parte de este cerebro, de este binario, de
2:46 esta parte más interna de nuestro arnés? lo que se conoce como el bucle de la
2:51 gente. Y a mí me gusta explicar esta parte como visualización de un
2:55 videojuego, ¿no? Si has programado videojuegos, seguramente esta parte la
2:59 vayas a entender muy bien. Y es que en general cuando nosotros estamos
3:01 programando videojuegos, tenemos un concepto que se llama game loop, que es
3:05 básicamente qué ocurre en cada frame de nuestro juego. Pues por ejemplo, en un
3:10 juego que va a 60 frames por segundo, lo que tendríamos es un bucle en el que lo
3:15 primero que hacemos es leer el input del usuario. Por ejemplo, si el usuario ha
3:20 pulsado una tecla en el teclado o si ha hecho un movimiento con el mando o si ha
3:24 hecho clic con el ratón en algún sitio para disparar, leemos la entrada, ese
3:29 input es lo que primero ocurre en el frame. Luego tenemos la actualización
3:34 del estado del juego, es decir, en base a este input, ¿qué tenemos que modificar
3:39 de nuestro estado del juego? Tenemos que mover al personaje, tenemos que accionar
3:43 el disparo, tenemos que aumentar la vida. Aquí entrarían, pues, por ejemplo,
3:47 sistemas de física y todo esto. Luego tendríamos el renderizado del nuevo
3:52 estado, es decir, una vez hemos hecho la acción sobre el estado del juego, ¿cómo
3:57 se ve esto en pantalla? Tenemos que mostrar ahora un flash porque hemos
4:01 disparado. Tenemos que mostrar un corazón extra porque nos hemos curado.
4:05 Tenemos que mover al personaje realmente para que se renderice conforme se ha
4:10 movido. Activar una animación. Finalmente, una vez hemos terminado,
4:14 volveríamos a empezar el bucle del juego y así infinitamente. Así es modo de
4:19 resumen cómo nosotros programaríamos un videojuego. Pues lo mismo tenemos que
4:23 implementar cuando implementamos un agente. Cuando implementamos un sistema
4:27 de agentes, un arnés, nuestro bucle es muy similar. Lo que tendríamos es
4:31 también un bucle en el que hacemos read de la entrada, en este caso del usuario.
4:37 Sería cuando nosotros escribimos, ¿no?, en abrimos Claude Code, tenemos el input
4:42 de chat y escribimos algo. Luego nosotros evaluamos esta entrada, es
4:47 decir, hacemos algo con ella. Recordemos en el videojuego actualizábamos el
4:50 estado, pues aquí agarramos la entrada y decidimos qué hacer. Se la mandamos al
4:54 SDK de nuestra IA preferida. Hemos implementado que si nosotros escribimos,
4:58 por ejemplo, barra command, nuestro arnés no lo delegue a la IA sino que
5:02 ejecute algo interno para mostrarnos, por ejemplo, el listado de comandos.
5:06 Hemos hecho que si el usuario escribe la palabra caca, aparezca una caca por ahí
5:11 en ASCII diciéndonos algo. ¿Cómo reaccionamos a nuestra entrada? Sería
5:15 esta fase. Luego tendríamos la parte de print o de imprimir, es decir, cómo
5:20 reacciona nuestra UI, cómo le mostramos al usuario lo que está ocurriendo, el
5:24 resultado, ¿vale? Y finalmente tendríamos la parte de bucle que nos
5:30 indicaría que tenemos que volver a empezar todo el bucle. Fijaros que es el
5:33 mismo bucle que teníamos en un videojuego en literatura, en artículos
5:37 de internet, en algunos sitios lo vais a ver como REPL, un bucle reple o un bucle
5:44 de evaluación, básicamente por las siglas de read, eval, print y loop.
5:50 Entonces, en este caso nosotros tendríamos un bucle que sería el bucle
5:53 REPL que lo podríamos visualizar como algo así, ¿no? Lo que ya hemos
5:56 comentado. Ahora bien, la parte de evaluación no es tan sencilla como
6:00 parece. Cuando nosotros tenemos el input aquí y le damos a enter, lanzamos la
6:06 fase de evaluación. Pero fíjate que la fase de evaluación puede tener múltiples
6:11 pasos. En este caso, ahora solamente nos ha hecho un paso. Fijaros que hemos
6:14 vuelto a la parte inicial del bucle, que es otra vez esperar un input. Pero si
6:19 nosotros le vamos pidiendo cosas que son cada vez más complicadas a nuestro
6:22 bucle, va a llegar un momento donde tenemos que hacer varias peticiones a la
6:26 inteligencia artificial. En este caso le he pedido que lea diferentes ficheros,
6:31 por lo tanto, cada vez va ejecutando lo que se conocen como herramientas. Va
6:35 decidiendo pues qué ficheros de leer, lee uno, luego lee el otro. Es decir,
6:40 dentro de la propia fase de evaluación van ocurriendo múltiples cosas. En este
6:44 caso, lo que significa es que dentro de esta fase de EVAL tenemos lo que se
6:50 conoce como el bucle interno. Es el bucle interno el que se va comunicando
6:53 con la LLM, con nuestro proveedor de inteligencia artificial, en este caso
6:57 con el SDK de Anthropic, con el SDK de OpenAI con nuestra IA local, lo que
7:03 necesitemos. Y aquí lo tendríamos definido. ¿Qué ocurre dentro de el bucle
7:09 interno del bucle de evaluación? Pues básicamente lo que podemos hacer es
7:13 llamamos al modelo y el modelo nos dice qué cosas tiene que hacer. Si lo puede
7:18 hacer directamente, como hemos visto, nos va a responder. Terminamos el bucle.
7:22 Ahora bien, puede que tenga que ejecutar alguna tool. Veremos después cómo se
7:26 implementan las tools, pero por ejemplo, una tool podría ser leer un fichero. Por
7:30 lo tanto, el modelo decide que tiene que leer un fichero, devuelve lo que se
7:36 conoce como un tool use, es decir, necesito utilizar esta tool. Entonces,
7:40 aquí leemos el fichero, que lo podemos entender también de una forma más
7:44 abstracta cómo se ejecuta la tool. Y esto lo vamos repitiendo. Se ejecuta la
7:49 tool, se lo volvemos a pasar al modelo de IA, es decir, vamos a hacer una
7:52 llamada, el modelo de IA decide si tiene que ejecutar otra tool o si ya termina.
7:57 Vamos haciendo todo este flujo. Por lo tanto, todo esto es un bucle que una vez
8:01 que el modelo diga ya he terminado, ya no tengo que hacer más llamadas a
8:04 ninguna herramienta y ya puedo dar una respuesta, lo devuelve al bucle
8:08 principal, al bucle REPL. Por lo tanto, si te has quedar con algo de lo que
8:12 sería la agent loop, es que son dos bucles. El bucle grande que gestiona la
8:16 interacción que tú ves con el usuario y el bucle pequeño, que es cuando tú le
8:20 das a enter y ves que la IA está empezando a hacer cosas que ahora se va a un
8:23 fichero, que ahora se va otro, que ahora escribe algo, que ahora escriben una
8:27 cosa. Todo esto es el bucle interno, ¿vale? Y cuando termina vuelves a
8:29 empezar. ¿Cómo se ve esto en código? Pues lo que hemos implementado en este
8:33 repositorio es un bucle sersencillito para demostrar, para enseñar exactamente
8:39 cómo lo puedes hacer tú por tu cuenta. Hemos utilizado Go para hacer este
8:43 proyecto porque al final el lenguaje no es tan importante. La idea es que tú
8:46 puedas ver esto y entender el concepto. Y lo que hemos visto es, vale, nos vamos
8:50 a generar una función main. Fijaros que aquí estamos importando la biblioteca,
8:55 ¿no? La dependencia de Anthropic, porque de momento este bucle lo vamos a tener
8:59 con el modelo de Anthropic, con Claude, con Opus concretamente. Y fíjate que
9:03 aquí empezamos con nuestro primer loop. En este caso imprimimos nada, una
9:08 flechita para indicar que el usuario puede escribir. Y una vez el usuario ha
9:11 escrito algún tipo de texto, algún tipo de prompt, se lo mandamos a Anthropic, se
9:16 lo mandamos al SDK para generar lo que sería el contexto, ¿vale? Aquí nosotros
9:21 estamos generando el contexto que nosotros le vamos a mandar con esta
9:24 función NewMessages. Fijaos que aquí empieza ya el agent loop, que sería el bucle
9:29 interno. Es decir, este bucle de aquí es el bucle REPL y este bucle de aquí es el
9:36 bucle interno, el bucle de evaluación. Fijaos que el bucle de evaluación
9:39 recibe, como he dicho, eh, el contexto, recibe el historial de mensajes y en
9:44 este caso lo que hacemos es construir los mensajes ya pensando en el SDK de
9:49 Anthropic, ¿vale? Esto al final es una API que nosotros tenemos que podemos
9:52 utilizar y aquí le estamos mandando directamente estos mensajes a la IA.
9:57 Aquí ya estamos haciendo la llamada a nuestra client.messages.new.
10:02 Estamos haciendo la llamada a la LLM diciéndole, "Ey, tengo este mensaje de
10:05 usuario." Y la LLM me da una serie de respuestas. Fíjate que los mensajes de
10:10 respuesta son también un array. ¿Por qué? Porque puedo recibir, como he
10:14 dicho, diferentes respuestas o diferentes llamadas a diferentes
10:17 herramientas. En este caso, lo que tengo que hacer es ir iterando todo este
10:21 bloque de respuestas. Esto sería el bucle de ejecución, ¿no?, de
10:25 cada una de las respuestas. Y fíjate que lo que hacemos es distinguir cuando me
10:29 está diciendo una respuesta directamente contexto, con este caso de aquí de
10:32 Anthropic text o cuando me está diciendo, "Ey, quiero ejecutar una herramienta."
10:37 Si quiere ejecutar una herramienta, porque la LLM considera que tiene que
10:40 leer un fichero, que tiene que hacer un commit, que tiene que hacer cualquier
10:42 cosa, que tiene que invocar un MCP, lo que sea, si detecta que ha de ejecutar
10:46 una herramienta, tengo aquí una función que se llama ejecutar herramienta.
10:50 Entonces la ejecuta, devuelve los resultados y finalmente cuando termina
10:55 el bucle interno, en este caso con un stop reason que ya he terminado de hacer
11:01 todas las ejecuciones, devuelve. Por lo tanto, fíjate que aquí tenemos el agent
11:05 loop, que sería el bucle interno. Una vez termina el bucle interno, esto
11:09 vuelve a empezar. ¿Qué pinta tendría esto cuando yo lo ejecuto? Pues mira, si
11:12 yo me descargo el repositorio, que te dejo aquí abajo en la descripción, pues
11:16 mira, si yo hago go run examples minimal main.go para ejecutar este código que
11:22 tengo aquí, yo le doy y fíjate que me sale esto de aquí. Ahora tengo el bucle
11:27 REPL esperando a mi input. Yo le puedo decir, "Hello", ahora está ejecutando la
11:32 llamada a la LLM y ya me ha contestado. Esto por detrás está haciendo la llamada
11:37 a la API de Claude con eh el API Key, que tenga una variable de entorno y por lo
11:41 tanto lo está pudiendo hacer de forma correcta. Yo le puedo decir ahora, por
11:45 ejemplo, "How many files are there in this folder?" Para que instancie una
11:51 herramienta y me pida ejecutar. En este caso, fijaros que me está queriendo
11:55 ejecutar esta herramienta de aquí, la herramienta de bash. ¿Qué serían estas
11:59 herramientas que yo tengo aquí definidas? Pues mira, las tengo aquí
12:02 abajo. En Execute Tool tengo la implementación de cada una de estas
12:06 herramientas. Pues tengo en este caso la herramienta de bash, ¿vale?, que está
12:11 aquí arriba definida y aquí la tengo. En el caso de que la IA quiera ejecutar
12:17 bash, lo que tengo que hacer es en este caso ejecutar bash. Entonces, fíjate que
12:22 estoy programando las herramientas que la IA va a poder utilizar. La IA no
12:26 ejecuta las herramientas. La IA solamente las conoce y le dice al arnés,
12:31 "Ey, quiero ejecutar esta herramienta." Es como ver el martillo en la mesa y
12:34 decirle al arnés, quiero utilizar este martillo. Pero la LLM no sabe si el
12:39 martillo golpea o no golpea. Eso lo hace el arnés. El arnés lo que la LLM le pide y
12:44 lo ejecuta en tu máquina, ¿vale? Entonces, fíjate que tengo para ejecutar
12:47 bash para leer un fichero, que en este caso lo que tengo es directamente
12:51 leerlo, ¿vale?, con read file y escribirá un fichero, que en este caso
12:55 es escribirlo con Write file. Por lo tanto, yo aquí me programo las herramientas.
13:01 ¿Cómo la LLM sabe las herramientas a las que tiene acceso? ¿Cómo sabe que tiene
13:05 o que puede ejecutar bash? Porque cuando yo aquí me he construido este
13:11 sistema, este arnés tan pequeñito, fíjate que al SDK de Anthropic le estoy pasando
13:18 las herramientas que existen. Yo le tengo que decir al proveedor, ¿vale? En
13:23 este caso, al SDK de Anthropic, si fuera el SDK de OpenAI seguramente tendría que
13:27 hacer esto diferente y no todos los SDK soportan tools, por lo que hay que mirar
13:31 eso, la documentación de cada proveedor de IA. Pero en este caso yo le digo al
13:36 SDK de Anthropic, mira, tienes la tool de bash, la tool de leer ficheros y la tool de
13:41 escribir ficheros. Y fijaros que le paso la información necesaria para que la LLM
13:45 sepa que ha de usar. Le digo, "Mira, la tool de Bash ejecuta un comando shell y
13:50 devuelve lo que devuelve a STD out y a STDerr". Leer fichero. Pues mira, es una
13:55 tool que lee los contenidos de un fichero en un path concreto y le digo los
13:59 parámetros necesarios que le tengo que pedir a la IA. Okay, estoy mostrándole a
14:04 la inteligencia artificial las herramientas a las que tiene acceso. Si
14:08 yo no le defino una buena descripción, es posible que la IA no sepa que tiene
14:13 que utilizar bash para hacer esto que tiene que hacer. ¿De acuerdo? Por lo
14:17 importante definir bien la descripción porque en función de esto es la propia
14:21 LLM quien por inferencia decide qué herramienta usar. Entonces, fíjate que
14:25 yo simplemente diciéndole cómo, cuántos ficheros hay en esta carpeta, ella ya
14:29 sabe que tiene que utilizar bash. Si yo le digo, "Write me a new file with the
14:36 word "hello" in it", seguramente va a saber que tiene que ejecutar write file
14:41 y aquí está, ha encontrado esta tool y me la ha llamado. Entonces, esto
14:45 sería el bucle principal y la definición de herramientas en un arnés de
14:49 inteligencia artificial. Como veis, son 175 líneas de código simplemente con la
14:55 dependencia externa de el Anthropic SDK. Por lo tanto, los arneses son muy
15:02 sencillos. Ahora bien, todo lo que construyas por encima de este bucle, de
15:06 la gestión de las herramientas, de cómo yo llamo a la gente, de cómo interactúo
15:13 con el bucle, van a ser cosas extra que yo le voy enchufando al arnés. Entonces,
15:16 ahora mismo tenemos construido algo como esto. Tenemos en la parte
15:23 del LLM, pues la definición de las tools, pero claro, cuando yo estoy
15:28 construyendo un arnés propio, el gran poder o la gran capacidad que yo tengo
15:33 cuando construyo un tipo de arnés así es poder cambiar el modelo de IA. Yo quiero
15:38 poder agarrar esta LLM y que este LLM, pues por ejemplo, sea o bien Claude o sea Codex.
15:48 O sea, o llama, quiero poder cambiar el modelo de una forma sencilla. ¿Cómo
15:53 puedo hacer esto? Con polimorfismo. De la misma manera en el que yo aquí dentro
15:57 tengo este SDK y estoy llamando directamente a los SDK de Anthropic, yo
16:03 puedo generarme un sistema polimórfico para poder cambiar estas piezas bajo
16:08 demanda. Es decir, yo me puedo generar en mi lenguaje favorito, pues yo que sé,
16:13 una clase, una interfaz que sea Provider en la que yo defino una serie
16:18 de funcionalidades, pues por ejemplo, definirme una tool, eh, mandar un
16:23 mensaje, cualquier cosa que yo necesite en mi arnés y luego tener el Anthropic
16:28 Provider, el OpenAI Provider y así poder soportar diferentes modelos de
16:34 inteligencia artificial, como lo he montado yo en este repositorio. Si te
16:38 vas a la carpeta internal de este repo, vas a poder ver exactamente todo lo que
16:43 se está montando. Y tenemos aquí una parte que es la carpeta de provider que
16:48 como ves tiene diferentes ficheros de Go. Te voy a enseñar el fichero
16:53 agnóstico, ¿vale? Lo que sería la interfaz o la parte más polimórfica, que
16:57 es este fichero de provider.go. Fíjate que provider.go simplemente me
17:02 define una interfaz en la que yo puedo setear el modelo y leer el modelo.
17:07 Básicamente porque, por ejemplo, Anthropic tiene diferentes modelos,
17:09 tenemos Opus, tenemos Sonnet, OpenAI también tiene diferentes modelos,
17:13 incluso versiones de cada uno y me ofrece una función para yo enviarle un
17:19 mensaje. Date cuenta que le mando un mensaje, le mando las tools que tiene
17:23 disponibles y le mando un contexto. Y obviamente esta interfaz me tiene que
17:27 devolver una respuesta. Fíjate que todos estos tipos que hay aquí, el API
17:33 Message, API Tool Def y API Response, son tipos genéricos, son tipos que yo me
17:39 he creado. ¿Por qué? Porque cada SDK va a ser de su padre y de su madre. Cada
17:44 SDK va a exponer distintos datos, va a tener diferente estructura. Por lo
17:48 tanto, yo quiero limitar el impacto que tiene el cambiar un SDK por otro en mi
17:53 código. Si quieres aprender a programar utilizando estas técnicas,
17:56 aprovechándote del polimorfismo y de las interfaces, te dejo aquí abajo una serie
17:59 de vídeos en la que hablo de principios SOLID y de patrones de diseño que puedes
18:03 utilizar. Por lo tanto, estoy generando una serie de clases genéricas que van a
18:09 ser convertidas después en cada uno de mis providers a las clases específicas
18:15 de cada provider. Por ejemplo, en el caso de Anthropic, pues aquí es el único
18:19 sitio de mi arnés donde importamos el SDK de Anthropic y lo que hacemos es
18:24 definirnos pues las funcionalidades específicas de este SDK, cómo se
18:28 construye y luego implementamos las funciones, pues por ejemplo, para
18:33 obtener el modelo, para setear el modelo y aquí abajo, la más importante, para
18:38 enviarle un mensaje al modelo. Fíjate que estoy reimplementando la función
18:43 Send, ¿vale?, que es la función que tenemos definida en la interfaz y le
18:45 estoy diciendo, mira, aparte de hacerme aquí unos logs, que yo esto tengo una
18:49 serie de logs para una cosa que te voy a enseñar después que está muy chula, lo
18:52 que quiero es que llames al SDK de Anthropic, fíjate que es la misma función
18:57 Messages New que teníamos antes, con esta información que es básicamente una
19:02 traducción de los ítems genéricos que le estoy introduciendo, pues por ejemplo,
19:07 las tools, los mensajes y configuraciones, por ejemplo, el máximo
19:11 número de tokens que quiero que utilice el modelo, si quiero que active el
19:15 modo thinking o no, etcétera. Es decir, estoy abstrayendo exactamente lo que
19:20 ocurre cuando le envío un mensaje a la LLM y implemento aquí dentro un bucle
19:25 que me convierte las respuestas de Anthropic a mis respuestas genéricas.
19:29 Fíjate que yo aquí estoy construyendo un output content, que es una respuesta
19:35 genérica de mi arnés. Vale, estoy traduciendo la respuesta que me da
19:39 Anthropic en este caso a la respuesta de mi arnés genérica para finalmente
19:42 devolverla. Quiero implementar OpenAI, pues lo mismo, tengo otro fichero
19:48 OpenAI con las mismas funciones. En este caso, aquí también tengo una función
19:53 Send. Y fíjate que aquí lo que hago es, en vez de hacer la llamada que hacía antes
19:57 Anthropic, aquí la hago al SDK de OpenAI que tiene una estructura y una forma
20:02 distinta. Y luego lo mismo, vuelvo a traducir las respuestas a mi respuesta
20:06 genérica, por lo tanto estoy abstrayéndome de todos los modelos y
20:12 providers de inteligencia artificial. Fíjate que aquí es el único sitio donde
20:17 yo estoy importando OpenAI, que yo necesito ahora un modelo local para no
20:24 sé qué, me puedo generar un nuevo fichero de Go, comunicarme con este
20:28 modelo local, con el SDK, con la API que sea y utilizarlo. Que necesito un modelo
20:33 MOC para hacer tests y que no me cobren cuando yo ejecuto los tests. Tengo un
20:37 modelo MOC en el que reimplemento estas funciones con la función sendas
20:45 aleatorias para yo poder ejecutar los tests. Entonces, fíjate lo fácil que es
20:50 simplemente abstraerte del proveedor de las LLMs. Simplemente tienes unas APIs a
20:55 las que llamas y te generas un wrapper por encima. Por lo tanto, cuando yo ahora me
20:59 voy a mi bucle agéntico, al mi bucle de este arnés, es decir, me voy a la
21:03 función main, lo que veo es que tengo un arnés que, okay, lee un system prompt,
21:09 que es un prompt que yo le he colocado aquí con una serie de explicaciones.
21:14 Este es el primer prompt que se manda a cualquier modelo de inteligencia
21:17 artificial. Tengo que lea también si tengo un fichero agent.md para
21:22 incorporarlo también al System prompt. Ya os digo, esto es decisión del arnés.
21:26 Cada arnés puede hacerlo cuando quiera, puede leerlo y meterlo en el system
21:30 prompt, puede leerlo y meterlo como mensaje de usuario. Al final, estos son
21:33 decisiones de cada uno de los arneses, ¿no? Podría incluso leer el repo en el
21:37 que está actuando y meterlo también del system prompt para darle más contexto a
21:42 la LLM. Bueno, aquí me puedo montar yo lo que necesite. Entonces, fíjate que
21:46 leo el system prompt, lo genero y luego aquí me instancio el proveedor. Tengo
21:52 esta función aquí, NewProvider, que lo que hace es, vale, mira, pues si quiero
21:56 utilizar Anthropic, genero el de Anthropic o genero el de OpenAI. ¿De acuerdo?
22:01 Por lo tanto, yo aquí puedo construir diferentes proveedores en función de lo
22:05 que necesite. Cosas que podría hacer aquí para mejorar esto. Podría leer esto
22:09 de un fichero de configuración, ¿vale? para escoger si quiero ir a un modelo o
22:13 a otro. Por ejemplo, este arnés no tiene ningún sistema de configuración externo.
22:17 Todo está en el código porque quiero que quede muy claro cómo el hecho de exponer
22:23 partes de configuración también permiten que tú puedas modificar o afectar el
22:27 arnés desde fuera, ¿vale? Lo que hemos hecho de las capas, puedes hacer harness
22:31 engineering en la capa de binario o puedes hacer harness engineering en la
22:36 capa de configuración. Todo depende de cuánto el arnés te deja o no afectar su
22:42 propio comportamiento. ¿Okay? Entonces, yo aquí generaría ya el proveedor de
22:47 LLM y aquí en esta función le mandaría el mensaje a mi LLM, a mi agente. Por lo
22:53 tanto, aquí estaría llamando ya a la función para ejecutar el loop interno.
22:58 Entonces, fíjate que es un poco más complejo porque le hemos metido UI, le
23:01 hemos metido un poquito de cosas por encima, pero en el fondo no deja de ser
23:06 un simple bucle. Entonces, hasta aquí ya tenemos algo que empieza a parecerse a
23:10 un agente real, pero ahora mismo, como hemos visto, nuestro arnés ejecuta tools
23:15 sin ningún tipo de supervisión, lo que supone un riesgo de seguridad. ¿Cómo
23:19 podemos evitar que la gente haga cosas sin que yo me entere, sin mi permiso?
23:23 Pues obviamente implementando en el ARNES un sistema de permisos para la
23:28 ejecución de cada una de estas tools. Ahora que hemos visto el código, hemos
23:31 visto cómo se lanzan, cómo se ejecutan estas herramientas, podemos afectar
23:35 meternos ahí dentro y implementar salvaguardas, implementar rails para
23:40 que la IA no haga cosas que no tiene que hacer. ¿Cómo implemento yo un gateway de
23:44 seguridad? Pues si me voy a la función que ejecuta mis tools, recordemos, eh,
23:49 estamos en el bucle interno, en la parte de ejecución de las tools. Cuando ya la
23:54 LLM nos ha dicho, "Quiero ejecutar esto." Yo tengo programado que se lance
24:00 esta función de aquí, ¿vale? Recordemos el ejemplo pequeño. Esto sería como
24:04 irnos a nuestro bucle, irnos a nuestro agent loop, luego aquí abajo irnos a la
24:10 función que nos ejecuta la tool y aquí antes de ejecutar la tool añadir la
24:16 seguridad. ¿Vale? ¿Qué puede ser esta seguridad? Pues que te aparezca un
24:19 mensaje de, "Ey, se quiere ejecutar esto, ¿lo vas a aceptar o no?" Si lo
24:23 aceptas continúas. Si no lo aceptas, no ejecutas nada. Haces una nueva operación
24:28 y te vas. ¿Vale? Recordemos que esto sería el ejemplo pequeño. En el ejemplo
24:31 ya completo que hemos visto al inicio del vídeo, lo que tenemos es que la
24:36 propia función para ejecutar la tool tiene aquí la salvaguarda de aprobación.
24:41 Y en caso de que el usuario confirme la llamada de aprobación, es decir, si dice
24:47 que okay, que se puede ejecutar la tool, vamos a continuar a partir de esta
24:51 línea. Si no, terminamos diciendo que el usuario no ha permitido hacerlo. Si lo
24:56 permitimos hacer, pum, llamamos al execute de la tool específica. Fijaros
25:00 que yo tengo aquí construida la carpeta de tools porque cada una de las
25:05 herramientas está implementada de forma independiente. Lo que hemos visto antes
25:08 en el ejemplo mínimo. Eh, esta, por ejemplo, es la tool de Bash. Yo tengo
25:12 aquí definida la definición y la función de ejecución utilizando de nuevo
25:17 polimorfismo para poder generar tools de una forma sencilla. La de escritura de
25:22 fichero, lo mismo. Tengo aquí una función definition y aquí una función
25:26 execute. La función definition es la que le da la descripción a la LLM. La función
25:31 execute es la que hace que el arnés haga la acción. Entonces, fijaros que
25:34 utilizando polimorfismo, yo estoy consiguiendo montar un proyecto en el
25:38 que tengo las tools, tengo los proveedores y, en general, tengo un
25:43 montón de capacidad para yo poder expandir, experimentar y probar con el
25:47 desarrollo de un arnés propio. Pero esto al final era un poco básico, no dejaba
25:51 de ser un bucle que iba haciendo llamadas a un SDK de Anthropic. Los
25:54 arneses de hoy en día, como Claude Code, como Codex, tienen capacidades mucho más
25:59 potentes. Por ejemplo, son capaces de generar subagentes. Yo le puedo pedir
26:04 algo a Claude Code y que de golpe me lance tres subagentes o yo puedo definir
26:09 subagentes, como vimos en vídeos anteriores, para implementar el flujo de
26:11 TDD. ¿Cómo se haría esto cuando yo estoy trabajando en la capa core de mi
26:15 harness? Pues básicamente tengo el control total. De la misma manera que yo
26:19 puedo generarme un proveedor y enviarle mensajes, yo puedo generarme también
26:25 agentes. Un agente no deja de ser una instancia concreta de mi proveedor. Por
26:30 lo tanto, de la misma forma que yo puedo crear diferentes tools, también puedo
26:34 crear diferentes agentes y lo mejor de todo, lo puedo hacer bajo demanda. Es
26:38 decir, yo me puedo crear aquí este tipo Agent y generarme un constructor en el
26:42 que directamente estoy devolviendo un conjunto de proveedores, tools y un
26:48 system prompt. Fijaros aquí que estoy construyendo un agente en el propio
26:51 código. Obviamente, cuando yo me genero agentes, tengo que poder mandarle
26:55 mensajes a este agente, por lo que defino las funciones para setear,
26:59 limpiar los mensajes, enviar los mensajes al proveedor, que esto
27:02 básicamente lo que hace es lanzar el loop dentro del agente, que sería de
27:06 nuevo el loop interno, y también tengo que darle a la gente la capacidad de
27:11 ejecutar tools. Entonces, fíjate que estoy agarrando mi bucle interno, lo
27:17 estoy guardando o empaquetando, en este caso, en una clase que me va a permitir
27:22 instanciar diferentes bucles internos, como si fueran enemigos de un
27:25 videojuego, como si fueran personajes de una simulación. Yo tengo el control de
27:30 cuántos agentes instancio y de cómo los configuro. Fíjate que yo le paso el
27:35 provider cuando estoy construyendo el agente. Por lo tanto, yo podría tener en
27:38 mi mismo arnés al mismo tiempo un agente con el proveedor de OpenAI y un agente con
27:45 el proveedor de Anthropic y luego también una parte en programación local, por
27:50 lo que podría montarme arneses que en función de ciertas características hagan
27:54 unos agentes u otros. También, ¿qué le defino al agente? Las tools a las que
27:58 tiene acceso. Quizá quiero que un modelo concreto con un proveedor o un tipo de
28:03 agente solamente sea capaz de leer ficheros porque no quiero que pueda
28:06 escribir o quiero tener otra agente que solo se encargue de herramientas de Git
28:10 y me genero unas tools aquí de acceso a Git y que eso solamente pueda hacer
28:15 cosas de Git, pero no pueda leer ficheros ni escribir ficheros en mi
28:19 dispositivo. Es decir, el potencial como ya estoy en una capa tan baja del
28:23 desarrollo del harness es prácticamente infinito. Por lo tanto, si yo me defino
28:27 estas clases de agentes, cuando yo me vaya a mi función main, a mi bucle
28:32 principal, a mi bucle REPL, podemos entender que cuando yo construí el
28:37 system prompt original, que es cuando yo enciendo mi arnés, cuando yo agarro el
28:42 proveedor de IA que quiero utilizar, lo primero que voy a hacer, fíjate, es
28:47 generarme el root agent. El root agent es el agente raíz, es el agente que
28:52 recibe el system prompt que tengo yo aquí hardcodeado, que podía también
28:56 tener en un fichero sin ningún tipo de problema y es el primer agente que se
29:01 genera, es la raíz. Por lo tanto, fíjate qué poder tiene el hecho de empaquetar
29:06 el concepto de agente dentro de una clase de código para que yo luego lo
29:10 pueda instanciar de forma libre. Ahora bien, quizá la pregunta que tienes es,
29:14 ¿vale, Marty, he visto que aquí tienes el new, ¿no? O bueno, mejor dicho, la
29:18 definición de el root agent. Este es el root agent que está en el bucle
29:22 principal. Pero esto de los subagentes, ¿cómo funciona? ¿Cómo hago yo que de
29:27 golpe le pido algo y me genere subagentes? ¿Cómo hago yo que si yo le
29:31 digo a mi IA que me lance, pues, por ejemplo, subagentes de investigación, mi
29:36 arnés sea capaz de tomar la decisión y de instanciar estos subagentes?
29:41 Fíjate que le he pedido que realice unas investigaciones. Me lee los ficheros y
29:45 aquí ya empieza a delegar a un subagente. Fíjate que está thinking del
29:49 agente de research. Eso es porque yo he configurado mi UI para que los
29:54 subagentes se vean así, ¿vale? Se vean como una flechita que va hacia
29:59 dentro. Eso es que lo está haciendo otro agente. ¿Cómo hago esto? Pues en verdad
30:03 ya tenemos todos los ingredientes para poder implementar algo así. Lo que
30:06 queremos es que nuestro agente haga una acción. ¿Qué acciones puede hacer
30:10 nuestra agente? Puedes ejecutar comandos de bash, leer ficheros, escribir
30:14 ficheros. ¿Cuál es la nueva acción que queremos que pueda hacer? Delegar o
30:18 instanciar subagentes. Tengo aquí una tool que es la delegate tool que es la
30:23 encargada de instanciar subagentes. Fíjate que yo aquí en la definición le
30:29 paso la descripción de mi subagente. Yo esto lo puedo tener guardado allí donde
30:33 necesite. ¿Vale? Fíjate que aquí tengo una clase subagente en la que, por
30:38 ejemplo, tengo un agente de research que tiene una descripción que explica qué es
30:43 capaz de hacer este agente para darle al agente principal el contexto de la
30:47 herramienta sin más. Y si yo me voy aquí a esta herramienta, pues mira, le paso
30:51 la descripción, lo que el input schema y la parte de ejecutar lo que hace es,
30:57 epa, ejecutar el subagente. Por lo tanto, fíjate que no es magia, es simplemente
31:01 una herramienta más que la LLM puede decidir utilizar. Lo único es que esta
31:05 herramienta lo que hace es instanciar un nuevo subagente, ¿vale? Con el comando
31:10 run, que esto a su vez vuelve a empezar, me genera otro bucle interno, me acaba
31:14 de spawnear un nuevo enemigo, me acaba de spawnear un nuevo subagente. El cómo
31:19 yo spawneo este subagente ya es una decisión del propio arnés. Por ejemplo,
31:24 yo aquí he tomado la decisión de que este subagente empieza con un contexto
31:28 vacío, no hereda los mensajes de la gente raíz, pero lo podría hacer. Yo le
31:33 podría pasar eh aquí una nueva variable, le podría pasar lo el historial de
31:38 mensajes, podría tomar las decisiones que yo considere porque yo tengo el
31:42 control completo de cómo estoy implementando mi arnés. Y es por esto
31:45 que cambiar de un arnés a otro tiene tantas implicaciones, porque estas
31:48 decisiones no siempre son las mismas. Con esto ya tenemos una base bastante
31:52 potente y podemos empezar a razonar y a extender este arnés como nosotros
31:56 necesitemos. Y créeme, hay un montón de cosas que nosotros podemos añadir. Ahora
32:00 mismo nuestra eh interfaz, nuestro arnés, es algo muy sencillo, no deja de
32:05 ser muy similar a como podría ser Claude Code, etcétera, en el que tenemos una
32:09 serie de comandos, ¿vale? pues para ver las tools que tenemos disponibles y los
32:14 agentes que se están ejecutando. Y tenemos un poquito un status bar que
32:18 nosotros aquí podemos popular y podemos programar como queramos, pero hay un
32:21 montón de cosas que nosotros podemos añadir, por ejemplo, soporte para MCPs.
32:25 ¿Cómo podríamos implementar nosotros un MCP en un arnés como el que tenemos?
32:30 Bueno, pues depende de cómo queramos. Podríamos reutilizar nuestra herramienta
32:34 de tools. Si yo me voy a la carpeta MCP, yo puedo ver que tengo un struct que se
32:40 llama MCP Tool, que lo que tiene es dentro una definición de una tool. Por
32:45 lo tanto, estoy haciendo un wrapper sobre mi sistema de tooling para que yo
32:49 pueda crear tools utilizando MCPs. Fíjate que es exactamente lo mismo, eh,
32:54 tengo una definición y tengo una función execute. La única diferencia es que en
32:57 este caso yo quiero poder registrar MCPs en remoto, quiero poder pasar una URL y
33:04 que se lean o se instalen los MCPs necesarios para poder trabajar. Es por
33:09 esto que este MCP register tiene una función load config, que lo que hace es
33:14 cargar el típico fichero de mcp.json, que por ejemplo tengo aquí abajo
33:19 para hacer una prueba, lee esto, agarra esto de aquí, la definición, por
33:24 ejemplo, de DuckDB, y lo que hace es guardar aquí en un map, en una
33:29 estructura, el MCP, es decir, una vez hemos leído el fichero, hace una
33:33 petición al servidor mediante fetch, obtiene lo necesario y lo registra en el
33:39 registry, que el registry no es nada más y nada menos que un map con las nuevas
33:45 tools. De acuerdo. Como curiosidad tuve que hacer que se cargaran los MCPs en
33:51 paralelo porque claro, como tenía que hacer peticiones HTTP para obtener estas
33:56 tools, pues esto bloqueaba el arnés y tardaba un ratito en cargar esto, ¿no?
34:00 Entonces lo puse como una gorrutina para que lo haga en paralelo sin afectar
34:06 al thread principal de la UI y va cargando las tools de MCP en background
34:11 y yo, por lo tanto, puedo ir interactuando con mi UI. ¿Qué más
34:14 cosas puedo implementar? Bueno, pues por ejemplo, los slash commands. Yo puedo
34:18 hacer /help y si le quito el modo debug voy a ver todos los comandos que
34:23 tengo disponibles. Como esto es un arnés para aprender, digamos que he querido
34:28 utilizar mucho polimorfismo para poder cambiar las piezas de una forma muy
34:31 sencilla. Una de las piezas que se pueden cambiar es la metodología de
34:36 compactación de la conversación. Ahora mismo tenemos implementadas la sliding,
34:40 la summary y ninguna, pero está pensado para que tú puedas experimentar. La
34:44 compactación es lo que ocurre cuando tienes el contexto muy lleno en tu
34:47 modelo del LLM y quieres resumirlo, pues o bien para ahorrar tokens o bien para
34:52 poder seguir conversando sin que se degrade la conversación, ¿no? En este
34:56 caso tengo aquí la carpeta compact donde tengo las diferentes estrategias de
35:01 compactación, ¿vale? La estrategia de compactación es simplemente una interfaz
35:05 que recibe esto de aquí, recibe los mensajes y devuelve los mensajes
35:09 compactados. Hay diferentes estrategias, o bien no resumas, que no hace nada, o
35:14 bien sliding window, que como veis simplemente se queda con un trozo
35:18 concreto de la ventana, y la parte de summary, que sería un poquito la más
35:23 interesante en la que utilizo la propia LLM para mandarle un prompt diciéndole,
35:28 "Ey, resúmeme la conversación y me actualiza el contexto con la información
35:34 resumida." ¿Vale? Entonces, si quieres probar nuevas estrategias, es tan fácil
35:37 como irte a la carpeta de compact y implementar una nueva de estas. Y luego
35:41 te irías aquí a el arnés /compact y escoges la nueva herramienta
35:48 que quieres utilizar, la nueva estrategia. Lo mismo con el provider,
35:50 eh, puedes cambiarlo aquí, puedes cambiar el modelo, puedes listar los
35:54 subagentes, pero también que me parece interesante, puedes listar los tokens
35:58 gastados y si yo le pido algo, aquí me irá saliendo el coste que me devuelve el
36:05 provider del LLM. Fíjate que si te vas al código, aquí vemos los tokens que yo
36:09 le he enviado, los tokens que me ha devuelto y el precio. Si te vas al
36:12 código de cada uno de los providers, vas a ver que hay una serie de
36:17 configuraciones de coste, ¿vale? En función del modelo tengo definido cuánto
36:21 cuesta cada uno de ellos. Esto obviamente puede ir cambiando, se tiene
36:25 que actualizar mediante la documentación, pero esto lo único que
36:29 hace es que cuando me devuelve una respuesta el proveedor, yo puedo saber
36:33 cuántos tokens me ha devuelto porque me lo devuelve la propia API y realizo la
36:37 multiplicación y entonces ya tenemos el coste y el uso. ¿Qué otras cosas se
36:41 pueden implementar que pueden ser guay? Por ejemplo, sistemas de memoria. Llega
36:45 un punto cuando vas trabajando con la IA que si cierras la sesión y la vuelves a
36:48 encender tal como lo teníamos hasta ahora, pues empezabas de cero, no tenías
36:53 un sistema de memoria, no sabías lo que habías hecho anteriormente. ¿Por qué?
36:56 Porque todo el contexto, todo lo que nosotros le pasábamos a nivel de
36:59 mensajes estaba guardado en la propia RAM, en la memoria, en una variable del
37:04 proceso. ¿Cómo podríamos implementar un sistema de memoria? Pues sencillamente
37:08 de la misma forma que hemos implementado subagentes, en vez de tener una tool
37:11 para instanciar un subagente, tendremos una tool para guardar memoria y para
37:16 recordar de memoria, que son precisamente estas dos nuevas tools que
37:20 añadí aquí posteriormente. La tool de recall, que es para recordar cosas de la
37:26 memoria, y la tool de remember, que es para guardar cosas en la memoria. De
37:31 nuevo, estos son tools. Depende de cómo yo le defina la descripción, la LLM va a
37:35 decidir si las quiere utilizar o no. Es la LLM que decide si se acuerda o merece
37:40 la pena acordarse de algo o merece la pena ir a buscar a su memoria algo del
37:44 pasado. La implementación de estas tools, la función execute, ya depende de
37:49 cada uno de nosotros. En mi caso, yo lo guardo directamente en ficheros JSON,
37:54 ¿vale? Lo guardo en una carpeta con ficheros JSON, pero tú puedes
37:57 implementar que esto lo guarde en SQL. Puedes implementar una librería que lo
38:01 guarde en una base de datos en remoto y lo programas directamente aquí. Luego
38:04 aquí en el recall pues ejecuto cómo busco la memoria, ¿no? Cómo me aseguro
38:09 quiero buscar por palabra, quiero buscar por tag, cómo quiero interactuar con la
38:12 memoria a nivel programático cuando la IA me diga, "Ey, quiero recordar, ¿vale?
38:16 ¿Qué hago?" Entonces, para que tú puedas experimentar con diferentes sistemas de
38:20 memoria y puedas implementarte los tuyos propios, aquí tengo la carpeta memory en
38:24 la que he definido el store. En este caso, tú puedes modificar estos ficheros
38:27 de memoria para acabar de definir diferentes stores. Definir recalls,
38:33 definir preambles y definir save. Defines las tres funciones que
38:35 interactúan con el store de memoria. Y por ejemplo, aquí tengo que tengo un
38:40 store de ficheros, lo que ha comentado que son JSONs, donde yo lo guardo en un
38:45 fichero de JSON con una serie de logs y errores donde voy indexando todas las
38:50 instancias, las sesiones de las que me quiero acordar y tengo aquí el save y
38:55 tengo aquí el recall, que lo que hace es básicamente ir a buscar el fichero de
39:00 memoria y fíjate hacer toda la serie también de guardados de ficheros y en
39:05 general gestionar todo lo que sería mi acceso, mi interacción con la memoria,
39:10 que en este caso no dejan de ser ficheros JSON, que están en este caso
39:15 dentro de la carpeta harness. Si yo le pido a la LLM, dime qué hicimos ayer,
39:22 esto me va a lanzar la tool de recordar. Fíjate, me está instanciando la tool de
39:28 recall con esta query. Por lo tanto, esto es en mi sesión de tools recall con
39:35 esta query, ¿vale? Entonces, fíjate que luego aquí ya qué hace esta tool es lo
39:40 que yo implemento. Le puedo dar a yes. Sigo dándole a yes y pues ahora mismo
39:45 está yendo a hacer diferentes pruebas. Fíjate que ahora mismo estoy en el
39:49 bucle, ¿vale?, de aprobación de llamadas de tools en el bucle interno de este
39:53 agente. Como ves, ha detectado que no tiene nada de antayer, por lo que lo que
39:57 está en la memoria, que está dentro de esta carpeta, termina en ese punto, no
40:00 tiene memoria de ese de ese momento. Para que veas eh directamente cómo está
40:04 guardado todo esto, tengo aquí la carpeta .harness. Esto porque yo lo
40:08 he decidido así en mi código, lo podía poner en una configuración, eso es
40:12 totalmente libre. Si yo entro ahí, veo mi fichero de JSON de las diferentes
40:16 sesiones, donde tengo pues lo que se ha ido guardando en la memoria, ¿no? Con
40:21 sus tags para luego poderlo buscar. Esto es lo que yo tengo implementado en
40:26 session files. Aquí toda esta lógica de cómo se guarda lo tengo implementado
40:29 aquí. Y si me voy a la parte de sessions, aquí ya tengo pues cada uno de
40:34 mis recuerdos más explicados. Entonces, lo que he implementado es que la memoria
40:39 va a buscar en este index a qué fichero tiene que ir y luego agarra el fichero
40:42 para tener todo el contexto. Entonces, fíjate que yo aquí puedo implementarme
40:47 lo que quiera. Tengo el control total de mi harness. Es que, como ves, podemos
40:52 complicarlo todo lo que queramos. Podemos añadirle piezas, quitarle
40:55 piezas, eh, añadirle más providers, añadirle diferentes sistemas de memoria,
41:01 más comandos para cambiar más cosas. Pero al fin y al cabo, construir un
41:05 arnés no deja de ser tener un bucle. Es como construir un videojuego. Tienes un
41:09 bucle y lo que haces es le añades diferentes piezas de memoria, de tools,
41:14 de acceso a diferentes herramientas como MCPs, de diferentes formas de UI para
41:20 ver el coste. En este caso yo he utilizado una herramienta que se llama
41:23 Bubble Tea, que es básicamente una herramienta para poder construir
41:28 herramientas de terminal de una forma muy sencilla con Go, pero que no tiene
41:31 más secreto. Podría haber hecho una página web, podría haber hecho una línea
41:34 de comandos o podría haber hecho una UI con .NET si hubiera querido. Y si
41:39 seguiera explicando, puedo estar aquí durante horas hablando sobre cómo he
41:44 montado este proyecto, pero para eso precisamente he dejado el repositorio
41:47 del proyecto completo aquí abajo en la descripción para que le puedas echar un
41:51 ojo. Este repositorio que voy a dejar público justo cuando publique este
41:54 vídeo, pues tiene toda la explicación de todo lo que he ido explicando en este
41:59 vídeo y además algunas cosas extra que he ido haciendo fuera de cámara para
42:03 construir tu propio agente o tu propio arnés. Hay versión en inglés y
42:08 versión en español. Y aquí tienes básicamente todo lo que he ido haciendo,
42:12 todo lo que he ido explicando con las diferentes partes, el manejador de
42:16 contexto, el manejador de memoria, las herramientas, los subagentes, los
42:19 servidores MCP y una especie de tutorial, una especie de capítulos que
42:24 tú puedes ir leyendo para entender exactamente las decisiones y ver en
42:28 ejemplos de código mucho más concretos por qué hemos tomado ciertas decisiones
42:32 o hemos tomado otras. Por ejemplo, si quieres aprender más a cómo funciona el
42:36 loop de agentes o lo quieres construir tú por tu cuenta desde cero, te puedes
42:39 ir al capítulo número uno, ¿vale?, que está en el repositorio o al capítulo
42:45 uno, pero de la página web y ver exactamente qué es lo que sucede, qué es
42:50 el REPL con el ejemplo del videojuego, cómo lo puedes construir y algunos
42:55 ejemplos sacados de el proceso que yo he seguido cuando he construido mi arnés
43:00 para que tú puedas montarlo por tu cuenta siguiendo poco a poco cada uno de
43:04 los pasos. Obviamente cuando llegas al final de cada uno de los pasos, tienes
43:08 el botón de siguiente para ir implementando siguientes partes sobre tu
43:12 propio proyecto. La idea de este repositorio y la idea del propio arnés
43:16 es que sea un proyecto educativo. Es probable que no siga las mejores
43:20 prácticas de programación en Go. Es posible que si lo quisieras
43:23 comercializar como producto tuviera algunas partes que se tienen que
43:26 mejorar. Por lo tanto, el objetivo de este repo es ofrecerte un proyecto
43:32 suficientemente complejo para que puedas jugar, pero suficientemente sencillo
43:36 para que lo puedas entender. Para que todo esto sea mucho más visual, para que
43:40 puedas incluso utilizar el propio arnés que te puede descargar del repo para
43:44 practicar, he implementado el modo debug. Si tú pones /debug on, te
43:50 va a aparecer aquí este sistema de aquí, que es básicamente un visualizador, como
43:55 ves, de todo lo que va ocurriendo en el arnés. En este caso, pues estamos viendo
43:59 que le mandado "hello". Estamos viendo la llamada al provider, en este caso a
44:04 Anthropic. Si le das a enter, puedes ver exactamente el payload, el JSON que le
44:10 estamos mandando, ¿de acuerdo? y puedes ver si vas de izquierda a derecha la
44:14 respuesta que hemos recibido de Anthropic. Por lo tanto, tú puedes ir
44:18 viendo exactamente cómo afecta pues la gestión de la memoria, cómo afecta la
44:23 gestión del contexto en las llamadas que vas haciendo. Como ves aquí, el agent.md
44:27 me ha hinchado el system prompt de una manera brutal. Si yo le doy ahora
44:32 escape y vuelvo a poner "hello 2", fíjate que se me ha sumado a tres el número de
44:37 mensajes, ¿no?, que yo le he enviado, porque le voy mandando todo el
44:41 historial. Si yo le doy ahora aquí a leer esto, veré el hello inicial, luego
44:45 veo la respuesta de mi asistente y todo esto forma parte del contexto. Luego el
44:50 hello 2 y finalmente todo el system prompt. Fíjate como el system prompt ha
44:54 de ser pequeño. ¿Por qué? Porque yo lo llamo cada vez. Entonces, los input
44:58 tokens van sumando. Entonces, ver esto así es muy útil. También yo podría hacer
45:02 ahora el /compact y ponerle "sumar" para compactar el contexto y mandarle a
45:08 la, en este caso, el LLM de Anthropic que me genere la compactación. Le doy a esto
45:13 y vale, no me ha compactado nada porque no hay mucha cosa. Vamos a añadir otro
45:16 hello, le vamos a decir "write me a poem", ¿vale? Y ahora le vamos a decir, ahora
45:21 sí, "compact summary". Fíjate que el Compact Summary ahora me ha lanzado una
45:27 llamada a mi proveedor, por lo tanto, esta sumarización de contexto me ha
45:30 consumido tokens. Le doy a enter y veo aquí lo que yo le he mandado.
45:35 "Summary: hazme un resumen de la conversación de forma concisa, bla, bla..."
45:40 Entonces, yo aquí puedo ir viendo exactamente y aquí la respuesta. Este
45:42 sería el resultado. El contexto ahora incluye esto. El usuario me ha dicho,
45:47 "Hola con hello". El asistente ha ofrecido opciones para la sesión...
45:52 No ha habido ninguna temática escogida, no ha habido cambios de código y no ha
45:55 habido llamadas de herramientas. Por lo tanto, fíjate cómo el contexto ha
45:59 cambiado. ¿De acuerdo? /debug on es algo super interesante que puedes utilizar
46:04 para ir probando las cosas que necesites. Eh, fíjate aquí también que
46:08 ves el cambio de contexto. Y si aplicas también el Verbose, no me acuerdo, creo
46:13 que era así, Verbose. Vamos a poner sí, /verbose on. Ahora, si yo hago compact y
46:18 hago summary, voy a ver en el propio chat el antes y el después del contexto,
46:23 ¿vale? De esta forma podemos ver información más precisa. Es decir, la
46:27 idea es daros un arnés, que podáis jugar con él, que podáis extenderlo, que
46:32 podáis romperlo, que podáis añadir un provider, que podáis conectarlo con una
46:37 IA local, que podáis añadir comandos, que podáis implementar, yo que sé,
46:41 skills, que podáis implementar aquí una UI donde veáis los subagentes haciendo
46:45 cosas. La idea es que juguéis, que trasteéis con esto y quién sabe si
46:49 después de estar jugando un poquito con las diferentes lecciones y las
46:53 diferentes cosas que nosotros tenemos en este arnés, os planteáis lanzar un nuevo
46:57 producto, ¿no?, que hoy en día parece ser que sacamos un arnés hasta debajo de
47:01 las piedras, pues bienvenido sea. Aparte de las lecciones con el tutorial de cómo
47:05 construirlo paso a paso, en este repositorio, en esta web también
47:08 compartimos una serie de tutoriales directos, ¿vale? por ejemplo, cómo
47:13 añadir políticas de permisos nuevas, cómo añadir nuevos proveedores o cómo
47:16 añadir nuevas herramientas para que lo puedas ir siguiendo paso a paso. Y para
47:22 mí lo que creo que es más interesante de este repositorio son los ejercicios.
47:27 Es posible que vayamos incorporando más ejercicios, pero de momento pues están
47:30 estos seis de aquí, que es pues diferentes cosas que puedes hacer
47:35 agarrando el código tal como está del repositorio para aprender algún concepto
47:39 interesante. Por ejemplo, cómo modificar el agent loop para implementar reintento
47:44 de errores en las herramientas y tienes aquí una serie de enunciados para
47:49 poderlo hacer. También, por ejemplo, cómo añadir subagentes con Markdown,
47:55 ¿no? Hasta ahora los teníamos hardcodeados. ¿Cómo puedo hacer que se
47:59 cargue un Markdown de este estilo, como por ejemplo hacemos en Claude Code, y se
48:04 carguen estos agentes? Pues aquí tenemos también una serie de explicaciones sobre
48:09 cómo se podría implementar. Insisto, este repo es para jugar, para aprender,
48:14 para trastear un poquito. Échale un ojo y deja tus comentarios. De nuevo, sin
48:18 mucho más, te dejo el enlace en la descripción. Sé que este vídeo ha sido
48:21 muy largo, que ha habido muchos conceptos, pero con esto cerramos ya
48:25 nuestra serie de ingeniería de arneses. Espero que este repositorio te sea útil,
48:29 que puedas jugar con él, que te guste. Si has sido así, por favor, suscríbete y
48:32 déjame un buen like y nos vemos en el siguiente vídeo con más informática.