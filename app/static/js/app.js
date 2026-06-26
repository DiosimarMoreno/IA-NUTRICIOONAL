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

    document.querySelectorAll('.ir-a-registro').forEach(boton => {
        boton.addEventListener('click', () => mostrarVista(vistaRegistro));
    });

    document.querySelectorAll('.ir-a-login').forEach(boton => {
        boton.addEventListener('click', () => mostrarVista(vistaLogin));
    });

    document.querySelectorAll('.btn-volver-inicio').forEach(boton => {
        boton.addEventListener('click', () => mostrarVista(vistaLanding));
    });
});
