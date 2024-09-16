from neurapolis_common.models.file_section import FileSection
from neurapolis_common.services.db_session_builder import db_session_builder

from neurapolis_retriever.state.hit import Hit
from neurapolis_retriever.state.hit_step import HitStep
from neurapolis_retriever.state.search_step import SearchStep
from neurapolis_retriever.state.state import State


def cleaner_node(state: State):
    unique_file_chunk_ids: list[str] = []
    for x_search in state.searches:
        if x_search.step != SearchStep.RETRIEVED:
            continue
        for x_hit in x_search.hits:
            if (
                x_hit.step != HitStep.RETRIEVED
                or x_hit.file_chunk.id in unique_file_chunk_ids
            ):
                continue
            unique_file_chunk_ids.append(x_hit.file_chunk.id)
    # Retrieve the file sections of the hits (Parent document retrieval)
    with db_session_builder.build() as db_session:
        db_results = db_session.run(
            """
            MATCH (file_chunk_node:FileChunk)<-[:FILE_SECTION_HAS_FILE_CHUNK]-(file_section_node:FileSection)
            WHERE file_chunk_node.id IN $file_chunk_ids
            RETURN file_chunk_node.id AS file_chunk_id, file_section_node
            """,
            file_chunk_ids=unique_file_chunk_ids,
        )
        file_chunk_to_file_section_map: dict[str, FileSection] = {}
        for x_db_result in db_results:
            file_chunk_id = x_db_result["file_chunk_id"]
            file_section = FileSection.from_db_node_dict(
                x_db_result["file_section_node"],
            )
            file_chunk_to_file_section_map[file_chunk_id] = file_section

    # Assign the file sections to the hits
    for x_search in state.searches:
        if x_search.step != SearchStep.RETRIEVED:
            continue
        for x_hit in x_search.hits:
            if x_hit.step != HitStep.RETRIEVED:
                continue
            file_section = file_chunk_to_file_section_map[x_hit.file_chunk.id]
            x_hit.file_section = file_section
            x_hit.step = HitStep.FILE_SECTION_RETRIEVED
        x_search.step = SearchStep.FILE_SECTIONS_RETRIEVED

    # Mark hits as doubled when they have the same file section as other hits
    unique_hits: list[Hit] = []
    for x_search in state.searches:
        if x_search.step != SearchStep.FILE_SECTIONS_RETRIEVED:
            continue
        for x_hit in x_search.hits:
            if x_hit.step != HitStep.FILE_SECTION_RETRIEVED:
                continue
            existing_unique_hit = None
            for y_unique_hit in unique_hits:
                if y_unique_hit.file_section.id != x_hit.file_section.id:
                    continue
                existing_unique_hit = y_unique_hit
                break
            if existing_unique_hit:
                x_hit.step = HitStep.DOUBLED
                x_hit.doubled_hit_id = existing_unique_hit.id
            else:
                x_hit.step = HitStep.NOT_DOUBLED
                unique_hits.append(x_hit)
        x_search.step = SearchStep.UNDOUBLED

    return {"searches": state.searches}
