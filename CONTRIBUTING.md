# Guía de contribución

## Cómo previsualizar el README

Antes de enviar cambios al archivo `README.md`, es importante comprobar que su contenido se visualice correctamente en GitHub.

### Previsualización desde la rama propia

1. Subir los cambios a la rama de trabajo del repositorio personal.
2. Abrir el repositorio en GitHub y seleccionar la rama correspondiente.
3. Entrar al archivo `README.md`.
4. Seleccionar la vista **Preview**, si está disponible, para comprobar cómo se muestra el contenido Markdown.
5. Revisar que los títulos, enlaces, listas e imágenes se visualicen correctamente.

### Previsualización desde el Pull Request

1. Abrir el Pull Request que contiene los cambios del README.
2. Seleccionar la pestaña **Files changed**.
3. Buscar el archivo `README.md` entre los archivos modificados.
4. Abrir el menú del archivo y seleccionar **View file**, cuando esté disponible, para revisar su contenido renderizado.
5. Comprobar que el formato, los enlaces y las imágenes se muestren correctamente antes de solicitar la revisión.

### Comprobación del modo oscuro

1. Abrir GitHub e ingresar a **Settings**.
2. Seleccionar **Appearance**.
3. Cambiar el tema a **Dark**.
4. Regresar al README y comprobar que el texto, los enlaces y las imágenes sean legibles.
5. Repetir la comprobación con el tema **Light** para verificar que el contenido se visualice correctamente en ambos modos.

## Reglas de edición del README

Para mantener organizada la documentación del repositorio, se deben seguir estas reglas al modificar los archivos `README.md` y `README.en.md`:

1. **Marcadores de sección:** El marcador `<!-- seccion:X -->` identifica una sección del README. La letra `X` representa el nombre o identificador de esa sección. Se deben respetar estos marcadores para mantener la estructura del documento.

2. **Bloques automáticos:** El marcador `<!-- auto:X -->` indica el inicio de un bloque generado automáticamente y `<!-- /auto:X -->` indica su final. Nunca se debe editar manualmente el contenido que se encuentra entre ambos marcadores.

3. **Una sección por Pull Request:** Cada PR debe modificar únicamente una sección del README, evitando cambios en otras partes del documento.

4. **Consistencia entre idiomas:** Los archivos `README.md` y `README.en.md` deben contener las mismas secciones y mantener el mismo orden, aunque estén escritos en idiomas diferentes.

5. **Revisión de cambios:** Antes de enviar un PR, se debe comprobar que los marcadores se hayan respetado y que solamente se haya modificado la sección correspondiente.

## Revisión y merge de Pull Requests

Antes de integrar los cambios en el proyecto, cada Pull Request debe pasar por un proceso de revisión para comprobar que cumple los requisitos del repositorio.

### Revisión del Pull Request

1. Verificar que el Pull Request tenga como rama de destino `dev`, salvo que la tarea indique otra rama.
2. Revisar la descripción del PR y comprobar que los cambios correspondan a la issue asociada.
3. Esperar la revisión de los responsables del código (*CODEOWNERS*) cuando corresponda y atender las observaciones recibidas.
4. Realizar las correcciones solicitadas y actualizar el Pull Request.

### Comprobaciones antes del merge

Antes de integrar los cambios, se debe comprobar que:

- Las verificaciones de integración continua (CI) hayan finalizado correctamente y estén en verde.
- No existan conflictos pendientes con la rama de destino.
- Se hayan atendido las observaciones de revisión y se cumplan las aprobaciones exigidas por las reglas del repositorio.

### Integración de los cambios

1. Confirmar que el Pull Request cumple los requisitos de revisión y las comprobaciones automáticas.
2. Utilizar el mecanismo de merge habilitado por el repositorio y respetar sus reglas de integración.
3. No realizar `push` directamente a `main`. Los cambios deben integrarse mediante un Pull Request y seguir el proceso de revisión establecido.
4. Después del merge, comprobar que el Pull Request figure como integrado y que la issue asociada se cierre cuando corresponda.
