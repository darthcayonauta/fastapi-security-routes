<?php
// Define la URL de la ruta protegida que deseas acceder
$protectedUrl = "http://localhost:8000/users/some";

// Configura la solicitud GET o POST
$ch = curl_init($protectedUrl);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

// Agrega el token de acceso en el encabezado 'Authorization'
$headers = ["Authorization: Bearer $accessToken"];
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

// Realiza la solicitud
$response = curl_exec($ch);

// Cierra la conexión cURL
curl_close($ch);

// Procesa la respuesta (puede ser JSON u otro formato según tu API)
// ...
?>
