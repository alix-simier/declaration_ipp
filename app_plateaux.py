import streamlit as st
import io
from construction import declarations_ipp

st.title("Déclaration IPP")

if "declaration_file" not in st.session_state:
    st.session_state.declaration_file = None

plateaux = st.file_uploader("Télécharger l'export des plateaux à déclarer", type="xlsx")
destinataires = st.file_uploader("Télécharger l'export des références destinataires", type="xlsx")

if st.button("Lancer le traitement"):
    if not plateaux or not destinataires:
        st.error("Merci d'importer les deux fichiers avant de lancer le traitement.")
    else:
        try:
            # Générer le DataFrame
            declaration = declarations_ipp(plateaux, destinataires)

            # Créer un buffer pour le fichier Excel
            buffer_declaration = io.BytesIO()
            declaration.to_excel(buffer_declaration, index=False)
            buffer_declaration.seek(0)  # Revenir au début du buffer

            st.session_state.declaration_file = buffer_declaration

            st.success("La déclaration IPP a été générée avec succès.")

        except Exception as e:
            st.error(f"Une erreur a eu lieu : {e}")

# Bouton de téléchargement
if st.session_state.declaration_file:
    st.download_button(
        label="Télécharger la déclaration IPP",
        data=st.session_state.declaration_file,
        file_name="declaration_ipp.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
