import streamlit as st #Aviso del uso de la libreria
from groq import Groq #

#Configuracion de la ventana de la web
st.set_page_config(page_title="chat bot IA", page_icon="👾")

#Titulo a la pagina
st.title("charla de BOT IA con Streamlit")

#input
nombre = st.text_input("¿cual es tu nombre?")

#crear un boton con fucionalidad
if st.button("Saludar!") :
    #Escribimos un mensaje en pantalla 
    st.write(f"!hola {nombre} ¿en que puedo ayudarte?") 


MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

#Nos conecta con la api, creando un usuario
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"] #Obtenemos la clave de la api
    return Groq(api_key = clave_secreta) #conectamos a la api

#selecciona el modelo de la IA
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo, #Seleccion el modelo de la IA
        messages = [{"role":"user", "content" : mensajeDeEntrada }],
        stream = True #Funcionalidad para IA, reponde a tiempo real
    ) #Devuelve la respuesta a que manda la IA

#Historial de mensaje
def inicializar_estado():
    #si no existe "mensajes" entonces creamos un historial
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [] #Historial vacio

def configurar_pagina():
    st.title("chat bot IA") #Titulo
    st.sidebar.title("Ajustes")#Titulo
    opcion = st.sidebar.selectbox(
        "Elegi modelo", #titulo
        options = MODELOS, #opciones deben estar en una lista
        index = 1 #valorPorDefecto
    )
    return opcion #!agregamos esto para obtener el orden del modelo

def actualizar_historial(rol, contenido, avatar):
    #F1 metodo append(dato) Agrega datos a la lista
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar": avatar}
    )

def mostrar_historial(): #Guarda la estructura visual del mensaje
    for mensaje in st.session_state.mensajes: 
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]) :
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height= 400, border= True)
    with contenedorDelChat : mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = "" #variable vacia
    for frase in chat_completo:
        if frase.choices[0].delta.content: #Evitamos el dato NONE
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content

    return respuesta_completa           


#? INVOCACION DE FUNCIONES
modelo = configurar_pagina() #Agarramos el modelo seleccionado
clienteUsuario = crear_usuario_groq() #conecta con la API GROQ
inicializar_estado() #Se crea en memoria el historial vacio
area_chat() #Se crea el contenedor de los mensajes
mensaje = st.chat_input("Escribi un mensaje...")
#Verificar que la variable mensaje tenga contenido
if mensaje:
    actualizar_historial("user", mensaje, "🤖") #Mostramos el mensaje en el chat
    chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje) #Obtenemos la respuesta de la IA
    if chat_completo: #verificamos que la variable tenga algo
        with st.chat_message("assistant") :
            respuesta_completa =st.write_stream(generar_respuesta(chat_completo))
            actualizar_historial("assistant", respuesta_completa, "🤖")
            st.rerun() #Actualizar
