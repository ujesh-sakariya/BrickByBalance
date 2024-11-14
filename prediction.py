def get_contribution(savings,years_to_save, deposit, value):
    '''
    Calculates the optimal split of monthly savings between a Lifetime ISA (LISA) and an S&P 500 investment 
    to achieve a target house deposit within a specified time frame.

    Parameters:
    - Savings (float): Current savings already accumulated towards the goal.
    - years_to_save (int): Number of years planned for saving to reach the target.
    - deposit (float): Target deposit amount needed for the house purchase.
    - value (float): Total estimated purchase price of the house.

    Returns:
    - lisa_monthly (int): Recommended monthly contribution to the Lifetime ISA, factoring in the £4,000 annual limit.
    - SP_monthly (int): Recommended monthly investment in an S&P 500 fund to meet the remainder of the goal, 
    based on a projected annual return rate.
    '''
    savings = float(savings)
    deposit -= savings
    years_to_save = float(years_to_save) 
    value = float(value) 

    if(savings >= value):
        return 0, 0, 0
    
    if value > 450000:
        lisa_montly,sp_montly = calculate_mixed_strategy_savings(deposit_goal=deposit,
                                                            lisa_limit=0,annual_return=10,
                                                            years=years_to_save)
    else:
        lisa_montly,sp_montly = calculate_mixed_strategy_savings(deposit_goal=deposit,
                                                            lisa_limit=4000,annual_return=10,
                                                            years=years_to_save)
        
    return lisa_montly/12, sp_montly

def calculate_mixed_strategy_savings(deposit_goal, annual_return, years, lisa_limit=4000, lisa_bonus=0.25):
    # Monthly return for additional investment
    monthly_return = annual_return / 12 / 100
    # Total months in the saving period
    total_months = years * 12
    
    # Calculate total LISA savings and bonus over the years
    lisa_contribution = min(lisa_limit, deposit_goal / years)  
    lisa_total = (lisa_contribution * years) * (1 + lisa_bonus)  
    
    # Remaining deposit goal after LISA contributions
    remaining_goal = deposit_goal - lisa_total
    if remaining_goal <= 0:
        return lisa_contribution, 0
    
    # Monthly contribution for the remaining goal in S&P 500
    monthly_savings_s_and_p = (remaining_goal * monthly_return) / ((1 + monthly_return) ** total_months - 1)
    
    return lisa_contribution, monthly_savings_s_and_p

if __name__ == '__main__':
    years = 14
    house_price = 350000
    deposit = 35000
    print(get_contribution(savings=8000,years_to_save=years,deposit=deposit,
                           value=house_price))
