import dearpygui.dearpygui as dpg
import random
import time
import math
from enum import Enum
#from config import ConfigManager
#from logger import LoggerManager
#from stats import StatsTracker
import os 
import json
import re
from datetime import datetime
from typing import Optional, Tuple, List
import threading
import zlib
import threading
from pathlib import Path






class Location(Enum):
    SPACE = "Space"
    MERCURY = "Mercury"
    VENUS = "Venus"
    EARTH = "Earth"
    MARS = "Mars"
    JUPITER = "Jupiter"
    SATURN = "Saturn"
    URANUS = "Uranus"
    NEPTUNE = "Neptune"
    QUANTUM_CORE = "Quantum Core"

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

ENVIRONMENTS = {
    Location.SPACE: {
        "gravity": 0,
        "features": {
            "vacuum": True,
            "radiation": 0.8,
            "description": "A vast emptiness with occasional particles"
        },
        "visible": True,
        "facts": [
            "Space is not completely empty - it contains a few hydrogen atoms per cubic meter.",
            "The temperature in space is about -270.45°C, just slightly above absolute zero.",
            "Space is completely silent because there's no medium for sound waves to travel through."
        ]
    },
    Location.MERCURY: {
        "gravity": 3.7,
        "features": {
            "atmosphere": "Thin exosphere",
            "temperature": "Extreme variations",
            "description": "Smallest planet, heavily cratered"
        },
        "visible": True,
        "facts": [
            "Mercury is the smallest planet in our solar system - only slightly larger than Earth's Moon.",
            "A day on Mercury (one full rotation) takes 59 Earth days, but a year (one orbit around the Sun) takes only 88 days!",
            "Mercury has the most extreme temperature variations in the solar system, from -173°C at night to 427°C during the day."
        ]
    },
    Location.VENUS: {
        "gravity": 8.87,
        "features": {
            "atmosphere": "Dense CO2",
            "pressure": 92,
            "description": "Hottest planet with acidic clouds"
        },
        "visible": True,
        "facts": [
            "Venus is the hottest planet in our solar system with surface temperatures hot enough to melt lead (about 465°C).",
            "A day on Venus (243 Earth days) is longer than its year (225 Earth days).",
            "Venus rotates in the opposite direction to most planets - the Sun rises in the west and sets in the east."
        ]
    },
    Location.EARTH: {
        "gravity": 9.81,
        "features": {
            "atmosphere": "Nitrogen-Oxygen",
            "pressure": 101.325,
            "description": "Familiar terrestrial environment"
        },
        "visible": True,
        "facts": [
            "Earth is the only known planet in the universe confirmed to host life.",
            "About 71% of Earth's surface is covered in water, mostly in oceans.",
            "Earth's atmosphere is 78% nitrogen, 21% oxygen, and 1% other gases - perfect for life as we know it."
        ]
    },
    Location.MARS: {
        "gravity": 3.71,
        "features": {
            "atmosphere": "Thin CO2",
            "pressure": 0.636,
            "description": "Cold desert with rust-colored surface"
        },
        "visible": True,
        "facts": [
            "Mars is home to the tallest mountain in the solar system - Olympus Mons, which is nearly three times taller than Mount Everest.",
            "Mars has the largest dust storms in the solar system, sometimes covering the entire planet for months.",
            "Evidence suggests Mars once had rivers, lakes and even an ocean, making it a prime candidate for past life."
        ]
    },
    Location.JUPITER: {
        "gravity": 24.79,
        "features": {
            "composition": "Gas giant",
            "great_red_spot": True,
            "description": "Largest planet with intense storms"
        },
        "visible": True,
        "facts": [
            "Jupiter is so massive that it has 2.5 times the mass of all other planets in the solar system combined.",
            "The Great Red Spot is a giant storm that has been raging for at least 400 years - big enough to fit three Earths inside it.",
            "Jupiter has 95 known moons - the largest number of any planet in our solar system."
        ]
    },
    Location.SATURN: {
        "gravity": 10.44,
        "features": {
            "rings": True,
            "composition": "Gas giant",
            "description": "Famous for its beautiful ring system"
        },
        "visible": True,
        "facts": [
            "Saturn's rings are made mostly of chunks of ice and small amounts of carbonaceous dust.",
            "Saturn is the least dense planet in our solar system - it would float if you could find a bathtub big enough!",
            "A day on Saturn is only about 10.7 hours - the second shortest in the solar system after Jupiter."
        ]
    },
    Location.URANUS: {
        "gravity": 8.69,
        "features": {
            "axial_tilt": 98,
            "composition": "Ice giant",
            "description": "Rotates on its side with icy atmosphere"
        },
        "visible": True,
        "facts": [
            "Uranus rotates on its side with an axial tilt of 98 degrees - it essentially rolls around the Sun on its side.",
            "Uranus is the coldest planet in the solar system with minimum atmospheric temperature of -224°C.",
            "Uranus was the first planet discovered with a telescope, by William Herschel in 1781."
        ]
    },
    Location.NEPTUNE: {
        "gravity": 11.15,
        "features": {
            "winds": "Fastest in solar system",
            "composition": "Ice giant",
            "description": "Cold blue world with violent storms"
        },
        "visible": True,
        "facts": [
            "Neptune has the strongest winds in the solar system, reaching speeds of 2,100 km/h (1,300 mph).",
            "Neptune was the first planet located through mathematical predictions rather than direct observation.",
            "Despite being farther from the Sun, Neptune's internal heat makes its temperatures similar to Uranus's."
        ]
    },
    Location.QUANTUM_CORE: {
        "gravity": 0,
        "features": {
            "quantum_fluctuations": True,
            "description": "A mysterious realm where physics behaves strangely"
        },
        "visible": False,
        "unlock_threshold": 5,
        "facts": [
            "The Quantum Core is a theoretical region where quantum effects dominate over classical physics.",
            "In the Quantum Core, particles can exist in multiple states simultaneously until observed.",
            "Reaching the Quantum Core requires mastering both classical and quantum physics concepts."
        ]
    }
}

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    VICTORY = 3
    ANSWERING_QUESTION = 4

class Electron:
    def __init__(self):
        self.name = "Quantum Electron"
        self.age = None
        self.gender = None
        self.energy = 100
        self.max_energy = 150
        self.location = Location.SPACE
        self.goal = Location.QUANTUM_CORE
        self.game_state = GameState.MENU
        self.message_log = []
        self.last_action_time = time.time()
        self.asking_intro = True
        self.pending_question = "name"
        self.difficulty = Difficulty.EASY
        self.knowledge_score = 0
        self.questions_answered = 0
        self.quantum_core_unlocked = False
        self.used_questions = set()  # Track used questions to avoid repeats
        self.add_message("Welcome to this game, you are a lone electron navigating through space-time.")
        self.add_message("Note: you are allowed to use the internet for the game-related questions")
        self.add_message("Note: as the difficulty increases, if you don't match the difficulty, the internet will be your friend")
        self.add_message("To salvage your self esteem, we all start somewhere...")
        self.add_message("And.. you can always type 'help' for navigating the UI")
        self.add_message("If you at any point close the window, the code will abort and you'll need to reboot")
        self.add_message("What's your name? (Alphabetic characters only)")
        
        # Expanded physics and math problems database with clues
        self.problems = {
            Difficulty.EASY: [
                {
                    "id": "easy1",
                    "question": "What is the value of π (pi) to two decimal places?",
                    "answer": "3.14",
                    "explanation": "π is approximately 3.14159, so rounded to two decimal places it's 3.14",
                    "clue": "Think about the ratio of a circle's circumference to its diameter."
                },
                {
                    "id": "easy2",
                    "question": "What is Newton's First Law also known as?",
                    "answer": "law of inertia",
                    "explanation": "Newton's First Law states that an object in motion stays in motion unless acted upon by an external force.",
                    "clue": "It describes an object's resistance to changes in motion."
                },
                {
                    "id": "easy3",
                    "question": "What force keeps planets in orbit around the Sun?",
                    "answer": "gravity",
                    "explanation": "Gravity is the attractive force between masses that keeps planets in orbit.",
                    "clue": "It's the same force that makes apples fall from trees."
                },
                {
                    "id": "easy4",
                    "question": "What is the speed of light in vacuum (in m/s)?",
                    "answer": "299792458",
                    "explanation": "The speed of light in vacuum is exactly 299,792,458 meters per second.",
                    "clue": {"It's approximately 300,000 km/s .",
                    "\n you can use (sqrt(permittivity_of_vacum*permeability_of_vacuum))",
                    "\nwhich is respectively 8.85418782e-12 and 4*pi*e-7 "}
                },
                {
                    "id": "easy5",
                    "question": "What element has the atomic number 1?",
                    "answer": "hydrogen",
                    "explanation": "Hydrogen is the lightest and most abundant element in the universe.",
                    "clue": "It's the primary component of stars like our Sun."
                }
            ],
            Difficulty.MEDIUM: [
                {
                    "id": "medium1",
                    "question": "What is the gravitational force (in N) on a 10kg object on Earth? (g=9.81 m/s²)",
                    "answer": "98.1",
                    "explanation": "F = m * g = 10kg * 9.81 m/s² = 98.1 N",
                    "clue": "Use the formula F = m * g where m is mass and g is gravitational acceleration."
                },
                {
                    "id": "medium2",
                    "question": "What is the kinetic energy (in J) of a 5kg object moving at 4 m/s?",
                    "answer": "40",
                    "explanation": "KE = ½mv² = 0.5 * 5kg * (4 m/s)² = 40 J",
                    "clue": "The formula is KE = ½ * mass * velocity²."
                },
                {
                    "id": "medium3",
                    "question": "What is the acceleration due to gravity on Mars (in m/s²)?",
                    "answer": "3.71",
                    "explanation": "Mars has about 38% of Earth's gravity, at 3.71 m/s².",
                    "clue": "Mars's gravity is about 0.38 times Earth's gravity (9.81 m/s²)."
                },
                {
                    "id": "medium4",
                    "question": "Calculate the energy (in J) of a photon with frequency 6e+14 Hz (h=6.63e-34 J·s)",
                    "answer": "3.978e-19",
                    "explanation": "E = hf = 6.63e-34 * 6e14 ≈ 3.978e-19 J", #-19
                    "clue": "Use Planck's equation E = h * frequency where h is Planck's constant."
                },
                {
                    "id": "medium5",
                    "question": "What is the escape velocity from Earth (in km/s)?",
                    "answer": "11.2",
                    "explanation": "Earth's escape velocity is about 11.2 km/s to overcome gravity.",
                    "clue": "It's the speed needed to break free from Earth's gravitational pull without further propulsion."
                },
                {
                    "id": "medium6",
                    "question": "How many Earth days does it take Mercury to orbit the Sun?",
                    "answer": "88",
                    "explanation": "Mercury has the shortest orbital period in our solar system at 88 Earth days.",
                    "clue": "It's less than a quarter of Earth's orbital period."
                }
            ],
            Difficulty.HARD: [
                {
                    "id": "hard1",
                    "question": "What is the Schwarzschild radius (in m) of a 10 solar mass black hole? (M_sun=2e+30 kg, G=6.67e-11 N(m/kg)², c=3e+8 m/s)",
                    "answer": "29530",
                    "explanation": "R_schwarzschild = 2GM/c² = 2*6.67e-11*10*2e30/(3e8)² ≈ 29530 meters",
                    "clue": "Use the formula R_schwarzschild = 2GM/c² where M is the mass of the black hole."
                },
                {
                    "id": "hard2",
                    "question": "What is the wavelength (in nm) of a photon with 3.3 eV energy? (h=4.14e-15 eV·s, c=3e+8 m/s)",
                    "answer": "376",
                    "explanation": "wavelength = hc/E = (4.14e-15 * 3e8)/3.3 ≈ 376 nm",
                    "clue": "Use the equation wavelength = hc/E where E is the photon energy."
                },
                {
                    "id": "hard3",
                    "question": "Calculate the orbital velocity (in km/s) of Earth around the Sun (G=6.67e-11 N(m/kg)², M_sun=2e+30 kg, r=1.5e+11 m)",
                    "answer": "29.8",
                    "explanation": "v = sqrt(GM/r) = sqrt(6.67e-11*2e30/1.5e11) ≈ 29.8 km/s",
                    "clue": "Use the formula v = sqrt(GM/r) where r is the orbital radius."
                },
                {
                    "id": "hard4",
                    "question": "What is the surface temperature (in K) of a star with peak emission at 400 nm? (b=2.9e-3 m·K)",
                    "answer": "7250",
                    "explanation": "T = b/wavelength_max = 2.9e-3/400e-9 = 7250 K",
                    "clue": "Use Wien's displacement law: T = b/wavelength_max where b is Wien's constant."
                },
                {
                    "id": "hard5",
                    "question": "Calculate the gravitational potential energy (in J) between Earth and Moon (M_earth=6e+24 kg, M_moon=7.3e+22 kg, r=3.8e+8 m, G=6.67e-11 N(m/kg)²)",
                    "answer": "-7.7e28",
                    "explanation": "U = -GM_earthM_moon/r = -6.67e-11*6e24*7.3e22/3.8e8 ≈ -7.7e+28 J",
                    "clue": "Use the formula U = -GMm/r where M and m are the masses of the two bodies."
                },
                {   "id": "hard6",
                    "question": "What is the pressure (in Pa) at Jupiter's core (R=7e+7 m, rho=1600 kg/m³, G=6.67e-11 N(m/kg)²)?",
                    "answer": "4.3e12",
                    "explanation": "P ≈ (2/3)πG(rho)²R² ≈ (2/3)*3.14*6.67e-11*(1600)²*(7e7)² ≈ 4.3e+12 Pa",
                    "clue": "Use the approximation P ≈ (2/3)πG(rho)²R² for planetary core pressure."
                },
                {
                    "id": "hard7",
                    "question": "Calculate the tidal force ratio between Jupiter and Earth (M_jupiter=1.9e+27 kg, M_earth=6e+24 kg, D_jupiter=7.8e+11 m, D_earth=1.5e+11 m)",
                    "answer": "2.4",
                    "explanation": "Ratio = (M_jupiter/M_earth)*(D_earth/D_jupiter)³ = (1.9e27/6e24)*(1.5e11/7.8e11)³ ≈ 2.4",
                    "clue": "Tidal forces depend on mass and distance: Ratio = (M1/M2)*(D2/D1)³."
                },
                {
                    "id": "hard8",
                    "question": "What is the orbital period (in years) of Neptune (a=4.5e+12 m, M_sun=2e+30 kg, G=6.67e-11 N(m/kg)²)?",
                    "answer": "165",
                    "explanation": "T = 2πsqrt(a³/GM) = 2*3.14*sqrt((4.5e12)³/(6.67e-11*2e30))/(60*60*24*365) ≈ 165 years",
                    "clue": "Use Kepler's third law: T = 2πsqrt(a³/GM) and convert seconds to years."
                },
                {
                    "id": "hard9",
                    "question": "Calculate the Roche limit (in km) for a satellite with density 3000 kg/m³ orbiting Earth (rho_earth=5500 kg/m³, R_earth=6371 km)",
                    "answer": "18000",
                    "explanation": "d = 2.44R_earth(rho_earth/rho_satellite)^(1/3) = 2.44*6371*(5500/3000)^(1/3) ≈ 18000 km",
                    "clue": "Use the formula d = 2.44R(rho_planet/rho_satellite)^(1/3)."
                }
            ]
        }
        self.current_problem = None

    def add_message(self, message):
        timestamp = time.strftime("%H:%M:%S")
        msg = f"[{timestamp}] {message}"
        self.message_log.append(msg)
        if len(self.message_log) > 100:
            self.message_log.pop(0)
    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "energy": self.energy,
            "location": self.location.name,
            "knowledge_score": self.knowledge_score,
            "questions_answered": self.questions_answered,
            "difficulty": self.difficulty.name
        }
    
    def from_dict(cls, data):
        instance = cls()
        instance.name = data.get("name")
        instance.age = data.get("age")
        instance.gender = data.get("gender")
        instance.energy = data.get("energy",100)
        instance.location = Location[data.get("location", "SPACE")]
        instance.knowledge_score = data.get("knowledge_score", 0)
        instance.questions_answered = data.get("questions_answered",0)
        instance.difficulty = Difficulty[data.get("difficulty", "EASY")]
        instance.asking_intro = False
        instance.game_state = GameState.PLAYING
        instance.add_message("Game loaded. Welcome back!")
        return instance


    def adjust_difficulty(self):
        if self.questions_answered == 0:
            return
        
        accuracy = self.knowledge_score / self.questions_answered
        if accuracy > 0.75:
            if self.difficulty != Difficulty.HARD:
                self.add_message("\nYour knowledge is impressive! Increasing difficulty.\n")
            self.difficulty = Difficulty.HARD
        elif accuracy > 0.5:
            if self.difficulty != Difficulty.MEDIUM:
                self.add_message("\nYou're doing well! Adjusting difficulty.\n")
            self.difficulty = Difficulty.MEDIUM
        else:
            if self.difficulty != Difficulty.EASY:
                self.add_message("\nLet's try some easier questions.\n")
            self.difficulty = Difficulty.EASY

    def check_quantum_core_unlock(self):
        if not self.quantum_core_unlocked and self.knowledge_score >= ENVIRONMENTS[Location.QUANTUM_CORE]["unlock_threshold"]:
            self.quantum_core_unlocked = True
            ENVIRONMENTS[Location.QUANTUM_CORE]["visible"] = True
            self.add_message("\n*** COSMIC DISCOVERY ***")
            self.add_message("Your knowledge has revealed a hidden location!")
            self.add_message("The Quantum Core is now accessible!")
            self.add_message(f"Your new goal is to reach the {self.goal.value}\n")

    def get_unused_question(self, difficulty):
        available = [q for q in self.problems[difficulty] if q["id"] not in self.used_questions]
        if not available:
            # If all questions have been used, reset the used questions
            self.add_message("You've answered all questions at this difficulty! Resetting question pool.")
            self.used_questions = set()
            available = self.problems[difficulty]
        return random.choice(available)

    def ask_physics_question(self):
        self.adjust_difficulty()
        question = self.get_unused_question(self.difficulty)
        self.current_problem = question
        self.used_questions.add(question["id"])
        self.add_message("\nPhysics Question:")
        self.add_message(self.current_problem["question"])
        self.add_message("Type your answer below and press Enter (or type 'clue' for a hint):")
        self.game_state = GameState.ANSWERING_QUESTION
        return True

    def check_physics_answer(self, answer):
        if answer.lower().strip() == "clue":
            self.add_message(f"\nClue: {self.current_problem['clue']}")
            self.add_message("Try answering the question now:")
            return False
        
        self.game_state = GameState.PLAYING
        correct_answer = self.current_problem["answer"].lower().strip()
        user_answer = answer.lower().strip()
        
        self.questions_answered += 1
        
        try:
            if correct_answer.replace('.', '', 1).isdigit():
                tolerance = 0.01 * float(correct_answer)
                if abs(float(user_answer) - float(correct_answer)) <= tolerance:
                    self.knowledge_score += 1
                    self.add_message(f"Correct! {self.current_problem['explanation']}")
                    self.check_quantum_core_unlock()
                    return True
            elif user_answer == correct_answer:
                self.knowledge_score += 1
                self.add_message(f"Correct! {self.current_problem['explanation']}")
                self.check_quantum_core_unlock()
                return True
        except ValueError:
            pass
        
        self.add_message(f"Incorrect. The correct answer is: {self.current_problem['answer']}")
        self.add_message(f"Explanation: {self.current_problem['explanation']}")
        return False

    def move(self, new_location):
        energy_cost = {
            Difficulty.EASY: 5,
            Difficulty.MEDIUM: 10,
            Difficulty.HARD: 15
        }[self.difficulty]
        
        if self.energy < energy_cost:
            self.add_message(f"Not enough energy to travel! Need {energy_cost}, have {self.energy}.")
            return False

        self.add_message(f"Traveling to {new_location.value}...")
        
        if random.random() < 0.5:
            self.add_message("\nYou encounter a cosmic physics challenge!")
            return self.ask_physics_question()
        else:
            self.energy -= energy_cost
        
        self.location = new_location

        if self.energy <= 0:
            self.game_state = GameState.GAME_OVER
            self.add_message("You've run out of energy. Game Over.")
            self.add_message("Type 'restart' to play again.")
            return False
        elif self.location == self.goal:
            self.game_state = GameState.VICTORY
            self.add_message("You've reached the Quantum Core! Victory!")
            self.add_message("Type 'restart' to play again.")
            return True
        else:
            env = ENVIRONMENTS[new_location]
            self.add_message(f"\nArrived at {new_location.value}.")
            self.add_message(f"Gravity: {env['gravity']} m/s²")
            self.add_message(f"Environment: {env['features']['description']}")
            
            # Show planet facts when arriving
            self.add_message("\nPlanet Facts:")
            for fact in env["facts"]:
                self.add_message(f"- {fact}")
                
            self.add_message(f"\nCurrent energy: {self.energy}/{self.max_energy}")
            return True

    def get_visible_locations(self):
        return [loc for loc in Location if ENVIRONMENTS[loc]["visible"]]

    def is_valid_name(self, name):
        return all(c.isalpha() or c.isspace() for c in name) and name.strip() != ""
    
    def is_valid_age(self, age_str):
        try:
            age = int(age_str)
            return age > 0
        except ValueError:
            return False
    
    def is_valid_gender(self, gender):
        return gender.lower() in ['male', 'female', 'else']
        

class SaveManager:
    """
    Enhanced save manager with GUI integration for Quantum Physics Quest
    """
    SAVE_DIR = "saves"
    SAVE_PREFIX = "save_"
    SAVE_EXTENSION = ".qpquest"
    VERSION = "1.0"
    COMPRESSION_LEVEL = 6
    
    def __init__(self):
        os.makedirs(self.SAVE_DIR, exist_ok=True)
        self.current_ui = None
    
    def save(self, game) -> Tuple[bool, str]:
        """Save game data and user data to game.txt"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Extract data from game
            name = getattr(game, "name", "Unknown")
            age = getattr(game, "age", "Unknown")
            gender = getattr(game, "gender", "Unknown")
            energy = getattr(game, "energy", "Unknown")
            location = getattr(game, "location", "Unknown")
            knowledge_score = getattr(game, "knowledge_score", "Unknown")
            questions_answered = getattr(game, "questions_answered", "Unknown")
            difficulty = getattr(game, "difficulty", "Unknown")

            # Build gameplay log
            gameplay_log = "\n".join(game.message_log)

            # Combine all data
            user_data = (
                f"Time: {timestamp}\n"
                f"Name: {name}\n"
                f"Age: {age}\n"
                f"Gender: {gender}\n"
                f"Energy: {energy}\n"
                f"Location: {location}\n"
                f"Knowledge Score: {knowledge_score}\n"
                f"Questions Answered: {questions_answered}\n"
                f"Difficulty: {difficulty}\n"
                f"Gameplay Log:\n{gameplay_log}\n"
                "-------------------------------------\n"
            )

            with open("game.txt", "a") as file:
                file.write(user_data)

            return True, "Game data saved successfully."

        except Exception as e:
            return False, f"Failed to save game: {str(e)}"
    
    def load(self) -> Tuple[bool, list]:
        """Load game data from game.txt"""
        try:
            with open("game.txt", "r") as file:
                content = file.read()

            entries = content.strip().split("-------------------------------------\n")
            games = []

            for entry in entries:
                if not entry.strip():
                    continue  # Skip empty blocks
                lines = entry.strip().split("\n")
                game_data = {}

                for line in lines:
                    if line.startswith("Time:"):
                        game_data["timestamp"] = line.replace("Time:", "").strip()
                    elif line.startswith("Name:"):
                        game_data["name"] = line.replace("Name:", "").strip()
                    elif line.startswith("Age:"):
                        game_data["age"] = line.replace("Age:", "").strip()
                    elif line.startswith("Gender:"):
                        game_data["gender"] = line.replace("Gender:", "").strip()
                    elif line.startswith("Energy:"):
                        game_data["energy"] = line.replace("Energy:", "").strip()
                    elif line.startswith("Location:"):
                        game_data["location"] = line.replace("Location:", "").strip()
                    elif line.startswith("Knowledge Score:"):
                        game_data["knowledge_score"] = line.replace("Knowledge Score:", "").strip()
                    elif line.startswith("Questions Answered:"):
                        game_data["questions_answered"] = line.replace("Questions Answered:", "").strip()
                    elif line.startswith("Difficulty:"):
                        game_data["difficulty"] = line.replace("Difficulty:", "").strip()
                    elif line.startswith("Gameplay Log:"):
                        game_data["gameplay_log"] = "\n".join(lines[lines.index(line) + 1:])

                games.append(game_data)

            return True, games

        except FileNotFoundError:
            return False, "game.txt not found."
        except Exception as e:
            return False, f"Error loading game data: {str(e)}"
    
    def list_saves(self) -> List[dict[str, any]]:
        """List all saves with metadata"""
        saves = []
        for file in Path(self.SAVE_DIR).iterdir():
            if file.is_file() and file.name.startswith(self.SAVE_PREFIX) and file.suffix == self.SAVE_EXTENSION:
                save_info = self._inspect_save(file)
                saves.append(save_info)
        return sorted(saves, key=lambda x: x.get('timestamp', ''), reverse=True)
    
    def show_save_dialog(self, game, callback=None):
        """Show save dialog in GUI"""
        with dpg.window(label="Save Game", modal=True, tag="save_dialog", width=400, height=300):
            dpg.add_text("Save current game progress:")
            dpg.add_spacer(height=10)
            
            with dpg.group(horizontal=True):
                dpg.add_button(label="Quick Save", callback=lambda: self._quick_save(game, callback))
                dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("save_dialog"))
            
            dpg.add_separator()
            dpg.add_text("Existing Saves:")
            
            with dpg.child_window(height=150, border=False):
                saves = self.list_saves()
                if not saves:
                    dpg.add_text("No saves found")
                else:
                    for save in saves:
                        with dpg.group(horizontal=True):
                            dpg.add_text(f"{save['filename']} - {save['metadata']['player_name']}")
                            dpg.add_text(f"Score: {save['metadata']['knowledge_score']}")
    
    def show_load_dialog(self, callback):
        """Show load dialog in GUI"""
        with dpg.window(label="Load Game", modal=True, tag="load_dialog", width=500, height=400):
            dpg.add_text("Select a save to load:")
            dpg.add_spacer(height=10)
            
            with dpg.child_window(height=300, border=False):
                saves = self.list_saves()
                if not saves:
                    dpg.add_text("No saves found")
                else:
                    for save in saves:
                        with dpg.group(horizontal=True):
                            col1 = dpg.add_text(f"{save['filename']}")
                            col2 = dpg.add_text(f"Player: {save['metadata']['player_name']}")
                            col3 = dpg.add_text(f"Score: {save['metadata']['knowledge_score']}")
                            
                            if save['valid']:
                                dpg.add_button(
                                    label="Load",
                                    callback=lambda s=save: self._handle_load(s, callback)
                                )
                            else:
                                dpg.add_text("(Corrupted)")
            
            dpg.add_spacer(height=10)
            dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("load_dialog"))
    
    def _quick_save(self, game, callback=None):
        success, message = self.save(game)
        if success:
            dpg.add_text("Save successful!", parent="save_dialog")
            game.add_message(f"Game saved: {message}")
        else:
            dpg.add_text("Save failed!", parent="save_dialog")
            game.add_message(f"Save error: {message}")
        
        if callback:
            callback()
    
    def _handle_load(self, save, callback):
        game, message = self.load(save['filename'])
        if game:
            dpg.delete_item("load_dialog")
            callback(game)
        else:
            dpg.add_text(f"Load failed: {message}", parent="load_dialog")
    
    def _get_next_save_path(self) -> Path:
        existing = [f.name for f in Path(self.SAVE_DIR).iterdir() 
                  if f.is_file() and f.name.startswith(self.SAVE_PREFIX)]
        
        if not existing:
            next_num = 1
        else:
            nums = [int(re.search(r'\d+', name).group()) for name in existing if re.search(r'\d+', name)]
            next_num = max(nums) + 1 if nums else 1
        
        return Path(self.SAVE_DIR) / f"{self.SAVE_PREFIX}{next_num}{self.SAVE_EXTENSION}"
    
    def _prepare_save_data(self, game) -> dict[str, any]:
        return {
            'version': self.VERSION,
            'timestamp': datetime.now().isoformat(),
            'metadata': {
                'player_name': game.name,
                'location': game.location.name,
                'energy': game.energy,
                'knowledge_score': game.knowledge_score,
                'questions_answered': game.questions_answered,
                'difficulty': game.difficulty.name,
                'quantum_core_unlocked': game.quantum_core_unlocked
            },
            'game_state': game.to_dict()
        }
    
    def _inspect_save(self, filepath: Path) -> dict[str, any]:
        try:
            with open(filepath, 'rb') as f:
                compressed = f.read()
                decompressed = zlib.decompress(compressed)
                data = json.loads(decompressed.decode('utf-8'))
            
            return {
                'filename': filepath.name,
                'valid': True,
                'version': data.get('version'),
                'timestamp': data.get('timestamp'),
                'metadata': data.get('metadata', {}),
                'size_kb': os.path.getsize(filepath) / 1024
            }
        except Exception as e:
            return {
                'filename': filepath.name,
                'valid': False,
                'error': str(e)
            }

# ... [Keep all your existing Electron class code exactly the same] ...
    

class QuantumPhysicsQuestUI:
    
    def __init__(self):
        self.game = Electron()
        self.calculator_elements = []
        self.setup_ui()
        self.setup_calculator()
        self.save_manager = SaveManager()
        #self.config = ConfigManager()
        #self.logger = LoggerManager()
        #self.stats = StatsTracker()
    
    def show_save_dialog(self):
        """show the save game dialog"""
        self.save_manager.show_load_dialog(self.handle_loaded_game)
    def show_load_dialog(self):
        """show the load game dialog"""
        self.save_manager.show_load_dialog(self.handle_loaded_game)
    def handle_loaded_game(self, loaded_game):
        """Callback when a game is loaded"""
        self.game = loaded_game
        self.update_ui()
        self.game.add_message("Game loaded successfully!")

        

    def setup_calculator(self):
        # Create themes first
        with dpg.theme() as self.primarybtn_green_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Button, (16, 194, 75), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0,0,0), category=dpg.mvThemeCat_Core)

        with dpg.theme() as self.primarybtn_red_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Button, (155,0,0), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0,0,0), category=dpg.mvThemeCat_Core)

        # Create calculator window
        with dpg.window(label="Calculator", tag="calculator_window", width=800, height=625, 
                       no_resize=True, no_collapse=True, show=False):
            dpg.add_text("0", tag="calculator_input")
            dpg.add_spacer(height=10)
            
            # Calculator buttons layout...
            with dpg.group(horizontal=True):
                dpg.add_button(label="6", width=100, height=100, callback=lambda: self.calculate("6"))
                dpg.add_button(label="7", width=100, height=100, callback=lambda: self.calculate("7"))
                dpg.add_button(label="8", width=100, height=100, callback=lambda: self.calculate("8"))
                dpg.add_button(label="9", width=100, height=100, callback=lambda: self.calculate("9"))
                dpg.add_button(label="%", width=100, height=100, callback=lambda: self.calculate("%"))
                dpg.add_button(label="sqrt", width=100, height=100, callback=lambda: self.calculate("sqrt"))
                dpg.add_button(label="Close", width=100, height=50, callback=lambda: dpg.hide_item("calculator_window"))


            with dpg.group(horizontal=True):
                dpg.add_button(label="1", width=100, height=100, callback=lambda: self.calculate("1"))    
                dpg.add_button(label="2", width=100, height=100, callback=lambda: self.calculate("2"))
                dpg.add_button(label="3", width=100, height=100, callback=lambda: self.calculate("3"))
                dpg.add_button(label="4", width=100, height=100, callback=lambda: self.calculate("4"))
                dpg.add_button(label="5", width=100, height=100, callback=lambda: self.calculate("5"))
                dpg.add_button(label="*", width=100, height=100, callback=lambda: self.calculate("*"))        
                dpg.add_button(label="÷", width=100, height=100, callback=lambda: self.calculate("/"))
            with dpg.group(horizontal=True):
                dpg.add_button(label="00", width=100, height=100, callback=lambda: self.calculate("00"))
                dpg.add_button(label=".", width=100, height=100, callback=lambda: self.calculate("."))
                dpg.add_button(label="(", width=100, height=100, callback=lambda: self.calculate("("))
                dpg.add_button(label=")", width=100, height=100, callback=lambda: self.calculate(")"))

            with dpg.group(horizontal=True):
                equals = dpg.add_button(label="=", width=317, height=100, callback=lambda: self.calculate("="))
                dpg.bind_item_theme(equals, self.primarybtn_green_theme)
                delete = dpg.add_button(label="DEL", width=100, height=100, callback=lambda: self.calculate("del"))
                dpg.bind_item_theme(delete, self.primarybtn_red_theme)
                clear = dpg.add_button(label="CLEAR", width=100, height=100, callback=lambda: self.calculate("clear"))
                dpg.bind_item_theme(clear, self.primarybtn_red_theme)

    def calculate(self, symbol: str):
        try:
            if symbol == '=':
                if self.calculator_elements:  # Only calculate if there's input
                    result = eval("".join(str(i) for i in self.calculator_elements))
                    self.calculator_elements.clear()
                    self.game.add_message(f"Calculator result: {result}")
                    dpg.set_value("calculator_input", str(result))
                    #dpg.hide_item("calculator_window")
            elif symbol == 'clear':
                self.calculator_elements.clear()
                dpg.set_value("calculator_input", "0")
            elif symbol == 'del':
                if self.calculator_elements:
                    self.calculator_elements = self.calculator_elements[:-1]
                    dpg.set_value("calculator_input", "".join(str(i) for i in self.calculator_elements) or "0")
            elif symbol == 'sqrt':
                self.calculator_elements.append('**0.5')
                dpg.set_value("calculator_input", "".join(str(i) for i in self.calculator_elements))
            elif symbol.isdigit() or symbol in ['+', '-', '*', '/', '.', '(', ')', '%']:
                self.calculator_elements.append(symbol)
                dpg.set_value("calculator_input", "".join(str(i) for i in self.calculator_elements))
            elif symbol == "pi":
                self.calculator_elements.append("math.pi")
                dpg.set_value("calculator_input", "".join(str(i) for i in self.calculator_elements))
        except Exception as err:
            self.game.add_message(f"Calculator error: {err}")
            dpg.set_value("calculator_input", "Error")
            self.calculator_elements.clear()

    def show_calculator(self):
        if not dpg.does_item_exist("calculator_window"):
            self.setup_calculator()
        dpg.show_item("calculator_window")
        dpg.focus_item("calculator_window")
        dpg.set_value("calculator_input", "0")
        self.calculator_elements.clear()

    def setup_ui(self):
        dpg.create_context()
        dpg.create_viewport(title='Quantum Physics Quest', width=1000, height=600)

        with dpg.window(tag="Primary Window", width=900, height=600):
            with dpg.child_window(height=-50, width=-1):
                self.game_log = dpg.add_input_text(
                    multiline=True, 
                    readonly=True, 
                    height=-1,
                    width=-1,
                    tag="game_log"
                )
            self.user_input = dpg.add_input_text(
                tag="user_input", 
                hint="Type a command...", 
                on_enter=True, 
                callback=self.on_user_input,
                width=-1
            )
            dpg.set_item_height(self.user_input, 40)
        
        dpg.set_primary_window("Primary Window", True)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        self.update_ui() #show initial game messages


    def on_user_input(self, sender, app_data):
        command = dpg.get_value(sender).strip()
        dpg.set_value(sender, "")

        if not command:
            return

        if self.game.asking_intro:
            self.handle_intro_questions(command)
            self.update_ui()
            return

        self.game.add_message(f"> {command}")

        if self.game.game_state == GameState.ANSWERING_QUESTION:
            self.game.check_physics_answer(command)
            self.update_ui()
            return

        self.handle_game_commands(command)
        self.update_ui()

    def handle_intro_questions(self, command):
        if self.game.pending_question == "name":
            if self.game.is_valid_name(command):
                self.game.name = command
                self.game.add_message(f"Nice to meet you, {self.game.name}!")
                self.game.add_message("How old are you? (Positive numbers only)")
                self.game.pending_question = "age"
            else:
                self.game.add_message("Invalid name! Please use only alphabetic characters and spaces.")
                self.game.add_message("What's your name? (Alphabetic characters only)")
        
        elif self.game.pending_question == "age":
            if self.game.is_valid_age(command):
                self.game.age = command
                self.game.add_message(f"Got it. Age: {self.game.age}")
                self.game.add_message("What's your gender? (male/female/else)")
                self.game.pending_question = "gender"
            else:
                self.game.add_message("Invalid age! Please enter a positive whole number.")
                self.game.add_message("How old are you? (Positive numbers only)")
        
        elif self.game.pending_question == "gender":
            if self.game.is_valid_gender(command):
                self.game.gender = command.lower()
                self.game.add_message(f"Thank you! Gender set to: {self.game.gender}")
                self.game.asking_intro = False
                self.game.game_state = GameState.PLAYING
                self.game.add_message("\nType 'help' for a list of available commands.")
                self.game.add_message("You'll need to solve physics problems to navigate space!")
                self.game.add_message("Solve enough problems to discover your ultimate destination!")
            else:
                self.game.add_message("Invalid gender! Please enter 'male', 'female', or 'else'.")
                self.game.add_message("What's your gender? (male/female/else)")

    def handle_game_commands(self, command):
        #global needed
        cmd = command.lower()

        if cmd == "help":
            self.game.add_message("Commands:")
            self.game.add_message("travel <location> - Move to a new location")
            self.game.add_message("solve - Attempt to solve a physics problem for energy")
            self.game.add_message("status - Show your current status")
            self.game.add_message("difficulty - Show current difficulty level")
            self.game.add_message("locations - List available travel destinations")
            self.game.add_message("facts - Show interesting facts about current location")
            self.game.add_message("calc- Open a calculator for physics calculations")
            self.game.add_message("save - Save your game progress")
            self.game.add_message("load - Load a saved game")
        elif cmd.startswith("travel"):
            parts = cmd.split()
            if len(parts) > 1:
                try:
                    dest_name = parts[1].upper()
                    if "_" in dest_name:
                        dest_name = dest_name.replace("_", " ")
                    dest = Location[dest_name]
                    if not ENVIRONMENTS[dest]["visible"]:
                        self.game.add_message("This location is not yet known to you!")
                        self.game.add_message("Solve more physics problems to unlock new locations.")
                    else:
                        self.game.move(dest)
                except KeyError:
                    self.game.add_message(f"Unknown location: {parts[1]}")
                    self.show_available_locations()
            else:
                self.game.add_message("Usage: travel <location>")
                self.show_available_locations()
        elif cmd == "solve":
            self.game.ask_physics_question()
        elif cmd == "status":
          self.game.add_message(f"Name: {self.game.name}")
          self.game.add_message(f"Age: {self.game.age}")
          self.game.add_message(f"Gender: {self.game.gender}")
          self.game.add_message(f"Energy: {self.game.energy}/{self.game.max_energy}")
          self.game.add_message(f"Location: {self.game.location.value}")
          self.game.add_message(f"Knowledge score: {self.game.knowledge_score}/{self.game.questions_answered}")
          if not self.game.quantum_core_unlocked:
              needed = ENVIRONMENTS[Location.QUANTUM_CORE]["unlock_threshold"] - self.game.knowledge_score
              self.game.add_message(f"Solve {needed} more problems to discover your ultimate destination!")
        elif cmd == "difficulty":
            self.game.add_message(f"Current difficulty: {self.game.difficulty.name}")
        elif cmd == "locations":
            self.show_available_locations()
        elif cmd == "facts":
            self.show_location_facts()
        elif cmd == "calc":
            self.game.add_message("Opening calculator... Type your expression and press =")
            self.show_calculator()
        elif cmd == "closecalc":
          if dpg.does_item_exist("calculator_window"):
            dpg.hide_item("calculator_window")
            self.game.add_message("Calculator closed")
          else:
            self.game.add_message("No calculator is open")
        elif cmd == "restart":
            dpg.delete_item("Primary Window", children_only=False)
            self.__init__()  # Recursively reinit the whole UI and smoothly use recursion
            self.run()       # Start loop again
        elif cmd == "save":
            success, message = self.save_manager.save(self.game)
            if success:
                self.game.add_message("Game saved successfully.")
            else:
                self.game.add_message(f"Failed to save game: {message}")
        elif cmd == "load":
            success, games = self.save_manager.load()
            if success:
                self.game.add_message("Available saved games:")
                for idx, game_data in enumerate(games, start=1):
                    self.game.add_message(f"{idx}. {game_data['timestamp']} - {game_data['name']} (Score: {game_data['knowledge_score']})")
                self.game.add_message("Use the GUI to load a specific save.")
            else:
                self.game.add_message(f"Failed to load saves: {games}")
        else:
            self.game.add_message("Unknown command. Type 'help' for options.")

    def show_available_locations(self):
        visible_locs = self.game.get_visible_locations()
        self.game.add_message("Available locations:")
        for loc in visible_locs:
            self.game.add_message(f"- {loc.value.replace('_', ' ')}")
        if not self.game.quantum_core_unlocked:
            needed = ENVIRONMENTS[Location.QUANTUM_CORE]["unlock_threshold"] - self.game.knowledge_score
            self.game.add_message(f"Solve {needed} more problems to discover hidden locations!")

    def show_location_facts(self):
        env = ENVIRONMENTS[self.game.location]
        self.game.add_message(f"\nFacts about {self.game.location.value}:")
        for fact in env["facts"]:
            self.game.add_message(f"- {fact}")

    def update_ui(self):
        log_text = "\n".join(self.game.message_log)
        dpg.set_value(self.game_log, log_text)
        # Force scroll to bottom
        line_count = len(self.game.message_log)
        dpg.set_item_height(self.game_log, line_count * 20)  # Approximate line height
        dpg.focus_item("user_input")

    def run(self):
        dpg.start_dearpygui()
        while dpg.is_dearpygui_running():
            self.update_ui()
            dpg.render_dearpygui_frame()
        dpg.destroy_context()

if __name__ == "__main__":
    ui = QuantumPhysicsQuestUI()

    ui.run()
