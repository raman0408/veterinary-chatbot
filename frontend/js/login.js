const loginBtn = document.getElementById("loginBtn");

loginBtn.addEventListener("click", async () => {
    const phone = document.getElementById("phoneInput").value;

    if (!phone){
        alert("Please enter a phone number")
        return;
    }
    try{
        const response = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                phone: phone
            })
        });
        const data = await response.json();

        console.log(data);

        localStorage.setItem("phone", phone);

        window.location.href = "chat.html";

    } catch (error){
        console.error(error);
        alert("Login failed");
    }
});
