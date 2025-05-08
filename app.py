import os
import streamlit as st
import requests
import tempfile

# Configuration de la page
st.set_page_config(
    page_title="Groq Assistant - Texte, Audio, Traduction",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #4285F4;
        text-align: center;
    }
    .task-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .task-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #4285F4;
    }
    .output-container {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #e0e0e0;
        margin-top: 15px;
    }
    .output-header {
        font-weight: bold;
        margin-bottom: 10px;
        color: #333;
    }
    .info-box {
        background-color: #e7f3fe;
        border-left: 6px solid #2196F3;
        padding: 10px;
        margin: 10px 0;
    }
    .progress-indicator {
        display: flex;
        align-items: center;
        margin: 10px 0;
    }
    .progress-indicator span {
        height: 8px;
        width: 8px;
        margin: 0 2px;
        background-color: #4285F4;
        border-radius: 50%;
        display: inline-block;
        animation: bounce 1.5s infinite ease-in-out;
    }
    .progress-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }
    .progress-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }
    @keyframes bounce {
        0% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0); }
    }
    .api-key-input {
        margin-bottom: 15px;
    }
    .stButton>button {
        background-color: #4285F4;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5em 1em;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #356ac3;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .chain-container {
        background-color: #f0f8ff;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        border: 1px dashed #4285F4;
    }
    .model-description {
        font-size: 0.8rem;
        color: #666;
        font-style: italic;
    }
    .footer {
        text-align: center;
        margin-top: 30px;
        color: #666;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Fonctions d'API Groq
def get_groq_api_key():
    """Récupère la clé API Groq depuis les variables d'environnement ou la session"""
    # Essayer d'abord la variable d'environnement
    env_api_key = os.environ.get('groq_api_key')
    if env_api_key:
        return env_api_key
    
    # Sinon, utiliser la clé stockée en session
    if 'GROQ_API_KEY' in st.session_state:
        return st.session_state['GROQ_API_KEY']
    
    return None

def set_groq_api_key(api_key):
    """Enregistre la clé API Groq dans la session"""
    st.session_state['GROQ_API_KEY'] = api_key

def text_generation(prompt, model="llama-3.3-70b-versatile", temperature=0.7, max_tokens=1000, system_prompt=None):
    """Génère du texte avec l'API Groq"""
    api_key = get_groq_api_key()
    if not api_key:
        st.error("Clé API Groq non configurée")
        return None
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            st.error(f"Erreur API: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API: {str(e)}")
        return None

def speech_to_text(audio_file, model="whisper-large-v3"):
    """Convertit l'audio en texte avec l'API Groq"""
    api_key = get_groq_api_key()
    if not api_key:
        st.error("Clé API Groq non configurée")
        return None
    
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        files = {"file": audio_file}
        data = {"model": model}
        
        response = requests.post(url, headers=headers, files=files, data=data)
        if response.status_code == 200:
            return response.json()["text"]
        else:
            st.error(f"Erreur API: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API: {str(e)}")
        return None

def translate_text(text, source_lang, target_lang, model="llama-3.3-70b-versatile"):
    """Traduit le texte avec l'API Groq"""
    system_prompt = "Vous êtes un traducteur professionnel."
    user_prompt = f"""Traduisez le texte suivant de {source_lang} vers {target_lang}.
Texte à traduire: {text}
Conservez le format du texte original et toutes les nuances de sens. Fournissez uniquement la traduction sans commentaires supplémentaires."""
    
    translation = text_generation(user_prompt, model=model, system_prompt=system_prompt)
    return translation

def summarize_text(text, length="medium", language="Français", model="llama-3.3-70b-versatile"):
    """Résume le texte avec l'API Groq dans la langue spécifiée"""
    length_map = {
        "court": "très concis (environ 10% du texte original)",
        "medium": "longueur moyenne (environ 25% du texte original)",
        "long": "détaillé mais condensé (environ 40% du texte original)"
    }
    
    system_prompt = f"Vous êtes un expert en résumé de texte. Répondez en {language}."
    user_prompt = f"""Résumez le texte suivant avec un résumé {length_map[length]}.
Texte à résumer: {text}
Conservez les points clés, les idées principales et les informations essentielles. Le résumé doit être cohérent et fluide.
IMPORTANT: Votre résumé doit être en {language}."""
    
    summary = text_generation(user_prompt, model=model, system_prompt=system_prompt)
    return summary

# Interface utilisateur
def main():
    st.markdown("<h1 class='main-title'>Groq Assistant</h1>", unsafe_allow_html=True)
    
    # Barre latérale pour la configuration
    with st.sidebar:
        st.subheader("Configuration")
        
        # Vérifier si la clé est déjà disponible dans l'environnement
        env_api_key = os.environ.get('groq_api_key')
        if env_api_key:
            st.success("✅ Clé API Groq détectée dans l'environnement")
            api_key = env_api_key
            set_groq_api_key(env_api_key)  # Stocker aussi en session
        else:
            # Input API Key manuellement
            api_key = st.text_input("Clé API Groq", type="password", key="api_key_input", 
                                   help="Entrez votre clé API Groq", value=get_groq_api_key() or "")
            if st.button("Enregistrer la clé API"):
                if api_key:
                    set_groq_api_key(api_key)
                    st.success("Clé API enregistrée avec succès")
                else:
                    st.error("Veuillez entrer une clé API valide")
        
        st.divider()
        
        # Sélection du modèle
        model_descriptions = {
            "llama-3.3-70b-versatile": "🧠 Polyvalent et puissant (128K)",
            "llama-3.1-8b-instant": "🚀 Rapide et économique (128K)",
            "gemma2-9b-it": "📝 Efficace et compact (8K)",
            "whisper-large-v3": "🎙️ Transcription audio standard",
            "whisper-large-v3-turbo": "🎙️ Transcription audio rapide",
            "distil-whisper-large-v3-en": "🎙️ Transcription audio (anglais)"
        }
        
        text_model = st.selectbox(
            "Modèle pour le traitement de texte",
            options=["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it"],
            format_func=lambda x: f"{x} - {model_descriptions[x].split(' (')[0]}"
        )
        st.markdown(f"<div class='model-description'>{model_descriptions[text_model]}</div>", unsafe_allow_html=True)
        
        audio_model = st.selectbox(
            "Modèle pour la transcription audio",
            options=["whisper-large-v3", "whisper-large-v3-turbo", "distil-whisper-large-v3-en"],
            format_func=lambda x: f"{x} - {model_descriptions[x].split(' (')[0]}"
        )
        st.markdown(f"<div class='model-description'>{model_descriptions[audio_model]}</div>", unsafe_allow_html=True)
        
        st.divider()
        
        # Paramètres avancés
        with st.expander("Paramètres avancés", expanded=True):
            temperature = st.slider("Température", 0.0, 1.0, 0.7, 0.1,
                                   help="Valeur plus basse = réponses plus prévisibles, valeur plus haute = réponses plus créatives")
            max_tokens = st.slider("Longueur maximale", 100, 4000, 1000, 100,
                                  help="Nombre maximum de tokens à générer")
    
    # Création des onglets pour les différentes fonctionnalités
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Génération de texte", "🎙️ Transcription audio", "🔄 Traduction", "📊 Chaîne de traitements"])
    
    # Onglet 1: Génération de texte
    with tab1:
        st.markdown("<h2 class='task-title'>Génération de texte</h2>", unsafe_allow_html=True)
        
        prompt = st.text_area("Entrez votre prompt", height=150,
                             placeholder="Entrez votre question ou demande ici...")
        
        system_prompt = st.text_area("Message système (optionnel)", height=100,
                                    placeholder="Instructions de contexte pour l'IA (ex: 'Vous êtes un expert en marketing...')")
        
        if st.button("Générer", key="generate_button"):
            if not get_groq_api_key():
                st.error("Veuillez configurer votre clé API Groq dans la barre latérale")
            elif not prompt:
                st.error("Veuillez entrer un prompt")
            else:
                with st.spinner("Génération en cours..."):
                    result = text_generation(prompt, model=text_model, temperature=temperature, 
                                            max_tokens=max_tokens, system_prompt=system_prompt if system_prompt else None)
                    if result:
                        st.markdown("<div class='output-container'>", unsafe_allow_html=True)
                        st.markdown("<div class='output-header'>Réponse:</div>", unsafe_allow_html=True)
                        st.write(result)
                        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Onglet 2: Transcription audio
    with tab2:
        st.markdown("<h2 class='task-title'>Transcription audio</h2>", unsafe_allow_html=True)
        
        st.markdown("<div class='info-box'>Formats acceptés: mp3, mp4, mpeg, mpga, m4a, wav, webm (taille max: 25 MB)</div>", unsafe_allow_html=True)
        
        audio_file = st.file_uploader("Télécharger un fichier audio", type=["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"])
        
        col1, col2 = st.columns(2)
        with col1:
            transcribe_button = st.button("Transcrire", key="transcribe_button", disabled=audio_file is None)
        with col2:
            if st.button("Réinitialiser", key="reset_audio", disabled=audio_file is None):
                st.session_state.pop("transcription_result", None)
                st.rerun()
        
        if transcribe_button and audio_file:
            if not get_groq_api_key():
                st.error("Veuillez configurer votre clé API Groq dans la barre latérale")
            else:
                with st.spinner("Transcription en cours..."):
                    # Créer un fichier temporaire pour éviter les problèmes de flux
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_file.name.split('.')[-1]}") as tmp:
                        tmp.write(audio_file.getvalue())
                        tmp_path = tmp.name
                    
                    # Ouvrir le fichier pour l'API
                    with open(tmp_path, "rb") as audio:
                        result = speech_to_text(audio, model=audio_model)
                    
                    # Nettoyer le fichier temporaire
                    os.unlink(tmp_path)
                    
                    if result:
                        st.session_state["transcription_result"] = result
        
        # Afficher le résultat de la transcription
        if "transcription_result" in st.session_state and st.session_state["transcription_result"]:
            st.markdown("<div class='output-container'>", unsafe_allow_html=True)
            st.markdown("<div class='output-header'>Transcription:</div>", unsafe_allow_html=True)
            st.write(st.session_state["transcription_result"])
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Onglet 3: Traduction
    with tab3:
        st.markdown("<h2 class='task-title'>Traduction</h2>", unsafe_allow_html=True)
        
        languages = ["Français", "Anglais", "Espagnol", "Allemand", "Italien", "Portugais", "Russe", "Chinois", "Japonais", "Arabe"]
        
        col1, col2 = st.columns(2)
        with col1:
            source_lang = st.selectbox("Langue source", languages, index=1)
        with col2:
            target_lang = st.selectbox("Langue cible", languages, index=0)
        
        text_to_translate = st.text_area("Texte à traduire", height=150, 
                                       placeholder="Entrez le texte à traduire...")
        
        # Option pour utiliser le résultat de la transcription
        if "transcription_result" in st.session_state and st.session_state["transcription_result"]:
            if st.checkbox("Utiliser le texte transcrit", key="use_transcription"):
                text_to_translate = st.session_state["transcription_result"]
                st.info("Utilisation du texte transcrit")
        
        if st.button("Traduire", key="translate_button"):
            if not get_groq_api_key():
                st.error("Veuillez configurer votre clé API Groq dans la barre latérale")
            elif not text_to_translate:
                st.error("Veuillez entrer un texte à traduire")
            else:
                with st.spinner("Traduction en cours..."):
                    result = translate_text(text_to_translate, source_lang, target_lang, model=text_model)
                    if result:
                        st.session_state["translation_result"] = result
                        st.markdown("<div class='output-container'>", unsafe_allow_html=True)
                        st.markdown("<div class='output-header'>Traduction:</div>", unsafe_allow_html=True)
                        st.write(result)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Onglet 4: Chaîne de traitements
    with tab4:
        st.markdown("<h2 class='task-title'>Chaîne de traitements</h2>", unsafe_allow_html=True)
        
        st.markdown("Combinez plusieurs opérations en une seule chaîne de traitements.")
        
        # Étape 1: Source
        st.subheader("Étape 1: Source")
        source_type = st.radio("Choisissez la source", ["Texte", "Audio"], horizontal=True)
        
        if source_type == "Texte":
            chain_text = st.text_area("Entrez votre texte", height=150,
                                     placeholder="Entrez votre texte ici...")
        else:  # Audio
            chain_audio = st.file_uploader("Télécharger un fichier audio pour la chaîne", 
                                         type=["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"])
        
        # Étape 2: Opérations
        st.subheader("Étape 2: Opérations")
        
        operations = []
        if st.checkbox("Transcription audio", disabled=source_type != "Audio"):
            operations.append("transcription")
        
        if st.checkbox("Traduction"):
            operations.append("traduction")
            chain_source_lang = st.selectbox("Langue source (traduction)", languages, index=1, key="chain_source_lang")
            chain_target_lang = st.selectbox("Langue cible (traduction)", languages, index=0, key="chain_target_lang")
        
        if st.checkbox("Résumé"):
            operations.append("résumé")
            chain_summary_length = st.select_slider("Longueur du résumé", 
                                                  options=["court", "medium", "long"], 
                                                  value="medium")
            chain_summary_lang = st.selectbox("Langue du résumé", languages, index=0, key="chain_summary_lang")
        
        # Étape 3: Exécution
        st.subheader("Étape 3: Exécution")
        
        if st.button("Exécuter la chaîne", key="execute_chain"):
            if not get_groq_api_key():
                st.error("Veuillez configurer votre clé API Groq dans la barre latérale")
            elif (source_type == "Texte" and not chain_text) or (source_type == "Audio" and not chain_audio):
                st.error("Veuillez fournir une source (texte ou audio)")
            elif not operations:
                st.error("Veuillez sélectionner au moins une opération")
            else:
                # Créer un conteneur pour afficher les résultats intermédiaires
                results_container = st.container()
                
                # Dictionnaire pour stocker les résultats intermédiaires
                intermediate_results = {}
                current_text = None
                
                # Partie 1: Obtenir le texte initial
                with st.spinner("Traitement en cours..."):
                    if source_type == "Audio":
                        # Créer un fichier temporaire pour éviter les problèmes de flux
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{chain_audio.name.split('.')[-1]}") as tmp:
                            tmp.write(chain_audio.getvalue())
                            tmp_path = tmp.name
                        
                        # Ouvrir le fichier pour l'API
                        with open(tmp_path, "rb") as audio:
                            current_text = speech_to_text(audio, model=audio_model)
                        
                        # Nettoyer le fichier temporaire
                        os.unlink(tmp_path)
                        
                        intermediate_results["transcription"] = current_text
                        st.success("✅ Transcription terminée")
                    else:
                        current_text = chain_text
                        intermediate_results["texte_source"] = current_text
                    
                    # Partie 2: Appliquer les opérations
                    if "traduction" in operations and current_text:
                        current_text = translate_text(current_text, chain_source_lang, chain_target_lang, model=text_model)
                        intermediate_results["traduction"] = current_text
                        st.success("✅ Traduction terminée")
                    
                    if "résumé" in operations and current_text:
                        current_text = summarize_text(current_text, chain_summary_length, chain_summary_lang, model=text_model)
                        intermediate_results["résumé"] = current_text
                        st.success("✅ Résumé terminé")
                    
                    final_result = current_text
                
                # Afficher tous les résultats intermédiaires
                with results_container:
                    st.markdown("<h3>Résultats par étape</h3>", unsafe_allow_html=True)
                    
                    for step, result in intermediate_results.items():
                        with st.expander(f"Résultat de l'étape: {step.capitalize()}", expanded=True):
                            st.write(result)

                    
                    st.markdown("<h3>Résultat final</h3>", unsafe_allow_html=True)
                    st.write(final_result)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Pied de page
    st.markdown("<div class='footer'>Créé avec Streamlit & l'API Groq</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()