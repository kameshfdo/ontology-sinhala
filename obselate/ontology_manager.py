import os
import re
from datetime import datetime
from dataclasses import dataclass

from owlready2 import (
    get_ontology,
    Thing,
    DataProperty,  #used to link an individual to a literal value,
    ObjectProperty, #used to link an individual to another individual,
    FunctionalProperty, # a special type of DataProperty or ObjectProperty that can only have one value for each individual
)

# --- Configuration ---
ONTOLOGY_IRI = "http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology"
ONTOLOGY_FILE = "new-ontology.owl"


@dataclass
class FormattedNewsArticle:
    """A data class to hold structured news article information."""
    headline: str
    content: str
    timestamp: datetime
    url: str
    source: str


class OntologyManager:
    def __init__(self, filepath, ontology_iri):
        """
        Initializes the OntologyManager.
        It loads the ontology from the given filepath if it exists,
        otherwise it creates a new one with the specified IRI.
        """
        self.filepath = filepath
        self.ontology_iri = ontology_iri

        if os.path.exists(self.filepath):
            print(f"Loading ontology from '{self.filepath}'...")
            self.ontology = get_ontology(f"file://{self.filepath}").load()
        else:
            print(
                f"File not found. Creating new ontology with IRI: '{self.ontology_iri}'"
            )
            self.ontology = get_ontology(self.ontology_iri)
            self._create_ontology_structure()

    def _create_ontology_structure(self):
        """Defines the classes and properties for a new ontology."""
        print("Defining ontology structure (classes and properties)...")
        with self.ontology:
            # --- Core Classes ---
            class NewsArticle(Thing):
                pass

            class NewsCategory(Thing):
                pass

            class NamedEntity(Thing):
                pass

            class Statement(Thing):
                pass

            class NewsVerb(Thing):
                pass

            class NewsOccurDuration(Thing):  #-- Date/Time: Specifies the date or time of an event or action (e.g., "අද" – "today").
                pass

            # --- mainclass of NewsCategory ---

            class PoliticsAndGovernance(NewsCategory):
                pass

            class ScienceAndTechnology(NewsCategory):
                pass

            class CultureAndEntertainment(NewsCategory):
                pass

            class Sports(NewsCategory):
                pass

            class CrimeAndJustice(NewsCategory):
                pass

            # --- subcategory of main NewsCategory ---
            
            #---1--
            class InternationalPolitics(PoliticsAndGovernance):
                pass
            class DomesticPolitics(PoliticsAndGovernance):
                pass
            #---2--
            class TechAndInnovation(ScienceAndTechnology):
                pass
            class ResearchAndSpace(ScienceAndTechnology):
                pass
            #---3--
            class ScreenAndStage(CultureAndEntertainment):
                pass

            class MusicAndArts(CultureAndEntertainment):
                pass
            #---4--
            class Cricket(Sports):
                pass
            class Football(Sports):
                pass
            class Other(Sports):
                pass
            #---5--
            class CrimeReport(CrimeAndJustice):
                pass
            class CourtsAndInvestigation(CrimeAndJustice):
                pass
 
            # --- Constrained Subclasses of NamedEntity ---
            class Person(NamedEntity):
                pass

            class Organization(NamedEntity):
                pass

            class Location(NamedEntity):
                pass

            class Event(NamedEntity):
                pass

            # --- Data Properties for NewsArticle ---
            class hasTitle(DataProperty, FunctionalProperty):
                range = [str]

            class hasFullText(DataProperty):
                range = [str]

            class hasPublicationDate(DataProperty, FunctionalProperty):
                range = [datetime]

            class hasSourceURL(DataProperty, FunctionalProperty):
                range = [str]

            class processedDate(DataProperty, FunctionalProperty):
                range = [datetime]

            class publisherName(DataProperty):
                range = [str]

            # --- Data Properties for NamedEntity ---
            class canonicalName(DataProperty, FunctionalProperty):
                range = [str]

            class hasAlias(DataProperty):
                range = [str]
            
            class hasAlias(DataProperty):
                range = [str]

            # --- Data Properties for Statement ---
            class hasPredicateVerb(DataProperty, FunctionalProperty):
                range = [str]

            class sourceSentence(DataProperty):
                range = [str]

            # --- Object Properties --- defines a relationship between two individuals
            class hasSubject(ObjectProperty, FunctionalProperty):
                range = [NamedEntity]

            class hasActionVerb(ObjectProperty, FunctionalProperty):
                range = [NewsVerb]

            class hasCategory(ObjectProperty):
                domain=[NewsArticle]
                range = [NewsCategory]

            class mentionsEntity(ObjectProperty):
                range = [NamedEntity]

            class containsStatement(ObjectProperty):
                range = [Statement]

            class hasStatementSubject(ObjectProperty, FunctionalProperty):
                range = [NamedEntity]

            class hasStatementObjectEntity(ObjectProperty, FunctionalProperty):
                range = [NamedEntity]

            class hasStatementObjectLiteral(DataProperty, FunctionalProperty):
                range = [str]
            
            class hasActionVerb(ObjectProperty): #--News Verb: Describes the main action in the news (e.g., "වාර්තා කර තිබේ" – "has been reported", "පවසා ඇති" – "stated").
                range = [NewsVerb]

            class hasLocation(ObjectProperty):
                range = [Location]
            
            class hasNewsOccurDuration(ObjectProperty):
                range = [NewsOccurDuration]
                

            #--relationships between catagory
            #---1. politics and governance---
            #---1.1. International Politics---
            class hasForeignCountry(ObjectProperty): #--Country/Entities Involved: Specifies the countries or entities involved in the news. For example, "ඊශ්‍රායල" (Israel), "ඉරාන" (Iran), "අමෙරිකානු" (American).
                range = [NamedEntity]
            class hasPositionOfRole(ObjectProperty): # -- Position or Role: Could specify the role of the individuals mentioned (e.g., "ජනාධිපති" – "President", "අමෙරිකානු" – "American", "අරබි" – "Arab").
                range = [Person]
            
            #---1.2. Domestic Politics---
            class hasSrilanka(ObjectProperty): #--     
                range = [str]

            #---2. Science and Technology---
            #---2.1. Tech and Innovation---
            class hasTechnology(ObjectProperty): #--Technology: Specifies the technology or innovation being discussed (e.g., "කෘතිම බුද්ධිය" – "Artificial Intelligence", "රොබෝ" – "Robot").
                range = [str]
            
            class hasTechCompany(ObjectProperty): #--Tech Company: Specifies the company or organization involved in the technology (e.g., "ගූගල්" – "Google", "ඇපල්" – "Apple").
                range = [Organization]
            
            class hasTechEvent(ObjectProperty): #--Tech Event: Specifies the event related to the technology (e.g., "කොන්ෆරන්ස්" – "Conference", "සමුළුව" – "Summit").
                range = [Event]
            
            class hasTechPerson(ObjectProperty): #--Tech Person: Specifies the person related to the technology (e.g., "විද්‍යාඥ" – "Scientist", "ඉංජිනේරු" – "Engineer").
                range = [Person]
            
            class hasInnovation(ObjectProperty): #--Innovation: Specifies the innovation being discussed (e.g., "නවෝත්පාදනය" – "Innovation", "අලුත්ම තාක්ෂණය" – "Latest Technology").
                range = [str]
            
            class hasTechImpact(ObjectProperty): #--Impact: Specifies the impact of the technology or innovation (e.g., "සමාජය" – "Society", "ආර්ථිකය" – "Economy").           
                range = [str]

            class hasTechField(ObjectProperty): #--Field: Specifies the field of technology (e.g., "තොරතුරු තාක්ෂණය" – "Information Technology", "ජීව විද්‍යාව" – "Biotechnology").
                range = [str]
            


            #---2.2. Research and Space---

            class hasResearchTopic(ObjectProperty): #--Research Topic: Specifies the topic of research (e.g., "ජීව විද්‍යාව" – "Biology", "භූ විද්‍යාව" – "Geology").
                range = [str]
            
            class hasResearchInstitution(ObjectProperty): #--Research Institution: Specifies the institution conducting the research (e.g., "විශ්ව විද්‍යාලය" – "University", "ගවේෂණාගාරය" – "Research Center").
                range = [Organization]
            
            class hasResearchPerson(ObjectProperty): #--Research Person: Specifies the person conducting the research (e.g., "ගවේෂක" – "Researcher", "විද්‍යාඥ" – "Scientist").
                range = [Person]
            
            class hasResearchFunding(ObjectProperty): #--Funding: Specifies the funding source for the research (e.g., "රජයේ" – "Government", "පෞද්ගලික" – "Private").
                range = [Organization]

            class hasSpaceMission(ObjectProperty): #--Space Mission: Specifies the space mission being discussed (e.g., "අභ්‍යවකාශ යානය" – "Spacecraft", "රොකට්" – "Rocket").
                range = [str]

            class hasSpaceAgency(ObjectProperty): #--Space Agency: Specifies the space agency involved (e.g., "NASA", "ඇසෝස්" – "ESA").
                range = [Organization]  
            
            class hasSpaceDiscovery(ObjectProperty): #--Discovery: Specifies the discovery made in space (e.g., "නව ග්‍රහලෝකය" – "New Planet", "අභ්‍යවකාශයේ සොයා ගැනීම" – "Space Discovery").
                range = [str]
            
            class hasSpaceEquivement(ObjectProperty):  #--Equipment: Specifies the equipment used in space exploration (e.g., "රොබෝ" – "Robot", "කැමරා" – "Camera").
                range = [str]  


            #---3. Culture and Entertainment---
            class hasEventType(ObjectProperty): #--Event Type: Specifies the type of cultural or entertainment event (e.g., "සංගීත" – "Music", "චිත්‍රපට" – "Film").
                range = [str]

            class hasArtform(ObjectProperty): #--Art Form: Specifies the form of art being discussed (e.g., "චිත්‍රකලාව" – "Painting", "සංගීතය" – "Music").
                range = [str]

            class hasVenue(ObjectProperty): #--Venue: Specifies the venue of the event (e.g., "කලාපිටිය" – "Art Gallery", "සංගීත ශාලාව" – "Concert Hall").
                range = [str]
            
            class hasAwards(ObjectProperty): #--Awards: Specifies the awards won by the film (e.g., "ඔස්කාර්" – "Oscar", "ගෝල්ඩන් ග්ලෝබ්" – "Golden Globe").
                range = [str]

            #---3.1. Screen and Stage---

            class hasFilmGenre(ObjectProperty): #--Film Genre: Specifies the genre of the film (e.g., "ක්‍රියාදාම" – "Action", "රොමෑන්තික" – "Romantic").
                range = [str]
            
            class hasFilmDirector(ObjectProperty): #--Film Director: Specifies the director of the film (e.g., "අධ්‍යක්ෂ" – "Director", "නළුවා" – "Actor").
                range = [Person]

            class hasFilmProductionCompany(ObjectProperty): #--Production Company: Specifies the production company of the film (e.g., "හොලිවුඩ්" – "Hollywood", "බොලිවුඩ්" – "Bollywood").
                range = [Organization]
            
            class hasFilmReleaseDate(ObjectProperty): #--Release Date: Specifies the release date of the film (e.g., "නවම්බර් 2025" – "November 2025").
                range = [datetime]
            
            
            
            class hasFilmCast(ObjectProperty): #--Cast: Specifies the cast of the film (e.g., "නළුවා" – "Actor", "නළිය" – "Actress").
                range = [Person]



            #---3.2. Music and Arts---

            class hasMusicGenre(ObjectProperty): #--Music Genre: Specifies the genre of music (e.g., "රොක්" – "Rock", "ජාතික" – "Folk").
                range = [str]
            
            class hasMusicArtist(ObjectProperty): #--Music Artist: Specifies the artist or band (e.g., "ගායක" – "Singer", "බෑන්ඩ්" – "Band").
                range = [Person]
            
            class hasMusicAlbum(ObjectProperty): #--Music Album: Specifies the album of the music (e.g., "ඇල්බමය" – "Album", "සංගීත කට්ටලය" – "Music Collection").
                range = [str]

            class hasArtExhibition(ObjectProperty): #--Art Exhibition: Specifies the art exhibition being discussed (e.g., "චිත්‍රකලාව" – "Painting", "කලාපිටිය" – "Art Gallery").
                range = [str]
        
            class mediaCoverage(ObjectProperty): #--Media Coverage: Specifies the media coverage of the event (e.g., "පුවත්පත" – "Newspaper", "රූපවාහිනී" – "Television").
                range = [str]
            
            class hasArtisticStyle(ObjectProperty): #--Artistic Style: Specifies the style of art (e.g., "අභිප්‍රේරණය" – "Impressionism", "අබ්ස්ට්‍රැක්ට්" – "Abstract").
                range = [str]
            



            #---4. Sports---
            class hasSportType(ObjectProperty): #--Sport Type: Specifies the type of sport being discussed (e.g., "ක්‍රිකට්" – "Cricket", "පැදුරු ක්‍රීඩා" – "Motor Sports").
                range = [str]
            
            class hasSportEvent(ObjectProperty): #--Sport Event: Specifies the event related to the sport (e.g., "ලෝක කුසලාන" – "World Cup", "ආසියානු ක්‍රීඩා" – "Asian Games").
                range = [str]
            
            class hasSportLocation(ObjectProperty): #--Sport Location: Specifies the location of the sport event (e.g., "ක්‍රීඩාංගනය" – "Stadium", "මහේල මාලිගාව" – "Mahinda Rajapaksa Stadium").
                range = [str]
            
            class hasEventDate(ObjectProperty): #--Event Date: Specifies the date of the sport event (e.g., "ජූනි 2025" – "June 2025").
                range = [datetime]

            #---4.1. Cricket---

            class hasCricketMatch(ObjectProperty): #--Cricket Match: Specifies the cricket match being discussed (e.g., "ලෝක කුසලාන" – "World Cup", "අන්තර්ජාතික තරගය" – "International Match").
                range = [str]
            
            class hasCricketTeam(ObjectProperty): #--Cricket Team: Specifies the cricket team being discussed (e.g., "ශ්‍රී ලංකා කණ්ඩායම" – "Sri Lanka Team", "ඉන්දීය කණ්ඩායම" – "India Team").
                range = [Organization]
            
            class hasCricketPlayer(ObjectProperty): #--Cricket Player: Specifies the cricket player being discussed (e.g., "කණ්ඩායම් නායකයා" – "Team Captain", "ඉන්දීය ක්‍රීඩකයා" – "Indian Player").
                range = [Person]
            
            class hasCricketVenue(ObjectProperty): #--Cricket Venue: Specifies the venue of the cricket match (e.g., "ක්‍රිකට් ක්‍රීඩාංගනය" – "Cricket Stadium", "මහේල මාලිගාව" – "Mahinda Rajapaksa Stadium").
                range = [str]
            
            class hasCricketTournament(ObjectProperty): #--Cricket Tournament: Specifies the cricket tournament being discussed (e.g., "ලෝක කුසලාන" – "World Cup", "අන්තර්ජාතික තරගය" – "International Match").
                range = [str]
            
            class hasCricketScore(ObjectProperty): #--Cricket Score: Specifies the score of the cricket match (e.g., "රන්" – "Runs", "ඉන්ඩි" – "Innings").
                range = [str]
            
            class hasCricketUmpire(ObjectProperty): #--Cricket Umpire: Specifies the umpire of the cricket match (e.g., "අධිකාරියා" – "Umpire", "නිර්ණායකයා" – "Referee").
                range = [Person]
            
            class hasCricketCommentary(ObjectProperty): #--Cricket Commentary: Specifies the commentary of the cricket match (e.g., "සජීවී විකාශනය" – "Live Broadcast", "විචාරකයා" – "Commentator").
                range = [str]
            



            #---4.2. Football---

            class hasFootballMatch(ObjectProperty): #--Football Match: Specifies the football match being discussed (e.g., "ලෝක කුසලාන" – "World Cup", "ආසියානු කුසලාන" – "Asian Cup").
                range = [str]

            class hasFootballTeam(ObjectProperty): #--Football Team: Specifies the football team being discussed (e.g., "ශ්‍රී ලංකා කණ්ඩායම" – "Sri Lanka Team", "ඉන්දීය කණ්ඩායම" – "India Team").
                range = [Organization]
            
            class hasFootballPlayer(ObjectProperty): #--Football Player: Specifies the football player being discussed (e.g., "කණ්ඩායම් නායකයා" – "Team Captain", "ඉන්දීය ක්‍රීඩකයා" – "Indian Player").
                range = [Person]
            
            class hasFootballVenue(ObjectProperty): #--Football Venue: Specifies the venue of the football match (e.g., "ෆුට්බෝල් ක්‍රීඩාංගනය" – "Football Stadium", "මහේල මාලිගාව" – "Mahinda Rajapaksa Stadium").
                range = [str]

            class hasFootballTournament(ObjectProperty): #--Football Tournament: Specifies the football tournament being discussed (e.g., "ලෝක කුසලාන" – "World Cup", "ආසියානු කුසලාන" – "Asian Cup").
                range = [str]
            
            class hasFootballScore(ObjectProperty): #--Football Score: Specifies the score of the football match (e.g., "ගෝල්" – "Goals", "ඉන්ඩි" – "Innings").
                range = [str]
            
            class hasFootballReferee(ObjectProperty): #--Football Referee: Specifies the referee of the football match (e.g., "අධිකාරියා" – "Referee", "නිර්ණායකයා" – "Umpire").
                range = [Person]
            
            class hasFootballCommentary(ObjectProperty): #--Football Commentary: Specifies the commentary of the football match (e.g., "සජීවී විකාශනය" – "Live Broadcast", "විචාරකයා" – "Commentator").
                range = [str]
            
            class hasFootballLeague(ObjectProperty): #--Football League: Specifies the football league being discussed (e.g., "ප්‍රිමියර් ලීග්" – "Premier League", "ලාලිගා" – "La Liga").
                range = [str]
            
            class hasFootballPlayerStatistics(ObjectProperty): #--Player Statistics: Specifies the statistics of the football player (e.g., "ගෝල්" – "Goals", "ඉන්ඩි" – "Innings").
                range = [str]

            

            #---4.3. Other---

            class hasOtherSportType(ObjectProperty): #--Other Sport Type: Specifies the type of other sport being discussed (e.g., "බේස්බෝල්" – "Baseball", "හොකී" – "Hockey").
                range = [str]
            



            #---5. Crime and Justice---
            class hasWitnessStatement(ObjectProperty): #--Witness Statement: Specifies the statement given by a witness (e.g., "සහයෝගී" – "Cooperator", "සහයෝගීයා" – "Witness").
                range = [str]
            class hasWitness(ObjectProperty): #--Witness: Specifies the witness of the crime (e.g., "සහයෝගී" – "Cooperator", "සහයෝගීයා" – "Witness").
                range = [Person]
            
            class hasInvestigation(ObjectProperty): #--Investigation: Specifies the agency conducting the investigation (e.g., "පොලිසිය" – "Police", "අධිකාරිය" – "Authority").
                range = [Organization]

            class hasCase(ObjectProperty): #--Case: Specifies the court case related to the crime (e.g., "අධිකරණය" – "Court", "අධිකාරිය" – "Authority").
                range = [str]

            class hasEvidence(ObjectProperty): #--Crime or court Evidence: Specifies the evidence related to the crime (e.g., "සහයෝගී" – "Cooperator", "සහයෝගීයා" – "Witness").
                range = [str]

            class hasVictim(ObjectProperty): #--Victim: Specifies the victim of the crime (e.g., "පීඩිතයා" – "Victim", "අත්හිටුවා ඇති" – "Arrested").
                range = [Person]

            #---5.1. Crime Report---

            class hasCrimeType(ObjectProperty): #--Crime Type: Specifies the type of crime being reported (e.g., "අත්හිටුවීම" – "Arrest", "අත්‍යචාරය" – "Assault").
                range = [str]
            
            class hasCrimeLocation(ObjectProperty): #--Crime Location: Specifies the location of the crime (e.g., "නගරය" – "City", "පොලිසිය" – "Police Station").
                range = [Location]
            
            class hasCrimeDate(ObjectProperty): #--Crime Date: Specifies the date of the crime (e.g., "ජූනි 2025" – "June 2025").
                range = [datetime]

            class hasCrimeSuspect(ObjectProperty): #--Crime Suspect: Specifies the suspect of the crime (e.g., "අත්හිටුවා ඇති" – "Arrested", "අත්‍යචාරකයා" – "Assailant").
                range = [Person]
            

            #---5.2. Courts and Investigation---

            class hasCourtCase(ObjectProperty): #--Court Case: Specifies the court case related to the crime (e.g., "අධිකරණය" – "Court", "අධිකාරිය" – "Authority").
                range = [str]

            class hasCourtVerdict(ObjectProperty): #--Court Verdict: Specifies the verdict of the court case (e.g., "අධිකරණය" – "Court", "අධිකාරිය" – "Authority").
                range = [str]
            
            class hasCourtJudge(ObjectProperty): #--Court Judge: Specifies the judge of the court case (e.g., "අධිකරණය" – "Court", "අධිකාරිය" – "Authority").
                range = [Person]
            
            class hasCourtHearingDate(ObjectProperty): #--Hearing Date: Specifies the date of the court hearing (e.g., "ජූනි 2025" – "June 2025").
                range = [datetime]


        print("Ontology structure defined successfully.")
     

    def _get_safe_name(self, name):
        """Creates a safe name for an ontology individual."""
        name = re.sub(r"^https?://", "", name)
        return re.sub(r"[^a-zA-Z0-9_]", "_", name)

    def addNewsToOntology(self, article: FormattedNewsArticle):
        """
        Adds a news article to the ontology as a new individual, populating
        its properties from the provided article object.
        """
        with self.ontology:
            article_name = self._get_safe_name(article.url)
            news_individual = self.ontology.NewsArticle(article_name)

            # Use assignment (=) for Functional Properties
            news_individual.hasTitle = article.headline
            news_individual.hasPublicationDate = article.timestamp
            news_individual.hasSourceURL = article.url
            news_individual.processedDate = datetime.now()

            # Use .append() for non-functional properties
            news_individual.hasFullText.append(article.content)
            news_individual.publisherName.append(article.source)

        print(f"Added news article individual: '{article_name}'")
        return news_individual

    def save(self, format="rdfxml"):
        """Saves the ontology to the file specified during initialization."""
        self.ontology.save(file=self.filepath, format=format)
        print(f"Ontology successfully saved to '{self.filepath}'")


# --- Example Usage ---
if __name__ == "__main__":
    manager = OntologyManager(ONTOLOGY_FILE, ONTOLOGY_IRI)
    onto = manager.ontology

    sample_article = FormattedNewsArticle(
        headline="AI Conference Announces Major Breakthroughs",
        content="Scientists at the annual AI summit revealed new models...",
        timestamp=datetime(2025, 6, 8, 14, 30, 0),
        url="http://news.example.com/ai-breakthrough-2025",
        source="Example News",
    )

    manager.addNewsToOntology(sample_article)

    print("\nCurrent NewsArticle individuals in the ontology:")
    for instance in onto.NewsArticle.instances():
        print(f"- {instance.name}")
        # You can now access its properties correctly
        print(f"  Title: {instance.hasTitle}")

    manager.save()