def kpts_coord(kpt, w_image, h_image):
    x = kpt[0][0][0]
    y = kpt[0][0][1]

    x_prop = x / w_image
    y_prop = y / h_image
    
    return x_prop, y_prop

def class_coord(kpt, w_image, h_image):
    x_ini = kpt[0][0]
    y_ini = kpt[0][1]
    x_end = kpt[1][0]
    y_end = kpt[1][1]

    if (x_ini > x_end):
        temp = x_ini
        x_ini = x_end
        x_end = temp

    if(y_ini > y_end):                  
        temp = y_ini
        y_ini = y_end
        y_end = temp

    w = max(x_ini,x_end) - min(x_ini,x_end)
    h = max(y_ini,y_end) - min(y_ini,y_end)

    x_mid = x_ini+(w/2)
    y_mid = y_ini+(h/2)

    x_prop = x_mid / w_image
    y_prop = y_mid / h_image
    w_prop = w / w_image
    h_prop = h / h_image

    return x_prop, y_prop, w_prop, h_prop 