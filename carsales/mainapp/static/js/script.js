document.addEventListener('DOMContentLoaded', function() {
    // Универсальная функция для всех кнопок с классом .scroll-btn
    document.querySelectorAll('.scroll-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Получаем ID целевого элемента из href кнопки
            const targetId = this.getAttribute('href').substring(1);
            const target = document.getElementById(targetId);

            if (target) {
                if ('scrollBehavior' in document.documentElement.style) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                } else {
                    smoothScrollPolyfill(target);
                }
            }
        });
    });

    // Полифил для плавной прокрутки
    function smoothScrollPolyfill(target) {
        const targetPosition = target.getBoundingClientRect().top + window.pageYOffset;
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        const duration = 800;
        let startTime = null;

        function animation(currentTime) {
            if (!startTime) startTime = currentTime;
            const timeElapsed = currentTime - startTime;
            const progress = Math.min(timeElapsed / duration, 1);
            const ease = easeInOutQuad(progress);
            window.scrollTo(0, startPosition + distance * ease);
            if (timeElapsed < duration) requestAnimationFrame(animation);
        }

        function easeInOutQuad(t) {
            return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
        }
        
        requestAnimationFrame(animation);
    }
});

// Динамическая загрузка моделей при изменении производителя
document.addEventListener('DOMContentLoaded', function() {
    const manufacturerSelect = document.getElementById('id_manufacturer');
    const modelSelect = document.getElementById('id_model');
    
    if (manufacturerSelect && modelSelect) {
        manufacturerSelect.addEventListener('change', function() {
            const manufacturerId = this.value;
            
            if (manufacturerId) {
                fetch(`/cars/get-models/?manufacturer=${manufacturerId}`)
                    .then(response => response.json())
                    .then(data => {
                        modelSelect.innerHTML = '';
                        const defaultOption = document.createElement('option');
                        defaultOption.value = '';
                        defaultOption.textContent = '---------';
                        modelSelect.appendChild(defaultOption);
                        
                        data.models.forEach(model => {
                            const option = document.createElement('option');
                            option.value = model.id;
                            option.textContent = model.name;
                            modelSelect.appendChild(option);
                        });
                    });
            } else {
                modelSelect.innerHTML = '';
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.textContent = '---------';
                modelSelect.appendChild(defaultOption);
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const slider = document.getElementById('sliderContainer');
    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const dots = document.querySelectorAll('.dot');
    const totalSlides = slides.length;
    let currentIndex = 0;
    
    // Функция обновления слайдера
    function updateSlider() {
        slider.style.transform = `translateX(-${currentIndex * 100}%)`;
        
        // Обновление точек
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentIndex);
        });
    }
    
    // Переключение слайдов
    function goToSlide(index) {
        currentIndex = index;
        updateSlider();
    }
    
    // Следующий слайд
    function nextSlide() {
        currentIndex = (currentIndex + 1) % totalSlides;
        updateSlider();
    }
    
    // Предыдущий слайд
    function prevSlide() {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        updateSlider();
    }
    
    // Обработчики событий
    if (prevBtn) prevBtn.addEventListener('click', prevSlide);
    if (nextBtn) nextBtn.addEventListener('click', nextSlide);
    
    dots.forEach(dot => {
        dot.addEventListener('click', function() {
            const index = parseInt(this.getAttribute('data-index'));
            goToSlide(index);
        });
    });
    
    // Клик по краям изображения
    slider.addEventListener('click', function(e) {
        const rect = this.getBoundingClientRect();
        const clickPosition = e.clientX - rect.left;
        const third = rect.width / 3;
        
        if (clickPosition < third) prevSlide();
        if (clickPosition > 2 * third) nextSlide();
    });
    
    // Автопрокрутка
    let slideInterval = setInterval(nextSlide, 5000);
    
    slider.addEventListener('mouseenter', () => clearInterval(slideInterval));
    slider.addEventListener('mouseleave', () => slideInterval = setInterval(nextSlide, 5000));
});

document.querySelectorAll('.scroll-btn').forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        const targetSection = this.getAttribute('data-target');
        const currentPage = window.location.pathname;

        // Если текущая страница — главная (или другая целевая), прокручиваем к секции
        if (currentPage === '/' || currentPage === '/index.html') {
            const section = document.getElementById(targetSection);
            if (section) {
                section.scrollIntoView({ behavior: 'smooth' });
            }
        } else {
            // Иначе перенаправляем на главную с якорем
            window.location.href = `/#${targetSection}`;
        }
    });
});