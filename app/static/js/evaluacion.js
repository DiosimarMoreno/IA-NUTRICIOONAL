document.addEventListener('DOMContentLoaded', () => {

    const inputEstatura = document.getElementById('estatura');
    const inputPeso = document.getElementById('peso');
    const btnSubmit = document.getElementById('btn-submit-clinico');
    const helperText = document.getElementById('helper-submit-text');
    const errorEstatura = document.getElementById('error-estatura');
    const errorPeso = document.getElementById('error-peso');
    const btnLimpiar = document.getElementById('btn-limpiar-form');

    const ESTATURA_MIN = 100;
    const ESTATURA_MAX = 250;
    const PESO_MIN = 30;
    const PESO_MAX = 250;

    function validarFormulario() {
        if (!inputEstatura || !inputPeso || !btnSubmit) return;

        const estatura = parseFloat(inputEstatura.value);
        const peso = parseFloat(inputPeso.value);
        const estaturaLleno = inputEstatura.value.trim() !== '';
        const pesoLleno = inputPeso.value.trim() !== '';
        const actividadSeleccionada = document.querySelector('input[name="nivel_actividad"]:checked') !== null;
        const objetivoSeleccionado = document.querySelector('input[name="objetivo_principal"]:checked') !== null;

        let estaturaValida = estaturaLleno && estatura >= ESTATURA_MIN && estatura <= ESTATURA_MAX;
        let pesoValido = pesoLleno && peso >= PESO_MIN && peso <= PESO_MAX;

        if (estaturaLleno && !estaturaValida) {
            inputEstatura.classList.add('input-invalid');
            if (errorEstatura) errorEstatura.classList.add('visible');
        } else {
            inputEstatura.classList.remove('input-invalid');
            if (errorEstatura) errorEstatura.classList.remove('visible');
        }

        if (pesoLleno && !pesoValido) {
            inputPeso.classList.add('input-invalid');
            if (errorPeso) errorPeso.classList.add('visible');
        } else {
            inputPeso.classList.remove('input-invalid');
            if (errorPeso) errorPeso.classList.remove('visible');
        }

        if (estaturaValida && pesoValido && actividadSeleccionada && objetivoSeleccionado) {
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

    // Pre-select radio buttons that were pre-filled via HTML checked attribute
    document.querySelectorAll('.card-select-option input[type="radio"]:checked, .card-select-option-box input[type="radio"]:checked').forEach(radio => {
        radio.dispatchEvent(new Event('change'));
    });

    // Limpiar formulario
    if (btnLimpiar) {
        btnLimpiar.addEventListener('click', () => {
            inputEstatura.value = '';
            inputPeso.value = '';
            document.getElementById('grasa-corporal').value = '';

            document.querySelectorAll('.card-select-option input[type="radio"], .card-select-option-box input[type="radio"]').forEach(r => {
                r.checked = false;
            });

            document.querySelectorAll('.card-select-inner, .card-box-inner-dest').forEach(el => {
                el.classList.remove('checked-border-verde', 'checked-border-azul', 'checked-border-naranja');
                el.querySelector('.checkmark-icon-indicator')?.remove();
            });

            inputEstatura.classList.remove('input-invalid');
            inputPeso.classList.remove('input-invalid');
            if (errorEstatura) errorEstatura.classList.remove('visible');
            if (errorPeso) errorPeso.classList.remove('visible');

            const banner = document.getElementById('prefill-banner');
            if (banner) banner.style.display = 'none';

            validarFormulario();
        });
    }

    // Auto-activate submit if fields have pre-filled values
    validarFormulario();

});
