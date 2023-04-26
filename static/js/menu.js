'use stricks'

// "mobile menu"
const btnNav = document.querySelector(".btn-nav");
const header = document.querySelector(".main-header");

openMenu = function() {
    header.classList.toggle("nav-open")
    btnNav.classList.toggle("N800-c")
    console.log("click");
}

btnNav.addEventListener("click", openMenu);

// "sticky menu"
const marker = document.querySelector(".sticty-marker");

const observer = new IntersectionObserver(function(entries){
    const ent = entries[0];
    if(ent.isIntersecting)
        document.body.classList.remove("sticky-nav")    

    if(ent.isIntersecting === false)
        document.body.classList.add("sticky-nav")
}, 
{
    root:null, 
    threshold : 0,
    rootMargin : "-80px"
});
observer.observe( marker );