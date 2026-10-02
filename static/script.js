const input = document.getElementById("inputText");
const result = document.getElementById("result");
const loading = document.getElementById("loading");


async function sendRequest(endpoint) {

    const text = input.value.trim();

    if (!text) {
        alert("Please enter a question or topic.");
        return;
    }

    result.innerText = "";
    loading.innerText = "🤖 EduGenie is thinking...";


    try {

        const response = await fetch(endpoint, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: text
            })

        });


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "Something went wrong."
            );

        }


        loading.innerText = "✅ Response generated";

        result.innerText = data.result;


    } catch (error) {

        loading.innerText = "❌ Error";

        result.innerText =
            "Error: " + error.message;

    }

}


function askQuestion() {

    sendRequest("/ask");

}


function generateQuiz() {

    sendRequest("/quiz");

}


function summarizeText() {

    sendRequest("/summarize");

}


function learningPath() {

    sendRequest("/learning-path");

}
