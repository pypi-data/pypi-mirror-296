from neurapolis_common.models.agenda_item import AgendaItem
from neurapolis_common.models.consultation import Consultation
from neurapolis_common.models.file import File
from neurapolis_common.models.meeting import Meeting
from neurapolis_common.models.organization import Organization
from neurapolis_common.models.paper import Paper
from neurapolis_common.models.person import Person
from neurapolis_common.models.retriever_state import RetrieverState
from neurapolis_common.services.db_session_builder import db_session_builder

from neurapolis_retriever.state.hit_step import HitStep
from neurapolis_retriever.state.search_step import SearchStep
from neurapolis_retriever.state.state import State


# TODO Paper can have multiple consultations and consultations
def related_data_gatherer_node(state: State):
    # the node connected to the file seciton is always first a File
    # That file can then be connected to a Meeting via relationship or to a Paper
    # When it is connected to a Meeting, retrieve the meeting, the AgendaItem(s) of the Meeting and the Persons connected to the Meeting + the Organizations connected to the Meeting
    # When it is connected to a Paper, retrieve the Paper, then the Consultation and then go from Consultation to AgendaItem. Then from AgendaItem to Meeting.
    # Then from Meeting get all AgendaItem(s) and the Persons and Organizations connected to the Meeting.
    # TODO only for relevant file sections

    # Get the file of each file section
    with db_session_builder.build() as db_session:
        unique_file_section_ids: list[str] = []
        for x_search in state.searches:
            if x_search.step != SearchStep.RELEVANCE_GRADED:
                continue
            for y_hit in x_search.hits:
                if (
                    y_hit.step != HitStep.RELEVANCE_GRADED
                    or y_hit.grading.is_relevant == False
                    or y_hit.file_section.id in unique_file_section_ids
                ):
                    continue
                unique_file_section_ids.append(y_hit.file_section.id)
        db_query = """
        MATCH (file_section_node:FileSection)<-[:FILE_HAS_FILE_SECTION]-(file_node:File)
        WHERE file_section_node.id IN $file_section_ids
        RETURN file_section_node.id AS file_section_id, file_node
        """
        db_results = db_session.run(db_query, file_section_ids=unique_file_section_ids)
        file_section_id_to_file_map: dict[str, File] = {}
        for x_db_result in db_results:
            file_section_id = x_db_result["file_section_id"]
            file = File.from_db_node_dict(x_db_result["file_node"])
            print("filesection_id", file_section_id, "file", file.id)
            file_section_id_to_file_map[file_section_id] = file
        for x_search in state.searches:
            if x_search.step != SearchStep.RELEVANCE_GRADED:
                continue
            for y_hit in x_search.hits:
                if (
                    y_hit.step != HitStep.RELEVANCE_GRADED
                    or y_hit.grading.is_relevant == False
                ):
                    continue
                related_file = file_section_id_to_file_map[y_hit.file_section.id]
                y_hit.related_file = related_file

        # Go from file to meeting and gather data on the way
        unique_file_ids = []
        for x_search in state.searches:
            if x_search.step != SearchStep.RELEVANCE_GRADED:
                continue
            for y_hit in x_search.hits:
                if (
                    y_hit.step != HitStep.RELEVANCE_GRADED
                    or y_hit.grading.is_relevant == False
                    or y_hit.related_file.id in unique_file_ids
                ):
                    continue
                unique_file_ids.append(y_hit.related_file.id)
        db_query = """
        MATCH (file_node:File)<-[:MEETING_HAS_INVITATION_FILE|MEETING_HAS_RESULTS_PROTOCOL_FILE|MEETING_HAS_VERBATIM_PROTOCOL_FILE|MEETING_HAS_AUXILIARY_FILE]-(meeting_node:Meeting)
        WHERE file_node.id IN $file_ids
        RETURN file_node.id as file_id, meeting_node, null as paper_node, null as consultation_node, null as agenda_item_node
        UNION
        MATCH (file_node:File)<-[:PAPER_HAS_MAIN_FILE|PAPER_HAS_AUXILIARY_FILE]-(paper_node:Paper)-[:PAPER_HAS_CONSULTATION]->(consultation_node:Consultation)<-[:AGENDA_ITEM_HAS_CONSULTATION]-(agenda_item_node:AgendaItem)<-[:MEETING_HAS_AGENDA_ITEM]-(meeting_node:Meeting)
        WHERE file_node.id IN $file_ids
        RETURN file_node.id as file_id, meeting_node, paper_node, consultation_node, agenda_item_node
        """
        db_results = db_session.run(db_query, file_ids=unique_file_ids)
        file_id_to_related_data_map: dict[str, list[RetrieverState]] = {}
        for x_db_result in db_results:
            file_id = x_db_result["file_id"]
            print(file_id)
            related_meeting = Meeting.from_db_node_dict(x_db_result["meeting_node"])
            print("related_meeting", related_meeting)
            related_paper = (
                None
                if x_db_result["paper_node"] == None
                else Paper.from_db_node_dict(x_db_result["paper_node"])
            )
            print("related_paper", related_paper)
            related_consultation = (
                None
                if x_db_result["consultation_node"] == None
                else Consultation.from_db_node_dict(x_db_result["consultation_node"])
            )
            print("related_consultation", related_consultation)
            related_agenda_item = (
                None
                if x_db_result["agenda_item_node"] == None
                else AgendaItem.from_db_node_dict(x_db_result["agenda_item_node"])
            )
            print("related_agenda_item", related_agenda_item)
            related_data = {
                "meeting": related_meeting,
                "paper": related_paper,
                "consultation": related_consultation,
                "agenda_item": related_agenda_item,
            }
            file_id_to_related_data_map[file_id] = related_data
        for x_search in state.searches:
            if x_search.step != SearchStep.RELEVANCE_GRADED:
                continue
            for y_hit in x_search.hits:
                if (
                    y_hit.step != HitStep.RELEVANCE_GRADED
                    or y_hit.grading.is_relevant == False
                ):
                    continue
                # HACK: Why is this coming up?
                if y_hit.related_file.id not in file_id_to_related_data_map:
                    print(f"Missing file ID: {y_hit.related_file.id}")
                else:
                    related_data = file_id_to_related_data_map[y_hit.related_file.id]
                    if related_data["meeting"] != None:
                        y_hit.related_meeting = related_data["meeting"]
                    if related_data["paper"] != None:
                        y_hit.related_paper = related_data["paper"]
                    if related_data["consultation"] != None:
                        y_hit.related_consultation = related_data["consultation"]
                    if related_data["agenda_item"] != None:
                        y_hit.related_agenda_item = related_data["agenda_item"]
        # Go from meetings to its persons and organizations
        unique_meeting_ids = []
        for x_search in state.searches:
            if x_search.step != SearchStep.RELEVANCE_GRADED:
                continue
            for y_hit in x_search.hits:
                if (
                    y_hit.step != HitStep.RELEVANCE_GRADED
                    or y_hit.grading.is_relevant == False
                    or y_hit.related_meeting == None
                    or y_hit.related_meeting.id in unique_meeting_ids
                ):
                    continue
                unique_meeting_ids.append(y_hit.related_meeting.id)
        db_query = """
        MATCH (meeting_node:Meeting)
        OPTIONAL MATCH (meeting_node)<-[:PERSON_HAS_MEETING]-(person_node:Person)
        OPTIONAL MATCH (meeting_node)<-[:ORGANIZATION_HAS_MEETING]-(organization_node:Organization)
        WHERE meeting_node.id IN $meeting_ids
        RETURN meeting_node.id as meeting_id,
            COLLECT(DISTINCT person_node) AS persons,
            COLLECT(DISTINCT organization_node) AS organizations
        """
        db_results = db_session.run(db_query, meeting_ids=unique_meeting_ids)
        meeting_id_to_related_data_map: dict[str, list[RetrieverState]] = {}
        for x_db_result in db_results:
            meeting_id = x_db_result["meeting_id"]
            related_persons = []
            for x_person_node in x_db_result["persons"]:
                related_persons.append(Person.from_db_node_dict(x_person_node))
            related_organizations = []
            for x_organization_node in x_db_result["organizations"]:
                related_organizations.append(
                    Organization.from_db_node_dict(x_organization_node)
                )
            related_data = {
                "persons": related_persons,
                "organizations": related_organizations,
            }
            meeting_id_to_related_data_map[meeting_id] = related_data
        for x_search in state.searches:
            if x_search.step != SearchStep.RELEVANCE_GRADED:
                continue
            for y_hit in x_search.hits:
                if (
                    y_hit.step != HitStep.RELEVANCE_GRADED
                    or y_hit.grading.is_relevant == False
                    or y_hit.related_meeting == None
                ):
                    continue
                # HACK: Why is this coming up?
                if y_hit.related_meeting.id not in meeting_id_to_related_data_map:
                    print(f"Missing meeting ID: {y_hit.related_meeting.id}")
                else:
                    related_data = meeting_id_to_related_data_map[
                        y_hit.related_meeting.id
                    ]
                    y_hit.related_persons = related_data["persons"]
                    y_hit.related_organizations = related_data["organizations"]
                y_hit.step = HitStep.RELATED_DATA_GATHERED
            x_search.step = SearchStep.RELATED_DATA_GATHERED
    return state
