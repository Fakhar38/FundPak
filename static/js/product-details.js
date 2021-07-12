let productStoryBtn = document.querySelector(".product-section-2-menu-link-1");
let productContactBtn = document.querySelector(".product-section-2-menu-link-3");

let productStorySection = document.querySelector(".product-section-2-tab-1");
let productContactSection = document.querySelector(".product-section-2-tab-2");

productStoryBtn.addEventListener("click",()=>{
    productContactBtn.classList.remove("product-section-2-menu-link-active");
    productStoryBtn.classList.add("product-section-2-menu-link-active");
    productStorySection.style.display = "block";
    productContactSection.style.display = "none"
})


productContactBtn.addEventListener("click",()=>{
    productContactBtn.classList.add("product-section-2-menu-link-active");
    productStoryBtn.classList.remove("product-section-2-menu-link-active");
    productContactSection.style.display = "block";
    productStorySection.style.display = "none"
})