# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import random
import urllib3
import json
import re
import ask_sdk_model
import ask_sdk_core.utils as ask_utils
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective
from utils import create_presigned_url


from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import get_supported_interfaces
from ask_sdk_model import ui

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
wordlist = [ "Goddess", "Walking", "Ponds", "Apocalypse", "Jockeys", "Rattles", "Daggers", "Hearts", "Cosmetic Containers", "Shintō", "Antelope", "Picnics", "Witches", "Athletes", "Machines", "Stairs", "Lizards", "Museums", "Tea Houses", "Bakers", "Centaurs", "Sun", "Trumpets", "Games", "Shells", "Mermen", "Clothing", "Motorcycles", "Unicorns", "Samurai", "Obelisks", "Sewing", "Lightning", "Mermaids", "Harpsichords", "Musicians", "Boars", "Corsets", "Kings", "Trophies", "Telescopes", "Tea Drinking", "Dishes", "Parrots", "Patroclus", "Military Clothing", "Cattle", "Vases", "Emperors", "Courtyards", "Sundials", "Crowd", "Bathrooms", "Incense Burners", "Coffins", "Lanterns", "Octopus", "Cross", "Boats", "Leopards", "Camps", "Illness", "Wrestling", "Tents", "Accordions", "Slavery", "Hotels", "Thrones", "Princes", "Roofs", "Fathers", "Pheasants", "Frogs", "Ritual Objects", "Daily Life", "Turkeys", "Poets", "Carrots", "Military Equipment", "Harbors", "Adam", "Baboons", "Chariots", "Needlework", "Manna", "Demons", "Basins", "Lutes", "Cradles", "Streetcars", "Bread", "Egg and Dart", "Tankards", "Lakes", "Shipwrecks", "Cities", "Tombstones", "Butchers", "Tablets", "Plows", "Theatre", "Allegory", "Doors", "Last Supper", "Books", "Hands", "Banners", "Fairies", "Pins", "Scissors", "Horse Riding", "Soldiers", "Garlands", "Pianos", "Drinking Glasses", "Poverty", "Gourds", "Kettles", "Angels", "Performance", "Family", "Buildings", "Arrowheads", "Gates", "Sailing", "Butterflies", "Squirrels", "Scorpions", "Schools", "Jackals", "Bears", "Peacocks", "Monuments", "Beds", "Spoons", "Running", "Oceans", "Utilitarian Objects", "Potatoes", "Buffalos", "Zodiac", "Skulls", "Heaven", "Tractors", "Victory", "Cloisters", "Shuttlecock", "Knives", "Anklet", "Photography", "Poppies", "Chests", "Elephants", "Cypresses", "Reading", "Roses", "Ladles", "Actors", "Funerary Objects", "Violets", "Cooking", "Urns", "Windows", "Education", "Fluting", "Tombs", "Santa Claus", "Hair", "Buckles", "Pipes", "Hens", "Tennis", "Towers", "Reliquaries", "Sculpture", "Doorways", "Tools", "Swords", "Globes", "Zeus", "Cinema", "Watches", "Dance", "Graffiti", "Pens", "Rhinocerus", "Navy", "Rosaries", "Cellos", "Nature", "Candles", "Fences", "Shepherds", "Lovers", "Military Transport", "Generals", "Cupid", "Shirts", "Strawberries", "Prisoners", "Television", "Tea Caddy", "Oysters", "Cooking Containers", "Monsters", "Fishing", "Mouths", "Diadems", "Government", "Plants", "Burial Grounds", "Playing Cards", "Microscopes", "Thanksgiving", "Bamboo", "Nuns", "Animals", "Gardens", "Bracelets", "Spring", "Politics", "Reservoirs", "Funerary Monuments", "Lemons", "Palms", "Playing", "Wreaths", "Water Lilies", "Doves", "Nymphs", "Air Force", "Violas", "Acorns", "Tureens", "Stage Design", "Lobsters", "Cooking Equipment", "Amazons", "Railways", "Docks", "Gambling", "Execution", "Ibex", "Whales", "Squid", "Skiing", "Mirrors", "Ballet", "Belts", "Weddings", "Leaves", "Fire", "Fear", "Nose Rings", "Peonies", "Corn", "Seas", "Organs", "Stars", "Herbs", "Tiger", "Science", "Concerts", "Girls", "Rivers", "Massacres", "Banquets", "Smoking", "Stadiums", "Prostitutes", "Historical Figures", "Lighthouses", "Police", "Deer", "Cosmetic Tools", "Dressers", "Lamps", "Barrels", "Fortification", "Trucks", "Columns", "Football", "Goblets", "Earrings", "Chairs", "Streets", "Trombones", "Gluttony", "Rabbits", "Eggs", "Crucifix", "Pigs", "Male Nudes", "Trays", "Elms", "Phones", "Tomatoes", "Eggplants", "Spiders", "Rams", "Footwear", "Bicycles", "Restaurants", "Moats", "Washing", "Panthers", "Islands", "Pitchers", "Tables", "Medallions", "Female Nudes", "Desks", "Camels", "Geometry", "Dragonflies", "Textiles", "Violins", "Processions", "Lambs", "Hourglass", "Autumn", "Coffee", "Mailbox", "Churches", "Transportation", "Gloves", "Forests", "Bottles", "Factories", "Correspondence", "Oaks", "Buckets", "Spectators", "Elections", "Love", "Hawks", "Post Offices", "Streams", "Literature", "Miter", "Umbrellas", "Economy", "Archery", "Blacksmiths", "Jewelry", "Peaches", "Screens", "Princesses", "Anchors", "Visitation", "Trees", "Christ", "Masks", "Pastoral", "Fires", "Tigers", "Landscapes", "Scales", "Towns", "Monks", "Harps", "Women", "Planes", "Manuscripts", "Suits", "Bedrooms", "Stupas", "Ceremony", "Pineapples", "Coat of Arms", "Armed Forces", "Bridges", "Parasols", "Boxes", "Boots", "Dolphins", "Fireplaces", "Swans", "Turtles", "Wagons", "Chickens", "Easter", "Wigs", "Villages", "David", "Gods", "Poetry", "Dawn", "Guitars", "Crayfish", "Looms", "Falcons", "Kites", "Acrobats", "Roads", "Cats", "Working", "Shields", "Faces", "Queens", "Calendars", "Chapels", "Onions", "Balloons", "Mars", "Earthquakes", "Hats", "Paris", "Lilies", "Scarves", "Minotaurs", "Flora", "Palmettes", "Teapots", "Axes", "Commodes", "Headrests", "Baskets", "Dresses", "Storms", "Painting", "Subways", "Aqueducts", "Winter", "Insignia", "Chalices", "Olive Trees", "Carts", "Morning", "Cows", "Fauns", "Crypts", "Stables", "Sunflowers", "Helmets", "Light bulbs", "Buses", "Apples", "Clowns", "Snakes", "Houses", "Sleeping", "Drawing", "Firefighters", "Double Basses", "Arrows", "Wars", "Pocket Watches", "Swimming", "Hospitals", "Ducks", "Taverns", "Burials", "Cranes", "Birth", "Nursing", "Vestments", "Crocodiles", "Pendants", "Cathedrals", "Wine", "Necklaces", "Cups", "Mountains", "Hedgehogs", "Warehouses", "Bellows", "Jackets", "Badges", "Acanthus", "Geese", "Devil", "Death", "Dice", "Easels", "Ladders", "Baseball", "Fruit", "Ears", "Cafe", "Dragons", "Barns", "Sleighs", "Music", "Volcanoes", "Chaises", "Helicopters", "Goats", "Palaces", "Benches", "Merchants", "Dining Rooms", "Train Stations", "Mercury", "Admirals", "Cheetahs", "Spears", "Vegetables", "Furniture", "Chess", "Knitting", "Dogs", "Medals", "Bats", "Crabs", "Fashion", "Lighting", "Bagpipes", "Lions", "Street Scene", "Deities", "Leisure", "Keyboards", "Kitchens", "Clouds", "Narcissus", "Robes", "Medicine", "Headdresses", "Children", "Billiards", "Beakers", "Serpents", "Zebras", "Vines", "Griffins", "Satire", "Scarabs", "Portraits", "Feet", "Bees", "Prisons", "Pelicans", "Domes", "Pilasters", "Sheep", "Tunnels", "Weapons", "Drunkenness", "Eagles", "Peace", "Hurricanes", "Rowing", "Pagodas", "Cherries", "Couples", "Fog", "Hercules", "Amphitheatres", "Mushrooms", "Trailers", "Amusement Parks", "Circus", "Architecture", "Caves", "Infants", "Irons", "Mothers", "Inns", "Greek", "Feathers", "Knights", "Puppets", "Ewers", "Flutes", "Praying", "Moon", "Diaries", "Temples", "Gladiators", "Pavilions", "Hammers", "Windmills", "Buddha", "Newspapers", "Murals", "Money", "Drums", "Brooches", "Advertisements", "Fans", "Ambulances", "Lotuses", "Flowers", "Cornucopia", "Seahorses", "Parables", "Gas Station", "Warriors", "Opera", "Altars", "Ceilings", "Uniforms", "Tea", "Snails", "Daisies", "Balconies", "Cakes", "Bells", "Saturn", "Deserts", "Tools and Equipment", "Documents", "Ice", "Seals", "Shacks", "Couches", "Coffeepots", "Grapes", "Sword Guards", "Necktie", "Evangelists", "Military", "Armor", "Fireworks", "Dolls", "Marines", "Bowls", "Air Transports", "Magicians", "Taxis", "Bes", "Caricature", "Maenads", "Owls", "Medusa", "Bathing", "Clergy", "Horses", "Insects", "Libraries", "Castles", "Crowns", "Hilts", "Shoes", "Singers", "Sports", "Seasons", "Cameras", "Arms", "Floods", "Pegasus", "Rats", "Rainbows", "Waves", "Writing", "Dressing", "Beads", "Industry", "Amulets", "Farms", "Candelabra", "Drinking Vessels", "Signs", "Hippos", "Pomegranates", "Lockets", "Pigeons", "Fish", "Sailors", "Cheese", "Curtains", "Markets", "Spindles", "Apes", "Anger", "Toys", "Ships", "Sledging", "Harvesting", "Cannons", "Fencing", "Trains", "Army", "Food", "Singing", "Boys", "Candlesticks", "Roosters", "Rings", "Mosques", "Job", "Vessels", "Drinking", "Wind", "Ruins", "Giraffes", "Ox", "Eating", "Hunting", "Waterfalls", "Scientists", "Slaves", "Piers", "Eyes", "Palettes", "Musical Instruments", "Censers", "Night", "Typewriters", "Cigarettes", "Entombment", "Wolves", "Canals", "Sirens", "Architects", "Phoenix", "Artists", "Monkeys", "Maps", "Tea Ceremony", "Foxes", "Hills", "Shops", "Sadness", "Corpses", "Keys", "Emblems", "Watermills", "Doctors", "Dancing", "Party", "Legs", "Donkeys", "Magic", "Bulls", "Farmers", "Venus", "Horns", "Jugs", "Philosophers", "Scrolls", "Orchids", "Tulips", "Living Rooms", "Capitals", "Dining", "Men", "Stools", "Salamanders", "Genie", "Haystacks", "Teachers", "Coins", "Skeletons", "Carriages", "Firearms", "Cabinets", "Funerals", "Nurses", "Silenus", "Agriculture", "Parks", "Snow", "Ornament", "Flags", "Resurrection", "Alligators", "Mice", "Students", "Pyramids", "Christmas", "Abbeys", "Helen", "Rain", "Arches", "Chandelier", "Mathematics", "Wells", "Jars", "Pears", "Sky", "Boxing", "Birds", "Planets", "Dancers", "Costumes", "Phaeton", "Heads", "Hammocks", "Cars", "Skating", "Gardeners", "Evening", "Clocks", "Summer", "Cemeteries", "Battles", "Flagellation", "Happiness", "Bow and Arrow", "Bubbles", "Chemistry", "Fountains", "Purses", "Hot Air Balloons", "Drink-and-Be-Merry", "Golf", "Beaches", "Servants"]

def is_APL_supported(handler_input):
    return get_supported_interfaces(handler_input).alexa_presentation_apl is not None

def _load_apl_document(file_path):
    with open(file_path) as f:
        return json.load(f)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to Art in Objects. Please let me know what you want to find, such as, find dog. if you want some inspiration, just say get inspiration"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class GetInspirationHandler(AbstractRequestHandler):
    """Handler for Get Inspiration Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetInspirationIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        words = random.sample(wordlist, 3)
        speak_output = "I find three objects for you. The first is: " + words[0] + ". The second is: " + words[1] + ". The third is: " + words[2] + ". Please let me know the object you want to find, such as, find dogs."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class FindArtHandler(AbstractRequestHandler):
    """Handler for Find Art Intent."""
    def searchArt(self, host, word, isHighlight):
        #type: (string, string, bool) -> string
        http = urllib3.PoolManager()
        address = host +"public/collection/v1/search?" + "isHighlight=true&"*isHighlight + "tags=true&q=" + word
        print(address)
        resp = http.request("GET", address)
        if resp.status != 200:
            return "HttpError"
        j = json.loads(resp.data)
        print(resp.data)
        if j["total"] == 0:
            return "ArtNotFound"
        id_list = j["objectIDs"]
        print(id_list)
        return str(random.choice(id_list))
    
    def getArt(self, host, id):
        http = urllib3.PoolManager()
        address = host + "public/collection/v1/objects/" + id
        resp = http.request("GET", address)
        print(address)
        if resp.status != 200:
            return None
        j = json.loads(resp.data)
        return j
    
    def build_speakout(self, art_detail, word):
        object_name = art_detail["objectName"]
        title = art_detail["title"]
        if object_name:
            object_name = re.sub(r'\([^\(\)]*\)','',object_name)
            object_name = object_name.replace('&'," and ")
        if title:
            # alexa has trouble speaking out parentheses
            title = re.sub(r'\([^\(\)]*\)','',title)
            title = title.replace('&'," and ")
        speak_out = "I find an art of {} related to {} in MET museum. It is called {}.".format(object_name, word, title)
        
        return speak_out
    
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("FindArtIntent")(handler_input)
        
    def build_datasource(self, art_detail, word):
        return {
            "artDetail": {
                "imageUrl": art_detail["primaryImageSmall"] if art_detail["primaryImageSmall"] else "https://www.metmuseum.org/-/media/images/visit/plan-your-visit/pyv-marble/original_gh.jpg",
                "title": art_detail["title"],
                "bio": art_detail["artistDisplayName"]+"<br />"+art_detail["artistDisplayBio"]+"<br />"+art_detail["medium"]+"<br />"+art_detail["dimensions"],
                "logoUrl": create_presigned_url("Media/logo_Art_in_Objects.png"),
                "word": word,
                "desc": ""
            }
        }
    
    def build_card(self, art_detail, word):
        text = []
        for item in [art_detail["artistDisplayName"], art_detail["artistDisplayBio"], art_detail["medium"], art_detail["dimensions"]]:
            if item:
                text.append(item)
        text=" | ".join(text)
        return ui.StandardCard(
            title=word.capitalize() + " | " + art_detail["title"],
            text=text,
            image=ui.Image(
                small_image_url=art_detail["primaryImageSmall"],
                large_image_url=art_detail["primaryImageSmall"]
                )
            )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        word = slots["object"].value
        print(word)
        host = "https://collectionapi.metmuseum.org/"
        id = self.searchArt(host, word, False)
        
        if id == "HttpError":
            return (handler_input.response_builder.speak("I have some troubles, please try again later").response)
        if id == "ArtNotFound":
            speak_out = "Sorry we don't have art with this object, please try anohter word."
            return (handler_input.response_builder.speak(speak_out).ask(speak_out).response)
        
        art_detail = self.getArt(host, id)
        if not art_detail:
            return (handler_input.response_builder.speak("I have some troubles, please try again later").response)
        speak_out = self.build_speakout(art_detail, word)
        
        card = self.build_card(art_detail, word)
        ask = "If you want to find another art piece, just say find with its name. If you want to stop, please say stop."
        
        builder = handler_input.response_builder.speak(speak_out + ask).set_card(card).ask(ask)
        if is_APL_supported(handler_input): 
            data = self.build_datasource(art_detail, word)
            
            builder.add_directive(
                    RenderDocumentDirective(
                        token="Token",
                        document=_load_apl_document("ForkTemplate.json"),
                        datasources=data
                    )
                )
        
        return (
            builder.response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say \"find dog\". If you want some inspiration, just say get inspiration"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Thank you for using Art in Objects. Good bye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say 'find dog'. If you want some inspiration, just say get inspiration"
        reprompt = speech

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(GetInspirationHandler())
sb.add_request_handler(FindArtHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()