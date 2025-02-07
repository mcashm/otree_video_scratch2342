document.addEventListener("DOMContentLoaded", () => {

    if (window.self == window.top){
        document.querySelector("#ovl-error").classList.remove("d-none")
    } else {
        document.querySelector("#ovl-error").remove()
    }

});
