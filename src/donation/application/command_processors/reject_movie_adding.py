import logging
from typing import Optional

from uuid_extensions import uuid7

from donation.domain import (
    AchievementId,
    RejectContribution,
)
from donation.application.common import (
    OperationId,
    CommandProcessor,
    TransactionProcessor,
    AchievementEearnedCallbackProcessor,
    UserDoesNotExistError,
    ContributionDoesNotExistError,
    AchievementDoesNotExistError,
    AddMovieContributionGateway,
    UserGateway,
    AchievementGateway,
    UnitOfWork,
    OnEventOccurred,
    AchievementEarnedEvent,
)
from donation.application.commands import RejectMovieAddingCommand


logger = logging.getLogger(__name__)


def reject_movie_adding_factory(
    operation_id: OperationId,
    reject_contribution: RejectContribution,
    add_movie_contribution_gateway: AddMovieContributionGateway,
    user_gateway: UserGateway,
    achievement_gateway: AchievementGateway,
    unit_of_work: UnitOfWork,
    on_achievement_earned: OnEventOccurred[AchievementEarnedEvent],
) -> CommandProcessor[RejectMovieAddingCommand, Optional[AchievementId]]:
    reject_movie_adding_processor = RejectMovieAddingProcessor(
        reject_contribution=reject_contribution,
        add_movie_contribution_gateway=add_movie_contribution_gateway,
        user_gateway=user_gateway,
        achievement_gateway=achievement_gateway,
    )
    callback_processor = AchievementEearnedCallbackProcessor(
        processor=reject_movie_adding_processor,
        achievement_gateway=achievement_gateway,
        on_achievement_earned=on_achievement_earned,
    )
    tx_processor = TransactionProcessor(
        processor=callback_processor,
        unit_of_work=unit_of_work,
    )
    log_processor = RejectMovieAddingLoggingProcessor(
        processor=tx_processor,
        operation_id=operation_id,
    )

    return log_processor


class RejectMovieAddingProcessor:
    def __init__(
        self,
        *,
        reject_contribution: RejectContribution,
        add_movie_contribution_gateway: AddMovieContributionGateway,
        user_gateway: UserGateway,
        achievement_gateway: AchievementGateway,
    ):
        self._reject_contribution = reject_contribution
        self._add_movie_contribution_gateway = add_movie_contribution_gateway
        self._user_gateway = user_gateway
        self._achievement_gateway = achievement_gateway

    async def process(
        self,
        command: RejectMovieAddingCommand,
    ) -> Optional[AchievementId]:
        contribution = (
            await self._add_movie_contribution_gateway.acquire_by_id(
                id=command.contribution_id,
            )
        )
        if not contribution:
            raise ContributionDoesNotExistError()

        author = await self._user_gateway.acquire_by_id(
            id=contribution.author_id,
        )
        if not author:
            raise UserDoesNotExistError()

        achievement = self._reject_contribution(
            achievement_id=AchievementId(uuid7()),
            contribution=contribution,
            author=author,
            current_timestamp=command.rejected_at,
        )
        if achievement:
            await self._achievement_gateway.save(achievement)

        await self._user_gateway.update(author)
        await self._add_movie_contribution_gateway.update(contribution)

        return achievement.id if achievement else None


class RejectMovieAddingLoggingProcessor:
    def __init__(
        self,
        *,
        processor: TransactionProcessor,
        operation_id: OperationId,
    ):
        self._processor = processor
        self._operation_id = operation_id

    async def process(
        self,
        command: RejectMovieAddingCommand,
    ) -> Optional[AchievementId]:
        logger.debug(
            "'Reject Movie Adding' command processing started",
            extra={
                "operation_id": self._operation_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except ContributionDoesNotExistError as error:
            logger.error(
                "Unexpected error occurred: Contribution doesn't exist",
                extra={"operation_id": self._operation_id},
            )
            raise error
        except UserDoesNotExistError as error:
            logger.error(
                "Unexpected error occurred: Contribution has author id, "
                "using which user gateway returns None",
                extra={"operation_id": self._operation_id},
            )
            raise error
        except AchievementDoesNotExistError as error:
            logger.error(
                "Unexpected error occurred: Achievement was created, "
                "but achievement gateway returns None",
                extra={"operation_id": self._operation_id},
            )
            raise error
        except Exception as error:
            logger.exception(
                "Unexpected error occurred",
                extra={"operation_id": self._operation_id},
            )
            raise error

        logger.debug(
            "'Reject Movie Adding' command processing completed",
            extra={
                "operation_id": self._operation_id,
                "achievement_id": result,
            },
        )

        return result
