#Invoices App Recognizer. D&C Solutions.
#Dev by Lic. Humberto Peña
#V1.1

import streamlit as st
from PIL import Image
from invoicesapp_b import *
from datetime import datetime

def timetoName(name):
    return '{}{}.csv'.format(name, datetime.now().strftime("%Y.%m.%d-%H.%M"))

def convert_df(df):
    return df.to_csv().encode('utf-8')

if __name__ == "__main__":
    st.set_page_config('Invoice Recognizer')
    image = Image.open('../images/logo.png')

    general_df =  outGen_df = None
    items_df = outIt_df = None
    e = None
    flag = None
    with st.sidebar:
        st.image(image)
        uploaded_files = st.file_uploader(label="", accept_multiple_files=True)

        if st.button('Iniciar'):
                id = 0
                try:
                    for uploaded_file in uploaded_files:
                        bytes_data = uploaded_file.read()
                        try:
                            flag = 'Processing'
                            (id, outGen_df, outIt_df) = analyze_invoice(bytes_data, id)
                        except:
                            flag = 'Exception'
                            pass
                        if flag == 'Processing':
                            try:
                                if general_df is None:
                                    general_df = outGen_df.copy()
                                else:
                                    general_df = pd.concat([general_df, outGen_df]).copy()

                                if items_df is None:
                                    items_df = outIt_df.copy()
                                else:
                                    items_df = pd.concat([items_df, outIt_df]).copy()
                                flag = 'Done'
                            except:
                                flag = 'Exception'
                                pass
                except:
                    flag = 'Exception'
                    pass
                    
    st.header('Reconocimiento de Facturas')
    if flag is None:
        st.subheader("Instrucciones de uso:")
        st.markdown('1. Dar click en el botón del lado izquierdo **Subir archivo**.')
        st.markdown('2. Subir la factura en alguno de los siguientes formatos **JPEG, PNG, PDF, TIFF, BMP**.')
        st.markdown('3. Dar click en el botón del lado izquierdo **Iniciar**.')
        st.markdown('4. Se mostrará en una tabla debajo con los datos de la factura, que se podrá descargar en formato excel.')
        st.info('**Comienza un reconocimiento...**')

    if flag == 'Done':
        general_df = general_df.dropna(axis=1, how='all').fillna(value='-').applymap(lambda x: str(x) if not isinstance(x, str) else x)
        items_df= items_df.dropna(axis=1, how='all').fillna(value='-').applymap(lambda x: str(x) if not isinstance(x, str) else x)
        all_rows = pd.merge(general_df, items_df, how='inner', left_on='invoice_number', right_on='invoice_number')

        with st.container():
            st.success('Proceso terminado.')
            st.markdown('Antes de descargar el archivo, asegurate de haber terminado de observar los datos, porque se borrarán. Selecciona la casilla para que el botón de descarga aparezca.')
            col1, col2, col3 = st.columns(3)
            with col2:
                with st.expander('Descargar datos.'):
                    st.download_button(
                    label="🔽 Descargar Datos",
                    data=convert_df(all_rows),
                    file_name= timetoName('Factura'),
                    mime='text/csv',
                    key='downloadAll')
            with st.expander('Ver datos', expanded=True):
                st.dataframe(all_rows)
            with st.expander('Ver datos de facturación'):
                st.dataframe(general_df)
            with st.expander('Ver datos de items'):
                st.dataframe(items_df)
            
    if flag == 'Processing':
        st.spinner('Proceso en ejecución')

    if flag == 'Exception':
        st.exception(e)
        st.error('Existe un error en el procesamiento de los datos.')