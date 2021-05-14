import pandas as pd

def discount_per_qnty(qnty, price):
    """
    esta función se encarga de ajustar el precio de venta por unidad vendida
    dependiendo de la cantidad de unidades compradas y la media de lo que 
    se suele comprar
    """
    mean = int(qnty.mean())
    result_price = []
    
    for indiv_qnty, indiv_price in zip(list(qnty), list(price)):

        if (indiv_qnty < mean/2):
            indiv_price += 200      #aumenta 200 pesos

        elif ((indiv_qnty > mean/2) and (indiv_qnty < mean)):
            indiv_price += 100      #aumenta 100 pesos

        else:
            indiv_price -= 100      #hace un descuento de 100 pesos

        result_price.append(indiv_price)

    return result_price

def recalculate_tot_income(qnty, price):
    """
    esta función se encarga de recalcular el ingreso total por transacción
    ya que con la función de arriba 'discount_per_qnty' se está alterando 
    el precio de venta, y esos cambios deben reflejarse
    """

    result_income = []

    for indiv_qnty, indiv_price in zip(list(qnty), list(price)):
        result_income.append( indiv_qnty * indiv_price )

    return result_income

#lectura del csv e impresión inicial
sales1 = pd.read_csv("./sales.csv")
print(sales1[:6])

#recalcula los precios y sobreescribe sales
new_prices = discount_per_qnty(sales1["quantity"], sales1["price_per_unit"])
sales1["price_per_unit"] = new_prices

#actualiza total_income
new_tot_income = recalculate_tot_income(sales1["quantity"], sales1["price_per_unit"])
sales1["total_income"] = new_tot_income

#borra columnas
sales1.drop(['quantity'], axis = 1, inplace = True)
sales1.drop(['unit_gr'], axis = 1, inplace = True)
sales1.drop(['price_per_unit'], axis = 1, inplace = True)

#renombra una columna
sales1.rename(columns = {'total_gr':'quantity'}, inplace = True)

#añade una columna de unidades de medida
#todas las mediciones se hicieron bajo la unidad de medida
#con código 2
sales1['id_unit_measurement_eqv'] = [2] * len(sales1)

sales1 = sales1[['id', 'date', 'quantity', 'total_income', 'id_crop', 'id_unit_measurement_eqv']]

print(sales1[:6])

#guarda el dataframe como csv
sales1.to_csv("sales_updated.csv", index=False)

