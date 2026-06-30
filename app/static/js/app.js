document.addEventListener('DOMContentLoaded', () => {

    const vistaLanding = document.getElementById('vista-landing');
    const vistaRegistro = document.getElementById('vista-registro');
    const vistaLogin = document.getElementById('vista-login');

    if (!vistaLanding || !vistaRegistro || !vistaLogin) return;

    const mostrarVista = (vistaObjetivo) => {
        vistaLanding.classList.add('hidden');
        vistaRegistro.classList.add('hidden');
        vistaLogin.classList.add('hidden');
        vistaObjetivo.classList.remove('hidden');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const actualizarRoleUI = (role) => {
        const field = document.getElementById('role-field');
        const badge = document.getElementById('role-badge');
        if (field) field.value = role;
        if (badge) {
            badge.textContent = role === 'nutritionist' ? 'NUTRICIONISTA' : 'USUARIO';
            badge.className = 'role-badge ' + (role === 'nutritionist' ? 'nutricionista' : 'usuario');
        }
    };

    document.querySelectorAll('.ir-a-registro').forEach(boton => {
        boton.addEventListener('click', () => {
            actualizarRoleUI('user');
            mostrarVista(vistaRegistro);
        });
    });

    document.querySelectorAll('.ir-a-registro-nutricionista').forEach(boton => {
        boton.addEventListener('click', () => {
            actualizarRoleUI('nutritionist');
            mostrarVista(vistaRegistro);
        });
    });

    document.querySelectorAll('.ir-a-login').forEach(boton => {
        boton.addEventListener('click', () => mostrarVista(vistaLogin));
    });

    document.querySelectorAll('.btn-volver-inicio').forEach(boton => {
        boton.addEventListener('click', () => mostrarVista(vistaLanding));
    });
});
