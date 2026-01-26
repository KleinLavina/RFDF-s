document.addEventListener('DOMContentLoaded', function() {
  const toggle = document.querySelector('.rdfs-header__toggle-x1');
  const nav = document.querySelector('.rdfs-header__nav-x1');
  const links = document.querySelectorAll('.rdfs-header__link-x1');

  if(!toggle || !nav) {
    console.log('Menu elements not found');
    return;
  }

  // Initialize links as visible
  links.forEach(link => {
    link.style.opacity = '1';
    link.style.transform = 'translateX(0)';
  });

  toggle.addEventListener('click', function(e) {
    e.stopPropagation();
    const isOpen = nav.classList.toggle('is-open-x1');
    toggle.setAttribute('aria-expanded', isOpen);
  });

  document.addEventListener('click', function(e) {
    if(!nav.contains(e.target) && !toggle.contains(e.target)){
      nav.classList.remove('is-open-x1');
      toggle.setAttribute('aria-expanded','false');
    }
  });

  document.addEventListener('keydown', function(e) {
    if(e.key === 'Escape'){
      nav.classList.remove('is-open-x1');
      toggle.setAttribute('aria-expanded','false');
    }
  });
});