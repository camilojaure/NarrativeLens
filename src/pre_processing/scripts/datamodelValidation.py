from pydantic import BaseModel, validator
from enum import Enum
import json

class CreativeTheme(str, Enum):
    PRODUCT_CENTRIC = "Product-Centric"
    LIFESTYLE_ASPIRATIONAL = "Lifestyle & Aspirational"
    TESTIMONIAL_SOCIAL_PROOF = "Testimonial & Social Proof"
    EDUCATIONAL_EXPLAINER = "Educational & Explainer"
    PROMOTIONAL_OFFER_BASED = "Promotional & Offer-Based"
    HUMOR_ENTERTAINMENT = "Humor & Entertainment"
    BRAND_STORY_MISSION_DRIVEN = "Brand Story & Mission-Driven"
    TREND_BASED_REACTIVE = "Trend-Based & Reactive"
    NOT_APPLICABLE = "Not Applicable"

class CreativeConcept(str, Enum):
    DAY_IN_THE_LIFE = "Day-in-the-life story"
    PRODUCT_DEMO = "Product demo"
    EXPERT_REVIEW = "Expert review"
    ANIMATED_EXPLAINER = "Animated explainer"
    LIMITED_TIME_OFFER = "Limited-time offer"
    MEME_BASED = "Meme-based content"
    FOUNDER_STORY = "Founder story"
    BEHIND_THE_SCENES = "Behind-the-scenes"
    COMPARISON = "Comparison"
    UNBOXING = "Unboxing"
    CINEMATIC_BRAND_FILM = "Cinematic brand film"
    ASPIRATIONAL_CREATOR = "Aspirational creator collaboration"
    BEFORE_AND_AFTER = "Before-and-after story"
    MYTH_BUSTING = "Myth-busting"
    FAQ = "FAQ"
    FLASH_SALE = "Flash sale"
    COUNTDOWN_TIMER = "Countdown timer"
    MEMBER_DEAL = "Member deal"
    PARODY = "Parody"
    SATIRE = "Satire"
    REAL_TIME_REACTIVE = "Real-time reactive"
    TRENDING_CREATOR = "Trending creator collaboration"
    EVENT_DRIVEN = "Event-driven"
    UGC = "User-generated content (UGC)"
    NONE = "None"
    NOT_APPLICABLE = "Not Applicable"

class FormatProductionStyle(str, Enum):
    STATIC_IMAGE = "Static Image"
    CAROUSEL = "Carousel"
    NATIVE_VIDEO = "Native Video"
    HIGH_PRODUCTION_VIDEO = "High-Production Video"
    ANIMATION_MOTION_GRAPHICS = "Animation & Motion Graphics"
    SHOPPABLE_AD = "Shoppable Ad"
    DYNAMIC_CREATIVE = "Dynamic Creative"
    POLL = "Poll"
    QUIZ = "Quiz"
    GAMIFIED_EXPERIENCE = "Gamified Experience"
    UNCLEAR = "Unclear"

class TalentType(str, Enum):
    ACTORS = "Actors"
    INFLUENCERS = "Influencers"
    CUSTOMERS = "Customers"
    EXPERTS = "Experts"
    ACTORS_CUSTOMERS = "Combination of actors and customers"
    INFLUENCERS_CUSTOMERS = "Combination of influencers and customers"
    NONE = "None"
    UNCLEAR = "Unclear"

class DemographicRepresentation(str, Enum):
    YOUNG_ADULTS = "Primarily Young Adults"
    MIDDLE_AGED_ADULTS = "Primarily Middle-Aged Adults"
    OLDER_ADULTS = "Primarily Older Adults"
    DIVERSE_AGE_RANGE = "Diverse Age Range"
    PRIMARILY_MALE = "Primarily Male"
    PRIMARILY_FEMALE = "Primarily Female"
    DIVERSE_GENDER = "Diverse Gender Representation"
    PRIMARILY_WHITE = "Primarily White"
    PRIMARILY_BLACK = "Primarily Black/African American"
    PRIMARILY_ASIAN = "Primarily Asian"
    PRIMARILY_HISPANIC = "Primarily Hispanic/Latino"
    DIVERSE_ETHNICITY = "Diverse Ethnic Representation"
    UNCLEAR = "Unclear"
    NO_PEOPLE = "No People Featured"

class AudienceFocus(str, Enum):
    UNAWARE = "Unaware Audience"
    PROBLEM_AWARE = "Problem Aware"
    SOLUTION_AWARE = "Solution Aware"
    PRODUCT_AWARE = "Product Aware"
    MOST_AWARE = "Most Aware"
    UNCLEAR = "Unclear"

class CampaignObjective(str, Enum):
    AWARENESS = "Awareness"
    TRAFFIC = "Traffic"
    ENGAGEMENT = "Engagement"
    LEADS = "Leads"
    APP_PROMOTION = "App Promotion"
    SALES = "Sales"
    UNCLEAR = "Unclear"

class AdAnalysis(BaseModel):
    creative_theme: CreativeTheme
    creative_concept: CreativeConcept
    format_production_style: FormatProductionStyle
    talent_type: TalentType
    demographic_representation: DemographicRepresentation
    audience_focus: AudienceFocus
    campaign_objective: CampaignObjective