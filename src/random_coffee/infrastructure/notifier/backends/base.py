from typing import Protocol, Any, Iterable


class NotifierBackend(Protocol):
    def get_enum_value(self) -> str:
        """
        Get enum type method

        :return:
            String, that matches enum member of `NotifierBackendEnum`.
        """
        raise NotImplementedError()

    def send_notification(
            self,
            internal_destination_identifier: str,
            notification_content: Any,
            priority: int | None = None
    ) -> Any:
        """
        Send notification method

        :param internal_destination_identifier:
            identifier of send destination within a notifier. the actual meaning
            of this value is notifier implementation detail.
        :param notification_content:
            the text of the notification to be sent.
        :param priority:
            priority of sending against other requests.
        :return:
            backend response
        """

        raise NotImplementedError()

    def broadcast_notification(
            self,
            internal_destination_identifiers: Iterable[str],
            notification_content: Any,
            priority: int | None = None
    ) -> Any:
        """
        Broadcast notification method

        Semantically equivalent to call `NotifierBackend.send_notification` several times
        with same notification content but different internal destination identifiers.
        As common use case that cause bottlenecks, implementation can contain optimisations.

        :param internal_destination_identifiers:
            identifiers of send destinations within a notifier. the actual meaning
            of this value is notifier implementation detail.  order of supplying is
            not ensured.
        :param notification_content:
            the text of the notification to be sent.
        :param priority:
            priority of sending against other requests.
        :return:
            backend response
        """

        raise NotImplementedError()
