from apiflask import Schema
from apiflask.fields import String, List, Nested
from apiflask.validators import Length, Regexp, URL, OneOf



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
        "BSc Biochemistry"
        "BSc Food Science and Technology"
        "BSc Biological Sciences"
        "BSc Environmental Science"
        "BSc Chemistry"
        "BSc Computer Science"
        "BSc Mathematics"
        "BSc Statistics"
        "BSc Physics"
        "BSc Actuarial Science"
        "Doctor of Optometry (OD)"
        "BSc Meteorology and Climate Science"
    ],
}

colleges = [key for key, value in colleges_programmes.items()]

programmes = []

for key, value in colleges_programmes.items():
    programmes += value

class ElectionSchema(Schema):
    id = String(required=True, dump_only=True)
    name = String(validate=[Length(5, 100)], required=True)
    organization_id = String(
        required=True, validate=[Regexp("^org-"), Length(equal=32)]
    )
    route_name = String(required=True, validate=[Length(min=4, max=50)])
    type = String(required=True, validate=[OneOf(types)])
    college = String(required=False, validate=[OneOf(colleges)])
    programme = String(required=False, validate=[OneOf(programmes)])


class ElectionsSchema(Schema):
    elections = List(Nested(ElectionSchema))


class ElectionUpdateSchema(Schema):
    name = String(validate=[Length(5, 100)], required=True)
    route_name = String(required=False, validate=[Length(min=4, max=50)])


class OfficeSchema(Schema):
    id = String(required=True, dump_only=True)
    name = String(required=True)
    route_name = String(required=True, validate=[Length(min=4, max=50)])
    election_id = String(required=True, validate=[Regexp("^elec-"), Length(equal=32)])


class OfficesSchema(Schema):
    offices = List(Nested(OfficeSchema))


class OfficeUpdateSchema(Schema):
    name = String(required=True)
    route_name = String(required=True, validate=[Length(min=4, max=50)])


class CandidateSchema(Schema):
    name = String(validate=[Length(5, 80)], required=True)
    public_id = String(validate=[Length(equal=16)], dump_only=True)
    organization_id = String(validate=[Length(equal=32)])
    election_id = String(validate=[Length(equal=32)])
    profile_image_url = String(validate=[URL(schemes=["https"])])
    office_id = String(required=True, validate=[Regexp("^off-")])
    programme = String(required=True, validate=[Length(min=10, max=100)])


class CandidatesSchema(Schema):
    candidates = List(Nested(CandidateSchema))

