import re
import random
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import time

class AdvancedRuleBasedChatbot:
    def __init__(self):
        self.name = "Alex"
        self.user_name = None
        self.context = {
            "topic": None,
            "last_question": None,
            "conversation_history": [],
            "mood": "neutral",
            "user_interests": set()
        }
        
        # Knowledge base with categorized responses
        self.knowledge_base = {
            "greetings": {
                "patterns": [
                    r"hello", r"hi", r"hey", r"good morning", r"good afternoon", 
                    r"good evening", r"howdy", r"greetings", r"sup"
                ],
                "responses": [
                    "Hello! How can I assist you today?",
                    "Hi there! What's on your mind?",
                    "Hey! Great to see you. How can I help?",
                    "Greetings! I'm here to help with whatever you need."
                ]
            },
            "farewells": {
                "patterns": [
                    r"bye", r"goodbye", r"see you", r"farewell", r"take care",
                    r"quit", r"exit", r"stop", r"end chat"
                ],
                "responses": [
                    "Goodbye! Have a wonderful day!",
                    "See you later! It was nice talking to you.",
                    "Take care! Come back anytime.",
                    "Farewell! Don't hesitate to return if you have more questions."
                ]
            },
            "name_query": {
                "patterns": [
                    r"what is your name", r"who are you", r"your name",
                    r"are you called", r"what should i call you"
                ],
                "responses": [
                    "I'm {bot_name}, your virtual assistant!",
                    "You can call me {bot_name}. I'm here to help you!",
                    "I go by {bot_name}. What's your name?"
                ]
            },
            "user_name": {
                "patterns": [
                    r"my name is (\w+)", r"i am (\w+)", r"i'm (\w+)",
                    r"call me (\w+)", r"you can call me (\w+)"
                ],
                "responses": [
                    "Nice to meet you, {user_name}! How can I help you today?",
                    "Hello {user_name}! What brings you here?",
                    "Great to meet you, {user_name}! I'm here to assist."
                ]
            },
            "how_are_you": {
                "patterns": [
                    r"how are you", r"how do you feel", r"are you okay",
                    r"what's up", r"how's it going"
                ],
                "responses": [
                    "I'm doing great, thanks for asking! How about you?",
                    "I'm functioning perfectly! How can I assist you?",
                    "All systems operational! What's on your mind?"
                ]
            },
            "help": {
                "patterns": [
                    r"help", r"what can you do", r"capabilities",
                    r"functions", r"assist"
                ],
                "responses": [
                    "I can help with many things! Here's what I can do:\n"
                    "1. Answer questions about various topics\n"
                    "2. Perform calculations\n"
                    "3. Tell you the current time and date\n"
                    "4. Have conversations on different topics\n"
                    "5. Help with basic problem-solving\n"
                    "Just ask me anything!",
                    "I'm a multi-purpose chatbot. I can chat, calculate, "
                    "tell time, and answer questions. What would you like to try?"
                ]
            },
            "time": {
                "patterns": [
                    r"what time is it", r"current time", r"time now",
                    r"what's the time", r"tell me the time"
                ],
                "responses": [
                    "The current time is {current_time}.",
                    "It's {current_time} right now.",
                    "According to my clock, it's {current_time}."
                ]
            },
            "date": {
                "patterns": [
                    r"what is today", r"current date", r"what's the date",
                    r"today's date", r"date today"
                ],
                "responses": [
                    "Today is {current_date}.",
                    "The current date is {current_date}.",
                    "It's {current_date} today."
                ]
            },
            "weather": {
                "patterns": [
                    r"weather", r"temperature", r"forecast", 
                    r"raining", r"sunny", r"cold", r"hot"
                ],
                "responses": [
                    "I'm sorry, I don't have real-time weather data. "
                    "But I recommend checking a weather service for accurate information!",
                    "For current weather conditions, you might want to check "
                    "a weather website or app. I can help with other things though!"
                ]
            },
            "joke": {
                "patterns": [
                    r"tell me a joke", r"make me laugh", r"joke",
                    r"funny story", r"entertain me"
                ],
                "responses": [
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "Why did the scarecrow win an award? He was outstanding in his field!",
                    "What do you call fake spaghetti? An impasta!",
                    "Why don't eggs tell jokes? They'd crack each other up!"
                ]
            },
            "thanks": {
                "patterns": [
                    r"thank you", r"thanks", r"appreciate it",
                    r"you're helpful", r"grateful"
                ],
                "responses": [
                    "You're welcome! Happy to help.",
                    "My pleasure! Is there anything else I can do for you?",
                    "Glad I could assist! Don't hesitate to ask if you need more help."
                ]
            },
            "math": {
                "patterns": [
                    r"calculate (\d+[\+\-\*/]\d+)", r"what is (\d+[\+\-\*/]\d+)",
                    r"(\d+[\+\-\*/]\d+)", r"add (\d+) and (\d+)",
                    r"subtract (\d+) from (\d+)", r"multiply (\d+) by (\d+)",
                    r"divide (\d+) by (\d+)"
                ],
                "responses": [
                    "The result is {result}.",
                    "That would be {result}.",
                    "Let me calculate... it's {result}."
                ]
            },
            "age": {
                "patterns": [
                    r"how old are you", r"what is your age",
                    r"when were you created", r"your age"
                ],
                "responses": [
                    "I'm a chatbot, so I don't have an age in the traditional sense! "
                    "But I was created to help users like you.",
                    "Age is just a number for AIs! I exist to assist you whenever you need."
                ]
            },
            "purpose": {
                "patterns": [
                    r"what is your purpose", r"why were you made",
                    r"what do you do", r"your purpose"
                ],
                "responses": [
                    "My purpose is to assist you with information, "
                    "answer questions, and have engaging conversations!",
                    "I was created to be a helpful companion that can "
                    "answer questions and assist with various tasks."
                ]
            }
        }
        
        # Contextual follow-up questions
        self.follow_ups = {
            "how_are_you": [
                "What have you been up to lately?",
                "Is there anything interesting happening in your life?",
                "How has your day been so far?"
            ],
            "help": [
                "Would you like me to explain any of my capabilities in detail?",
                "Is there something specific you'd like help with?"
            ],
            "joke": [
                "Would you like to hear another one?",
                "Did that make you smile?"
            ]
        }
        
        # Default responses for unmatched queries
        self.default_responses = [
            "That's interesting! Tell me more.",
            "I'm not sure I understand completely. Could you rephrase that?",
            "I see. What are your thoughts on that?",
            "That's something to think about. Can you elaborate?",
            "Interesting point. How does that relate to your interests?"
        ]
        
    def match_pattern(self, user_input: str) -> Tuple[Optional[str], Optional[Dict]]:
        """Match user input to patterns in knowledge base."""
        user_input = user_input.lower().strip()
        
        for category, data in self.knowledge_base.items():
            for pattern in data["patterns"]:
                match = re.search(pattern, user_input)
                if match:
                    return category, match
        return None, None
    
    def extract_name(self, user_input: str) -> Optional[str]:
        """Extract user name from input."""
        patterns = [
            r"my name is (\w+)",
            r"i am (\w+)",
            r"i'm (\w+)",
            r"call me (\w+)",
            r"you can call me (\w+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                return match.group(1).capitalize()
        return None
    
    def calculate_math(self, expression: str) -> Optional[float]:
        """Evaluate mathematical expressions safely."""
        try:
            # Remove non-math characters and evaluate
            expression = re.sub(r'[^\d\+\-\*\/\.]', '', expression)
            # Use eval cautiously (with only math operations)
            if re.match(r'^[\d\+\-\*\/\.]+$', expression):
                return eval(expression)
        except:
            pass
        return None
    
    def get_time_date(self) -> Tuple[str, str]:
        """Get current time and date."""
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        current_date = now.strftime("%B %d, %Y")
        return current_time, current_date
    
    def generate_response(self, category: str, match=None) -> str:
        """Generate appropriate response based on matched category."""
        if category not in self.knowledge_base:
            return random.choice(self.default_responses)
        
        # Get random response from category
        response_template = random.choice(self.knowledge_base[category]["responses"])
        
        # Replace placeholders with actual values
        if "{bot_name}" in response_template:
            response_template = response_template.format(bot_name=self.name)
        
        if "{user_name}" in response_template and self.user_name:
            response_template = response_template.format(user_name=self.user_name)
        
        if "{current_time}" in response_template or "{current_date}" in response_template:
            current_time, current_date = self.get_time_date()
            response_template = response_template.format(
                current_time=current_time,
                current_date=current_date
            )
        
        # Handle math calculations
        if category == "math" and match:
            math_expr = match.group(1) if match.group(1) else f"{match.group(2)} {match.group(3)} {match.group(4)}"
            result = self.calculate_math(math_expr)
            if result is not None:
                response_template = response_template.format(result=result)
            else:
                response_template = "I couldn't calculate that. Please provide a valid mathematical expression."
        
        return response_template
    
    def add_follow_up(self, category: str) -> str:
        """Add contextual follow-up question."""
        if category in self.follow_ups:
            return " " + random.choice(self.follow_ups[category])
        return ""
    
    def update_context(self, user_input: str, bot_response: str, category: str):
        """Update conversation context."""
        self.context["last_question"] = category
        self.context["conversation_history"].append({
            "user": user_input,
            "bot": bot_response,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        
        # Keep only last 10 messages in history
        if len(self.context["conversation_history"]) > 10:
            self.context["conversation_history"] = self.context["conversation_history"][-10:]
    
    def get_personalized_response(self, user_input: str) -> str:
        """Generate personalized responses based on user interests."""
        user_input_lower = user_input.lower()
        
        # Detect interests from input
        interests_keywords = {
            "sports": ["sports", "football", "basketball", "soccer", "tennis", "game"],
            "music": ["music", "song", "band", "concert", "album", "listen"],
            "movies": ["movie", "film", "cinema", "actor", "actress", "watch"],
            "books": ["book", "read", "author", "novel", "literature"],
            "technology": ["tech", "computer", "software", "programming", "code", "ai"]
        }
        
        for interest, keywords in interests_keywords.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    self.context["user_interests"].add(interest)
        
        # If we know user interests, personalize response
        if self.context["user_interests"]:
            interests_list = list(self.context["user_interests"])
            interest = random.choice(interests_list)
            
            personalized_responses = {
                "sports": [
                    f"Since you like {interest}, have you been following any games lately?",
                    f"Talking about {interest}, who's your favorite team?"
                ],
                "music": [
                    f"Since you mentioned {interest}, what's your favorite genre?",
                    f"Music is great! What have you been listening to recently?"
                ],
                "movies": [
                    f"Since you like {interest}, have you seen any good films lately?",
                    f"Movies are wonderful! What's your all-time favorite?"
                ],
                "books": [
                    f"Since you enjoy {interest}, what are you reading currently?",
                    f"Books open new worlds! What's the best book you've read recently?"
                ],
                "technology": [
                    f"Since you're interested in {interest}, what tech excites you most?",
                    f"Technology evolves so fast! What's your favorite gadget?"
                ]
            }
            
            if interest in personalized_responses:
                return random.choice(personalized_responses[interest])
        
        return random.choice(self.default_responses)
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate response."""
        # Check for empty input
        if not user_input.strip():
            return "I didn't catch that. Could you please say something?"
        
        # Update user name if mentioned
        extracted_name = self.extract_name(user_input)
        if extracted_name and not self.user_name:
            self.user_name = extracted_name
        
        # Match pattern in knowledge base
        category, match = self.match_pattern(user_input)
        
        # Generate response
        if category:
            response = self.generate_response(category, match)
            # Add follow-up for certain categories
            if category in ["how_are_you", "help", "joke"]:
                response += self.add_follow_up(category)
        else:
            # Use personalized response for unmatched queries
            response = self.get_personalized_response(user_input)
        
        # Update context
        self.update_context(user_input, response, category or "unknown")
        
        return response
    
    def start_conversation(self):
        """Start interactive conversation with the chatbot."""
        print(f"\n{'='*60}")
        print(f"Welcome to the Advanced Rule-Based Chatbot!")
        print(f"My name is {self.name}. I'm here to assist you.")
        print(f"Type 'quit', 'exit', or 'bye' to end the conversation.")
        print(f"{'='*60}\n")
        
        # Initial greeting
        print(f"{self.name}: {random.choice(self.knowledge_base['greetings']['responses'])}")
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                # Check for exit commands
                if any(exit_cmd in user_input.lower() for exit_cmd in 
                       ["bye", "goodbye", "exit", "quit", "stop", "end"]):
                    farewell = random.choice(self.knowledge_base["farewells"]["responses"])
                    if self.user_name:
                        farewell = farewell.replace("!", f", {self.user_name}!")
                    print(f"\n{self.name}: {farewell}")
                    
                    # Show conversation summary
                    print(f"\n{'='*60}")
                    print("Conversation Summary:")
                    print(f"Total messages exchanged: {len(self.context['conversation_history'])}")
                    if self.context['user_interests']:
                        print(f"Your interests detected: {', '.join(self.context['user_interests'])}")
                    print(f"{'='*60}")
                    break
                
                # Process input and get response
                response = self.process_input(user_input)
                
                # Print response with slight delay for natural feel
                time.sleep(0.3)
                print(f"{self.name}: {response}")
                
            except KeyboardInterrupt:
                print(f"\n\n{self.name}: Goodbye! Thanks for chatting!")
                break
            except Exception as e:
                print(f"\n{self.name}: Sorry, I encountered an error. Let's continue.")
                continue

def main():
    """Main function to run the chatbot."""
    chatbot = AdvancedRuleBasedChatbot()
    chatbot.start_conversation()

if __name__ == "__main__":
    main()