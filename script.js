// Smooth scroll effect

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener("click", function(e) {
    e.preventDefault();

    document.querySelector(this.getAttribute("href")).scrollIntoView({
      behavior: "smooth"
    });
  });
});

// Sticky Navbar Shadow

window.addEventListener("scroll", () => {
  const navbar = document.querySelector(".navbar");

  if(window.scrollY > 50){
    navbar.style.boxShadow = "0 4px 20px rgba(0,0,0,0.15)";
  } else {
    navbar.style.boxShadow = "0 2px 10px rgba(0,0,0,0.08)";
  }
});
