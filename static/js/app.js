console.log("APP JS LOADED");
// ======================================================
// SCROLL REVEAL ANIMATION
// ======================================================

const revealElements =
document.querySelectorAll(

    ".property-card, \
     .analytics-card, \
     .inbox-card, \
     .chat-container, \
     .review-card, \
     .compare-table-wrapper, \
     .property-form-card, \
     .agent-card"

);

revealElements.forEach((element) => {

    element.classList.add("reveal");

});

const revealObserver =
new IntersectionObserver(

    (entries) => {

        entries.forEach((entry) => {

            if(entry.isIntersecting){

                entry.target.classList.add(
                    "active-reveal"
                );

            }

        });

    },

    {
        threshold:0.1
    }

);

revealElements.forEach((element) => {

    revealObserver.observe(element);

});

// ======================================================
// GET CSRF TOKEN
// ======================================================

function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {

        const cookies =
        document.cookie.split(";");

        for (let i = 0; i < cookies.length; i++) {

            const cookie =
            cookies[i].trim();

            if (
                cookie.substring(0, name.length + 1) ===
                (name + "=")
            ) {

                cookieValue =
                decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

                break;
            }

        }

    }

    return cookieValue;

}
// ======================================================
// MOBILE NAVBAR
// ======================================================

const menuToggle = document.getElementById("menuToggle");

const navLinks = document.getElementById("navLinks");

if(menuToggle){

    menuToggle.addEventListener("click", () => {

        navLinks.classList.toggle("active");

    });

}


// ======================================================
// PROFILE DROPDOWN
// ======================================================

const profileTrigger = document.querySelector(".profile-trigger");

const dropdownMenu = document.querySelector(".dropdown-menu");

if(profileTrigger){

    profileTrigger.addEventListener("click", () => {

        dropdownMenu.classList.toggle("show-dropdown");

    });

}


// ======================================================
// CLOSE MENU ON OUTSIDE CLICK
// ======================================================

document.addEventListener("click", (e) => {

    if(
        profileTrigger &&
        dropdownMenu &&
        !profileTrigger.contains(e.target) &&
        !dropdownMenu.contains(e.target)
    ){

        dropdownMenu.classList.remove("show-dropdown");

    }

});


// ======================================================
// NAVBAR SCROLL EFFECT
// ======================================================

const navbar = document.querySelector(".navbar");

window.addEventListener("scroll", () => {

    if(window.scrollY > 50){

        navbar.classList.add("navbar-scrolled");

    }

    else{

        navbar.classList.remove("navbar-scrolled");

    }

});

// ======================================================
// PROPERTY IMAGE SLIDER
// ======================================================

function changePropertyImage(element){

    const mainImage =
    document.getElementById("mainPropertyImage");

    mainImage.src = element.src;

    const thumbnails =
    document.querySelectorAll(".thumbnail-image");

    thumbnails.forEach((thumb) => {

        thumb.classList.remove("active-thumbnail");

    });

    element.classList.add("active-thumbnail");

}


// ACTIVE FIRST THUMBNAIL

const firstThumbnail =
document.querySelector(".thumbnail-image");

if(firstThumbnail){

    firstThumbnail.classList.add("active-thumbnail");

}

// ======================================================
// LIVE PROPERTY SEARCH FILTER
// ======================================================

const liveSearchInput =
document.getElementById("liveSearchInput");

const searchableProperties =
document.querySelectorAll(".searchable-property");

if(liveSearchInput){

    liveSearchInput.addEventListener("keyup", () => {

        const searchValue =
        liveSearchInput.value.toLowerCase();

        searchableProperties.forEach((property) => {

            const title =
            property.dataset.title;

            const location =
            property.dataset.location;

            const type =
            property.dataset.type;

            const matches =
            title.includes(searchValue) ||
            location.includes(searchValue) ||
            type.includes(searchValue);

            if(matches){

                property.parentElement.style.display = "block";

                property.style.opacity = "1";

                property.style.transform =
                "scale(1)";

            }

            else{

                property.parentElement.style.display = "none";

            }

        });

    });

}
// ======================================================
// AJAX FAVORITE TOGGLE
// ======================================================

const favoriteBtn =
document.getElementById("favoriteBtn");

if(favoriteBtn){

    favoriteBtn.addEventListener("click", async () => {

        const propertyId =
        favoriteBtn.dataset.propertyId;

        try{

           const response = await fetch(
    `/toggle-favorite/${propertyId}/`,
    {
        method: "POST",

        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
    }
);

            const data = await response.json();

            if(data.saved){

                favoriteBtn.classList.add("saved");

                favoriteBtn.innerHTML =
                "❤️ Saved";
showToast("Property saved ❤️");
            }

            else{

                favoriteBtn.classList.remove("saved");

                favoriteBtn.innerHTML =
                "🤍 Save Property";
   showToast("Property removed");

            }

        }

        catch(error){

            console.log(
                "Favorite Error:",
                error
            );

        }

    });

}

// ======================================================
// SIMPLE TOAST SYSTEM
// ======================================================

function showToast(message){

    if(!message){
        return;
    }

    const toast =
    document.createElement("div");

    toast.innerText = message;

    toast.style.position = "fixed";
    toast.style.top = "100px";
    toast.style.right = "20px";
    toast.style.background = "#16a34a";
    toast.style.color = "white";
    toast.style.padding = "16px 22px";
    toast.style.borderRadius = "12px";
    toast.style.fontWeight = "600";
    toast.style.zIndex = "99999";

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.remove();

    }, 3000);

}
/// ======================================================
// DARK MODE SYSTEM
// ======================================================

window.addEventListener("DOMContentLoaded", () => {

    const themeToggle =
    document.getElementById("themeToggle");

    if(!themeToggle){
        return;
    }

    // LOAD SAVED THEME

    const savedTheme =
    localStorage.getItem("theme");

    if(savedTheme === "dark"){

        document.body.classList.add(
            "dark-mode"
        );

        themeToggle.innerHTML = "☀️";
    }

    else{

        themeToggle.innerHTML = "🌙";
    }

    // TOGGLE THEME

    themeToggle.addEventListener("click", () => {

        document.body.classList.toggle(
            "dark-mode"
        );

        if(
            document.body.classList.contains(
                "dark-mode"
            )
        ){

            localStorage.setItem(
                "theme",
                "dark"
            );

            themeToggle.innerHTML = "☀️";
        }

        else{

            localStorage.setItem(
                "theme",
                "light"
            );

            themeToggle.innerHTML = "🌙";
        }

    });

});