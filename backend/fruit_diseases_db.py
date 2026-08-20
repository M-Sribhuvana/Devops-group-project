"""
Fruit Crop Disease Database
Contains comprehensive agricultural diagnostic data for common fruit crop diseases.
Covers Apple, Grape, Peach, Strawberry, Cherry, and Citrus/Orange crops.
"""

FRUIT_DISEASE_DB = {
    "apple_scab": {
        "id": "apple_scab",
        "display_name": "Apple Scab",
        "crop_type": "Apple (Malus domestica)",
        "scientific_name": "Venturia inaequalis",
        "status": "Diseased",
        "severity": "High",
        "description": "A serious fungal disease that affects apple leaves and fruit, causing olive-green to dark brown velvet-like lesions, premature leaf drop, and deformed fruit.",
        "symptoms": [
            "Olive-green velvet-like spots on upper leaf surfaces.",
            "Lesions turning dark brown or black with raised borders.",
            "Yellowing leaves surrounding lesions followed by early leaf drop.",
            "Scabby, cracked lesions on young developing apples."
        ],
        "organic_remedies": [
            "Apply neem oil or sulfur-based organic fungicide at bud break.",
            "Prune canopy tree branches to enhance sunlight penetration and airflow.",
            "Rake and destroy fallen infected leaves in autumn to disrupt fungal overwintering spores."
        ],
        "chemical_treatments": [
            "Apply Myclobutanil or Captan fungicide at tight cluster stage.",
            "Use Dithianon or Mancozeb sprays during high moisture spring infection periods.",
            "Rotate fungicide groups (FRAC codes) to avoid pathogen chemical resistance."
        ],
        "prevention": [
            "Plant scab-resistant apple cultivars such as Honeycrisp, Enterprise, or Liberty.",
            "Maintain wide tree spacing (4-5 meters) to ensure dry foliage.",
            "Avoid overhead sprinkler irrigation; use drip irrigation systems at ground level."
        ],
        "recommended_irrigation": "Drip irrigation early morning. Keep leaves dry.",
        "npk_fertilizer_tip": "Avoid excessive nitrogen fertilizers, which spur tender susceptible growth."
    },

    "apple_black_rot": {
        "id": "apple_black_rot",
        "display_name": "Apple Black Rot (Frog-Eye Leaf Spot)",
        "crop_type": "Apple (Malus domestica)",
        "scientific_name": "Botryosphaeria obtusa",
        "status": "Diseased",
        "severity": "High",
        "description": "Fungal pathogen producing distinct 'frog-eye' purple-bordered spots on leaves, cankers on branches, and black, mummified rot on ripening fruit.",
        "symptoms": [
            "Small purple spots expanding into circular tan spots with purple margins (frog-eye pattern).",
            "Sunken, dark reddish-brown cankers on twigs and limbs.",
            "Fruit developing concentric rings of dark rot, eventually mummifying on branches."
        ],
        "organic_remedies": [
            "Prune out all dead or cankered wood during dormant winter pruning.",
            "Remove mummified apples remaining on the tree or orchard floor.",
            "Apply bio-fungicides containing Bacillus subtilis during leaf flushing."
        ],
        "chemical_treatments": [
            "Fungicide sprays with Thiophanate-methyl combined with Captan.",
            "Apply Copper hydroxide early before bloom for overwintered spore control."
        ],
        "prevention": [
            "Sanitize pruning shears between cuts using 70% isopropyl alcohol.",
            "Minimize tree injury from hail or improper pruning cuts."
        ],
        "recommended_irrigation": "Ground drip or micro-sprinkler.",
        "npk_fertilizer_tip": "Maintain balanced N-P-K (10-10-10) to promote bark tissue health."
    },

    "apple_cedar_rust": {
        "id": "apple_cedar_rust",
        "display_name": "Cedar Apple Rust",
        "crop_type": "Apple (Malus domestica)",
        "scientific_name": "Gymnosporangium juniperi-virginianae",
        "status": "Diseased",
        "severity": "Medium",
        "description": "A heteroecious fungal rust requiring Eastern Red Cedar (juniper) and apple trees to complete its life cycle, producing bright yellow-orange leaf spots.",
        "symptoms": [
            "Bright orange-yellow leaf spots on upper leaf surfaces in late spring.",
            "Small black dots (pycnidia) inside orange spots.",
            "Tube-like fungal structures (aecia) on leaf undersides emitting spores."
        ],
        "organic_remedies": [
            "Remove nearby Eastern Red Cedar or juniper host plants within 500 meters.",
            "Apply liquid sulfur sprays at pink bud stage."
        ],
        "chemical_treatments": [
            "Apply Sterol Inhibitors (SI) such as Myclobutanil or Propiconazole from pink bud through petal fall."
        ],
        "prevention": [
            "Select resistant varieties (e.g., Red Delicious, Empire, Freedom)."
        ],
        "recommended_irrigation": "Sub-surface irrigation.",
        "npk_fertilizer_tip": "Balanced slow-release potassium to strengthen cell walls."
    },

    "apple_healthy": {
        "id": "apple_healthy",
        "display_name": "Apple - Healthy Leaf",
        "crop_type": "Apple (Malus domestica)",
        "scientific_name": "N/A",
        "status": "Healthy",
        "severity": "None",
        "description": "Vibrant green, unblemished apple leaf exhibiting strong photosynthetic capacity, clean serrated leaf margins, and robust cellular structure.",
        "symptoms": ["No disease symptoms detected. Leaves are lush green and intact."],
        "organic_remedies": ["Continue good horticultural practices and organic compost application."],
        "chemical_treatments": ["No chemical treatment required."],
        "prevention": [
            "Inspect foliage weekly for early pest or fungal signs.",
            "Maintain soil mulch and balanced organic matter."
        ],
        "recommended_irrigation": "Standard 25-30mm per week based on weather conditions.",
        "npk_fertilizer_tip": "Apply balanced organic fertilizer (e.g. 5-5-5) in early spring."
    },

    "grape_black_rot": {
        "id": "grape_black_rot",
        "display_name": "Grape Black Rot",
        "crop_type": "Grape (Vitis vinifera)",
        "scientific_name": "Guignardia bidwellii",
        "status": "Diseased",
        "severity": "Critical",
        "description": "Destructive fungal disease of grapevines capable of destroying up to 100% of the crop under warm, humid conditions.",
        "symptoms": [
            "Small reddish-brown circular spots on leaves with dark borders.",
            "Tiny black spore specks (pycnidia) inside spots.",
            "Grapes turn brown, shrivel into hard, black mummified berries."
        ],
        "organic_remedies": [
            "Apply copper octanoate or sulfur early in spring.",
            "Prune for open canopy leaf ventilation (canopy shoot thinning)."
        ],
        "chemical_treatments": [
            "Mancozeb, Ziram, or Strobilurin (Azoxystrobin) applications from pre-bloom to 4 weeks post-bloom."
        ],
        "prevention": [
            "Remove all mummified fruit clusters during winter pruning."
        ],
        "recommended_irrigation": "Drip lines under canopy.",
        "npk_fertilizer_tip": "Potassium supplementation promotes sugar translocation and berry firmness."
    },

    "grape_esca": {
        "id": "grape_esca",
        "display_name": "Grape Esca (Black Measles)",
        "crop_type": "Grape (Vitis vinifera)",
        "scientific_name": "Phaeomoniella chlamydospora",
        "status": "Diseased",
        "severity": "High",
        "description": "Complex grapevine trunk disease causing 'tiger-stripe' leaf chlorosis and necrosis alongside spotted, dark fruit berries.",
        "symptoms": [
            "Interveinal leaf yellowing and reddish-brown necrosis ('tiger stripe' pattern).",
            "Dark purple specks ('black measles') on grape berries.",
            "Internal trunk wood cross-sections showing brown vascular streaking."
        ],
        "organic_remedies": [
            "Paint winter pruning wounds with Trichoderma-based bio-protectants."
        ],
        "chemical_treatments": [
            "Apply wound sealing paints containing pyraclostrobin or tebuconazole post-pruning."
        ],
        "prevention": [
            "Avoid pruning in wet weather to prevent airborne fungal entry."
        ],
        "recommended_irrigation": "Regulated deficit irrigation.",
        "npk_fertilizer_tip": "Ensure adequate micronutrients (Zinc, Boron, Magnesium)."
    },

    "grape_leaf_blight": {
        "id": "grape_leaf_blight",
        "display_name": "Grape Leaf Blight",
        "crop_type": "Grape (Vitis vinifera)",
        "scientific_name": "Pseudocercospora vitis",
        "status": "Diseased",
        "severity": "Medium",
        "description": "Fungal leaf spot disease causing dark olive spots that merge into extensive leaf necrosis, leading to early leaf drop.",
        "symptoms": [
            "Irregular reddish-brown lesions bounded by leaf veins.",
            "Dark olive-green fuzzy fungal growth on leaf undersides."
        ],
        "organic_remedies": [
            "Bordeaux mixture (Copper sulfate + hydrated lime) post-harvest."
        ],
        "chemical_treatments": [
            "Foliar sprays of Chlorothalonil or Copper Oxychloride."
        ],
        "prevention": [
            "Rake and bury infected fallen leaves."
        ],
        "recommended_irrigation": "Drip irrigation.",
        "npk_fertilizer_tip": "Sufficient Calcium to strengthen cell membranes."
    },

    "grape_healthy": {
        "id": "grape_healthy",
        "display_name": "Grape - Healthy Leaf",
        "crop_type": "Grape (Vitis vinifera)",
        "scientific_name": "N/A",
        "status": "Healthy",
        "severity": "None",
        "description": "Clean green grapevine leaf with intact lobed structure and healthy vascular vein network.",
        "symptoms": ["No signs of chlorosis, spots, or fungal growth."],
        "organic_remedies": ["Maintain organic vineyard compost tea sprays."],
        "chemical_treatments": ["None required."],
        "prevention": ["Routine trellis pruning and weeding."],
        "recommended_irrigation": "Drip irrigation twice weekly.",
        "npk_fertilizer_tip": "Magnesium and Iron for photosynthesis."
    },

    "peach_bacterial_spot": {
        "id": "peach_bacterial_spot",
        "display_name": "Peach Bacterial Spot",
        "crop_type": "Peach (Prunus persica)",
        "scientific_name": "Xanthomonas arboricola pv. pruni",
        "status": "Diseased",
        "severity": "High",
        "description": "Bacterial infection causing angular purplish-black leaf lesions that drop out leaving a 'shot-hole' appearance, alongside pitted fruit skin.",
        "symptoms": [
            "Small water-soaked angular leaf spots turning purple-black.",
            "Center of leaf spots falling out, creating a shot-hole pattern.",
            "Pitted, cracked brown skin on peaches."
        ],
        "organic_remedies": [
            "Spray copper hydroxide at dormant stage.",
            "Plant windbreaks to prevent storm-induced leaf micro-wounds."
        ],
        "chemical_treatments": [
            "Oxytetracycline or bactericidal copper formulations during cover sprays."
        ],
        "prevention": [
            "Plant bacterial spot resistant peach varieties (e.g. Bounty, Candor)."
        ],
        "recommended_irrigation": "Under-canopy drip.",
        "npk_fertilizer_tip": "Avoid excess spring Nitrogen."
    },

    "peach_healthy": {
        "id": "peach_healthy",
        "display_name": "Peach - Healthy Leaf",
        "crop_type": "Peach (Prunus persica)",
        "scientific_name": "N/A",
        "status": "Healthy",
        "severity": "None",
        "description": "Elongated lanceolate green leaf with smooth surface and crisp tips.",
        "symptoms": ["Leaf tissue clean, unblemished green."],
        "organic_remedies": ["Standard organic compost mulch."],
        "chemical_treatments": ["None required."],
        "prevention": ["Regular pest monitoring."],
        "recommended_irrigation": "Deep root watering.",
        "npk_fertilizer_tip": "Balanced spring fertilization."
    },

    "strawberry_leaf_scorch": {
        "id": "strawberry_leaf_scorch",
        "display_name": "Strawberry Leaf Scorch",
        "crop_type": "Strawberry (Fragaria × ananassa)",
        "scientific_name": "Diplocarpon earlianum",
        "status": "Diseased",
        "severity": "Medium",
        "description": "Fungal leaf disease producing purplish spots that expand until the entire leaf appears scorched by drought or fire.",
        "symptoms": [
            "Dark purple irregular spots on leaves.",
            "Centers of spots turning brown while margins remain purple.",
            "Entire leaf drying out, curling upward, and taking on a burnt appearance."
        ],
        "organic_remedies": [
            "Remove older infected leaves immediately.",
            "Apply potassium bicarbonate sprays."
        ],
        "chemical_treatments": [
            "Captan or Pyraclostrobin sprays during renovation."
        ],
        "prevention": [
            "Use straw mulch to minimize splash dispersal of fungal spores."
        ],
        "recommended_irrigation": "Drip tape under plastic mulch.",
        "npk_fertilizer_tip": "Avoid heavy Nitrogen during fruiting phase."
    },

    "strawberry_healthy": {
        "id": "strawberry_healthy",
        "display_name": "Strawberry - Healthy Leaf",
        "crop_type": "Strawberry (Fragaria × ananassa)",
        "scientific_name": "N/A",
        "status": "Healthy",
        "severity": "None",
        "description": "Trifoliate deep green strawberry leaf with serrated margins and vibrant tissue.",
        "symptoms": ["Healthy foliage."],
        "organic_remedies": ["Maintain clean pine/straw mulch."],
        "chemical_treatments": ["None required."],
        "prevention": ["Weed control."],
        "recommended_irrigation": "Drip irrigation.",
        "npk_fertilizer_tip": "High Potassium for berry sweetness."
    },

    "cherry_powdery_mildew": {
        "id": "cherry_powdery_mildew",
        "display_name": "Cherry Powdery Mildew",
        "crop_type": "Cherry (Prunus avium)",
        "scientific_name": "Podosphaera clandestina",
        "status": "Diseased",
        "severity": "Medium",
        "description": "Fungal infection forming powdery white patches of mycelium on leaves and green fruit stems.",
        "symptoms": [
            "White dusty powder coating on young leaves.",
            "Curled leaf margins and stunted terminal shoots."
        ],
        "organic_remedies": [
            "Apply potassium bicarbonate, neem oil, or horticultural oils."
        ],
        "chemical_treatments": [
            "Tebuconazole, Quinoxyfen, or Sulfur fungicides."
        ],
        "prevention": [
            "Prune dense canopy shoots for maximum solar penetration."
        ],
        "recommended_irrigation": "Overhead avoided; use micro-jets near trunk.",
        "npk_fertilizer_tip": "Balanced organic NPK."
    },

    "cherry_healthy": {
        "id": "cherry_healthy",
        "display_name": "Cherry - Healthy Leaf",
        "crop_type": "Cherry (Prunus avium)",
        "scientific_name": "N/A",
        "status": "Healthy",
        "severity": "None",
        "description": "Broad oval glossy green cherry leaf with prominent veins and clean petiole.",
        "symptoms": ["No disease marks."],
        "organic_remedies": ["Organic mulch around drip line."],
        "chemical_treatments": ["None."],
        "prevention": ["Winter sanitation."],
        "recommended_irrigation": "Deep soil soaking.",
        "npk_fertilizer_tip": "Spring nitrogen boost."
    },

    "citrus_greening": {
        "id": "citrus_greening",
        "display_name": "Citrus Greening (Huanglongbing / HLB)",
        "crop_type": "Citrus / Orange (Citrus sinensis)",
        "scientific_name": "Candidatus Liberibacter asiaticus",
        "status": "Diseased",
        "severity": "Critical",
        "description": "Incurable bacterial disease transmitted by Asian Citrus Psyllids, causing blotchy mottle chlorosis, bitter lopsided fruit, and eventual tree decline.",
        "symptoms": [
            "Asymmetrical blotchy yellow mottle across leaf veins.",
            "Yellow shoots (huanglongbing = yellow dragon disease).",
            "Small, lopsided green fruit with bitter, dark seeds."
        ],
        "organic_remedies": [
            "Control Asian Citrus Psyllid vector with kaolin clay sprays and neem oil.",
            "Apply nutritional foliar sprays (Zinc, Manganese, Boron) to sustain tree life."
        ],
        "chemical_treatments": [
            "Systemic insecticides (Imidacloprid, Thiamethoxam) to manage psyllid populations."
        ],
        "prevention": [
            "Plant certified disease-free nursery trees under protective screen houses."
        ],
        "recommended_irrigation": "Micro-drip with fertigation.",
        "npk_fertilizer_tip": "Frequent micro-nutrient foliar feeds."
    },

    "citrus_healthy": {
        "id": "citrus_healthy",
        "display_name": "Citrus - Healthy Leaf",
        "crop_type": "Citrus / Orange (Citrus sinensis)",
        "scientific_name": "N/A",
        "status": "Healthy",
        "severity": "None",
        "description": "Glossy dark green citrus leaf with distinct winged petiole and citrus oil glands.",
        "symptoms": ["Healthy glossy leaf tissue."],
        "organic_remedies": ["Compost tea."],
        "chemical_treatments": ["None."],
        "prevention": ["Psyllid monitoring sticky traps."],
        "recommended_irrigation": "Regular deep watering.",
        "npk_fertilizer_tip": "High Nitrogen & Iron for evergreen leaves."
    },
        # ========================================================
    # CORN
    # ========================================================

    "corn_cercospora_leaf_spot": {
        "id": "corn_cercospora_leaf_spot",
        "display_name": "Corn Cercospora Leaf Spot",
        "crop_type": "Corn (Zea mays)",
        "scientific_name": "Cercospora zeae-maydis",
        "status": "Diseased",
        "severity": "Medium",
        "description": "Fungal leaf disease producing gray to tan rectangular lesions that can reduce photosynthetic activity.",
        "symptoms": [
            "Long gray or tan lesions on leaves.",
            "Lesions often develop parallel to leaf veins.",
            "Premature leaf drying in severe infections."
        ],
        "organic_remedies": [
            "Remove severely infected plant debris.",
            "Improve field airflow and avoid excessive leaf wetness."
        ],
        "chemical_treatments": [
            "Use an approved corn fungicide when disease pressure is high."
        ],
        "prevention": [
            "Use resistant hybrids.",
            "Practice crop rotation.",
            "Manage infected crop residue."
        ],
        "recommended_irrigation": "Avoid excessive overhead irrigation.",
        "npk_fertilizer_tip": "Maintain balanced nitrogen and potassium nutrition."
    },


    "corn_common_rust": {
        "id": "corn_common_rust",
        "display_name": "Corn Common Rust",
        "crop_type": "Corn (Zea mays)",
        "scientific_name": "Puccinia sorghi",
        "status": "Diseased",
        "severity": "Medium",
        "description": "Fungal rust disease producing reddish-brown pustules on corn leaves.",
        "symptoms": [
            "Small reddish-brown rust pustules.",
            "Pustules occur on both leaf surfaces.",
            "Severe infections can cause premature leaf senescence."
        ],
        "organic_remedies": [
            "Remove heavily infected plant debris.",
            "Maintain good field airflow."
        ],
        "chemical_treatments": [
            "Use an approved fungicide when economically justified."
        ],
        "prevention": [
            "Plant resistant corn hybrids.",
            "Use crop rotation."
        ],
        "recommended_irrigation": "Use efficient irrigation and avoid prolonged leaf wetness.",
        "npk_fertilizer_tip": "Maintain balanced NPK nutrition."
    },


    "corn_northern_leaf_blight": {
        "id": "corn_northern_leaf_blight",
        "display_name": "Corn Northern Leaf Blight",
        "crop_type": "Corn (Zea mays)",
        "scientific_name": "Exserohilum turcicum",
        "status": "Diseased",
        "severity": "High",
        "description": "Fungal disease producing characteristic elongated gray-green to tan lesions on corn leaves.",
        "symptoms": [
            "Long cigar-shaped lesions.",
            "Gray-green lesions becoming tan or brown.",
            "Severe disease causes major leaf area loss."
        ],
        "organic_remedies": [
            "Remove or properly manage infected crop residue.",
            "Improve field sanitation."
        ],
        "chemical_treatments": [
            "Apply an approved fungicide according to local agricultural guidance."
        ],
        "prevention": [
            "Use resistant hybrids.",
            "Rotate crops.",
            "Manage crop residue."
        ],
        "recommended_irrigation": "Avoid unnecessary overhead irrigation.",
        "npk_fertilizer_tip": "Maintain balanced nitrogen and potassium."
    },


    "corn_healthy": {
        "id": "corn_healthy",
        "display_name": "Corn - Healthy Leaf",
        "crop_type": "Corn (Zea mays)",
        "scientific_name": "N/A",
        "status": "Healthy",
        "severity": "None",
        "description": "Healthy green corn foliage without visible disease lesions.",
        "symptoms": [
            "No significant disease symptoms detected."
        ],
        "organic_remedies": [
            "Continue good crop management practices."
        ],
        "chemical_treatments": [
            "No treatment required."
        ],
        "prevention": [
            "Monitor leaves regularly.",
            "Maintain proper field sanitation."
        ],
        "recommended_irrigation": "Regular irrigation according to crop growth stage and weather.",
        "npk_fertilizer_tip": "Maintain balanced NPK nutrition."
    },


    # ========================================================
    # POTATO
    # ========================================================

    "potato_early_blight": {
        "id": "potato_early_blight",
        "display_name": "Potato Early Blight",
        "crop_type": "Potato (Solanum tuberosum)",
        "scientific_name": "Alternaria solani",
        "status": "Diseased",
        "severity": "High",
        "description": "Fungal disease producing dark concentric lesions on potato leaves.",
        "symptoms": [
            "Dark brown circular leaf spots.",
            "Concentric ring patterns resembling a target.",
            "Yellowing around older lesions."
        ],
        "organic_remedies": [
            "Remove severely infected foliage.",
            "Improve field sanitation."
        ],
        "chemical_treatments": [
            "Use an approved fungicide according to local recommendations."
        ],
        "prevention": [
            "Use crop rotation.",
            "Avoid prolonged leaf wetness.",
            "Remove infected crop debris."
        ],
        "recommended_irrigation": "Prefer drip irrigation where practical.",
        "npk_fertilizer_tip": "Avoid excessive nitrogen and maintain adequate potassium."
    },


    "potato_late_blight": {
        "id": "potato_late_blight",
        "display_name": "Potato Late Blight",
        "crop_type": "Potato (Solanum tuberosum)",
        "scientific_name": "Phytophthora infestans",
        "status": "Diseased",
        "severity": "Critical",
        "description": "Highly destructive disease causing rapidly expanding dark lesions on potato leaves.",
        "symptoms": [
            "Irregular dark brown or black leaf lesions.",
            "Rapid leaf tissue collapse.",
            "White fungal growth may appear under humid conditions."
        ],
        "organic_remedies": [
            "Remove severely infected plant material.",
            "Avoid prolonged leaf wetness."
        ],
        "chemical_treatments": [
            "Use locally approved late-blight fungicides according to label directions."
        ],
        "prevention": [
            "Use certified disease-free seed.",
            "Remove volunteer potato plants.",
            "Monitor crops during cool and humid weather."
        ],
        "recommended_irrigation": "Prefer drip irrigation and avoid unnecessary overhead watering.",
        "npk_fertilizer_tip": "Maintain balanced nutrition and avoid excessive nitrogen."
    },


    "potato_healthy": {
        "id": "potato_healthy",
        "display_name": "Potato - Healthy Leaf",
        "crop_type": "Potato (Solanum tuberosum)",
        "scientific_name": "N/A",
        "status": "Healthy",
        "severity": "None",
        "description": "Healthy green potato foliage without significant visible disease symptoms.",
        "symptoms": [
            "Leaves appear green and intact.",
            "No significant lesions detected."
        ],
        "organic_remedies": [
            "Continue normal crop care."
        ],
        "chemical_treatments": [
            "No treatment required."
        ],
        "prevention": [
            "Regularly inspect plants.",
            "Use clean planting material."
        ],
        "recommended_irrigation": "Consistent irrigation according to soil and weather conditions.",
        "npk_fertilizer_tip": "Maintain balanced NPK nutrition."
    },


    # ========================================================
    # TOMATO
    # ========================================================

    "tomato_bacterial_spot": {
        "id": "tomato_bacterial_spot",
        "display_name": "Tomato Bacterial Spot",
        "crop_type": "Tomato (Solanum lycopersicum)",
        "scientific_name": "Xanthomonas spp.",
        "status": "Diseased",
        "severity": "High",
        "description": "Bacterial disease causing small dark spots on tomato leaves and fruit.",
        "symptoms": [
            "Small dark leaf spots.",
            "Yellow halos may surround lesions.",
            "Fruit can develop raised dark spots."
        ],
        "organic_remedies": [
            "Remove heavily infected plant material.",
            "Avoid working with plants when foliage is wet."
        ],
        "chemical_treatments": [
            "Use approved copper-based products according to label directions."
        ],
        "prevention": [
            "Use disease-free seed and transplants.",
            "Avoid overhead irrigation."
        ],
        "recommended_irrigation": "Drip irrigation.",
        "npk_fertilizer_tip": "Maintain balanced plant nutrition."
    },


    "tomato_early_blight": {
        "id": "tomato_early_blight",
        "display_name": "Tomato Early Blight",
        "crop_type": "Tomato (Solanum lycopersicum)",
        "scientific_name": "Alternaria solani",
        "status": "Diseased",
        "severity": "High",
        "description": "Fungal disease producing dark concentric-ring lesions on tomato leaves.",
        "symptoms": [
            "Dark circular lesions.",
            "Concentric ring patterns.",
            "Yellowing around infected tissue."
        ],
        "organic_remedies": [
            "Remove infected lower leaves.",
            "Improve airflow around plants."
        ],
        "chemical_treatments": [
            "Use an approved fungicide according to local recommendations."
        ],
        "prevention": [
            "Rotate crops.",
            "Remove infected plant debris.",
            "Avoid overhead irrigation."
        ],
        "recommended_irrigation": "Drip irrigation.",
        "npk_fertilizer_tip": "Maintain balanced NPK nutrition."
    },


    "tomato_late_blight": {
        "id": "tomato_late_blight",
        "display_name": "Tomato Late Blight",
        "crop_type": "Tomato (Solanum lycopersicum)",
        "scientific_name": "Phytophthora infestans",
        "status": "Diseased",
        "severity": "Critical",
        "description": "Rapidly developing disease that produces dark water-soaked lesions on tomato leaves.",
        "symptoms": [
            "Dark irregular leaf lesions.",
            "Water-soaked appearance.",
            "Rapid tissue collapse under favorable conditions."
        ],
        "organic_remedies": [
            "Remove infected plant material.",
            "Keep foliage as dry as practical."
        ],
        "chemical_treatments": [
            "Use locally approved late-blight fungicides according to label directions."
        ],
        "prevention": [
            "Avoid prolonged leaf wetness.",
            "Remove infected debris.",
            "Monitor during cool humid weather."
        ],
        "recommended_irrigation": "Drip irrigation.",
        "npk_fertilizer_tip": "Maintain balanced nutrition."
    },


    "tomato_leaf_mold": {
        "id": "tomato_leaf_mold",
        "display_name": "Tomato Leaf Mold",
        "crop_type": "Tomato (Solanum lycopersicum)",
        "scientific_name": "Passalora fulva",
        "status": "Diseased",
        "severity": "Medium",
        "description": "Fungal disease commonly associated with high humidity and poor air circulation.",
        "symptoms": [
            "Yellow patches on upper leaf surfaces.",
            "Olive-green to brown fungal growth underneath leaves.",
            "Leaves may curl and drop."
        ],
        "organic_remedies": [
            "Improve ventilation.",
            "Remove severely infected leaves."
        ],
        "chemical_treatments": [
            "Use an approved fungicide when necessary."
        ],
        "prevention": [
            "Maintain good greenhouse ventilation.",
            "Avoid excessive humidity.",
            "Use resistant varieties when available."
        ],
        "recommended_irrigation": "Drip irrigation.",
        "npk_fertilizer_tip": "Avoid excessive nitrogen."
    },


    "tomato_septoria_leaf_spot": {
        "id": "tomato_septoria_leaf_spot",
        "display_name": "Tomato Septoria Leaf Spot",
        "crop_type": "Tomato (Solanum lycopersicum)",
        "scientific_name": "Septoria lycopersici",
        "status": "Diseased",
        "severity": "Medium",
        "description": "Fungal leaf spot disease characterized by numerous small circular lesions.",
        "symptoms": [
            "Small circular spots with dark margins.",
            "Tiny dark structures inside lesions.",
            "Progressive yellowing and leaf drop."
        ],
        "organic_remedies": [
            "Remove infected lower leaves.",
            "Improve plant airflow."
        ],
        "chemical_treatments": [
            "Use an approved fungicide according to label directions."
        ],
        "prevention": [
            "Remove infected debris.",
            "Avoid overhead irrigation.",
            "Use crop rotation."
        ],
        "recommended_irrigation": "Drip irrigation.",
        "npk_fertilizer_tip": "Maintain balanced nutrition."
    },


    "tomato_spider_mites": {
        "id": "tomato_spider_mites",
        "display_name": "Tomato Spider Mites",
        "crop_type": "Tomato (Solanum lycopersicum)",
        "scientific_name": "Tetranychus spp.",
        "status": "Diseased",
        "severity": "Medium",
        "description": "Spider mite infestation causing stippling, yellowing and weakening of tomato leaves.",
        "symptoms": [
            "Fine yellow or pale stippling.",
            "Bronzing of leaves.",
            "Fine webbing may appear during heavy infestations."
        ],
        "organic_remedies": [
            "Use strong water sprays to dislodge mites.",
            "Encourage beneficial predatory mites."
        ],
        "chemical_treatments": [
            "Use an approved miticide when necessary."
        ],
        "prevention": [
            "Monitor leaf undersides regularly.",
            "Avoid excessive plant stress."
        ],
        "recommended_irrigation": "Maintain consistent irrigation.",
        "npk_fertilizer_tip": "Avoid excessive nitrogen."
    },


    "tomato_target_spot": {
        "id": "tomato_target_spot",
        "display_name": "Tomato Target Spot",
        "crop_type": "Tomato (Solanum lycopersicum)",
        "scientific_name": "Corynespora cassiicola",
        "status": "Diseased",
        "severity": "Medium",
        "description": "Fungal disease producing circular target-like lesions on tomato leaves and fruit.",
        "symptoms": [
            "Circular brown lesions.",
            "Concentric target-like rings.",
            "Leaf yellowing and premature drop."
        ],
        "organic_remedies": [
            "Remove infected foliage.",
            "Improve airflow."
        ],
        "chemical_treatments": [
            "Use an approved fungicide according to local guidance."
        ],
        "prevention": [
            "Avoid prolonged leaf wetness.",
            "Remove infected crop residue."
        ],
        "recommended_irrigation": "Drip irrigation.",
        "npk_fertilizer_tip": "Maintain balanced nutrition."
    },


    "tomato_yellow_leaf_curl_virus": {
        "id": "tomato_yellow_leaf_curl_virus",
        "display_name": "Tomato Yellow Leaf Curl Virus",
        "crop_type": "Tomato (Solanum lycopersicum)",
        "scientific_name": "Tomato yellow leaf curl virus",
        "status": "Diseased",
        "severity": "Critical",
        "description": "Viral disease causing severe leaf curling, yellowing and plant stunting, commonly transmitted by whiteflies.",
        "symptoms": [
            "Upward curling of leaves.",
            "Yellowing around leaf margins.",
            "Severe plant stunting."
        ],
        "organic_remedies": [
            "Remove severely infected plants.",
            "Use insect-exclusion practices to reduce whiteflies."
        ],
        "chemical_treatments": [
            "Manage whitefly vectors using locally approved products."
        ],
        "prevention": [
            "Use virus-free transplants.",
            "Control whitefly populations.",
            "Remove infected plants promptly."
        ],
        "recommended_irrigation": "Consistent drip irrigation.",
        "npk_fertilizer_tip": "Maintain balanced nutrition."
    },


    "tomato_mosaic_virus": {
        "id": "tomato_mosaic_virus",
        "display_name": "Tomato Mosaic Virus",
        "crop_type": "Tomato (Solanum lycopersicum)",
        "scientific_name": "Tomato mosaic virus",
        "status": "Diseased",
        "severity": "High",
        "description": "Viral disease causing characteristic mosaic patterns, leaf distortion and reduced plant growth.",
        "symptoms": [
            "Light and dark green mosaic patterns.",
            "Leaf distortion.",
            "Reduced plant growth."
        ],
        "organic_remedies": [
            "Remove infected plants.",
            "Disinfect tools after handling infected plants."
        ],
        "chemical_treatments": [
            "There is no curative chemical treatment for an infected plant."
        ],
        "prevention": [
            "Use certified disease-free seed.",
            "Disinfect tools.",
            "Avoid handling plants when hands are contaminated."
        ],
        "recommended_irrigation": "Regular irrigation according to crop requirements.",
        "npk_fertilizer_tip": "Maintain balanced nutrition."
    },


    "tomato_healthy": {
        "id": "tomato_healthy",
        "display_name": "Tomato - Healthy Leaf",
        "crop_type": "Tomato (Solanum lycopersicum)",
        "scientific_name": "N/A",
        "status": "Healthy",
        "severity": "None",
        "description": "Healthy tomato foliage with normal green coloration and no significant visible disease symptoms.",
        "symptoms": [
            "Green leaves.",
            "No significant disease lesions.",
            "Normal leaf structure."
        ],
        "organic_remedies": [
            "Continue good crop management."
        ],
        "chemical_treatments": [
            "No treatment required."
        ],
        "prevention": [
            "Inspect plants regularly.",
            "Maintain field sanitation."
        ],
        "recommended_irrigation": "Regular drip irrigation.",
        "npk_fertilizer_tip": "Maintain balanced NPK nutrition."
    },
}

def get_disease_by_id(disease_id: str):
    """Retrieve disease details from database by ID key."""
    return FRUIT_DISEASE_DB.get(disease_id, FRUIT_DISEASE_DB["apple_scab"])

def list_all_crops():
    """List distinct fruit crops available in database."""
    crops = set()
    for disease in FRUIT_DISEASE_DB.values():
        crops.add(disease["crop_type"])
    return sorted(list(crops))
