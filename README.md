# Function Identifier

> This is a school project made by : 
> - Fabien Charpentier
> - Sarah Chaabouni
> - Hugo Aoyagi (myself)
 
This code allows you to either add noise to values if you wish to, or identify the caracteristics of 3 type of functions:
 - Line (ax + b)
 - First order transfer function
 - Second order transfer function (only with swings)
 
## Example

 ![results menu](https://github.com/Hugo-AOYAGI/function-identifier/blob/master/assets/example.png?raw=true)

## How it works

The algorithm calculates all the partial derivatives of the cost function to find (through Newton's Method) the best modification of the function's parameters.

Once the parameters have stabilized, you can display the equation either in latex or in python.

