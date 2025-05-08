# 🤖 Groq Assistant — Texte, Audio, Traduction & Traitement Intelligent

Groq Assistant est une interface web interactive développée avec **Streamlit** qui exploite les **API Groq** pour fournir des services d'IA de nouvelle génération : **génération de texte**, **transcription audio**, **traduction multilingue** et **chaînes de traitements intelligents**.

Ce projet illustre comment intégrer des modèles LLM avancés et des modèles de transcription dans des applications concrètes et modulables.

---

## 🚀 Fonctionnalités

### 📝 Génération de texte
Générez du contenu structuré, des idées créatives, des réponses techniques ou du résumé automatique grâce à des modèles LLM comme `llama-3.3-70b-versatile`.

- Prise en charge de prompt système et utilisateur
- Personnalisation de la température et du nombre de tokens
- Interface visuelle pour l'itération rapide

---

### 🎙️ Transcription audio
Utilisez l’API Whisper via Groq pour convertir des fichiers audio en texte de manière rapide et fiable.

- Prend en charge les formats mp3, mp4, wav, etc.
- Plusieurs modèles de transcription disponibles (standard, turbo, distillé)
- Prétraitement intelligent via fichiers temporaires

---

### 🔄 Traduction multilingue
Traduisez automatiquement des contenus dans une dizaine de langues avec conservation du format et des nuances.

- Traduction contextualisée (modèle guidé par prompt système)
- Basée sur LLM pour un rendu qualitatif
- Intégration fluide avec les autres modules (ex: texte ou transcription)

---

### 📊 Chaîne de traitements combinés
Créez des pipelines personnalisés combinant les modules ci-dessus :

- Texte ou audio en entrée
- Enchaînement de transcription, traduction, résumé
- Résultat unique, centralisé, affiché dans l’interface

---

## 🧠 Technologies & Stack

| Composant         | Description                               |
|------------------|-------------------------------------------|
| **Python**       | Langage principal                         |
| **Streamlit**    | Framework UI léger et rapide              |
| **API Groq**     | Accès aux modèles LLM et transcription    |
| **LLM Groq**     | `llama-3.3-70b-versatile`, `gemma2`, etc. |
| **Whisper**      | Transcription audio de haute qualité      |
| **CSS custom**   | Personnalisation de l'apparence Streamlit |

---

## 🧪 Exécution locale

### 1. Cloner le dépôt
```bash
git clone https://github.com/yannthur/groq-chatbot
cd groq-chatbot
```
### 2. Installer les dependances
```bash
pip install -r requirements.txt
```
### 3. Ajouter votre clé API Groq
* Soit en définissant une variable d’environnement :
```bash
export groq_api_key=VOTRE_CLÉ_API
```
* Soit via l’interface Streamlit (dans la sidebar)

### 4. Lancer l’application
```bash
streamlit run app.py
```


