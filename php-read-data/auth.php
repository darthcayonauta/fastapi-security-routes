<?php
// Define las credenciales para la autenticación
$credentials = [
    "username" => "tim",
    "password" => "tim1234"
];

// Define la URL del endpoint de autenticación
$authUrl = "http://localhost:8000/token";

// Configura la solicitud POST
$ch = curl_init($authUrl);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($credentials));

// Realiza la solicitud
$response = curl_exec($ch);

// Cierra la conexión cURL
curl_close($ch);

// Decodifica la respuesta JSON
$tokenData = json_decode($response, true);

// Extrae el token de acceso
$accessToken = $tokenData["access_token"];

// Utiliza $accessToken para realizar solicitudes a rutas protegidas

// Define la URL de la ruta protegida que deseas acceder
$protectedUrl = "http://localhost:8000/users/some"; // Asegúrate de que coincida con la ruta protegida en tu API

// Configura la solicitud GET
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
if ($response) {
    $data = json_decode($response, true);
    if ($data) {
        // Procesa los datos como sea necesario
        print_r($data);
    } else {
        echo "Error al decodificar la respuesta JSON.";
    }
} else {
    echo "Error al realizar la solicitud.";
}
?>
