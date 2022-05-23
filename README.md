# TFM 2022
Sensorización de las aulas, análisis de datos y decisiones de actuación

Archivos dentro del folder Arduino son aquellos que pertenecen a los sensores ubicados en el aula. Cada uno de los sensores se encuentra identificado dentro del mismo archivo y de ser necesario actualizar determinada mota se deben actualizar los datos del HEADER de la trama para no perder su identificacion.

Archivos dentro del folder Python son aquellos que pertenecen al Raspberry tal como la lectura y decodificacion de las tramas provenientes de los sensores, su comunicacion con la DB o Cloud mediante el protocolo MQTT y su comunicacion con los actuadores.

Archivos dentro del folder Test solo se utilizan para prototipar o realizar pruebas provenientes de los sensores, no debe afectar el funcionamiento de ningun componente.
