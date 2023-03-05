
# Manufacturer who makes 8 products, has access to 10 ingredients to make the products
# Manufacturer can legally only produce 1000 units a week as a production limit
# Manufacturer has 25 processes which can run cuncurrently
# Product 1: provides $30 profit per unit, requires ingredient[1,4,6,7]
# Product 1: mix ratio [15%, 25%, 40%, 20%]
# Product 2: provides $35 profit per unit, requires ingredient[1,2,3,4,5,6,7,8]
# Product 2: mix ratio [12.5%, 12.5%, 12.5%, 12.5%, 12.5%, 12.5%, 12.5%, 12.5%]
# Product 3: provides $40 profit per unit, requires ingredient[3,4,5,9,10]
# Product 3: mix ratio [20%, 20%, 20%, 20%, 20%]
# Product 4: provides $25 profit per unit, requires ingredient[7,8,10]
# Product 4: mix ratio [25%, 15%, 60%]
# Product 5: provides $55 profit per unit, requires ingredient[3,4,7,8,9,10]
# Product 5: mix ratio [1%, 17%, 22%, 16%, 25%, 19%]
# Product 6: provides $25 profit per unit, requires ingredient[2,6,7,8,9]
# Product 6: mix ratio [10%, 20%, 5%, 10%, 55%]
# Product 7: provides $50 profit per unit, requires ingredient[2,3,5,6,7]
# Product 7: mix ratio [14%, 16%, 22.5%, 33.5%, 14%]
# Product 8: provides $35 profit per unit, requires ingredient[1,2,3,6,7,8,9,10]
# Product 8: mix ratio [10%, 10%, 15%, 25%, 10%, 10%, 10%, 10%]
# Ingredient source-ability in units per week is listed below in the code



import pulp
import numpy as np


# Define the problem, name the output, declare if it is a min/max problem
problem = pulp.LpProblem("LP_Manufacturing_Max", pulp.LpMaximize)

# Define decision variables
# Because we can not make half of something, I went ahead and bound the category to integer for each of the Products.
# Leaving time as continuous due to the fact that time is not bound to being a hard integer, rather it is a float.
x1 = pulp.LpVariable('product1', lowBound=0, upBound=1000, cat='Integer')
x2 = pulp.LpVariable('product2', lowBound=0, upBound=1000, cat='Integer')
x3 = pulp.LpVariable('product3', lowBound=0, upBound=1000, cat='Integer')
x4 = pulp.LpVariable('product4', lowBound=0, upBound=1000, cat='Integer')
x5 = pulp.LpVariable('product5', lowBound=0, upBound=1000, cat='Integer')
x6 = pulp.LpVariable('product6', lowBound=0, upBound=1000, cat='Integer')
x7 = pulp.LpVariable('product7', lowBound=0, upBound=1000, cat='Integer')
x8 = pulp.LpVariable('product8', lowBound=0, upBound=1000, cat='Integer')
t = pulp.LpVariable('total_time', lowBound=0, cat='Continuous')

# Define the objective function
# Note that the numbers represent the profit gained in relation to each of the 8 Products
problem += pulp.lpSum([30*x1, 35*x2, 40*x3, 25*x4, 55*x5, 25*x6, 50*x7, 35*x8])

# Define the coefficients of the constraints
A = np.array([
    [0.15, 0.125, 0, 0, 0, 0, 0, 0.10],  # Product requirements for ingredient 1
    [0, 0.125, 0, 0, 0, 0.10, 0.14, 0.10],  # Product requirements for ingredient 2
    [0, 0.125, 0.20, 0, 0.01, 0, 0.16, 0.15],  # Product requirements for ingredient 3
    [0.25, 0.125, 0.20, 0, 0.17, 0, 0, 0],  # Product requirements for ingredient 4
    [0, 0.125, 0.20, 0, 0, 0, 0.225, 0],  # Product requirements for ingredient 5
    [0.40, 0.125, 0, 0, 0, 0.20, 0.335, 0.25],  # Product requirements for ingredient 6
    [0.20, 0.125, 0, 0.25, 0.22, 0.05, 0.14, 0.10],  # Product requirements for ingredient 7
    [0, 0.125, 0, 0.15, 0.16, 0.10, 0, 0.10],  # Product requirements for ingredient 8
    [0, 0, 0.20, 0, 0.25, 0.55, 0, 0.10],  # Product requirements for ingredient 9
    [0, 0, 0.20, 0.60, 0.19, 0, 0, 0.10],  # Product requirements for ingredient 10
    [3, 5, 5, 5, 8, 4, 8, 5]])  # Time requirements of each product to transform from raw material to finished good

# Define the Right-Hand Side of the constraints
b = np.array([500,  # Ingredient 1 accessible/available in units per week
              800,  # Ingredient 2 accessible/available in units per week
              650,  # Ingredient 3 accessible/available in units per week
              750,  # Ingredient 4 accessible/available in units per week
              400,  # Ingredient 5 accessible/available in units per week
              800,  # Ingredient 6 accessible/available in units per week
              1500,  # Ingredient 7 accessible/available in units per week
              1200,  # Ingredient 8 accessible/available in units per week
              900,  # Ingredient 9 accessible/available in units per week
              1100,  # Ingredient 10 accessible/available in units per week
              4200])  # Total hours of time in a week (168 hours per week, we have 25 process we can run concurrently)


# Define the names of the constraints
constraint_names = ["Ingredient_1",
                    "Ingredient_2",
                    "Ingredient_3",
                    "Ingredient_4",
                    "Ingredient_5",
                    "Ingredient_6",
                    "Ingredient_7",
                    "Ingredient_8",
                    "Ingredient_9",
                    "Ingredient_10",
                    "Time_Requirement"]

# Adding the constraints to the problem
for i in range(A.shape[0]):
    problem += pulp.lpDot(A[i], [x1, x2, x3, x4, x5, x6, x7, x8, t]) <= b[i], constraint_names[i]

# Add the production limit of 1000 units
problem += x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 <= 1000, "Production_Limit"


# Solve the problem
problem.solve()

# Print the results
print("Status:", pulp.LpStatus[problem.status])
print("Objective Value:", pulp.value(problem.objective))
print("Solution:")
print("x1 =", x1.varValue)
print("x2 =", x2.varValue)
print("x3 =", x3.varValue)
print("x4 =", x4.varValue)
print("x5 =", x5.varValue)
print("x6 =", x6.varValue)
print("x7 =", x7.varValue)
print("x8 =", x8.varValue)

# Printing the LHS variables
# Note constraint.sense is telling you what kind of sign the constraint has so <= is -1 for example
for name, constraint in problem.constraints.items():
    lhs_sum = 0
    for var, coef in constraint.items():
        lhs_sum += abs(coef) * var.varValue
    print(f"{name}: {lhs_sum} {constraint.sense} {constraint.constant}")
