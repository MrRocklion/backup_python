import firebase_admin
from firebase_admin import credentials,firestore
import pandas as pd
import numpy as np
import uuid




cred = credentials.Certificate("firebase/public-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()




accesorios = [{}]
departamentos = [{}]
propietarios = [{}]
responsables = [{}]
tipo_equipos = [{}]
ubicaciones = [{}]
equipos = [{}]
data_informacion = {}

doc_ref = db.collection(u'informacion').document(u'parametros')
doc = doc_ref.get()
if doc.exists:
    data = doc.to_dict()
    departamentos = data['departamentos']
    propietarios = data['propietarios']
    responsables = data['responsables']
    tipo_equipos = data['tequipo']
    ubicaciones = data['ubicaciones']
    equipos_db = data['equipos']
else:
    print(u'No such document!')



#traemos los accesorios
accesorios_db = db.collection(u'accesorios').stream()
accesorios = []
for acc in accesorios_db:
    accesorios.append(acc.to_dict())

def enviarFirebase(ref,data):
    doc_ref = db.collection(u'pruebas').document(ref)
    doc_ref.set(data)

def obtenerAccesorios(codigo):
    aux_accesorios = []
    for acc in accesorios:
        if acc['codigo_equipo'] == codigo:
            aux_accesorios.append(acc)
    return aux_accesorios

def obtenerDepartamento(codigo):
    for depa in departamentos:
        if depa['codigo'] == codigo:
                return depa
    return {}
def obtenerEquipo(codigo):
    for equip in equipos_db:
        if equip['codigo']== codigo:
                return equip
    return {}
def obtenerPropietario(codigo):
    for prop in propietarios:
        if prop['codigo']== codigo:
                return prop
    return {}
        
def obtenerResponsable(codigo):
    for respo in responsables:
        if respo['codigo']== codigo:
                return respo
def obtenerTipoEquipo(codigo):
    for tequi in tipo_equipos:
        if tequi['codigo']== codigo:
                return tequi
    return {}
def obtenerUbicaciones(codigo):
    for ubi in ubicaciones:
        if ubi['codigo']== codigo:
                return ubi
    return {}

df = pd.read_excel("equipos.xlsx")
equipos = df.to_dict('records')
print(df)
for equipo in equipos:
    codigo = equipo['codigo'].split('-')

    for clave in equipo:
        dato = equipo[clave]
        if pd.isna(equipo[clave]):
            equipo[clave] = ''
    equipo['accesorios'] = obtenerAccesorios(equipo['codigo'])
    equipo['codigos_historial'] = [equipo['codigo']]
    equipo['equipo'] = obtenerEquipo(int(codigo[4]))
    equipo['img'] = "sin dato"
    equipo['mantenimientos'] = []
    equipo['ubicacion'] = obtenerUbicaciones(int(codigo[0]))
    equipo['departamento'] = obtenerDepartamento(int(codigo[1]))
    equipo['responsable'] = obtenerResponsable(int(codigo[2]))
    equipo['tipo_equipo'] = obtenerTipoEquipo(int(codigo[3]))
    equipo['reubicado'] = False
    
    print(codigo)
    print("Enviar-->",equipo)
    enviarFirebase(equipo['id'],equipo)

    print('\n')


