/**
 * Animates elements on scroll using the Intersection Observer API.
 *
 * How it works:
 * 1. It selects all elements with the class 'animate-on-scroll'.
 * 2. An IntersectionObserver is created to watch these elements.
 * 3. When an element enters the viewport (is 'intersecting'), the 'is-visible' class is added to it.
 * 4. CSS transitions handle the animation from the initial state to the 'is-visible' state.
 * 5. The observer stops watching the element after it has become visible to prevent re-animation.
 */
document.addEventListener('DOMContentLoaded', () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target); // Animate only once
            }
        });
    }, { threshold: 0.1 }); // Trigger when 10% of the element is visible

    const elementsToAnimate = document.querySelectorAll('.animate-on-scroll');
    elementsToAnimate.forEach(element => observer.observe(element));
});