import logging
from datetime import datetime, timezone

from uuid_extensions import uuid7

from donation.domain import (
    AddPersonContributionId,
    UserIsNotActiveError,
    AddPerson,
)
from donation.application.common import (
    OperationId,
    AccessConcern,
    CommandProcessor,
    AuthorizationProcessor,
    TransactionProcessor,
    UserDoesNotExistError,
    NotEnoughPermissionsError,
    AddPersonContributionGateway,
    UserGateway,
    PermissionsGateway,
    UnitOfWork,
    IdentityProvider,
    OnEventOccurred,
    PersonAddedEvent,
)
from donation.application.commands import AddPersonCommand


logger = logging.getLogger(__name__)


def add_person_factory(
    operation_id: OperationId,
    add_person: AddPerson,
    access_concern: AccessConcern,
    add_person_contribution_gateway: AddPersonContributionGateway,
    user_gateway: UserGateway,
    permissions_gateway: PermissionsGateway,
    unit_of_work: UnitOfWork,
    identity_provider: IdentityProvider,
    on_person_added: OnEventOccurred[PersonAddedEvent],
) -> CommandProcessor[AddPersonCommand, AddPersonContributionId]:
    current_timestamp = datetime.now(timezone.utc)

    add_person_processor = AddPersonProcessor(
        add_person=add_person,
        add_person_contribution_gateway=add_person_contribution_gateway,
        user_gateway=user_gateway,
        identity_provider=identity_provider,
        current_timestamp=current_timestamp,
    )
    authz_processor = AuthorizationProcessor(
        processor=add_person_processor,
        access_concern=access_concern,
        permissions_gateway=permissions_gateway,
        identity_provider=identity_provider,
    )
    callback_processor = AddPersonCallbackProcessor(
        processor=authz_processor,
        identity_provider=identity_provider,
        on_person_added=on_person_added,
        current_timestamp=current_timestamp,
    )
    tx_processor = TransactionProcessor(
        processor=callback_processor,
        unit_of_work=unit_of_work,
    )
    log_processor = AddPersonLoggingProcessor(
        processor=tx_processor,
        operation_id=operation_id,
        identity_provider=identity_provider,
    )

    return log_processor


class AddPersonProcessor:
    def __init__(
        self,
        *,
        add_person: AddPerson,
        add_person_contribution_gateway: AddPersonContributionGateway,
        user_gateway: UserGateway,
        identity_provider: IdentityProvider,
        current_timestamp: datetime,
    ):
        self._add_person = add_person
        self._add_person_contribution_gateway = add_person_contribution_gateway
        self._user_gateway = user_gateway
        self._identity_provider = identity_provider
        self._current_timestamp = current_timestamp

    async def process(
        self,
        command: AddPersonCommand,
    ) -> AddPersonContributionId:
        current_user_id = await self._identity_provider.user_id()

        author = await self._user_gateway.by_id(current_user_id)
        if not author:
            raise UserDoesNotExistError()

        contribution = self._add_person(
            id=AddPersonContributionId(uuid7()),
            author=author,
            first_name=command.first_name,
            last_name=command.last_name,
            sex=command.sex,
            birth_date=command.birth_date,
            death_date=command.death_date,
            photos=command.photos,
            current_timestamp=self._current_timestamp,
        )
        await self._add_person_contribution_gateway.save(contribution)

        return contribution.id


class AddPersonCallbackProcessor:
    def __init__(
        self,
        *,
        processor: AuthorizationProcessor,
        identity_provider: IdentityProvider,
        on_person_added: OnEventOccurred[PersonAddedEvent],
        current_timestamp: datetime,
    ):
        self._processor = processor
        self._identity_provider = identity_provider
        self._on_person_added = on_person_added
        self._current_timestamp = current_timestamp

    async def process(
        self,
        command: AddPersonCommand,
    ) -> AddPersonContributionId:
        result = await self._processor.process(command)
        current_user_id = await self._identity_provider.user_id()

        event = PersonAddedEvent(
            contribtion_id=result,
            author_id=current_user_id,
            first_name=command.first_name,
            last_name=command.last_name,
            sex=command.sex,
            birth_date=command.birth_date,
            death_date=command.death_date,
            photos=command.photos,
            added_at=self._current_timestamp,
        )
        await self._on_person_added(event)

        return result


class AddPersonLoggingProcessor:
    def __init__(
        self,
        *,
        processor: TransactionProcessor,
        operation_id: OperationId,
        identity_provider: IdentityProvider,
    ):
        self._processor = processor
        self._operation_id = operation_id
        self._identity_provider = identity_provider

    async def process(
        self,
        command: AddPersonCommand,
    ) -> AddPersonContributionId:
        current_user_id = await self._identity_provider.user_id()

        logger.debug(
            msg="'Add Person' command processing started",
            extra={
                "operation_id": self._operation_id,
                "user_id": current_user_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except NotEnoughPermissionsError as error:
            logger.info(
                "Expected error occurred: User has not enough permissions",
                extra={
                    "operation_id": self._operation_id,
                    "current_user_permissions": (
                        await self._identity_provider.permissions()
                    ),
                },
            )
            raise error
        except UserDoesNotExistError as error:
            logger.error(
                "Unexpected error occurred: "
                "User is authenticated, but user gateway returns None",
                extra={"operation_id": self._operation_id},
            )
            raise error
        except UserIsNotActiveError as error:
            logger.debug(
                "Expected error occurred: User is not active",
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
            msg="'Add Person' command processing completed",
            extra={
                "operation_id": self._operation_id,
                "contribution_id": result,
            },
        )

        return result
