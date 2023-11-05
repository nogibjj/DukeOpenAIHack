# NBA Live Commentary Generator with GPT-4.0


## Table of Contents
- [Demo](https://youtu.be/ZzF3iewrsoo)
- [Technical Overview](#technical-overview)
  - [API Integration](#api-integration)
  - [Data Management](#data-management)
  - [Audio Integration](#audio-integration)
  - [User Interface](#user-interface)
- [Accessibility and Inclusion](#accessibility-and-inclusion)
- [Future Enhancements](#future-enhancements)
- [Conclusion](#conclusion)

## Technical Overview
The NBA Live Commentary Generator is an innovative project that combines real-time data, advanced language generation, and API integration to offer dynamic commentary during NBA games. Here's a deep dive into the technical aspects of this groundbreaking solution:

### API Integration
- **NBA Stats API:** We leverage the NBA Stats API to access live play-by-play data, player statistics, and season/career insights. This API forms the backbone of our data-driven commentary, enabling us to provide up-to-the-minute analysis and real-time insights about players.

- **SportRadar API:** Complementing the NBA Stats API, the SportRadar API furnishes additional sports-related data, including player biographies, team information, and historical statistics. This enriches our commentary, offering a comprehensive view of the game and the players involved.

### Data Management
- **Faiss Vector Database:** To manage context effectively, we use Faiss, a powerful vector database. Faiss helps us store and retrieve context information efficiently, ensuring our commentary remains relevant and insightful as the game unfolds.

- **Langchain:** Langchain technology is integrated into our project to persist contextual data and chain together current and past events' context to enhance the responses.

### Audio Integration
- **Google Cloud API:** We utilize the Google Cloud speech-to-text service to convert the generated commentary into real-time audio, enhancing the fan experience by providing both text and speech commentary simultaneously.

### User Interface
- **Streamlit:** Streamlit serves as the foundation of our user-friendly interface, displaying real-time commentary, statistics, and insights. This intuitive interface allows fans to engage with our commentary seamlessly.

## Accessibility and Inclusion
Our project isn't just about technology; it's about accessibility and financial inclusion:

- **Accessibility for Fans with Disabilities:** Our real-time commentary makes NBA games more accessible to visually impaired fans by providing detailed play-by-play, statistics, and text-to-speech functionality for an immersive experience.

- **Bridging the Financial Gap:** We offer subsidized and flexible payment structures, making NBA games accessible to fans who can't afford subscriptions or in-person attendance.

## Future Enhancements
Our commitment to innovation drives us to explore future enhancements:

- **Multilingual Support:** We plan to expand commentary to support multiple languages to reach a broader audience.

- **User Preferences:** Allowing users to customize the commentary, such as choosing their favorite team or player to focus on, tailoring their experience.

- **Predictive Analysis:** Implementing more advanced algorithms to provide predictions and game insights based on historical data and current game dynamics.

- **Integration with Smart Devices:** Developing applications for smart speakers and other voice-controlled devices to provide a hands-free experience for users.

- **Real-time Visualizations:** Incorporating real-time graphs and visualizations to supplement the commentary.

## For Developers

To run

```pip install -r requirements.txt```

Start the Text to Speech service

```
cd src
python tts.py
```

Run Streamlit App

```
cd ..
streamlit run web_app.py
```

Run commentary generation

```
#check for API keys and all configuration for APIs
cd src
python generator.py
```

## Conclusion
The NBA Live Commentary Generator is a groundbreaking project that enhances the fan experience with real-time, dynamic commentary. With robust API integration, advanced data management, audio integration, and a user-friendly interface, we offer a comprehensive solution. Accessibility and future enhancements are integral to our mission, making sports commentary more inclusive and dynamic. Join us in this exciting journey of transforming sports commentary with our NBA Live Commentary Generator powered by GPT-4.0!

