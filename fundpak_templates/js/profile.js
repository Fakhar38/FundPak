let actionBtn = document.querySelectorAll(".profile-section-details-campaign-card-links-btn");


actionBtn.forEach((e)=>{
    e.addEventListener("click",()=>{
        if (e.nextElementSibling.style.display == "none") {
            e.nextElementSibling.style.display = "block"
        }
        else {
            e.nextElementSibling.style.display = "none"
        }
    })
})


let campaignBtn = document.querySelector(".profile-section-details-menu-link-1");
let contributeBtn = document.querySelector(".profile-section-details-menu-link-2");

let campaignSection = document.querySelector(".profile-section-details-campaign");
let contributeSection = document.querySelector(".profile-section-details-contributions");

campaignBtn.addEventListener("click",()=>{
    campaignBtn.classList.add("profile-section-details-menu-link-active")
    contributeBtn.classList.remove("profile-section-details-menu-link-active")
    campaignSection.style.display = "block";
    contributeSection.style.display = "none"
})

contributeBtn.addEventListener("click",()=>{
    contributeBtn.classList.add("profile-section-details-menu-link-active")
    campaignBtn.classList.remove("profile-section-details-menu-link-active")
    contributeSection.style.display = "block";
    campaignSection.style.display = "none"
})