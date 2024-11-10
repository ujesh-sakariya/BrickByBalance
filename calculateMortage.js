src="https://cdn.jsdelivr.net/npm/chart.js"

function calculateMortgage(){
    const loanAmount = parseFloat(document.getElementById('loanAmount').value)
    const downPayment = parseFloat(document.getElementById('downPayment').value);
    const loanTerm = parseInt(document.getElementById('loanTerm').value);
    const interestRate = parseFloat(document.getElementById('interestRate').value) / 100;
    const monthlySavings = parseFloat(document.getElementById('monthlySavings').value);

    if (isNaN(loanAmount) || isNaN(downPayment) || isNaN(loanTerm) || isNaN(interestRate) || isNaN(monthlySavings)) {
        alert("Please fill in all fields with valid numbers.");
        return;
    }

    const principal = loanAmount - downPayment;
    const monthlyRate = interestRate / 12;
    const totalPayments = loanTerm * 12
    const monthlyPayment = (principal * monthlyRate * Math.pow(i + monthlyRate, totalPayments)) / (Math.pow(1 + monthlyRate, totalPayments) - 1);

    document.getElementById('mortgageResult').innerHTML = `Your estimated monthly mortgage payment is £${monthlyPayment.toFixed(2)}`;

    const daysToSave = 365 * loanTerm;  // Total days for saving
    const savingsValues = getSavingsValues(downPayment, monthlySavings, interestRate, true, daysToSave);

    displaySavingsChart(savingsValues, daysToSave);
}

function displaySavingsChart(savingsValues, daysToSave) {
    const labels = [];
    for (let i = 0; i <= daysToSave; i += 365) {
        labels.push(`Year ${i / 365}`);
    }

    const ctx = document.getElementById('mortgageChart').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Savings over Time (£)',
                data: savingsValues.slice(0, labels.length),
                borderColor: '#FF6B01',
                backgroundColor: 'rgba(255, 107, 1, 0.2)',
                fill: true,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}