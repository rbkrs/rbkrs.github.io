# History Learner 📚

Een Streamlit-applicatie voor het leren van geschiedenis examens met automatische flashcard generatie, tijdlijn visualisatie en spaced repetition.

## Functies

- **Tekst Analyse**: Automatische extractie van kernbegrippen, jaartallen en namen
- **Flashcards**: Automatisch gegenereerde vraag-antwoord kaarten
- **Tijdlijn**: Chronologische visualisatie van gebeurtenissen
- **Open Vragen**: Generatie van oefenvragen over oorzaken en gevolgen
- **Spaced Repetition**: Slim herhalingssysteem voor optimaal leren

## Installatie

1. Clone deze repository:
```bash
git clone <repository-url>
cd history-learner
```

2. Installeer de dependencies:
```bash
pip install -r requirements.txt
```

3. Start de applicatie:
```bash
streamlit run history_learner.py
```

## Gebruik

1. **Tekst Invoer**: Plak je studiemateriaal in het tekstvak of upload een bestand
2. **Analyse**: Klik op "Analyseer Tekst" om de informatie te extraheren
3. **Oefenen**: Gebruik de verschillende pagina's om te oefenen met flashcards, tijdlijn en open vragen
4. **Herhaling**: Gebruik het spaced repetition systeem voor optimale herhalingen

## Deployment op GitHub Pages

Voor deployment op GitHub Pages met Streamlit Cloud:

1. Push dit project naar een GitHub repository
2. Ga naar [share.streamlit.io](https://share.streamlit.io)
3. Verbind je GitHub account en selecteer deze repository
4. Kies `history_learner.py` als main file
5. De app wordt automatisch gedeployed

## AI Integratie (Optioneel)

De code bevat placeholders voor AI API integratie om betere flashcards en vragen te genereren:

- `history_learner.py:165` - FlashcardGenerator.generate_from_text()
- `history_learner.py:233` - QuestionGenerator.generate_open_questions()

Voeg hier je OpenAI of Claude API calls toe voor geavanceerdere vraag generatie.

## Technische Details

- **Framework**: Streamlit
- **Dependencies**: Alleen Python standaard libraries + Streamlit
- **Tekstanalyse**: Regex-based extractie van jaartallen, namen en begrippen
- **Herhalingssysteem**: Basis spaced repetition algoritme

## Structuur

```
history-learner/
├── history_learner.py      # Hoofdapplicatie
├── requirements.txt        # Dependencies
└── README.md              # Deze file
```

## Licentie

Open source - gebruik naar believen voor educatieve doeleinden.