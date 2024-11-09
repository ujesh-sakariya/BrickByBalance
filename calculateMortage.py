from flask import Flask, render_template, request, jsonify
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Route for the Mortgage Calculator page
@app.route("/mortgage_calculator")
def mortgage_calculator():
    return render_template("mortgage_calculator.html")

# Route to calculate mortgage
@app.route("/calculate_mortgage", methods=["POST"])
def calculate_mortgage():
    # Get values from the form
    loan_amount = float(request.form.get("loanAmount"))
    down_payment = float(request.form.get("downPayment"))
    loan_term_years = int(request.form.get("loanTerm"))
    annual_interest_rate = float(request.form.get("interestRate")) / 100

    # Calculate the loan principal (loan amount minus down payment)
    principal = loan_amount - down_payment
    
    # Monthly interest rate
    monthly_interest_rate = annual_interest_rate / 12
    
    # Number of monthly payments
    num_payments = loan_term_years * 12
    
    # Mortgage calculation formula for monthly payments
    monthly_payment = (principal * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments)
    
    # Calculate total interest paid over the term of the loan
    total_interest = monthly_payment * num_payments - principal
    
    # Return the results as JSON
    result = {
        "monthlyPayment": round(monthly_payment, 2),
        "totalInterest": round(total_interest, 2)
    }
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
