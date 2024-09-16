window.CarouselModule = window.CarouselModule || (function() {
    const carousels = new Map();

        function initializeCarousel(carousel) {
            if (carousels.has(carousel)) return;

            const items = Array.from(carousel.querySelectorAll('[data-carousel-item]'));
            const content = carousel.querySelector('[data-ref="content"]');
            const prevButton = carousel.querySelector('[data-ref="prevButton"]');
            const nextButton = carousel.querySelector('[data-ref="nextButton"]');

            const {autoplay, orientation} = carousel.dataset;

            let currentIndex = 0;
            let autoplayInterval;

            const {height} = carousel.getBoundingClientRect();

            function setupOrientation() {
                if (orientation === 'vertical') {

                    items.forEach(item => item.classList.add('pt-4'));
                    content.classList.add('-mt-4', 'flex-col');
                    content.style.height =  `${Math.floor(height+16)}px`
                    if (prevButton) prevButton.classList.add('-top-12', 'left-1/2', '-translate-x-1/2', 'rotate-90');
                    if (nextButton) nextButton.classList.add('-bottom-12', 'left-1/2', '-translate-x-1/2', 'rotate-90');
                } else {
                    items.forEach(item => item.classList.add('pl-4'));
                    content.classList.add('-ml-4');
                    prevButton.classList.add('-left-12', 'top-1/2', '-translate-y-1/2');
                    nextButton.classList.add('-right-12', 'top-1/2', '-translate-y-1/2');
                }
            }

            function updateCarousel() {
                if (orientation === 'horizontal') content.style.transform = `translate3d(-${currentIndex * 100}%, 0px, 0px)` 
                else content.style.transform = `translate3d(0px, -${(height+16) * currentIndex}px, 0px)`
            }

            function moveCarousel(direction) {
                currentIndex = (currentIndex + direction + items.length) % items.length;
                updateCarousel();
            }

            function setupEventListeners() {
                if (prevButton) prevButton.addEventListener('click', () => moveCarousel(-1));
                if (nextButton) nextButton.addEventListener('click', () => moveCarousel(1));
            }

            function startAutoplay() {
                if (autoplay === 'true' && !autoplayInterval) {
                    autoplayInterval = setInterval(() => moveCarousel(1), 5000);
                }
            }

            function stopAutoplay() {
                if (autoplayInterval) {
                    clearInterval(autoplayInterval);
                    autoplayInterval = null;
                }
            }

            setupOrientation();
            setupEventListeners();
            startAutoplay();

            carousels.set(carousel, { stopAutoplay });
        }

        function initializeAllCarousels() {
            document.querySelectorAll('[data-ref="carousel"]').forEach(initializeCarousel);
        }

        function handleNavigation() {
            carousels.forEach(({ stopAutoplay }) => stopAutoplay());
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', initializeAllCarousels);
        window.addEventListener('popstate', handleNavigation);
        if ('navigation' in window) {
            navigation.addEventListener('navigate', event => {
                if (event.navigationType === 'push' || event.navigationType === 'replace') {
                    handleNavigation();
                }
            });
        }

        // Public API
        return {
            init: initializeAllCarousels,
        };
    })();

    // Initialize after HTMX swaps
    document.body.addEventListener('htmx:afterSwap', CarouselModule.init);