from donation.domain.constants import Writing
from donation.domain.entities import Writer
from donation.domain.maybe import Maybe


class UpdateWriter:
    def __call__(
        self,
        writer: Writer,
        *,
        writing: Maybe[Writing],
    ) -> None:
        if writing.is_set:
            writer.writing = writing.value
