function calculateMortage(){
    const form = document.getElementById('mortgageForm');
            const formData = new FormData(form);
            
            fetch('/calculate_mortgage', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('result').innerHTML = `
                    <p><strong>Monthly Payment:</strong> £${data.monthly_payment}</p>
                    <p><strong>Total Interest Paid:</strong> £${data.total_interest}</p>
                `;
            })
            .catch(error => console.error('Error:', error));
}