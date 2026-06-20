document.addEventListener('DOMContentLoaded', () => {

    const usuarioGuardado = JSON.parse(localStorage.getItem("usuario_nutriexpert"));
    const navNombre = document.getElementById("nav-nombre-usuario");
    const navAvatar = document.getElementById("user-avatar-circle");
    const txtBienvenida = document.getElementById("bienvenida-usuario"); 

    if (usuarioGuardado) {
        if (navNombre) navNombre.textContent = usuarioGuardado.nombre.toLowerCase();
        
        if (navAvatar) navAvatar.textContent = usuarioGuardado.nombre.charAt(0).toUpperCase();
        
        if (txtBienvenida) {
            const nombreFormateado = usuarioGuardado.nombre.charAt(0).toUpperCase() + usuarioGuardado.nombre.slice(1).toLowerCase();
            
            txtBienvenida.innerHTML = `Hola, <span class="nombre-completo-gradiente">${nombreFormateado}</span>`;
        }
    }

    const vistaLanding = document.getElementById('vista-landing');
    const vistaRegistro = document.getElementById('vista-registro');
    const vistaLogin = document.getElementById('vista-login');

    const botonesIrARegistro = document.querySelectorAll('.ir-a-registro');
    const botonesIrALogin = document.querySelectorAll('.ir-a-login');
    const botonesVolverInicio = document.querySelectorAll('.btn-volver-inicio');

    const mostrarVista = (vistaObjetivo) => {
        if (!vistaLanding || !vistaRegistro || !vistaLogin) return;
        
        vistaLanding.classList.add('hidden');
        vistaRegistro.classList.add('hidden');
        vistaLogin.classList.add('hidden');

        vistaObjetivo.classList.remove('hidden');
        
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    botonesIrARegistro.forEach(boton => {
        boton.addEventListener('click', () => mostrarVista(vistaRegistro));
    });

    botonesIrALogin.forEach(boton => {
        boton.addEventListener('click', () => mostrarVista(vistaLogin));
    });

    botonesVolverInicio.forEach(boton => {
        boton.addEventListener('click', () => mostrarVista(vistaLanding));
    });

    const formRegistro = document.getElementById('form-registro');
    const formLogin = document.getElementById('form-login');

    if (formRegistro) {
        formRegistro.addEventListener('submit', async (e) => {
            e.preventDefault(); 
            
            const nombre = formRegistro.querySelector('input[type="text"]').value;
            const correo = formRegistro.querySelector('input[type="email"]').value;
            const edad = formRegistro.querySelector('input[type="number"]').value;
            const sexo = formRegistro.querySelector('select').value;
            const contrasena = formRegistro.querySelector('input[type="password"]').value;

            const datosUsuario = { nombre, correo, edad, sexo, contrasena };

            try {
                const respuesta = await fetch("http://localhost:3000/api/registrar", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(datosUsuario)
                });

                const resultado = await respuesta.json();

                if (resultado.status === "success") {
                    alert("✨ " + resultado.message);
                    formRegistro.reset(); 
                    mostrarVista(vistaLogin);
                } else {
                    alert("❌ Error: " + resultado.message);
                }
            } catch (error) {
                console.error("Error en la conexión de registro:", error);
                alert("⚠️ No se pudo establecer conexión con el servidor de Node.js.");
            }
        });
    }

    if (formLogin) {
        formLogin.addEventListener('submit', async (e) => {
            e.preventDefault(); 

            const correo = formLogin.querySelector('input[type="email"]').value;
            const contrasena = formLogin.querySelector('input[type="password"]').value;
            const credenciales = { correo, contrasena };

            try {
                const respuesta = await fetch("http://localhost:3000/api/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(credenciales)
                });

                const resultado = await respuesta.json();

                if (resultado.status === "success") {
                    alert("🔑 " + resultado.message);
                    formLogin.reset(); 
                    localStorage.setItem("usuario_nutriexpert", JSON.stringify(resultado.usuario));
                    window.location.href = "cuenta.html";
                } else {
                    alert("❌ Error de acceso: " + resultado.message);
                }
            } catch (error) {
                console.error("Error en la conexión de login:", error);
                alert("⚠️ No se pudo conectar con el servidor para validar tus credenciales.");
            }
        });
    }

    const inputEstatura = document.getElementById("estatura");
    const inputPeso = document.getElementById("peso");
    const btnSubmit = document.getElementById("btn-submit-clinico");
    const helperText = document.getElementById("helper-submit-text");

    function validarFormulario() {
        if (!inputEstatura || !inputPeso || !btnSubmit) return; 

        const estaturaLleno = inputEstatura.value.trim() !== "";
        const pesoLleno = inputPeso.value.trim() !== "";
        const actividadSeleccionada = document.querySelector('input[name="nivel_actividad"]:checked') !== null;
        const objetivoSeleccionado = document.querySelector('input[name="objetivo_principal"]:checked') !== null;

        if (estaturaLleno && pesoLleno && actividadSeleccionada && objetivoSeleccionado) {
            btnSubmit.removeAttribute("disabled");
            btnSubmit.classList.add("btn-analisis-activo");
            if (helperText) {
                helperText.textContent = "¡Campos validados! Todo listo para ejecutar.";
                helperText.style.color = "#00e676";
            }
        } else {
            btnSubmit.setAttribute("disabled", "true");
            btnSubmit.classList.remove("btn-analisis-activo");
            if (helperText) {
                helperText.textContent = "Por favor complete todos los campos obligatorios para desbloquear el análisis.";
                helperText.style.color = "#2c3a50";
            }
        }
    }

    if (inputEstatura) inputEstatura.addEventListener("input", validarFormulario);
    if (inputPeso) inputPeso.addEventListener("input", validarFormulario);

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

    if (btnSubmit) {
        btnSubmit.addEventListener("click", (e) => {
            e.preventDefault(); 
            window.location.href = "resultados.html";
        });
    }

    const btnCerrarSesion = document.getElementById("btn-cerrar-sesion");
    if (btnCerrarSesion) {
        btnCerrarSesion.addEventListener("click", () => {
            localStorage.removeItem("usuario_nutriexpert");
            window.location.href = "index.html"; 
        });
    }

});