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

function complexTimeToSave(savings, savePerMonth, interestRate, value)
{
    predictedSavingAmount = 0
    plannedDays = 0
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
            i += 1;
            if(savePerMonth > isa_limit){
                isa_limit -= savePerMonth
                fromLifetimeISA += savePerMonth * 0.25 * (dailyInterest ** (daysToSave - i * 30))
            }
            else{
                fromLifetimeISA += savePerMonth * 0.25 * (dailyInterest ** (daysToSave - i * 30))
                isa_limit = 0;
            }
            if(i % 12 == 0){
                isa_limit = 4000
            }
        }
    }
    return(defaultAmount + fromAdditionlSaving + fromLifetimeISA);
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


a = new Date('2022-01-01');
b = new Date('2022-02-01');
x = getDays(a, b);
y = simpleTimeToSave(5, 100, 50);
console.log(x);
console.log(y);
console.log(resultOfSavingsComplex(1000, 200, 1.05, 75))
console.log("\n")
x = complexTimeToSave(1000, 200, 1.05, 1411.68)
console.log(x)
console.log(resultOfSavingsComplex(1000, 200, 1.05, x))
console.log("\nLifetime")
console.log(resultOfSavingsComplex(1000, 200, 1.05, 365 * 2))
x = ISATimeToSave(1000, 200, 1.05, 5000)
console.log(x)
console.log(resultOfSavingsISA(1000, 200, 1.05, x))
console.log(resultOfSavingsISA(1000, 200, 1.05, x - 1))
console.log(getSavingsValues(1000, 200, 1.05, true, 100))

