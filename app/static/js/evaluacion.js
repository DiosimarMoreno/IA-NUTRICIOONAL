document.addEventListener('DOMContentLoaded', () => {

    const inputEstatura = document.getElementById('estatura');
    const inputPeso = document.getElementById('peso');
    const btnSubmit = document.getElementById('btn-submit-clinico');
    const helperText = document.getElementById('helper-submit-text');

    function validarFormulario() {
        if (!inputEstatura || !inputPeso || !btnSubmit) return;

        const estaturaLleno = inputEstatura.value.trim() !== '';
        const pesoLleno = inputPeso.value.trim() !== '';
        const actividadSeleccionada = document.querySelector('input[name="nivel_actividad"]:checked') !== null;
        const objetivoSeleccionado = document.querySelector('input[name="objetivo_principal"]:checked') !== null;

        if (estaturaLleno && pesoLleno && actividadSeleccionada && objetivoSeleccionado) {
            btnSubmit.removeAttribute('disabled');
            btnSubmit.classList.add('btn-analisis-activo');
            if (helperText) {
                helperText.textContent = '¡Campos validados! Todo listo para ejecutar.';
                helperText.style.color = '#00e676';
            }
        } else {
            btnSubmit.setAttribute('disabled', 'true');
            btnSubmit.classList.remove('btn-analisis-activo');
            if (helperText) {
                helperText.textContent = 'Por favor complete todos los campos obligatorios para desbloquear el análisis.';
                helperText.style.color = '#2c3a50';
            }
        }
    }

    if (inputEstatura) inputEstatura.addEventListener('input', validarFormulario);
    if (inputPeso) inputPeso.addEventListener('input', validarFormulario);

    document.querySelectorAll('.card-select-option input[type="radio"]').forEach(radio => {
        radio.addEventListener('change', () => {
            document.querySelectorAll('.card-select-option .card-select-inner').forEach(inner => {
                inner.classList.remove('checked-border-verde');
                inner.querySelector('.checkmark-icon-indicator')?.remove();
            });

            if (radio.checked) {
                const contenedorInterno = radio.closest('.card-select-option').querySelector('.card-select-inner');
                if (contenedorInterno) {
                    contenedorInterno.classList.add('checked-border-verde');
                    contenedorInterno.insertAdjacentHTML('beforeend', '<div class="checkmark-icon-indicator"><ion-icon name="checkmark-circle"></ion-icon></div>');
                }
            }
            validarFormulario();
        });
    });

    document.querySelectorAll('.card-select-option-box input[type="radio"]').forEach(radio => {
        radio.addEventListener('change', () => {
            document.querySelectorAll('.card-box-inner-dest').forEach(box => {
                box.classList.remove('checked-border-verde', 'checked-border-azul', 'checked-border-naranja');
                box.querySelector('.checkmark-icon-indicator')?.remove();
            });

            if (radio.checked) {
                const contenedorCaja = radio.closest('.card-select-option-box').querySelector('.card-box-inner-dest');
                if (contenedorCaja) {
                    const colorDestino = contenedorCaja.getAttribute('data-target-color');
                    contenedorCaja.classList.add(`checked-border-${colorDestino}`);
                    contenedorCaja.insertAdjacentHTML('beforeend', '<div class="checkmark-icon-indicator"><ion-icon name="checkmark-circle"></ion-icon></div>');
                }
            }
            validarFormulario();
        });
    });

});
