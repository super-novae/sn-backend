types = ["SRC", "College", "Department"]

colleges_programmes = {
    "College of Agriculture and Natural Resources": [
        "BSc Agriculture",
        "BSc Natural Resources Management",
        "BSc Post Harvest Technology",
        "BSc Dairy and Meat Science and Technology",
        "BSc Landscape Design and Management",
        "BSc Agricultural Biotechnology",
        "BSc Agribusiness Management",
        "BSc Forest Resources Technology",
        "BSc Aquaculture & Water Resources Management",
    ],
    "College of Art and Built Environment": [
        "BSc Architecture",
        "BSc Construction Technology & Management",
        "BSc Quantity Surveying & Construction Economics",
        "BSc Development Planning",
        "BSc Human Settlement Planning",
        "BSc Land Economy",
        "BSc Real Estate",
        "BFA Painting and Sculpture",
        "BA Communication Design",
        "BA Industrial Art" "BA Integrated Rural Art and Industry",
        "BA Publishing Studies",
        "BA Integrated Rural Art and Industry",
        "BA Publishing Studies",
        "BA Communication Design",
        "BFA Painting and Sculpture",
    ],
    "College of Humanities and Social Sciences": [
        "BA Economics",
        "BA Geography and Rural Development",
        "BA Sociology",
        "BA Social Work",
        "BA Religious Studies",
        "BA History",
        "BA Political Studies",
        "BA French",
        "BA Akan",
        "BA Culture and Tourism",
        "BA English",
        "BSc. Business Administration",
        "LLB",
    ],
    "College of Engineering": [
        "BSc Agricultural Engineering",
        "BSc Chemical Engineering",
        "BSc Civil Engineering",
        "BSc Geomatic Engineering (Geodetic Engineering)",
        "BSc Materials Engineering",
        "BSc Mechanical Engineering",
        "BSc Electrical & Electronic Engineering",
        "BSc Computer Engineering",
        "BSc Aerospace Engineering",
        "BSc Petroleum Engineering",
        "BSc Telecommunication Engineering",
        "BSc Geological Engineering",
        "BSc Biomedical Engineering",
        "BSc Petrochemical Engineering",
        "BSc Metallurgical Engineering",
    ],
    "College of Health Sciences": [
        "Pharm D (Doctor of Pharmacy)",
        "BSc Herbal Medicine",
        "BSc Human Biology (Medicine)",
        "BSc Medical Laboratory Technology",
        "BSc Sports and Exercise Science",
        "BSc Nursing",
        "BSc Midwifery",
        "BSc Emergency Nursing",
        "BSc BDS Dental Surgery",
        "DVM (Doctor of Veterinary Medicine)",
        "BSc Sonography",
        "BSc Disability & Rehabilitation Studies",
    ],
    "College of Science": [
        "BSc Biochemistry",
        "BSc Food Science and Technology",
        "BSc Biological Sciences",
        "BSc Environmental Science",
        "BSc Chemistry",
        "BSc Computer Science",
        "BSc Mathematics",
        "BSc Statistics",
        "BSc Physics",
        "BSc Actuarial Science",
        "Doctor of Optometry (OD)",
        "BSc Meteorology and Climate Science",
    ],
}

colleges = [key for key, value in colleges_programmes.items()]

programmes = []

for key, value in colleges_programmes.items():
    programmes += value

years = ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Year 6"]
