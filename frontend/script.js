document.getElementById("bioForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    const career = document.getElementById("career").value;
    const personality = document.getElementById("personality").value;
    const interests = document.getElementById("interests").value;
    const goals = document.getElementById("goals").value;

    const formData = {
        preferences: {
            career: career,
            personality: personality,
            interests: interests,
            goals: goals
        }
    };

    fetch('http://127.0.0.1:5000/generate_bio/ui/hugging_face_API', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.bio) {
            document.getElementById("generatedBio").textContent = data.bio;
        } else {
            document.getElementById("generatedBio").textContent = "Error generating bio.";
        }
    })
    .catch(error => {
        document.getElementById("generatedBio").textContent = "Error connecting to the server.";
        console.error('Error:', error);
    });
});
