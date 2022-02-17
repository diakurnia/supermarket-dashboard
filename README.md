# Supermarket Customer Behavior Dashboard

## Dashboard Link
 ** https://diakurniadewi-batch6.herokuapp.com/ **

## Objective Statement 
 - Get insight about how much customer daily spending.
 - Get insight regarding customer satisfaction level with supermarket services
 - Get insight about when customer spend most of their time to shop.
 - Get insight about what kind of payment method most customer used.

## Data Understanding
- The dataset is one of the historical sales of supermarket company which has recorded in 3 different branches for 3 months data
- Source Data: Supermarket sales Kaggle. https://www.kaggle.com/aungpyaeap/supermarket-sales
- The dataset has 17 columns and 1000 rows.
- Dataset Dictionary:
  - Invoice id: Computer generated sales slip invoice identification number
  - Branch: Branch of supercenter (3 branches are available identified by A, B and C).
  - City: Location of supercenters
  - Customer type: Type of customers, recorded by Members for customers using member card and Normal for without member card.
  - Gender: Gender type of customer
  - Product line: General item categorization groups - Electronic accessories, Fashion accessories, Food and beverages, Health and beauty, Home and lifestyle,      Sports and travel
  - Unit price: Price of each product in $
  - Quantity: Number of products purchased by customer
  - Tax: 5% tax fee for customer buying
  - Total: Total price including tax
  - Date: Date of purchase (Record available from January 2019 to March 2019)
  - Time: Purchase time (10am to 9pm)
  - Payment: Payment used by customer for purchase (3 methods are available – Cash, Credit card and Ewallet)
  - COGS: Cost of goods sold
  - Gross margin percentage: Gross margin percentage
  - Gross income: Gross income
  - Rating: Customer stratification rating on their overall shopping experience (On a scale of 1 to 10)
  
## Data preparation
 - EDA Libraries : Pandas, Numpy, Matplotlib, Seaborn.
 - Dashboard Library : Streamlit.

## Data Cleansing
 - Handling data type of columns that does not match its representation.
 - Delete a column that has the exact same value as another column.

