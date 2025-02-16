document.getElementById("show_wifi").addEventListener("click",function() {
    document.querySelector(".title").textContent = "Wifi QR code";
    let buttonsToHide = ["show_wifi","show_url"]
    buttonsToHide.forEach(id => {
        let button = document.getElementById(id);
        if (button) button.style.display = "none";      // Ocultar botones
    });
    

    let form = document.getElementById("hidden-wifi");
    if (form) {
        form.style.transitionDuration = "0.6s"
        form.classList.add("show");                     // Mostrar formulario
    }

    setupValidation("hidden-wifi", "confirm_button_wifi");
});

document.getElementById("back_button").addEventListener("click",function(){
    document.querySelector(".title").textContent = "Select the type of QR code"
    let form = document.getElementById("hidden-wifi");
    if (form) {
        form.style.transitionDuration = (0) + 's'
        form.classList.remove("show"); // Ocultar el formulario correctamente
    }
    let buttonsToShow = ["show_wifi","show_url"]
    buttonsToShow.forEach(id =>{
        let button = document.getElementById(id)
        if (button) button.style.display = "block"; // Volver a mostrar los botones
    })
});
document.getElementById("confirm_button_wifi").addEventListener("click", function() {
    let input = document.createElement("input");
    input.type = "hidden";
    input.name = "qr_type";
    input.value = "wifi";
    document.getElementById("hidden-wifi").appendChild(input);
    const imagen = document.getElementById("imagen");
    imagen.style.display= "block";
});
// URL
document.getElementById("show_url").addEventListener("click",function(){
    document.querySelector(".title").textContent = "URL QR code";
    let buttonsToHide = ["show_wifi","show_url"]
    buttonsToHide.forEach(id => {
        let button = document.getElementById(id)
        if (button) button.style.display = "none"
    });
    let form = document.getElementById("hidden-url");
    if (form) {
        form.style.transitionDuration = "0.6s"
        form.classList.add("show");
    }
    setupValidation("hidden-url", "confirm_button_url");
});
document.getElementById("back_bttn").addEventListener("click",function(){
    document.querySelector(".title").textContent = "Select the type of QR code"
    let form = document.getElementById("hidden-url");
    if (form) {
        form.style.transitionDuration = (0) + 's'
        form.classList.remove("show"); // Ocultar el formulario correctamente
    }
    let buttonsToShow = ["show_wifi","show_url"]
    buttonsToShow.forEach(id =>{
        let button = document.getElementById(id)
        if (button) button.style.display = "block"; // Volver a mostrar los botones
    })
});
document.getElementById("confirm_button_url").addEventListener("click", function() {
    let input = document.createElement("input");
    input.type = "hidden";
    input.name = "qr_type";
    input.value = "link";
    document.getElementById("hidden-url").appendChild(input);
    const imagen = document.getElementById("imagen");
    imagen.style.display= "block";
});
/////////////
document.getElementById("hidden-wifi").addEventListener("submit", async function(event) {
    event.preventDefault();  // Evita que la página se recargue

    let formData = new FormData(this);

    let response = await fetch("/", {
        method: "POST",
        body: formData
    });


    if (response.redirected) {
        window.location.href = response.url;  // Redirige automáticamente si Flask devuelve una redirección
    } else {
        let result = await response.text();
        document.body.innerHTML = result;
    }
});
const imagen = document.getElementById("imagen");
if (imagen && imagen.src) {
    imagen.style.display = "block";
}
// VALIDACION

function setupValidation(formId, buttonId) {
    let form = document.getElementById(formId);
    if (!form.classList.contains("show")) return;  // Si el formulario no está visible, no hacer nada

    let inputs = form.querySelectorAll(".form-control");
    let selects = form.querySelectorAll(".form-select");
    let button = document.getElementById(buttonId);

    function verifyFields() {
        let inputsEmpty = Array.from(inputs).some(input => input.value.trim() === "");
        let selectsInvalid = Array.from(selects).some(select => select.value === "default");
        button.disabled = inputsEmpty || selectsInvalid;
    }

    inputs.forEach(input => input.addEventListener("input", verifyFields));
    selects.forEach(select => select.addEventListener("change", verifyFields));

    verifyFields();  // Ejecutar validación inicial
}