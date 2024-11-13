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
    years_to_save = float(years_to_save) 
    value = float(value) 

    if(savings >= value):
        return 0, 0, 0
    
    if value > 450000:
        lisa_montly,sp_montly = calculate_mixed_strategy_savings(deposit_goal=deposit,
                                                            lisa_limit=0,annual_return=5,
                                                            years=years_to_save)
    else:
        lisa_montly,sp_montly = calculate_mixed_strategy_savings(deposit_goal=deposit,
                                                            lisa_limit=4000,annual_return=5,
                                                            years=years_to_save)
        
    return lisa_montly, sp_montly