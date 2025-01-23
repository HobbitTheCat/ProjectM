// URL de base pour votre API
const BASE_URL = "http://0.0.0.0:8000";

// Variable globale pour stocker le jeton
let token;

// Test de connexion de l'utilisateur
async function testSignIn() {
    const payload = new URLSearchParams({
        username: "permanent_test_user@mock.com",
        password: "testPassword",
    });

    const headers = {
        accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    };

    try {
        const response = await fetch(`${BASE_URL}/api/v1/user/auth/signin`, {
            method: "POST",
            headers: headers,
            body: payload,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        // Assurons-nous que le jeton est bien présent dans la réponse
        console.assert(data.access_token, "Le jeton n'a pas été trouvé dans la réponse");
        console.assert(data.token_type === "Bearer", "Type de jeton incorrect");

        // Sauvegarder le jeton pour des tests ultérieurs
        token = data.access_token;

        console.log("Test d'entrée réussi, jeton :", token);
    } catch (error) {
        console.error("Erreur de test d'entrée :", error);
    }
}

// Test de l'emploi du temps hebdomadaire
async function testWeekSchedule() {
    if (!token) {
        console.error("Le jeton est manquant. Exécutez d'abord testSignIn.");
        return;
    }

    const headers = {
        accept: "application/json",
        Authorization: `Bearer ${token}`,
    };

    try {
        const response = await fetch(
            `${BASE_URL}/api/v1/schedule/week?date=2025-01-06`,
            {
                method: "GET",
                headers: headers,
            }
        );

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        console.assert(response.status === 200, "Le statut de la réponse doit être 200");
        console.log("Test de programmation réussi, données :", data);
    } catch (error) {
        console.error("Erreur du test de programmation :", error);
    }
}

// Exécution des tests
(async function runTests() {
    console.log("Exécution des tests...");
    await testSignIn(); // Tout d'abord, nous effectuons un test d'entrée
    await testWeekSchedule(); // Ensuite, le test de l'horaire
})();
