document.addEventListener("DOMContentLoaded", function () {
  if ("geolocation" in navigator) {
    navigator.permissions
      .query({ name: "geolocation" })
      .then(function (result) {
        if (result.state === "granted" || result.state === "prompt") {
          navigator.geolocation.getCurrentPosition(
            function (position) {
              const lat = position.coords.latitude;
              const lon = position.coords.longitude;
              console.log("Position obtenue :", lat, lon);

              // Enregistrement via fetch
              fetch("/save-location/", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                  "X-CSRFToken": "{{ csrf_token }}",
                },
                body: JSON.stringify({ lat: lat, lon: lon }),
              })
                .then((response) => response.json())
                .then((data) => console.log("Réponse serveur :", data));
            },
            function (error) {
              switch (error.code) {
                case error.PERMISSION_DENIED:
                  alert("Autorisation de localisation refusée.");
                  break;
                case error.POSITION_UNAVAILABLE:
                  alert("Position indisponible.");
                  break;
                case error.TIMEOUT:
                  alert("La demande de localisation a expiré.");
                  break;
                default:
                  alert("Erreur de localisation.");
              }
            },
            {
              enableHighAccuracy: true,
              timeout: 10000,
              maximumAge: 0,
            }
          );
        } else {
          alert(
            "La localisation est désactivée. Activez-la dans les paramètres du navigateur."
          );
        }
      });
  } else {
    alert("La géolocalisation n'est pas supportée par votre navigateur.");
  }
});
