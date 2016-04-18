from carbone.func import *
product = get_product_infos(7291647867788)
distance = get_distance_infos(product)
print distance

print 'composition :'+str(get_ingredients_list(product))
