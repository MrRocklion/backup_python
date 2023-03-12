#script para enviar accesorios
import firebase_admin
from firebase_admin import credentials,firestore
import pandas as pd
import numpy as np
import uuid as v4

cred = credentials.Certificate("firebase/public-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


doc_ref = db.collection(u'informacion').document(u'parametros')
doc = doc_ref.get()



def enviarFirebase(ref,data):
    doc_ref = db.collection(u'accesorios').document(ref)
    doc_ref.set(data)




df = pd.read_excel("accesorios.xlsx")
accesorios = df.to_dict('records')

for acc in accesorios:
    id = str(v4.uuid4())
    acc['id'] = str(id)
    enviarFirebase(id,acc)
   