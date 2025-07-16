"""
History Learner - Een Streamlit applicatie voor het leren van geschiedenis
==========================================================================

Deze applicatie helpt bij het leren voor geschiedenis examens door:
- Tekst analyse voor kernbegrippen, jaartallen en namen
- Automatische flashcard generatie
- Tijdlijn visualisatie
- Open vragen generatie
- Spaced repetition voor herhaling

Dependencies: streamlit, datetime, re, random, collections
"""

import streamlit as st
import re
import datetime
import random
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional
import json

# Configuratie
st.set_page_config(
    page_title="History Learner",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state initialisatie
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = []
if 'current_card' not in st.session_state:
    st.session_state.current_card = 0
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'key_terms' not in st.session_state:
    st.session_state.key_terms = []
if 'timeline_events' not in st.session_state:
    st.session_state.timeline_events = []
if 'open_questions' not in st.session_state:
    st.session_state.open_questions = []
if 'spaced_repetition' not in st.session_state:
    st.session_state.spaced_repetition = {}

class TextAnalyzer:
    """Klasse voor het analyseren van tekst en extracteren van belangrijke informatie."""
    
    @staticmethod
    def extract_years(text: str) -> List[Tuple[int, str]]:
        """
        Extraheert jaartallen uit tekst met context.
        
        Args:
            text: De te analyseren tekst
            
        Returns:
            List van tuples (jaar, context)
        """
        years = []
        # Patroon voor jaren (1000-2099)
        year_pattern = r'\b(1[0-9]{3}|20[0-9]{2})\b'
        
        sentences = text.split('.')
        for sentence in sentences:
            matches = re.findall(year_pattern, sentence)
            for year in matches:
                years.append((int(year), sentence.strip()))
        
        return sorted(set(years))
    
    @staticmethod
    def extract_names(text: str) -> List[str]:
        """
        Extraheert namen uit tekst (hoofdletters gevolgd door kleine letters).
        
        Args:
            text: De te analyseren tekst
            
        Returns:
            List van unieke namen
        """
        # Patroon voor namen (hoofdletter gevolgd door kleine letters)
        name_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        names = re.findall(name_pattern, text)
        
        # Filter veelvoorkomende woorden uit
        common_words = {'De', 'Het', 'Een', 'In', 'Op', 'Van', 'Voor', 'Na', 'Door', 'Tijdens', 'Onder'}
        names = [name for name in names if name not in common_words]
        
        return list(set(names))
    
    @staticmethod
    def extract_key_terms(text: str) -> List[str]:
        """
        Extraheert kernbegrippen uit tekst.
        
        Args:
            text: De te analyseren tekst
            
        Returns:
            List van kernbegrippen
        """
        # Woorden die vaak voorkomen in geschiedenis
        history_keywords = [
            'oorlog', 'revolutie', 'koning', 'keizer', 'republiek', 'democratie',
            'fascisme', 'socialisme', 'kapitalisme', 'kolonialisme', 'imperialisme',
            'renaissance', 'reformatie', 'verlichting', 'industrialisatie',
            'verdrag', 'grondwet', 'parlement', 'regering', 'politiek'
        ]
        
        words = re.findall(r'\b\w+\b', text.lower())
        word_counts = Counter(words)
        
        # Vind veelvoorkomende woorden en geschiedenis-gerelateerde termen
        key_terms = []
        for word, count in word_counts.most_common(20):
            if len(word) > 3 and count > 1:
                key_terms.append(word)
        
        # Voeg geschiedenis-specifieke termen toe
        for word in history_keywords:
            if word in text.lower():
                key_terms.append(word)
        
        return list(set(key_terms))

class FlashcardGenerator:
    """Klasse voor het genereren van flashcards."""
    
    @staticmethod
    def generate_from_text(text: str, years: List[Tuple[int, str]], names: List[str], key_terms: List[str]) -> List[Dict]:
        """
        Genereert flashcards op basis van geanalyseerde tekst.
        
        Args:
            text: Originele tekst
            years: Lijst van jaren met context
            names: Lijst van namen
            key_terms: Lijst van kernbegrippen
            
        Returns:
            List van flashcard dictionaries
        """
        flashcards = []
        
        # Jaar-gebaseerde flashcards
        for year, context in years:
            flashcards.append({
                'question': f"Wat gebeurde er in {year}?",
                'answer': context,
                'type': 'year',
                'difficulty': 1
            })
        
        # Namen-gebaseerde flashcards
        for name in names:
            # Zoek context rondom de naam
            sentences = text.split('.')
            context = ""
            for sentence in sentences:
                if name in sentence:
                    context = sentence.strip()
                    break
            
            flashcards.append({
                'question': f"Wie was {name}?",
                'answer': context if context else f"{name} wordt genoemd in de tekst.",
                'type': 'person',
                'difficulty': 2
            })
        
        # Begrippen-gebaseerde flashcards
        for term in key_terms[:10]:  # Limiteer tot top 10
            flashcards.append({
                'question': f"Wat betekent '{term}' in deze context?",
                'answer': f"'{term}' is een belangrijk begrip in de tekst.",
                'type': 'concept',
                'difficulty': 3
            })
        
        # TODO: Hier zou je een AI API kunnen aanroepen voor betere flashcards
        # bijvoorbeeld: improved_flashcards = call_ai_api(text, flashcards)
        
        return flashcards

class TimelineGenerator:
    """Klasse voor het genereren van tijdlijnen."""
    
    @staticmethod
    def create_timeline(years: List[Tuple[int, str]]) -> List[Dict]:
        """
        Maakt een tijdlijn van gebeurtenissen.
        
        Args:
            years: Lijst van jaren met context
            
        Returns:
            List van tijdlijn events
        """
        timeline = []
        for year, context in sorted(years):
            timeline.append({
                'year': year,
                'event': context,
                'description': f"Gebeurtenis in {year}"
            })
        
        return timeline

class QuestionGenerator:
    """Klasse voor het genereren van open vragen."""
    
    @staticmethod
    def generate_open_questions(text: str, key_terms: List[str], years: List[Tuple[int, str]]) -> List[str]:
        """
        Genereert open vragen over oorzaken, gevolgen en samenhang.
        
        Args:
            text: Originele tekst
            key_terms: Lijst van kernbegrippen
            years: Lijst van jaren met context
            
        Returns:
            List van open vragen
        """
        questions = []
        
        # Oorzaak-gevolg vragen
        questions.extend([
            "Wat waren de belangrijkste oorzaken van de beschreven gebeurtenissen?",
            "Welke gevolgen hadden deze gebeurtenissen voor de samenleving?",
            "Hoe hingen de verschillende gebeurtenissen met elkaar samen?"
        ])
        
        # Jaar-specifieke vragen
        if years:
            earliest_year = min(years, key=lambda x: x[0])[0]
            latest_year = max(years, key=lambda x: x[0])[0]
            questions.append(f"Beschrijf de ontwikkelingen tussen {earliest_year} en {latest_year}.")
        
        # Begrip-specifieke vragen
        for term in key_terms[:3]:
            questions.append(f"Leg uit hoe '{term}' een rol speelde in deze periode.")
        
        # TODO: Hier zou je een AI API kunnen aanroepen voor betere vragen
        # bijvoorbeeld: improved_questions = call_ai_api_for_questions(text, questions)
        
        return questions

class SpacedRepetition:
    """Basis implementatie van spaced repetition systeem."""
    
    @staticmethod
    def calculate_next_review(difficulty: int, performance: int) -> int:
        """
        Berekent het aantal dagen tot de volgende herhaling.
        
        Args:
            difficulty: Moeilijkheidsgraad van de kaart (1-5)
            performance: Prestatie van de gebruiker (1-5)
            
        Returns:
            Aantal dagen tot volgende herhaling
        """
        base_interval = {1: 1, 2: 3, 3: 7, 4: 14, 5: 30}
        multiplier = performance / 3.0
        
        return int(base_interval.get(difficulty, 7) * multiplier)

def main():
    """Hoofdfunctie van de applicatie."""
    
    st.title("📚 History Learner")
    st.markdown("*Een tool voor het leren van geschiedenis examens*")
    
    # Sidebar voor navigatie
    st.sidebar.title("Navigatie")
    page = st.sidebar.radio("Kies een pagina:", [
        "📝 Tekst Invoer",
        "🎯 Kernbegrippen",
        "📚 Flashcards",
        "📅 Tijdlijn",
        "❓ Open Vragen",
        "🔄 Herhaling"
    ])
    
    if page == "📝 Tekst Invoer":
        show_text_input()
    elif page == "🎯 Kernbegrippen":
        show_key_terms()
    elif page == "📚 Flashcards":
        show_flashcards()
    elif page == "📅 Tijdlijn":
        show_timeline()
    elif page == "❓ Open Vragen":
        show_open_questions()
    elif page == "🔄 Herhaling":
        show_spaced_repetition()

def show_text_input():
    """Toont de tekst invoer pagina."""
    st.header("📝 Tekst Invoer")
    
    # Tabs voor verschillende invoer methodes
    tab1, tab2 = st.tabs(["Tekst Invoeren", "Bestand Uploaden"])
    
    with tab1:
        st.subheader("Voer je tekst in")
        text_input = st.text_area(
            "Plak hier je samenvatting of tekst uit het geschiedenisboek:",
            height=300,
            help="Voer de tekst in die je wilt analyseren voor het maken van flashcards en vragen."
        )
        
        if st.button("Analyseer Tekst", type="primary"):
            if text_input:
                analyze_text(text_input)
            else:
                st.warning("Voer eerst tekst in om te analyseren.")
    
    with tab2:
        st.subheader("Upload een tekstbestand")
        uploaded_file = st.file_uploader(
            "Kies een tekstbestand",
            type=['txt', 'md'],
            help="Upload een .txt of .md bestand met je studiemateriaal."
        )
        
        if uploaded_file is not None:
            text_content = uploaded_file.read().decode('utf-8')
            st.text_area("Inhoud van het bestand:", text_content, height=200)
            
            if st.button("Analyseer Geupload Bestand", type="primary"):
                analyze_text(text_content)

def analyze_text(text: str):
    """Analyseert de ingevoerde tekst en slaat resultaten op."""
    with st.spinner("Tekst analyseren..."):
        analyzer = TextAnalyzer()
        
        # Extracteer informatie
        years = analyzer.extract_years(text)
        names = analyzer.extract_names(text)
        key_terms = analyzer.extract_key_terms(text)
        
        # Genereer flashcards
        flashcard_gen = FlashcardGenerator()
        flashcards = flashcard_gen.generate_from_text(text, years, names, key_terms)
        
        # Genereer tijdlijn
        timeline_gen = TimelineGenerator()
        timeline = timeline_gen.create_timeline(years)
        
        # Genereer open vragen
        question_gen = QuestionGenerator()
        open_questions = question_gen.generate_open_questions(text, key_terms, years)
        
        # Sla resultaten op in session state
        st.session_state.key_terms = key_terms
        st.session_state.flashcards = flashcards
        st.session_state.timeline_events = timeline
        st.session_state.open_questions = open_questions
        
        # Toon resultaten
        st.success(f"Analyse voltooid! Gevonden: {len(key_terms)} kernbegrippen, {len(years)} jaartallen, {len(names)} namen.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Flashcards", len(flashcards))
        with col2:
            st.metric("Tijdlijn Events", len(timeline))
        with col3:
            st.metric("Open Vragen", len(open_questions))

def show_key_terms():
    """Toont de kernbegrippen pagina."""
    st.header("🎯 Kernbegrippen")
    
    if not st.session_state.key_terms:
        st.info("Eerst tekst analyseren om kernbegrippen te zien.")
        return
    
    st.subheader("Gevonden Kernbegrippen")
    
    # Toon kernbegrippen in kolommen
    cols = st.columns(3)
    for i, term in enumerate(st.session_state.key_terms):
        with cols[i % 3]:
            st.write(f"• {term}")

def show_flashcards():
    """Toont de flashcards oefenpagina."""
    st.header("📚 Flashcards")
    
    if not st.session_state.flashcards:
        st.info("Eerst tekst analyseren om flashcards te genereren.")
        return
    
    total_cards = len(st.session_state.flashcards)
    current_idx = st.session_state.current_card
    
    if current_idx >= total_cards:
        st.session_state.current_card = 0
        current_idx = 0
    
    # Progress bar
    progress = (current_idx + 1) / total_cards
    st.progress(progress)
    st.write(f"Kaart {current_idx + 1} van {total_cards}")
    
    # Huidige flashcard
    card = st.session_state.flashcards[current_idx]
    
    # Vraag tonen
    st.subheader("Vraag:")
    st.write(card['question'])
    
    # Antwoord tonen/verbergen
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Toon Antwoord"):
            st.session_state.show_answer = True
    
    with col2:
        if st.button("Verberg Antwoord"):
            st.session_state.show_answer = False
    
    if st.session_state.show_answer:
        st.subheader("Antwoord:")
        st.write(card['answer'])
        
        # Prestatie feedback
        st.subheader("Hoe goed kende je dit?")
        performance_cols = st.columns(5)
        
        for i, label in enumerate(["Slecht", "Matig", "Redelijk", "Goed", "Perfect"], 1):
            with performance_cols[i-1]:
                if st.button(label):
                    record_performance(current_idx, i)
                    next_card()
    
    # Navigatie
    st.subheader("Navigatie")
    nav_cols = st.columns(3)
    
    with nav_cols[0]:
        if st.button("⬅️ Vorige"):
            previous_card()
    
    with nav_cols[1]:
        if st.button("🔄 Shuffle"):
            random.shuffle(st.session_state.flashcards)
            st.session_state.current_card = 0
            st.session_state.show_answer = False
    
    with nav_cols[2]:
        if st.button("➡️ Volgende"):
            next_card()

def next_card():
    """Gaat naar de volgende flashcard."""
    st.session_state.current_card = (st.session_state.current_card + 1) % len(st.session_state.flashcards)
    st.session_state.show_answer = False

def previous_card():
    """Gaat naar de vorige flashcard."""
    st.session_state.current_card = (st.session_state.current_card - 1) % len(st.session_state.flashcards)
    st.session_state.show_answer = False

def record_performance(card_idx: int, performance: int):
    """Registreert prestatie voor spaced repetition."""
    card_id = f"card_{card_idx}"
    
    if card_id not in st.session_state.spaced_repetition:
        st.session_state.spaced_repetition[card_id] = []
    
    st.session_state.spaced_repetition[card_id].append({
        'date': datetime.datetime.now().isoformat(),
        'performance': performance
    })

def show_timeline():
    """Toont de tijdlijn pagina."""
    st.header("📅 Tijdlijn")
    
    if not st.session_state.timeline_events:
        st.info("Eerst tekst analyseren om tijdlijn te genereren.")
        return
    
    st.subheader("Chronologische Tijdlijn")
    
    for event in st.session_state.timeline_events:
        with st.expander(f"📅 {event['year']}"):
            st.write(event['event'])

def show_open_questions():
    """Toont de open vragen pagina."""
    st.header("❓ Open Vragen")
    
    if not st.session_state.open_questions:
        st.info("Eerst tekst analyseren om open vragen te genereren.")
        return
    
    st.subheader("Oefenvragen")
    st.write("Gebruik deze vragen om je kennis te testen:")
    
    for i, question in enumerate(st.session_state.open_questions, 1):
        st.write(f"{i}. {question}")
        
        # Ruimte voor antwoord
        answer_key = f"answer_{i}"
        st.text_area(f"Jouw antwoord op vraag {i}:", key=answer_key, height=100)

def show_spaced_repetition():
    """Toont de spaced repetition pagina."""
    st.header("🔄 Herhaling")
    
    if not st.session_state.spaced_repetition:
        st.info("Eerst flashcards oefenen om herhalingen te zien.")
        return
    
    st.subheader("Herhalings Statistieken")
    
    # Toon statistieken
    total_reviews = sum(len(reviews) for reviews in st.session_state.spaced_repetition.values())
    st.metric("Totaal aantal herhalingen", total_reviews)
    
    # Toon kaarten die herhaling nodig hebben
    st.subheader("Kaarten voor Herhaling")
    
    spaced_rep = SpacedRepetition()
    cards_for_review = []
    
    for card_id, reviews in st.session_state.spaced_repetition.items():
        if reviews:
            last_review = reviews[-1]
            performance = last_review['performance']
            difficulty = 2  # Default difficulty
            
            days_since = (datetime.datetime.now() - datetime.datetime.fromisoformat(last_review['date'])).days
            next_review_days = spaced_rep.calculate_next_review(difficulty, performance)
            
            if days_since >= next_review_days:
                cards_for_review.append(card_id)
    
    if cards_for_review:
        st.write(f"Je hebt {len(cards_for_review)} kaarten die herhaling nodig hebben.")
        if st.button("Start Herhaling"):
            # Filter flashcards voor herhaling
            review_indices = [int(card_id.split('_')[1]) for card_id in cards_for_review]
            st.session_state.current_card = review_indices[0] if review_indices else 0
            st.session_state.show_answer = False
            st.switch_page("📚 Flashcards")
    else:
        st.success("Geen kaarten hebben op dit moment herhaling nodig!")

if __name__ == "__main__":
    main()