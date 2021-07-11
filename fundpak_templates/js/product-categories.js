let categoryBtn = document.querySelectorAll(".product-categories-showroom-menu-category-heading");

categoryBtn.forEach((e)=>{
    e.addEventListener("click",()=>{
        // console.log(e.nextElementSibling.style.overflow)

        if (e.nextElementSibling.style.overflow == "hidden") {
            e.nextElementSibling.style.transition = "all 0.5s ease-in-out";
            e.nextElementSibling.style.overflow = "visible";
            e.nextElementSibling.style.height = "35vh";
            e.children[1].style.transform = "rotate(180deg)";            
            
        }
        else {
            e.nextElementSibling.style.transition = "all 0.5s ease-in-out";
            e.nextElementSibling.style.overflow = "hidden";
            e.nextElementSibling.style.height = "0";
            e.children[1].style.transform = "rotate(0deg)";
        }
    })
})
