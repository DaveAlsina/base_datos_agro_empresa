-- Total de ganancias por cultivo.

select opc.crop_name, cast(sum(sls.total_income) as float) as total_income
from sales sls join crop cr on(sls.id_crop = cr.id) join optimum_condition opc on(cr.id_crop_name_optimum_condition = opc.id_crop_name)
group by opc.crop_name

-- Total en toneladas producido por cultivo

select opc.crop_name, cast(sum(sls.quantity)/1000000 as float) as total_t
from sales sls join crop cr on(sls.id_crop = cr.id) join optimum_condition opc on(cr.id_crop_name_optimum_condition = opc.id_crop_name)
group by opc.crop_name