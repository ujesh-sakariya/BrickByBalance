//import { interestRate, indexFund, interestRateAndISA, indexFundAndISA, getSavingsValues } from "predictor.js"

const millisecondsInDay = 1000 * 60 * 60 * 24;
const bankOfEnglandRate = 1.05
const SNPGrowthRate = 1.1

function getDays(startDate, endDate)
{
    startDate = new Date(startDate);
    endDate = new Date(endDate);
    milliDiff = endDate - startDate;
    return (milliDiff / millisecondsInDay);
}


function simpleTimeToSave(daysToSave, value, savings){
    if(savings > value){
        return 0;
    }
    else{
        return (value - savings) / daysToSave;
    }
}

function resultOfSavings(savings, savePerMonth,interestRate, daysToSave){
    
    defaultAmount = savings * (interestRate ** (daysToSave / 365))
    fromAdditionlSaving = savePerMonth * (Math.floor(daysToSave / 30))
    return defaultAmount + fromAdditionlSaving

}

function compoundTimeToSave(savings, savePerMonth, interestRate, value)
{
    predictedSavingAmount = 0
    plannedDays = 0
    while(predictedSavingAmount < value && plannedDays < 365*100){
        predictedSavingAmount = resultOfSavings(savings, savePerMonth, interestRate, plannedDays)
        plannedDays += 1
    }
    if(plannedDays >= 365 * 100){
        return false
    }
    else{
        return plannedDays
    }

}


function resultOfSavingsComplex(savings, savePerMonth,interestRate, daysToSave){
    dailyInterest = interestRate ** (1 / 365);
    defaultAmount = savings * (dailyInterest ** daysToSave);
    fromAdditionlSaving = 0;

    numberOfAdditionalSavings = Math.floor(daysToSave / 30);
    if(numberOfAdditionalSavings >= 1){
        for (let i = 1; i <= numberOfAdditionalSavings; i++) {
            fromAdditionlSaving += savePerMonth * (dailyInterest ** (daysToSave - i * 30));
        }
    }
    return(defaultAmount + fromAdditionlSaving);

}

function complexAmountPerMonthToSave(savings, interestRate, value, daysToSave){
    predictedSavingAmount = 0
    plannedSavingPerMonth = 0
    while(value > predictedSavingAmount && plannedSavingPerMonth < 1E7){
        plannedSavingPerMonth += 10
        predictedSavingAmount = resultOfSavingsComplex(savings, plannedSavingPerMonth, interestRate, daysToSave)
    }
    if(plannedSavingPerMonth >= 1E7){
        return false
    }
    else{
        return plannedSavingPerMonth
    }
}

function complexTimeToSave(savings, savePerMonth, interestRate, value){
    predictedSavingAmount = 0
    plannedSavePerMonth = 0
    while(predictedSavingAmount < value && plannedDays < 365*100){
        plannedDays += 1
        predictedSavingAmount = resultOfSavingsComplex(savings, savePerMonth, interestRate, plannedDays)
    }
    if(plannedDays >= 365 * 100){
        return false
    }
    else{
        return plannedDays
    }
}

function resultOfSavingsISA(savings, savePerMonth,interestRate, daysToSave){
    dailyInterest = interestRate ** (1 / 365);
    defaultAmount = savings * (dailyInterest ** daysToSave);
    fromAdditionlSaving = 0;
    fromLifetimeISA = 0;

    numberOfAdditionalSavings = Math.floor(daysToSave / 30);
    if(numberOfAdditionalSavings >= 1){
        i = 1;
        isa_limit = 4000
        while(numberOfAdditionalSavings >= i){
            fromAdditionlSaving += savePerMonth * (dailyInterest ** (daysToSave - i * 30));
            if(savePerMonth < isa_limit){
                isa_limit -= savePerMonth
                fromLifetimeISA += savePerMonth * 0.25 * (dailyInterest ** (daysToSave - i * 30))
            }
            else{
                fromLifetimeISA += isa_limit * 0.25 * (dailyInterest ** (daysToSave - i * 30))
                isa_limit = 0;
            }
            if(i % 12 == 0){
                isa_limit = 4000
            }
            i += 1;
        }
    }
    return(defaultAmount + fromAdditionlSaving + fromLifetimeISA);
}

function ISAAmountPerMonthToSave(savings, interestRate, value, daysToSave){
    if(value >= 450000){
        return complexAmountToSave(savings, savePerMonth, interestRate, value)
    }
    predictedSavingAmount = 0
    plannedSavingPerMonth = 0
    while(value > predictedSavingAmount && plannedSavingPerMonth < 1E7){
        plannedSavingPerMonth += 10
        predictedSavingAmount = resultOfSavingsISA(savings, plannedSavingPerMonth, interestRate, daysToSave)
    }
    if(plannedSavingPerMonth >= 1E7){
        return false
    }
    else{
        return plannedSavingPerMonth
    }
}

function ISATimeToSave(savings, savePerMonth, interestRate, value)
{
    if(value >= 450000){
        return complexTimeToSave(savings, savePerMonth, interestRate, value)
    }
    predictedSavingAmount = 0
    plannedDays = 0
    while(predictedSavingAmount < value && plannedDays < 365*100){
        plannedDays += 1
        predictedSavingAmount = resultOfSavingsISA(savings, savePerMonth, interestRate, plannedDays)
    }
    if(plannedDays >= 365 * 100){
        return false
    }
    else{
        return plannedDays
    }
}

function getSavingsValues(savings, savePerMonth, interestRate, isIsa, daysToSave,){
    values = []
    for(let i = 0; i <= daysToSave; i++){
        if(isIsa){
            values.push(resultOfSavingsISA(savings, savePerMonth, interestRate, i))
        }
        else{
            values.push(resultOfSavings(savings, savePerMonth, interestRate, i))
        }
        
    }
    return values
}

function wittleTest(){
    console.log("Test")
}

function makeGraph(xAxis, yAxis){
    var ctx = document.getElementById('myChart').getContext('2d');
    var myLineChart = new Chart(ctx, {
        type: 'line',  // Type of chart
        data: {
            labels: xAxis, // X-axis labels
            datasets: [{
                label: 'My Dataset', // Label for the dataset
                data: yAxis, // Data for the Y-axis
                borderColor: 'rgba(75, 192, 192, 1)', // Line color
                backgroundColor: 'rgba(75, 192, 192, 0.2)', // Fill color under the line
                fill: true, // Fill area under the line
                tension: 0.1 // Line smoothing (optional)
            },
            {
                label: 'Dataset 2', // Label for the second dataset
                data: [], // Data for the second dataset
                borderColor: 'rgba(153, 102, 255, 1)', // Line color for dataset 2
                backgroundColor: 'rgba(153, 102, 255, 0.2)', // Fill color for dataset 2
                fill: true, // Fill area under the second line
                tension: 0.1 // Line smoothing for dataset 2
            }
        ]
            
        },
        options: {
            responsive: true, // Makes the chart responsive to screen size
            scales: {
                y: {
                    beginAtZero: true // Ensures Y-axis starts from zero
                }
            }
        }
    });

}

//This works out how many years they will need to reach their desired value given their monthly savings
function getTimeRequired(savings, isSNP, isIsa, amountPerMonth, value){
    today = new Date()
    interest = 1
    if(isSNP)
    {
        interest = SNPGrowthRate
    }
    else{
        interest = bankOfEnglandRate
    }

    amountPerMonth = 0
    if(isIsa){
        amountPerMonth = ISATimeToSave(savings, amountPerMonth, interest, value)
    }
    else{
        amountPerMonth = complexTimeToSave(savings, amountPerMonth, interest, value)
    }
    return amountPerMonth
}

//This works out how much they need to contribute per month to reach desired value in the given number of years
//value of inital savings, whether uses SNP 10% growth(if not 5% interest), whether is lifetime ISA, number of years for desired value to be reached, deposit value
function getContribution(savings, isSNP, isIsa, yearsToSave, value){
    
    today = new Date()
    interest = 1
    if(isSNP)
    {
        interest = SNPGrowthRate
    }
    else{
        interest = bankOfEnglandRate
    }

    amountPerMonth = 0
    if(isIsa){
        amountPerMonth = ISAAmountPerMonthToSave(savings, interest, value, yearsToSave * 365)
    }
    else{
        amountPerMonth = complexAmountPerMonthToSave(savings, interest, value, yearsToSave * 365)
    }
    return amountPerMonth

    values = getSavingsValues(savings, amountPerMonth, interest, isIsa, yearsToSave * 365)
    
    var futureDate =  new Date(today.getTime() + yearsToSave * 1000 * 60 * 60 * 24 * 30)
    daysArray = []

    while (today <= futureDate) {
        daysArray.push(new Date(today));  // Add the current date to the array
        today.setDate(today.getDate() + 1);  // Move to the next day
    }
    xAxis = []
    daysArray.forEach(element => {
        xAxis.push(element.getFullYear() + element.getMonth() + element.getDate())
    });
    makeGraph(xAxis, values)

}

//Returns savings value after given amount of time
function predictSavings(savings, isSNP, isIsa, amountPerMonth, yearsToSave, value){
    today = new Date()
    interest = 1
    if(isSNP)
    {
        interest = SNPGrowthRate
    }
    else{
        interest = bankOfEnglandRate
    }

    amountPerMonth = 0
    if(isIsa){
        finalSavings = resultOfSavingsISA(savings, amountPerMonth, interest, yearsToSave * 365)
    }
    else{
        finalSavings = resultOfSavingsComplex(savings, amountPerMonth, interest, yearsToSave * 365)
    }
    return finalSavings
}

/*
function interestRate(savings, savePerMonth, value){
    return complexTimeToSave(savings, savePerMonth, bankOfEnglandRate, value)
}

function indexFund(savings, savePerMonth, value){
    return complexTimeToSave(savings, savePerMonth, SNPGrowthRate, value)
}

function interestRateAndISA(savings, savePerMonth, value){
    return ISATimeToSave(savings, savePerMonth, bankOfEnglandRate, value)
}

function indexFundAndISA(savings, savePerMonth, value){
    return ISATimeToSave(savings, savePerMonth, SNPGrowthRate, value)
}

fixAndPredictSavings(1000, true, true, 1)

x = ISAAmountPerMonthToSave(1000, SNPGrowthRate, 5000, 45)
console.log(x)
console.log(resultOfSavingsISA(1000, x, SNPGrowthRate, 45))
console.log("\n")
y = complexAmountPerMonthToSave(1000, SNPGrowthRate, 5000, 45)
console.log(y)
console.log(resultOfSavingsComplex(1000, x, SNPGrowthRate, 45))
*/