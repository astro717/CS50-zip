

document.addEventListener('DOMContentLoaded', function () {
 // Verificar si estamos en la página de Trivia
 if (document.title === 'Trivia test') {
    let score = 0; // Variable para la puntuación
    const scoreDisplay = document.getElementById('score');
    const questions = document.querySelectorAll('.trivia-question');
    const showScoreButton = document.getElementById('showScore');

    questions.forEach((question) => {
        const buttons = question.querySelectorAll('.trivia-btn');

        buttons.forEach(button => {
            button.addEventListener('click', function () {
                // Verificar si la respuesta es correcta
                if (button.textContent === 'Madrid' || button.textContent === '1936' || button.textContent === '9.58s' || button.textContent === 'Rust' || button.textContent === 'TCP') {
                    button.classList.remove('btn-danger');
                    button.classList.add('btn-success'); // Muestra que la respuesta es correcta
                    score++; // Aumenta la puntuación
                } else {
                    button.classList.remove('btn-danger');
                    button.classList.add('btn-danger'); // Muestra que la respuesta es incorrecta
                }

                // Desactivar todos los botones de la misma pregunta
                buttons.forEach(btn => btn.disabled = true);
            });
        });
    });

    // Mostrar la puntuación al hacer clic en el botón de "Show Score"
    showScoreButton.addEventListener('click', function () {
        scoreDisplay.textContent = score;
    });
}
// Verificar si estamos en la página de List of Tasks
if (document.title === 'List of Tasks') {

    const inputTarea = document.getElementById('nuevaTarea');
        const botonAgregar = document.getElementById('agregarTarea');
        const listaTareas = document.getElementById('listaTareas');
        const botonBorrarTodas = document.getElementById('borrarTodas');

        botonAgregar.addEventListener('click', function () {
            // Capturar el valor del input y validar si está vacío
            const tarea = inputTarea.value.trim();
            if (tarea === '') {
                alert('Please enter a task!');
                return;
            }

            // Crear un nuevo elemento de lista y agregar el texto de la tarea
            const li = document.createElement('li');
            li.textContent = tarea;
            li.classList.add('list-group-item', 'mt-2'); // Añadir clases de estilo

            // Crear el botón de eliminar y agregarlo al <li>
            const botonEliminar = document.createElement('button');
            botonEliminar.textContent = 'Delete';
            botonEliminar.classList.add('btn', 'btn-danger', 'ml-2');
            botonEliminar.addEventListener('click', function () {
                li.remove(); // Elimina la tarea específica
            });

            li.appendChild(botonEliminar); // Agregar el botón al <li>
            listaTareas.appendChild(li); // Agregar el <li> a la lista

            // Limpiar el campo de entrada
            inputTarea.value = '';
        });

        // Lógica para borrar todas las tareas
        botonBorrarTodas.addEventListener('click', function () {
            listaTareas.innerHTML = ''; // Elimina todo el contenido de la lista
        });

}

// Verificar si estamos en la página de Motivation 101
if (document.title === 'Motivation 101') {

    // Lógica específica para la página de Motivation 101
    const quotes = ['"The only way to do great work is to love what you do." – Steve Jobs',
                    '"Don’t watch the clock; do what it does. Keep going." – Sam Levenson',
                    '"The harder you work for something, the greater you’ll feel when you achieve it."',
                    '"Success is not the key to happiness. Happiness is the key to success. If you love what you are doing, you will be successful." – Albert Schweitzer',
                    '"Your limitation—it’s only your imagination."',
                    "Push yourself, because no one else is going to do it for you."];

    const button = document.getElementById('generarFrase');
    const output = document.getElementById('fraseMostrada');
    button.addEventListener('click', function()
        {
        // floor redondea hacia abajo
        const randomQuote = Math.floor(Math.random() * quotes.length);
        const selectedQuote = quotes[randomQuote];
        output.textContent = selectedQuote;
        });
    }
});

