"""
Read data from Cube 'Plan_BudgetPlan' through MDX on Instance A 
then copy it to Cube 'Plan_BudgetPlan' on Instance B.

Assumption: Metadata (Cube and Dimensions) are in sync.

"""

from TM1py.Services import TM1Service

# Connection Parameters
tm1_source_parameters = {
    "address": "localhost",
    "port": "12354",
    "user": "admin",
    "password": "apple",
    "ssl": True
}
tm1_target_parameters = {
    "address": "localhost",
    "port": "9123",
    "user": "admin",
    "password": "apple",
    "ssl": True
}

# Setup Connections
tm1_source = TM1Service(**tm1_source_parameters)
tm1_target = TM1Service(**tm1_target_parameters)


# Query data from source TM1 model through MDX
mdx = "SELECT " \
      "{[plan_chart_of_accounts].[41101],[plan_chart_of_accounts].[42201]} on ROWS, " \
      "{[plan_time].[Oct-2004],[plan_time].[Nov-2004],[plan_time].[Dec-2004]} on COLUMNS  " \
      "FROM [Plan_BudgetPlan] " \
      "WHERE " \
      "([plan_version].[FY 2004 Budget],[plan_business_unit].[10110],[plan_department].[410]," \
      "[plan_exchange_rates].[local],[plan_source].[input])"
data = tm1_source.data.execute_mdx(mdx)
# Rearrange data
values = [cell['Value'] for cell in data.values()]
# Send data to target TM1 instance
tm1_target.data.write_values_through_cellset(mdx, values)

# Explicit Logout
tm1_source.logout()
tm1_target.logout()
