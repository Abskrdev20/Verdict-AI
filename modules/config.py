"""Centralizes all hardcoded paths, credentials, and bulky demo text."""

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# File Paths
DATASET_PATH = "Training_Dataset/train.csv"
LOGO_PATH = "logo.png"
DEMO_IMAGE_PATH = "demo.jpg"

# Demo Mode Static Text
DEMO_STUDENT_TEXT = (
    "(Q1) A circle in the sky that goes from top to bottom.\n"
    "(Q2) The line across the middle of the sky like Earth's equator.\n"
    "(Q3) The path the Sun follows through the stars.\n"
    "(Q4) A group of stars making a shape like Orion.\n"
    "(Q5) Orion, the Big Dipper, and Scorpius.\n"
    "(Q6) Because the Earth spins and moves around the Sun.\n"
    "(Q7) The twelve constellations along the Sun's path.\n"
    "(Q8) They used stars to travel, tell stories, and make calendars.\n"
    "(Q9) We use telescopes, binoculars, and star maps.\n"
    "(Q10) City lights make it too bright to see faint stars."
)

DEMO_RUBRIC_TEXT = (
    "(Q1) A circle passing through zenith, nadir, and celestial poles.\n"
    "(Q2) Earth's equator projected onto the celestial sphere.\n"
    "(Q3) The Sun's apparent yearly path across the celestial sphere.\n"
    "(Q4) A group of stars forming a recognizable pattern, often named after myths.\n"
    "(Q5) Orion, Ursa Major, Scorpius.\n"
    "(Q6) Earth's rotation and orbit around the Sun.\n"
    "(Q7) 12 constellations along the ecliptic, used in astrology.\n"
    "(Q8) For navigation, calendars, and storytelling.\n"
    "(Q9) Telescopes, binoculars, star maps.\n"
    "(Q10) Light pollution hides faint stars."
)