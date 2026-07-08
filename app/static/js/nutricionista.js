(function () {
    'use strict';

    /* ─────────── SEARCH ─────────── */
    var searchInput = document.getElementById('busqueda-paciente');
    var patientItems = document.querySelectorAll('[data-paciente-id]');

    if (searchInput && patientItems.length) {
        searchInput.addEventListener('input', function () {
            var term = this.value.toLowerCase().trim();
            patientItems.forEach(function (item) {
                var name = (item.getAttribute('data-paciente-nombre') || '').toLowerCase();
                var email = (item.getAttribute('data-paciente-correo') || '').toLowerCase();
                var match = name.indexOf(term) !== -1 || email.indexOf(term) !== -1;
                item.style.display = match ? '' : 'none';
            });
        });
    }

    /* ─────────── TABLE SEARCH ─────────── */
    var tableSearch = document.getElementById('busqueda-tabla');
    var tableRows = document.querySelectorAll('#tabla-pacientes tbody tr');

    if (tableSearch && tableRows.length) {
        tableSearch.addEventListener('input', function () {
            var term = this.value.toLowerCase().trim();
            tableRows.forEach(function (row) {
                var text = row.textContent.toLowerCase();
                row.style.display = text.indexOf(term) !== -1 ? '' : 'none';
            });
        });
    }

    /* ─────────── RISK FILTER (table) ─────────── */
    var riskFilter = document.getElementById('filtro-riesgo');
    if (riskFilter && tableRows.length) {
        riskFilter.addEventListener('change', function () {
            var value = this.value;
            tableRows.forEach(function (row) {
                var risk = row.getAttribute('data-riesgo') || '';
                if (!value || risk === value) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    /* ─────────── DATE FILTER (table) ─────────── */
    var dateStart = document.getElementById('filtro-fecha-inicio');
    var dateEnd = document.getElementById('filtro-fecha-fin');

    function filterByDate() {
        if (!tableRows.length) return;
        var startVal = dateStart ? dateStart.value : '';
        var endVal = dateEnd ? dateEnd.value : '';

        tableRows.forEach(function (row) {
            var dateStr = row.getAttribute('data-fecha-actividad') || '';
            if (!startVal && !endVal) {
                row.style.display = '';
                return;
            }
            if (!dateStr) {
                row.style.display = 'none';
                return;
            }
            /* dateStr expected format: YYYY-MM-DD */
            var ts = dateStr.replace(/(\d{2})\/(\d{2})\/(\d{4})/, '$3-$2-$1');
            if (startVal && ts < startVal) {
                row.style.display = 'none';
                return;
            }
            if (endVal && ts > endVal) {
                row.style.display = 'none';
                return;
            }
            row.style.display = '';
        });
    }

    if (dateStart) dateStart.addEventListener('change', filterByDate);
    if (dateEnd) dateEnd.addEventListener('change', filterByDate);

    /* ─────────── FLASH MESSAGES AUTO-DISMISS ─────────── */
    var flashContainer = document.querySelector('.flash-contenedor');
    if (flashContainer) {
        flashContainer.addEventListener('click', function (e) {
            if (e.target.classList.contains('flash-cerrar')) {
                flashContainer.style.opacity = '0';
                setTimeout(function () { flashContainer.remove(); }, 300);
            }
        });
        setTimeout(function () {
            flashContainer.style.opacity = '0';
            setTimeout(function () { flashContainer.remove(); }, 300);
        }, 5000);
    }

    /* ─────────── PAGINATION ─────────── */
    var paginationBtns = document.querySelectorAll('.pagination-btn[data-page]');
    paginationBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            var page = parseInt(this.getAttribute('data-page'), 10);
            if (isNaN(page)) return;
            var url = new URL(window.location.href);
            url.searchParams.set('page', page);
            window.location.href = url.toString();
        });
    });

    /* ─────────── ANIMATIONS ─────────── */
    /* Intersection Observer for staggered reveals */
    if (window.IntersectionObserver) {
        var animItems = document.querySelectorAll('.anim-fade-up');
        if (animItems.length) {
            var observer = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });

            animItems.forEach(function (el) {
                el.style.opacity = '0';
                el.style.transform = 'translateY(16px)';
                el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                observer.observe(el);
            });
        }
    }

    /* ─────────── COUNTER ANIMATION ─────────── */
    var statNumbers = document.querySelectorAll('[data-count-to]');
    statNumbers.forEach(function (el) {
        var target = parseInt(el.getAttribute('data-count-to'), 10);
        if (isNaN(target)) return;
        var duration = 1200;
        var startTime = null;

        function step(timestamp) {
            if (!startTime) startTime = timestamp;
            var progress = Math.min((timestamp - startTime) / duration, 1);
            var eased = 1 - Math.pow(1 - progress, 3);
            var current = Math.floor(eased * target);
            el.textContent = current.toLocaleString('es');
            if (progress < 1) {
                requestAnimationFrame(step);
            }
        }
        requestAnimationFrame(step);
    });

})();
