import enum
from typing import Optional


class Base:
    pass


class College(Base):
    __tablename__ = "college"

    name: str


class School(Base):
    __tablename__ = "school"

    name: str
    college: College


class Staff(Base):
    __tablename__ = "staff"

    name: str
    email: str
    phone_number: str


class ExamDiet(enum.Enum):
    MAIN_S1 = "MAIN_S1"
    RESIT_S1 = "RESIT_S1"
    MAIN_S2 = "MAIN_S2"
    RESIT_S2 = "RESIT_S2"


class Exam(Base):
    __tablename__ = "exam"

    course: "Course"
    date: str
    time: str
    location: str
    minutes: int
    paper_name: str
    diet: ExamDiet


class Course(Base):
    __tablename__ = "course"

    euclid_code: str
    name: str
    academic_year_starting: int
    school: School
    scqf_level: int
    scqf_credits: int
    ects_credits: int
    summary: str
    course_description: str

    prerequisites: list["CourseCondition"]
    corequisites: list["CourseCondition"]
    prohibited_combinations: list["CourseCondition"]
    other_requirements: str

    visiting_student_prerequisites: Optional[str]
    visiting_student_high_demand: Optional[bool]

    availability: str
    quota: Optional[int]
    week_start: int
    week_end: int
    period: str

    total_hours: int
    hours: list["LearningTeachingActivityBreakdown"]
    assessments: list["AssessmentActivityBreakdown"]
    additional_assessment_info: str
    feedback_info: str

    exams: list[Exam]

    learning_outcomes: list[str]

    reading_list: list[str]

    graduate_attribute_skills: Optional[str]
    keywords: list[str]

    # e.g. "Special Arrangements", "Course URL", "Additional Class Delivery Information"
    additional_meta: dict[str, str]

    course_organizer: Staff
    course_secretary: Staff


class CourseConditionOperator(enum.Enum):
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    LEAF = "LEAF"


class CourseCondition(Base):
    __tablename__ = "course_condition"

    operator: CourseConditionOperator
    parent: Optional["CourseCondition"]
    leaf_course: Optional[Course]


class LearningTeachingActivityType(Base):
    __tablename__ = "learning_teaching_activity_type"

    name: str


class LearningTeachingActivityBreakdown(Base):
    __tablename__ = "learning_teaching_activity_breakdown"

    course: Course
    activity_type: LearningTeachingActivityType
    hours: int


class AssessmentActivityType(Base):
    __tablename__ = "assessment_activity_type"

    name: str


class AssessmentActivityBreakdown(Base):
    __tablename__ = "assessment_activity_breakdown"

    course: Course
    activity_type: AssessmentActivityType
    percentage: int


class CourseRelationType(enum.Enum):
    # e.g. multiple courses into one, one course into multiple, or
    # a course being fundamentally restuctured.
    RESTRUCTURED = "RESTRUCTURED"
    # e.g. course code change and/or name change, different organizer, but
    # essentially the same course.
    REPLACED = "REPLACED"
    # the same course but in another year. contractually, euclid code will
    # stay the same.
    SUCCEEDED = "SUCCEEDED"


class CourseRelation(Base):
    __tablename__ = "course_relation"

    from_course: Course
    to_course: Course
    relation_type: CourseRelationType


class DegreeDeliveryType(enum.Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    PART_TIME_INTERMITTENT = "PART_TIME_INTERMITTENT"


class DegreeLevelType(enum.Enum):
    UNDERGRADUATE = "UNDERGRADUATE"
    POSTGRADUATE = "POSTGRADUATE"
    DOCTORATE = "DOCTORATE"


class Degree(Base):
    __tablename__ = "degree"

    ext_id: str
    name: str
    college: College
    school: School
    honours: bool
    title: str  # MSc, BEng, MA, PhD with Integrated Study, etc
    code: str  # same as ext_id?
    level: DegreeLevelType
    delivery_type: DegreeDeliveryType
    duration_year_options: list[int]


class DegreeInstance(Base):
    __tablename__ = "degree_instance"

    degree: Degree
    academic_year_starting: int
