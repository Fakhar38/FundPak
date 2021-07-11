// // // // // // // // // // //
// code to make the swiper work
// // // // // // // // // // //

const swiper = new Swiper('.swiper-container', {
    direction: 'horizontal',
    loop: true,
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
});

// // // // // // // // // // // // // // // // //
//   code to make the search input work in header
// // // // // // // // // // // // // // // // //

let headerSearchBtn = document.querySelector(".header-search-icon-img");
let headerSearchInput = document.querySelector(".header-search-input-box");

document.body.addEventListener('click', function(e) {
    if (!e.target.classList.contains('header-search-icon-img')) {
        headerSearchInput.classList.remove("header-search-input-box-shown");
    }
});

headerSearchBtn.addEventListener("click",()=>{
    headerSearchInput.classList.add("header-search-input-box-shown");
    headerSearchInput.focus();
})

// // // // // // // // // // // // //
// code to make the scroll smooth work
// // // // // // // // // // // // //


// Select all links with hashes
$('a[href*="#"]')
  // Remove links that don't actually link to anything
  .not('[href="#"]')
  .not('[href="#0"]')
  .click(function(event) {
    // On-page links
    if (
      location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') 
      && 
      location.hostname == this.hostname
    ) {
      // Figure out element to scroll to
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      // Does a scroll target exist?
      if (target.length) {
        // Only prevent default if animation is actually gonna happen
        event.preventDefault();
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 500, function() {
          // Callback after animation
          // Must change focus!
          var $target = $(target);
          $target.focus();
          if ($target.is(":focus")) { // Checking if the target was focused
            return false;
          } else {
            $target.attr('tabindex','-1'); // Adding tabindex for elements not focusable
            $target.focus(); // Set focus again
          };
        });
      }
    }
  });

// // // // // // // // // // // // //
//   code to make the like button work
// // // // // // // // // // // // //

let likeBtn = document.querySelectorAll(".popular-projects-row-card-toprow-favorite-icon");

likeBtn.forEach((e)=>{
    e.addEventListener("click",()=>{
        console.log("im clicked")
        e.classList.toggle("popular-projects-row-card-toprow-favorite-icon-bigger")
        e.firstElementChild.classList.toggle("popular-projects-row-card-toprow-favorite-icon-path-liked");        
    })
})