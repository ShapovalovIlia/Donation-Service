# mypy: disable-error-code="assignment"

from typing import Any, Iterable, Sequence

from pymongo import InsertOne, UpdateOne, DeleteOne
from motor.motor_asyncio import AsyncIOMotorClientSession

from donation.domain import (
    MovieRole,
    MovieWriter,
    MovieCrewMember,
    AddMovieContribution,
)
from donation.infra.database.collections import (
    AddMovieContributionCollection,
)


class CommitAddMovieContributionCollectionChanges:
    def __init__(
        self,
        collection: AddMovieContributionCollection,
        session: AsyncIOMotorClientSession,
    ):
        self._collection = collection
        self._session = session

    async def __call__(
        self,
        *,
        new: Sequence[AddMovieContribution],
        clean: Sequence[AddMovieContribution],
        dirty: Sequence[AddMovieContribution],
        deleted: Sequence[AddMovieContribution],
    ) -> None:
        inserts = [
            InsertOne(self._contribution_to_document(contribution))
            for contribution in new
        ]
        updates = [
            UpdateOne(
                {"id": clean_contribution.id.hex},
                self._pipeline_to_update_contribution(
                    clean_contribution,
                    dirty_contribution,
                ),
            )
            for clean_contribution, dirty_contribution in zip(clean, dirty)
        ]
        deletes = [
            DeleteOne({"id": contribution.id.hex}) for contribution in deleted
        ]

        changes: list[InsertOne, UpdateOne, DeleteOne] = [
            *inserts,
            *updates,
            *deletes,
        ]
        if changes:
            await self._collection.bulk_write(
                requests=changes,
                session=self._session,
            )

    def _contribution_to_document(
        self,
        contribution: AddMovieContribution,
    ) -> dict[str, Any]:
        document = {
            "id": contribution.id.hex,
            "status": contribution.status,
            "author_id": contribution.author_id.hex,
            "eng_title": contribution.eng_title,
            "original_title": contribution.original_title,
            "summary": contribution.summary,
            "description": contribution.description,
            "release_date": contribution.release_date.isoformat(),
            "countries": list(contribution.countries),
            "genres": list(contribution.genres),
            "mpaa": contribution.mpaa,
            "duration": contribution.duration,
            "photos": list(contribution.photos),
        }

        if contribution.status_updated_at:
            document[
                "status_updated_at"
            ] = contribution.status_updated_at.isoformat()
        else:
            document["status_updated_at"] = None
        if contribution.budget:
            document["budget"] = {
                "amount": str(contribution.budget.amount),
                "currency": contribution.budget.currency,
            }
        else:
            document["budget"] = None
        if contribution.revenue:
            document["revenue"] = {
                "amount": str(contribution.revenue.amount),
                "currency": contribution.revenue.currency,
            }
        else:
            document["revenue"] = None

        document["roles"] = self._movie_roles_to_dicts(
            movie_roles=contribution.roles,
        )
        document["writers"] = self._movie_writers_to_dicts(
            movie_writers=contribution.writers,
        )
        document["crew"] = self._movie_crew_to_dicts(
            movie_crew=contribution.crew,
        )

        return document

    def _pipeline_to_update_contribution(
        self,
        clean: AddMovieContribution,
        dirty: AddMovieContribution,
    ) -> dict[str, Any]:
        pipeline = {"$set": {}}

        if clean.status != dirty.status:
            pipeline["$set"]["status"] = dirty.status
        if clean.status_updated_at != dirty.status_updated_at:
            if dirty.status_updated_at:
                pipeline["$set"][
                    "status_updated_at"
                ] = dirty.status_updated_at.isoformat()
            else:
                pipeline["$set"]["status_updated_at"] = None
        if clean.eng_title != dirty.eng_title:
            pipeline["$set"]["eng_title"] = dirty.eng_title
        if clean.original_title != dirty.original_title:
            pipeline["$set"]["original_title"] = dirty.original_title
        if clean.summary != dirty.summary:
            pipeline["$set"]["summary"] = dirty.summary
        if clean.description != dirty.description:
            pipeline["$set"]["description"] = dirty.description
        if clean.release_date != dirty.release_date:
            pipeline["$set"]["release_date"] = dirty.release_date.isoformat()
        if clean.countries != dirty.countries:
            pipeline["$set"]["countries"] = list(dirty.countries)
        if clean.genres != dirty.genres:
            pipeline["$set"]["genres"] = list(dirty.genres)
        if clean.mpaa != dirty.mpaa:
            pipeline["$set"]["mpaa"] = dirty.mpaa
        if clean.duration != dirty.duration:
            pipeline["$set"]["duration"] = dirty.duration
        if clean.budget != dirty.budget:
            if dirty.budget:
                pipeline["$set"]["budget"] = {
                    "amount": str(dirty.budget.amount),
                    "currency": dirty.budget.currency,
                }
            else:
                pipeline["$set"]["budget"] = None
        if clean.revenue != dirty.revenue:
            if dirty.revenue:
                pipeline["$set"]["revenue"] = {
                    "amount": str(dirty.revenue.amount),
                    "currency": dirty.revenue.currency,
                }
            else:
                pipeline["$set"]["revenue"] = None
        if clean.roles != dirty.roles:
            pipeline["$set"]["roles"] = self._movie_roles_to_dicts(dirty.roles)
        if clean.writers != dirty.writers:
            pipeline["$set"]["writers"] = self._movie_writers_to_dicts(
                dirty.writers,
            )
        if clean.crew != dirty.crew:
            pipeline["$set"]["crew"] = self._movie_crew_to_dicts(dirty.crew)
        if clean.photos != dirty.photos:
            pipeline["$set"]["photos"] = list(dirty.photos)

        return pipeline

    def _movie_roles_to_dicts(
        self,
        movie_roles: Iterable[MovieRole],
    ) -> list[dict[str, Any]]:
        movie_roles_as_dicts = []
        for movie_role in movie_roles:
            movie_role_as_dict = {
                "id": movie_role.id.hex,
                "person_id": movie_role.person_id.hex,
                "character": movie_role.character,
                "importance": movie_role.importance,
                "is_spoiler": movie_role.is_spoiler,
            }
            movie_roles_as_dicts.append(movie_role_as_dict)

        return movie_roles_as_dicts

    def _movie_writers_to_dicts(
        self,
        movie_writers: Iterable[MovieWriter],
    ) -> list[dict[str, Any]]:
        movie_writers_as_dicts = []
        for movie_writer in movie_writers:
            movie_writer_as_dict = {
                "id": movie_writer.id.hex,
                "person_id": movie_writer.person_id.hex,
                "writing": movie_writer.writing,
            }
            movie_writers_as_dicts.append(movie_writer_as_dict)

        return movie_writers_as_dicts

    def _movie_crew_to_dicts(
        self,
        movie_crew: Iterable[MovieCrewMember],
    ) -> list[dict[str, Any]]:
        movie_crew_as_dicts = []
        for movie_crew_member in movie_crew:
            movie_crew_member_as_dict = {
                "id": movie_crew_member.id.hex,
                "person_id": movie_crew_member.person_id.hex,
                "membership": movie_crew_member.membership,
            }
            movie_crew_as_dicts.append(movie_crew_member_as_dict)

        return movie_crew_as_dicts
