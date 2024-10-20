function submitRule() {
    const rule = document.getElementById("ruleInput").value;

    fetch('/create_rule/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rule_string: rule })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = "Rule submitted with ID: " + data.rule_id;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
