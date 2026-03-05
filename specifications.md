# Specifications: Telugu AI Storyteller

## Overview
The Telugu AI Storyteller is a tool designed to convert Telugu folklore into high-quality audio using the Sarvam AI Text-to-Speech (TTS) API.

## Core Features
- **Text-to-Speech Conversion:** Convert Telugu text into natural-sounding audio.
- **Voice Selection:** Support for multiple voice types (e.g., Vini - Female, Arvind - Male).
- **Audio Output:** Generate audio files in WAV format.

## Technical Requirements
- **Language:** Python
- **API:** Sarvam AI TTS API
- **Dependencies:** `requests` library

## Data Requirements
- **Input:** Telugu folklore stories in text format.
- **Authentication:** API Key for Sarvam AI.

## Workflow
1. Input Telugu text into the system.
2. Select desired voice (Male/Female).
3. Send request to Sarvam AI TTS API.
4. Save the returned audio stream as a WAV file.
