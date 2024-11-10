milliseconds_in_day = 1000 * 60 * 60 * 24
bank_of_england_rate = 1.05
snp_growth_rate = 1.1

'''
def get_days(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    milli_diff = (end_date - start_date).total_seconds() * 1000
    return milli_diff / milliseconds_in_day
'''

def simple_time_to_save(days_to_save, value, savings):
    if savings > value:
        return 0
    else:
        return (value - savings) / days_to_save

def result_of_savings(savings, save_per_month, interest_rate, days_to_save):
    default_amount = savings * (interest_rate ** (days_to_save / 365))
    from_additional_saving = save_per_month * (days_to_save // 30)
    return default_amount + from_additional_saving

def compound_time_to_save(savings, save_per_month, interest_rate, value):
    predicted_saving_amount = 0
    planned_days = 0
    while predicted_saving_amount < value and planned_days < 365 * 100:
        predicted_saving_amount = result_of_savings(savings, save_per_month, interest_rate, planned_days)
        planned_days += 1
    return planned_days if planned_days < 365 * 100 else False

def result_of_savings_complex(savings, save_per_month, interest_rate, days_to_save):
    daily_interest = interest_rate ** (1 / 365)
    default_amount = savings * (daily_interest ** days_to_save)
    from_additional_saving = 0

    number_of_additional_savings = days_to_save // 30
    if number_of_additional_savings >= 1:
        for i in range(1, number_of_additional_savings + 1):
            from_additional_saving += save_per_month * (daily_interest ** (days_to_save - i * 30))
    return default_amount + from_additional_saving

def complex_amount_per_month_to_save(savings, interest_rate, value, days_to_save):
    predicted_saving_amount = 0
    planned_saving_per_month = 0
    while value > predicted_saving_amount and planned_saving_per_month < 1E7:
        planned_saving_per_month += 10
        predicted_saving_amount = result_of_savings_complex(savings, planned_saving_per_month, interest_rate, days_to_save)
    return planned_saving_per_month if planned_saving_per_month < 1E7 else False

def complex_time_to_save(savings, save_per_month, interest_rate, value):
    predicted_saving_amount = 0
    planned_days = 0
    while predicted_saving_amount < value and planned_days < 365 * 100:
        planned_days += 1
        predicted_saving_amount = result_of_savings_complex(savings, save_per_month, interest_rate, planned_days)
    return planned_days if planned_days < 365 * 100 else False

def result_of_savings_isa(savings, save_per_month, interest_rate, days_to_save):
    daily_interest = interest_rate ** (1 / 365)
    default_amount = savings * (daily_interest ** days_to_save)
    from_additional_saving = 0
    from_lifetime_isa = 0
    index_cont = 0
    isa_cont = 0
    number_of_additional_savings = days_to_save // 30
    if number_of_additional_savings >= 1:
        i = 1
        isa_limit = 4000

        while number_of_additional_savings >= i:
            from_additional_saving += save_per_month * (daily_interest ** (days_to_save - i * 30))
            if save_per_month < isa_limit:
                isa_limit -= save_per_month
                #
                isa_cont += save_per_month
                from_lifetime_isa += save_per_month * 0.25 * (daily_interest ** (days_to_save - i * 30))
            else:
                from_lifetime_isa += isa_limit * 0.25 * (daily_interest ** (days_to_save - i * 30))
                isa_cont += isa_limit
                index_cont += save_per_month - isa_limit
                isa_limit = 0
            if i % 12 == 0:
                isa_limit = 4000
            i += 1
        monthlyIndex = index_cont // number_of_additional_savings
        monthlyIsa = isa_cont // number_of_additional_savings
    return default_amount + from_additional_saving + from_lifetime_isa

def isa_amount_per_month_to_save(savings, interest_rate, value, days_to_save):
    if value >= 450000:
        return complex_amount_per_month_to_save(savings, interest_rate, value, days_to_save)
    predicted_saving_amount = 0
    planned_saving_per_month = 0
    while value > predicted_saving_amount and planned_saving_per_month < 1E7:
        planned_saving_per_month += 10
        predicted_saving_amount = result_of_savings_isa(savings, planned_saving_per_month, interest_rate, days_to_save)
    return planned_saving_per_month if planned_saving_per_month < 1E7 else False

def isa_time_to_save(savings, save_per_month, interest_rate, value):
    if value >= 450000:
        return complex_time_to_save(savings, save_per_month, interest_rate, value)
    predicted_saving_amount = 0
    planned_days = 0
    while predicted_saving_amount < value and planned_days < 365 * 100:
        planned_days += 1
        predicted_saving_amount = result_of_savings_isa(savings, save_per_month, interest_rate, planned_days)
    return planned_days if planned_days < 365 * 100 else False

def get_savings_values(savings, save_per_month, interest_rate, is_isa, days_to_save):
    values = []
    for i in range(days_to_save + 1):
        if is_isa:
            values.append(result_of_savings_isa(savings, save_per_month, interest_rate, i))
        else:
            values.append(result_of_savings(savings, save_per_month, interest_rate, i))
    return values

#gets time you need to save for
def get_time_required(savings, is_snp, is_isa, amount_per_month, value):
    interest = snp_growth_rate if is_snp else bank_of_england_rate
    days = 0

    if is_isa:
        days = isa_time_to_save(savings, amount_per_month, interest, value)
    else:
        days = complex_time_to_save(savings, amount_per_month, interest, value)
    return days

#gets amount you need to save per month
def get_contribution(savings, is_snp, is_isa, years_to_save, value):
    if(savings >= value):
        return 0
    interest = snp_growth_rate if is_snp else bank_of_england_rate

    amount_per_month = 0
    isa_amount_per_month = 0
    index_per_month = 0
    if is_isa:
        amount_per_month = isa_amount_per_month_to_save(savings, interest, value, years_to_save * 365)
    else:
        amount_per_month = complex_amount_per_month_to_save(savings, interest, value, years_to_save * 365)

    return amount_per_month, 0, 0

#predicts savings
def predict_savings(savings, is_snp, is_isa, amount_per_month, years_to_save):
    interest = snp_growth_rate if is_snp else bank_of_england_rate

    if is_isa:
        final_savings = result_of_savings_isa(savings, amount_per_month, interest, years_to_save * 365)
    else:
        final_savings = result_of_savings_complex(savings, amount_per_month, interest, years_to_save * 365)
    return final_savings
