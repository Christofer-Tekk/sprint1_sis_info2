# CAMBIA SOLO ESTO 👇
USAR_NUBE = False   # True = nube | False = local

if USAR_NUBE:
    from conexion_nube import conectar
else:
    from conexion_local import conectar
