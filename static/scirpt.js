document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");
    const button = document.querySelector("button");

    form.addEventListener("submit", function () {

        button.innerHTML = "Analyzing Resume...";
        button.disabled = true;

    });

});